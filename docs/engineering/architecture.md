# Architecture

**Scope:** KTX/SRT timetables only.  
**P0:** [traffic.md](./traffic.md) — keyless hosted + TAGO 10k/day via DB cache.

## Hosted stack

| Layer | Service |
|-------|---------|
| Compute | Fly.io (`nrt`) — MCP HTTP + `/internal/sync` |
| Database | Supabase Postgres — `train_departures` |
| Scheduler | pg_cron → `POST /internal/sync` |

Deploy: [deploy.md](../getting-started/deploy.md)

## Application stack

| Layer | Choice |
|-------|--------|
| Language | Python 3.11+ |
| MCP | FastMCP 2.x |
| DB | asyncpg |
| Models | Pydantic v2 |

## Data flow

```text
MCP /mcp → Postgres SELECT (0 TAGO on request)

pg_cron → POST /internal/sync → TAGO → UPSERT (KTX/SRT rows only)
```

## Tools vs TAGO

| Tool | TAGO on user request |
|------|----------------------|
| `get_today_kst` | 0 |
| `search_stations` | 0 (static catalog) |
| `search_trains` | 0 |
| `compare_ktx_srt` | 0 |

## Deployment modes

| Mode | User TAGO key |
|------|---------------|
| Hosted (default) | None |
| Local BYOK | Optional |

Registry: `io.github.plainfold/ktx-mcp`
