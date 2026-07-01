import pytest
from starlette.requests import Request

from ktx_mcp.config import Settings
from ktx_mcp.http.routes import HttpState, make_health_handler, make_sync_handler
from ktx_mcp.store.timetable import InMemoryTimetableStore
from ktx_mcp.sync.worker import SyncWorker


def test_http_routes_import() -> None:
    from ktx_mcp.http import routes  # noqa: F401

    assert routes.HttpState is not None


@pytest.mark.asyncio
async def test_health_handler_in_memory() -> None:
    state = HttpState(
        settings=Settings(transport="http"),
        timetable_store=InMemoryTimetableStore(),
        sync_worker=SyncWorker(InMemoryTimetableStore(), tago=None),
    )
    handler = make_health_handler(state)
    response = await handler(Request({"type": "http", "method": "GET", "path": "/health"}))
    assert response.status_code == 200
    body = __import__("json").loads(response.body)
    assert body["status"] == "ok"
    assert body["store"] == "in_memory"


@pytest.mark.asyncio
async def test_sync_handler_requires_secret() -> None:
    state = HttpState(
        settings=Settings(transport="http", sync_secret="test-secret"),
        timetable_store=InMemoryTimetableStore(),
        sync_worker=SyncWorker(InMemoryTimetableStore(), tago=None),
    )
    handler = make_sync_handler(state)

    unauthorized = await handler(
        Request({"type": "http", "method": "POST", "path": "/internal/sync", "headers": []})
    )
    assert unauthorized.status_code == 401

    skipped = await handler(
        Request(
            {
                "type": "http",
                "method": "POST",
                "path": "/internal/sync",
                "headers": [(b"x-sync-secret", b"test-secret")],
            }
        )
    )
    assert skipped.status_code == 200
    body = __import__("json").loads(skipped.body)
    assert body["status"] == "skipped"
