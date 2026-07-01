# Roadmap

**P0:**

1. **Keyless hosted MCP** — users never apply for data.go.kr keys  
2. **TAGO 10k/day survival** — [traffic.md](../engineering/traffic.md) DB materialization  

**Current phase:** Phase 1 — **deploy-ready** (Fly + Supabase + sync).

**Infrastructure:** Fly.io (`nrt`) + Supabase — [deploy.md](../getting-started/deploy.md).

## Phase 0 — Preparation ✅

| ID | Task | Status |
|----|------|--------|
| 0.4 | Repo `plainfold/ktx-mcp` | Done |
| 0.5 | `smoke_tago.py` | Done |
| 0.6 | Documentation | Done |

## Phase 1 — Hosted keyless + traffic **← NOW**

| ID | Task | Status |
|----|------|--------|
| 1.0 | Supabase migration + `PostgresTimetableStore` | Done |
| 1.1 | Fly deploy (`fly.toml`, `Dockerfile`) | Ready — `fly deploy` |
| 1.2 | `/internal/sync` + `run_sync.py` | Done |
| 1.3 | `search_trains` / `compare_ktx_srt` read DB | Done |
| 1.4 | Korail 15127571 sync routes (73 segments) | Done |
| 1.5 | Streamable HTTP hosted server | Done |
| 1.6 | pg_cron on Supabase | Ops — see deploy.md |
| 1.7 | `tago_calls_today` metrics | Todo |

**Exit criteria:** MCP request path → **0 TAGO**; full sync < 4,000 TAGO/day at 30 min cron.

**Deferred:** [15125762](https://www.data.go.kr/data/15125762/openapi.do) Korail run API — official sample broken; not used.

## Phase 2 — Distribution (2 weeks)

| ID | Task |
|----|------|
| 2.1 | PyPI `uvx ktx-mcp` (BYOK path) |
| 2.2 | `server.json` Registry |
| 2.3 | `locale` summaries polish |

## Phase 3 — Scale + distribution

Pre-warm top KTX/SRT routes, ops TAGO key, Smithery / PulseMCP.

## Phase 4 — Monetization

Plus $3/mo, rate limits.

## Phase 5 — v1.0

pytest 30+, demo video, tag `v1.0.0`.

## Success metrics

| Milestone | Target |
|-----------|--------|
| **P0 traffic** | `tago_calls / mcp_calls` < **0.2** |
| **P0 hosted** | Foreign user connects with **zero** portal signup |
| MVP | EN Seoul→Busan 1 turn, keyless |

## Out of scope

- User-facing BYOK as default
- Ticket booking / seat availability
- Korail 15125762 until API is stable
- KRIC rail portal API
