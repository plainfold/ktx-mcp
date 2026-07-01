# Setup Guide

## Recommended: keyless hosted (no API key)

For travelers, ChatGPT, and Cursor users — no [data.go.kr](https://www.data.go.kr) account required.

```json
{
  "mcpServers": {
    "ktx-mcp": {
      "url": "https://ktx-mcp.fly.dev/mcp"
    }
  }
}
```

Deploy your own: [deploy.md](deploy.md).  
Server holds the TAGO key; clients only connect to `/mcp`.

---

## Optional: self-host (developers / BYOK)

### Prerequisites

- Python **3.11+**
- [data.go.kr](https://www.data.go.kr) account (for TAGO key)
- [TAGO 열차정보 15098552](https://www.data.go.kr/data/15098552/openapi.do) 활용신청

### 1. Install

```bash
git clone https://github.com/plainfold/ktx-mcp.git
cd ktx-mcp
pip install -e ".[dev]"
```

### 2. Environment

```bash
cp docs/getting-started/env.template .env
```

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATA_GO_KR_SERVICE_KEY` | BYOK / sync | — | TAGO Decoding key |
| `DATABASE_URL` | Postgres | — | Supabase pooler URL |
| `SYNC_SECRET` | Hosted sync | — | `X-Sync-Secret` for `/internal/sync` |
| `KTX_MCP_TRANSPORT` | No | `stdio` | `stdio` or `http` |
| `KTX_MCP_PORT` | No | `8080` | HTTP port |
| `KTX_MCP_DEFAULT_LOCALE` | No | `en` | Response language |

### 3. Smoke test TAGO

```bash
python scripts/smoke_tago.py
```

### 4. Station & route data (official sources only)

| Script / file | Role |
|---------------|------|
| `scripts/fetch_korail_ktx_lines.py` | [15127571](https://www.data.go.kr/data/15127571/fileData.do) → `ktx_line_stations.json` |
| `priority_station_codes.json` | KTX 정차역 TAGO `nodeid` 목록 (70) |
| `scripts/build_stations.py` | TAGO API → `stations_i18n.json` |
| `scripts/list_regional_stations.py` | 지역별 역 목록 출력 (검증용) |

- `search_stations`: TAGO `nodename`(한글) 또는 `NAT...` 코드만
- Wiki·수동 en/ja/zh 별칭 **금지** — [compliance.md](../legal/compliance.md)

### 5. Database

```bash
python scripts/db_setup.py --migrate
python scripts/seed_sync_routes.py    # optional metadata
python scripts/run_sync.py            # TAGO → Postgres
```

| Supabase URL | Port | Note |
|--------------|------|------|
| Session pooler | `:5432` | Local dev (IPv4) |
| Transaction pooler | `:6543` | Fly production reads |

### 6. Run

**stdio (Cursor local):**

```bash
ktx-mcp
```

**http (matches Fly):**

```bash
KTX_MCP_TRANSPORT=http ktx-mcp
curl http://localhost:8080/health
```

### 7. Cursor (local BYOK)

```json
{
  "mcpServers": {
    "ktx-mcp": {
      "command": "uvx",
      "args": ["ktx-mcp"],
      "env": {
        "DATA_GO_KR_SERVICE_KEY": "YOUR_KEY",
        "DATABASE_URL": "postgresql://..."
      }
    }
  }
}
```

### 8. Tests

```bash
pytest
ruff check src tests scripts
```

---

## 한국어 요약

| 대상 | 방법 |
|------|------|
| **일반 사용자** | 호스팅 URL — 키 불필요 |
| **운영자** | Fly + Supabase — [deploy.md](deploy.md) |
| **개발자** | `.env` + `pip install -e ".[dev]"` |

TAGO 일 1만 건 한도는 [traffic.md](../engineering/traffic.md) 캐시 전략으로 운영합니다.
