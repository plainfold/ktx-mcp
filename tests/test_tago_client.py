from ktx_mcp.adapters.tago_client import parse_cities, parse_stations


def test_parse_cities_fixture():
    import json
    from pathlib import Path

    payload = json.loads(Path("tests/fixtures/tago_cities.json").read_text(encoding="utf-8"))
    rows = parse_cities(payload)
    assert rows[0]["city_code"] == "11"
    assert rows[0]["city_name"] == "서울"


def test_parse_stations_fixture():
    import json
    from pathlib import Path

    payload = json.loads(Path("tests/fixtures/tago_stations_seoul.json").read_text(encoding="utf-8"))
    rows = parse_stations(payload)
    assert rows[0]["station_code"] == "NAT010000"
    assert rows[0]["station_name"] == "서울"
