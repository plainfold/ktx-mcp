


from ktx_mcp.tools.stations import resolve_station_code, search_stations_payload


def test_search_stations_korean_nodename():

    payload = search_stations_payload("서울", locale="ko")

    assert payload["error"] is None

    assert payload["matches"][0]["station_code"] == "NAT010000"

    assert payload["matches"][0]["station_name"] == "서울"





def test_search_stations_busan():

    payload = search_stations_payload("부산", locale="ko")

    assert payload["matches"][0]["station_code"] == "NAT014445"





def test_search_stations_english_not_matched():

    payload = search_stations_payload("Seoul", locale="en")

    assert payload["error"] == "STATION_NOT_FOUND"





def test_search_stations_gyeongju_tago_name():

    payload = search_stations_payload("경주", locale="ko")

    assert payload["matches"][0]["station_code"] == "NATH13421"

    assert payload["matches"][0]["station_name"] == "경주"





def test_search_stations_not_found():

    payload = search_stations_payload("Atlantis", locale="en")

    assert payload["error"] == "STATION_NOT_FOUND"

    assert payload["matches"] == []





def test_resolve_station_code_accepts_nat_code():

    assert resolve_station_code("NAT010000") == "NAT010000"





def test_resolve_station_code_korean_name():

    assert resolve_station_code("부산") == "NAT014445"

