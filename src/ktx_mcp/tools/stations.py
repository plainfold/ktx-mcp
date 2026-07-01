from __future__ import annotations

import json
from functools import lru_cache
from importlib import resources
from typing import Any

from ktx_mcp.models.station import StationMatch
from ktx_mcp.tools.common import normalize_locale, tool_envelope


@lru_cache(maxsize=1)
def _load_station_catalog() -> list[dict[str, Any]]:
    raw = resources.files("ktx_mcp.data").joinpath("stations_i18n.json").read_text(encoding="utf-8")
    return json.loads(raw)


def _score_match(query: str, candidate: str) -> float:
    q = query.strip().casefold()
    c = candidate.strip().casefold()
    if not q or not c:
        return 0.0
    if q == c:
        return 1.0
    if q in c or c in q:
        return 0.85
    return 0.0


def search_stations_payload(query: str, locale: str = "en") -> dict[str, Any]:
    loc = normalize_locale(locale)
    catalog = _load_station_catalog()
    ranked: list[StationMatch] = []

    for entry in catalog:
        name = str(entry["canonical"])
        score = _score_match(query, name)
        if score > 0:
            ranked.append(
                StationMatch(
                    station_name=name,
                    station_code=entry["code"],
                    score=score,
                )
            )

    ranked.sort(key=lambda item: (-item.score, item.station_name))
    matches = [match.model_dump(exclude={"score"}) for match in ranked[:5]]

    summary = (
        f"Found {len(matches)} station(s) for '{query}'."
        if matches
        else f"No stations matched '{query}'. Use TAGO nodename (Korean) or nodeid (NAT...)."
    )
    return tool_envelope(
        {
            "matches": matches,
            "summary": summary,
            "error": None if matches else "STATION_NOT_FOUND",
        },
        locale=loc,
    )


def resolve_station_code(name_or_code: str) -> str | None:
    value = name_or_code.strip()
    if value.upper().startswith("NAT"):
        return value.upper()

    payload = search_stations_payload(value, locale="ko")
    matches = payload.get("matches") or []
    if not matches:
        return None
    return str(matches[0]["station_code"])
