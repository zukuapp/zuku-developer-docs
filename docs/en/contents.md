---
title: Contents
description: Create, read, update, archive, and publish ZUKU content across the Hype, Swipe, Jump, Vive, and Vine categories.
section: API
---

# Contents

> **Base URL**: `/api/v1`
> Use only the paths and fields documented here. For newer fields, check the API response and the page for that feature.

All media categories (`hype` / `swipe` / `jump` / `vive` / `vine`) share a single content contract. Get upload URLs from [Media](media.md) first, then reference them in this page's `thumbnail_url` / `media_url` / package metadata fields.

---

## Categories and `type`

| `category` | Allowed `type` | Description |
|---|---|---|
| `hype` | `interactive_longform` · `horizontal_media` · `photo_media` | Interactive long-form, landscape media, photos |
| `swipe` | `vertical_video` | Vertical short-form video |
| `jump` | `game` | HTML5 ZIP or ZWF game package |
| `vive` | `literary_work` · `serial_chapter` · `short_essay` | Writing, serials, essays |
| `vine` | `audio_track` · `score_attach` · `voice_clip` · `utau_asset` · `virtual_idol` | Audio, sheet music, voice, and sound assets |

If `category` and `type` don't match the table above, the response is `422` + `VALIDATION_ERROR` (`field: "type"`).

Age rating `age_rating`: `all` | `12` | `15` | `18` (defaults to `all` on create).

---

## GET `/api/v1/contents/{id}`

Returns public content details. JUMP drafts can be previewed only by their author with Bearer authentication; other users and guests get `404`. Archived content is also excluded from public lookups, feeds, search, and Thread. When `Authorization: Bearer …` is present, viewer-scoped fields such as `is_liked` / `is_bookmarked` / `is_following_creator` are filled in. If conversion information exists, it is attached as `content.conversion`.

**Response `data`**

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

Unknown ID → `404` · `CONTENT_NOT_FOUND`.

### curl

```bash
curl -sS "https://zuzunza.com/api/v1/contents/{id}" \
  -H "Accept: application/json"
```

### JS/TS (`fetch`)

```ts
const res = await fetch(`/api/v1/contents/${id}`, {
  headers: { Accept: 'application/json' },
});
const envelope = await res.json();
if (!envelope.success) throw new Error(envelope.error.code);
const { content } = envelope.data;
```

---

## GET `/api/v1/contents/{id}/conversion`

Returns only the **conversion status** derived from legacy SWF/FLV and similar sources. This is a separate contract from the original `media_url`.

**Response `data`**: `{ "conversion": ConversionInfo }`

| Field | Meaning |
|---|---|
| `status` | Conversion pipeline status string |
| `converter_version` | Converter version |
| `playback_url` | Playback URL (`null` or omitted when absent) |
| `preview` | Whether this is a preview |
| `poster_url` / `thumbnail_url` | Poster and thumbnail |
| `duration_sec` | Duration (seconds) |
| `source_kind` | `animation` \| `game` |
| `error_code` / `message` | On failure |

If the content has no conversion record → `404` · `CONTENT_NOT_FOUND`.

For Jump playback and the IR stream, see [Media](media.md).

---

## Automatic game thumbnails

After a JUMP game is registered, a thumbnail is generated from the actual game screen. HTML5 ZIP, ZWF, and legacy SWF are supported, and generation does not change the publish status. Existing games are checked in sequence and valid images are kept. A manually uploaded image is replaced by a generated one only when you explicitly request replacement.

### GET `/api/v1/contents/{id}/thumbnail-job`

Requires author authentication. Read progress from `data.thumbnail_job` in the success response.

| Field | Value or meaning |
|---|---|
| `status` | `none`, `pending`, `running`, `ready`, `preserved`, `failed` |
| `mode` | `audit` checks the existing image, `generate` takes a new capture, `null` when there is no job |
| `thumbnail_url` | URL of the image currently shown |
| `thumbnail_origin` | `legacy`, `manual`, `automatic` |
| `attempt_count` | Attempts for the current job, up to 3 |
| `error_code` | Failure code or `null` |
| `can_generate` | Whether the generation service is available |
| `updated_at` | Time of the last status change |
| `thumbnail_revision` | String indicating the order of image changes |

While `pending` or `running`, you can poll every 5 seconds. `preserved` means the existing image was kept. If the source is missing or the game cannot run, the status becomes `failed`; a failure screen is never treated as a successful thumbnail.

### POST `/api/v1/contents/{id}/thumbnail-job`

