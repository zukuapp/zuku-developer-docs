---
title: 변경 이력
description: ZukuJS CLI 릴리스와 ZUKU API v1의 변경 이력, 버전 표기, 브레이킹 체인지·폐기 정책을 정리합니다.
section: Reference
---

# 변경 이력

## ZukuJS CLI

### 0.3.0 — 첫 공개 릴리스

2026-10-04 공개 설치 검증 기준입니다.

- **공개 설치**: 공식 설치 스크립트로 설치합니다. 설치 도구가 관리형 Node.js 22를 함께 준비합니다. npm 레지스트리 배포는 하지 않습니다.

  ```sh
  # macOS / Linux (curl)
  curl -fsSL --proto '=https' --tlsv1.2 https://zuzunza.com/install.sh -o install-zuku-cli.sh && bash install-zuku-cli.sh

  # macOS / Linux (wget)
  wget --https-only -O install-zuku-cli.sh https://zuzunza.com/install.sh && bash install-zuku-cli.sh
  ```

  ```powershell
  # Windows PowerShell
  & ([scriptblock]::Create((irm 'https://zuzunza.com/install.ps1')))
  ```

  고정 버전 아카이브는 `https://zuzunza.com/downloads/zukujs/cli/0.3.0/zukujs-cli-0.3.0.tgz`입니다. 자세한 내용은 [설치](installation.md)를 보세요.
