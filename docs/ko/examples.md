---
title: 예제
description: 로그인부터 업로드, 콘텐츠 등록, 피드, 소셜, Game Cloud까지 문서화된 API만으로 구성한 curl 예제 모음입니다.
section: API
---

# 예제

인증, 캡차, 업로드, 콘텐츠, 피드, 소셜, Game Cloud를 잇는 실전 흐름을 curl로 보여 줍니다. 모든 예제는 이 문서에 설명된 엔드포인트만 사용합니다.

## 빠른 예제

```bash
export API="https://zuzunza.com/api/v1"
curl -sS "$API/feeds/hype?page=1&per_page=20"
```

## 준비

```bash
export API="https://zuzunza.com/api/v1"
```

- 응답은 `{ success, data, meta }` 또는 `{ success, error, meta }` 형식입니다. `success`가 `false`이면 `error.code`로 분기하세요.
- 문의 추적을 위해 `-H "X-Request-Id: $(uuidgen)"`를, 한국어 메시지를 받으려면 `-H "Accept-Language: ko-KR"`를 추가할 수 있습니다.

## 1. 로그인하고 내 정보 확인

```bash
# 로그인 (캡차가 비활성인 서버)
curl -sS -X POST "$API/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"identifier":"demo_user","password":"SecureP@ss123"}'
# → data.tokens.access_token 을 ACCESS 에, refresh_token 을 REFRESH 에 저장

# 내 정보
curl -sS "$API/auth/me" -H "Authorization: Bearer $ACCESS"

# access 토큰 갱신
curl -sS -X POST "$API/auth/refresh" \
  -H "Content-Type: application/json" \
  -d "{\"refresh_token\":\"$REFRESH\"}"
```

필드 상세: [인증](authentication.md)

## 2. 캡차를 포함한 가입

캡차가 활성화된 서버에서는 `zcaptcha_token`이 필요합니다.

```bash
# 1) 챌린지 받기
curl -sS -X POST "$API/captcha/challenge"

# 2) 클라이언트에서 PoW를 풀어 base64 토큰을 만든 뒤(TOKEN), 가입
curl -sS -X POST "$API/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "new@example.com",
    "password": "SecureP@ss123",
    "password_confirm": "SecureP@ss123",
    "handle": "newcreator",
    "zcaptcha_token": "'"$TOKEN"'"
  }'
```

풀이 방법: [캡차](captcha.md)

## 3. 공개 피드 보기

```bash
# HYPE 미디어 피드
curl -sS "$API/feeds/hype?page=1&per_page=20"

# 카테고리 쿼리 (sort/order 쿼리는 지원하지 않음)
curl -sS "$API/feeds?category=swipe&page=1&per_page=12"

# 커뮤니티 타임라인 — 다음 페이지는 next_cursor 를 before 로
curl -sS "$API/feed?limit=20"
curl -sS "$API/feed?limit=20&before=$NEXT_CURSOR"

# 새로 공개된 JUMP 게임
curl -sS "$API/jump/games?sort=new&page=1&per_page=20"
```

상세: [피드](feeds.md)

## 4. 업로드하고 콘텐츠 등록

```bash
# 1) 파일 업로드 → data.upload.url
curl -sS -X POST "$API/uploads" \
  -H "Authorization: Bearer $ACCESS" \
  -F "file=@./clip.mp4"

# 2) 받은 URL(URL)로 가로형 미디어 등록
curl -sS -X POST "$API/contents" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{"category":"hype","type":"horizontal_media","title":"첫 작품","media_url":"'"$URL"'"}'
```

서버 간 호출에서는 `Authorization` 대신 `-H "X-API-Key: $ZUKU_API_KEY"`로 콘텐츠를 생성할 수 있습니다.

### JUMP 게임 초안 → 게시

```bash
# 1) HTML5 ZIP 업로드 → data.upload.url
curl -sS -X POST "$API/uploads" \
  -H "Authorization: Bearer $ACCESS" \
  -F "file=@./game.zip"

# 2) 초안 등록 (jump.status 는 draft)
curl -sS -X POST "$API/contents" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{
    "category": "jump",
    "type": "game",
    "title": "점프 러너",
    "jump": {
      "game_type": "html5",
      "package": { "format": "zip", "entry_point": "index.html", "url": "'"$URL"'" },
      "status": "draft"
    }
  }'

# 3) 게시
curl -sS -X POST "$API/contents/$CONTENT_ID/publish" \
  -H "Authorization: Bearer $ACCESS"
```

`jump` 메타의 전체 필드는 [콘텐츠](contents.md)를, 업로드 한도는 [미디어](media.md)를 참고하세요.

## 5. 좋아요, 북마크, 팔로우

```bash
curl -sS -X POST "$API/contents/$CONTENT_ID/like" -H "Authorization: Bearer $ACCESS"
curl -sS -X POST "$API/contents/$CONTENT_ID/bookmark" -H "Authorization: Bearer $ACCESS"
curl -sS -X POST "$API/creators/$HANDLE/follow" -H "Authorization: Bearer $ACCESS"
```

## 6. 댓글, 알림, DM

```bash
# 댓글
curl -sS -X POST "$API/contents/$CONTENT_ID/comments" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{"body":"좋은 작품이에요!"}'

# 알림 목록과 미읽음 수
curl -sS "$API/notifications" -H "Authorization: Bearer $ACCESS"
curl -sS "$API/notifications/unread-count" -H "Authorization: Bearer $ACCESS"

# DM 대화 시작 → data.conversation.id 를 CONV 에
curl -sS -X POST "$API/dm/conversations" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{"handle":"friend_handle"}'

curl -sS -X POST "$API/dm/conversations/$CONV/messages" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{"body":"안녕"}'
```

상세: [소셜](social.md)

## 7. Game Cloud

먼저 프로젝트를 만들고 `projectId`(PROJECT)를 얻습니다.

```bash
curl -sS -X POST "$API/cloud/projects" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{"name":"내 RPG","description":"온라인 멀티 RPG"}'

# 지갑
curl -sS "$API/cloud/economy/balance?projectId=$PROJECT" \
  -H "Authorization: Bearer $ACCESS"

# 최고 점수 갱신
curl -sS -X POST "$API/cloud/vars/mutate" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{"projectId":"'"$PROJECT"'","scope":"user","key":"high_score","op":"max","num":9999}'

# 세이브
curl -sS -X POST "$API/cloud/saves/save" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{"projectId":"'"$PROJECT"'","slot":"default","data":{"level":3,"inventory":["sword"]}}'
```

게임 샌드박스에 계정 토큰을 넘기지 말고, 세션을 관리하는 신뢰할 수 있는 앱에서 호출하세요. 상세: [Game Cloud](game-cloud.md)

## 8. 오류 처리

| `error.code` | 권장 처리 |
|---|---|
| `CAPTCHA_FAILED` | 새 챌린지를 받아 다시 시도 |
| `UNAUTHORIZED` | `POST /auth/refresh`로 갱신하거나 다시 로그인 |
| `INVALID_REFRESH_TOKEN` | 다시 로그인 |
| `VALIDATION_ERROR` | `error.details`의 필드별 메시지 확인 |
| `RATE_LIMITED` | `X-RateLimit-Reset` 이후 재시도([요청 한도](rate-limits.md)) |

전체 코드: [오류](errors.md)

## 관련 문서

- [시작하기](getting-started.md)
- [인증](authentication.md) · [캡차](captcha.md)
- [콘텐츠](contents.md) · [미디어](media.md) · [피드](feeds.md) · [소셜](social.md)
- [Game Cloud](game-cloud.md) · [개발자 콘솔](devconsole.md)
