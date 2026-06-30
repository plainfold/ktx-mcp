# Contributing

Thanks for helping improve ktx-mcp.

## Before you start

1. Read [LEGAL.md](./LEGAL.md) — we only use **TAGO** public data.
2. Read [TOOLS.md](./TOOLS.md) for the tool contract.
3. Do not add Korail scraping, KRIC rail portal, or booking features.

## Development setup

```bash
git clone https://github.com/plainfold/ktx-mcp.git
cd ktx-mcp
pip install -e ".[dev]"
cp .env.example .env   # add DATA_GO_KR_SERVICE_KEY
pytest
```

## Code style

- Python 3.11+
- `ruff` for lint/format
- Type hints on public functions
- Tool descriptions in **English**

## Pull requests

1. Fork → branch from `main`
2. One focused change per PR
3. Add tests for new behavior
4. Update [TOOLS.md](./TOOLS.md) if MCP tools change
5. Update [CHANGELOG.md](../CHANGELOG.md) under `Unreleased`

## Commit messages

```
feat: add search_stations with i18n aliases
fix: handle TAGO empty train list
docs: update SETUP for Windows
test: add Seoul→Busan fixture
```

## Reporting issues

Include:

- MCP client (Cursor, Claude Desktop, etc.)
- Tool name and inputs
- Expected vs actual (no API keys in issues)

## License

By contributing, you agree your contributions are licensed under the [MIT License](../LICENSE).
