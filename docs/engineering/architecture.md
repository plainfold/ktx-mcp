# Architecture

High-level design for ktx-mcp.  
**P0:** [traffic.md](./traffic.md) — keyless hosted + TAGO 10k/day via DB materialization.

## Official hosted stack

| Layer | Service | Account |
|-------|---------|---------|
| **Compute** | [Fly.io](https://fly.io) (`nrt`) — MCP HTTP + sync endpoint | ✅ |
| **Database** | [Supabase](https://supabase.com) Postgres — `train_departures` | ✅ |
| **Scheduler** | Supabase `pg_cron` → `POST /internal/sync` on Fly | ✅ |
| **Redis** | — | MVP skip (Postgres only) |

Deploy guide: [deploy.md](../getting-started/deploy.md)

## Stack (application)

| Layer | Choice |
|-------|--------|
| Language | Python 3.11+ |
| MCP | FastMCP 2.x |
| HTTP | httpx (async) |
| DB client | asyncpg or psycopg3 (Phase 1) |
| Models | Pydantic v2 |
| Package | hatchling / uv |
| Tests | pytest + pytest-httpx |

## Data flow (hosted — default)

```text
MCP Client (no API key)
    → Fly.io FastMCP HTTP (/mcp)
    → Supabase Postgres (pooler, SELECT only)

Supabase pg_cron (30 min)
    → Fly POST /internal/sync
    → TAGO API (DATA_GO_KR_SERVICE_KEY on Fly only)
    → UPSERT Supabase Postgres
```

## Zero-TAGO tools (runtime)

| Tool | Data source |
|------|-------------|
| `get_today_kst` | System clock (KST) |
| `search_stations` | `stations_i18n.json` only |
| `get_booking_links` | Static URLs |
| `holiday_check` | 공휴일 API (not TAGO train) |

## TAGO-consuming tools (read DB only)

| Tool | TAGO on user request |
|------|----------------------|
| `search_trains` | **0** |
| `compare_ktx_srt` | **0** (SQL filter KTX/SRT) |
| `plan_trip` | **0** |

## Deployment modes

| Mode | Where | User TAGO key |
|------|-------|---------------|
| **Hosted (default)** | Fly + Supabase | None |
| Local BYOK (dev) | `stdio` on laptop | Optional |

## Registry identity

- `io.github.plainfold/ktx-mcp`
- PyPI: `ktx-mcp` (BYOK dev path)
