#!/usr/bin/env python3
"""Smoke test: one TAGO train API call via data.go.kr key."""

from __future__ import annotations

import os
import sys
from urllib.parse import urlencode

import httpx

# TAGO train schedule endpoint (verify against latest TAGO docs)
TAGO_TRAIN_URL = "http://apis.data.go.kr/1613000/TrainInfoService/getStrtpntAlocFndTrainInfo"


def main() -> int:
    key = os.environ.get("DATA_GO_KR_SERVICE_KEY", "").strip()
    if not key:
        print("Set DATA_GO_KR_SERVICE_KEY (data.go.kr TAGO train API 15098552)", file=sys.stderr)
        return 1

    params = {
        "serviceKey": key,
        "depPlaceId": "NAT010000",
        "arrPlaceId": "NAT014445",
        "depPlandTime": "20260701",
        "numOfRows": "3",
        "pageNo": "1",
        "_type": "json",
    }
    url = f"{TAGO_TRAIN_URL}?{urlencode(params)}"

    print(f"GET {TAGO_TRAIN_URL} ...")
    try:
        with httpx.Client(timeout=30.0) as client:
            resp = client.get(url)
            resp.raise_for_status()
            print(f"status={resp.status_code} bytes={len(resp.content)}")
            print(resp.text[:500])
    except httpx.HTTPError as exc:
        print(f"HTTP error: {exc}", file=sys.stderr)
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
