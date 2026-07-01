from __future__ import annotations

import json
from functools import lru_cache
from importlib import resources


@lru_cache(maxsize=1)
def load_priority_nodeids() -> list[str]:
    raw = resources.files("ktx_mcp.data").joinpath("priority_station_codes.json").read_text(
        encoding="utf-8"
    )
    table = json.loads(raw)
    nodeids = table.get("priority_nodeids", [])
    return [str(nodeid).strip() for nodeid in nodeids if str(nodeid).strip()]
