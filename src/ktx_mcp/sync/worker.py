from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from ktx_mcp.adapters.tago import TagoGateway
from ktx_mcp.store.timetable import TimetableStore

KST = ZoneInfo("Asia/Seoul")

DEFAULT_SYNC_ROUTES: list[tuple[str, str, str]] = [
    ("NAT010000", "NAT014445", "Seoul-Busan"),
    ("NATH30000", "NAT014445", "Suseo-Busan"),
    ("NAT010000", "NAT013271", "Seoul-Dongdaegu"),
    ("NAT011668", "NAT013271", "Daejeon-Dongdaegu"),
]


@dataclass(slots=True)
class SyncResult:
    status: str
    tago_calls: int = 0
    routes_synced: int = 0
    rows_upserted: int = 0
    travel_dates: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


class SyncWorker:
    def __init__(self, store: TimetableStore, tago: TagoGateway | None) -> None:
        self._store = store
        self._tago = tago

    async def run(
        self,
        *,
        routes: list[tuple[str, str, str]] | None = None,
        travel_dates: list[str] | None = None,
    ) -> SyncResult:
        if self._tago is None:
            return SyncResult(status="skipped", errors=["TAGO key not configured"])

        routes = routes or DEFAULT_SYNC_ROUTES
        travel_dates = travel_dates or _default_travel_dates()
        result = SyncResult(status="running", travel_dates=travel_dates)

        for dep_code, arr_code, _label in routes:
            for travel_date in travel_dates:
                try:
                    rows = await self._tago.fetch_route(dep_code, arr_code, travel_date)
                    upserted = await self._store.upsert_many(rows)
                    result.tago_calls += 1
                    result.rows_upserted += upserted
                    result.routes_synced += 1
                except Exception as exc:  # noqa: BLE001 — sync worker aggregates per-route errors
                    result.errors.append(f"{dep_code}->{arr_code}@{travel_date}: {exc}")

        result.status = "ok" if not result.errors else "partial"
        return result


def _default_travel_dates() -> list[str]:
    today = datetime.now(KST).date()
    tomorrow = today + timedelta(days=1)
    return [today.strftime("%Y%m%d"), tomorrow.strftime("%Y%m%d")]
