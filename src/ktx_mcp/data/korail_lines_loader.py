from __future__ import annotations

import json
import re
from functools import lru_cache
from importlib import resources

SEOUL_CODE = "NAT010000"
SUSEO_CODE = "NATH30000"
BUSAN_CODE = "NAT014445"

_PAREN_SUFFIX = re.compile(r"^(.+?)\(.+\)$")


@lru_cache(maxsize=1)
def load_ktx_line_stations() -> dict:
    raw = resources.files("ktx_mcp.data").joinpath("ktx_line_stations.json").read_text(
        encoding="utf-8"
    )
    return json.loads(raw)


def korail_station_name_candidates(korail_name: str) -> list[str]:
    """Map Korail file (15127571) station label to TAGO nodename candidates."""
    name = korail_name.strip()
    candidates = [name]
    match = _PAREN_SUFFIX.match(name)
    if match:
        candidates.append(match.group(1).strip())
    return candidates


def match_korail_name_to_tago(
    korail_name: str,
    by_name: dict[str, list[str]],
) -> tuple[str | None, str | None]:
    for candidate in korail_station_name_candidates(korail_name):
        codes = by_name.get(candidate, [])
        if codes:
            return codes[0], candidate
    return None, None


def route_label(dep_code: str, arr_code: str, names_by_code: dict[str, str]) -> str:
    dep = names_by_code.get(dep_code, dep_code)
    arr = names_by_code.get(arr_code, arr_code)
    return f"{dep}-{arr}"


def _names_by_code_from_lines(data: dict) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for stations in data.get("lines", {}).values():
        for station in stations:
            nodeid = station.get("nodeid")
            tago_name = station.get("tago_nodename") or station.get("station_name")
            if nodeid and tago_name:
                mapping[nodeid] = tago_name
    return mapping


@lru_cache(maxsize=1)
def _names_from_stations_catalog() -> dict[str, str]:
    raw = resources.files("ktx_mcp.data").joinpath("stations_i18n.json").read_text(encoding="utf-8")
    entries = json.loads(raw)
    return {entry["code"]: entry["canonical"] for entry in entries}


def build_sync_routes() -> list[tuple[str, str, str]]:
    """Sync routes from Korail KTX line file (15127571) adjacent pairs + SRT supplement."""
    data = load_ktx_line_stations()
    names_by_code = _names_by_code_from_lines(data)
    names_by_code.update(_names_from_stations_catalog())
    routes: list[tuple[str, str, str]] = []
    seen: set[tuple[str, str]] = set()

    for item in data.get("adjacent_routes", []):
        dep_code = item["dep_code"]
        arr_code = item["arr_code"]
        key = (dep_code, arr_code)
        if key in seen:
            continue
        seen.add(key)
        label = route_label(dep_code, arr_code, names_by_code)
        routes.append((dep_code, arr_code, label))

    supplemental = (SUSEO_CODE, BUSAN_CODE)
    if supplemental not in seen:
        routes.append(
            (
                SUSEO_CODE,
                BUSAN_CODE,
                route_label(SUSEO_CODE, BUSAN_CODE, names_by_code),
            )
        )

    routes.sort(key=lambda item: item[2])
    return routes


DEFAULT_SYNC_ROUTES: list[tuple[str, str, str]] = build_sync_routes()
