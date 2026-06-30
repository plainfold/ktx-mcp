from __future__ import annotations

from typing import TYPE_CHECKING

from ktx_mcp.tools.common import normalize_locale, tool_envelope
from ktx_mcp.tools.stations import resolve_station_code

if TYPE_CHECKING:
    from ktx_mcp.store.timetable import TimetableStore


def _train_dict(row) -> dict[str, str | int | None]:
    return {
        "departure_time": row.dep_time,
        "arrival_time": row.arr_time,
        "train_type": row.train_type,
        "train_no": row.train_no,
        "duration_min": row.duration_min,
    }


async def search_trains_payload(
    store: TimetableStore,
    *,
    departure: str,
    arrival: str,
    date: str,
    time: str | None = None,
    train_type: str = "ALL",
    locale: str = "en",
) -> dict:
    loc = normalize_locale(locale)
    dep_code = resolve_station_code(departure)
    arr_code = resolve_station_code(arrival)

    if not dep_code or not arr_code:
        return tool_envelope(
            {
                "trains": [],
                "summary": "Station not found. Run search_stations first.",
                "error": "STATION_NOT_FOUND",
            },
            locale=loc,
        )

    dep_after = time if time else None
    rows = await store.search_trains(
        dep_code,
        arr_code,
        date,
        train_type=train_type,
        dep_after=dep_after,
    )

    if not rows:
        return tool_envelope(
            {
                "trains": [],
                "summary": (
                    f"No trains in timetable store for {departure} → {arrival} on {date}. "
                    "Data may not be synced yet."
                ),
                "error": "NO_TRAINS",
                "fetched_at": None,
            },
            locale=loc,
        )

    trains = [_train_dict(row) for row in rows]
    return tool_envelope(
        {
            "trains": trains,
            "summary": f"{len(trains)} train(s) from {departure} to {arrival} on {date}.",
            "error": None,
            "dep_code": dep_code,
            "arr_code": arr_code,
        },
        locale=loc,
    )


async def compare_ktx_srt_payload(
    store: TimetableStore,
    *,
    departure: str,
    arrival: str,
    date: str,
    time: str | None = None,
    locale: str = "en",
) -> dict:
    loc = normalize_locale(locale)
    ktx = await search_trains_payload(
        store,
        departure=departure,
        arrival=arrival,
        date=date,
        time=time,
        train_type="KTX",
        locale=loc,
    )
    srt = await search_trains_payload(
        store,
        departure=departure,
        arrival=arrival,
        date=date,
        time=time,
        train_type="SRT",
        locale=loc,
    )

    ktx_trains = ktx.get("trains") or []
    srt_trains = srt.get("trains") or []

    if not ktx_trains and not srt_trains:
        summary = ktx.get("summary") or "No KTX or SRT options in store."
        return tool_envelope(
            {
                "ktx_options": [],
                "srt_options": [],
                "recommendation_summary": summary,
                "error": "NO_TRAINS",
            },
            locale=loc,
        )

    recommendation = _recommendation(ktx_trains, srt_trains)
    return tool_envelope(
        {
            "ktx_options": ktx_trains,
            "srt_options": srt_trains,
            "recommendation_summary": recommendation,
            "error": None,
        },
        locale=loc,
    )


def _recommendation(ktx_trains: list[dict], srt_trains: list[dict]) -> str:
    if ktx_trains and not srt_trains:
        return "Only KTX options are available for this route in the store."
    if srt_trains and not ktx_trains:
        return "Only SRT options are available for this route in the store."
    return (
        f"Found {len(ktx_trains)} KTX and {len(srt_trains)} SRT option(s). "
        "Compare departure times and stations (Seoul vs Suseo)."
    )
