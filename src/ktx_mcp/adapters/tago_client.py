from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import httpx

# data.go.kr 15098552 — TAGO 열차정보 (공식 REST)
# Example:
#   .../TrainInfo/GetCtyAcctoTrainSttnList?serviceKey=...&cityCode=11&numOfRows=20
TAGO_TRAIN_BASE = "https://apis.data.go.kr/1613000/TrainInfo"

# PascalCase operation names per portal spec
OP_CITY_CODES = "GetCtyCodeList"
OP_CITY_STATIONS = "GetCtyAcctoTrainSttnList"
OP_TRAIN_TIMETABLE = "GetStrtpntAlocFndTrainInfo"

TAGO_RESULT_OK = "00"


class TagoApiError(RuntimeError):
    def __init__(self, result_code: str, result_msg: str, *, operation: str) -> None:
        super().__init__(f"TAGO {operation} failed: [{result_code}] {result_msg}")
        self.result_code = result_code
        self.result_msg = result_msg
        self.operation = operation


_KEY_NAMES = (
    "DATA_GO_KR_SERVICE_KEY_Decoding",
    "DATA_GO_KR_SERVICE_KEY",
    "DATA_GO_KR_SERVICE_KEY_Encoding",
)


def _read_dotenv() -> dict[str, str]:
    env_path = Path(".env")
    if not env_path.is_file():
        return {}
    values: dict[str, str] = {}
    for line in env_path.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def load_service_key() -> str:
    dotenv = _read_dotenv()
    for name in _KEY_NAMES:
        value = os.environ.get(name, "").strip() or dotenv.get(name, "").strip()
        if value:
            return value

    raise TagoApiError(
        "ENV",
        "Set DATA_GO_KR_SERVICE_KEY_Decoding (TAGO 열차정보 15098552)",
        operation="auth",
    )


def tago_get(
    operation: str,
    *,
    service_key: str,
    client: httpx.Client | None = None,
    **params: str,
) -> dict[str, Any]:
    query: dict[str, str] = {
        "serviceKey": service_key,
        **{k: str(v) for k, v in params.items()},
    }
    if "_type" not in query:
        query["_type"] = "json"
    url = f"{TAGO_TRAIN_BASE}/{operation}"

    if client is None:
        with httpx.Client(timeout=30.0) as owned:
            response = owned.get(url, params=query)
    else:
        response = client.get(url, params=query)

    response.raise_for_status()
    payload = response.json()
    header = payload.get("response", {}).get("header", {})
    result_code = str(header.get("resultCode", ""))
    result_msg = str(header.get("resultMsg", ""))
    if result_code != TAGO_RESULT_OK:
        raise TagoApiError(result_code, result_msg, operation=operation)
    return payload


def extract_items(payload: dict[str, Any]) -> list[dict[str, Any]]:
    body = payload.get("response", {}).get("body", {})
    items = body.get("items")
    if not items:
        return []
    raw = items.get("item", [])
    if raw is None:
        return []
    if isinstance(raw, dict):
        return [raw]
    return list(raw)


def pick_field(item: dict[str, Any], *keys: str) -> str:
    for key in keys:
        value = item.get(key)
        if value is not None and str(value).strip():
            return str(value).strip()
    return ""


def parse_cities(payload: dict[str, Any]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for item in extract_items(payload):
        code = pick_field(item, "citycode", "cityCode")
        name = pick_field(item, "cityname", "cityName")
        if code and name:
            rows.append({"city_code": code, "city_name": name})
    return rows


def parse_stations(payload: dict[str, Any]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for item in extract_items(payload):
        code = pick_field(item, "nodeid", "nodeId")
        name = pick_field(item, "nodename", "nodenm", "nodeNm")
        if code and name:
            rows.append({"station_code": code, "station_name": name})
    return rows


def fetch_all_cities(
    service_key: str, *, client: httpx.Client | None = None
) -> list[dict[str, str]]:
    page = 1
    rows: list[dict[str, str]] = []
    while True:
        payload = tago_get(
            OP_CITY_CODES,
            service_key=service_key,
            client=client,
            numOfRows="100",
            pageNo=str(page),
        )
        batch = parse_cities(payload)
        if not batch:
            break
        rows.extend(batch)
        total = int(payload.get("response", {}).get("body", {}).get("totalCount") or 0)
        if len(rows) >= total:
            break
        page += 1
    return rows


def fetch_stations_for_city(
    service_key: str,
    city_code: str,
    *,
    client: httpx.Client | None = None,
) -> list[dict[str, str]]:
    page = 1
    rows: list[dict[str, str]] = []
    while True:
        payload = tago_get(
            OP_CITY_STATIONS,
            service_key=service_key,
            client=client,
            cityCode=city_code,
            numOfRows="200",
            pageNo=str(page),
        )
        batch = parse_stations(payload)
        if not batch:
            break
        rows.extend(batch)
        total = int(payload.get("response", {}).get("body", {}).get("totalCount") or 0)
        if len(rows) >= total:
            break
        page += 1
    return rows


def fetch_all_stations(service_key: str) -> list[dict[str, str]]:
    by_code: dict[str, dict[str, str]] = {}
    with httpx.Client(timeout=30.0) as client:
        cities = fetch_all_cities(service_key, client=client)
        for city in cities:
            for station in fetch_stations_for_city(
                service_key, city["city_code"], client=client
            ):
                by_code[station["station_code"]] = {
                    "canonical": station["station_name"],
                    "code": station["station_code"],
                    "city_code": city["city_code"],
                    "city_name": city["city_name"],
                }
    return list(by_code.values())
