# Legal & Data Compliance

**Not legal advice.** Confirm with TAGO / data.go.kr before high-volume commercial use.

## Data source

| Item | Value |
|------|--------|
| **API** | [TAGO 열차정보](https://www.data.go.kr/data/15098552/openapi.do) |
| **Provider** | Ministry of Land, Infrastructure and Transport / TAGO |
| **Portal ID** | 15098552 |
| **License** | **이용허락범위 제한 없음** (public data type 0) |
| **Policy** | [TAGO public data policy](https://www.tago.go.kr/v5/notice/publicData.jsp) — commercial use permitted |

## Required attribution (recommended)

Display in README, tool responses, and hosted UI:

**English**

> This service uses public data from the Ministry of Land, Infrastructure and Transport / National Public Transport Information Center (TAGO).

**Korean**

> 본 서비스는 국토교통부 국가대중교통정보센터(TAGO) 공공데이터를 활용하였습니다.  
> 출처: 국토교통부 / 국가대중교통정보센터

## What we do NOT use

| Source | Reason |
|--------|--------|
| **KRIC 레일포털** (`openapi.kric.go.kr`) | Commercial use and Open API re-provision restricted |
| **Korail / SRT scraping** | ToS risk, no official seat API |
| **KRX / market data** | Out of scope |

## Product disclaimers

Include in every MCP response (`disclaimer` field) and README:

### English

> Timetable information only. Schedules may change. This MCP does not book tickets or guarantee seat availability. Use official Korail / SRT apps for booking. Not affiliated with Korail or SR.

### Korean

> 시각표 참고용입니다. 운행 시각은 변경될 수 있습니다. 승차권 예매·잔여석 조회를 제공하지 않습니다. 예매는 코레일톡·SRT 공식 앱을 이용하세요. 코레일·SR 공식 제휴가 아닙니다.

### Japanese

> 時刻表の参考情報です。運行時刻は変更される場合があります。予約・空席確認は行いません。予約はコレイル公式アプリまたはSRT公式サイトをご利用ください。

### Chinese

> 仅供参考的时刻表信息。运行时间可能变更。不提供订票或余票查询。请使用 Korail / SRT 官方应用购票。

## Archive checklist

Store under `docs/legal/`:

- [ ] Screenshot: data.go.kr 이용허락범위 **제한 없음**
- [ ] Screenshot: TAGO 이용정책 (commercial use)
- [ ] Date captured and API portal ID noted

## Hosting registration (data.go.kr)

When applying for a **production** key, register a use case such as:

> AI agent (Cursor, ChatGPT) MCP for Korea KTX/SRT train timetables.  
> Uses TAGO train API. No ticket booking.

## Non-goals (legal safety)

- No ticket booking or payment on behalf of users
- No claim of official Korail / SR partnership
- No resale of raw TAGO JSON as a standalone data product
