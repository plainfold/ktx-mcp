# ktx-mcp

**Ask in any language — get KTX/SRT schedules in one agent turn.**

MCP server for Korea long-distance rail (KTX, SRT, ITX).  
**No API key required** — hosted on Fly.io, data on Supabase.

## Status

Phase 1 scaffold — MCP tools, in-memory timetable store, `/health` + `/internal/sync` (no Postgres yet). See [docs/README.md](docs/README.md).

## Documentation (5 categories)

| Category | Start here |
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

See [deploy guide](docs/getting-started/deploy.md).

## Demo

- EN: *What's the earliest KTX from Seoul to Busan tomorrow?*
- KO: *내일 서울에서 부산 가는 KTX 첫차·막차 알려줘*

More: [demo-queries](docs/product/demo-queries.md)

## License

MIT — [LICENSE](LICENSE)