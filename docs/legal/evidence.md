# Legal archive

Store compliance evidence here. **Do not commit API keys.**

## Required files

| File | Description |
|------|-------------|
| `tago-license-type0.png` | data.go.kr — 이용허락범위 **제한 없음** for API 15098552 |
| `tago-policy-commercial.png` | [TAGO policy page](https://www.tago.go.kr/v5/notice/publicData.jsp) — commercial use |

## How to capture

1. Open [TAGO 열차정보 API](https://www.data.go.kr/data/15098552/openapi.do) while logged in.
2. Screenshot the **이용허락범위** section.
3. Save as `tago-license-type0.png` in this folder.
4. Note capture date in commit message.

## Git ignore

Binary screenshots may be gitignored via `docs/legal/*.png` in `.gitignore`.  
Keep copies locally even if not pushed.

See [compliance.md](./compliance.md) for attribution text.
