# MCP Tools Reference

**Status:** Phase 1 scaffold — `get_today_kst`, `search_stations`, `search_trains`, `compare_ktx_srt` implemented (in-memory store; Postgres later).

All tool **names and descriptions are English** (LLM routing).  
Responses support `locale`: `en` | `ko` | `ja` | `zh`.

## Recommended call chain

For one user question, prefer this sequence (6–7 tool calls):

```
get_today_kst
  → search_stations (departure)
  → search_stations (arrival)
  → holiday_check          (if holiday / peak season)
  → compare_ktx_srt        (or search_trains)
  → plan_trip
  → get_booking_links
```

---

## `get_today_kst`

Return today's date in Korea Standard Time. **Call before any date-sensitive query.**

| | |
|---|---|
| **Input** | None |
| **Output** | `date` (YYYYMMDD), `timezone`, `day_of_week`, `summary` |

**Implemented:** Yes

---

## `search_stations`

Resolve station name to TAGO station code. Accepts multilingual aliases.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | Yes | e.g. `Seoul`, `서울`, `ソウル`, `首尔` |
| `locale` | string | No | `en` \| `ko` \| `ja` \| `zh` (default `en`) |

**Output:** `matches[]` with `station_name`, `station_code`, `note`

**Implemented:** Yes (static `stations_i18n.json`)

---

## `search_trains`

Timetable for a route on a given date.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `departure` | string | Yes | Station name or code |
| `arrival` | string | Yes | Station name or code |
| `date` | string | Yes | YYYYMMDD |
| `time` | string | No | HHMM departure filter |
| `train_type` | string | No | `KTX` \| `SRT` \| `ALL` (default `ALL`) |
| `locale` | string | No | Response `summary` language |

**Output:** `trains[]` with `departure_time`, `arrival_time`, `train_type`, `train_no`

**Does not provide:** seat availability, fares, booking

**Implemented:** Yes (in-memory timetable store; sync via `POST /internal/sync`)

---

## `compare_ktx_srt`

Same route split into KTX vs SRT options.

| Parameter | Same as `search_trains` |
|-----------|-------------------------|

**Output:** `ktx_options[]`, `srt_options[]`, `recommendation_summary`

**Implemented:** Yes (Phase 1 scaffold)

---

## `holiday_check`

Check if a date is a Korean public holiday or weekend.

| Parameter | Type | Required |
|-----------|------|----------|
| `date` | string (YYYYMMDD) | Yes |

**Output:** `is_holiday`, `is_weekend`, `holiday_name`

**Implemented:** Planned (Phase 2)

---

## `get_booking_links`

Official booking links only — no scraping, no proxy booking.

| Parameter | Type | Required |
|-----------|------|----------|
| `departure` | string | No |
| `arrival` | string | No |
| `date` | string | No |

**Output:** `korail_talk`, `korail_web`, `srt`, `note`

**Implemented:** Planned (Phase 2)

---

## `plan_trip`

Multilingual trip summary in one call (may invoke other tools internally).

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `departure` | string | Yes | Origin station |
| `arrival` | string | Yes | Destination station |
| `date` | string | Yes | YYYYMMDD |
| `preference` | string | No | `earliest` \| `latest` \| `fewest_transfers` |
| `locale` | string | No | `en` \| `ko` \| `ja` \| `zh` |

**Output:** `summary`, structured `trains`, booking hints

**Implemented:** Planned (Phase 2)

---

## Common response fields

Every tool response includes:

| Field | Description |
|-------|-------------|
| `data_source` | `"tago"` |
| `attribution` | TAGO source string |
| `as_of` | ISO8601 KST timestamp |
| `disclaimer` | Short legal disclaimer |
| `summary` | One-sentence LLM-friendly summary |

## Error codes

| Code | Meaning |
|------|---------|
| `STATION_NOT_FOUND` | Run `search_stations` first |
| `NO_TRAINS` | No trains on that date/route |
| `TAGO_API_ERROR` | Upstream failure — retry |
| `RATE_LIMIT` | Daily quota exceeded |
| `INVALID_DATE` | Bad or past date — use `get_today_kst` |

## v1.1 (planned)

| Tool | Description |
|------|-------------|
| `search_trains_morning` | Departures 05:00–12:00 |
| `search_trains_afternoon` | Departures 12:00–18:00 |
| `search_trains_evening` | Departures 18:00–24:00 |
