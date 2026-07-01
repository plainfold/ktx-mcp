#!/usr/bin/env python3
"""Download Korail KTX line stations CSV (data.go.kr 15127571) and build sync inputs."""

from __future__ import annotations

import argparse
import csv
import io
import json
import sys
import zipfile
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

DATASET_PK = "15127571"
UDDI = "uddi:ab540482-aa65-411d-908b-c961aadae08b"
RAW_DIR = ROOT / "src" / "ktx_mcp" / "data" / "raw"
OUTPUT_LINES = ROOT / "src" / "ktx_mcp" / "data" / "ktx_line_stations.json"
OUTPUT_PRIORITY = ROOT / "src" / "ktx_mcp" / "data" / "priority_station_codes.json"


def _download_csv_bytes() -> bytes:
    meta = httpx.get(
        "https://www.data.go.kr/tcs/dss/selectFileDataDownload.do",
        params={"publicDataPk": DATASET_PK, "fileDetailSn": "1"},
        timeout=60,
    )
    meta.raise_for_status()
    payload = meta.json()
    atch = payload.get("atchFileId") or payload.get("dataSetFileDetailInfo", {}).get("atchFileId")
    if not atch:
        raise RuntimeError("atchFileId not found in file metadata")

    file_resp = httpx.get(
        "https://www.data.go.kr/cmm/cmm/fileDownload.do",
        params={"atchFileId": atch},
        timeout=120,
        follow_redirects=True,
    )
    file_resp.raise_for_status()
    content = file_resp.content
    if content[:2] == b"PK":
        with zipfile.ZipFile(io.BytesIO(content)) as archive:
            names = [name for name in archive.namelist() if name.lower().endswith(".csv")]
            if not names:
                raise RuntimeError("zip has no csv")
            return archive.read(names[0])
    return content


def _decode_csv(raw: bytes) -> str:
    for encoding in ("utf-8-sig", "cp949", "euc-kr"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def parse_korail_lines(csv_text: str) -> dict:
    reader = csv.DictReader(io.StringIO(csv_text))
    if not reader.fieldnames:
        raise RuntimeError("CSV has no header")

    # Normalize header keys
    rows = []
    for row in reader:
        normalized = {key.strip(): (value or "").strip() for key, value in row.items() if key}
        if any(normalized.values()):
            rows.append(normalized)

    # Detect column names (Korail CSV varies slightly by revision)
    sample = rows[0]
    line_key = next((k for k in sample if "노선" in k), "노선명")
    station_key = next(
        (k for k in sample if k in {"역명", "역 명", "역이름"} or "역명" in k),
        "역명",
    )
    order_key = next((k for k in sample if "순번" in k or "순서" in k), "역순번")

    lines: dict[str, list[dict]] = {}
    for row in rows:
        line_name = row.get(line_key, "")
        station_name = row.get(station_key, "")
        if not line_name or not station_name:
            continue
        order_raw = row.get(order_key, "0")
        try:
            order = int(float(order_raw))
        except ValueError:
            order = len(lines.get(line_name, [])) + 1
        entry = {
            "station_name": station_name,
            "order": order,
            "source": "korail_file_15127571",
        }
        for key, value in row.items():
            if key in {line_key, station_key, order_key} or not value:
                continue
            entry[key] = value
        lines.setdefault(line_name, []).append(entry)

    for stations in lines.values():
        stations.sort(key=lambda item: item["order"])

    return {
        "_meta": {
            "source": "data.go.kr/15127571",
            "dataset": "한국철도공사_KTX 노선별 역정보",
            "note": "Line order from Korail file; nodeid from TAGO at build time.",
        },
        "lines": lines,
    }


def _match_tago_nodeids(line_data: dict) -> tuple[dict, list[str]]:
    from ktx_mcp.adapters.tago_client import fetch_all_stations, load_service_key
    from ktx_mcp.data.korail_lines_loader import match_korail_name_to_tago

    service_key = load_service_key()
    tago_rows = fetch_all_stations(service_key)
    by_name: dict[str, list[str]] = {}
    for row in tago_rows:
        by_name.setdefault(row["canonical"], []).append(row["code"])

    missing: list[str] = []
    for _line, stations in line_data["lines"].items():
        for station in stations:
            name = station["station_name"]
            nodeid, tago_name = match_korail_name_to_tago(name, by_name)
            if nodeid:
                station["nodeid"] = nodeid
                station["tago_nodename"] = tago_name
                if tago_name != name:
                    station["korail_name"] = name
            else:
                missing.append(name)

    return line_data, sorted(set(missing))


def _adjacent_routes(line_data: dict) -> list[dict]:
    routes: list[dict] = []
    seen: set[tuple[str, str]] = set()
    for line_name, stations in line_data["lines"].items():
        with_code = [s for s in stations if s.get("nodeid")]
        for left, right in zip(with_code, with_code[1:], strict=False):
            dep, arr = left["nodeid"], right["nodeid"]
            key = (dep, arr)
            if key in seen:
                continue
            seen.add(key)
            routes.append(
                {
                    "dep_code": dep,
                    "arr_code": arr,
                    "dep_name": left["station_name"],
                    "arr_name": right["station_name"],
                    "line": line_name,
                    "source": "korail_file_15127571",
                }
            )
    return routes


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skip-tago", action="store_true")
    args = parser.parse_args()

    print("Downloading Korail KTX line stations (15127571) ...")
    raw = _download_csv_bytes()
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    raw_path = RAW_DIR / "korail_ktx_line_stations.csv"
    raw_path.write_bytes(raw)

    csv_text = _decode_csv(raw)
    line_data = parse_korail_lines(csv_text)
    print(f"Parsed lines: {len(line_data['lines'])}")

    missing: list[str] = []
    if not args.skip_tago:
        try:
            line_data, missing = _match_tago_nodeids(line_data)
        except Exception as exc:  # noqa: BLE001
            print(f"TAGO match skipped: {exc}", file=sys.stderr)

    routes = _adjacent_routes(line_data)
    line_data["adjacent_routes"] = routes

    nodeids: list[str] = []
    seen_nodes: set[str] = set()
    for stations in line_data["lines"].values():
        for station in stations:
            nodeid = station.get("nodeid")
            if nodeid and nodeid not in seen_nodes:
                seen_nodes.add(nodeid)
                nodeids.append(nodeid)

    # SRT 수서 — not listed in Korail KTX line file (15127571)
    from ktx_mcp.data.korail_lines_loader import SUSEO_CODE

    if SUSEO_CODE not in seen_nodes:
        nodeids.append(SUSEO_CODE)

    if args.dry_run:
        summary = {
            "lines": list(line_data["lines"].keys()),
            "stations": len(nodeids),
            "routes": len(routes),
        }
        print(json.dumps(summary, ensure_ascii=False))
        if missing:
            print("missing TAGO:", ", ".join(missing[:20]))
        return 0

    OUTPUT_LINES.write_text(
        json.dumps(line_data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    priority = {
        "_meta": {
            "source": "data.go.kr/15127571 + TAGO nodeid match",
            "description": "KTX line stations from Korail official file; codes from TAGO.",
        },
        "priority_nodeids": nodeids,
    }
    OUTPUT_PRIORITY.write_text(
        json.dumps(priority, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {OUTPUT_LINES}")
    print(f"Wrote {OUTPUT_PRIORITY} ({len(nodeids)} nodeids, {len(routes)} adjacent routes)")
    if missing:
        print("Warning: TAGO nodename not found:", ", ".join(missing), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
