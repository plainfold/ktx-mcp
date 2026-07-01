#!/usr/bin/env python3
"""Build stations_i18n.json from official TAGO APIs + station_aliases.json.

TAGO TrainInfo (data.go.kr 15098552):
  - GetCtyCodeList
  - GetCtyAcctoTrainSttnList?cityCode=11

  nodeid  → stations_i18n.code
  nodename → matched via station_aliases.json `tago_name` when set

  en/ja/zh/ko → station_aliases.json only (not in TAGO API)

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

from ktx_mcp.adapters.tago_client import TagoApiError, fetch_all_stations, load_service_key  # noqa: E402
from ktx_mcp.data.station_aliases_loader import (  # noqa: E402
    load_station_aliases,
    priority_station_names,
    tago_name_for,
)

DATA_DIR = ROOT / "src" / "ktx_mcp/data"
OUTPUT_PATH = DATA_DIR / "stations_i18n.json"


def _build_entry(
    display_name: str,
    station: dict[str, str],
    alias_row: dict,
) -> dict:
    tago_name = tago_name_for(display_name, alias_row)
    entry: dict = {
        "canonical": display_name,
        "code": station["code"],
        "aliases": {
            "en": alias_row.get("en", []),
            "ja": alias_row.get("ja", []),
            "zh": alias_row.get("zh", []),
        },
    }
    if tago_name != display_name:
        entry["tago_name"] = tago_name
    ko = alias_row.get("ko")
    if ko:
        entry["aliases"]["ko"] = ko
    note = alias_row.get("note")
    if note:
        entry["note"] = note
    return entry


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

    alias_table = load_station_aliases()
    by_tago_name = {row["canonical"]: row for row in stations}

    if args.all:
        selected: list[tuple[str, dict[str, str]]] = [
            (row["canonical"], row) for row in stations
        ]
    else:
        selected = []
        missing: list[str] = []
        for display_name in priority_station_names():
            alias_row = alias_table[display_name]
            lookup = tago_name_for(display_name, alias_row)
            row = by_tago_name.get(lookup)
            if row:
                selected.append((display_name, row))
            else:
                missing.append(f"{display_name}→{lookup}")
        if missing:
            print("Warning: TAGO nodename not found:", ", ".join(missing), file=sys.stderr)

    entries = [
        _build_entry(name, row, alias_table.get(name, {}))
        for name, row in selected
    ]
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
