---
title: Feeds and Community Posts
description: Media feeds for Hype, Swipe, and Jump, plus community short posts, threads, likes, and hashtags.
section: API
---

# Feeds and Community Posts

This page covers the media feeds (Hype / Swipe / Jump) and the community short-post (posts) API.

**Base URL**

| Environment | Base URL |
|-------------|----------|
| Production | `https://zuzunza.com/api/v1` |
| Local | `http://localhost:3001/api/v1` |

## Contents

1. [Overview](#1-overview)
2. [Pagination](#2-pagination)
3. [Endpoints](#3-endpoints)
4. [Media feeds](#4-media-feeds)
5. [Community feed](#5-community-feed-get-feed)
6. [Posts](#6-posts)
7. [curl and JS/TS examples](#7-curl-and-jsts-examples)
8. [Photo editing and hashtags](#photo-editing-and-hashtags)
9. [Jump game list sorting](#jump-game-list-sorting)

---

## 1. Overview

| Area | Path prefix | Description |
|------|-------------|-------------|
| **Media feeds** | `/feeds`, `/feeds/{category}` | Lists of works (content). `page` / `per_page` |
| **Community timeline** | `/feed` | Short-post timeline. Cursor `before` |
| **Community posts** | `/posts…` | Single post, thread, replies, likes, deletion |

Authentication:

- **Reads** (feeds, feed, single post/thread): Bearer is optional. When logged in, viewer state such as `is_liked` may be filled in.
- **Writes** (create, reply, like, delete): **Bearer required**. X-API-Key is not used on these routes.

Responses follow the common envelope `{ success, data, meta }` / `{ success, error, meta }`. Successful deletes return **204 No Content**.

> **Note:** there is **no** `GET /api/v1/posts` (list) route. For lists, use `GET /feed` or `GET /users/me/posts`.

---

## 2. Pagination

### page / per_page (media feeds)

| Query | Default | Rule |
|-------|---------|------|
| `page` | `1` | Minimum 1 |
| `per_page` | `20` | Minimum 1 |

Example `data.pagination`:

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

The media `/feeds` routes **do not use `sort` / `order` queries.** The server uses a fixed sort order.

### cursor (community)

| Query | Default | Use |
|-------|---------|-----|
| `limit` | Per endpoint (below) | Page size (`> 0`) |
| `before` | None | Timeline and my posts: go **before** (older than) this id |
| `after` | None | Thread: go **after** (newer than / continuing from) this id |

| Endpoint | Default `limit` | Cursor field |
|----------|-----------------|--------------|
| `GET /feed` | 20 | `before` → response `next_cursor` |
| `GET /posts/{id}/thread` | 50 | `after` → response `next_cursor` |
| `POST` routes | — | — |

`next_cursor` is the **id of the last item** on this page. For an empty page it is `null`, at which point the client can turn off "load more".

---

## 3. Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `GET` | `/feeds` | Optional | All or per-category media feed |
| `GET` | `/feeds/hype` | Optional | Hype only |
| `GET` | `/feeds/swipe` | Optional | Swipe only |
| `GET` | `/feeds/jump` | Optional | Jump only |
| `GET` | `/feed` | Optional | Community timeline |
| `POST` | `/posts` | Bearer | Create a root post → `201` |
| `GET` | `/posts/{id}` | Optional | Single post |
| `PATCH` | `/posts/{id}` | Bearer | Partially update your post's body and photos |
| `GET` | `/posts/hashtags` | None | Popular tags from the last 7 days, prefix search |
| `GET` | `/posts/{id}/thread` | Optional | Thread (root + replies) |
| `POST` | `/posts/{id}/replies` | Bearer | Reply → `201` |
| `POST` | `/posts/{id}/like` | Bearer | Like |
| `DELETE` | `/posts/{id}/like` | Bearer | Unlike |
| `DELETE` | `/posts/{id}` | Bearer | Soft delete → `204` |

---

## 4. Media feeds

### `GET /feeds`

Query:

| Parameter | Description |
|-----------|-------------|
| `category` | `hype` \| `swipe` \| `jump` (an invalid value may be treated the same as all categories) |
| `page`, `per_page` | See the table above |

Response `data`:

```json
{
  "feeds": [ /* Content[] */ ],
  "pagination": { }
}
```

`swipe` uses a dedicated feed list. Other categories and the all-categories feed use the general content list. The server attaches conversion metadata.

### Shortcut routes

| Path | Behavior |
|------|----------|
| `GET /feeds/hype` | Same as `category=hype` |
| `GET /feeds/swipe` | Dedicated swipe feed |
| `GET /feeds/jump` | Same as `category=jump` |

Shortcut routes accept `page` / `per_page` the same way.

---

## 5. Community feed (`GET /feed`)

The community short-post timeline.

```
GET /feed?limit=20&before=post_xxx
```

Response `data`:

```json
{
  "posts": [ /* Post[] */ ],
  "next_cursor": "post_last_id_or_null"
}
```

`Post` fields: `id`, `author`, `body`, `image_urls`, `parent_id`, `root_id`, `like_count`, `reply_count`, `is_liked`, `is_deleted`, `created_at`, `updated_at`

Maximum body length: **280 characters**.

---

## 6. Posts

### `POST /posts`

```json
{ "body": "Hello #ZUKU", "image_urls": ["/uploads/2026-09/image-id.jpg"] }
```

- **201**: `data.post`
- Body up to 280 characters, up to 4 photos. Photo-only posts are allowed.
- Photos must be JPEG, PNG, WEBP, GIF, or AVIF files of 10MB or less that you uploaded yourself.
- Validation failure: **422** (body length, photo count, ownership, size, and so on)
- Not authenticated: **401**

### `GET /posts/{id}`

- Success: `data.post`
- Not found: **404** `POST_NOT_FOUND`

### `GET /posts/{id}/thread`

Even when called with a reply id, this returns the thread (`root_id`) the post belongs to. Build the tree in the UI using `parent_id`.

Query: `limit` (default 50), `after`

Response:

```json
{
  "root_id": "…",
  "posts": [ ],
  "next_cursor": "…"
}
```

### `POST /posts/{id}/replies`

Replies to a parent post (or any post in the thread). The body is `{ "body": "…", "image_urls": [] }` and uses the same photo rules as root posts.
Parent not found → **404** `POST_NOT_FOUND`.

### Like

| Method | Meaning |
|--------|---------|
| `POST /posts/{id}/like` | Like on |
| `DELETE /posts/{id}/like` | Like off |

Response:

```json
{ "is_liked": true, "like_count": 12 }
```

### `DELETE /posts/{id}`

Soft delete (the reply's position in the thread is kept). Only the owner can delete.
Someone else's post and a missing post both return **404** `POST_NOT_FOUND` (to avoid revealing whether it exists).
Success: **204**.

---

## 7. curl and JS/TS examples

### Media feeds

```bash
curl -sS "http://localhost:3001/api/v1/feeds?category=hype&page=1&per_page=20"
curl -sS "http://localhost:3001/api/v1/feeds/swipe?page=1&per_page=10"
```

```ts
const base = "http://localhost:3001/api/v1";

const feedsRes = await fetch(
  `${base}/feeds?category=hype&page=1&per_page=20`,
);
const feedsJson = await feedsRes.json();
console.log(feedsJson.data.feeds.length, feedsJson.data.pagination);
```

### Community timeline (cursor)

```bash
curl -sS "http://localhost:3001/api/v1/feed?limit=20"
curl -sS "http://localhost:3001/api/v1/feed?limit=20&before=POST_ID"
```

```ts
async function loadTimeline(before?: string) {
  const q = new URLSearchParams({ limit: "20" });
  if (before) q.set("before", before);
  const res = await fetch(`${base}/feed?${q}`);
  const json = await res.json();
  return json.data as { posts: unknown[]; next_cursor: string | null };
}

let cursor: string | null | undefined;
const page1 = await loadTimeline();
cursor = page1.next_cursor;
if (cursor) await loadTimeline(cursor);
```

### Create a post, read a thread, like

```bash
curl -sS -X POST "http://localhost:3001/api/v1/posts" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{"body":"My first post"}'

curl -sS "http://localhost:3001/api/v1/posts/$POST_ID/thread?limit=50"

curl -sS -X POST "http://localhost:3001/api/v1/posts/$POST_ID/like" \
  -H "Authorization: Bearer $ACCESS"
```

```ts
const accessToken = "…";

const createRes = await fetch(`${base}/posts`, {
  method: "POST",
  headers: {
    Authorization: `Bearer ${accessToken}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({ body: "My first post" }),
});
const { post } = (await createRes.json()).data;

const threadRes = await fetch(
  `${base}/posts/${post.id}/thread?limit=50`,
);
const thread = await threadRes.json();

await fetch(`${base}/posts/${post.id}/like`, {
  method: "POST",
  headers: { Authorization: `Bearer ${accessToken}` },
});

await fetch(`${base}/posts/${post.id}/replies`, {
  method: "POST",
  headers: {
    Authorization: `Bearer ${accessToken}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({ body: "This is a reply" }),
});
```

---

## Error codes (this page)

| code | HTTP | Situation |
|------|------|-----------|
| `UNAUTHORIZED` | 401 | Route requires Bearer |
| `POST_NOT_FOUND` | 404 | Post missing or not permitted (deletion and so on) |
| `VALIDATION_ERROR` / body validation | 422 | Body length and similar |
| `ROUTE_NOT_FOUND` | 404 | Route does not exist |

See [Errors](errors.md) and [Rate limits](rate-limits.md) for shared behavior.

---

## Photo editing and hashtags

`PATCH /posts/{id}` can be called only by the owner and changes only the fields you send among `body` and `image_urls`. `image_urls: []` removes all photos. If the result would have neither a body nor photos, the response is `422` and the existing post is kept.

`GET /feed?tag=game` searches for the exact `#game` tag in post bodies. `q` is a general body search; when `tag` is also present, `tag` takes precedence. Korean and other Unicode tags are supported, and compatibility characters and Latin letter case are normalized.

`GET /posts/hashtags?q=ga` returns up to 8 tags from the last 7 days that match the prefix. Each `data.tags` item is `{ tag, count, today_count, source: "community" }`, and `data.window_days` is `7`. Results are ordered by post count in the last day, then post count over 7 days, and deleted posts are excluded.

## Jump game list sorting

`GET /api/v1/jump/games` accepts list queries such as `sort`, `page`, `per_page`, `source`, and `exclude_ids`.

| `sort` | Behavior |
|---|---|
| Omitted · `hot` · `recommended` | Newly published games first, then existing popular recommendations |
| `new` · `latest` · `recent` | Original publish time, descending |
| `top` | Existing popularity order |

The new-first window depends on `N`, the number of games published in the last 7 days: `min(7 days, 7 days × 6 / max(N, 1))`. Games within the window come first, ordered by original publish time descending. Reaction counts and whether a thumbnail exists never override this priority order. Once the window expires exactly, the game returns to the regular recommendation order.

`N` is counted over all published JUMP games, so it doesn't change with the `source` or `exclude_ids` filters. Drafts, archived games, and future publish times are excluded. A long-saved draft published for the first time today is treated as a new game, and repeated requests or saves don't refresh the publish time.

Page order reflects publish state, reactions, and time as of the request. Use `pagination.has_next` and `next_cursor`, and don't reuse a cursor across different filters.
