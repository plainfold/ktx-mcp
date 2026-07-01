---
name: ktx-trip-research
description: Research Korea KTX and SRT train schedules via TAGO public data. Use when the user asks about KTX, SRT, bullet train, 고속철도, 新幹線, or 高铁 timetables between Korean cities.
---

# ktx-trip-research

KTX/SRT timetable research using the `ktx-mcp` MCP server.

## When to use

- KTX or SRT schedule questions
- Compare KTX vs SRT on the same route

## When NOT to use

- ITX, Mugunghwa, or other train types
- Ticket booking or seat availability
- Seoul subway / bus

## MCP server

Hosted `ktx-mcp` URL (no user API key). See [setup](../../docs/getting-started/setup.md) for BYOK.

## SOP

1. **`get_today_kst`**
2. **`search_stations`** — departure (Korean TAGO name or `NAT...`)
3. **`search_stations`** — arrival
4. **`compare_ktx_srt`** if comparing operators; else **`search_trains`**

Use `locale`: `en` | `ko` | `ja` | `zh` for response summaries.

## Trigger examples

- 서울에서 부산 KTX 시간표
- 내일 수서→부산 SRT랑 KTX 비교해줘
- KTX schedule Seoul to Busan tomorrow
- compare KTX vs SRT Suseo to Busan

## Disclaimer

Timetable reference only. Book via official Korail / SRT apps.

More prompts: [demo-queries](../../docs/product/demo-queries.md).
