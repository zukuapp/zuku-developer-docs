---
title: Rate limits
description: Per-plan request limits, request kinds, rate-limit headers, 429 responses, and the CLI publish limit for the ZUKU API.
section: API
---

# Rate limits

> Policy version: 2026-10-01 · API v1

## Default limits per plan

Each number is the requests allowed in 60 seconds. Signed-in users are counted per account, so opening more tabs, devices or API keys doesn't raise the limit. Guests are counted by IP.

| Plan | Read `read` | Write `write` | Platform pages `platform` | Upload/publish `upload` | AI start `ai` | Cloud `cloud` |
|---|---:|---:|---:|---:|---:|---:|
| Guest `guest` | 240 | 30 | 120 | 3 | 2 | 180 |
| Free `free` | 600 | 120 | 240 | 12 | 6 | 600 |
| Super ZUKU `super_zuku` | 1,200 | 240 | 360 | 24 | 12 | 1,200 |
| Creator `creator` | 1,800 | 360 | 480 | 60 | 20 | 1,800 |
| Cloud Pro `cloud_pro` | 3,000 | 600 | 720 | 120 | 30 | 2,400 |
| Cloud Scale `cloud_scale` | 6,000 | 1,200 | 1,200 | 240 | 60 | 12,000 |
| Game Dedicated `cloud_dedicated` | 12,000 | 2,400 | 1,800 | 480 | 120 | 30,000 |

The server normalizes `game_dedicated` to `cloud_dedicated`. The numbers are call-rate limits only; the guest `upload` and `ai` values don't grant upload or paid-feature access. Sign-in, permissions, balance and publishing conditions are checked separately by each API.

The game Cloud bridge is limited to 6 requests per second and 3 concurrent requests.

## Request kinds and additional rules

| Kind | Examples |
|---|---|
| `read` | General GET/HEAD, content and comment reads, AI/conversion job status checks |
| `write` | General changes other than likes, comments and account actions; editing and saving |
| `platform` | ZUKU page navigation |
| `upload` | File uploads, content creation and publishing, starting imports, builds and conversions |
| `ai` | Starting AI runs and chats, translation requests |
| `cloud` | Cloud project APIs, game runtime requests |
| `auth` | Sign-in, sign-up, captcha, passkeys and other authentication paths |

Regular API routes use the limit for their kind. AI status checks don't use up AI start quota.

Read, page, write, upload and AI requests also have a fixed 10-second window. By default it's one third of the per-minute limit, rounded up, with minimums of 20 for read and page, 3 for write, and 1 for upload and AI. Cloud has no 10-second window. Authentication is limited to 20 per 10 seconds regardless of plan.

Authentication is 30 per minute per signed-in account on every plan, including paid plans. Guest authentication is 120 per minute per IP. Existing failed-login, MFA lockout and one-time verification rules take precedence when they're stricter.

Sensitive authentication requests are also limited per target. If a sign-in email and handle point to the same account, they share one target limit. These rules apply regardless of plan.

| Authentication target | Allowed | Window |
|---|---:|---:|
| Sign-in target | 10 | 10 minutes |
| Sign-up target | 5 | 15 minutes |
| Username lookup / password recovery request target | 5 | 15 minutes |
| Password reset proof verification | 10 | 5 minutes |

Authentication bodies over 16 KiB are rejected before processing. Regular `/auth/me` and session list reads count as `read`, and profile edits count as `write`, so they don't use authentication attempts.

Signed-in accounts also get a separate protection limit on the total traffic from a shared IP.

| Per-IP aggregate protection | Requests/minute |
|---|---:|
| Read | 20,000 |
| Write | 5,000 |
| Pages | 6,000 |
| Upload/publish | 1,200 |
| AI start | 600 |
| Cloud | 60,000 |
| Authentication | 600 |
| Total across all kinds | 90,000 |

Guests on a shared network share one IP limit. Once signed in, a user gets the per-account limits, and the per-IP protection still applies. Changing plans doesn't lift the per-IP protection or the 10-second windows.

Use a user key issued from [`/developer/keys`](authentication.md#11-developer-api-keys) as the public API `X-API-Key`. Each key also has a default limit of 600 per minute. Multiple keys share their owner account's limits.

Monthly Cloud usage, free allowances, QoS, spending caps and AI provider limits are separate from these rate limits. A request can pass the rate limit and still be rejected for usage or cost reasons.

## Responses and retries

Rate-limited requests carry the following headers. Success responses describe the default 60-second window for that kind. A `429` describes the window of the condition that rejected the request.

| Header | Meaning |
|---|---|
| `X-RateLimit-Limit` | Allowed requests in the reported window |
| `X-RateLimit-Remaining` | Requests left after this one |
| `X-RateLimit-Reset` | End of the window, in Unix epoch seconds |
| `X-RateLimit-Window` | Window length in seconds |
| `X-RateLimit-Scope` | Request kind, or the IP/key protection that rejected the request |
| `X-RateLimit-Plan` | Server-verified plan (`unknown` for IP protection before authentication) |
| `Retry-After` | Seconds to wait before retrying, on `429` |

These headers are attached only to limited requests. Health checks, OPTIONS and static assets are excluded requests. The remaining count covers one limit only. Other limits apply separately.

```json
{
  "success": false,
  "error": {
    "code": "RATE_LIMITED",
    "message": "Too many requests at once. Please try again after the time shown.",
    "details": {
      "plan": "free",
      "scope": "read",
      "limit": 600,
      "remaining": 0,
      "window_seconds": 60,
      "retry_after_seconds": 12,
      "reset_at": 1790812860,
      "upgrade_available": true
    }
  }
}
```

Clients should follow the actual `Retry-After` first. If it's missing, use the actual reset information or the error message from the service that applied the limit. Pause polling, and spread multiple jobs through a queue. Automatically repeating POST, payment, upload or AI generation requests can create duplicate work, so check job status and any existing idempotency contract first. If the counter can't be checked, the API returns `503 RATE_LIMIT_UNAVAILABLE` with retry guidance.

## Policy endpoints

`GET /api/v1/rate-limits/policy` returns the plan table, per-IP protection, 10-second window rules and API key defaults. It doesn't require authentication and doesn't use up any counter.

## CLI publish limit

The `zuku` CLI's production publish (`zuku deploy --yolo`, or `zuku agent --yolo`) has its own server-enforced limit: 3 successful publishes per ZUKU account in a rolling 6 hours. Unsettled reservations also hold a slot. Retrying the same account, content and package SHA-256 doesn't use another slot, and failed or rejected publishes don't count. Going over returns `429 DEPLOY_QUOTA_EXCEEDED` with `Retry-After`. Drafts and uploads don't use this limit, though uploads still count toward the `upload` request kind above. Check your status with `zuku account --quota`. See [Publishing](cli/publishing.md).

Related: [Errors](errors.md) · [Authentication](authentication.md) · [Game Cloud](game-cloud.md)
