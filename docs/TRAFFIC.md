# Traffic Strategy (P0)

**Top priority:** run **keyless hosted MCP** for global users while staying under the TAGO **10,000 calls/day** ceiling (development key), then scale via operations + cache — not by asking foreigners to sign up at [data.go.kr](https://www.data.go.kr).

## Two meters (do not confuse)

| Meter | What counts | Limit | Who cares |
|-------|-------------|-------|-----------|
| **MCP tool calls** | Each `@tool` invocation | Free 500 / Plus 5,000 per user per day | Product, billing, Skill SOP |
| **TAGO upstream calls** | HTTP to TAGO train API | **10,000/day** (dev key) → higher after ops approval | Infra, cache design |

**Goal:** maximize MCP tool calls, **minimize** TAGO upstream calls.

```
Many MCP calls  ──►  few TAGO calls  (cache + dedup + static data)
```

---

## Product default: keyless hosted

| User | Experience |
|------|------------|
| **Traveler / ChatGPT / Cursor** | Connect hosted URL — **no API key**, no data.go.kr account |
| **Developer (optional)** | Self-host with own `DATA_GO_KR_SERVICE_KEY` (BYOK) |

Foreign users cannot reliably complete Korean portal signup → **hosted is not optional for GTM, it is the product.**

Server holds **one** TAGO service key. All users share the **10k/day** pool until production quota is raised.

---

## Naive vs optimized (1 user question)

Skill SOP triggers **6–7 MCP tool calls**. TAGO cost depends on implementation:

| Tool | TAGO calls (naive) | TAGO calls (optimized) |
|------|-------------------|------------------------|
| `get_today_kst` | 0 | 0 |
| `search_stations` ×2 | 0–2 | **0** (static `stations_i18n.json`) |
| `holiday_check` | 0* | 0* (*separate 공휴일 API, not TAGO train) |
| `search_trains` | 1 | 0–1 (cache hit = 0) |
| `compare_ktx_srt` | 2 | **0–1** (one fetch, split in memory) |
| `plan_trip` | +1 internal | **0** (reuse same request cache) |
| `get_booking_links` | 0 | 0 |

| Scenario | TAGO / question | Questions / day @ 10k TAGO |
|----------|-----------------|----------------------------|
| **Naive** | ~3 | ~3,300 |
| **Optimized** | **~1** | **~10,000** |
| **Optimized + 15m cache** (repeat routes) | ~0.2 effective | **~50,000+** equivalent |

---

## Layered defense (implementation order)

### L1 — Zero-TAGO tools (Week 1)

- `search_stations` → **only** `stations_i18n.json` + TAGO city list synced **daily** (1 TAGO job, not per user)
- `get_today_kst`, `get_booking_links` → no upstream
- `holiday_check` → 천문연 공휴일 API (separate quota)

### L2 — `TagoGateway` single entry (Week 1)

All train timetable reads go through one module:

```text
tools → TagoGateway.get_trains(dep, arr, date) → cache → HTTP
```

- `search_trains` and `compare_ktx_srt` **must not** call TAGO separately for the same `(dep, arr, date)`.
- `compare_ktx_srt` = one TAGO response, partition KTX vs SRT in Python.
- `plan_trip` = read from **request-scoped cache** only.

### L3 — TTL cache (Week 1–2)

| Cache key | TTL | Notes |
|-----------|-----|-------|
| `trains:{dep_code}:{arr_code}:{date}` | **15 min** default | Timetables rarely change minute-to-minute |
| `trains:...` (top-20 routes) | **30 min** | Seoul–Busan, Suseo–Busan, etc. |
| `stations:manifest` | **24 h** | Background refresh, not user-triggered |
| `holiday:{year}` | **7 d** | |

Hosted: **Redis** (shared across instances).  
Local dev: in-memory LRU.

### L4 — In-flight deduplication (Week 2)

Concurrent identical `(dep, arr, date)` → **one** TAGO request, others await (singleflight pattern).

### L5 — Stale-while-revalidate (Week 2–3)

When TAGO daily budget > 80%:

- Serve cache up to **60 min** stale with `disclaimer: "cached, may not reflect latest"`.
- Block only on cache miss + budget exhausted.

### L6 — Pre-warm (Week 3)

Cron at **04:00 KST** (before morning peak):

- Top **20 routes** × **today + tomorrow** = ≤40 TAGO calls/day fixed cost.
- Covers majority of tourist queries.

### L7 — Operational quota (Week 3–4, parallel)

1. Register **use case** on data.go.kr (hosted AI agent MCP, no booking).
2. Apply for **production / operations** key.
3. Request **traffic increase** (활용사례 등록 후 증설 신청).

Target: move from 10k → 100k+ TAGO/day before marketing push.

### L8 — MCP-side rate limit (protect TAGO pool)

Even with cache, cap **per-user** MCP calls (500 Free) so one bot cannot burn the shared TAGO budget.

---

## Budget dashboard (required metrics)

Log and alert on:

| Metric | Alert |
|--------|-------|
| `tago_calls_today` | > 8,000 (80%) |
| `tago_cache_hit_rate` | < 70% |
| `tago_calls_per_mcp_call` | > 0.5 rolling 1h |
| `mcp_calls_today` | growth only |

Expose internally: `GET /health` → `{ tago_remaining_estimate, cache_hit_rate }`.

---

## Capacity examples (optimized stack)

Assume **1 TAGO call per unique route/date** (15m cache), **6 MCP calls per user question**:

| Daily TAGO budget | Unique route/date fetches | MCP tool calls served (6×, 50% cache hit on repeats) |
|-------------------|---------------------------|--------------------------------------------------------|
| 10,000 | 10,000 | ~60,000–120,000 |
| 50,000 (ops) | 50,000 | ~300,000+ |

Pre-warm 40 + station sync 1 ≈ **41 TAGO/day** fixed overhead.

---

## What we will NOT do

- Ask end users for data.go.kr keys (except BYOK self-host docs)
- Call TAGO per `search_stations` query
- Run `compare_ktx_srt` as two uncached TAGO round-trips
- Scale by adding more dev keys (ToS / abuse risk)

---

## Checklist (P0 before public hosted launch)

- [ ] `TagoGateway` with Redis cache
- [ ] `search_stations` — static only at runtime
- [ ] `compare_ktx_srt` — single fetch
- [ ] Request-scoped dedup in `plan_trip`
- [ ] `tago_calls_today` counter + 80% alert
- [ ] Stale-while-revalidate when > 80% budget
- [ ] Hosted MCP — **no** `DATA_GO_KR_SERVICE_KEY` in client config
- [ ] Production key + use case submitted

See [ROADMAP.md](./ROADMAP.md) for phased delivery.
