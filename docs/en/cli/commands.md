---
title: Command reference
description: Every ZUKU CLI 0.3.0 command and flag, with synopsis, behavior and examples.
section: Reference
---

# Command reference

This page lists every command in ZUKU CLI 0.3.0. `zuku` and `zukujs` are the same program and accept the same commands. The examples use `zuku`.

```sh
zuku [command] [options]
```

If you run `zuku` without a command, or start with a quoted request or an agent flag such as `--yolo`, the CLI runs the [game agent](agent.md).

## Global options

| Option | Description |
| --- | --- |
| `--help`, `-h` | Show help. Also works after a command, for example `zuku package --help`. |
| `--version`, `-v` | Show the runtime and CLI versions. |
| `--json` | Print a single-line JSON envelope instead of human output. See [Output format](#output-format). |

## Summary

| Command | Network | Description |
| --- | --- | --- |
| [`help`](#help) | No | List commands |
| [`version`](#version) | No | Show versions |
| [`status`, `diagnostics`](#status-and-diagnostics) | Optional | Show local setup and credential state |
| [`doctor`](#doctor) | No | Check the CLI, Agent Core, provider and project |
| [`completion`](#completion) | No | Print a shell completion script |
| [`create`](#create) | No | Create a new project |
| [`run`](#run) | No | Preview the current project locally |
| [`validate`](#validate) | No | Check a project, `.zwf` or `.zip` |
| [`package`](#package) | No | Build a reproducible `.zwf` or `.zip` |
| [`agent`](#agent) | Yes | Build, verify and optionally publish a game with the agent |
| [`init`](#init) | Yes | Create a new game in the current folder with the agent |
| [`chat`](#chat) | Yes | Keep working on the current game with the agent |
| [`test`](#test) | No | Run the project's declared tests in a sandbox |
| [`build`](#build) | No | Build the current game |
| [`studio`](#studio) | Local | Start the local browser adapter |
| [`provider`](#provider) | Varies | Manage AI providers |
| [`model`](#model) | Varies | List and select models |
| [`auth`](#auth) | Varies | Provider sign-in status, login and logout |
| [`login`](#login) | Yes | Connect a ZUKU account or the experimental Codex integration |
| [`account`](#account) | Yes | Show ZUKU account connection and publish quota |
| [`upload`](#upload) | Yes | Upload a package and create a draft |
| [`deploy`](#deploy) | Yes | Publish to production in one explicit step |

## Basic commands

### help

```sh
zuku help
zuku --help
zuku <command> --help
```

Prints the list of commands, their usage and common flags.

### version

```sh
zuku version
zuku --version
```

Prints the runtime name, runtime version, command protocol and CLI version.

### status and diagnostics

```sh
zuku status [--check-api]
zuku diagnostics [--check-api]
```

Without flags, reports the runtime and CLI versions, the API address and whether credentials are configured. It makes no network requests.

| Flag | Description |
| --- | --- |
| `--check-api` | Make read-only requests to confirm the public API is reachable and, if you are signed in, that your credentials work. |

Account IDs, email addresses and tokens are never printed.

```sh
# Check local setup without touching the network
zuku status

# Also confirm the API and your sign-in
zuku status --check-api
```

### doctor

```sh
zuku doctor [--no-start]
```

Read-only health report: CLI identity (both names), Agent Core connection, active provider and model, auth status (metadata only), framework availability and what kind of folder you are in. It never prints credentials.

| Flag | Description |
| --- | --- |
| `--no-start` | Don't start Agent Core if it isn't already running. |

### completion

```sh
zuku completion bash|zsh|fish
```

Prints a completion script for your shell.

```sh
# Load completions in the current Bash session
source <(zuku completion bash)
```

## Project commands

These commands work entirely on your machine. See [Getting started](../getting-started.md) for a walkthrough.

### create

```sh
zuku create <name>
```

Creates a new folder `<name>/` with a playable HTML5 game: a Canvas JUMP obstacle runner where Space or a tap makes the player jump.

- `<name>` may contain lowercase letters, digits, `_` and `-`, up to 64 characters.
- The command never overwrites an existing path. If `<name>` already exists, it fails with `PROJECT_EXISTS`.
- `create` takes only a name. There is no template flag.

Generated files:

| File | Purpose |
| --- | --- |
| `zukujs.json` | Project manifest (`zukujs-project/1`), version `0.1.0`, package format `zwf` |
| `src/index.html` | Entry point |
| `src/game.js` | Game code |
| `README.md` | Project notes |
| `.gitignore` | Ignores build output and local files |

```sh
# Create a project and move into it
zuku create my-game
cd my-game
```

For other starting points, see [Starters](../starters/index.md).

### run

```sh
zuku run [--port <n>] [--once]
```

Previews the game in the **current folder**. `run` doesn't take a path, so `cd` into the project first. The CLI asks Agent Core for a read-only snapshot of the project and serves it on `127.0.0.1` until you press Ctrl+C. Stopping with Ctrl+C is a normal exit (code 0).

| Flag | Default | Description |
| --- | --- | --- |
| `--port <n>` | Random free port | Port to listen on (0–65535) |
| `--once` | Off | Return the preview metadata only, without starting a server |

```sh
cd my-game
# Serve a preview and print its local URL
zuku run

# Use a fixed port
zuku run --port 5173
```

### validate

```sh
zuku validate <dir | file.zwf | file.zip>
```

Checks a project or package without running any of its code.

- **Directory**: normalizes `zukujs.json` and checks the source files against the package rules.
- **`.zwf` / `.zip`**: checks the package with the public ZWF validation rules.

`validate`, `package` and `upload` share the same checks, so a project that validates will package the same way.

```sh
# Validate the project in the current folder
zuku validate .

# Validate a built package
zuku validate dist/my-game-0.1.0.zwf
```

### package

```sh
zuku package <dir> [--format zwf|zip] [--output <file> | -o <file>] [--force]
```

Builds a deterministic package. Paths are sorted and timestamps are fixed, so the same input always produces the same bytes.

| Flag | Default | Description |
| --- | --- | --- |
| `--format zwf\|zip` | `package.format` in the manifest, otherwise `zwf` | Output format. The flag overrides the manifest. |
| `--output <file>`, `-o <file>` | `dist/<name>-<version>.<format>` | Output path |
| `--force` | Off | Overwrite an existing output file |

Packaging rejects symbolic links, hard links, path traversal, special files, native executables, case-only name collisions and archives that exceed the decompression budget. It never runs build commands from the project.

```sh
# Build the default ZWF package
zuku package . --format zwf

# Build a ZIP at a custom path, replacing any existing file
zuku package . --format zip -o build/my-game.zip --force
```

## Agent commands

The agent commands run through Agent Core, the local service that `zuku`, `zukujs` and [ZUKU Studio](studio.md) share. The agent only accepts ZUKU game-development tasks. The default model is `zuku/auto`, and the CLI never switches to a paid provider on its own. See [Game agent](agent.md) for the full workflow.

### agent

```sh
zuku agent ["<request>"] [--name <name>] [--model <provider/model>]
           [--draft | --yolo] [--experimental] [--resume <run_id>]
zuku "<request>" [flags]
```

Builds the game, verifies it in a browser and reports the result. In an existing ZUKU game folder, it maintains that game. Anywhere else, or with `--name` or `--resume`, it creates a new game. Without `--draft` or `--yolo`, nothing is uploaded.

| Flag | Description |
| --- | --- |
| `--name <name>` | Name for a new game |
| `--model <provider/model>` | Model to use. `auto` means `zuku/auto`. See [Models](models.md). |
| `--draft` | After verification, upload the game as a **draft** only |
| `--yolo` | After verification, publish to production once, with no further prompt. Limited by the server to 3 successful production publishes per account in a rolling 6 hours. |
| `--experimental` | Required to run with an experimental `(exp!)` auth method, such as the Codex integration |
| `--resume <run_id>` | Resume an earlier run from this folder |

`--browser <path>` is listed in help, but the current Agent Core protocol can't accept it.

```sh
# Build and verify a game, without uploading
zuku agent "A one-button runner where a cat jumps over cacti"

# Same, then save it as a draft on ZUKU
zuku "A one-button runner where a cat jumps over cacti" --draft

# Build, verify and publish to production in one go
zuku agent "Neon brick breaker" --name neon-bricks --yolo
```

### init

```sh
zuku init ["<request>"] [--name <name>] [--model <provider/model>]
          [--draft | --yolo] [--experimental]
```

Always creates a **new** game in the current folder through Agent Core. Flags mean the same as for `agent`.

### chat

```sh
zuku chat ["<message>"] [--model <provider/model>] [--experimental] [--draft | --yolo]
```

Maintains the ZUKU game in the current folder in a single agent session. Without a message, it reads turns from the terminal until you enter an empty line.

```sh
cd my-game
# Ask for one change
zuku chat "Make the jump a little higher"
```

### test

```sh
zuku test
```

Runs the project's declared tests inside Agent Core's OS sandbox. The current folder must be a ZUKU game.

### build

```sh
zuku build
```

If the ZukuJS web framework is installed in the project, `build` is passed to the framework (see [Web framework commands](#web-framework-commands)). Otherwise, if the current folder is a ZUKU game, Agent Core builds it. In any other folder it fails with `FRAMEWORK_UNAVAILABLE`.

### studio

```sh
zuku studio [--port <n>]
```

Starts the local browser adapter on `127.0.0.1` (default port `43127`) for the official local browser frontend at `https://ai.zuzunza.com`, backed by the same Agent Core. Browser pairing, session resume and sign-in requests must be approved in this terminal. Press Ctrl+C to stop; running agent sessions are not cancelled. Hosted web AI access is currently closed. See [ZUKU Studio](studio.md).

## Providers, models and credentials

All three commands share settings with Agent Core and Studio, and never print secrets.

### provider

```sh
zuku provider [list]
zuku provider show <id>
zuku provider use <id>
zuku provider add --id <id> --type openai-chat|openai-responses|anthropic --base-url <url>
                  [--name <name>] [--model <id>]... [--api-key-env <VAR> | --api-key-stdin]
zuku provider configure <id> [--option KEY=VALUE]... [--model <id>] [--api-key-env <VAR>]
zuku provider remove <id> [--yes]
zuku provider enable <id>
zuku provider disable <id>
```

The official provider is ZUKU AI (`zuku`). Custom endpoints you add are marked `(exp!)`. See [Providers](providers.md) for supported types and `--option` keys.

```sh
# List providers and see which one is active
zuku provider list

# Add an OpenAI-compatible endpoint, reading the key from an environment variable
zuku provider add --id my-llm --type openai-chat --base-url https://llm.example.com/v1 --api-key-env MY_LLM_KEY
```

### model

```sh
zuku model [list] [--provider <id>] [--refresh]
zuku model refresh [--provider <id>]
zuku model current
zuku model use <provider/model>
zuku model info <provider/model> [--refresh]
```

Model addresses are `<provider>/<model>`, split at the first `/`. The default is `zuku/auto`. The ZUKU AI model catalog is dynamic, so use `model list` to see what's available. See [Models](models.md).

```sh
# Show the active model
zuku model current

# Switch back to the default
zuku model use zuku/auto
```

### auth

```sh
zuku auth [list] [--provider <id>]
zuku auth login --provider <id> [--api-key-stdin | --api-key-env <VAR>] [--experimental] [--no-browser]
zuku auth logout --provider <id>
```

Shows sign-in status, or signs in to or out of a provider. Keys are read from a hidden prompt, one line of stdin or an environment variable. Never pass a key as an argument. See [Authentication](authentication.md).

```sh
# Pipe an API key in without it appearing in shell history
printf '%s\n' "$MY_LLM_KEY" | zuku auth login --provider my-llm --api-key-stdin
```

## Account and publishing

### login

```sh
zuku login zuku [--no-browser] [--generate]
zuku login codex --experimental [--account <id>]
```

`login zuku` connects your ZUKU account with a device code. The CLI prints the official URL and approval code and opens your browser unless you pass `--no-browser`. `--generate` also requests the native game-generation scope.

`login codex --experimental` connects the Codex integration. This integration is experimental and unofficial, and is marked `(exp!)`. `--experimental` is required.

```sh
# Connect your ZUKU account on a machine without a browser
zuku login zuku --no-browser
```

### account

```sh
zuku account [--quota]
zuku account logout
```

Shows whether a ZUKU account is connected and its scope. `--quota` also shows your remaining production publishes. `logout` removes the local sign-in first, then tries to revoke it on the server.

### upload

```sh
zuku upload <dir | file.zwf | file.zip> [options]
```

Uploads a package and creates a **draft** JUMP game. It never publishes. If you pass a directory, it's packaged with the same rules as `package` first. Metadata comes from `zukujs.json`, and flags override it.

| Flag | Description |
| --- | --- |
| `--title <text>` | Title, 1–100 characters |
| `--description <text>` | Description, up to 500 characters |
| `--game-id <id>` | `jump.game_id` client metadata (not the content ID) |
| `--genre <genre>` | `jump.genre` |
| `--version <version>` | Package version |
| `--age-rating all\|12\|15\|18` | Age rating |
| `--tag <tag>` | Tag; repeat for more, up to 10 |
| `--platform pc,mobile,tablet` | Platforms the game actually supports, comma-separated |
| `--receipt-dir <dir>` | Receipt folder (default `.zukujs/receipts`) |
| `--verify` | Read the draft back as owner after creating it |

Uploads are never retried automatically. If the result is unclear, it's recorded in a receipt. Check whether the draft exists before running the command again. Don't commit `.zukujs/` to version control.

```sh
# Package the current folder and create a draft
zuku upload .

# Upload a built package with metadata and confirm the draft
zuku upload dist/my-game-0.1.0.zwf --title "My Game" --platform pc,mobile --tag arcade --verify
```

### deploy

```sh
zuku deploy <dir | file.zwf | file.zip> --yolo [upload options]
zuku deploy --content <content_id> --yolo [--receipt-dir <dir>]
```

Publishes to production in one explicit step: upload, create the draft, then publish. Requires a connected ZUKU account (`zuku login zuku`) and exactly one `--yolo`. Accepts the same metadata flags as `upload`.

The server allows 3 successful production publishes per account in a rolling 6 hours. A deploy is bound to your account and package hash, and the CLI never repeats a publish request when the outcome is unclear. The second form recovers a deploy recorded in the receipt folder. See [Publishing](publishing.md).

```sh
# Check your remaining quota, then publish
zuku account --quota
zuku deploy . --yolo --title "My Game" --platform pc,mobile
```

## Web framework commands

```sh
zuku dev|build|start|info|analyze|typegen|telemetry|upgrade [options]
```

If the ZukuJS web framework package `zukujs` is installed in the project, these commands are passed straight to it, with its own arguments, output and exit codes. The game `--json` envelope doesn't apply. The CLI doesn't install the framework. If it's missing, these commands fail with `FRAMEWORK_UNAVAILABLE` (except `build` in a ZUKU game folder, described above).

## Output format

Commands print results as `zuku-command/1`.

| Case | Stream | Format |
| --- | --- | --- |
| Success, `--json` | stdout | One line: `{"success":true,"data":...,"meta":{...}}` |
| Success | stdout | Human-readable output |
| Failure, `--json` | stderr | One line: `{"success":false,"error":{"code","message"},"meta":{...}}` |
| Failure | stderr | `CODE: message` |

## Exit codes

| Code | Meaning |
| --- | --- |
| 0 | Success (including stopping `run` or `studio` with Ctrl+C) |
| 1 | Failure: validation, packaging, credentials, API errors and so on |
| 2 | Invalid arguments (`INVALID_INPUT`) or unknown command (`UNKNOWN_COMMAND`) |
| 130 | Cancelled by the user (`COMMAND_CANCELLED`, Ctrl+C) |

Server errors are reported with the HTTP status and a verified API error code, such as `UNAUTHORIZED`, `INVALID_PACKAGE`, `PAYLOAD_TOO_LARGE` or `VALIDATION_ERROR`. See [Errors](../errors.md).
