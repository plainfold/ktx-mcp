# ktx-mcp

**Ask in any language — get KTX/SRT schedules in one agent turn.**

MCP server for Korea **KTX and SRT** train schedules (TAGO public data).  
Hosted on **Fly.io** with timetables in **Supabase Postgres** — users need **no data.go.kr key**.

## Status

**Phase 1 (deploy-ready):** MCP tools, Postgres store, `/health`, `/internal/sync`, Korail KTX route sync (73 segments).  
See [docs/README.md](docs/README.md).

## Documentation

| Category | Start here |
|----------|------------|
| **Getting started** | [deploy](docs/getting-started/deploy.md) · [setup](docs/getting-started/setup.md) |
| **Product** | [tools](docs/product/tools.md) · [pricing](docs/product/pricing.md) |
| **Engineering** | [architecture](docs/engineering/architecture.md) · [traffic](docs/engineering/traffic.md) |
| **Planning** | [roadmap](docs/planning/roadmap.md) · [spec](docs/planning/spec.md) |
| **Legal** | [compliance](docs/legal/compliance.md) |

## Quick start (hosted)

```json
{
  "mcpServers": {
    "ktx-mcp": {
      "url": "https://ktx-mcp.fly.dev/mcp"
    }
  }
}
```

Deploy your own instance: [deploy guide](docs/getting-started/deploy.md).

## Demo

- EN: *What's the earliest KTX from Seoul to Busan tomorrow?*
- KO: *내일 서울에서 부산 가는 KTX 첫차·막차 알려줘*

More: [demo-queries](docs/product/demo-queries.md)

## Data sources

| Data | Source |
|------|--------|
| Timetables | [TAGO 15098552](https://www.data.go.kr/data/15098552/openapi.do) |
| KTX stations & sync routes | [Korail 15127571](https://www.data.go.kr/data/15127571/fileData.do) file |

Station names in search are **TAGO `nodename` (Korean)** or `NAT...` codes only.

## License

MIT — [LICENSE](LICENSE)
