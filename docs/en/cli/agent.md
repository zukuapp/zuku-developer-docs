---
title: Game agent
description: Build a ZUKU game locally with zuku agent, verify it in a real browser, and optionally upload a draft or publish it.
section: Guide
---

# Game agent

`zuku agent` turns a one-line request into a playable HTML5 game on your machine. It plans the game, writes the code, checks it against quality gates, plays it in a real sandboxed Chromium, and packages it. Nothing leaves your machine as a game until you ask for it with `--draft` or `--yolo`.

The agent only works on the ZUKU games ecosystem. It creates and maintains ZUKU/ZukuJS game projects and rejects unrelated tasks with `AGENT_REQUEST_OUT_OF_SCOPE`.

## Before you start

Generation needs a selected model and that provider's credentials, or a working local model. The default model address is `zuku/auto`, the official ZUKU AI provider. A ZUKU account is needed for ZUKU AI, draft uploads and publishing; generating with your own external-provider key or local model does not require a ZUKU account:

- [Authentication](authentication.md): sign in with `zuku login zuku`. ZUKU generation uses the `games:generate` permission, which you request explicitly with `zuku login zuku --generate`.
- [Providers](providers.md): configure where model calls go.
- [Models](models.md): pick a model with `zuku model use <provider/model>`. Without a choice, the agent uses `zuku/auto`.

Run the agent as a regular user, not root. The playtest browser always runs with its sandbox enabled. `--browser` remains in help and the parser, but currently fails with `CORE_PROTOCOL_GAP` because Agent Core cannot accept it.

## Usage

```sh
zuku agent "an arcade game where you dodge falling blocks across three lanes"
zuku agent "..." --name lane-dodger     # choose the project directory name
zuku agent "..." --model zuku/auto      # pass a model address
zuku agent "..." --draft                # build, then upload a draft only
zuku agent "..." --yolo                 # build, then publish to production once
zuku agent --resume <run_id> --yolo     # resume a recorded run
```

| Flag | Meaning |
| --- | --- |
| `--name <name>` | New project directory name (`[a-z0-9][a-z0-9_-]{0,63}`). An existing path is refused before any model call. |
| `--model <id>` | Model address. Defaults to your selected model, then `zuku/auto`. |
| `--draft` | After packaging, upload and create a **draft** only. Cannot be combined with `--yolo`. |
| `--yolo` | Your explicit, one-time approval to publish to production. |
| `--resume <run_id>` | Continue a recorded run. Cannot be combined with a request, `--name` or `--model`. |
| `--experimental` | Explicit opt-in for an Agent Core session using Codex or a custom provider. |

Unknown, duplicated or conflicting flags fail with `INVALID_INPUT` (exit code 2) before anything is touched. If you omit the request in an interactive terminal, the agent asks for one line. Non-interactive runs fail with `AGENT_REQUEST_REQUIRED`. Requests are limited to 4,000 characters.

## The five-stage pipeline

Each model stage is bound to one mandatory game skill and returns schema-validated JSON only:

1. **design**: player verbs, core loop, loss and reset conditions, key mapping, HUD and menus.
2. **architecture**: module layout with simulation, render, input and boot roles.
3. **implementation**: the files under `src/`.
4. **playtest**: an input script that a real browser executes.
5. **publish**: store metadata such as title, description and tags.

The CLI checks every stage with code gates. Unsafe output (path escapes, commands, network access, secrets) is never written. The project is then validated, played in sandboxed Chromium on `127.0.0.1` with external requests blocked, and packaged with the same core as `zuku package`. If the playtest fails, the editable project stays on disk but nothing is packaged, uploaded or published.

**Engines.** The agent can generate Phaser games when the `phaser` package is installed alongside the CLI; Phaser is not bundled with CLI 0.3.0. Otherwise, it uses the Canvas scaffold family from `zuku create`.

## Modes

- **Default**: stops at `packaged`. Nothing is uploaded or published.
- **`--draft`**: creates a draft through the regular upload flow. The draft is not published.
- **`--yolo`**: publishes exactly once, and only if the packaged bytes match the bytes that passed the playtest. There are no extra confirmation prompts.

The server allows **3 successful production publishes per ZUKU account in a rolling 6 hours**. Failed or rejected publishes do not count. A fourth attempt gets `DEPLOY_QUOTA_EXCEEDED` with a retry time, and `--yolo` checks the quota before spending model tokens. Check it with `zuku account --quota`. See [Publishing](publishing.md).

## Unknown outcomes and recovery

Publishing involves paid model usage and a quota-limited server action, so the agent never retries blindly. If a publish times out or the response can't be read, the run is recorded as `AGENT_PUBLISH_OUTCOME_UNKNOWN` and is **not** retried automatically. Resume it instead:

```sh
zuku agent --resume <run_id> --yolo
```

Resuming asks the server for the state first. A run that was already published is marked as a success and not sent again. The agent publishes only after the server confirms the game was not published, and only after the source still matches and passes the playtest again. If the server can't be reached, the run stops with `AGENT_RECOVERY_REQUIRED`. Resuming never calls the model.

Run state and receipts live in `.zukujs/agent/` in your working directory. Don't commit `.zukujs/`.
