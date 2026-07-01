# 데이터·면책

**법률 자문 아님.** 상용·호스팅 전 [data.go.kr](https://www.data.go.kr) 활용사례 등록 및 필요 시 TAGO(054-459-7870) 확인.

## 데이터

| | |
|---|---|
| **사용** | [TAGO 열차정보 15098552](https://www.data.go.kr/data/15098552/openapi.do) — 이용허락 **제한 없음**(제0유형). [TAGO 정책](https://www.tago.go.kr/v5/notice/publicData.jsp) |
| **사용 (구조)** | [Korail KTX 노선별 역정보 15127571](https://www.data.go.kr/data/15127571/fileData.do) — 정차역·sync 구간 (파일) |
| **저장** | 동기화·DB 보관은 가공 서비스용. raw JSON 재판매 금지 |
| **미사용** | [15125762](https://www.data.go.kr/data/15125762/openapi.do) 코레일 열차운행정보 API (서비스 불안정·샘플 조회 불가), 레일포털(KRIC), 코레일/SRT 스크래핑, 예매·잔여석 비공식 API |

## 데이터 출처 원칙 (필수)

**역명·역코드·시간표는 공식 API 응답값만 사용한다.**

다음 출처는 **절대 사용하지 않는다**: 위키피디아, 나무위키, 블로그, 여행 가이드, 수동 작성 별칭(en/ja/zh), 추정 로마자 표기.

| 데이터 | 허용 출처 |
|--------|-----------|
| 역 `nodeid`, `nodename` | TAGO TrainInfo API ([15098552](https://www.data.go.kr/data/15098552/openapi.do)) |
| 시간표 | TAGO `GetStrtpntAlocFndTrainInfo` (sync worker) |
| v1 역 목록 범위 | `priority_station_codes.json` (nodeid); Korail [15127571](https://www.data.go.kr/data/15127571/fileData.do) + TAGO `nodeid` 매칭 |
| sync 노선 | `ktx_line_stations.json` — 15127571 인접 역쌍 + 수서→부산 |

Cursor 규칙: `.cursor/rules/tago-api-only-data.mdc`

## 출처·면책 (README / MCP `attribution`·`disclaimer`)

```
출처: 국토교통부 국가대중교통정보센터(TAGO) 공공데이터
시각표 참고용. 운행 시각 변경 가능. 예매·잔여석 미제공. 코레일·SR 공식 제휴 아님.
```

영문: `This service uses TAGO public data (MOLIT). Timetables only; no booking. Not affiliated with Korail or SR.`

## 증빙

`docs/legal/*.png` — 이용허락·TAGO 정책 스크린샷(캡처일 기록). API 키 커밋 금지.
