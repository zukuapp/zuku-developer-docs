---
title: Rate limits
description: Per-plan request limits, request kinds, rate-limit headers, 429 responses, and the CLI publish limit for the ZUKU API.
section: API
---

# Rate limits

> **Policy version**: 2026-10-01 · API v1
>
> This page describes the newly implemented policy. Check responses and `GET /api/v1/rate-limits/policy` to see what's active on the live service. Until the policy is rolled out to production, existing responses may stay the same.

## Default limits per plan

Each number is the **requests allowed in 60 seconds**. Signed-in users are counted per account, so opening more tabs, devices or API keys doesn't raise the limit. Guests are counted by IP, as verified through the trusted proxy path.

| Plan | Read `read` | Write `write` | Platform pages `platform` | Upload/publish `upload` | AI start `ai` | Cloud `cloud` |
|---|---:|---:|---:|---:|---:|---:|
| Guest `guest` | 240 | 30 | 120 | 3 | 2 | 180 |
| Free `free` | 600 | 120 | 240 | 12 | 6 | 600 |
| Super ZUKU `super_zuku` | 1,200 | 240 | 360 | 24 | 12 | 1,200 |
| Creator `creator` | 1,800 | 360 | 480 | 60 | 20 | 1,800 |
| Cloud Pro `cloud_pro` | 3,000 | 600 | 720 | 120 | 30 | 2,400 |
| Cloud Scale `cloud_scale` | 6,000 | 1,200 | 1,200 | 240 | 60 | 12,000 |
| Game Dedicated `cloud_dedicated` | 12,000 | 2,400 | 1,800 | 480 | 120 | 30,000 |

The server normalizes `game_dedicated` to `cloud_dedicated`. These limits only control request rate. They don't let guests upload or grant access to paid features. Sign-in, permissions, balance and publishing conditions are still checked separately by each API.

The defaults reflect real client behavior. Aist job polling runs about every 1.2 seconds (up to about 50 per minute), media conversion polling every 4 seconds (15 per minute), and DM background checks every 30 seconds (2 per minute). The Free read limit of 600 leaves room for several jobs plus normal browsing. The game Cloud bridge has its own limit of 6 requests per second and 3 concurrent requests, so Cloud gets no extra 10-second window. These values are an initial policy derived from polling intervals in the code. They aren't measured production load or a throughput guarantee.

## Request kinds and additional rules

| Kind | Examples |
|---|---|
| `read` | General GET/HEAD, content and comment reads, AI/conversion job status checks |
| `write` | General changes other than likes, comments and account actions; editing and saving |
| `platform` | ZUKU page navigation, entry checks for APIs implemented by the web server |
| `upload` | File uploads, content creation and publishing, starting imports, builds and conversions |
| `ai` | Starting AI runs and chats, translation requests |
| `cloud` | Cloud project APIs, game runtime requests |
| `auth` | Sign-in, sign-up, captcha, passkeys and other authentication paths |

Regular API routes use the limit for their kind. APIs handled directly by the web server check both `platform` and their own kind. AI status checks don't use up AI start quota. A rejected request never cancels or duplicates a job that has already started, and the client keeps your edits.

Read, page, write, upload and AI requests also have a **fixed 10-second window**. By default it's one third of the per-minute limit, rounded up, with minimums of 20 for read and page, 3 for write, and 1 for upload and AI. Cloud has no 10-second window. Authentication is limited to 20 per 10 seconds regardless of plan. Requests from adjacent fixed windows can land close together at a window boundary, so don't read the per-minute numbers as a steady per-second throughput.

Authentication is **30 per minute** per signed-in account on every plan, including paid plans. Guest authentication is **120 per minute** per IP. Existing failed-login, MFA lockout and one-time verification rules take precedence when they're stricter. Paying doesn't lower authentication protection.

Sensitive authentication requests are also limited per target after a small body check. If a sign-in email and handle point to the same local account, they share one target limit. Identifiers are hashed in the stored counter key. These rules apply regardless of plan.

| Authentication target | Allowed | Window |
|---|---:|---:|
| Sign-in target | 10 | 10 minutes |
| Sign-up target | 5 | 15 minutes |
| Username lookup / password recovery request target | 5 | 15 minutes |
| Password reset proof verification | 10 | 5 minutes |

Authentication bodies over 16 KiB are rejected before processing. Regular `/auth/me` and session list reads count as `read`, and profile edits count as `write`, so they don't use authentication attempts.

Signed-in accounts also get a separate protection limit on the total traffic from a shared IP. It's set well above the per-account limits so normal shared-network users aren't affected.

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

