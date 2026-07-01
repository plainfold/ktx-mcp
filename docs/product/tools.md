# MCP Tools Reference

**Scope:** KTX and SRT timetables only.

**Implemented:** `get_today_kst`, `search_stations`, `search_trains`, `compare_ktx_srt`

Tool names and descriptions are **English**. Response `summary` supports `locale`: `en` | `ko` | `ja` | `zh`.

## Call chain

```
get_today_kst → search_stations (dep) → search_stations (arr) → compare_ktx_srt | search_trains
```

---

## `get_today_kst`

KST today before any date query.

**Implemented:** Yes

---

## `search_stations`

Match TAGO Korean `nodename` or `NAT...` nodeid.

| Parameter | Required | Description |
|-----------|----------|-------------|
| `query` | Yes | e.g. `서울`, `부산`, `NAT010000` |
| `locale` | No | `summary` language |

**Catalog:** 70 KTX/SRT stations (`stations_i18n.json`)

**Implemented:** Yes

---

## `search_trains`

KTX/SRT timetable for a route and date. Reads Postgres cache — no TAGO on request.

| Parameter | Required | Description |
|-----------|----------|-------------|
| `departure` | Yes | Station name (Korean) or code |
| `arrival` | Yes | Station name (Korean) or code |
| `date` | Yes | YYYYMMDD |
| `time` | No | HHMM — departures after this time |
| `train_type` | No | `KTX` \| `SRT` \| `ALL` (default: both KTX and SRT) |
| `locale` | No | `summary` language |

**Not provided:** seats, fares, booking, ITX or other train types

**Implemented:** Yes

---

## `compare_ktx_srt`

KTX vs SRT on the same route and date.

**Implemented:** Yes

---

## HTTP (hosted)

| Method | Path | Auth |
|--------|------|------|
| `GET` | `/health` | None |
| `POST` | `/internal/sync` | `X-Sync-Secret` |

Sync: 73 KTX adjacent segments × today/tomorrow (KST), **KTX/SRT rows only**.
