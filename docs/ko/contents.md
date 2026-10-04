---
title: 콘텐츠
description: HYPE, SWIPE, JUMP, VIVE, VINE 콘텐츠의 조회, 생성, 수정, 아카이브, JUMP 게시와 썸네일 작업 API를 설명합니다.
section: API
---

# 콘텐츠

ZUKU의 모든 작품은 하나의 콘텐츠 계약으로 다룹니다. 카테고리는 `hype`, `swipe`, `jump`, `vive`, `vine`이며, 파일은 먼저 [미디어](media.md)의 업로드 API로 올린 뒤 받은 URL을 `thumbnail_url`, `media_url`, 패키지 필드에 넣습니다.

**Base URL**: `https://zuzunza.com/api/v1`

## 빠른 예제

```bash
curl -sS "https://zuzunza.com/api/v1/contents/$CONTENT_ID" \
  -H "Accept: application/json"
```

## 엔드포인트 요약

| Method | Path | 인증 | 설명 |
|---|---|---|---|
| `GET` | `/contents/{id}` | 선택 | 콘텐츠 상세 |
| `GET` | `/contents/{id}/conversion` | 없음 | 변환 상태 |
| `GET` | `/contents/{id}/recommendations` | 없음 | 관련 추천 |
| `POST` | `/contents` | Bearer 또는 `X-API-Key` | 생성 → `201` |
| `PATCH` | `/contents/{id}` | Bearer(작성자) | 부분 수정 |
| `DELETE` | `/contents/{id}` | Bearer(작성자) | 아카이브 |
| `POST` | `/contents/{id}/publish` | Bearer(작성자) | JUMP 초안 게시 |
| `GET` | `/contents/{id}/thumbnail-job` | Bearer(작성자) | 썸네일 작업 상태 |
| `POST` | `/contents/{id}/thumbnail-job` | Bearer(작성자) | 썸네일 생성 요청 → `202` |
| `POST` | `/contents/{id}/like` | Bearer | 좋아요 토글 |
| `POST` | `/contents/{id}/bookmark` | Bearer | 북마크 토글 |

## 카테고리와 type

| `category` | 허용 `type` | 설명 |
|---|---|---|
| `hype` | `interactive_longform` · `horizontal_media` · `photo_media` | 인터랙티브 롱폼, 가로형 미디어, 사진 |
| `swipe` | `vertical_video` | 세로형 숏폼 영상 |
| `jump` | `game` | HTML5 ZIP·ZWF 게임 패키지 |
| `vive` | `literary_work` · `serial_chapter` · `short_essay` | 글, 연재, 에세이 |
| `vine` | `audio_track` · `score_attach` · `voice_clip` · `utau_asset` · `virtual_idol` | 오디오, 악보, 음성, 음원 자산 |

`category`와 `type` 조합이 맞지 않으면 `422 VALIDATION_ERROR`(`field: "type"`)입니다. 연령 등급 `age_rating`은 `all` | `12` | `15` | `18`이며 기본값은 `all`입니다.

## GET /contents/{id}

공개 콘텐츠 상세를 조회합니다.

- `Authorization: Bearer …`를 보내면 `is_liked`, `is_bookmarked`, `is_following_creator` 등 뷰어 필드가 채워집니다.
- JUMP 초안은 작성자만 Bearer로 미리 볼 수 있으며, 다른 사용자와 게스트에게는 `404`입니다.
- 아카이브된 콘텐츠는 공개 조회, 피드, 검색, Thread에서 제외됩니다.
- 변환 정보가 있으면 `content.conversion`에 포함됩니다.

### 응답

`200 OK` — `data`:

```json
{
  "content": {
    "id": "…",
    "category": "hype",
    "type": "horizontal_media",
    "title": "…",
    "description": "…",
    "thumbnail_url": "/uploads/…",
    "media_url": "/uploads/…",
    "creator": { "id": "…", "display_name": "…", "handle": "…", "avatar_url": "…", "is_verified": false },
    "stats": { "like_count": 0, "comment_count": 0, "view_count": 0, "share_count": 0, "bookmark_count": 0 },
    "tags": [],
    "age_rating": "all",
    "is_liked": false,
    "is_bookmarked": false,
    "is_following_creator": false,
    "created_at": "…",
    "updated_at": "…",
    "hype": null,
    "swipe": null,
    "jump": null,
    "conversion": null
  }
}
```

없는 ID는 `404 CONTENT_NOT_FOUND`입니다.

