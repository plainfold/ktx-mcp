from __future__ import annotations

from ktx_mcp.store.postgres import PostgresTimetableStore
from ktx_mcp.store.timetable import InMemoryTimetableStore, TimetableStore


def create_timetable_store(database_url: str | None) -> TimetableStore:
    if database_url:
        return PostgresTimetableStore(database_url)
    return InMemoryTimetableStore()
