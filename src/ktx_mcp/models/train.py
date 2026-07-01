from __future__ import annotations

from pydantic import BaseModel


def is_ktx_or_srt(train_type: str) -> bool:
    upper = train_type.upper()
    return "KTX" in upper or "SRT" in upper


class TrainDeparture(BaseModel):
    dep_code: str
    arr_code: str
    travel_date: str
    dep_time: str
    arr_time: str
    train_type: str
    train_no: str = ""
    duration_min: int | None = None

    def matches_type(self, train_type: str) -> bool:
        if train_type.upper() == "ALL":
            return is_ktx_or_srt(self.train_type)
        return train_type.upper() in self.train_type.upper()
