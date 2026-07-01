from __future__ import annotations

import asyncpg

from ktx_mcp.models.train import TrainDeparture

_SEARCH_SQL = """
SELECT dep_code, arr_code, travel_date, dep_time, arr_time, train_type, train_no, duration_min
FROM train_departures
WHERE dep_code = $1
  AND arr_code = $2
  AND travel_date = $3
  AND ($5::text IS NULL OR dep_time >= $5)
  AND (
    ($4 = 'ALL' AND (train_type ILIKE '%KTX%' OR train_type ILIKE '%SRT%'))
    OR ($4 <> 'ALL' AND train_type ILIKE '%' || $4 || '%')
  )
ORDER BY dep_time
"""

_UPSERT_SQL = """
INSERT INTO train_departures (
  dep_code, arr_code, travel_date, dep_time, arr_time, train_type, train_no, duration_min
) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
ON CONFLICT (dep_code, arr_code, travel_date, dep_time, train_type, train_no)
DO UPDATE SET
  arr_time = EXCLUDED.arr_time,
  duration_min = EXCLUDED.duration_min,
  fetched_at = now()
"""


def _pool_ssl(database_url: str) -> str | bool:
    if "supabase.co" in database_url:
        return "require"
    return False


class PostgresTimetableStore:
    """Postgres-backed timetable store (Supabase)."""

    def __init__(self, database_url: str) -> None:
        self._database_url = database_url
        self._pool: asyncpg.Pool | None = None

    async def _pool_or_create(self) -> asyncpg.Pool:
        if self._pool is None:
            self._pool = await asyncpg.create_pool(
                self._database_url,
                min_size=1,
                max_size=5,
                ssl=_pool_ssl(self._database_url),
            )
        return self._pool

    async def ping(self) -> bool:
        pool = await self._pool_or_create()
        async with pool.acquire() as conn:
            await conn.fetchval("SELECT 1")
        return True

    async def close(self) -> None:
        if self._pool is not None:
            await self._pool.close()
            self._pool = None

    async def search_trains(
        self,
        dep_code: str,
        arr_code: str,
        travel_date: str,
        *,
        train_type: str = "ALL",
        dep_after: str | None = None,
    ) -> list[TrainDeparture]:
        pool = await self._pool_or_create()
        type_filter = train_type.upper()
        async with pool.acquire() as conn:
            rows = await conn.fetch(
                _SEARCH_SQL,
                dep_code,
                arr_code,
                travel_date,
                type_filter,
                dep_after,
            )
        return [_row_to_departure(row) for row in rows]

    async def upsert_many(self, rows: list[TrainDeparture]) -> int:
        if not rows:
            return 0
        pool = await self._pool_or_create()
        records = [
            (
                row.dep_code,
                row.arr_code,
                row.travel_date,
                row.dep_time,
                row.arr_time,
                row.train_type,
                row.train_no,
                row.duration_min,
            )
            for row in rows
        ]
        async with pool.acquire() as conn:
            await conn.executemany(_UPSERT_SQL, records)
        return len(records)

    async def count_rows(self) -> int:
        pool = await self._pool_or_create()
        async with pool.acquire() as conn:
            value = await conn.fetchval("SELECT COUNT(*)::int FROM train_departures")
        return int(value or 0)


def _row_to_departure(row: asyncpg.Record) -> TrainDeparture:
    return TrainDeparture(
        dep_code=row["dep_code"],
        arr_code=row["arr_code"],
        travel_date=row["travel_date"],
        dep_time=row["dep_time"],
        arr_time=row["arr_time"],
        train_type=row["train_type"],
        train_no=row["train_no"] or "",
        duration_min=row["duration_min"],
    )
