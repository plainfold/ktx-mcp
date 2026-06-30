from __future__ import annotations

from typing import Any
from urllib.parse import urlencode

import httpx

from ktx_mcp.models.train import TrainDeparture

TAGO_TRAIN_URL = (
    "http://apis.data.go.kr/1613000/TrainInfoService/getStrtpntAlocFndTrainInfo"
)


class TagoGateway:
    """TAGO train timetable client (sync worker only — not on MCP request path)."""

    def __init__(self, service_key: str, *, client: httpx.AsyncClient | None = None) -> None:
        self._service_key = service_key
        self._client = client
        self.calls_today = 0

    async def fetch_route(
        self,
        dep_code: str,
        arr_code: str,
        travel_date: str,
        *,
        num_rows: int = 100,
    ) -> list[TrainDeparture]:
        params = {
            "serviceKey": self._service_key,
            "depPlaceId": dep_code,
            "arrPlaceId": arr_code,
            "depPlandTime": travel_date,
            "numOfRows": str(num_rows),
            "pageNo": "1",
            "_type": "json",
        }
        url = f"{TAGO_TRAIN_URL}?{urlencode(params)}"

        if self._client is None:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url)
        else:
            response = await self._client.get(url)

        response.raise_for_status()
        self.calls_today += 1
        return _parse_train_items(response.json(), dep_code, arr_code, travel_date)


def _parse_train_items(
    payload: dict[str, Any],
    dep_code: str,
    arr_code: str,
    travel_date: str,
) -> list[TrainDeparture]:
    body = payload.get("response", {}).get("body", {})
    items = body.get("items", {})
    raw_items = items.get("item", [])
    if raw_items is None:
        return []
    if isinstance(raw_items, dict):
        raw_items = [raw_items]

    rows: list[TrainDeparture] = []
    for item in raw_items:
        dep_time = _normalize_time(item.get("depplandtime") or item.get("depPlanTime"))
        arr_time = _normalize_time(item.get("arrplandtime") or item.get("arrPlanTime"))
        train_type = str(item.get("traingradename") or item.get("trainGradeName") or "UNKNOWN")
        train_no = str(item.get("trainno") or item.get("trainNo") or "")
        if not dep_time or not arr_time:
            continue
        rows.append(
            TrainDeparture(
                dep_code=dep_code,
                arr_code=arr_code,
                travel_date=travel_date,
                dep_time=dep_time,
                arr_time=arr_time,
                train_type=train_type,
                train_no=train_no,
                duration_min=_duration_minutes(dep_time, arr_time),
            )
        )
    return rows


def _normalize_time(value: Any) -> str:
    text = str(value or "").strip()
    digits = "".join(ch for ch in text if ch.isdigit())
    if len(digits) >= 12:
        return digits[8:12]
    if len(digits) >= 4:
        return digits[-4:]
    return ""


def _duration_minutes(dep_time: str, arr_time: str) -> int | None:
    if len(dep_time) != 4 or len(arr_time) != 4:
        return None
    dep = int(dep_time[:2]) * 60 + int(dep_time[2:])
    arr = int(arr_time[:2]) * 60 + int(arr_time[2:])
    if arr < dep:
        arr += 24 * 60
    return arr - dep
