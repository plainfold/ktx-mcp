#!/usr/bin/env python3
"""Upsert v1 sync routes into sync_routes table."""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ktx_mcp.config import Settings  # noqa: E402
from ktx_mcp.sync.routes import DEFAULT_SYNC_ROUTES  # noqa: E402

_UPSERT = """
INSERT INTO sync_routes (dep_code, arr_code, priority, label)
VALUES ($1, $2, $3, $4)
ON CONFLICT (dep_code, arr_code)
DO UPDATE SET priority = EXCLUDED.priority, label = EXCLUDED.label
"""


async def main_async() -> int:
    settings = Settings.from_env()
    if not settings.database_url:
        print("DATABASE_URL is not set", file=sys.stderr)
        return 1

    import asyncpg

    conn = await asyncpg.connect(
        settings.database_url,
        ssl="require" if "supabase.co" in settings.database_url else False,
    )
    try:
        valid = {(dep_code, arr_code) for dep_code, arr_code, _label in DEFAULT_SYNC_ROUTES}
        for index, (dep_code, arr_code, label) in enumerate(DEFAULT_SYNC_ROUTES, start=1):
            priority = min(index * 10, 999)
            await conn.execute(_UPSERT, dep_code, arr_code, priority, label)

        for row in await conn.fetch("SELECT dep_code, arr_code FROM sync_routes"):
            key = (row["dep_code"], row["arr_code"])
            if key not in valid:
                await conn.execute(
                    "DELETE FROM sync_routes WHERE dep_code = $1 AND arr_code = $2",
                    key[0],
                    key[1],
                )
    finally:
        await conn.close()

    print(f"seeded {len(DEFAULT_SYNC_ROUTES)} sync_routes")
    return 0


def main() -> int:
    return asyncio.run(main_async())


if __name__ == "__main__":
    raise SystemExit(main())