The author requests generation or regeneration. The default body is `{}`; to replace a manually uploaded image, send `{ "replace_manual": true }`. Success returns `202 Accepted` with the same `data.thumbnail_job` shape. If a job is already pending or running, no duplicate job is created.

Requesting without the replacement flag when a manual image exists returns `409` · `MANUAL_THUMBNAIL_PROTECTED`. If the generation service isn't ready, the response is `503` · `THUMBNAIL_WORKER_UNAVAILABLE`. Games owned by other authors and archived games return `404`.

If the source package or manual image changes during capture, the earlier job's result is discarded. Replacing a game's source schedules a new capture when needed, without changing the publish time or ranking basis of a published game.

---

## GET `/api/v1/contents/{id}/recommendations`

Related recommendations.

| Query | Default | Range | Description |
|---|---|---|---|
| `limit` | `8` | **1–50** (clamped) | Number of items per request |
| `offset` | `0` | ≥ 0 | Number of items to skip |

**Response `data`**

```json
{
  "recommendations": [ /* Content[] */ ],
  "pagination": {
    "total": 0,
    "limit": 8,
    "offset": 0,
    "has_more": false
  }
}
```

If the base content doesn't exist → `404` · `CONTENT_NOT_FOUND`.
`has_more` is computed with LIMIT+1. When more items exist, `total` is a lower bound (`offset+limit+1`).
For Jump details, `GET /jump/games/{id}?include=related,popular` returns the same shelf in a single request.

### curl

```bash
curl -sS "https://zuzunza.com/api/v1/contents/{id}/recommendations?limit=8&offset=0"
```

### JS/TS

```ts
const q = new URLSearchParams({ limit: '8', offset: '0' });
const res = await fetch(`/api/v1/contents/${id}/recommendations?${q}`);
const { data } = await res.json();
// data.recommendations, data.pagination
```

---

## POST `/api/v1/contents`

Creates content. **Authentication required**: `Authorization: Bearer <access_token>` **or** `X-API-Key: <developer_key>`.

Success → `201 Created` · `data.content`.

### `CreateContentRequest` fields

| Field | Required | Notes |
|---|---|---|
| `category` | Yes | `hype` \| `swipe` \| `jump` \| `vive` \| `vine` |
| `type` | Yes | JSON key name is `type` |
| `title` | Yes | 1–100 characters (whitespace only is not allowed) |
| `description` | | Default `""`, up to 500 characters. VIVE bodies allow up to 200,000 characters. |
| `thumbnail_url` | | Default `""`, usually `/uploads/…` |
| `media_url` | | `string \| null`, default `null` |
| `tags` | | Default `[]`, up to 10 |
| `age_rating` | | Default `"all"` |
| `hype` | | Metadata object when the category is hype (optional) |
| `swipe` | | Metadata object when the category is swipe (optional) |
| `jump` | Required for JUMP | Created with `status: "draft"`. Publishing uses a separate publish API. |
| `publish_to_thread` | | Also post to Thread, default `true`. JUMP content isn't shown in Thread until it is published. |

File bytes are not accepted here. Get a URL from [Media](media.md) and reference it.

#### `hype` (`HypeMeta`)

| Field | Description |
|---|---|
| `hype_type` | `quiz` \| `poll` \| `story` \| `challenge` \| `interaction` |
| `wasm?` | `{ package_url, memory_cap_mb, entry_point }` |
| `video?` | `{ duration_sec, aspect_ratio, quality }`; `quality`: `S`\|`A`\|`B`\|`C` |
| `gallery?` | `{ image_urls: string[] }` |

#### `swipe` (`SwipeMeta`)

| Field | Description |
|---|---|
| `duration_sec` | Duration (seconds) |
| `resolution` | Resolution string |
| `orientation` | `portrait` \| `landscape` \| `square` |
| `aspect_ratio` | Aspect ratio string |
| `quality` | Quality grade |
| `auto_play` | Default `true` |
| `loop` | Default `true` (JSON key `loop`) |
| `audio_credit?` | Audio credit |

#### `jump` (`JumpMeta`)

| Field | Description |
|---|---|
| `game_id` | Game identifier |
| `game_type` | `html5` \| `zwf` \| `wasm` \| `unity` \| `godot` \| `other` |
| `genre` | Genre |
| `distribution_mode` | `online` \| `offline` \| `both` |
| `platform` | `{ pc, mobile, tablet }` |
| `mobile_optimized` | `{ certified, level? }` |
| `package` | `{ format, entry_point, size_bytes, hash, version, url? }`; `format`: `zip` or `zwf`. Put the upload URL in `url`. |
| `play_count` / `rating_avg` / `rating_count` | Initial stats |
| `status` | Must be `draft` on create. Becomes `published` after a successful publish. |

