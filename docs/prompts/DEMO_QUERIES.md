# Demo Queries

Use these in README, GIFs, Smithery listing, and ChatGPT Connector samples.

## English

1. *What's the earliest KTX from Seoul to Busan tomorrow?*
2. *Compare KTX vs SRT from Suseo to Busan on July 3rd.*
3. *Is December 25 a holiday in Korea? I want to take the train from Seoul to Busan.*
4. *Show me afternoon trains from Daejeon to Dongdaegu next Friday.*

## Korean

1. *내일 서울에서 부산 가는 KTX 첫차·막차 알려줘*
2. *7월 3일 수서→부산 KTX랑 SRT 비교해줘*
3. *추석 전날 서울 부산 기차 많을까? 공휴일인지도 확인해줘*
4. *이번 주 토요일 대전에서 동대구 가는 오후 열차*

## Japanese

1. *明日ソウルから釜山の一番早いKTXは？*
2. *7月3日、水西から釜山までKTXとSRTを比較して*
3. *来週の金曜日、大田から東大邱の午後の電車*

## Chinese

1. *明天从首尔到釜山最早的高铁是几点？*
2. *7月3号水西到釜山，对比一下KTX和SRT*
3. *下周五下午大田到东大邱有哪些车次？*

## Expected tool chain (agent)

Each query above should trigger roughly:

```
get_today_kst → search_stations ×2 → holiday_check? → search_trains|compare_ktx_srt → plan_trip → get_booking_links
```

## Gumroad skill pack

Bundle all 13 prompts above + `mcp.json` + `.env.example` as the $2 skill product.
