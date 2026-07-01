#!/usr/bin/env python3
"""Print KTX stations grouped by region (TAGO city_name) and by Korail line."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "src" / "ktx_mcp" / "data"


def main() -> int:
    stations = json.loads((DATA / "stations_i18n.json").read_text(encoding="utf-8"))
    lines = json.loads((DATA / "ktx_line_stations.json").read_text(encoding="utf-8"))

    st_to_lines: dict[str, set[str]] = defaultdict(set)
    for line_name, stns in lines["lines"].items():
        for st in stns:
            if st.get("nodeid"):
                st_to_lines[st["nodeid"]].add(line_name)

    by_region: dict[str, list[dict]] = defaultdict(list)
    for row in stations:
        by_region[row["city_name"]].append(row)

    region_order = [
        "서울특별시",
        "경기도",
        "인천광역시",
        "강원도",
        "충청북도",
        "충청남도",
        "대전광역시",
        "세종특별자치시",
        "광주광역시",
        "전라북도",
        "전라남도",
        "대구광역시",
        "경상북도",
        "울산광역시",
        "경상남도",
        "부산광역시",
    ]

    print("=" * 60)
    print("TAGO 행정구역별 KTX 역 (70역)")
    print("=" * 60)

    seen: set[str] = set()
    for region in region_order + sorted(set(by_region) - set(region_order)):
        if region not in by_region:
            continue
        seen.add(region)
        rows = sorted(by_region[region], key=lambda item: item["canonical"])
        print(f"\n[{region}] {len(rows)}역")
        for s in rows:
            line_names = ", ".join(sorted(st_to_lines.get(s["code"], []))) or "-"
            print(f"  {s['canonical']}\t{s['code']}\t노선: {line_names}")

    print("\n" + "=" * 60)
    print("KTX 노선별 정차역 (15127571)")
    print("=" * 60)

    for line_name, stns in lines["lines"].items():
        print(f"\n[{line_name}] {len(stns)}역")
        for st in stns:
            tago = st.get("tago_nodename") or st["station_name"]
            code = st.get("nodeid", "-")
            korail = st["station_name"]
            note = f"  (Korail표기: {korail})" if korail != tago else ""
            print(f"  {st['order']:>2}. {tago}\t{code}{note}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
