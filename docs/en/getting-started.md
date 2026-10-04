---
title: Getting Started
description: Create, preview, validate, and package the ZukuJS starter jump runner in about five minutes.
section: Starter
---

# Getting Started

In about five minutes you'll create a playable HTML5 game, preview it, check it, and package it for ZUKU. Everything on this page runs locally, and `create`, `validate`, and `package` never touch the network.

## Before you start

Install the CLI if you haven't already:

```sh
curl -fsSL --proto '=https' --tlsv1.2 https://zuzunza.com/install.sh -o install-zuku-cli.sh && bash install-zuku-cli.sh
```

On Windows, or for wget and other options, see [Installation](installation.md). You don't need to install Node.js; the installer manages its own Node.js 22 runtime.

`zuku` and `zukujs` are the same CLI. This guide uses `zuku`.

## 1. Create the project

```sh
# Scaffold a new project in ./my-game
zuku create my-game
cd my-game
```

Project names use lowercase letters, numbers, `_`, and `-`, up to 64 characters. `create` never overwrites an existing folder; if `my-game` already exists, it stops with `PROJECT_EXISTS`.

`create` takes only a name. There are no template flags.

## 2. Look at the files

```text
my-game/
├── zukujs.json      # Project manifest: name, title, version, entry, package format
├── README.md        # Project notes
├── .gitignore       # Keeps dist/, *.zwf, *.zip, .zukujs/, .env out of git
└── src/
    ├── index.html   # Entry point with the game canvas
    └── game.js      # The jump runner game logic
```

The generated `zukujs.json` starts at version `0.1.0`, uses `src` as the source folder and `index.html` as the entry, targets PC, mobile, and tablet, and packages as `zwf` by default.

## 3. Play it

```sh
# Start a local preview on 127.0.0.1 (press Ctrl+C to stop)
zuku run
```

Run it from inside the project folder. The CLI prints a local preview URL; open it in your browser. To choose a port, use `zuku run --port 8080`.

The starter is a Canvas obstacle runner:

- Press **Space** or **Arrow Up**, click, or **tap** to jump.
- Red blocks scroll toward you and speed up over time.
- Hit a block and the game ends; jump again to restart. Your score and best score show in the corner.

Edit `src/game.js` to change gravity, speed, or colors, then preview again.

## 4. Validate

```sh
# Check the manifest and source files against the package rules
zuku validate .
```

Validation does not execute your game code. It checks structure and safety, for example rejecting symlinks, path traversal, and native executables.

## 5. Package

```sh
# Build a reproducible ZWF package
zuku package . --format zwf
```

The output goes to `dist/<name>-<version>.zwf`, so here `dist/my-game-0.1.0.zwf`. The same input always produces the same bytes. Existing files are not overwritten unless you add `--force`, and you can choose a path with `--output` (`-o`) or build a ZIP with `--format zip`.

You can validate the package file too:

```sh
zuku validate dist/my-game-0.1.0.zwf
```

## What's next

You now have a ZWF package ready to share. From here:

- Upload it as a draft or publish it: [Publishing](cli/publishing.md)
- Let the local agent build and browser-check a game for you: [Agent](cli/agent.md)
- Explore other starting points: [Starters](starters/index.md) and [Bring an existing game](starters/existing-game.md)
- See every command and flag: [Command reference](cli/commands.md)
- Understand error codes: [Errors](errors.md)

The local agent can use your own external-provider credentials or a local model. A ZUKU account is needed for ZUKU AI and uploading or publishing games. Hosted web AI and in-app AI are in preparation, with no opening date set. An Android app preview is available at [apk.zuzunza.com](https://apk.zuzunza.com/).
