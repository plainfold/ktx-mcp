#!/usr/bin/env python3
"""Build stations_i18n.json from TAGO TrainInfo API only.

TAGO (data.go.kr 15098552):
  GetCtyCodeList → GetCtyAcctoTrainSttnList

  nodeid   → code
  nodename → canonical (only trusted name field)

Usage:
  python scripts/build_stations.py
  python scripts/build_stations.py --all
  python scripts/build_stations.py --dry-run
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ktx_mcp.adapters.tago_client import (  # noqa: E402
    TagoApiError,
    fetch_all_stations,
    load_service_key,
)
from ktx_mcp.data.priority_stations_loader import load_priority_nodeids  # noqa: E402

DATA_DIR = ROOT / "src" / "ktx_mcp/data"
OUTPUT_PATH = DATA_DIR / "stations_i18n.json"


def _build_entry(station: dict[str, str]) -> dict:
    return {
        "canonical": station["canonical"],
        "code": station["code"],
        "city_code": station.get("city_code", ""),
        "city_name": station.get("city_name", ""),
        "source": "tago",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build stations_i18n.json from TAGO API")
    parser.add_argument("--all", action="store_true", help="Include all TAGO stations")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    try:
        service_key = load_service_key()
    except TagoApiError as exc:
        print(exc, file=sys.stderr)
        return 1

    print("Fetching stations from TAGO TrainInfo API ...")
    try:
        stations = fetch_all_stations(service_key)
    except TagoApiError as exc:
        print(exc, file=sys.stderr)
        return 2

    by_code = {row["code"]: row for row in stations}

    if args.all:
        selected = [row for row in stations]
    else:
        selected = []
        missing: list[str] = []
        for nodeid in load_priority_nodeids():
            row = by_code.get(nodeid)
            if row:
                selected.append(row)
            else:
                missing.append(nodeid)
        if missing:
            print("Warning: TAGO nodeid not found:", ", ".join(missing), file=sys.stderr)

    entries = [_build_entry(row) for row in selected]
    entries.sort(key=lambda item: item["canonical"])

    print(f"TAGO stations total: {len(stations)}")
    print(f"Writing: {len(entries)} entries -> {OUTPUT_PATH}")

    if args.dry_run:
        for entry in entries[:5]:
            print(json.dumps(entry, ensure_ascii=False))
        return 0

    OUTPUT_PATH.write_text(
        json.dumps(entries, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
