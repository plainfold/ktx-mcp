# Pricing

Revenue from **MCP tool call volume**. TAGO upstream is server-side cache (see [traffic.md](../engineering/traffic.md)).

## Hosted (keyless)

Users connect to a URL — **no data.go.kr key**.

## Tiers

| Tier | Price | Daily MCP calls |
|------|-------|-----------------|
| **OSS (BYOK)** | Free | Unlimited* (self-host) |
| **Hosting Free** | Free | 500 |
| **Hosting Plus** | $3/month | 5,000 |
| **Overage** | $0.50 / 1,000 calls | Plus only |

\* BYOK uses your own TAGO 10k/day quota.

## Included tools (KTX/SRT)

- `get_today_kst`
- `search_stations`
- `search_trains`
- `compare_ktx_srt`

Multilingual `summary`: `en`, `ko`, `ja`, `zh`.

See [spec.md](../planning/spec.md) for product scope.
