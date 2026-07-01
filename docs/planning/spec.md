# ktx-mcp — 제품 SPEC (KTX/SRT)

**버전:** 2.0  
**범위:** **KTX·SRT 시각표 조회만** — ITX·무궁화·시내교통·예매 API 제외  
**상세 구현:** [tools.md](../product/tools.md) · [deploy.md](../getting-started/deploy.md) · [roadmap.md](./roadmap.md)

---

## 1. 포지션

> **Ask in any language — get KTX/SRT schedules in one agent turn.**

| 항목 | 내용 |
|------|------|
| **제공** | KTX·SRT 출발/도착 시각표, 구간별 KTX vs SRT 비교 |
| **미제공** | ITX·일반열차, 잔여석, 예매, 지하철·버스, 실시간 지연 |
| **데이터** | [TAGO 15098552](https://www.data.go.kr/data/15098552/openapi.do) + Korail [15127571](https://www.data.go.kr/data/15127571/fileData.do) (KTX 정차역·sync 구간) |
| **호스팅** | Fly.io + Supabase — 사용자 **API 키 불필요** |

법·출처: [compliance.md](../legal/compliance.md)

---

## 2. MCP 도구 (v1 구현)

| 도구 | 설명 |
|------|------|
| `get_today_kst` | KST 오늘 날짜 (시간표 질의 전 필수) |
| `search_stations` | TAGO `nodename`(한글) 또는 `NAT...` → 역 코드 |
| `search_trains` | 구간·일자 KTX/SRT 시각표 (DB 캐시) |
| `compare_ktx_srt` | 동일 구간 KTX vs SRT |

### 권장 호출 순서

```
get_today_kst → search_stations(출발) → search_stations(도착) → compare_ktx_srt | search_trains
```

### `search_trains` 파라미터

| 파라미터 | 필수 | 설명 |
|----------|------|------|
| `departure` | ✅ | 역명(한글) 또는 코드 |
| `arrival` | ✅ | 역명(한글) 또는 코드 |
| `date` | ✅ | YYYYMMDD |
| `time` | ❌ | HHMM 이후 출발만 |
| `train_type` | ❌ | `KTX` \| `SRT` \| `ALL` (기본 `ALL` = KTX+SRT만) |
| `locale` | ❌ | `en` \| `ko` \| `ja` \| `zh` — `summary` 언어 |

### `search_stations` 파라미터

| 파라미터 | 필수 | 설명 |
|----------|------|------|
| `query` | ✅ | TAGO 한글 역명 또는 `NAT...` |
| `locale` | ❌ | 응답 `summary` 언어 |

**역 검색:** 수동 en/ja/zh 별칭 없음. LLM이 사용자 입력을 TAGO 역명으로 해석하거나 `NAT` 코드 사용.

---

## 3. 데이터

### 3.1 시간표 (TAGO)

- API: `GetStrtpntAlocFndTrainInfo`
- sync: 73개 KTX 인접 구간 × 오늘·내일(KST)
- 저장 시 **KTX·SRT 편만** upsert (ITX 등 제외)

### 3.2 역·노선 (Korail 파일)

- `ktx_line_stations.json` — 15127571 KTX 노선 정차역
- `priority_station_codes.json` — 70역 (+ 수서 SRT)
- `stations_i18n.json` — TAGO `build_stations.py` 생성

### 3.3 미사용

- [15125762](https://www.data.go.kr/data/15125762/openapi.do) 코레일 운행정보 API (불안정)
- 레일포털(KRIC), korail2/SRT 스크래핑

---

## 4. Non-goals

- ITX·무궁화·새마을·청춘 등 **KTX/SRT 외 열차**
- 승차권 예약·결제·잔여석
- 서울 지하철·시내버스 (`korea-transit-mcp` 영역)
- 공휴일 API·공항·숙박 번들 (본 제품 스코프 외)

---

## 5. 아키텍처 (요약)

```text
MCP /mcp → Postgres SELECT (0 TAGO on request)
pg_cron / POST /internal/sync → TAGO → UPSERT (KTX/SRT rows only)
```

상세: [architecture.md](../engineering/architecture.md) · [traffic.md](../engineering/traffic.md)

---

## 6. 환경 변수

| 변수 | Fly | 로컬 |
|------|-----|------|
| `DATABASE_URL` | ✅ | 권장 |
| `DATA_GO_KR_SERVICE_KEY` | ✅ (sync만) | BYOK |
| `SYNC_SECRET` | ✅ | sync HTTP 시 |
| `KTX_MCP_TRANSPORT` | `http` | `stdio` \| `http` |

템플릿: [env.template](../getting-started/env.template)

---

## 7. 출시 체크리스트

- [ ] Supabase migration
- [ ] `fly deploy` + secrets
- [ ] `POST /internal/sync` → `row_count` > 0
- [ ] 서울→부산 KTX/SRT 1턴 (hosted, 키 없음)
- [ ] [compliance.md](../legal/compliance.md) 면책·출처 표기

---

## 8. 관련 문서

| 문서 | 용도 |
|------|------|
| [demand-research.md](./demand-research.md) | 니치 조사 아카이브 (스코프는 본 SPEC 기준) |
| [pricing.md](../product/pricing.md) | 호스팅 요금 |
| [demo-queries.md](../product/demo-queries.md) | 데모 질문 |
