---
title: 소셜
description: 좋아요, 북마크, 팔로우, 댓글, 알림, DM, 내 목록 API를 설명합니다.
section: API
---

# 소셜

콘텐츠 반응(좋아요·북마크), 크리에이터 팔로우, 댓글, 알림, 1:1 DM, 내 작품·좋아요·북마크·글 목록 API입니다.

**Base URL**: `https://zuzunza.com/api/v1`

## 빠른 예제

```bash
curl -sS -X POST "https://zuzunza.com/api/v1/contents/$CID/like" \
  -H "Authorization: Bearer $ACCESS"
```

## 인증

| 구분 | 인증 |
|---|---|
| 콘텐츠 좋아요·북마크, 팔로우 | Bearer 필수 |
| 댓글 목록 `GET` | 없음(공개). 콘텐츠가 없으면 404 |
| 댓글 작성·수정·삭제 | Bearer 필수 |
| 알림 목록 / 미읽음 수 | Bearer 선택(없으면 빈 목록 또는 0에 가깝게 동작) |
| 알림 모두 읽음 / 단건 읽음 | Bearer 필수 |
| DM 전체 | Bearer 필수, 대화 참여자만 |
| `GET /users/me/{kind}` | Bearer 필수 |

헤더 형식은 `Authorization: Bearer <access_token>`입니다. 이 페이지의 경로는 `X-API-Key`를 받지 않습니다(콘텐츠 *생성*과 다름). 응답은 공통 형식 `{ success, data, meta }` / `{ success, error, meta }`를 따르며, 댓글 삭제는 `204`입니다.

## 엔드포인트 요약

| Method | Path | 인증 | 설명 |
|---|---|---|---|
| `POST` | `/contents/{id}/like` | Bearer | 좋아요 토글 |
| `POST` | `/contents/{id}/bookmark` | Bearer | 북마크 토글 |
| `POST` | `/creators/{handle}/follow` | Bearer | 크리에이터 팔로우 토글 |
| `GET` | `/contents/{id}/comments` | 공개 | 댓글 목록 |
| `POST` | `/contents/{id}/comments` | Bearer | 댓글 작성 → `201` |
| `PATCH` | `/comments/{id}` | Bearer | 내 댓글 수정 |
| `DELETE` | `/comments/{id}` | Bearer | 소프트 삭제 → `204` |
| `GET` | `/notifications` | 선택 | 알림 목록 |
| `GET` | `/notifications/unread-count` | 선택 | 미읽음 개수 |
| `POST` | `/notifications/read-all` | Bearer | 모두 읽음 |
| `POST` | `/notifications/{id}/read` | Bearer | 단건 읽음 |
| `GET` | `/dm/conversations` | Bearer | 대화 목록 |
| `POST` | `/dm/conversations` | Bearer | 대화 시작 또는 재사용 → `201` |
| `GET` | `/dm/conversations/{id}/messages` | Bearer + 참여자 | 메시지 목록 |
| `POST` | `/dm/conversations/{id}/messages` | Bearer + 참여자 | 메시지 전송 → `201` |
| `POST` | `/dm/conversations/{id}/read` | Bearer + 참여자 | 대화 읽음 처리 |
| `GET` | `/users/me/{kind}` | Bearer | 내 작품·좋아요·북마크·글 |

## 좋아요와 북마크

### POST /contents/{id}/like

토글합니다. 응답 `data`: `{ "is_liked": true, "like_count": 42 }`

### POST /contents/{id}/bookmark

토글합니다. 응답 `data`: `{ "is_bookmarked": true, "bookmark_count": 7 }`

```bash
curl -sS -X POST "https://zuzunza.com/api/v1/contents/$CID/bookmark" \
  -H "Authorization: Bearer $ACCESS"
```

미인증은 `401`, 콘텐츠가 없으면 `404 CONTENT_NOT_FOUND`입니다.

## POST /creators/{handle}/follow

크리에이터 팔로우/언팔로우를 토글합니다. Bearer가 필요합니다.

응답 `200` · `data`: `{ "is_following": true, "follower_count": 1521 }`

| HTTP | code | 상황 |
|---|---|---|
| 401 | `UNAUTHORIZED` | 세션 없음 |
| 404 | `CREATOR_NOT_FOUND` | handle이 없거나 정지됨 |
| 409 | `CANNOT_FOLLOW_SELF` | 자기 자신 팔로우 |

공개 프로필 `GET /creators/{handle}`의 `is_following`, `follower_count`, `following_count`도 같은 팔로우 정보를 사용합니다. 홈 피드의 `sort=following`은 팔로우한 작성자의 작품만 반환합니다.

```bash
curl -sS -X POST "https://zuzunza.com/api/v1/creators/friend/follow" \
  -H "Authorization: Bearer $ACCESS"
```

## 댓글

### GET /contents/{id}/comments

| 쿼리 | 기본값 |
|---|---|
| `page` | 1 |
| `per_page` | 20 |

응답 `data`: `comments`, `pagination`.

```bash
curl -sS "https://zuzunza.com/api/v1/contents/$CID/comments?page=1&per_page=20"
```

### POST /contents/{id}/comments

| 필드 | 필수 | 규칙 |
|---|---|---|
| `body` | 예 | 최대 1000자 |
| `parent_id` | 아니요 | 대댓글일 때 부모 댓글 id |

