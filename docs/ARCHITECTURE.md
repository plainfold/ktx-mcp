# Architecture

High-level design for ktx-mcp.  
**P0:** [TRAFFIC.md](./TRAFFIC.md) — keyless hosted + TAGO 10k/day cache strategy.

## Stack

| Layer | Choice |
|-------|--------|
| Language | Python 3.11+ |
| MCP | FastMCP 2.x |
| HTTP | httpx (async) |
| Models | Pydantic v2 |
| Cache (hosted) | **Redis** |
| Package | hatchling / uv |
| Tests | pytest + pytest-httpx |

## Data flow (hosted — default)

```
MCP Client (no API key)
        │
        ▼
   FastMCP HTTP server
        │
        ├── tools/*  (6–7 MCP calls per user question)
        │
        ▼
   TagoGateway  ◄── P0: all TAGO traffic here
        │
        ├── request-scoped cache
        ├── Redis TTL cache
        ├── singleflight dedup
        └── TAGO API (≤1 call per route/date on miss)
```

## Zero-TAGO tools (runtime)

| Tool | Data source |
|------|-------------|
| `get_today_kst` | System clock (KST) |
| `search_stations` | `stations_i18n.json` only |
| `get_booking_links` | Static URLs |
| `holiday_check` | 공휴일 API (not TAGO train) |

## TAGO-consuming tools (via gateway)

| Tool | TAGO calls (optimized) |
|------|------------------------|
| `search_trains` | 0–1 (cache) |
| `compare_ktx_srt` | 0–1 (same fetch, split in memory) |
| `plan_trip` | **0** (reuses gateway cache in same request) |

## Deployment modes

| Mode | User key | TAGO key | Cache |
|------|----------|----------|-------|
| **Hosted (default)** | None | Server-side | Redis |
| Local BYOK (dev) | User's TAGO key | User | In-memory |

## Cache TTL

| Key | TTL |
|-----|-----|
| `trains:{dep}:{arr}:{date}` | 15 min (30 min top routes) |
| `stations:manifest` | 24 h (background job) |
| `holiday:{year}` | 7 d |

## Adapter rule

**v1:** `TagoAdapter` behind `TagoGateway` only.

**Forbidden:** per-tool direct TAGO HTTP; KRIC rail portal; Korail scraping.

## Registry identity

- `io.github.plainfold/ktx-mcp`
- PyPI: `ktx-mcp` (BYOK dev path)