### curl

```bash
curl -sS -X POST "https://zuzunza.com/api/v1/contents" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "category": "swipe",
    "type": "vertical_video",
    "title": "My first short",
    "description": "Description",
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

With a developer key:

```bash
curl -sS -X POST "https://zuzunza.com/api/v1/contents" \
  -H "X-API-Key: $ZUKU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ … }'
```

### JS/TS

```ts
async function createContent(token: string, body: unknown) {
  const res = await fetch('/api/v1/contents', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  });
  const envelope = await res.json();
  if (!envelope.success) {
    throw Object.assign(new Error(envelope.error.message), {
      code: envelope.error.code,
      details: envelope.error.details,
      status: res.status,
    });
  }
  return envelope.data.content;
}
```

---

## PATCH `/api/v1/contents/{id}`

Partial update. **Bearer only** (`X-API-Key` is not accepted). Only the author can update their own content.

`UpdateContentRequest`: only the fields you send are updated.

| Field | Validation |
|---|---|
| `title?` | 1–100 characters |
| `description?` | ≤ 500 characters; ≤ 200,000 for VIVE |
| `tags?` | ≤ 10 |
| `age_rating?` | `all`\|`12`\|`15`\|`18` |
| `thumbnail_url?` | String |

Success → `200` · `data.content`. Missing or not permitted → `404` · `CONTENT_NOT_FOUND` (the two cases are not distinguished).

### curl

```bash
curl -sS -X PATCH "https://zuzunza.com/api/v1/contents/{id}" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Updated title","tags":["a","b"]}'
```

### JS/TS

```ts
const res = await fetch(`/api/v1/contents/${id}`, {
  method: 'PATCH',
  headers: {
    Authorization: `Bearer ${token}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ title: 'Updated title' }),
});
const envelope = await res.json();
if (!envelope.success) throw new Error(envelope.error.code);
```

---

## DELETE `/api/v1/contents/{id}`

Soft **archive**. **Bearer only**, owner only. The content is hidden from public feeds, search, recommendations, and linked Thread posts.

Success → `200` · the archived `data.content`.

### curl

```bash
curl -sS -X DELETE "https://zuzunza.com/api/v1/contents/{id}" \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

---

## Likes and bookmarks (summary)

The detailed social and interaction contracts are in [Social](social.md). This section only summarizes the content-side boundary.

| Method | Path | Auth | Behavior |
|---|---|---|---|
| `POST` | `/api/v1/contents/{id}/like` | Bearer | Toggle like → `{ is_liked, like_count }` |
| `POST` | `/api/v1/contents/{id}/bookmark` | Bearer | Toggle bookmark → `{ is_bookmarked, bookmark_count }` |

Not authenticated → `401` · `UNAUTHORIZED`. Unknown content → `404` · `CONTENT_NOT_FOUND`.

---

## Related pages

- [Media](media.md): uploads, Jump play/stream/swf, conversion
- [Errors](errors.md): envelope, status codes, error codes
- [Rate limits](rate-limits.md): request limits
- [Changelog](changelog.md): versions and change history

## JUMP draft → publish

1. Upload an HTML5 ZIP or ZWF package through [uploads](media.md).
2. Create a draft with `POST /contents` using `category: "jump"`, `type: "game"`, and `jump.status: "draft"`.
3. As the owner, confirm the game runs, then send the publish request below.

### POST `/api/v1/contents/{id}/publish`

**The author's Bearer session is required.** No request body is needed.

```bash
curl -sS -X POST "https://zuzunza.com/api/v1/contents/$CONTENT_ID/publish" \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

Success is `200` · `data.content`, and `jump.status` becomes `published`. The package files and entry point are re-checked before the content goes public. Repeated or concurrent requests never create duplicate Thread posts and keep the original publish time. Regular saves don't change the original publish time either.

| HTTP | Situation |
|---|---|
| `401` | Not authenticated |
| `404` | Unknown content, content owned by another author, or archived |
| `409` | Not a publishable draft, or pending review, rejected, or changes requested |
| `422` | Executable package is missing or invalid |
| `503` | Storage failure. Handled atomically so that the draft and Thread are never partially published. |

Drafts are hidden from all content and game lookups except the owner's preview, and from public feeds, search, other users' profiles, and Thread. Upload URLs themselves are public file addresses, so don't use them to store secret files.
