#!/usr/bin/env python3
"""Apply Supabase migration and verify DATABASE_URL connectivity."""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ktx_mcp.config import Settings  # noqa: E402
from ktx_mcp.store.postgres import PostgresTimetableStore  # noqa: E402

MIGRATION = ROOT / "supabase" / "migrations" / "001_train_departures.sql"


def _split_sql(sql: str) -> list[str]:
    statements: list[str] = []
    buffer: list[str] = []
    for line in sql.splitlines():
        stripped = line.strip()
        if stripped.startswith("--"):
            continue
        buffer.append(line)
        if stripped.endswith(";"):
            statement = "\n".join(buffer).strip()
            if statement:
                statements.append(statement[:-1].strip())
            buffer = []
    tail = "\n".join(buffer).strip()
    if tail:
        statements.append(tail)
    return statements


async def apply_migration(database_url: str) -> None:
    import asyncpg

    sql = MIGRATION.read_text(encoding="utf-8")
    statements = _split_sql(sql)
    ssl = "require" if "supabase.co" in database_url else False
    conn = await asyncpg.connect(database_url, ssl=ssl)
    try:
        for statement in statements:
            try:
                await conn.execute(statement)
            except asyncpg.DuplicateObjectError:
                continue
            except asyncpg.exceptions.DuplicateTableError:
                continue
    finally:
        await conn.close()


async def check(database_url: str) -> int:
    store = PostgresTimetableStore(database_url)
    try:
        await store.ping()
        count = await store.count_rows()
    finally:
        await store.close()
    print(f"ok: connected, train_departures rows={count}")
    return 0


async def main_async(migrate: bool) -> int:
    settings = Settings.from_env()
    if not settings.database_url:
        print("DATABASE_URL is not set (.env or environment)", file=sys.stderr)
        return 1

    if migrate:
        print(f"Applying migration: {MIGRATION.name}")
        await apply_migration(settings.database_url)
        print("Migration applied.")

    return await check(settings.database_url)


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify Postgres / apply migration")
    parser.add_argument("--migrate", action="store_true", help="Apply 001_train_departures.sql")
    args = parser.parse_args()
    try:
        return asyncio.run(main_async(args.migrate))
    except Exception as exc:  # noqa: BLE001 — CLI surfaces connection errors
        hint = ""
        if "getaddrinfo" in str(exc).lower() or "11001" in str(exc):
            hint = (
                "\nHint: Supabase direct host (db.*.supabase.co) may be IPv6-only. "
                "Try Session pooler (*.pooler.supabase.com:5432) from the dashboard."
            )
        print(f"error: {exc}{hint}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
