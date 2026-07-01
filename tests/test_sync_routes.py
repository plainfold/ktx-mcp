from ktx_mcp.data.korail_lines_loader import (
    DEFAULT_SYNC_ROUTES,
    match_korail_name_to_tago,
)


def test_korail_paren_name_maps_to_tago():
    by_name = {"울산": ["NATH13717"], "진부": ["NAT601123"]}
    assert match_korail_name_to_tago("울산(통도사)", by_name) == ("NATH13717", "울산")
    assert match_korail_name_to_tago("진부(오대산)", by_name)[1] == "진부"


def test_sync_routes_from_korail_lines():
    assert len(DEFAULT_SYNC_ROUTES) >= 70


def test_sync_routes_include_suseo_busan_supplement():
    pairs = {(dep, arr) for dep, arr, _label in DEFAULT_SYNC_ROUTES}
    assert ("NATH30000", "NAT014445") in pairs


def test_sync_routes_unique_pairs():
    pairs = {(dep, arr) for dep, arr, _label in DEFAULT_SYNC_ROUTES}
    assert len(pairs) == len(DEFAULT_SYNC_ROUTES)
