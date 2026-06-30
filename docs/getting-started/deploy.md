# Deploy: Fly.io + Supabase

Official hosted stack. **You already have both accounts** — no Railway required.

| Service | Role |
|---------|------|
| **Supabase** | Postgres (`train_departures`), pg_cron → sync trigger, Vault (secrets) |
| **Fly.io** | Python app: MCP HTTP + `/internal/sync` worker endpoint |

Users connect to Fly — **no data.go.kr key**, no Supabase credentials.

---

## Architecture

```text
User (Cursor / ChatGPT)
    → https://ktx-mcp.fly.dev/mcp
         → SELECT Supabase Postgres (pooler)
         ← timetable rows

Supabase pg_cron (every 30 min)
    → POST https://ktx-mcp.fly.dev/internal/sync
         → TAGO API (server key only)
         → UPSERT Supabase Postgres
```

**Fly region:** `nrt` (Tokyo) — low latency to TAGO / Korean users.

---

## 1. Supabase setup

### 1.1 Run migration

From repo root (with [Supabase CLI](https://supabase.com/docs/guides/cli)):

```bash
supabase link --project-ref YOUR_PROJECT_REF
supabase db push
```

Or paste SQL from `supabase/migrations/001_train_departures.sql` into the SQL Editor.

### 1.2 Secrets (Vault)

Store in Supabase Vault or project secrets (for pg_cron HTTP):

| Secret | Value |
|--------|-------|
| `fly_sync_url` | `https://ktx-mcp.fly.dev/internal/sync` |
| `sync_secret` | Random string — same as Fly `SYNC_SECRET` |

### 1.3 Schedule sync (pg_cron + pg_net)

Enable extensions: `pg_cron`, `pg_net`.

```sql
-- Every 30 minutes: trigger Fly sync worker
SELECT cron.schedule(
  'tago-sync-hot-routes',
  '*/30 * * * *',
  $$
  SELECT net.http_post(
    url := 'https://ktx-mcp.fly.dev/internal/sync',
    headers := jsonb_build_object(
      'Content-Type', 'application/json',
      'Authorization', 'Bearer YOUR_SYNC_SECRET'
    ),
    body := jsonb_build_object('mode', 'hot'),
    timeout_milliseconds := 120000
  );
  $$
);
```

See [Supabase schedule functions](https://supabase.com/docs/guides/functions/schedule-functions).

### 1.4 Connection strings for Fly

In Supabase → Project Settings → Database:

| Variable | Use |
|----------|-----|
| `DATABASE_URL` | **Transaction pooler** (port 6543) — MCP reads |
| `SUPABASE_SERVICE_ROLE_KEY` | Optional admin tasks |

Set as Fly secrets (never in git).

---

## 2. Fly.io setup

### 2.1 Install CLI

```bash
fly auth login
```

### 2.2 Create app (first time)

```bash
fly apps create ktx-mcp
fly secrets set \
  DATABASE_URL="postgresql://..." \
  DATA_GO_KR_SERVICE_KEY="..." \
  SYNC_SECRET="..." \
  KTX_MCP_TRANSPORT=http
```

### 2.3 Deploy

```bash
fly deploy
```

### 2.4 Verify

```bash
fly status
fly logs
curl https://ktx-mcp.fly.dev/health
```

### 2.5 Custom domain (optional)

```bash
fly certs add mcp.yourdomain.com
```

Update Cursor `mcp.json` with the public URL.

---

## 3. Environment variables (Fly)

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Yes | Supabase pooler URL |
| `DATA_GO_KR_SERVICE_KEY` | Yes | TAGO key — **sync only** |
| `SYNC_SECRET` | Yes | Protects `/internal/sync` |
| `KTX_MCP_TRANSPORT` | Yes | `http` on Fly |
| `KTX_MCP_PORT` | No | `8080` (fly.toml internal_port) |
| `KTX_MCP_DEFAULT_LOCALE` | No | `en` |

**Not on Fly (users):** no client TAGO key.

---

## 4. MCP client config (keyless)

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

## 5. Cost estimate

| Service | MVP |
|---------|-----|
| Supabase Free | $0 (500 MB DB enough) |
| Fly.io | ~$5–10/mo (shared-cpu-1x, `nrt`) |
| **Total** | **~$5–10/mo** |

Skip Redis until Postgres read latency matters.

---

## 6. Local dev with same stack

```bash
cp .env.example .env
# DATABASE_URL = Supabase local or remote pooler
pip install -e ".[dev]"
KTX_MCP_TRANSPORT=http ktx-mcp
```

---

## Checklist

- [ ] Supabase migration applied
- [ ] pg_cron job scheduled
- [ ] Fly app deployed (`nrt`)
- [ ] Secrets set on Fly
- [ ] `/health` returns 200
- [ ] Manual `POST /internal/sync` fills `train_departures`
- [ ] Cursor connects to `/mcp` without user API key
