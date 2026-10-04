---
title: Developer Console API
description: Register apps, issue per-app API keys, and manage webhooks in the ZUKU Developer Console.
section: API
---

# Developer Console API

The ZUKU Developer Console API lets you register apps and manage API keys and webhooks.

This page covers the Developer Console endpoints only. The newer native AI APIs are not covered here.

## Base URL

`/api/v1/devconsole`

Every request requires `Authorization: Bearer <session_token>`.

---

## Apps

### List apps

```http
GET /api/v1/devconsole/apps
```

### Register an app

```http
POST /api/v1/devconsole/apps
Content-Type: application/json

{
  "app_name": "My Game Tool",
  "app_type": "game",
  "description": "Jump game integration tool",
  "redirect_uris": ["https://example.com/callback"],
  "scopes": ["contents:read", "jump:write"]
}
```

**app_type**: `web` · `mobile` · `server` · `cli` · `game`

### App details

```http
GET /api/v1/devconsole/apps/{app_id}
```

---

## API keys

Keys are issued per app. The raw key is returned **only once, in the creation response**.

### List keys

```http
GET /api/v1/devconsole/apps/{app_id}/keys
```

### Issue a key

```http
POST /api/v1/devconsole/apps/{app_id}/keys
Content-Type: application/json

{
  "key_name": "Production",
  "environment": "live"
}
```

### Revoke a key

```http
DELETE /api/v1/devconsole/keys/{key_id}
```

---

## Webhooks

### List webhooks

```http
GET /api/v1/devconsole/apps/{app_id}/webhooks
```

### Register a webhook

```http
POST /api/v1/devconsole/apps/{app_id}/webhooks
Content-Type: application/json

{
  "endpoint_url": "https://example.com/webhook",
  "events": ["content.published", "jump.play"]
}
```

A `secret` is issued on registration. The receiver verifies requests with the `X-Shizuku-Secret` header.

### Test a webhook

```http
POST /api/v1/devconsole/webhooks/{webhook_id}/test
```

### Delivery log

```http
GET /api/v1/devconsole/webhooks/{webhook_id}/deliveries
```

---

## UI access

- **Studio developer console**: `/studio/developer`
- **API docs**: [Docs home](README.md)

---

## Differences from legacy API keys

| | `/developer/keys` | `/devconsole/apps/.../keys` |
|--|-------------------|------------------------------|
| Scope of ownership | User | App |
| Use | Simple server-to-server (content creation) | Per-app keys and webhook management |
| Scopes | None | JSON `scopes` array |

The two systems run **side by side**. For user-level keys, see [Authentication](authentication.md#11-developer-api-keys). See also [Errors](errors.md) and [Rate limits](rate-limits.md).
