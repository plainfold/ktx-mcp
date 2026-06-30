# Roadmap

**P0 (before everything else):**

1. **Keyless hosted MCP** — users never apply for data.go.kr keys  
2. **TAGO 10k/day survival** — [traffic.md](../engineering/traffic.md) cache stack  

12-week plan from [spec.md](./spec.md).  
**Current phase:** Phase 0 done → **Phase 1 = hosted + cache**.

**Infrastructure:** Fly.io (`nrt`) + Supabase — see [deploy.md](../getting-started/deploy.md).

## Timeline (reordered)

```
W1-2   Phase 1  Supabase schema + Fly deploy + sync worker
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
| 1.0 | Supabase migration + `TimetableStore` | `train_departures` live |
| 1.1 | Fly deploy (`fly.toml`, `Dockerfile`) | `/health` 200 |
| 1.2 | `/internal/sync` + pg_cron on Supabase | TAGO → DB |
| 1.2 | `search_stations` static-only | EN/JA/ZH resolve |
| 1.3 | `search_trains` / `compare_ktx_srt` read DB only | Seoul→Busan |
| 1.4 | `tago_calls_today` on sync worker + metrics | Dashboard / logs |
| 1.5 | **Streamable HTTP** hosted server | Client needs **no key** |
| 1.6 | On-demand sync for long-tail routes (capped) | [traffic.md](../engineering/traffic.md) |

**Exit criteria:** 100 simulated users × 6 MCP calls → **0 TAGO on request path**; sync < 4,000 TAGO/day.

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
