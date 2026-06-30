# Roadmap

12-week plan from [KTX_MCP_SPEC.md](./KTX_MCP_SPEC.md).  
**Current phase:** Phase 0 complete (scaffold + docs). Phase 1 next.

## Timeline

```
W1-2   Phase 0-1  MVP + i18n station aliases
W3-4   Phase 2    PyPI + compare + holiday + plan_trip
W5-6   Phase 3    Gumroad Skill $2 + Registry
W7-9   Phase 4    Hosted MCP ($3/mo) + rate limits
W10-12 Phase 5    v1.0 release
```

## Phase 0 — Preparation ✅

| ID | Task | Status |
|----|------|--------|
| 0.1 | data.go.kr account | Manual |
| 0.2 | TAGO API application | Manual |
| 0.3 | License screenshots → `docs/legal/` | Pending |
| 0.4 | Repo scaffold (`plainfold/ktx-mcp`) | Done |
| 0.5 | `scripts/smoke_tago.py` | Done |
| 0.6 | Documentation set | Done |

## Phase 1 — Local MVP (2 weeks)

| ID | Task | Done when |
|----|------|-----------|
| 1.1 | `TagoAdapter` + `stations_i18n.json` | Seoul/Busan EN·JA·ZH resolve |
| 1.2 | `get_today_kst`, `search_stations` | pytest green |
| 1.3 | `search_trains` | Seoul→Busan tomorrow ≥1 result |
| 1.4 | FastMCP stdio + Cursor demo | 1-turn answer |
| 1.5 | README Quick Start verified | 5-minute install |

## Phase 2 — Differentiation + PyPI (2 weeks)

| ID | Task |
|----|------|
| 2.1 | `compare_ktx_srt` |
| 2.2 | `holiday_check` |
| 2.3 | `get_booking_links` |
| 2.4 | English tool descriptions + `locale` |
| 2.5 | `plan_trip` (en/ko/ja/zh) |
| 2.6 | PyPI publish `uvx ktx-mcp` |
| 2.7 | `server.json` for MCP Registry |

## Phase 3 — First revenue (2 weeks)

| ID | Task | Goal |
|----|------|------|
| 3.1 | Skill `ktx-trip-research` | Complete |
| 3.2 | Gumroad $2 pack | First sale |
| 3.3 | PulseMCP + Registry | Traffic |
| 3.4 | awesome-mcp-korea PR | Listing |

## Phase 4 — Hosted MCP (3 weeks)

| ID | Task |
|----|------|
| 4.1 | data.go.kr production key + use case |
| 4.2 | Streamable HTTP server |
| 4.3 | Rate limits: Free 500 / Plus 5,000 calls per day |
| 4.4 | Polar $3/mo + overage billing |
| 4.5 | ChatGPT Connector landing |

## Phase 5 — v1.0 (2 weeks)

| ID | Task |
|----|------|
| 5.1 | pytest 30+ cases, GitHub Actions CI |
| 5.2 | Smithery, Glama registration |
| 5.3 | Demo video (EN + KO subtitles) |
| 5.4 | Tag `v1.0.0` |

## Success metrics

| Milestone | Target |
|-----------|--------|
| MVP | EN: *earliest KTX Seoul to Busan tomorrow* → 1 turn |
| Revenue | Gumroad $2 or Ko-fi $1+ |
| Volume | 10,000 hosted tool calls / week |
| MRR | 10× Plus $3/mo or $5+ overage |

## Out of scope (all phases)

- Ticket booking / payment
- Real-time seat availability
- KRIC rail portal API
- Seoul subway / bus (see `korea-transit-mcp`)
