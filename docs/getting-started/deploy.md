# Deploy: Fly.io + Supabase

Official hosted stack.

| Service | Role |
|---------|------|
| **Supabase** | Postgres (`train_departures`), optional `pg_cron` → sync trigger |
| **Fly.io** | MCP HTTP (`/mcp`) + sync worker (`POST /internal/sync`) |

Users connect to Fly — **no data.go.kr key**, no Supabase credentials.

---

## Architecture

```text
User (Cursor / ChatGPT)
    → https://ktx-mcp.fly.dev/mcp
         → SELECT Supabase Postgres (pooler)
         ← timetable rows

pg_cron or manual trigger (every 30 min recommended)
    → POST https://ktx-mcp.fly.dev/internal/sync
         Header: X-Sync-Secret: <secret>
         → TAGO API (server key only)
         → UPSERT Postgres (73 KTX adjacent routes × 2 days)
```

**Fly region:** `nrt` (Tokyo).

---

## Prerequisites

- [Fly.io](https://fly.io) account + CLI (`fly auth login`)
- [Supabase](https://supabase.com) project
- [data.go.kr](https://www.data.go.kr) TAGO key ([15098552](https://www.data.go.kr/data/15098552/openapi.do)) — **server only**, never exposed to MCP clients

---

## 1. Supabase

### 1.1 Migration

```bash
python scripts/db_setup.py --migrate
python scripts/db_setup.py
```

Or paste `supabase/migrations/001_train_departures.sql` into the SQL Editor.

### 1.2 Connection string for Fly

| Variable | Supabase dashboard | Use on Fly |
|----------|-------------------|------------|
| `DATABASE_URL` | **Transaction pooler** `*.pooler.supabase.com:6543` | MCP reads + sync writes |

Local Windows dev: **Session pooler** `:5432` if direct `db.*` host fails (IPv6).

### 1.3 Seed sync route metadata (optional)

```bash
python scripts/seed_sync_routes.py
```

Populates `sync_routes` table (73 Korail KTX segments). The sync worker uses the in-repo route list; this table is for ops/dashboard later.

---

## 2. Fly.io

### 2.1 Create app (first time)

```bash
fly apps create ktx-mcp
fly secrets set \
  DATABASE_URL="postgresql://..." \
  DATA_GO_KR_SERVICE_KEY="..." \
  SYNC_SECRET="..." \
  KTX_MCP_TRANSPORT=http
```

`KTX_MCP_TRANSPORT` and `KTX_MCP_PORT` are also set in `fly.toml` `[env]`.

### 2.2 Deploy

```bash
fly deploy
```

### 2.3 Verify

```bash
curl https://ktx-mcp.fly.dev/health
```

Expected (with DB configured):

```json
{"status":"ok","store":"postgres","row_count":0,"transport":"http","database":"connected"}
```

### 2.4 Initial data sync

```bash
curl -X POST https://ktx-mcp.fly.dev/internal/sync \
  -H "Content-Type: application/json" \
  -H "X-Sync-Secret: YOUR_SYNC_SECRET"
```

Or from your machine (with `.env`):

```bash
python scripts/run_sync.py
```

Re-check `/health` — `row_count` should be > 0 after a successful sync (~73 routes × 2 days).

### 2.5 Logs

```bash
fly logs
fly status
```

---

## 3. Scheduled sync (pg_cron + pg_net)

Enable extensions: `pg_cron`, `pg_net`.

```sql
SELECT cron.schedule(
  'ktx-mcp-tago-sync',
  '*/30 * * * *',
  $$
  SELECT net.http_post(
    url := 'https://ktx-mcp.fly.dev/internal/sync',
    headers := jsonb_build_object(
      'Content-Type', 'application/json',
      'X-Sync-Secret', 'YOUR_SYNC_SECRET'
    ),
    body := '{}'::jsonb,
    timeout_milliseconds := 300000
  );
  $$
);
```

**TAGO budget:** 73 routes × 2 dates ≈ **146 calls** per full sync. At 30 min intervals ≈ 7k calls/day — within the 10k dev key limit.

---

## 4. Environment variables (Fly secrets)

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Yes | Supabase transaction pooler URL |
| `DATA_GO_KR_SERVICE_KEY` | Yes | TAGO Decoding key — sync worker only |
| `SYNC_SECRET` | Yes | `X-Sync-Secret` header for `/internal/sync` |
| `KTX_MCP_TRANSPORT` | Yes | `http` on Fly |
| `KTX_MCP_PORT` | No | `8080` (matches `fly.toml`) |
| `KTX_MCP_DEFAULT_LOCALE` | No | `en` |

Copy template: [env.template](env.template)

---

## 5. MCP client (keyless)

```json
{
  "mcpServers": {
    "ktx-mcp": {
      "url": "https://ktx-mcp.fly.dev/mcp"
    }
  }
}
```

---

## 6. Cost estimate

| Service | MVP |
|---------|-----|
| Supabase Free | $0 |
| Fly.io shared-cpu-1x (`nrt`) | ~$5–10/mo |

---

## 7. Local dev (same stack)

```bash
cp docs/getting-started/env.template .env
# Edit .env with your keys
pip install -e ".[dev]"
python scripts/db_setup.py --migrate
KTX_MCP_TRANSPORT=http ktx-mcp
```

---

## Deploy checklist

- [ ] `001_train_departures.sql` applied
- [ ] Fly secrets set (`DATABASE_URL`, `DATA_GO_KR_SERVICE_KEY`, `SYNC_SECRET`)
- [ ] `fly deploy` succeeds
- [ ] `GET /health` → `status: ok`, `database: connected`
- [ ] `POST /internal/sync` with `X-Sync-Secret` → `rows_upserted` > 0
- [ ] pg_cron job scheduled (or manual sync before demos)
- [ ] Cursor connects to `/mcp` without user API key
