# Roadmap

**P0 (before everything else):**

1. **Keyless hosted MCP** — users never apply for data.go.kr keys  
2. **TAGO 10k/day survival** — [TRAFFIC.md](./TRAFFIC.md) cache stack  

12-week plan from [KTX_MCP_SPEC.md](./KTX_MCP_SPEC.md).  
**Current phase:** Phase 0 done → **Phase 1 = hosted + cache**.

## Timeline (reordered)

```
W1-2   Phase 1  TagoGateway + cache + hosted HTTP (keyless)
W3-4   Phase 2  Full tools (stations, trains, compare, plan_trip)
W5-6   Phase 3  Pre-warm + ops key + Registry / Smithery
W7-8   Phase 4  Plus billing + traffic dashboard
W9-12  Phase 5  v1.0 + GTM
```

## Phase 0 — Preparation ✅

| ID | Task | Status |
|----|------|--------|
| 0.4 | Repo `plainfold/ktx-mcp` | Done |
| 0.5 | `smoke_tago.py` | Done |
| 0.6 | Documentation | Done |

## Phase 1 — Hosted keyless + traffic (2 weeks) **← NOW**

| ID | Task | Done when |
|----|------|-----------|
| 1.0 | **`TagoGateway`** + Redis/in-memory cache | Unit tests for hit/miss |
| 1.1 | **`search_stations`** static-only (no per-user TAGO) | EN/JA/ZH resolve |
| 1.2 | **`search_trains`** via gateway (1 TAGO per route/date) | Seoul→Busan |
| 1.3 | **`compare_ktx_srt`** single TAGO fetch | KTX/SRT split in memory |
| 1.4 | Request-scoped dedup + `tago_calls_today` metric | Dashboard / logs |
| 1.5 | **Streamable HTTP** hosted server | Client needs **no key** |
| 1.6 | Stale-while-revalidate at 80% daily budget | Spec in TRAFFIC.md |

**Exit criteria:** 100 simulated users × 6 MCP calls → **< 2,000 TAGO calls/day** (cache on).

## Phase 2 — Full MCP surface (2 weeks)

| ID | Task |
|----|------|
| 2.1 | `holiday_check`, `get_booking_links`, `plan_trip` |
| 2.2 | `locale` summaries (en/ko/ja/zh) |
| 2.3 | PyPI `uvx ktx-mcp` (BYOK path for devs) |
| 2.4 | `server.json` Registry |

## Phase 3 — Scale TAGO quota + distribution (2 weeks)

| ID | Task |
|----|------|
| 3.1 | data.go.kr **use case** + **production key** |
| 3.2 | Traffic increase application |
| 3.3 | Pre-warm top 20 routes (04:00 KST cron) |
| 3.4 | PulseMCP, Smithery, ChatGPT Connector |

## Phase 4 — Monetization (2 weeks)

| ID | Task |
|----|------|
| 4.1 | MCP rate limit: Free 500 / Plus 5,000 per user |
| 4.2 | Polar $3/mo + overage |
| 4.3 | Gumroad Skill $2 |

## Phase 5 — v1.0 (2 weeks)

| ID | Task |
|----|------|
| 5.1 | pytest 30+, CI |
| 5.2 | Demo video (EN) |
| 5.3 | Tag `v1.0.0` |

## Success metrics

| Milestone | Target |
|-----------|--------|
| **P0 traffic** | `tago_calls / mcp_calls` < **0.2** at steady state |
| **P0 hosted** | Foreign user connects with **zero** portal signup |
| MVP | EN Seoul→Busan 1 turn, keyless |
| Scale | Ops key → **50k+ TAGO/day** before marketing |

## Out of scope

- User-facing BYOK as default path
- Ticket booking / seat availability
- KRIC rail portal API
