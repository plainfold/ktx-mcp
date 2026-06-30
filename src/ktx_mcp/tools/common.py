from __future__ import annotations

from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

KST = ZoneInfo("Asia/Seoul")

_ATTRIBUTION = "Ministry of Land, Infrastructure and Transport / TAGO"
_DISCLAIMERS = {
    "en": (
        "Timetable reference only. Schedules may change. "
        "No booking or seat availability. Not affiliated with Korail or SR."
    ),
    "ko": (
        "시각표 참고용입니다. 운행 시각은 변경될 수 있습니다. "
        "예매·잔여석 미제공. 코레일·SR 공식 제휴 아님."
    ),
    "ja": "時刻表の参考情報です。予約・空席確認は行いません。",
    "zh": "仅供参考的时刻表信息。不提供订票或余票查询。",
}


def normalize_locale(locale: str | None, default: str = "en") -> str:
    if not locale:
        return default
    code = locale.strip().lower()[:2]
    return code if code in _DISCLAIMERS else default


def now_kst_iso() -> str:
    return datetime.now(KST).isoformat()


def tool_envelope(payload: dict[str, Any], *, locale: str = "en") -> dict[str, Any]:
    loc = normalize_locale(locale)
    return {
        **payload,
        "data_source": "tago",
        "attribution": _ATTRIBUTION,
        "as_of": now_kst_iso(),
        "disclaimer": _DISCLAIMERS[loc],
        "locale": loc,
    }
