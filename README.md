# ktx-mcp

**Ask in any language — get KTX/SRT schedules in one agent turn.**

MCP server for Korea long-distance rail (KTX, SRT, ITX) timetables.  
Data source: [TAGO train API](https://www.data.go.kr/data/15098552/openapi.do) (public data, commercial use allowed).

Supports natural-language queries in **English, Korean, Japanese, and Chinese**.

## Status

**Phase 0** — documentation and scaffold.  
`get_today_kst` is implemented; other tools are [specified](./docs/TOOLS.md) and in progress.

**Repository:** [github.com/plainfold/ktx-mcp](https://github.com/plainfold/ktx-mcp)

## Documentation

| Doc | Description |
|-----|-------------|
| [docs/SETUP.md](docs/SETUP.md) | Install & API key |
| [docs/TOOLS.md](docs/TOOLS.md) | MCP tool reference |
| [docs/LEGAL.md](docs/LEGAL.md) | License & disclaimers |
| [docs/ROADMAP.md](docs/ROADMAP.md) | Implementation plan |
| [docs/PRICING.md](docs/PRICING.md) | Hosting tiers |
| [docs/README.md](docs/README.md) | Full doc index |

## Quick start

1. Apply for a [data.go.kr](https://www.data.go.kr) API key (TAGO train info, ID `15098552`).
2. Install:

```bash
pip install -e ".[dev]"
export DATA_GO_KR_SERVICE_KEY="your-key"
ktx-mcp
```

3. Add to Cursor `mcp.json`:

```json
{
  "mcpServers": {
    "ktx-mcp": {
      "command": "uvx",
      "args": ["ktx-mcp"],
      "env": {
        "DATA_GO_KR_SERVICE_KEY": "YOUR_KEY"
      }
    }
  }
}
```

See [docs/SETUP.md](docs/SETUP.md) for Claude Desktop, smoke tests, and Windows notes.

## Demo queries

- EN: *What's the earliest KTX from Seoul to Busan tomorrow?*
- KO: *내일 서울에서 부산 가는 KTX 첫차·막차 알려줘*
- JA: *明日ソウルから釜山の一番早いKTXは？*
- ZH: *明天从首尔到釜山最早的高铁是几点？*

More: [docs/prompts/DEMO_QUERIES.md](docs/prompts/DEMO_QUERIES.md)

## Skills

Agent skill with 6-step SOP: [skills/ktx-trip-research/SKILL.md](skills/ktx-trip-research/SKILL.md)

## Repository layout

| Path | Purpose |
|------|---------|
| `src/ktx_mcp/` | MCP server implementation |
| `docs/` | User guides + product spec |
| `skills/` | L2 agent skills |
| `scripts/` | TAGO smoke test, registry scan |

## Data attribution

This service uses public data from the Ministry of Land, Infrastructure and Transport / National Public Transport Information Center (TAGO).

## License

MIT — see [LICENSE](LICENSE).

## Disclaimer

Timetable information only. Does not book tickets or guarantee seat availability. Use official Korail / SRT apps for booking. Not affiliated with Korail or SR.
