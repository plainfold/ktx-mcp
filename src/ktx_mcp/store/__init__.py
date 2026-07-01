"""Timetable persistence — Postgres when DATABASE_URL is set, else in-memory."""

from ktx_mcp.store.factory import create_timetable_store
from ktx_mcp.store.postgres import PostgresTimetableStore
from ktx_mcp.store.timetable import InMemoryTimetableStore, TimetableStore

__all__ = [
    "InMemoryTimetableStore",
    "PostgresTimetableStore",
    "TimetableStore",
    "create_timetable_store",
]
