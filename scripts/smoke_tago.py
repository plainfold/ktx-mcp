#!/usr/bin/env python3
"""Smoke test: TAGO TrainInfo API via apis.data.go.kr/1613000."""

from __future__ import annotations

import sys
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ktx_mcp.adapters.tago_client import (  # noqa: E402
    OP_TRAIN_TIMETABLE,
    TagoApiError,
    load_service_key,
    tago_get,
)

KST = ZoneInfo("Asia/Seoul")


def main() -> int:
    try:
        service_key = load_service_key()
    except TagoApiError as exc:
        print(exc, file=sys.stderr)
        return 1

    travel_date = (datetime.now(KST).date() + timedelta(days=1)).strftime("%Y%m%d")
    print("GET GetStrtpntAlocFndTrainInfo (Seoul -> Busan) ...")
    try:
        payload = tago_get(
            OP_TRAIN_TIMETABLE,
            service_key=service_key,
            depPlaceId="NAT010000",
            arrPlaceId="NAT014445",
            depPlandTime=travel_date,
            numOfRows="3",
            pageNo="1",
        )
    except TagoApiError as exc:
        print(exc, file=sys.stderr)
        if exc.result_code == "99":
            print("활용신청(15098552) 승인 및 인증키 확인 필요", file=sys.stderr)
        return 2

    items = payload.get("response", {}).get("body", {}).get("items", {})
    print("ok", items)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
