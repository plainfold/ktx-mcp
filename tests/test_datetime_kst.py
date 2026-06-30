from ktx_mcp.tools.datetime_kst import today_kst_payload


def test_today_kst_has_required_fields():
    payload = today_kst_payload()
    assert payload["timezone"] == "Asia/Seoul"
    assert len(payload["date"]) == 8
    assert payload["data_source"] == "tago"
    assert "summary" in payload
