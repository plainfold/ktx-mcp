import pytest

from ktx_mcp.tools.stations import resolve_station_code, search_stations_payload


def test_search_stations_seoul_english():
    payload = search_stations_payload("Seoul", locale="en")
    assert payload["error"] is None
    assert payload["matches"][0]["station_code"] == "NAT010000"
    assert payload["matches"][0]["station_name"] == "서울"


def test_search_stations_korean():
    payload = search_stations_payload("부산", locale="ko")
    assert payload["matches"][0]["station_code"] == "NAT014445"


def test_search_stations_tago_alias_mapping():
    """신경주 displays as canonical; TAGO nodename is 경주."""
    by_canonical = search_stations_payload("신경주", locale="ko")
    assert by_canonical["matches"][0]["station_code"] == "NATH13421"
    by_tago = search_stations_payload("경주", locale="ko")
    assert by_tago["matches"][0]["station_name"] == "신경주"


def test_search_stations_not_found():
    payload = search_stations_payload("Atlantis", locale="en")
    assert payload["error"] == "STATION_NOT_FOUND"
    assert payload["matches"] == []


def test_resolve_station_code_accepts_nat_code():
    assert resolve_station_code("NAT010000") == "NAT010000"
