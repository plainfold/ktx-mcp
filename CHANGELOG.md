# Changelog

## [Unreleased]

### Added

- Postgres `PostgresTimetableStore` (asyncpg) with Supabase SSL
- Korail [15127571](https://www.data.go.kr/data/15127571/fileData.do) KTX line data: 70 stations, 73 sync routes
- HTTP `/health` and `/internal/sync` (`X-Sync-Secret`)
- Scripts: `db_setup.py`, `run_sync.py`, `seed_sync_routes.py`, `fetch_korail_ktx_lines.py`, `list_regional_stations.py`
- CI workflow (pytest + ruff)
- [env.template](docs/getting-started/env.template)

### Changed

- **Product scope docs** — KTX/SRT only; ITX·holiday·plan_trip 등 제거
- **spec.md** slim rewrite (v2.0) focused on KTX/SRT
- Sync/search filter: **KTX·SRT rows only** (ITX excluded at ingest and query)
- `search_stations` matches Korean TAGO names or `NAT...` codes only
- Deploy docs aligned with `X-Sync-Secret`, TAGO sync budget, checklist
- Roadmap: Phase 1 deploy-ready; [15125762](https://www.data.go.kr/data/15125762/openapi.do) deferred (API unstable)

### Fixed

- `http/routes.py` import error that blocked Docker/Fly startup

## [0.1.0] - 2026-06-30

### Added

- Project scaffold (`src/ktx_mcp`)
- `get_today_kst` MCP tool
- TAGO smoke test (`scripts/smoke_tago.py`)
- In-memory timetable store + sync worker scaffold
