import pytest

from ktx_mcp.models.train import TrainDeparture
from ktx_mcp.store.timetable import InMemoryTimetableStore
from ktx_mcp.tools.trains import compare_ktx_srt_payload, search_trains_payload


@pytest.fixture
def store() -> InMemoryTimetableStore:
    return InMemoryTimetableStore()


@pytest.mark.asyncio
async def test_search_trains_empty_store(store: InMemoryTimetableStore):
    payload = await search_trains_payload(
        store,
        departure="Seoul",
        arrival="Busan",
        date="20260701",
        locale="en",
    )
    assert payload["error"] == "NO_TRAINS"
    assert payload["trains"] == []


@pytest.mark.asyncio
async def test_search_trains_reads_store(store: InMemoryTimetableStore):
    await store.upsert_many(
        [
            TrainDeparture(
                dep_code="NAT010000",
                arr_code="NAT014445",
                travel_date="20260701",
                dep_time="0500",
                arr_time="0730",
                train_type="KTX",
                train_no="101",
                duration_min=150,
            )
        ]
    )
    payload = await search_trains_payload(
        store,
        departure="Seoul",
        arrival="Busan",
        date="20260701",
        train_type="KTX",
        locale="en",
    )
    assert payload["error"] is None
    assert len(payload["trains"]) == 1
    assert payload["trains"][0]["train_no"] == "101"


@pytest.mark.asyncio
async def test_compare_ktx_srt(store: InMemoryTimetableStore):
    await store.upsert_many(
        [
            TrainDeparture(
                dep_code="NATH30000",
                arr_code="NAT014445",
                travel_date="20260701",
                dep_time="0600",
                arr_time="0830",
                train_type="SRT",
                train_no="301",
            ),
            TrainDeparture(
                dep_code="NAT010000",
                arr_code="NAT014445",
                travel_date="20260701",
                dep_time="0700",
                arr_time="0930",
                train_type="KTX",
                train_no="201",
            ),
        ]
    )
    payload = await compare_ktx_srt_payload(
        store,
        departure="Seoul",
        arrival="Busan",
        date="20260701",
        locale="en",
    )
    assert payload["error"] is None
    assert len(payload["ktx_options"]) == 1
    assert len(payload["srt_options"]) == 0
