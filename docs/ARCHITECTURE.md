# Architecture

High-level design for ktx-mcp. Details in [KTX_MCP_SPEC.md](../docs/KTX_MCP_SPEC.md).

## Stack

| Layer | Choice |
|-------|--------|
| Language | Python 3.11+ |
| MCP | FastMCP 2.x |
| HTTP | httpx (async) |
| Models | Pydantic v2 |
| Package | hatchling / uv |
| Tests | pytest + pytest-httpx |

## Data flow

```
MCP Client (Cursor / Claude / ChatGPT)
        │
        ▼
   FastMCP server.py
        │
        ├── tools/datetime_kst.py
        ├── tools/stations.py      ──► stations_i18n.json
        ├── tools/trains.py        ──► TagoAdapter ──► TTL cache ──► TAGO API
        ├── tools/compare.py
        ├── tools/holiday.py       ──► 공휴일 API (Phase 2)
        ├── tools/booking_links.py
        └── tools/plan_trip.py
```

## Adapter rule

**v1:** `TagoAdapter` only — wraps [data.go.kr TAGO train API](https://www.data.go.kr/data/15098552/openapi.do).

**Forbidden:** KRIC rail portal adapter, Korail scraping.

```python
class TrainDataPort(Protocol):
    async def search_stations(self, query: str) -> list[Station]: ...
    async def search_trains(
        self, dep: str, arr: str, date: str, **kwargs
    ) -> list[Train]: ...
```

## Deployment modes

| Mode | Transport | API key |
|------|-----------|---------|
| Local BYOK | stdio | User's `DATA_GO_KR_SERVICE_KEY` |
| Hosted Free/Plus | Streamable HTTP | Server-side key + rate limit |

## Cache (planned)

| Key pattern | TTL |
|-------------|-----|
| `stations:*` | 24h |
| `trains:{dep}:{arr}:{date}` | 10 min |
| `holiday:{year}` | 7d |

## Repository layout

```
src/ktx_mcp/     Implementation
docs/            User + spec documentation
skills/          L2 agent skills
scripts/         smoke_tago.py, registry scan
tests/           pytest
```

## Registry identity

- `io.github.plainfold/ktx-mcp`
- PyPI: `ktx-mcp`
