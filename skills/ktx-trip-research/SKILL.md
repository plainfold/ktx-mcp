---
name: ktx-trip-research
description: Research Korea KTX/SRT train schedules via TAGO public data. Use when the user asks about KTX, SRT, bullet train, 고속철도, 新幹線, or 高铁 timetables between Korean cities. Supports English, Korean, Japanese, and Chinese queries.
---

# ktx-trip-research

Korea long-distance rail timetable research using the `ktx-mcp` MCP server.

## When to use

- KTX / SRT / ITX schedule questions
- Compare KTX vs SRT on the same route
- Holiday or peak-season travel planning
- Foreign-language queries about Korean trains

## When NOT to use

- Ticket booking or seat availability
- Seoul subway / bus (use a transit MCP instead)
- Real-time delay guarantees

## Required MCP server

Connect `ktx-mcp` with `DATA_GO_KR_SERVICE_KEY` set. See [docs/SETUP.md](../../docs/SETUP.md).

## SOP — always follow this order

1. **`get_today_kst`** — resolve today's date in KST first
2. **`search_stations`** — departure station
3. **`search_stations`** — arrival station
4. **`holiday_check`** — if user mentions holidays, Chuseok, Lunar New Year, or "busy day"
5. **`compare_ktx_srt`** — if user compares KTX and SRT; else **`search_trains`**
6. **`plan_trip`** — set `locale` to match user language (`en`/`ko`/`ja`/`zh`)
7. **`get_booking_links`** — end every trip answer with official booking links

Do not skip steps to save calls unless the user already provided exact station codes and date.

## Locale detection

| User language | `locale` |
|---------------|----------|
| English | `en` |
| Korean | `ko` |
| Japanese | `ja` |
| Chinese | `zh` |
| Other | `en` (default) |

## Trigger examples

### Korean
- 서울에서 부산 KTX 시간표
- 내일 수서→부산 SRT랑 KTX 비교해줘
- 추석 전날 서울 부산 기차

### English
- KTX schedule Seoul to Busan tomorrow
- compare KTX vs SRT Suseo to Busan

### Japanese
- 明日ソウルから釜山のKTX
- 水西から釜山 SRT

### Chinese
- 明天首尔到釜山高铁
- 水西到釜山 KTX和SRT对比

## Response format

1. One-line answer in the user's language
2. Table or list: departure → arrival times, train type
3. Note if holiday/weekend affects demand
4. Official booking links (Korail / SRT) — state that this skill does not book tickets

## Disclaimer (include briefly)

Timetable reference only. Schedules may change. Book via official Korail / SRT apps.

## More prompts

See [docs/prompts/DEMO_QUERIES.md](../../docs/prompts/DEMO_QUERIES.md).
