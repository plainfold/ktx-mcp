# Pricing

Low entry price. Revenue from **MCP tool call volume** — not from TAGO upstream (server absorbs TAGO via cache).

## Default: keyless hosted

Users connect to a hosted URL. **No data.go.kr account or API key.**

See [TRAFFIC.md](./TRAFFIC.md) for how the server stretches the shared TAGO 10k/day budget.

## Tiers

| Tier | Price | Daily tool calls | Notes |
|------|-------|------------------|-------|
| **OSS (BYOK)** | Free | Unlimited* | Self-host only — **developers** |
| **Hosting Free** | Free | 500 | All 7 tools included |
| **Hosting Plus** | **$3/month** | 5,000 | Email support |
| **Overage** | **$0.50 / 1,000 calls** | — | Plus subscribers only |

## Two meters

| Meter | Free tier | Plus | Who pays TAGO |
|-------|-----------|------|---------------|
| **MCP tool calls** | 500/day | 5,000/day | — (our product limit) |
| **TAGO upstream** | — | — | **Server** (one shared key + cache) |

\* BYOK: user's own TAGO 10k/day — not the hosted pool.

## One-time products

| Product | Price | Contents |
|---------|-------|----------|
| **Gumroad Skill pack** | $2 | `ktx-trip-research` skill + `mcp.json` + prompts |
| **Ko-fi** | $1+ | Tip / support |

## What's included in every tier

- All v1.0 tools (`get_today_kst` through `plan_trip`)
- Multilingual responses (`en`, `ko`, `ja`, `zh`)
- Official booking links (no proxy booking)

## Revenue model

```
Free hosting (500 calls/day)
    → power users hit 80% limit
    → upsell Plus $3/mo
    → overage at $0.50/1k calls
    → affiliate clicks on get_booking_links
```

## Conservative monthly scenarios

| Monthly tool calls | Plus subs | Overage | Est. revenue |
|--------------------|-----------|---------|--------------|
| 10,000 | 2 | $0 | ~$6 |
| 50,000 | 15 | $5 | ~$50 |
| 200,000 | 50 | $40 | ~$190 |

## Not in v1

- ~~Solo $9 / Trip $29~~ (deprecated)
- B2B API ($199+) — Phase 5+ if demand exists

See [KTX_MCP_SPEC.md §11](./KTX_MCP_SPEC.md) for full commercial matrix.
