---
title: Authentication
description: Sign in to your ZUKU account for uploads and publishing, and connect AI provider credentials for the local game agent.
section: Guide
---

# Authentication

The ZUKU CLI uses two separate kinds of sign-in. They do different jobs, so it helps to keep them apart:

| Kind | What it is for | Commands |
| --- | --- | --- |
| ZUKU account | Uploading drafts, publishing games, and checking your publish quota | `zuku login zuku`, `zuku account` |
| AI provider credentials | Letting the local game agent call an AI model | `zuku auth`, `zuku provider`, `zuku model` |

`zuku` and `zukujs` are the same CLI. They share the same runtime, configuration, sign-in and state (`~/.config/zukujs/` (Windows: `%LOCALAPPDATA%\ZukuJS\`)), so signing in with one also signs you in with the other. User configuration and accounts live in that shared directory; a project's `.zukujs/` directory stores run records and receipts.

This page covers the CLI only. For bearer tokens used with the HTTP API, see [HTTP API authentication](../authentication.md).

## Sign in to your ZUKU account

```sh
zuku login zuku
```

The CLI opens the official ZUKU page in your browser. You confirm your account there and approve the connection, the same way you approve access for a game. The CLI never asks for your password or a copied token. On a machine without a browser, add `--no-browser` and open the URL the CLI prints yourself.

By default, the connection asks for the `games:upload games:create games:publish` permissions, which cover uploads and publishing. To use the official ZUKU AI provider (`zuku/auto`) with the local agent, also request the generation permission explicitly:

```sh
zuku login zuku --generate
```

A connection that only has the three default permissions keeps working for uploads and publishing. However, `zuku auth list` shows it as `scope-required`, and the agent can't use ZUKU AI until you sign in again with `--generate`.

Check the connection and your publish quota:

```sh
zuku account --quota
```

Publishing is limited by the server to three successful production publishes per account in a rolling six-hour window. See [Publishing](publishing.md) for details.

## Connect AI provider credentials

The local agent needs an AI provider. The default is the official ZUKU AI provider, `zuku`, with model `zuku/auto`. You can also use your own API key with a supported provider such as OpenAI or Anthropic. Official provider API keys are a normal, fully supported option.

```sh
zuku auth list                          # status only, never secret values
zuku auth login --provider openai       # hidden prompt in a terminal
zuku auth logout --provider openai
```

The CLI never accepts a secret as a command-line argument. In scripts, pass the key through stdin or point the CLI at an environment variable name:

```sh
printf '%s\n' "$KEY" | zuku auth login --provider openai --api-key-stdin
zuku auth login --provider openai --api-key-env MY_OPENAI_KEY
```

`auth login --verify` and `--header` currently fail with `CORE_PROTOCOL_GAP`; Agent Core has no carrier for them. Use `zuku auth list --provider <id>` to inspect stored status. It does not verify credentials with the remote service. The separate `upload --verify` draft-readback option remains supported.

If `--provider` is omitted, a terminal session lets you pick from a list, and a non-interactive session uses `zuku`. See [Providers](providers.md) for the full list and [Models](models.md) for choosing a model.

### Codex sign-in **Experimental**

```sh
zuku login codex --experimental
```

Codex sign-in through the CLI integration is an **Experimental**, unofficial integration. It is marked `(exp!)` in CLI output. The first sign-in requires `--experimental`, and the CLI records your sign-in opt-in in its own protected store. Separately, each new Agent Core game session using Codex or a custom provider requires `--experimental` on the agent command; otherwise it fails with `AUTH_EXPERIMENTAL_OPT_IN`. The CLI doesn't import an existing Codex session or key files from other tools. The selected provider never falls back to Codex, or to any other provider, on its own.

## Where credentials are stored

- API keys go into a protected secret store that only your user can read: owner-only files on Linux and macOS, and per-user DPAPI encryption on Windows. If the store can't be protected, the CLI fails instead of saving plaintext.
- Keys and tokens never appear in logs, error messages, `--json` output or model input.
- `zuku auth list` reports states such as `configured`, `environment`, `not-configured` and `scope-required`, and never prints the values.

## Sign out and clean up

```sh
zuku account logout                     # disconnect your ZUKU account
zuku auth logout --provider <id>        # remove a provider sign-in
```

Signing out of your ZUKU account leaves a token-free record, so a late login or refresh can't bring the connection back. If you set a key with `--api-key-env`, the CLI only stored the variable name, so also remove the variable from your shell. Keep publish receipts in `.zukujs/receipts` if you might need to recover a publish.

## Troubleshooting

| Code | Meaning |
| --- | --- |
| `AUTH_SECRET_ARGUMENT` | A secret was passed as an argument. Use the prompt, `--api-key-stdin` or `--api-key-env`. |
| `AUTH_INPUT_REQUIRED` | No input method was given in a non-interactive session. |
| `AUTH_REQUIRED` | The selected provider has no credentials. |
| `AUTH_EXPERIMENTAL_OPT_IN` | Codex was used without `--experimental` on first sign-in. |
| `ZUKU_GENERATE_SCOPE_REQUIRED` | Sign in again with `zuku login zuku --generate`. |
| `ZUKU_ACCOUNT_MIGRATION_REQUIRED` | Run `zuku login zuku` to approve the connection again. |

More codes are listed in [Errors](../errors.md).
