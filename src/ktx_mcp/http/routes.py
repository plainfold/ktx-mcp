from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass

from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from ktx_mcp.config import Settings
from ktx_mcp.store.postgres import PostgresTimetableStore
from ktx_mcp.store.timetable import TimetableStore
from ktx_mcp.sync.worker import SyncWorker


@dataclass(slots=True)
class HttpState:
    settings: Settings
    timetable_store: TimetableStore
    sync_worker: SyncWorker


def make_health_handler(state: HttpState) -> Callable[[Request], Response]:
    async def health_handler(request: Request) -> Response:
        store = state.timetable_store
        row_count = await store.count_rows()
        if isinstance(store, PostgresTimetableStore):
            try:
                await store.ping()
                database = "connected"
            except Exception as exc:  # noqa: BLE001 — health must surface DB errors
                return JSONResponse(
                    {
                        "status": "degraded",
                        "store": "postgres",
                        "database": "error",
                        "database_error": str(exc),
                        "row_count": row_count,
                        "transport": state.settings.transport,
                    },
                    status_code=503,
                )
            store_name = "postgres"
        else:
            store_name = "in_memory"
            database = "not_configured"

        return JSONResponse(
            {
                "status": "ok",
                "store": store_name,
                "row_count": row_count,
                "transport": state.settings.transport,
                "database": database,
            }
        )

    return health_handler


def make_sync_handler(state: HttpState) -> Callable[[Request], Response]:
    async def sync_handler(request: Request) -> Response:
        if not state.settings.sync_secret:
            return JSONResponse(
                {"status": "error", "message": "SYNC_SECRET not configured"},
                status_code=503,
            )

        provided = request.headers.get("X-Sync-Secret", "")
        if provided != state.settings.sync_secret:
            return JSONResponse({"status": "error", "message": "Unauthorized"}, status_code=401)

        body: dict = {}
        if request.headers.get("content-type", "").startswith("application/json"):
            try:
                body = await request.json()
            except json.JSONDecodeError:
                body = {}

        travel_dates = body.get("travel_dates")
        if travel_dates is not None and not isinstance(travel_dates, list):
            return JSONResponse(
                {"status": "error", "message": "travel_dates must be a list"},
                status_code=400,
            )

        result = await state.sync_worker.run(travel_dates=travel_dates)
        status_code = 200 if result.status in {"ok", "partial", "skipped"} else 500
        return JSONResponse(
            {
                "status": result.status,
                "tago_calls": result.tago_calls,
                "routes_synced": result.routes_synced,
                "rows_upserted": result.rows_upserted,
                "travel_dates": result.travel_dates,
                "errors": result.errors,
            },
            status_code=status_code,
        )

    return sync_handler
