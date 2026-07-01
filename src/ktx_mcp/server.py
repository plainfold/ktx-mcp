from __future__ import annotations

from functools import lru_cache

from fastmcp import FastMCP

from ktx_mcp.adapters.tago import TagoGateway
from ktx_mcp.config import Settings
from ktx_mcp.http.routes import HttpState, make_health_handler, make_sync_handler
from ktx_mcp.store.factory import create_timetable_store
from ktx_mcp.sync.worker import SyncWorker
from ktx_mcp.tools.datetime_kst import today_kst_payload
from ktx_mcp.tools.stations import search_stations_payload
from ktx_mcp.tools.trains import compare_ktx_srt_payload, search_trains_payload

mcp = FastMCP(
    name="ktx-mcp",
    instructions=(
        "Korea KTX and SRT train timetables from TAGO public data. "
        "Only KTX/SRT — not ITX or conventional trains. "
        "Station names must match TAGO nodename (Korean) or nodeid (NAT...). "
        "Always call get_today_kst before date-sensitive queries."
    ),
)


@lru_cache(maxsize=1)
def _http_state() -> HttpState:
    settings = Settings.from_env()
    store = create_timetable_store(settings.database_url)
    tago = TagoGateway(settings.tago_service_key) if settings.tago_service_key else None
    worker = SyncWorker(store, tago)
    return HttpState(settings=settings, timetable_store=store, sync_worker=worker)


def _register_http_routes() -> None:
    state = _http_state()
    mcp.custom_route("/health", methods=["GET"])(make_health_handler(state))
    mcp.custom_route("/internal/sync", methods=["POST"])(make_sync_handler(state))


_register_http_routes()


@mcp.tool(
    name="get_today_kst",
    description=(
        "Return today's date in Korea Standard Time (Asia/Seoul). "
        "Call this before any train schedule query to avoid date hallucination."
    ),
)
def get_today_kst() -> dict[str, str]:
    return today_kst_payload()


@mcp.tool(
    name="search_stations",
    description=(
        "Resolve a station name to TAGO station code. "
        "Query must be TAGO nodename (Korean) or nodeid (NAT...)."
    ),
)
def search_stations(query: str, locale: str = "en") -> dict:
    return search_stations_payload(query, locale=locale)


@mcp.tool(
    name="search_trains",
    description=(
        "KTX/SRT timetable for a route on a given date (YYYYMMDD). "
        "Reads from the local timetable store (synced from TAGO). "
        "train_type: KTX, SRT, or ALL (both). Does not include ITX or other trains."
    ),
)
async def search_trains(
    departure: str,
    arrival: str,
    date: str,
    time: str | None = None,
    train_type: str = "ALL",
    locale: str = "en",
) -> dict:
    store = _http_state().timetable_store
    return await search_trains_payload(
        store,
        departure=departure,
        arrival=arrival,
        date=date,
        time=time,
        train_type=train_type,
        locale=locale,
    )


@mcp.tool(
    name="compare_ktx_srt",
    description=(
        "Compare KTX and SRT options on the same route and date. "
        "Reads from the local timetable store."
    ),
)
async def compare_ktx_srt(
    departure: str,
    arrival: str,
    date: str,
    time: str | None = None,
    locale: str = "en",
) -> dict:
    store = _http_state().timetable_store
    return await compare_ktx_srt_payload(
        store,
        departure=departure,
        arrival=arrival,
        date=date,
        time=time,
        locale=locale,
    )


def main() -> None:
    settings = Settings.from_env()
    if settings.transport == "http":
        mcp.run(transport="http", host=settings.host, port=settings.port)
    else:
        mcp.run()


if __name__ == "__main__":
    main()
