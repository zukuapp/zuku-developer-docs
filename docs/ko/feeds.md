---
title: 피드
description: HYPE·SWIPE·JUMP 미디어 피드, 커뮤니티 타임라인과 짧은 글(posts), 해시태그, JUMP 게임 목록 정렬 API를 설명합니다.
section: API
---

# 피드

미디어 피드(HYPE / SWIPE / JUMP)와 커뮤니티 짧은 글(posts) API입니다. 미디어 피드는 `page`/`per_page` 페이지네이션을, 커뮤니티 타임라인과 스레드는 커서 페이지네이션을 사용합니다.

**Base URL**: `https://zuzunza.com/api/v1`

## 빠른 예제

```bash
curl -sS "https://zuzunza.com/api/v1/feeds?category=hype&page=1&per_page=20"
curl -sS "https://zuzunza.com/api/v1/feed?limit=20"
```

## 개요

| 영역 | 경로 | 설명 |
|---|---|---|
| 미디어 피드 | `/feeds`, `/feeds/{category}` | 작품(콘텐츠) 목록, `page` / `per_page` |
| 커뮤니티 타임라인 | `/feed` | 짧은 글 타임라인, 커서 `before` |
| 커뮤니티 글 | `/posts…` | 단건, 스레드, 답글, 좋아요, 수정, 삭제 |

**인증**

- 읽기(feeds, feed, 글 단건·스레드): Bearer 선택. 로그인하면 `is_liked` 등 뷰어 상태가 채워질 수 있습니다.
- 쓰기(작성, 답글, 좋아요, 수정, 삭제): **Bearer 필수**. 이 경로들은 `X-API-Key`를 받지 않습니다.

응답은 공통 형식 `{ success, data, meta }` / `{ success, error, meta }`를 따르며, 삭제 성공은 `204 No Content`입니다.

> 글 목록용 `GET /posts` 경로는 **없습니다**. 목록은 `GET /feed` 또는 `GET /users/me/posts`([소셜](social.md))를 사용하세요.

## 엔드포인트 요약

| Method | Path | 인증 | 설명 |
|---|---|---|---|
| `GET` | `/feeds` | 선택 | 전체 또는 카테고리별 미디어 피드 |
| `GET` | `/feeds/hype` | 선택 | HYPE만 |
| `GET` | `/feeds/swipe` | 선택 | SWIPE 전용 피드 |
| `GET` | `/feeds/jump` | 선택 | JUMP만 |
| `GET` | `/feed` | 선택 | 커뮤니티 타임라인 |
| `POST` | `/posts` | Bearer | 글 작성 → `201` |
| `GET` | `/posts/{id}` | 선택 | 글 단건 |
| `PATCH` | `/posts/{id}` | Bearer | 내 글 본문·사진 부분 수정 |
| `GET` | `/posts/hashtags` | 없음 | 최근 7일 인기 태그·접두사 검색 |
| `GET` | `/posts/{id}/thread` | 선택 | 스레드(루트 + 답글) |
| `POST` | `/posts/{id}/replies` | Bearer | 답글 → `201` |
| `POST` | `/posts/{id}/like` | Bearer | 좋아요 설정 |
| `DELETE` | `/posts/{id}/like` | Bearer | 좋아요 해제 |
| `DELETE` | `/posts/{id}` | Bearer | 소프트 삭제 → `204` |

## 페이지네이션

### page / per_page (미디어 피드)

| 쿼리 | 기본값 | 규칙 |
|---|---|---|
| `page` | `1` | 최소 1 |
| `per_page` | `20` | 최소 1 |

`data.pagination` 예:

```json
{
  "page": 1,
  "per_page": 20,
  "total": 113405,
  "total_pages": 5671,
  "has_next": true,
  "has_prev": false,
  "next_cursor": null,
  "prev_cursor": null
}
```

미디어 `/feeds` 계열은 `sort` / `order` 쿼리를 **사용하지 않으며**, 서버가 정한 순서로 반환합니다.

### 커서 (커뮤니티)