## GET /contents/{id}/conversion

레거시 SWF/FLV 등에서 파생된 **변환 상태**만 조회합니다. 원본 `media_url`과는 별개입니다.

응답 `data`: `{ "conversion": ConversionInfo }`

| 필드 | 설명 |
|---|---|
| `status` | 변환 상태 문자열 |
| `converter_version` | 변환기 버전 |
| `playback_url` | 재생 URL(없으면 `null` 또는 생략) |
| `preview` | 미리보기 여부 |
| `poster_url` / `thumbnail_url` | 포스터, 썸네일 |
| `duration_sec` | 길이(초) |
| `source_kind` | `animation` \| `game` |
| `error_code` / `message` | 실패 시 |

변환 레코드가 없으면 `404 CONTENT_NOT_FOUND`입니다. JUMP 재생과 IR 스트림은 [미디어](media.md)를 참고하세요.

```bash
curl -sS "https://zuzunza.com/api/v1/contents/$CONTENT_ID/conversion"
```

## GET /contents/{id}/recommendations

관련 추천 목록을 반환합니다.

| 쿼리 | 기본값 | 범위 | 설명 |
|---|---|---|---|
| `limit` | `8` | 1–50 (범위 밖은 보정) | 가져올 개수 |
| `offset` | `0` | 0 이상 | 건너뛸 개수 |

```json
{
  "recommendations": [],
  "pagination": { "total": 0, "limit": 8, "offset": 0, "has_more": false }
}
```

- 기준 콘텐츠가 없으면 `404 CONTENT_NOT_FOUND`입니다.
- `has_more`는 한 개를 더 조회해 계산하며, 더 있을 때 `total`은 하한값(`offset + limit + 1`)입니다.
- JUMP 상세는 `GET /jump/games/{id}?include=related,popular`로 같은 추천 목록을 함께 받을 수 있습니다.

```bash
curl -sS "https://zuzunza.com/api/v1/contents/$CONTENT_ID/recommendations?limit=8&offset=0"
```

## POST /contents

콘텐츠를 생성합니다. `Authorization: Bearer <access_token>` **또는** `X-API-Key: <developer_key>`가 필요합니다. 파일 바이트는 받지 않으므로 [미디어](media.md)에서 URL을 먼저 받으세요.

### 요청 본문

