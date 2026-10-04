---
title: Errors
description: The ZUKU API response envelope, HTTP status codes, error codes, rate-limit headers, and CLI troubleshooting.
section: API
---

# Errors

Every JSON response from the ZUKU API uses one shared envelope. Failures carry a stable `code`, a human-readable `message`, and, for field validation, a `details` array. Clients can map these to an `ApiFailure(code, message, status)` pattern.

## Response envelope

### Success

```json
{
  "success": true,
  "data": { },
  "meta": {
    "request_id": "…",
    "timestamp": "2026-08-22T00:00:00Z",
    "version": "v1"
  }
}
```

- `data`: the endpoint-specific payload.
- `meta.version`: currently always `"v1"`. It's the same API generation as the `/api/v1` URL prefix and the `X-API-Version` header.

### Failure

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Please check your input",
    "details": [
      { "field": "title", "message": "Title must be 1–100 characters" }
    ]
  },
  "meta": {
    "request_id": "…",
    "timestamp": "…",
    "version": "v1"
  }
}
```

- `details` is included only when there is field-level validation.
- Simple failures contain only `code` and `message`.

### Exceptions

| Situation | Body |
|---|---|
| `204 No Content` | Empty body (comment deletion, some archive APIs) |
| Successful Jump `stream` / `swf` | May be **binary**, not JSON |
| CORS preflight | `204` |

## HTTP status codes

| HTTP | Typical situation |
|---|---|
| `200 OK` | Successful read, update or toggle |
| `201 Created` | Created (content, upload, sign-up, post, and so on) |
| `204 No Content` | Success without a body / OPTIONS |
| `308 Permanent Redirect` | Legacy Jump path redirected to the canonical API |
| `400 Bad Request` | Malformed JSON or multipart (`BAD_REQUEST`) |
| `401 Unauthorized` | Missing or invalid session/token (`UNAUTHORIZED`) |
| `403 Forbidden` | Insufficient permission (`FORBIDDEN`) |
| `404 Not Found` | Resource or route not found (code varies by resource) |
| `409 Conflict` | Duplicate or state conflict (`EMAIL_EXISTS`, `HANDLE_EXISTS`, `ALREADY_AUTHENTICATED`, `LEGACY_ACCOUNT_EXISTS`, `SELF_ACTION_FORBIDDEN`, and others) |
| `413 Payload Too Large` | Upload limit exceeded (`PAYLOAD_TOO_LARGE`) |
| `415 Unsupported Media Type` | Magic bytes not supported (`UNSUPPORTED_MEDIA_TYPE`) |
| `422 Unprocessable Entity` | Field validation (`VALIDATION_ERROR`, Jump ID validation codes, and others) |
| `429 Too Many Requests` | Rate limit exceeded (`RATE_LIMITED`) |
| `500 Internal Server Error` | Server or database (`INTERNAL_ERROR`, `DB_UNAVAILABLE`) |
| `501 Not Implemented` | Out of scope (`NOT_IMPLEMENTED`, for example OAuth) |
| `503 Service Unavailable` | Captcha not configured (`CAPTCHA_NOT_CONFIGURED`), rate-limit counter unavailable (`RATE_LIMIT_UNAVAILABLE`) |

## Error codes

These are the codes the API actually returns. Delegated moderation and analytics modules may return the same codes.

### Authentication and permissions

| code | Typical HTTP | Meaning |
|---|---|---|
| `UNAUTHORIZED` | 401 | A Bearer session/Authorization header or a valid access token is required |
| `FORBIDDEN` | 403 | No permission, or admin only |
| `ALREADY_AUTHENTICATED` | 409 | Tried to sign up while already signed in |
| `SELF_ACTION_FORBIDDEN` | 409 | Forbidden administrative action on yourself |

### Validation and request format

| code | Typical HTTP | Meaning |
|---|---|---|
| `BAD_REQUEST` | 400 | Malformed request body or multipart |
| `VALIDATION_ERROR` | 422 | Field validation failed (comes with `details[]`) |
| `INVALID_CONTENT_ID` | 422 | Jump play ID breaks the character or length rules |
| `CONTENT_ID_MISMATCH` | 422 | Jump path ID differs from the body `content_id` |

### Sign-up and accounts

| code | Typical HTTP | Meaning |
|---|---|---|
| `EMAIL_EXISTS` | 409 | Email already in use |
| `HANDLE_EXISTS` | 409 | Handle already in use |
| `LEGACY_ACCOUNT_EXISTS` | 409 | Conflicts with an existing ZUKU account; sign in with that account instead |

### Captcha

| code | Typical HTTP | Meaning |
|---|---|---|
| `CAPTCHA_FAILED` | (verification failure) | Proof-of-work/captcha failed |
| `CAPTCHA_NOT_CONFIGURED` | 503 | Captcha secret isn't configured; fails closed |

### Not found

| code | Typical HTTP | Target |
|---|---|---|
| `NOT_FOUND` | 404 | General (session, captcha path, uploaded file, and so on) |
| `CONTENT_NOT_FOUND` | 404 | Content |
| `COMMENT_NOT_FOUND` | 404 | Comment |
| `POST_NOT_FOUND` | 404 | Community post |
| `CONVERSATION_NOT_FOUND` | 404 | DM conversation |
| `USER_NOT_FOUND` | 404 | User |
| `NOTIFICATION_NOT_FOUND` | 404 | Notification |
| `API_KEY_NOT_FOUND` | 404 | Developer API key |
| `ROUTE_NOT_FOUND` | 404 | No matching API route |

### Media and Jump

| code | Typical HTTP | Meaning |
|---|---|---|
| `UNSUPPORTED_MEDIA_TYPE` | 415 | Unsupported upload format |
| `PAYLOAD_TOO_LARGE` | 413 | Upload size limit exceeded |
| `SOURCE_UNAVAILABLE` | (playback failure) | No playable source |
| `SWF_PARSE_FAILED` | (playback failure) | SWF parsing, IR encoding or unsupported format |

### Rate limits

| code | Typical HTTP | Meaning |
|---|---|---|
| `RATE_LIMITED` | 429 | Request limit exceeded; see the headers below |
| `RATE_LIMIT_UNAVAILABLE` | 503 | The rate-limit counter couldn't be checked |

### Infrastructure and other

| code | Typical HTTP | Meaning |
|---|---|---|
| `DB_UNAVAILABLE` | 500 | Database pool or connection unavailable |
| `INTERNAL_ERROR` | 500 | Internal processing failure |
| `NOT_IMPLEMENTED` | 501 | Not implemented (for example, OAuth provider) |

> A client-side `ApiFailure` helper may produce `INVALID_RESPONSE` when the envelope can't be parsed, and `HTTP_ERROR` for an error with an empty body. These are generated by the **client**, not returned by the server.

## Field errors in `details[]`

For `VALIDATION_ERROR` and similar codes:

```json
"details": [
  { "field": "title", "message": "Title must be 1–100 characters" },
  { "field": "tags", "message": "Up to 10 tags are allowed" }
]
```

Common `field` values when creating content are `title`, `description`, `tags`, `age_rating` and `type`. Map `details` to inline field errors. When it's missing, show `error.message` as a toast or banner.

## Response headers

Rate-limited requests carry headers based on actual measured counts. Success responses describe the default window for that request kind. A `429` describes the window of the condition that actually rejected the request.

| Header | Current behavior |
|---|---|
| `X-API-Version` | Always `v1` |
| `X-RateLimit-Limit` | Allowed requests in the reported window |
| `X-RateLimit-Remaining` | Requests left after this one |
| `X-RateLimit-Reset` | End of the window, in Unix epoch seconds |
| `X-RateLimit-Window` | Window length in seconds |
| `X-RateLimit-Scope` / `X-RateLimit-Plan` | Request kind and the server-verified plan (`unknown` for IP protection before authentication) |
| `Retry-After` | Seconds to wait, on `429` |

For `429 RATE_LIMITED`, `error.details` includes `plan`, `scope`, `limit`, `remaining`, `window_seconds`, `retry_after_seconds`, `reset_at` and `upgrade_available`. `reset_at` is in Unix epoch seconds. If the counter can't be confirmed, the API returns `503 RATE_LIMIT_UNAVAILABLE`. Existing MFA, chat and provider limits keep their own error codes and retry guidance.

See [Rate limits](rate-limits.md) for the limits and rollout conditions. To tell the old placeholder headers from the new policy, check real responses and `GET /api/v1/rate-limits/policy`.

Other CORS and API version headers keep their existing contract. Personal limits and `429` responses aren't stored in shared caches.

## Handling errors in JavaScript

```ts
class ApiFailure extends Error {
  constructor(
    public code: string,
    message: string,
    public status: number,
    public details?: { field: string; message: string }[],
  ) {
    super(message);
    this.name = 'ApiFailure';
  }
}

