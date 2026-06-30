# ktx-mcp

**Ask in any language — get KTX/SRT schedules in one agent turn.**

MCP server for Korea long-distance rail (KTX, SRT, ITX) timetables.  
**No API key required** — connect to hosted MCP (TAGO key on server).

Data: [TAGO train API](https://www.data.go.kr/data/15098552/openapi.do) (public data, commercial use allowed).

## Status

**Phase 1 (P0):** keyless hosted MCP + TAGO 10k/day cache strategy.  
See [docs/TRAFFIC.md](docs/TRAFFIC.md).

**Repository:** [github.com/plainfold/ktx-mcp](https://github.com/plainfold/ktx-mcp)

## Quick start (hosted — recommended)

No data.go.kr signup. Connect in Cursor / ChatGPT:

```json
{
  "mcpServers": {
    "ktx-mcp": {
      "url": "https://mcp.example.com/mcp"
    }
  }
}
```

> Hosted URL coming in Phase 1. Track [ROADMAP.md](docs/ROADMAP.md).

## Quick start (developers — BYOK)

Optional self-host with your own TAGO key: [docs/SETUP.md](docs/SETUP.md).

## Documentation

| Doc | Description |
|-----|-------------|
| [docs/TRAFFIC.md](docs/TRAFFIC.md) | **P0** — cache & 10k/day strategy |
| [docs/SETUP.md](docs/SETUP.md) | Hosted + BYOK setup |
| [docs/TOOLS.md](docs/TOOLS.md) | MCP tool reference |
| [docs/ROADMAP.md](docs/ROADMAP.md) | Implementation plan |
| [docs/README.md](docs/README.md) | Full index |

## Demo queries

- EN: *What's the earliest KTX from Seoul to Busan tomorrow?*
- KO: *내일 서울에서 부산 가는 KTX 첫차·막차 알려줘*
- JA: *明日ソウルから釜山の一番早いKTXは？*
- ZH: *明天从首尔到釜山最早的高铁是几点？*

## License

MIT — see [LICENSE](LICENSE).

## Disclaimer

Timetable reference only. Not affiliated with Korail or SR. Book via official apps.
