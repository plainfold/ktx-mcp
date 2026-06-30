from __future__ import annotations

from pydantic import BaseModel, Field


class StationMatch(BaseModel):
    station_name: str
    station_code: str
    note: str | None = None
    score: float = Field(default=1.0, ge=0.0, le=1.0)
