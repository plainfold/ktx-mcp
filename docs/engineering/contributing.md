# Contributing

Thanks for helping improve ktx-mcp.

## Before you start

1. Read [compliance.md](../legal/compliance.md) — official TAGO + Korail file data only.
2. Read [tools.md](../product/tools.md) for the tool contract.
3. Do not add Korail scraping, KRIC rail portal, or booking features.

## Development setup

```bash
git clone https://github.com/plainfold/ktx-mcp.git
cd ktx-mcp
pip install -e ".[dev]"
cp docs/getting-started/env.template .env
pytest
```

## Code style

- Python 3.11+
- `ruff check src tests scripts`
- Type hints on public functions
- Tool descriptions in **English**

## Pull requests

1. Fork → branch from `main`
2. One focused change per PR
3. Add tests for new behavior
4. Update [tools.md](../product/tools.md) if MCP tools change
5. Update [CHANGELOG.md](../../CHANGELOG.md) under `Unreleased`

## Commit messages

```
feat: add postgres timetable store
fix: repair http routes import for fly deploy
docs: update deploy checklist
test: add sync route coverage
```

## Reporting issues

Include MCP client, tool name, inputs, expected vs actual (no API keys).

## License

Contributions are MIT — see [LICENSE](../../LICENSE).
