# Setup Guide

## Prerequisites

- Python **3.11+**
- [data.go.kr](https://www.data.go.kr) account
- TAGO **train info** API key ([portal ID `15098552`](https://www.data.go.kr/data/15098552/openapi.do))

## 1. Get a TAGO API key

1. Sign up at [data.go.kr](https://www.data.go.kr).
2. Open [국토교통부 TAGO 열차정보](https://www.data.go.kr/data/15098552/openapi.do).
3. Click **활용신청** (apply for use).
4. Copy the **일반 인증키 (Decoding)** service key.

**License:** 이용허락범위 **제한 없음** (type 0). Commercial use is allowed.  
See [LEGAL.md](./LEGAL.md) and [TAGO policy](https://www.tago.go.kr/v5/notice/publicData.jsp).

**Traffic limits:**

| Account | Daily limit |
|---------|-------------|
| Development | 10,000 calls |
| Production | Apply after registering a use case |

## 2. Install locally

```bash
git clone https://github.com/plainfold/ktx-mcp.git
cd ktx-mcp
pip install -e ".[dev]"
```

Or without cloning:

```bash
pip install ktx-mcp   # after PyPI publish
```

## 3. Configure environment

Copy the example file:

```bash
cp .env.example .env
```

Set your key:

```bash
# Windows PowerShell
$env:DATA_GO_KR_SERVICE_KEY = "your-decoding-key"

# macOS / Linux
export DATA_GO_KR_SERVICE_KEY="your-decoding-key"
```

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATA_GO_KR_SERVICE_KEY` | Yes (local BYOK) | — | data.go.kr service key |
| `KTX_MCP_TRANSPORT` | No | `stdio` | `stdio` or `http` |
| `KTX_MCP_DEFAULT_LOCALE` | No | `en` | Response language for `summary` |
| `KTX_MCP_CACHE_TTL` | No | `600` | Cache TTL in seconds |

## 4. Smoke test TAGO

```bash
python scripts/smoke_tago.py
```

Expect HTTP 200 and JSON from TAGO. If you see auth errors, verify the decoding key.

## 5. Run the MCP server

```bash
ktx-mcp
# or
uv run ktx-mcp
```

## 6. Cursor configuration

Add to `.cursor/mcp.json` or Cursor Settings → MCP:

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

For local development:

```json
{
  "mcpServers": {
    "ktx-mcp": {
      "command": "python",
      "args": ["-m", "ktx_mcp.server"],
      "cwd": "C:\\path\\to\\ktx-mcp",
      "env": {
        "DATA_GO_KR_SERVICE_KEY": "YOUR_KEY"
      }
    }
  }
}
```

## 7. Claude Desktop

Edit `claude_desktop_config.json`:

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

## 8. Run tests

```bash
pytest
```

Live TAGO tests (optional):

```bash
DATA_GO_KR_SERVICE_KEY=... pytest -m live
```

---

## 한국어 요약

1. [공공데이터포털](https://www.data.go.kr/data/15098552/openapi.do)에서 TAGO 열차정보 API 키 발급  
2. `pip install -e ".[dev]"`  
3. `DATA_GO_KR_SERVICE_KEY` 환경 변수 설정  
4. Cursor `mcp.json`에 서버 등록  
5. 데모 질문: *「내일 서울에서 부산 KTX 몇 시 있어?」*
