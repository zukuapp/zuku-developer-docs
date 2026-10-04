---
title: Publishing
description: Package a game, connect your ZUKU account, upload a draft, and publish to production with --yolo.
section: Guide
---

# Publishing

Getting a game onto ZUKU takes four steps: package it, sign in to your ZUKU account, upload a draft, and publish. Packaging is fully local. Uploading creates a draft that stays out of public listings. Publishing to production always needs the explicit `--yolo` flag.

## 1. Package

Run these commands inside your project directory:

```sh
zuku validate .
zuku package . --format zwf
```

The output goes to `dist/<name>-<version>.zwf` by default. Use `--format zip` for a ZIP, `-o <file>` to choose the path, and `--force` to overwrite an existing file. Packaging is deterministic, so the same input always produces the same bytes. Symlinks, hard links, path traversal, native executables and archives that go over the decompression budget are rejected. See [Commands](commands.md) for every flag.

## 2. Sign in to your ZUKU account

```sh
zuku login zuku
```

The CLI opens the official ZUKU page in your browser, where you confirm your account and approve the game permissions (`games:upload games:create games:publish`). The CLI never asks for your password or a copied token. Use `--no-browser` to open the page yourself.

`zuku` and `zukujs` share the same sign-in and state in `~/.config/zukujs/` (Windows: `%LOCALAPPDATA%\ZukuJS\`). Web sessions, developer keys and other environment credentials can't stand in for this connection. See [Authentication](authentication.md).

## 3. Upload a draft

```sh
zuku upload .
zuku upload dist/my-game-1.0.0.zwf --title "My Game" --platform pc,mobile --tag arcade --verify
```

`upload` uploads the package and creates a **draft** JUMP content item. It doesn't publish anything. Metadata comes from `zukujs.json`, and flags take precedence. `--verify` reads the draft back with owner permissions.

Drafts don't appear in public listings, but the uploaded `/uploads/...` file URL is public. Uploads and drafts don't count toward the publish limit.

The upload and the draft creation are separate requests, and the CLI never retries them automatically. If the result is ambiguous (5xx, 408, or a transport failure), the CLI records it in the receipt under `.zukujs/receipts`. Check whether the draft already exists before you run the command again.

## 4. Publish

```sh
zuku account --quota
zuku deploy ./my-game --yolo
```

`--yolo` is your explicit decision to publish the verified game to production right away. There's no separate approval prompt after it, and without `--yolo` `deploy` refuses to run (`DEPLOY_YOLO_REQUIRED`). The [game agent](agent.md) uses the same rule: `zuku agent "..." --yolo` builds, playtests and publishes once.

Before it publishes anything, the CLI saves a recovery record to `.zukujs/receipts` (or `--receipt-dir`). The record ties together your account, an operation key, and the package SHA-256 and size. The draft and the publish share the same `Idempotency-Key`. If you rerun the same source after it has already been published, the CLI only reads the result back. It doesn't publish again or use more quota.

### Limits

The server allows **3 successful production publishes per account in a rolling 6 hours**, across all devices and concurrent runs. Reservations whose outcome isn't settled yet also hold a slot. `zuku account --quota` shows:

| Field | Meaning |
| --- | --- |
| `used` | Successful publishes in the window |
| `pending` | Unsettled reservations |
| `remaining` | Publishes left |
| `reset_at` | When a slot frees up |
| `retry_after` | Seconds to wait |

When you hit the limit, you get `DEPLOY_QUOTA_EXCEEDED` (HTTP `429` with `Retry-After` from the server). Wait until the reset time. See [Rate limits](../rate-limits.md).

### Unknown outcomes

If the connection drops, the CLI asks the server for the state of the same operation key. It only counts a publish as successful when the state is complete and the source is verified. A `publishing` or `uncertain` state is never published again automatically, and you'll see `DEPLOY_OUTCOME_UNKNOWN`. Don't create a new key or delete local records to get around this. Check the saved deployment with:

```sh
zuku deploy --content cnt_EXAMPLE --yolo --receipt-dir .zukujs/receipts
```

This only works from the same installation, with the original account connection and the preserved recovery record.

## Account cleanup

```sh
zuku account logout
```

Logging out leaves a token-free record behind, so a late sign-in or refresh can't bring the connection back. If you switch accounts mid-run, in-progress publishing stops (`ZUKU_ACCOUNT_CHANGED`). Records from the earlier test server aren't converted. If you see `ZUKU_ACCOUNT_MIGRATION_REQUIRED`, run `zuku login zuku` again. Don't commit `.zukujs/` to a repository.
