from __future__ import annotations

import json
from functools import lru_cache
from importlib import resources
from typing import Any


@lru_cache(maxsize=1)
def load_station_aliases() -> dict[str, dict[str, Any]]:
    raw = resources.files("ktx_mcp.data").joinpath("station_aliases.json").read_text(
        encoding="utf-8"
    )
    table = json.loads(raw)
    return {key: value for key, value in table.items() if not key.startswith("_")}


def tago_name_for(display_name: str, row: dict[str, Any] | None = None) -> str:
    """TAGO API `nodename` used to resolve `nodeid` for this display station."""
    if row is not None:
        explicit = row.get("tago_name")
        if explicit:
            return str(explicit)
    return display_name


def priority_station_names() -> list[str]:
    return list(load_station_aliases().keys())