- **`zuku`와 `zukujs`**: 두 이름은 같은 명령이며 같은 런타임·설정·로그인 정보(`~/.config/zukujs/`(Windows: `%LOCALAPPDATA%\ZukuJS\`))를 공유합니다.
- **`zuku create <name>`**: 스페이스 키나 탭으로 장애물을 뛰어넘는 Canvas JUMP 러너 게임 프로젝트를 만듭니다. 옵션은 이름 하나뿐입니다.
- **로컬 작업 흐름**: 프로젝트 디렉터리 안에서 `zuku run`, `zuku validate .`, `zuku package . --format zwf`로 실행·검사·결정적 ZWF 패키징을 합니다.
- **초안 업로드**: `zuku upload`는 패키지를 올리고 비공개 초안만 만듭니다.
- **게임 개발 에이전트**: `zuku agent`가 로컬에서 게임을 만들고 실제 브라우저로 검증합니다. `--draft`는 초안만 업로드하고, `--yolo`는 명시적인 1회 프로덕션 게시이며 서버가 계정당 최근 6시간 동안 성공한 게시를 3회로 제한합니다. [게임 개발 에이전트](cli/agent.md), [패키징과 게시](cli/publishing.md)를 참고하세요.
- **Phaser**: CLI에는 Phaser가 포함되지 않습니다. Phaser로 시작하려면 Phaser를 포함한 스타터 아카이브를 내려받으세요.

## ZUKU API

### 버전 표기

| 위치 | 값 |
|---|---|
| URL 접두사 | `/api/v1/…` |
| 응답 헤더 | `X-API-Version: v1` |
| 봉투 `meta.version` | `"v1"` |

세 위치는 같은 API 세대를 가리킵니다. 클라이언트는 **URL의 `v1`을 기준**으로 삼고, 헤더와 `meta`는 관측·로깅에 사용하세요.

- **v1**: 활성(스테이징·프로덕션 계약)
- **v2**: 계획만 있음. 경로·봉투에 브레이킹 변경이 필요할 때 도입하며, 현재 `/api/v2`는 없습니다.

### 2026-10-01 · 요금제별 요청 한도

- 비회원·Free·Super ZUKU·Creator·Cloud 요금제를 서버에서 검증하고, 요청 종류별 실제 카운터와 429 응답을 구현했습니다.
- 계정·API 키·공유 IP 보호, 10초 구간, 실제 잔여 횟수·Reset·Retry-After 안내를 추가했습니다.
- ZUKU 탐색과 웹 API 입장 확인, 편집 내용을 유지하는 안내, 전용 `/rate-limit` 화면을 추가했습니다.
- 운영 적용에는 웹·백엔드·마이그레이션·캐시 정책을 함께 배포해야 합니다. 이 기록은 운영 활성화를 뜻하지 않습니다. [요청 한도](rate-limits.md)를 참고하세요.

### 2026-09-12 · 문서 이전과 JUMP 게시

- 공개 API 문서를 `docs.zuzunza.com`으로 이전했습니다. 기존 `/docs/api` 링크는 유지합니다.
- JUMP 초안과 게시 요청을 분리하고, 공개 전 미리보기 권한 검사와 중복 게시 방지를 추가했습니다.
- 최초 공개 시각 기준 신규 게임 우선 정렬과 `recent` 최신순 별칭을 추가했습니다.
- HTML5 ZWF2 패키지 재생, 이미지 AVIF·음원 업로드, 저장소 장애 응답을 반영했습니다.
- 커뮤니티 사진 첨부, 부분 수정, Unicode 해시태그 검색과 실제 지원 범위를 문서화했습니다.

### 2026-09-12 · JUMP 게임 썸네일

- 기존 게임의 이미지 검사와 새 게임의 실제 화면 자동 캡처를 추가했습니다.
- 작성자 전용 `GET` / `POST /api/v1/contents/{id}/thumbnail-job`으로 상태 확인과 재생성을 지원합니다.
- 직접 업로드한 이미지 보호, 원본 변경 시 재예약, 실패 재시도를 적용합니다. 썸네일 생성은 게임을 게시하지 않습니다.

### v1 기능 목록

날짜 없이 정리한 v1 구현 범위입니다. 세부 커밋은 저장소 이력을 따릅니다.

**Social · 팔로우**

- `follows` 테이블과 `POST /creators/{handle}/follow` 토글
- 공개 프로필의 `follower_count` / `following_count` / `is_following` 실측값
- 피드 `sort=following` — 팔로우한 작성자의 작품만

**문서**

- API 위키와 사이트 `/docs/api`(Captcha·Examples 상세 페이지 포함)

**Auth · 세션**

- `POST /api/v1/auth/register` · `signup` — 가입(캡차 게이트, 레거시 계정 충돌 차단)
- `POST /api/v1/auth/login` · `logout` · `refresh`
- `GET` / `PATCH /api/v1/auth/me`
- `GET /api/v1/auth/sessions` · `DELETE …/sessions/{id}` — 활성 세션 목록·폐기
- `POST /api/v1/auth/oauth/{provider}` — **501** `NOT_IMPLEMENTED`(범위 밖)

**Captcha**

- `POST /api/v1/captcha/challenge` · `verify` — 자체 호스팅 PoW
- 비밀 값 미설정 시 `CAPTCHA_NOT_CONFIGURED`로 실패 쪽으로 닫힘

**Feeds · Contents**

- `GET /api/v1/feeds` 및 `/feeds/hype|swipe|jump`
- `GET /api/v1/contents/{id}`
- `GET /api/v1/contents/{id}/conversion`
- `GET /api/v1/contents/{id}/recommendations` — `limit` 1–50(기본 8), `offset`, LIMIT+1 방식 `has_more`, 비로그인 짧은 캐시
- `GET /api/v1/jump/games/{id}?include=related,popular` — JUMP 상세 선반을 같은 봉투에 첨부
- `POST /api/v1/contents` — Bearer **또는** `X-API-Key`
- `PATCH` / `DELETE /api/v1/contents/{id}` — Bearer만, DELETE는 아카이브
- `POST …/like` · `POST …/bookmark`
- 댓글: `GET`/`POST …/comments`, `PATCH`/`DELETE /api/v1/comments/{id}`

**Uploads · JUMP stream**

- `POST /api/v1/uploads` — multipart, 매직 바이트 MIME 판정, 크기 한도
- `GET /uploads/{path}` — API 접두사 없는 정적 제공
- `GET /api/v1/jump/games` · `GET …/games/{id}`
- `POST …/play` · `…/stream`(IR) · `…/swf` — **POST는 인증 필수**

**Developer keys**

- `POST` / `GET /api/v1/developer/keys`
- `DELETE /api/v1/developer/keys/{id}`
- 발급한 키로 콘텐츠 생성(`X-API-Key`) 가능

**Community posts**

- `GET /api/v1/feed` — 타임라인
- `POST /api/v1/posts` · `GET …/posts/{id}` · `GET …/thread`
- `POST …/replies` · `POST`/`DELETE …/like` · `DELETE …/posts/{id}`

**DM**

- `GET`/`POST /api/v1/dm/conversations`
- `GET`/`POST …/conversations/{id}/messages`
- `POST …/conversations/{id}/read`
- 1:1 평문 저장(종단 간 암호화·그룹 채팅은 범위 밖)

**Notifications**

- `GET /api/v1/notifications`
- `GET …/unread-count`
- `POST …/read-all` · `POST …/{id}/read`

**기타**

- `GET /api/health`
- `GET /api/wasm/contract`
- 관리자 사용자 조회·수정, 레거시 JUMP 경로 308 리다이렉트
- moderation / analytics 모듈 위임 경로(각 모듈 게이트 적용)

## 브레이킹 체인지 정책

1. **URL 메이저 버전(`v1` → `v2`) 없이** 기존 클라이언트를 깨는 변경을 넣지 않습니다. 예: 필수 필드 추가·의미 변경, 성공 봉투 키 제거·이름 변경, 인증 방식 축소, 오류 코드 의미 뒤집기.
2. **허용되는 비브레이킹 변경**: 선택 필드 추가, 새 엔드포인트, 새 오류 코드 추가, 문서화되지 않았던 동작 명시, 한도 완화.
3. **브레이킹이 필요하면** `/api/v2`를 병행 배포하고, `X-API-Version`과 `meta.version`을 `v2`로 올리며, v1은 **폐기 예고 기간**을 둔 뒤 제거합니다.
4. 콘텐츠 DELETE의 **아카이브 의미**, JUMP play의 **경로 ID = 본문 ID**, 업로드의 **매직 바이트 우선**은 v1 계약의 일부입니다. 이를 바꾸려면 메이저 버전이 필요합니다.
5. 더미 rate-limit 헤더를 실제 한도로 전환하는 정책은 [요청 한도](rate-limits.md)에 공개합니다. 운영 적용 전에 정책·시점·재시도 계약을 안내하고 웹·백엔드·문서를 함께 배포합니다.

## 폐기 안내

| 항목 | 상태 | 안내 |
|---|---|---|
| `/api/v1/auth/signup` | v1에서 `register`와 같은 처리기 | 새 연동은 `register` 권장. signup 제거 시 폐기 공지 예정 |
| OAuth `…/auth/oauth/{provider}` | 501 `NOT_IMPLEMENTED` | 구현 예정 없음. 호출 결과를 성공으로 취급하지 말 것 |
| rate-limit 헤더 수치 | 실제 정책 구현, 운영 적용 전 안내 필요 | 실제 응답과 정책 조회로 확인([요청 한도](rate-limits.md)) |
| 레거시 JUMP URL(`/game/play/hg-…` 등) | 308 → 정규 `/api/v1/jump/…` | 새 클라이언트는 정규 경로만 사용 |
| 하드 삭제 기대 | 해당 없음 | `DELETE /contents/{id}`는 **아카이브**. 복구·완전 삭제 계약은 별도 |
| v2 | 미착수 | 일정·스키마 확정 전 문서만 예약 |

폐기 예정 API는 최소 **한 메이저 주기** 동안 병행하고, 응답이나 문서에 대체 경로를 명시합니다.

## 관련 문서

- [오류와 응답 형식](errors.md)
- [요청 한도](rate-limits.md)
- [명령 참조](cli/commands.md)
