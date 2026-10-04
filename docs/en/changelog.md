---
title: Changelog
description: ZUKU CLI releases, ZUKU API v1 changes, the versioning policy, and deprecation notes.
section: Reference
---

# Changelog

This page tracks the ZUKU CLI releases and the ZUKU API v1. API entries list only features that are actually routed in the API.

## ZUKU CLI

### CLI 0.3.0

- **Public release.** The `zuku` and `zukujs` commands are the same CLI. They share one runtime, config, sign-in and state in `~/.config/zukujs/` (Windows: `%LOCALAPPDATA%\ZukuJS\`).
- **Official installers are live.** Install with `curl` or `wget` using `https://zuzunza.com/install.sh`, or with PowerShell using `https://zuzunza.com/install.ps1`. The installer manages Node 22.22.3 for the CLI. A fixed release archive is also available at `/downloads/zukujs/cli/0.3.0/zukujs-cli-0.3.0.tgz`. See [Installation](installation.md).
- **CI on six native platforms.** CI succeeded for all six native platforms and for the three installer paths.
- **npm is not published.** `@zukujs/cli` isn't available from the npm registry. Use the official installers.
- `zuku create <name>` scaffolds a playable Canvas jump obstacle runner (space or tap to jump). There is no `--template` flag.
- `zuku agent` builds a game locally, playtests it in a real sandboxed browser, and packages it. `--draft` uploads a draft only. `--yolo` is an explicit one-time production publish, limited by the server to 3 successful publishes per account in a rolling 6 hours. See [Game agent](cli/agent.md) and [Publishing](cli/publishing.md).
- The official ZUKU AI provider is `zuku/auto`. The model catalog is dynamic.
- Phaser isn't bundled with the CLI. The agent uses Phaser only when the `phaser` package is installed alongside the CLI.

## API versioning

| Location | Value |
|---|---|
| URL prefix | `/api/v1/…` |
| Response header | `X-API-Version: v1` |
| Envelope `meta.version` | `"v1"` |

All three point to the same API generation. Treat the **`v1` in the URL as the source of truth**, and use the header and `meta` for observation and logging.

### Current status

- **v1**: active (staging and production contract).
- **v2**: planned only. It will be introduced when path, envelope or breaking changes are needed. There's no `/api/v2` route today.

## API changelog (v1)

A summary of what's implemented. Dates reflect when the docs were organized. See the repository history for individual commits.

### 2026-10-01 · Per-plan request limits

- Plans (guest, Free, Super ZUKU, Creator and Cloud) are verified on the server, with real per-kind counters and `429` responses.
- Added account, API key and shared-IP protection, 10-second windows, and real remaining-count, reset and `Retry-After` guidance.
- Added ZUKU navigation and web API entry checks, notices that keep your edits, and a dedicated `/rate-limit` page.
- Production rollout requires shipping web, backend, migration and cache policy together. This entry doesn't mean the policy is active in production. See [policy and rollout conditions](rate-limits.md).

### 2026-09-12 · JUMP game thumbnails

- Added image checks for existing games and automatic capture of real gameplay screens for new games.
- Owners can check status and regenerate with `GET` / `POST /api/v1/contents/{id}/thumbnail-job`.
- Directly uploaded images are protected, thumbnails are rescheduled when the source changes, and failures are retried. Generating a thumbnail doesn't publish the game.

### 2026-09-12 · Docs and JUMP publishing

- Moved the public API docs to `docs.zuzunza.com`. Existing `/docs/api` links still work.
- Separated JUMP drafts from publish requests, added preview permission checks before publishing, and prevented duplicate publishing.
- Newest games are sorted first by first publish time, with `recent` as an alias for newest first.
- Added HTML5 ZWF2 package playback, AVIF image and audio uploads, and storage outage responses.
- Documented community photo attachments, partial edits, Unicode hashtag search and their actual supported scope.

### Social · Follows

- `follows` table and the `POST /creators/{handle}/follow` toggle.
- Public profiles report real `follower_count`, `following_count` and `is_following`.
- Feed `sort=following` shows work from creators you follow only.

### Auth · Captcha · Docs

- API wiki on the site at `/docs/api`, including detailed Captcha and Examples pages.

### Auth · Sessions

- `POST /api/v1/auth/register` · `signup`: sign-up (captcha gate, blocks conflicts with legacy accounts).
- `POST /api/v1/auth/login` · `logout` · `refresh`.
- `GET` / `PATCH /api/v1/auth/me`.
- `GET /api/v1/auth/sessions` · `DELETE …/sessions/{id}`: list and revoke active sessions.
- `POST /api/v1/auth/oauth/{provider}`: returns **501** `NOT_IMPLEMENTED` (out of scope).

### Captcha

- `POST /api/v1/captcha/challenge` · `verify`: self-hosted proof of work.
- Fails closed with `CAPTCHA_NOT_CONFIGURED` when the secret isn't configured.

### Feeds · Contents

- `GET /api/v1/feeds` and `/feeds/hype|swipe|jump`.
- `GET /api/v1/contents/{id}`.
- `GET /api/v1/contents/{id}/conversion`.
- `GET /api/v1/contents/{id}/recommendations`: `limit` 1–50 (default 8) and `offset`; `has_more` via LIMIT+1; short cache for signed-out users.
- `GET /api/v1/jump/games/{id}?include=related,popular`: attaches the Jump detail shelves in the same envelope.
- `POST /api/v1/contents`: Bearer **or** `X-API-Key`.
- `PATCH` / `DELETE /api/v1/contents/{id}`: Bearer only; DELETE archives.
- `POST …/like` · `POST …/bookmark`.
- Comments: `GET`/`POST …/comments`, `PATCH`/`DELETE /api/v1/comments/{id}`.

### Uploads · Jump stream

- `POST /api/v1/uploads`: multipart, MIME by magic bytes, size limits.
- `GET /uploads/{path}`: static serving without the API prefix.
- `GET /api/v1/jump/games` · `GET …/games/{id}`.
- `POST …/play` · `…/stream` (IR) · `…/swf`: **POST requires authentication**.

### Developer keys

- `POST` / `GET /api/v1/developer/keys`.
- `DELETE /api/v1/developer/keys/{id}`.
- Issued keys can create content (`X-API-Key`).

### Community posts

- `GET /api/v1/feed`: timeline.
- `POST /api/v1/posts` · `GET …/posts/{id}` · `GET …/thread`.
- `POST …/replies` · `POST`/`DELETE …/like` · `DELETE …/posts/{id}`.

### DM

- `GET`/`POST /api/v1/dm/conversations`.
- `GET`/`POST …/conversations/{id}/messages`.
- `POST …/conversations/{id}/read`.
- One-to-one, stored as plain text (end-to-end encryption and group chat are out of scope).

### Notifications

- `GET /api/v1/notifications`.
- `GET …/unread-count`.
- `POST …/read-all` · `POST …/{id}/read`.

### Other routes

- `GET /api/health`.
- `GET /api/wasm/contract`.
- Admin user lookup and patch, `308` redirects for legacy Jump paths.
- Delegated moderation and analytics module routes (each behind its own module gate).

## Breaking change policy

1. **No change that breaks existing clients ships without a URL major version (`v1` → `v2`).** Examples: adding required fields or changing their meaning, removing or renaming success envelope keys, narrowing authentication methods, reversing the meaning of an error code.
2. **Allowed (non-breaking)**: adding optional fields, new endpoints and new error codes, documenting previously undocumented behavior, and relaxing limits.
3. **When a breaking change is needed**:
   - deploy `/api/v2` alongside v1,
   - bump `X-API-Version` and `meta.version` to `v2`,
   - remove v1 only after a **deprecation notice period**.
4. The **archive semantics** of content DELETE, the **path ID = body ID** rule for Jump play, and **magic bytes first** for uploads are part of the v1 contract. Changing any of them requires a major version.
5. The new policy that replaces placeholder rate-limit headers with real quotas is published in [Rate limits](rate-limits.md). Before production rollout, the policy, timing and retry contract are announced, and web, backend and docs ship together.

## Deprecation notes

| Item | Status | Guidance |
|---|---|---|
| `/api/v1/auth/signup` | Same handler as `register` in v1 | Use `register` for new integrations. A deprecation notice will precede removing `signup`. |
| OAuth `…/auth/oauth/{provider}` | 501 `NOT_IMPLEMENTED` | No implementation planned until provider secrets are issued. Never treat a call as successful. |
| Rate-limit header values | Real policy implemented; notice required before production rollout | Check real responses and the policy endpoint ([rate-limits.md](rate-limits.md)). |
| Legacy Jump URLs (`/game/play/hg-…` and others) | `308` to canonical `/api/v1/jump/…` | New clients should use canonical paths only. |
| Expecting hard deletes | Not applicable | `DELETE /contents/{id}` **archives**. Restore and permanent deletion are a separate contract. |
| v2 | Not started | Docs placeholder only until schedule and schema are confirmed. |

APIs scheduled for deprecation run in parallel for at least **one major cycle**, and the replacement path is stated in the response or the docs.

## Related pages

- [Contents](contents.md)
- [Media](media.md)
- [Errors](errors.md)
- [Rate limits](rate-limits.md)
