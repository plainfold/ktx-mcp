from __future__ import annotations

from typing import Protocol

from ktx_mcp.models.train import TrainDeparture


class TimetableStore(Protocol):
    async def search_trains(
        self,
        dep_code: str,
        arr_code: str,
        travel_date: str,
        *,
        train_type: str = "ALL",
        dep_after: str | None = None,
    ) -> list[TrainDeparture]: ...

    async def upsert_many(self, rows: list[TrainDeparture]) -> int: ...

    async def count_rows(self) -> int: ...


class InMemoryTimetableStore:
    """Phase 1 store — no database. Swap for Postgres later."""

    def __init__(self) -> None:
        self._rows: dict[tuple[str, str, str, str, str, str], TrainDeparture] = {}

    @staticmethod
    def _key(row: TrainDeparture) -> tuple[str, str, str, str, str, str]:
        return (
            row.dep_code,
            row.arr_code,
            row.travel_date,
            row.dep_time,
            row.train_type,
            row.train_no,
        )

    async def search_trains(
        self,
        dep_code: str,
        arr_code: str,
        travel_date: str,
        *,
        train_type: str = "ALL",
        dep_after: str | None = None,
    ) -> list[TrainDeparture]:
        rows = [
            row
            for row in self._rows.values()
            if row.dep_code == dep_code
            and row.arr_code == arr_code
            and row.travel_date == travel_date
            and row.matches_type(train_type)
            and (dep_after is None or row.dep_time >= dep_after)
        ]
        rows.sort(key=lambda row: row.dep_time)
        return rows

    async def upsert_many(self, rows: list[TrainDeparture]) -> int:
        for row in rows:
            self._rows[self._key(row)] = row
        return len(rows)

    async def count_rows(self) -> int:
        return len(self._rows)
