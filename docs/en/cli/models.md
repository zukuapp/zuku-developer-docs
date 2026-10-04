---
title: Models
description: List, select and inspect the AI models the local game agent uses, starting from the default zuku/auto.
section: Guide
---

# Models

The local game agent runs on one model from one provider. Unless you choose otherwise, that model is `zuku/auto` from the official ZUKU AI provider.

## Model addresses

Models are written as `<provider>/<model>`. The CLI splits the address at the **first** `/` only, so model IDs that contain slashes stay intact.

```text
zuku/auto
openai/<model>
anthropic/<model>
openrouter/<vendor>/<model>      # provider = openrouter, model = <vendor>/<model>
ollama/<model>
```

A provider ID uses lowercase letters, digits and `-`, up to 64 characters. A model ID can be up to 256 characters. Addresses with spaces, control characters, `%`, `\`, empty segments or `.`/`..` segments are rejected with `MODEL_ADDRESS_INVALID`.

## Commands

```sh
zuku model list [--provider <id>] [--refresh]   # default: current provider
zuku model refresh [--provider <id>]            # ignore the cache and fetch again
zuku model use <provider/model>                 # omit in a terminal to pick from a list
zuku model info [<provider/model>] [--refresh]  # default: current model
zuku model current
```

`zuku model use` sets the provider and the model together. `zukujs model ...` changes the same settings.

## The model catalog is dynamic

The CLI doesn't hard-code a list of models. In particular, `zuku/auto` is a routing alias on the ZUKU server, and the models behind it can change. To see what is available right now, run:

```sh
zuku model list --provider zuku
```

The ZUKU catalog requires a ZUKU account signed in with the generation permission (`zuku login zuku --generate`). See [Authentication](authentication.md).

Each entry has a `source`:

| `source` | Meaning |
| --- | --- |
| `builtin` | The native alias `zuku/auto` |
| `configured` | Added by you with `provider add` or `provider configure --model` |
| `discovered` | Returned by the provider's own model list API |

If a provider has a model list API, the CLI asks it. If not, the CLI shows only the models you registered and never makes up entries. Selecting a model that isn't listed fails with `MODEL_UNAVAILABLE`.

The list also reports a discovery status: `fresh`, `cached`, `stale` (the fetch failed and an earlier cache was used), `unavailable` or `unsupported`.

## Caching

Results are cached per provider for 15 minutes. The cache is skipped when the provider's endpoint, options, sign-in method or account changes. It never contains keys, tokens or secret header values. After you sign out, or when sign-in fails, the CLI won't show the previous account's catalog. Failed fetches aren't retried automatically. Run `zuku model refresh` when you want a fresh list.

## Model details

`zuku model info` shows a model's capabilities, context window, output limit and price where known. These values are only filled in when the provider's API or your own configuration supplies them. Unknown values are shown as `null` instead of being guessed.

```sh
zuku model info openai/<model> --json
```

## Using a model with the agent

```sh
zuku agent "a one-button space dodger" --model anthropic/<model>
```

- Without `--model`, the agent uses the model selected with `zuku model use`. If none is selected, it uses `zuku/auto`.
- `--model auto` means `zuku/auto`. A model ID without a provider is attached to the current provider.
- If the selected provider is disabled or the model is unknown, the run fails. The CLI never switches to another provider, and never to a paid one.
- Custom endpoints and Codex are **Experimental** and require `--experimental` on the agent command.

The agent is limited to ZUKU game development, whichever model you choose. See [Agent](agent.md), [Providers](providers.md) and [Commands](commands.md). Error codes are listed in [Errors](../errors.md).
