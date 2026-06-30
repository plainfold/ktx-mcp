# ktx-mcp

**Ask in any language — get KTX/SRT schedules in one agent turn.**

MCP server for Korea long-distance rail (KTX, SRT, ITX) timetables.  
Data source: [TAGO train API](https://www.data.go.kr/data/15098552/openapi.do) (public data, commercial use allowed).

Supports natural-language queries in **English, Korean, Japanese, and Chinese**.

## Status

Early scaffold — see [docs/KTX_MCP_SPEC.md](docs/KTX_MCP_SPEC.md) for the full product spec.

## Quick start (local)

1. Apply for a [data.go.kr](https://www.data.go.kr) API key (TAGO train info, ID `15098552`).
2. Install and run:

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

## Demo queries

- EN: *What's the earliest KTX from Seoul to Busan tomorrow?*
- KO: *내일 서울에서 부산 가는 KTX 첫차·막차 알려줘*
- JA: *明日ソウルから釜山の一番早いKTXは？*
- ZH: *明天从首尔到釜山最早的高铁是几点？*

## Repository layout

| Path | Purpose |
|------|---------|
| `src/ktx_mcp/` | MCP server implementation |
| `docs/` | Product spec & demand research |
| `scripts/` | TAGO smoke test, registry scan |
| `skills/` | L2 agent skills |

## Data attribution

This service uses public data from the Ministry of Land, Infrastructure and Transport / National Public Transport Information Center (TAGO).

Source: Ministry of Land, Infrastructure and Transport / TAGO

## License

MIT — see [LICENSE](LICENSE).

## Disclaimer

This MCP provides timetable information only. It does not book tickets or guarantee seat availability. Use official Korail / SRT apps for booking.
