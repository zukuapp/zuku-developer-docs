---
title: Social
description: Likes, bookmarks, follows, comments, notifications, direct messages, personal lists, and admin user APIs.
section: API
---

# Social

This page covers content social features (likes, bookmarks, comments), notifications, DMs, your own profile lists, and the admin user API.

**Base URL**

| Environment | Base URL |
|-------------|----------|
| Production | `https://zuzunza.com/api/v1` |
| Local | `http://localhost:3001/api/v1` |

## Contents

1. [Authentication requirements](#1-authentication-requirements)
2. [Endpoints](#2-endpoints)
3. [Content social](#3-content-social)
4. [Comments](#4-comments)
5. [Notifications](#5-notifications)
6. [DM](#6-dm)
7. [Your lists (users/me)](#7-your-lists-usersme)
8. [Admin users](#8-admin-users)
9. [curl and JS/TS examples](#9-curl-and-jsts-examples)

---

## 1. Authentication requirements

| Area | Auth |
|------|------|
| Content likes and bookmarks | **Bearer required** |
| Comment list `GET` | None (public). 404 if the content doesn't exist |
| Create, edit, delete comments | **Bearer required** |
| Notification list / unread-count | Bearer **optional** (without it, behaves as empty / close to 0) |
| Notification read-all / `{id}/read` | **Bearer required** |
| All DM routes | **Bearer required** + conversation participants only |
| `GET /users/me/{kind}` | **Bearer required** |
| Admin users | **Bearer + `role=admin`** (non-admins get **403** `FORBIDDEN`) |

Session format: `Authorization: Bearer <access_token>`.
The social, DM, and notification write routes on this page **do not accept X-API-Key** (unlike other routes such as content *creation*).

Common envelope: `{ success, data, meta }` / `{ success, error, meta }`.
Unlike marking a single notification as read, comment deletion and some other deletes may return **204**.

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
| `GET` | `/admin/users` | Admin | Search users |
| `GET` | `/admin/users/{id}` | Admin | User details |
| `PATCH` | `/admin/users/{id}` | Admin | Role / suspension |

---

## 3. Content social

### `POST /contents/{id}/like`

Toggle. Response:

```json
{ "is_liked": true, "like_count": 42 }
```

Content not found → **404** `CONTENT_NOT_FOUND`.

### `POST /contents/{id}/bookmark`

Toggle. Response:

```json
{ "is_bookmarked": true, "bookmark_count": 7 }
```

Not authenticated → **401**. Content not found → **404** `CONTENT_NOT_FOUND`.

### `POST /creators/{handle}/follow`

Toggles following or unfollowing a creator. **Bearer required**.

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

- `body` up to **1000 characters**
- `parent_id` optional (nested reply)
- **201**: `data.comment`

### `PATCH /comments/{id}`

```json
{ "body": "Edited comment" }
```

Author only. Someone else's comment or a missing one → **404** `COMMENT_NOT_FOUND` (to avoid revealing whether it exists).

### `DELETE /comments/{id}`

Soft delete (the reply's position is kept). Success **204**.

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

For badge polling. Returns only `data.unread_count`. (No WebSocket/SSE; single HTTP requests.)

### `POST /notifications/read-all`

`data.updated` = number of rows updated.

### `POST /notifications/{id}/read`

Your own notifications only. Success: `{ "id": "…", "is_read": true }`.
Not found → **404** `NOTIFICATION_NOT_FOUND`.

---

## 6. DM

One-to-one only. Group chats, end-to-end encryption, and real-time read sync are out of scope.
If you are not a participant, even the **existence** of the conversation is hidden → the same **404** `CONVERSATION_NOT_FOUND`.

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
- Yourself / user not found → **422** `VALIDATION_ERROR`
- If a conversation already exists, its summary is returned (same shape as the list) → **201** `data.conversation`

### `GET /dm/conversations/{id}/messages`

`limit` (default 50), `before`.
`next_cursor` is the **id of the first message** (matching the paging direction).

### `POST /dm/conversations/{id}/messages`

```json
{ "body": "Hello" }
```

Body up to **2000 characters**. **201** `data.message`.

### `POST /dm/conversations/{id}/read`

`data.marked_count`.

---

## 7. Your lists (users/me)

`GET /users/me/{kind}` always uses the **currently logged-in user** (the server applies the filter).

| `kind` | Meaning | Pagination |
|--------|---------|------------|
| `contents` or `authored` | Works you uploaded | `page` / `per_page` → `feeds` + `pagination` |
| `likes` or `liked` | Works you liked | Same |
| `bookmarks` or `bookmarked` | Works you bookmarked | Same |
| `posts` | Your community posts | `limit` (default 20) + `before` → `posts` + `next_cursor` |

Any other `kind` → **404** `ROUTE_NOT_FOUND`.

---

## 8. Admin users

All three routes require an admin user: not authenticated **401**, non-admin **403** `FORBIDDEN`.

### `GET /admin/users`

Query: `q` (search), `page`, `per_page` → `users` + `pagination`.

### `GET /admin/users/{id}`

`id` is parsed in the public format (`usr_…`). Returns details including activity counts.

### `PATCH /admin/users/{id}`

```json
{
  "role": "user",
  "is_suspended": true,
  "reason": "Violation of community policy"
}
```

- **At least one** of `role` / `is_suspended` is required
- `role`: `user` \| `admin` only
- Removing your own admin role or suspending yourself → **409** `SELF_ACTION_FORBIDDEN`

---

## 9. curl and JS/TS examples

### Content likes, bookmarks, comments

```bash
curl -sS -X POST "http://localhost:3001/api/v1/contents/$CID/like" \
  -H "Authorization: Bearer $ACCESS"

curl -sS -X POST "http://localhost:3001/api/v1/contents/$CID/bookmark" \
  -H "Authorization: Bearer $ACCESS"

curl -sS "http://localhost:3001/api/v1/contents/$CID/comments?page=1&per_page=20"

curl -sS -X POST "http://localhost:3001/api/v1/contents/$CID/comments" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{"body":"Love it!"}'
```

```ts
const base = "http://localhost:3001/api/v1";
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
curl -sS "http://localhost:3001/api/v1/notifications/unread-count" \
  -H "Authorization: Bearer $ACCESS"

curl -sS -X POST "http://localhost:3001/api/v1/notifications/read-all" \
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
curl -sS -X POST "http://localhost:3001/api/v1/dm/conversations" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{"handle":"friend"}'

curl -sS "http://localhost:3001/api/v1/dm/conversations/$CONV/messages?limit=50" \
  -H "Authorization: Bearer $ACCESS"

curl -sS -X POST "http://localhost:3001/api/v1/dm/conversations/$CONV/messages" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{"body":"Hi"}'

curl -sS -X POST "http://localhost:3001/api/v1/dm/conversations/$CONV/read" \
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
curl -sS "http://localhost:3001/api/v1/users/me/likes?page=1&per_page=20" \
  -H "Authorization: Bearer $ACCESS"

curl -sS "http://localhost:3001/api/v1/users/me/posts?limit=20" \
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

## Error codes (this page)

| code | HTTP | Situation |
|------|------|-----------|
| `UNAUTHORIZED` | 401 | Bearer required |
| `FORBIDDEN` | 403 | Non-admin calling an admin API |
| `CONTENT_NOT_FOUND` | 404 | Content |
| `COMMENT_NOT_FOUND` | 404 | Comment |
| `NOTIFICATION_NOT_FOUND` | 404 | Notification |
| `CONVERSATION_NOT_FOUND` | 404 | DM (including non-participants) |
| `VALIDATION_ERROR` | 422 | Body, recipient, and similar |
| `SELF_ACTION_FORBIDDEN` | 409 | Admin demoting or suspending themselves |
| `ROUTE_NOT_FOUND` | 404 | Invalid `/users/me/{kind}` and similar |

See [Errors](errors.md) and [Rate limits](rate-limits.md) for shared behavior.
