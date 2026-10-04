---
title: Authentication
description: Sign-up, login, sessions, captcha, and developer API keys for the ZUKU API.
section: API
---

# Authentication

This page covers the contracts for account sign-up, login, sessions, captcha, and developer API keys.

**Base URL**

| Environment | Base URL |
|-------------|----------|
| Production | `https://zuzunza.com/api/v1` |
| Local | `http://localhost:3001/api/v1` |

## Contents

1. [Authentication model](#1-authentication-model)
2. [Response envelope](#2-response-envelope)
3. [Endpoints](#3-endpoints)
4. [Captcha](#4-captcha)
5. [Register / Signup](#5-register--signup)
6. [Login](#6-login)
7. [Logout / Refresh](#7-logout--refresh)
8. [Me (profile)](#8-me-profile)
9. [Sessions](#9-sessions)
10. [OAuth](#10-oauth)
11. [Developer API keys](#11-developer-api-keys)
12. [curl and JS/TS examples](#12-curl-and-jsts-examples)
13. [Error code summary](#13-error-code-summary)
14. [Shared browser login](#shared-browser-login)

---

## 1. Authentication model

The ZUKU API accepts two kinds of credentials.

| Method | Header | Use |
|--------|--------|-----|
| **Bearer session** | `Authorization: Bearer <access_token>` | A login session. Required by most write APIs and by profile, session, and developer key management. |
| **X-API-Key** | `X-API-Key: sk_live_…` | A key issued from the developer portal. The `sk_live_` prefix is required. When no Bearer token is present, some server-to-server routes (for example, content creation) use it to identify the caller. |

Summary of rules:

- Session tokens are `tokens.access_token` and `tokens.refresh_token` from the `POST /auth/login` or `POST /auth/register` response.
- `token_type` is always `"Bearer"`.
- The raw developer key (`key`) is returned **only once, right after it is issued**. Afterwards, `GET /developer/keys` returns metadata only.
- Most routes in these docs, including social, notifications, DMs, and session management, accept **Bearer sessions only**.

---

## 2. Response envelope

Success:

```json
{
  "success": true,
  "data": { },
  "meta": {
    "request_id": "…",
    "timestamp": "2026-08-22T04:00:00Z",
    "version": "v1"
  }
}
```

Failure:

```json
{
  "success": false,
  "error": {
    "code": "UNAUTHORIZED",
    "message": "…",
    "details": [{ "field": "password", "message": "…" }]
  },
  "meta": { "request_id": "…", "timestamp": "…", "version": "v1" }
}
```

`details` is included only for cases such as validation errors (`VALIDATION_ERROR`).
Some successful responses are `204 No Content` with no body (logout, session revocation, API key deletion).

---

## 3. Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `POST` | `/auth/register` | None† | Sign up |
| `POST` | `/auth/signup` | None† | Same handler as `/auth/register` (alias) |
| `POST` | `/auth/login` | None† | Log in and issue a session |
| `POST` | `/auth/logout` | Bearer | Revoke the current access session → `204` |
| `POST` | `/auth/refresh` | None (token in body) | Rotate the access token |
| `GET` | `/auth/me` | Bearer | Current user |
| `PATCH` | `/auth/me` | Bearer | Partially update the profile |
| `GET` | `/auth/sessions` | Bearer | List active sessions |
| `DELETE` | `/auth/sessions/{id}` | Bearer | Revoke one session → `204` |
| `POST` | `/auth/oauth/{provider}` | — | **501** `NOT_IMPLEMENTED` |
| `POST` | `/captcha/challenge` | None | Issue a proof-of-work challenge |
| `POST` | `/captcha/verify` | None | Verify a token (server use and debugging) |
| `POST` | `/developer/keys` | Bearer | Issue an API key → `201` |
| `GET` | `/developer/keys` | Bearer | List your keys |
| `DELETE` | `/developer/keys/{id}` | Bearer | Revoke a key → `204` |

† In environments where `CAPTCHA_HMAC_SECRET` is set, the register and login bodies must include a valid `zcaptcha_token`.

---

## 4. Captcha

The captcha protocol, environment variables, and solving flow are described in detail in [Captcha](captcha.md).

### `POST /captcha/challenge`

- **503** `CAPTCHA_NOT_CONFIGURED`: `CAPTCHA_HMAC_SECRET` is not set
- Example `data` on success:

```json
{
  "algorithm": "SHA-256",
  "challenge": "…",
  "salt": "…",
  "signature": "…",
  "maxnumber": 100000
}
```

### `POST /captcha/verify`

Request:

```json
{ "token": "<solved-token>", "dev_host": "localhost" }
```

- **503** `CAPTCHA_NOT_CONFIGURED`
- **403** `CAPTCHA_FAILED`: invalid token
- Success: `{ "success": true }` (inside the envelope's `data`)

### Register / login gate (`zcaptcha_token`)

| Server configuration | Behavior |
|----------------------|----------|
| `CAPTCHA_HMAC_SECRET` **not set** | Gate disabled (passes). Sign-up and login are not blocked. |
| `CAPTCHA_HMAC_SECRET` **set** | `zcaptcha_token` is required in the body. On failure, **403** `CAPTCHA_FAILED`. |
| `CAPTCHA_DEV_BYPASS=1` + allowed token/host | Development bypass is possible |

---

## 5. Register / Signup

`POST /auth/register` ≡ `POST /auth/signup`

### Request body

| Field | Required | Rule |
|-------|----------|------|
| `email` | Yes | Must contain `@` |
| `password` | Yes | **At least 8 characters** |
| `password_confirm` | Yes | Must match `password` |
| `handle` | Yes | Must not be empty |
| `display_name` | Optional | Defaults to the handle |
| `zcaptcha_token` | Conditional | Required when the captcha secret is set |

### Success `201`

`data.user` + `data.tokens` (`access_token`, `refresh_token`, `token_type`, `expires_in`)

### Common errors

| HTTP | code | Situation |
|------|------|-----------|
| 409 | `ALREADY_AUTHENTICATED` | Sign-up attempted while already logged in with a valid Bearer token |
| 409 | `EMAIL_EXISTS` | Email already in use |
| 409 | `LEGACY_ACCOUNT_EXISTS` | An existing ZUKU account already has this email/handle → **direct the user to log in** |
| 409 | `HANDLE_EXISTS` | Handle already in use (or a database duplicate) |
| 422 | `VALIDATION_ERROR` | Password, email, or handle validation failed |
| 403 | `CAPTCHA_FAILED` | Captcha gate failed |

---

## 6. Login

`POST /auth/login`

### Request body

| Field | Required | Description |
|-------|----------|-------------|
| `identifier` or `email` | Yes (one of them) | `identifier` takes precedence. Accepts an email, username, or nickname. |
| `password` | Yes | |
| `device_id` | Optional | Session metadata |
| `zcaptcha_token` | Conditional | When the captcha secret is set |

The server first tries a current ZUKU account, then falls back to linking a legacy account. When a legacy login succeeds, the account is linked to a current ZUKU account and the password is re-hashed.

### Success `200`

`data.user` + `data.tokens`

### Common errors

| HTTP | code |
|------|------|
| 401 | `INVALID_CREDENTIALS` |
| 403 | `ACCOUNT_SUSPENDED` |
| 403 | `CAPTCHA_FAILED` |

---

## 7. Logout / Refresh

### `POST /auth/logout`

- Header: `Authorization: Bearer <access_token>`
- Success: **204** (no body)
- Missing or malformed header: **401** `UNAUTHORIZED`

### `POST /auth/refresh`

```json
{ "refresh_token": "…" }
```

- Success: `data.tokens` (a new `access_token`; the existing `refresh_token` is kept; `expires_in` ≈ 7 days)
- Failure: **401** `INVALID_REFRESH_TOKEN`

---

## 8. Me (profile)

### `GET /auth/me`

Bearer required. Returns `data.user`.

Example public user fields: `id` (`usr_…`), `email`, `display_name`, `handle`, `role`, `avatar_url`, `is_verified`, `created_at`, `profile_completion_status`, `bio`, `website_url`, `location`, `cover_url`, `banner_tone`

### `PATCH /auth/me`

Only the fields you send are updated. Allowed fields: `display_name`, `bio`, `website_url`, `location`, `banner_tone`, `cover_url`, `avatar_url`
`banner_tone` must be one of `cyan` | `swipe` | `jump` | `slate`.

---

## 9. Sessions

Instead of forcing a full logout when the same account signs in elsewhere, users can end only the sessions they don't recognize.

### `GET /auth/sessions`

`data.sessions[]`: `id`, `device_label`, `created_at`, `last_seen_at`, `is_current`
**Raw tokens are never returned.**

### `DELETE /auth/sessions/{id}`

- `{id}` is the numeric session id
- You can only revoke your own sessions. Missing or belonging to someone else → **404**
- Success: **204**

---

## 10. OAuth

`POST /auth/oauth/{provider}`

Always returns **501 Not Implemented** with code `NOT_IMPLEMENTED`.
OAuth providers are currently out of scope.

---

## 11. Developer API keys

All routes require **Bearer**.

### `POST /developer/keys`

```json
{ "name": "CI bot" }
```

- `name`: 1–50 characters
- **201**: `data.api_key` (metadata) + `data.key` (plaintext, **returned only once**)

### `GET /developer/keys`

`data.api_keys` array

### `DELETE /developer/keys/{id}`

Success: **204**. Missing or belonging to someone else → **404** `API_KEY_NOT_FOUND`

Issued keys can be used as `X-API-Key: sk_live_…` in place of Bearer on some APIs.

---

## 12. curl and JS/TS examples

These examples use the local base URL. For production, replace it with `https://zuzunza.com/api/v1`.

### Register

```bash
curl -sS -X POST "http://localhost:3001/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "demo@example.com",
    "password": "password1",
    "password_confirm": "password1",
    "handle": "demo_user",
    "zcaptcha_token": "OPTIONAL_WHEN_CAPTCHA_SET"
  }'
```

```ts
const base = "http://localhost:3001/api/v1";

const registerRes = await fetch(`${base}/auth/register`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    email: "demo@example.com",
    password: "password1",
    password_confirm: "password1",
    handle: "demo_user",
    // When CAPTCHA_HMAC_SECRET is set:
    // zcaptcha_token: solvedToken,
  }),
});
const registerJson = await registerRes.json();
const { access_token, refresh_token } = registerJson.data.tokens;
```

### Login

```bash
curl -sS -X POST "http://localhost:3001/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "identifier": "demo@example.com",
    "password": "password1"
  }'
```

```ts
const loginRes = await fetch(`${base}/auth/login`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    identifier: "demo@example.com",
    password: "password1",
  }),
});
const loginJson = await loginRes.json();
const accessToken = loginJson.data.tokens.access_token;
const refreshToken = loginJson.data.tokens.refresh_token;
```

### Refresh

```bash
curl -sS -X POST "http://localhost:3001/api/v1/auth/refresh" \
  -H "Content-Type: application/json" \
  -d "{\"refresh_token\":\"$REFRESH\"}"
```

```ts
const refreshRes = await fetch(`${base}/auth/refresh`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ refresh_token: refreshToken }),
});
const refreshed = await refreshRes.json();
const newAccess = refreshed.data.tokens.access_token;
```

### Me

```bash
curl -sS "http://localhost:3001/api/v1/auth/me" \
  -H "Authorization: Bearer $ACCESS"
```

```ts
const meRes = await fetch(`${base}/auth/me`, {
  headers: { Authorization: `Bearer ${accessToken}` },
});
const me = await meRes.json();
console.log(me.data.user.handle);
```

### Create an API key

```bash
curl -sS -X POST "http://localhost:3001/api/v1/developer/keys" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{"name":"my-integration"}'
```

```ts
const keyRes = await fetch(`${base}/developer/keys`, {
  method: "POST",
  headers: {
    Authorization: `Bearer ${accessToken}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({ name: "my-integration" }),
});
const keyJson = await keyRes.json();
// Store the plaintext key from this response; it is never shown again
const rawKey = keyJson.data.key;
```

---

## 13. Error code summary

| code | Typical HTTP | Meaning |
|------|--------------|---------|
| `ALREADY_AUTHENTICATED` | 409 | Sign-up while logged in |
| `EMAIL_EXISTS` | 409 | Email already in use |
| `LEGACY_ACCOUNT_EXISTS` | 409 | Legacy account exists → log in |
| `HANDLE_EXISTS` | 409 | Handle already in use |
| `VALIDATION_ERROR` | 422 | Field validation |
| `INVALID_CREDENTIALS` | 401 | Login failed |
| `ACCOUNT_SUSPENDED` | 403 | Suspended account |
| `UNAUTHORIZED` | 401 | Missing or invalid Bearer token |
| `INVALID_REFRESH_TOKEN` | 401 | Invalid refresh token |
| `CAPTCHA_NOT_CONFIGURED` | 503 | No captcha secret (challenge/verify) |
| `CAPTCHA_FAILED` | 403 | Captcha failed |
| `NOT_IMPLEMENTED` | 501 | OAuth |
| `API_KEY_NOT_FOUND` | 404 | Key to delete not found |
| `NOT_FOUND` | 404 | Sessions and similar |

See [Errors](errors.md) for the full list and [Rate limits](rate-limits.md) for request limits.

---

## Shared browser login

ZUKU's official domains share an HttpOnly session cookie. Set `credentials: 'include'` on regular browser API requests. When a valid shared cookie is present, the cookie's account takes precedence over a long-stored Bearer token. Server clients without cookies can keep using the existing Bearer contract.

```ts
const response = await fetch('https://zuzunza.com/api/v1/auth/me', {
  credentials: 'include',
  headers: { Accept: 'application/json' },
});
const { data } = await response.json();
// data.user: the user of the current shared session
```

A successful `GET /auth/me` extends the same browser session's expiry to 7 days. The cookie is HttpOnly and is never read by docs pages or game code. Existing cookies are migrated to a new browser session during a normal session check.

### POST `/api/v1/auth/session`

Use this when the user **explicitly selects** a different saved account. The selected account's `Authorization: Bearer <access_token>` is required, and no body is needed. Success is `200` with `data.user`, and the shared browser cookie switches to the selected account. Sending only the cookie returns `401`.

```ts
await fetch('https://zuzunza.com/api/v1/auth/session', {
  method: 'POST',
  credentials: 'include',
  headers: { Authorization: `Bearer ${selectedAccountAccessToken}` },
});
```

`POST /auth/refresh` keeps the existing `{ refresh_token }` → `data.tokens` contract and keeps the same browser session. `POST /auth/logout` ends the shared session and clears the cookie. Repeated logouts also return `204`. Browser session credentials themselves are never included in response JSON.