| 쿼리 | 용도 |
|---|---|
| `limit` | 페이지 크기(`> 0`) |
| `before` | 타임라인·내 글: 이 id보다 **오래된** 쪽 |
| `after` | 스레드: 이 id **이후** 쪽 |

| 엔드포인트 | `limit` 기본값 | 커서 |
|---|---|---|
| `GET /feed` | 20 | `before` → 응답 `next_cursor` |
| `GET /posts/{id}/thread` | 50 | `after` → 응답 `next_cursor` |

`next_cursor`는 현재 페이지 **마지막 항목의 id**입니다. 빈 페이지면 `null`이므로 "더 불러오기"를 끄면 됩니다.

## GET /feeds

| 쿼리 | 설명 |
|---|---|
| `category` | `hype` \| `swipe` \| `jump`. 인식할 수 없는 값은 전체 피드로 처리될 수 있습니다. |
| `page`, `per_page` | [페이지네이션](#page--per_page-미디어-피드) 참고 |

응답 `data`:

```json
{ "feeds": [], "pagination": { } }
```

`feeds`는 콘텐츠 배열이며, 변환 정보가 있으면 서버가 함께 포함합니다.

### 카테고리 단축 경로

| Path | 동작 |
|---|---|
| `GET /feeds/hype` | `category=hype`와 같음 |
| `GET /feeds/swipe` | SWIPE 전용 피드 |
| `GET /feeds/jump` | `category=jump`와 같음 |

단축 경로도 `page` / `per_page`를 받습니다.

```bash
curl -sS "https://zuzunza.com/api/v1/feeds/swipe?page=1&per_page=10"
```

## GET /feed

커뮤니티 짧은 글 타임라인입니다.

| 쿼리 | 설명 |
|---|---|
| `limit` | 기본 20 |
| `before` | 커서(이전 응답의 `next_cursor`) |
| `q` | 일반 본문 검색 |
| `tag` | 본문의 `#태그`를 정확히 검색. `q`와 함께 오면 `tag`가 우선 |

`tag`는 한글·Unicode 태그를 지원하며 호환 문자와 영문 대소문자를 정규화합니다. 예: `GET /feed?tag=게임`은 `#게임`을 찾습니다.

응답 `data`:

```json
{ "posts": [], "next_cursor": "post_last_id_or_null" }
```

`Post` 필드: `id`, `author`, `body`, `image_urls`, `parent_id`, `root_id`, `like_count`, `reply_count`, `is_liked`, `is_deleted`, `created_at`, `updated_at`

```bash
curl -sS "https://zuzunza.com/api/v1/feed?limit=20&before=$POST_ID"
```

## POST /posts

| 필드 | 필수 | 규칙 |
|---|---|---|
| `body` | 조건부 | 최대 280자. 사진이 있으면 생략할 수 있습니다. |
| `image_urls` | 아니요 | 최대 4장. 본인이 업로드한 10MB 이하 JPEG·PNG·WEBP·GIF·AVIF |

```bash
curl -sS -X POST "https://zuzunza.com/api/v1/posts" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{"body":"안녕하세요 #ZUKU","image_urls":["/uploads/2026-09/이미지-id.jpg"]}'
```

- `201` — `data.post`
- `422` — 본문 길이, 사진 수, 소유권, 크기 등 검증 실패
- `401` — 미인증

## GET /posts/{id}

성공 시 `data.post`, 없으면 `404 POST_NOT_FOUND`.

## PATCH /posts/{id}

작성자만 호출할 수 있으며 `body`와 `image_urls` 중 전달한 필드만 바꿉니다.

- `image_urls: []`는 사진 전체 삭제입니다.
- 수정 결과 본문과 사진이 모두 없으면 `422`이며 기존 글은 그대로 유지됩니다.

```bash
curl -sS -X PATCH "https://zuzunza.com/api/v1/posts/$POST_ID" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{"body":"수정한 글","image_urls":[]}'
```

## GET /posts/hashtags

접두사 `q`에 맞는 최근 7일 태그를 최대 8개 반환합니다. 예: `GET /posts/hashtags?q=게`

응답 `data`:

| 필드 | 설명 |
|---|---|
| `tags[]` | `{ tag, count, today_count, source: "community" }` |
| `window_days` | `7` |

최근 하루 글 수, 7일 글 수 순으로 정렬하며 삭제된 글은 제외합니다.

## GET /posts/{id}/thread

답글 id로 호출해도 그 글이 속한 스레드(`root_id`)를 반환합니다. 화면에서는 `parent_id`로 트리를 구성하세요.

쿼리: `limit`(기본 50), `after`

```json
{ "root_id": "…", "posts": [], "next_cursor": "…" }
```

```bash
curl -sS "https://zuzunza.com/api/v1/posts/$POST_ID/thread?limit=50"
```

## POST /posts/{id}/replies

부모 글(또는 스레드 안의 글)에 답글을 작성합니다. 본문은 `{ "body": "…", "image_urls": [] }`이며 루트 글과 같은 사진 규칙을 따릅니다. 성공 `201`, 부모가 없으면 `404 POST_NOT_FOUND`.

## 좋아요

| Method | Path | 의미 |
|---|---|---|
| `POST` | `/posts/{id}/like` | 좋아요 설정 |
| `DELETE` | `/posts/{id}/like` | 좋아요 해제 |

응답 `data`: `{ "is_liked": true, "like_count": 12 }`

```bash
curl -sS -X POST "https://zuzunza.com/api/v1/posts/$POST_ID/like" \
  -H "Authorization: Bearer $ACCESS"
```

## DELETE /posts/{id}

소프트 삭제하며 답글 자리는 보존됩니다. 작성자만 성공(`204`)하며, 다른 사람의 글과 없는 글은 모두 `404 POST_NOT_FOUND`입니다(존재 여부 비공개).

## JUMP 게임 목록 정렬

`GET /jump/games`([미디어](media.md))는 `sort`, `page`, `per_page`, `source`, `exclude_ids` 등의 쿼리를 받습니다.

| `sort` | 동작 |
|---|---|
| 생략 · `hot` · `recommended` | 신규 공개 게임을 먼저 보여 준 뒤 기존 인기 추천 |
| `new` · `latest` · `recent` | 최초 공개 시각 내림차순 |
| `top` | 기존 인기순 |

- 신규 우선 기간은 최근 7일 공개 게임 수 `N`에 따라 `min(7일, 7일 × 6 / max(N, 1))`입니다. 기간 안의 게임은 최초 공개 시각 내림차순으로 먼저 나오며, 반응 수나 썸네일 유무는 이 순서를 뒤집지 않습니다. 기간이 끝나면 일반 추천 순서로 돌아갑니다.
- `N`은 전체 공개 JUMP 게임 기준이므로 `source`나 `exclude_ids`에 따라 달라지지 않습니다. 초안, 아카이브, 미래 공개 시각은 제외합니다.
- 오래 저장한 초안을 오늘 처음 게시하면 새 게임으로 취급하며, 재요청이나 저장으로 공개 시각이 갱신되지 않습니다.
- 페이지 순서는 요청 시점의 공개 상태·반응·시간을 반영합니다. `pagination.has_next`와 `next_cursor`를 사용하고, 필터가 다른 요청의 커서를 재사용하지 마세요.

```bash
curl -sS "https://zuzunza.com/api/v1/jump/games?sort=new&page=1&per_page=20"
```

## 오류

| code | HTTP | 상황 |
|---|---|---|
| `UNAUTHORIZED` | 401 | Bearer가 필요한 경로 |
| `POST_NOT_FOUND` | 404 | 글이 없거나 권한 없음 |
| `VALIDATION_ERROR` | 422 | 본문 길이, 사진 규칙 등 |
| `ROUTE_NOT_FOUND` | 404 | 존재하지 않는 경로 |

## 관련 문서

- [콘텐츠](contents.md) · [미디어](media.md)
- [소셜](social.md) — 내 글 목록, 댓글, 알림
- [오류](errors.md) · [요청 한도](rate-limits.md)
