from __future__ import annotations

import pytest

from ktx_mcp.config import Settings
from ktx_mcp.models.train import TrainDeparture
from ktx_mcp.store.postgres import PostgresTimetableStore

pytestmark = pytest.mark.skipif(
    not Settings.from_env().database_url,
    reason="DATABASE_URL not configured",
)


@pytest.fixture
async def pg_store():
    settings = Settings.from_env()
    assert settings.database_url
    store = PostgresTimetableStore(settings.database_url)
    yield store
    await store.close()


@pytest.mark.asyncio
async def test_postgres_ping(pg_store: PostgresTimetableStore):
    assert await pg_store.ping() is True


@pytest.mark.asyncio
async def test_postgres_upsert_and_search(pg_store: PostgresTimetableStore):
    row = TrainDeparture(
        dep_code="NAT_TEST_DEP",
        arr_code="NAT_TEST_ARR",
        travel_date="20990101",
        dep_time="1200",
        arr_time="1300",
        train_type="KTX",
        train_no="TEST1",
        duration_min=60,
    )
    try:
        await pg_store.upsert_many([row])
        found = await pg_store.search_trains(
            "NAT_TEST_DEP",
            "NAT_TEST_ARR",
            "20990101",
            train_type="KTX",
        )
        assert len(found) == 1
        assert found[0].train_no == "TEST1"
    finally:
        import asyncpg

        settings = Settings.from_env()
        assert settings.database_url
        conn = await asyncpg.connect(
            settings.database_url,
            ssl="require" if "supabase.co" in settings.database_url else False,
        )
        try:
            await conn.execute(
                """
                DELETE FROM train_departures
                WHERE dep_code = $1 AND arr_code = $2 AND travel_date = $3
                """,
                row.dep_code,
                row.arr_code,
                row.travel_date,
            )
        finally:
            await conn.close()
