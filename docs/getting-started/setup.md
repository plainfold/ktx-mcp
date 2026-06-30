# Setup Guide

## Recommended: keyless hosted (no API key)

For **travelers, ChatGPT, and Cursor users** — no [data.go.kr](https://www.data.go.kr) account required.

```json
{
  "mcpServers": {
    "ktx-mcp": {
      "url": "https://mcp.example.com/mcp",
      "headers": {}
    }
  }
}
```

> **Hosted URL:** not live yet — see [roadmap.md](../planning/roadmap.md).  
> Server holds the TAGO key; you only connect to the MCP endpoint.

**Why hosted first:** foreign users cannot easily register on the Korean public data portal. See [traffic.md](../engineering/traffic.md).

---

## Optional: self-host (developers / BYOK)

For local development or running your own instance with **your** TAGO key.

### Prerequisites

- Python **3.11+**
- [data.go.kr](https://www.data.go.kr) account (Korea residents / developers)
- TAGO train API key ([portal ID `15098552`](https://www.data.go.kr/data/15098552/openapi.do))

### 1. Get a TAGO API key (BYOK only)

1. Sign up at [data.go.kr](https://www.data.go.kr) (English: [/en/](https://www.data.go.kr/en/index.do)).
2. Open [TAGO 열차정보](https://www.data.go.kr/data/15098552/openapi.do).
3. Click **활용신청** (apply for use).
4. Copy the **일반 인증키 (Decoding)** service key.

**Traffic limits (your key):**

| Account | Daily TAGO limit |
|---------|------------------|
| Development | 10,000 |
| Production | Apply after use-case registration |

Hosted production uses **server-side** caching to stretch 10k/day — see [traffic.md](../engineering/traffic.md).

### 2. Install

```bash
git clone https://github.com/plainfold/ktx-mcp.git
cd ktx-mcp
pip install -e ".[dev]"
```

### 3. Configure environment

```bash
cp .env.example .env
# Set DATA_GO_KR_SERVICE_KEY in .env (server-side only — never commit)
```

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATA_GO_KR_SERVICE_KEY` | BYOK / server | — | TAGO key (**server only** for hosted) |
| `KTX_MCP_TRANSPORT` | No | `stdio` | `stdio` or `http` |
| `KTX_MCP_DEFAULT_LOCALE` | No | `en` | Response language |
| `KTX_MCP_CACHE_TTL` | No | `900` | Train cache TTL (seconds) |
| `REDIS_URL` | Hosted | — | Shared cache (required for multi-user) |

### 4. Smoke test TAGO

```bash
python scripts/smoke_tago.py
```

### 5. Run locally

```bash
ktx-mcp
```

### 6. Cursor (local BYOK)

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

### 7. Tests

```bash
pytest
```

---

## 한국어 요약

| 대상 | 방법 |
|------|------|
| **일반 사용자·외국인** | 호스팅 URL 연결 — **키 불필요** (준비 중) |
| **개발자** | 자가 호스팅 + `DATA_GO_KR_SERVICE_KEY` |

서버는 TAGO 일 **1만 건/일** 한도를 [캐시 전략](../engineering/traffic.md)으로 늘려 씁니다.