| 필드 | 필수 | 설명 |
|---|---|---|
| `category` | 예 | `hype` \| `swipe` \| `jump` \| `vive` \| `vine` |
| `type` | 예 | [카테고리와 type](#카테고리와-type) 참고 |
| `title` | 예 | 1–100자, 공백만은 불가 |
| `description` | 아니요 | 기본 `""`, 최대 500자. VIVE 본문은 최대 200,000자 |
| `thumbnail_url` | 아니요 | 기본 `""`, 보통 `/uploads/…` |
| `media_url` | 아니요 | `string \| null`, 기본 `null` |
| `tags` | 아니요 | 기본 `[]`, 최대 10개 |
| `age_rating` | 아니요 | 기본 `"all"` |
| `hype` | 아니요 | hype 메타 객체 |
| `swipe` | 아니요 | swipe 메타 객체 |
| `jump` | JUMP에서 필수 | `status: "draft"`로 생성하며, 공개는 [게시 API](#post-contentsidpublish)로 합니다. |
| `publish_to_thread` | 아니요 | Thread 동시 게시, 기본 `true`. JUMP는 공개 전까지 Thread에 나타나지 않습니다. |

#### hype

| 필드 | 설명 |
|---|---|
| `hype_type` | `quiz` \| `poll` \| `story` \| `challenge` \| `interaction` |
| `wasm` (선택) | `{ package_url, memory_cap_mb, entry_point }` |
| `video` (선택) | `{ duration_sec, aspect_ratio, quality }` — `quality`: `S` \| `A` \| `B` \| `C` |
| `gallery` (선택) | `{ image_urls: string[] }` |

#### swipe

| 필드 | 설명 |
|---|---|
| `duration_sec` | 길이(초) |
| `resolution` | 해상도 문자열 |
| `orientation` | `portrait` \| `landscape` \| `square` |
| `aspect_ratio` | 비율 문자열 |
| `quality` | 품질 등급 |
| `auto_play` | 기본 `true` |
| `loop` | 기본 `true` |
| `audio_credit` (선택) | 음원 크레딧 |

#### jump

| 필드 | 설명 |
|---|---|
| `game_id` | 게임 식별자 |
| `game_type` | `html5` \| `zwf` \| `wasm` \| `unity` \| `godot` \| `other` |
| `genre` | 장르 |
| `distribution_mode` | `online` \| `offline` \| `both` |
| `platform` | `{ pc, mobile, tablet }` |
| `mobile_optimized` | `{ certified, level? }` |
| `package` | `{ format, entry_point, size_bytes, hash, version, url? }` — `format`은 `zip` 또는 `zwf`, `url`에 업로드 URL |
| `play_count` / `rating_avg` / `rating_count` | 통계 초기값 |
| `status` | 생성 시 `draft` 필수, 게시 후 `published` |

```bash
curl -sS -X POST "https://zuzunza.com/api/v1/contents" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "category": "swipe",
    "type": "vertical_video",
    "title": "첫 숏폼",
    "description": "설명",
    "thumbnail_url": "/uploads/2026-08/….jpg",
    "media_url": "/uploads/2026-08/….mp4",
    "tags": ["demo"],
    "age_rating": "all",
    "swipe": {
      "duration_sec": 15,
      "resolution": "1080x1920",
      "orientation": "portrait",
      "aspect_ratio": "9:16",
      "quality": "A",
      "auto_play": true,
      "loop": true
    }
  }'
```

개발자 키를 쓸 때는 `Authorization` 대신 `-H "X-API-Key: $ZUKU_API_KEY"`를 보냅니다.

### 응답

`201 Created` — `data.content`. 검증 실패는 `422 VALIDATION_ERROR`(`error.details`에 필드 정보).

## PATCH /contents/{id}

전달한 필드만 수정합니다. **Bearer만** 허용하며(`X-API-Key` 불가) 작성자 본인 콘텐츠만 수정할 수 있습니다.

| 필드 | 검증 |
|---|---|
| `title` | 1–100자 |
| `description` | 최대 500자, VIVE는 최대 200,000자 |
| `tags` | 최대 10개 |
| `age_rating` | `all` \| `12` \| `15` \| `18` |
| `thumbnail_url` | 문자열 |

성공은 `200` · `data.content`입니다. 없거나 권한이 없으면 구분 없이 `404 CONTENT_NOT_FOUND`입니다.

```bash
curl -sS -X PATCH "https://zuzunza.com/api/v1/contents/$CONTENT_ID" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"제목 수정","tags":["a","b"]}'
```

## DELETE /contents/{id}

콘텐츠를 소프트 **아카이브**합니다. **Bearer만**, 작성자만 가능합니다. 공개 피드, 검색, 추천, 연결된 Thread 게시물에서 숨겨집니다. 성공은 `200` · 아카이브된 `data.content`입니다.

```bash
curl -sS -X DELETE "https://zuzunza.com/api/v1/contents/$CONTENT_ID" \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

## JUMP 초안 게시

1. [미디어](media.md)의 업로드 API로 HTML5 ZIP 또는 ZWF 패키지를 올립니다.
2. `POST /contents`로 `category: "jump"`, `type: "game"`, `jump.status: "draft"`인 초안을 만듭니다.
3. 작성자 인증으로 게임 실행을 확인한 뒤 게시를 요청합니다.

### POST /contents/{id}/publish

작성자 Bearer 세션이 필요하며 본문은 없습니다.

```bash
curl -sS -X POST "https://zuzunza.com/api/v1/contents/$CONTENT_ID/publish" \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

- 성공: `200` · `data.content`, `jump.status`가 `published`로 바뀝니다.
- 공개 전에 패키지 파일과 실행 진입점을 다시 검사합니다.
- 여러 번 또는 동시에 요청해도 Thread를 중복 생성하지 않으며 최초 공개 시각을 유지합니다. 일반 저장도 최초 공개 시각을 바꾸지 않습니다.

| HTTP | 상황 |
|---|---|
| `401` | 인증되지 않음 |
| `404` | 없는 콘텐츠, 다른 작성자의 콘텐츠, 아카이브 |
| `409` | 게시할 수 있는 초안이 아니거나 심사 대기·반려·수정 요청 상태 |
| `422` | 실행 패키지가 없거나 유효하지 않음 |
| `503` | 저장 실패. 초안과 Thread가 일부만 게시되지 않도록 원자적으로 처리됩니다. |

초안은 작성자 미리보기를 제외한 콘텐츠·게임 조회, 공개 피드, 검색, 다른 사용자 프로필, Thread에서 숨겨집니다. 다만 업로드 URL 자체는 공개 파일 주소이므로 비밀 파일 보관에 쓰지 마세요.

## 게임 썸네일 자동 생성

JUMP 게임은 등록 후 실제 게임 화면을 캡처해 썸네일을 만듭니다. HTML5 ZIP·ZWF와 레거시 SWF를 지원하며, 생성은 게시 상태를 바꾸지 않습니다. 기존 게임은 순차 검사하고 정상 이미지는 유지합니다. 직접 올린 이미지는 명시적으로 교체를 요청할 때만 바뀝니다.

### GET /contents/{id}/thumbnail-job

작성자 인증이 필요합니다. 응답 `data.thumbnail_job`:

| 필드 | 값 또는 의미 |
|---|---|
| `status` | `none`, `pending`, `running`, `ready`, `preserved`, `failed` |
| `mode` | `audit`(기존 이미지 검사), `generate`(새 캡처), 작업이 없으면 `null` |
| `thumbnail_url` | 현재 표시할 이미지 URL |
| `thumbnail_origin` | `legacy`, `manual`, `automatic` |
| `attempt_count` | 현재 작업 시도 횟수(최대 3회) |
| `error_code` | 실패 코드 또는 `null` |
| `can_generate` | 생성 서비스 사용 가능 여부 |
| `updated_at` | 마지막 상태 변경 시각 |
| `thumbnail_revision` | 이미지 변경 순서를 나타내는 문자열 |

`pending` 또는 `running`일 때는 5초 간격으로 조회할 수 있습니다. `preserved`는 기존 이미지가 유지된 상태입니다. 원본이 없거나 게임을 실행할 수 없으면 `failed`가 되며, 실패 화면을 썸네일로 쓰지 않습니다.

### POST /contents/{id}/thumbnail-job

작성자가 생성 또는 재생성을 요청합니다. 본문 기본값은 `{}`이며, 직접 올린 이미지를 교체하려면 `{ "replace_manual": true }`를 보냅니다.

- 성공: `202 Accepted`, 같은 `data.thumbnail_job` 형식. 이미 대기·진행 중이면 작업을 중복 생성하지 않습니다.
- 교체 의사 없이 직접 올린 이미지가 있으면 `409 MANUAL_THUMBNAIL_PROTECTED`.
- 생성 서비스가 준비되지 않았으면 `503 THUMBNAIL_WORKER_UNAVAILABLE`.
- 다른 작성자의 게임이나 아카이브된 게임은 `404`.

```bash
curl -sS -X POST "https://zuzunza.com/api/v1/contents/$CONTENT_ID/thumbnail-job" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"replace_manual":true}'
```

캡처 중 원본 패키지나 직접 올린 이미지가 바뀌면 이전 작업 결과는 반영하지 않습니다. 게임 원본이 바뀌면 필요한 캡처를 다시 예약하며, 공개된 게임의 게시 시각이나 순위 기준은 바꾸지 않습니다.

## 좋아요와 북마크

| Method | Path | 인증 | 응답 `data` |
|---|---|---|---|
| `POST` | `/contents/{id}/like` | Bearer | `{ is_liked, like_count }` |
| `POST` | `/contents/{id}/bookmark` | Bearer | `{ is_bookmarked, bookmark_count }` |

둘 다 토글입니다. 미인증은 `401 UNAUTHORIZED`, 없는 콘텐츠는 `404 CONTENT_NOT_FOUND`입니다. 자세한 내용은 [소셜](social.md)을 참고하세요.

## 오류

| code / HTTP | 상황 |
|---|---|
| `CONTENT_NOT_FOUND` · 404 | 콘텐츠 없음, 권한 없음, 변환 레코드 없음 |
| `VALIDATION_ERROR` · 422 | 필드 검증 실패, `category`·`type` 불일치 |
| `UNAUTHORIZED` · 401 | 인증 필요 |
| `MANUAL_THUMBNAIL_PROTECTED` · 409 | 직접 올린 썸네일 보호 |
| `THUMBNAIL_WORKER_UNAVAILABLE` · 503 | 썸네일 생성 서비스 미준비 |

## 관련 문서

- [미디어](media.md) — 업로드, JUMP play/stream/swf, 변환
- [피드](feeds.md) · [소셜](social.md)
- [오류](errors.md) · [변경 이력](changelog.md)