성공 `201` · `data.comment`.

```bash
curl -sS -X POST "https://zuzunza.com/api/v1/contents/$CID/comments" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{"body":"좋은 작품이에요","parent_id":null}'
```

### PATCH /comments/{id}

본문 `{ "body": "수정한 댓글" }`. 작성자만 수정할 수 있으며, 다른 사람의 댓글이나 없는 댓글은 `404 COMMENT_NOT_FOUND`입니다(존재 여부 비공개).

### DELETE /comments/{id}

소프트 삭제하며 답글 자리는 보존됩니다. 성공 `204`.

## 알림

### GET /notifications

`page` / `per_page`를 받습니다. 응답 `data`:

```json
{ "notifications": [], "unread_count": 3, "pagination": { } }
```

알림 항목: `id`, `type`(`like` \| `comment` \| `follow` \| `mention` \| `system`), `actor`(선택), `message`, `link`(선택), `is_read`, `created_at`.

### GET /notifications/unread-count

배지 갱신용으로 `data.unread_count`만 반환합니다. WebSocket/SSE는 없으므로 HTTP로 주기적으로 조회하세요.

```bash
curl -sS "https://zuzunza.com/api/v1/notifications/unread-count" \
  -H "Authorization: Bearer $ACCESS"
```

### POST /notifications/read-all

`data.updated` — 읽음으로 바뀐 알림 수.

### POST /notifications/{id}/read

본인 알림만 처리합니다. 성공 `data`: `{ "id": "…", "is_read": true }`. 없으면 `404 NOTIFICATION_NOT_FOUND`.

## DM

1:1 대화만 지원하며 그룹 대화, 종단 간 암호화, 실시간 읽음 동기화는 제공하지 않습니다. 참여자가 아니면 대화의 존재 여부도 숨기고 `404 CONVERSATION_NOT_FOUND`를 반환합니다.

### GET /dm/conversations

| 쿼리 | 기본값 | 설명 |
|---|---|---|
| `limit` | 20 | 페이지 크기 |
| `before` | — | 대화 id 커서 |

응답 `data`: `conversations`, `next_cursor`(마지막 대화 id).

### POST /dm/conversations

| 필드 | 설명 |
|---|---|
| `user_id` | 상대 사용자 id(예: `usr_42`). 있으면 우선 |
| `handle` | `user_id`가 없을 때 상대 handle |

- 자기 자신이거나 상대가 없으면 `422 VALIDATION_ERROR`.
- 이미 대화가 있으면 기존 대화를 목록과 같은 형식으로 반환합니다. 성공 `201` · `data.conversation`.

```bash
curl -sS -X POST "https://zuzunza.com/api/v1/dm/conversations" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{"handle":"friend"}'
```

### GET /dm/conversations/{id}/messages

`limit`(기본 50), `before`. `next_cursor`는 현재 페이지 **첫 메시지의 id**입니다.

### POST /dm/conversations/{id}/messages

본문 `{ "body": "안녕하세요" }`, 최대 2000자. 성공 `201` · `data.message`.

```bash
curl -sS -X POST "https://zuzunza.com/api/v1/dm/conversations/$CONV/messages" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{"body":"안녕"}'
```

### POST /dm/conversations/{id}/read

대화를 읽음 처리합니다. `data.marked_count` — 읽음으로 바뀐 메시지 수.

## GET /users/me/{kind}

항상 현재 로그인한 사용자를 기준으로 반환합니다.

| `kind` | 의미 | 페이지네이션 / 응답 |
|---|---|---|
| `contents` 또는 `authored` | 내가 올린 작품 | `page` / `per_page` → `feeds` + `pagination` |
| `likes` 또는 `liked` | 좋아요한 작품 | 같음 |
| `bookmarks` 또는 `bookmarked` | 북마크한 작품 | 같음 |
| `posts` | 내 커뮤니티 글 | `limit`(기본 20) + `before` → `posts` + `next_cursor` |

그 밖의 `kind`는 `404 ROUTE_NOT_FOUND`입니다.

```bash
curl -sS "https://zuzunza.com/api/v1/users/me/likes?page=1&per_page=20" \
  -H "Authorization: Bearer $ACCESS"
```

## 오류

| code | HTTP | 상황 |
|---|---|---|
| `UNAUTHORIZED` | 401 | Bearer 필요 |
| `CONTENT_NOT_FOUND` | 404 | 콘텐츠 없음 |
| `CREATOR_NOT_FOUND` | 404 | 크리에이터 없음·정지 |
| `COMMENT_NOT_FOUND` | 404 | 댓글 없음 |
| `NOTIFICATION_NOT_FOUND` | 404 | 알림 없음 |
| `CONVERSATION_NOT_FOUND` | 404 | DM 없음(비참여자 포함) |
| `CANNOT_FOLLOW_SELF` | 409 | 자기 자신 팔로우 |
| `VALIDATION_ERROR` | 422 | 본문, 상대 지정 오류 등 |
| `ROUTE_NOT_FOUND` | 404 | 잘못된 `/users/me/{kind}` 등 |

## 관련 문서

- [콘텐츠](contents.md) · [피드](feeds.md)
- [인증](authentication.md)
- [오류](errors.md) · [요청 한도](rate-limits.md)
