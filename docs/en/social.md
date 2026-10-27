---
title: Social
description: Likes, bookmarks, follows, comments, notifications, direct messages, and personal lists.
section: API
---

# Social

**Base URL**: `https://zuzunza.com/api/v1`

## Contents

1. [Authentication requirements](#1-authentication-requirements)
2. [Endpoints](#2-endpoints)
3. [Content social](#3-content-social)
4. [Comments](#4-comments)
5. [Notifications](#5-notifications)
6. [DM](#6-dm)
7. [Your lists (users/me)](#7-your-lists-usersme)
8. [curl and JS/TS examples](#8-curl-and-jsts-examples)

---

## 1. Authentication requirements

| Area | Auth |
|------|------|
| Content likes and bookmarks | Bearer required |
| Comment list `GET` | None (public). 404 if the content doesn't exist |
| Create, edit, delete comments | Bearer required |
| Notification list / unread-count | Bearer optional (without it, behaves as empty / close to 0) |
| Notification read-all / `{id}/read` | Bearer required |
| All DM routes | Bearer required + conversation participants only |
| `GET /users/me/{kind}` | Bearer required |

Session format: `Authorization: Bearer <access_token>`.
The social, DM, and notification write routes on this page do not accept X-API-Key (unlike other routes such as content *creation*).

Common envelope: `{ success, data, meta }` / `{ success, error, meta }`.
Comment deletion and some other deletes return 204.

---

## 2. Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `POST` | `/contents/{id}/like` | Bearer | Toggle like |
| `POST` | `/contents/{id}/bookmark` | Bearer | Toggle bookmark |
| `POST` | `/creators/{handle}/follow` | Bearer | Toggle following a creator |
| `GET` | `/contents/{id}/comments` | Public | List comments (`page`/`per_page`) |
| `POST` | `/contents/{id}/comments` | Bearer | Create a comment → `201` |
| `PATCH` | `/comments/{id}` | Bearer | Edit your comment |
| `DELETE` | `/comments/{id}` | Bearer | Soft delete → `204` |
| `GET` | `/notifications` | Optional | List notifications |
| `GET` | `/notifications/unread-count` | Optional | Unread count only |
| `POST` | `/notifications/read-all` | Bearer | Mark all as read |
| `POST` | `/notifications/{id}/read` | Bearer | Mark one as read |
| `GET` | `/dm/conversations` | Bearer | List conversations (`before` cursor) |
| `POST` | `/dm/conversations` | Bearer | Start or reuse a conversation → `201` |
| `GET` | `/dm/conversations/{id}/messages` | Bearer + participant | List messages |
| `POST` | `/dm/conversations/{id}/messages` | Bearer + participant | Send → `201` |
| `POST` | `/dm/conversations/{id}/read` | Bearer + participant | Mark conversation as read |
| `GET` | `/users/me/{kind}` | Bearer | Your works, likes, bookmarks, posts |

---

## 3. Content social

### `POST /contents/{id}/like`

Toggle. Response:

```json
{ "is_liked": true, "like_count": 42 }
```

Content not found → 404 `CONTENT_NOT_FOUND`.

### `POST /contents/{id}/bookmark`

Toggle. Response:

```json
{ "is_bookmarked": true, "bookmark_count": 7 }
```

Not authenticated → 401. Content not found → 404 `CONTENT_NOT_FOUND`.

### `POST /creators/{handle}/follow`

Toggles following or unfollowing a creator. Bearer required.

Success `200` `data`:

```json
{ "is_following": true, "follower_count": 1521 }
```

| HTTP | code | Situation |
|------|------|-----------|
| 401 | `UNAUTHORIZED` | No session |
| 404 | `CREATOR_NOT_FOUND` | Handle not found or suspended |
| 409 | `CANNOT_FOLLOW_SELF` | Following yourself |

The `is_following`, `follower_count`, and `following_count` fields in the public profile `GET /creators/{handle}` response use the same data.
The home feed with `sort=following` returns only works from authors you follow.

---

## 4. Comments

### `GET /contents/{id}/comments`

| Query | Default |
|-------|---------|
| `page` | 1 |
| `per_page` | 20 |

Response: `data.comments`, `data.pagination`.

### `POST /contents/{id}/comments`

```json
{ "body": "Great work!", "parent_id": null }
```

- `body` up to 1000 characters
- `parent_id` optional (nested reply)
- **201**: `data.comment`

### `PATCH /comments/{id}`

```json
{ "body": "Edited comment" }
```

Author only. Someone else's comment or a missing one → 404 `COMMENT_NOT_FOUND`.

### `DELETE /comments/{id}`

Soft delete (the reply's position is kept). Success 204.

---

## 5. Notifications

### `GET /notifications`

`page` / `per_page`. Response:

```json
{
  "notifications": [ ],
  "unread_count": 3,
  "pagination": { }
}
```

Notification item: `id`, `type` (`like` \| `comment` \| `follow` \| `mention` \| `system`), `actor?`, `message`, `link?`, `is_read`, `created_at`.

### `GET /notifications/unread-count`

For badge polling. Returns only `data.unread_count`.

### `POST /notifications/read-all`

`data.updated` = number of rows updated.

### `POST /notifications/{id}/read`

Your own notifications only. Success: `{ "id": "…", "is_read": true }`.
Not found → 404 `NOTIFICATION_NOT_FOUND`.

---

## 6. DM

DMs are one-to-one. If you are not a participant → 404 `CONVERSATION_NOT_FOUND`.

### `GET /dm/conversations`

`limit` (default 20), `before` (conversation id cursor).
Response: `conversations`, `next_cursor` (id of the last conversation).

### `POST /dm/conversations`

```json
{ "user_id": "usr_42" }
```

or

```json
{ "handle": "peer_handle" }
```

- `user_id` takes precedence; otherwise `handle` is used
- Yourself / user not found → 422 `VALIDATION_ERROR`
- If a conversation already exists, its summary is returned (same shape as the list) → 201 `data.conversation`

### `GET /dm/conversations/{id}/messages`

`limit` (default 50), `before`.
`next_cursor` is the id of the first message (matching the paging direction).

### `POST /dm/conversations/{id}/messages`

```json
{ "body": "Hello" }
```

Body up to 2000 characters. 201 `data.message`.

### `POST /dm/conversations/{id}/read`

`data.marked_count`.

---

## 7. Your lists (users/me)

`GET /users/me/{kind}` always uses the currently logged-in user.

| `kind` | Meaning | Pagination |
|--------|---------|------------|
| `contents` or `authored` | Works you uploaded | `page` / `per_page` → `feeds` + `pagination` |
| `likes` or `liked` | Works you liked | Same |
| `bookmarks` or `bookmarked` | Works you bookmarked | Same |
| `posts` | Your community posts | `limit` (default 20) + `before` → `posts` + `next_cursor` |

Any other `kind` → 404 `ROUTE_NOT_FOUND`.

---

## 8. curl and JS/TS examples

### Content likes, bookmarks, comments

```bash
curl -sS -X POST "https://zuzunza.com/api/v1/contents/$CID/like" \
  -H "Authorization: Bearer $ACCESS"

curl -sS -X POST "https://zuzunza.com/api/v1/contents/$CID/bookmark" \
  -H "Authorization: Bearer $ACCESS"

curl -sS "https://zuzunza.com/api/v1/contents/$CID/comments?page=1&per_page=20"

curl -sS -X POST "https://zuzunza.com/api/v1/contents/$CID/comments" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{"body":"Love it!"}'
```

```ts
const base = "https://zuzunza.com/api/v1";
const headers = {
  Authorization: `Bearer ${accessToken}`,
  "Content-Type": "application/json",
};

await fetch(`${base}/contents/${contentId}/like`, {
  method: "POST",
  headers: { Authorization: headers.Authorization },
});

const commentsRes = await fetch(
  `${base}/contents/${contentId}/comments?page=1&per_page=20`,
);
const commentsJson = await commentsRes.json();

await fetch(`${base}/contents/${contentId}/comments`, {
  method: "POST",
  headers,
  body: JSON.stringify({ body: "Love it!" }),
});
```

### Notifications

```bash
curl -sS "https://zuzunza.com/api/v1/notifications/unread-count" \
  -H "Authorization: Bearer $ACCESS"

curl -sS -X POST "https://zuzunza.com/api/v1/notifications/read-all" \
  -H "Authorization: Bearer $ACCESS"
```

```ts
const unread = await fetch(`${base}/notifications/unread-count`, {
  headers: { Authorization: `Bearer ${accessToken}` },
}).then((r) => r.json());

await fetch(`${base}/notifications/read-all`, {
  method: "POST",
  headers: { Authorization: `Bearer ${accessToken}` },
});
```

### DM

```bash
curl -sS -X POST "https://zuzunza.com/api/v1/dm/conversations" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{"handle":"friend"}'

curl -sS "https://zuzunza.com/api/v1/dm/conversations/$CONV/messages?limit=50" \
  -H "Authorization: Bearer $ACCESS"

curl -sS -X POST "https://zuzunza.com/api/v1/dm/conversations/$CONV/messages" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{"body":"Hi"}'

curl -sS -X POST "https://zuzunza.com/api/v1/dm/conversations/$CONV/read" \
  -H "Authorization: Bearer $ACCESS"
```

```ts
const convRes = await fetch(`${base}/dm/conversations`, {
  method: "POST",
  headers,
  body: JSON.stringify({ handle: "friend" }),
});
const { conversation } = (await convRes.json()).data;

await fetch(`${base}/dm/conversations/${conversation.id}/messages`, {
  method: "POST",
  headers,
  body: JSON.stringify({ body: "Hi" }),
});

await fetch(`${base}/dm/conversations/${conversation.id}/read`, {
  method: "POST",
  headers: { Authorization: headers.Authorization },
});
```

### Your lists

```bash
curl -sS "https://zuzunza.com/api/v1/users/me/likes?page=1&per_page=20" \
  -H "Authorization: Bearer $ACCESS"

curl -sS "https://zuzunza.com/api/v1/users/me/posts?limit=20" \
  -H "Authorization: Bearer $ACCESS"
```

```ts
const likes = await fetch(`${base}/users/me/likes?page=1&per_page=20`, {
  headers: { Authorization: `Bearer ${accessToken}` },
}).then((r) => r.json());

const myPosts = await fetch(`${base}/users/me/posts?limit=20`, {
  headers: { Authorization: `Bearer ${accessToken}` },
}).then((r) => r.json());
```

---

## Error codes

| code | HTTP | Situation |
|------|------|-----------|
| `UNAUTHORIZED` | 401 | Bearer required |
| `CONTENT_NOT_FOUND` | 404 | Content |
| `COMMENT_NOT_FOUND` | 404 | Comment |
| `NOTIFICATION_NOT_FOUND` | 404 | Notification |
| `CONVERSATION_NOT_FOUND` | 404 | DM (including non-participants) |
| `VALIDATION_ERROR` | 422 | Body, recipient, and similar |
| `ROUTE_NOT_FOUND` | 404 | Invalid `/users/me/{kind}` and similar |

See [Errors](errors.md) and [Rate limits](rate-limits.md) for shared behavior.
