#!/usr/bin/env python3
"""Run TAGO sync into the configured timetable store."""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ktx_mcp.adapters.tago import TagoGateway  # noqa: E402
from ktx_mcp.config import Settings  # noqa: E402
from ktx_mcp.store.factory import create_timetable_store  # noqa: E402
from ktx_mcp.store.postgres import PostgresTimetableStore  # noqa: E402
from ktx_mcp.sync.worker import SyncWorker  # noqa: E402


async def run_sync(travel_dates: list[str] | None) -> int:
    settings = Settings.from_env()
    store = create_timetable_store(settings.database_url)
    tago = TagoGateway(settings.tago_service_key) if settings.tago_service_key else None
    worker = SyncWorker(store, tago)

    try:
        result = await worker.run(travel_dates=travel_dates)
    finally:
        if isinstance(store, PostgresTimetableStore):
            await store.close()

    print(json.dumps({
        "status": result.status,
        "tago_calls": result.tago_calls,
        "routes_synced": result.routes_synced,
        "rows_upserted": result.rows_upserted,
        "travel_dates": result.travel_dates,
        "errors": result.errors,
    }, ensure_ascii=False, indent=2))

    return 0 if result.status in {"ok", "partial"} and result.tago_calls > 0 else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync TAGO timetables to store")
    parser.add_argument(
        "--dates",
        nargs="*",
        help="Travel dates YYYYMMDD (default: today and tomorrow KST)",
    )
    args = parser.parse_args()
    try:
        return asyncio.run(run_sync(args.dates or None))
    except Exception as exc:  # noqa: BLE001
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
