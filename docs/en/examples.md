---
title: Examples
description: End-to-end ZUKU API scenarios that connect authentication, captcha, feeds, content, social, and Game Cloud.
section: Guide
---

# Examples

A collection of **real-world scenarios** that connect authentication, captcha, feeds, content, and social features.
All examples call the HTTP API directly with `curl` or `fetch`; no npm SDK is required. The base URL is production, `https://zuzunza.com/api/v1`. In the curl examples, set it first:

```bash
API="https://zuzunza.com/api/v1"
```

## Contents

1. [Shared helper](#1-shared-helper)
2. [Sign up → log in → me](#2-sign-up--log-in--me)
3. [Sign up with captcha](#3-sign-up-with-captcha)
4. [Read public feeds](#4-read-public-feeds)
5. [Create content and upload](#5-create-content-and-upload)
6. [Likes, bookmarks, follows](#6-likes-bookmarks-follows)
7. [Comments, notifications, DMs](#7-comments-notifications-dms)
8. [Game Cloud (online games)](#8-game-cloud-online-games)
9. [Error handling pattern](#9-error-handling-pattern)

---

## 1. Shared helper

```ts
const API = "https://zuzunza.com/api/v1";

type Envelope<T> =
  | { success: true; data: T; meta: { request_id: string; timestamp: string; version: string } }
  | {
      success: false;
      error: { code: string; message: string; details?: { field: string; message: string }[] };
      meta: { request_id: string; timestamp: string; version: string };
    };

async function api<T>(
  path: string,
  init: RequestInit & { token?: string; apiKey?: string } = {},
): Promise<T> {
  const headers = new Headers(init.headers);
  headers.set("Accept-Language", "ko-KR");
  headers.set("X-Request-Id", crypto.randomUUID());
  if (init.body && !headers.has("Content-Type") && !(init.body instanceof FormData)) {
    headers.set("Content-Type", "application/json");
  }
  if (init.token) headers.set("Authorization", `Bearer ${init.token}`);
  if (init.apiKey) headers.set("X-API-Key", init.apiKey);

  const res = await fetch(`${API}${path}`, { ...init, headers });
  if (res.status === 204) return undefined as T;
  const env = (await res.json()) as Envelope<T>;
  if (!env.success) {
    const err = new Error(`${env.error.code}: ${env.error.message}`);
    (err as Error & { code?: string }).code = env.error.code;
    throw err;
  }
  return env.data;
}
```

The helper returns the envelope's `data`.

---

## 2. Sign up → log in → me

### curl

```bash
# Log in (environment with the captcha gate disabled)
curl -sS -X POST "$API/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"identifier":"demo_user","password":"SecureP@ss123"}'

# me
curl -sS "$API/auth/me" -H "Authorization: Bearer $ACCESS"
```

### JS/TS

```ts
const tokens = await api<{
  tokens: { access_token: string; refresh_token: string; expires_in: number };
}>("/auth/login", {
  method: "POST",
  body: JSON.stringify({ identifier: "demo_user", password: "SecureP@ss123" }),
});

const me = await api<{ user: { id: string; handle: string } }>("/auth/me", {
  token: tokens.tokens.access_token,
});
```

Field details: [Authentication](authentication.md)

---

## 3. Sign up with captcha

When the captcha secret is enabled, `zcaptcha_token` is required.

```ts
const challenge = await api<{
  algorithm: string;
  challenge: string;
  salt: string;
  signature: string;
  maxnumber: number;
}>("/captcha/challenge", { method: "POST" });

// Solve the PoW → base64 JSON token (see the Captcha page for the protocol)
const zcaptcha_token = await solvePowInWorker(challenge);

await api("/auth/register", {
  method: "POST",
  body: JSON.stringify({
    email: "new@example.com",
    password: "SecureP@ss123",
    password_confirm: "SecureP@ss123",
    handle: "newcreator",
    zcaptcha_token,
  }),
});
```

`solvePowInWorker` is your own Web Worker solver. Full contract: [Captcha](captcha.md)

---

## 4. Read public feeds

```bash
curl -sS "$API/feeds/hype?page=1&per_page=20"
curl -sS "$API/feeds?category=swipe&page=1&per_page=12&sort=hot"
curl -sS "$API/feed?limit=20"   # Community timeline (cursor: before)
```

```ts
const feed = await api<{ items: unknown[]; pagination: unknown }>(
  "/feeds/hype?page=1&per_page=8",
);
```

Note: media `/feeds` routes use a fixed server sort and ignore `sort`, and the list is returned in `data.feeds` (with `data.pagination`). Details: [Feeds](feeds.md)

---

## 5. Create content and upload

### Upload (multipart)

```bash
curl -sS -X POST "$API/uploads" \
  -H "Authorization: Bearer $ACCESS" \
  -F "file=@./clip.mp4"
```

```ts
const fd = new FormData();
fd.append("file", fileBlob, "clip.mp4");
const uploaded = await api<{ url: string; mime: string; size: number }>(
  "/uploads",
  { method: "POST", body: fd, token: access },
);
```

Note: the upload response wraps the file metadata in `data.upload`, so read the URL from the `upload` object (see [Media](media.md)).

### Create content (Bearer or API key)

```bash
curl -sS -X POST "$API/contents" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{"category":"hype","type":"video","title":"My first work","media_url":"'"$URL"'"}'
```

Note: `type` must match the category. For `hype`, use one of `interactive_longform`, `horizontal_media`, or `photo_media`; otherwise the API returns `422` `VALIDATION_ERROR`.

Details: [Contents](contents.md) · [Media](media.md)

---

## 6. Likes, bookmarks, follows

```ts
await api(`/contents/${id}/like`, { method: "POST", token: access });
await api(`/contents/${id}/bookmark`, { method: "POST", token: access });

// Toggle following a creator (by handle)
const follow = await api<{ is_following: boolean; follower_count: number }>(
  `/creators/${handle}/follow`,
  { method: "POST", token: access },
);
```

Social overview: [Social](social.md)

---

## 7. Comments, notifications, DMs

```ts
await api(`/contents/${id}/comments`, {
  method: "POST",
  token: access,
  body: JSON.stringify({ body: "Great work!" }),
});

const notifs = await api<{ notifications: unknown[] }>("/notifications", {
  token: access,
});

const dm = await api<{ conversation: { id: string } }>("/dm/conversations", {
  method: "POST",
  token: access,
  body: JSON.stringify({ handle: "friend_handle" }),
});
```

---

## 8. Game Cloud (online games)

After creating a `projectId` in Studio → Game Cloud:

```ts
const PROJECT = "YOUR_PROJECT_UUID";

// Wallet
const wallet = await api<{ POINT: number; CASH_KRW: number }>(
  `/cloud/economy/balance?projectId=${PROJECT}`,
  { token: access },
);

// Variable (high score)
await api("/cloud/vars/mutate", {
  method: "POST",
  token: access,
  body: JSON.stringify({
    projectId: PROJECT,
    scope: "user",
    key: "high_score",
    op: "max",
    num: 9999,
  }),
});

// Save
await api("/cloud/saves/save", {
  method: "POST",
  token: access,
  body: JSON.stringify({
    projectId: PROJECT,
    slot: "default",
    data: { level: 3, inventory: ["sword"] },
  }),
});
```

Details: [Game Cloud](game-cloud.md)

---

## 9. Error handling pattern

```ts
try {
  await api("/auth/login", {
    method: "POST",
    body: JSON.stringify({ identifier, password }),
  });
} catch (e) {
  const code = (e as Error & { code?: string }).code;
  if (code === "CAPTCHA_FAILED") {
    // Fetch a new challenge and retry
  } else if (code === "UNAUTHORIZED") {
    // Refresh the token or log in again
  } else if (code === "RATE_LIMITED") {
    // Wait until X-RateLimit-Reset
  }
  throw e;
}
```

Code table: [Errors](errors.md) · Limits and retries: [Rate limits](rate-limits.md)

---

## Next steps

| Page | Use |
|------|-----|
| [Getting Started](getting-started.md) | Start here |
| [Captcha](captcha.md) | PoW details |
| [Authentication](authentication.md) | Sessions and API keys |
| [Changelog](changelog.md) | What changed and when |