async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`/api/v1${path}`, {
    ...init,
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers ?? {}),
    },
  });

  if (res.status === 204) return undefined as T;

  const envelope = await res.json();
  if (!envelope.success) {
    throw new ApiFailure(
      envelope.error.code,
      envelope.error.message,
      res.status,
      envelope.error.details,
    );
  }
  return envelope.data as T;
}

// Example
try {
  await apiFetch('/contents', { method: 'POST', body: JSON.stringify(payload), headers: {
    Authorization: `Bearer ${token}`,
  }});
} catch (e) {
  if (e instanceof ApiFailure) {
    switch (e.code) {
      case 'UNAUTHORIZED':
        // Prompt the user to sign in
        break;
      case 'VALIDATION_ERROR':
        // Highlight form fields using e.details
        break;
      case 'EMAIL_EXISTS':
      case 'HANDLE_EXISTS':
        // Sign-up form specific message
        break;
      case 'CAPTCHA_FAILED':
        // Retry the captcha
        break;
      case 'DB_UNAVAILABLE':
      case 'INTERNAL_ERROR':
        // Retry later
        break;
      default:
        console.error(e.code, e.message, e.status);
    }
  }
}
```

## CLI troubleshooting

The `zuku` CLI reports failures as `CODE: message` on stderr, or as `{"success":false,"error":{...}}` with `--json`. It reports server failures with the HTTP status and a verified API code, and never prints raw remote responses or tokens.

| Code | What to do |
|---|---|
| `INVALID_INPUT` (exit 2) | An argument is unknown, duplicated, conflicting or malformed. Check [Commands](cli/commands.md). |
| `UNAUTHORIZED`, `ZUKU_LOGIN_REQUIRED` | Connect your account with `zuku login zuku`. |
| `ZUKU_ACCOUNT_MIGRATION_REQUIRED` | The connection is from the earlier test server. Run `zuku login zuku` again. |
| `ZUKU_GENERATE_SCOPE_REQUIRED` | Approve generation explicitly with `zuku login zuku --generate`. |
| `DEPLOY_YOLO_REQUIRED` | Production publishing needs `--yolo`. |
| `DEPLOY_QUOTA_EXCEEDED` | You've used 3 successful publishes in the last 6 hours. Wait for `retry_after`. |
| `DEPLOY_OUTCOME_UNKNOWN`, `AGENT_PUBLISH_OUTCOME_UNKNOWN` | The result couldn't be confirmed, so the CLI didn't retry automatically. Check the receipt, then recover. See [Publishing](cli/publishing.md). |
| `AGENT_PLAYTEST_SANDBOX` | The browser sandbox couldn't start (for example, when you run as root). Run as a regular user. |
| `AGENT_PLAYTEST_FAILED` | The game failed the real browser playtest. Nothing was packaged, uploaded or published. |
| `AGENT_REQUEST_OUT_OF_SCOPE` | The agent only handles ZUKU/ZukuJS game development. See [Game agent](cli/agent.md). |
| `COMMAND_CANCELLED` (exit 130) | You cancelled with Ctrl+C. |

Don't assume every `422` has the same cause. For paid or publishing actions with an unknown outcome, check the state before you run the command again.

## Related pages

- [Contents](contents.md)
- [Media](media.md)
- [Rate limits](rate-limits.md)
- [Changelog](changelog.md): `meta.version` and `X-API-Version`
