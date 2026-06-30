from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

KST = ZoneInfo("Asia/Seoul")

_DAY_NAMES_EN = (
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
)


def today_kst_payload() -> dict[str, str]:
    now = datetime.now(KST)
    return {
        "date": now.strftime("%Y%m%d"),
        "timezone": "Asia/Seoul",
        "day_of_week": _DAY_NAMES_EN[now.weekday()],
        "summary": f"{now.strftime('%Y-%m-%d')} ({now.strftime('%a')}) — today in KST",
        "data_source": "tago",
        "attribution": "Ministry of Land, Infrastructure and Transport / TAGO",
        "as_of": now.isoformat(),
        "disclaimer": "Timetable reference only; not for booking.",
    }