An `X-API-Key` authenticated by the public API also has a default limit of **600 per minute per key**. If a server administrator set `api_keys.rate_limit_per_min`, that value is used instead. Multiple keys share their owner account's limits. The developer console `dev_api_keys` setting is a separate feature and isn't used for public API authentication or for determining a paid plan.

Monthly Cloud usage, free allowances, QoS, spending caps and AI provider limits are separate from these rate limits. A request can pass the rate limit and still be rejected for usage or cost reasons.

## Responses and retries

Rate-limited requests carry the following headers, based on actual counts. Success responses describe the default 60-second window for that kind. A `429` describes **the window of the condition that actually rejected the request**.

| Header | Meaning |
|---|---|
| `X-RateLimit-Limit` | Allowed requests in the reported window |
| `X-RateLimit-Remaining` | Requests left after this one |
| `X-RateLimit-Reset` | End of the window, in Unix epoch seconds |
| `X-RateLimit-Window` | Window length in seconds |
| `X-RateLimit-Scope` | Request kind, or the IP/key protection that rejected the request |
| `X-RateLimit-Plan` | Server-verified plan (`unknown` for IP protection before authentication) |
| `Retry-After` | Seconds to wait before retrying, on `429` |

Excluded requests such as health checks, OPTIONS and static assets may not have these headers. Success responses for limited requests include personal limit headers, so they're served as `private, no-store`. The remaining count covers one limit only and doesn't guarantee that a future request will pass every check.

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

The numbers above are illustrative. Clients should follow the actual `Retry-After` first. If it's missing, use the actual reset information or the error message from the service that applied the limit. Pause polling, and spread multiple jobs through a queue. Automatically repeating POST, payment, upload or AI generation requests can create duplicate work, so check job status and any existing idempotency contract first.

On the ZUKU website, API limits show up as a notice on the current screen and your edits are kept. If page navigation itself is limited, the site returns HTTP `429` with a dedicated `/rate-limit` page. It shows the confirmed wait time, plan and request kind, and you can go back once the wait is over. For provider errors with no wait time, the site doesn't make one up. The limit page, sign-in, plans, status and public docs are excluded from page navigation limits so you can always recover.

## Policy endpoints

`GET /api/v1/rate-limits/policy` returns the plan table, per-IP protection, 10-second window rules and API key defaults. It doesn't require authentication and doesn't use up any counter.

`POST /api/v1/rate-limits/platform` is used for web entry checks. The server verifies the Cookie or Bearer token to determine the plan and never trusts a plan or user ID sent by the client. Calling it directly uses the same entry limit. APIs handled directly by the web server also pass `path` and `method` so the matching kind is checked.

## Rollout conditions

Counters are stored in PostgreSQL and incremented atomically. Workers and servers that share the same database share the limits, and counters survive process restarts. Old counters are cleaned up in bounded batches. If the counter can't be checked, the API returns `503 RATE_LIMIT_UNAVAILABLE` with retry guidance.

Client IPs are resolved only through directly connected, verified proxies. Other connections use the TCP peer address. A forwarded address chain is followed from the right through trusted hops only, so a browser-supplied address or a user-supplied IP or plan header can't change your limit.

Server-side public data fetches forward the verified client IP path, so visitors don't all share the web server's loopback limit. For signed-in public reads, the web server can pass a verified session to the backend in a separate server-to-server header so account and plan limits apply. This identifier grants no permissions, public responses stay public, and tampered, expired or revoked sessions don't get account limits. Fetches that carry it are `no-store`, so session values and personal limit metadata never enter shared caches. Shared dynamic HTML caches are bypassed so every request goes through the entry check. Static assets and thumbnail caches are unchanged.

Switching from the old placeholder headers to real limits ships together across web, backend, database migration and docs, after the policy, timing and retry contract have been announced.

## CLI publish limit

The `zuku` CLI's production publish (`zuku deploy --yolo`, or `zuku agent --yolo`) has its own server-enforced limit: **3 successful publishes per ZUKU account in a rolling 6 hours**. Unsettled reservations also hold a slot. Retrying the same account, content and verified package SHA-256 doesn't use another slot, and failed or rejected publishes don't count. Going over returns `429 DEPLOY_QUOTA_EXCEEDED` with `Retry-After`. Drafts and uploads don't use this limit, though uploads still count toward the `upload` request kind above. Check your status with `zuku account --quota`. See [Publishing](cli/publishing.md).

Related: [Errors](errors.md) · [Authentication](authentication.md) · [Game Cloud](game-cloud.md)
