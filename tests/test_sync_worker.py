import pytest

from ktx_mcp.adapters.tago import _parse_train_items
from ktx_mcp.store.timetable import InMemoryTimetableStore
from ktx_mcp.sync.worker import SyncWorker


def test_parse_train_items():
    payload = {
        "response": {
            "body": {
                "items": {
                    "item": [
                        {
                            "traingradename": "KTX",
                            "trainno": "101",
                            "depplandtime": "20260701050000",
                            "arrplandtime": "20260701073000",
                        }
                    ]
                }
            }
        }
    }
    rows = _parse_train_items(payload, "NAT010000", "NAT010058", "20260701")
    assert len(rows) == 1
    assert rows[0].train_type == "KTX"
    assert rows[0].dep_time == "0500"


@pytest.mark.asyncio
async def test_sync_worker_without_tago_key():
    store = InMemoryTimetableStore()
    worker = SyncWorker(store, tago=None)
    result = await worker.run()
    assert result.status == "skipped"
    assert "TAGO key not configured" in result.errors[0]
