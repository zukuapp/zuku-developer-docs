---
title: Bring an existing game
description: Turn an HTML5, Canvas, or Phaser game you already have into a ZUKU project that validates and packages.
section: Starter
---

# Bring an existing game

Already have a browser game? You don't need a template. A ZUKU project is just your game files plus a small manifest. This guide shows you how to restructure an existing HTML5, Canvas, or Phaser game so that `zuku validate` passes and `zuku package` produces a `.zwf` file.

## The target layout

```text
my-game/
├── zukujs.json        # manifest at the project root (never packaged)
└── src/               # the packaged folder
    ├── index.html     # entry point, directly inside src/
    ├── game.js
    └── assets/...
```

Copy your game into `src/` so that `index.html` sits directly inside it, not in a subfolder. The source root must contain exactly one of `index.html` or `index.htm`.

## 1. Add zukujs.json

Create `zukujs.json` in the project root. Only `schema`, `name`, `title`, and `version` are required:

```json
{
  "schema": "zukujs-project/1",
  "name": "my-game",
  "title": "My Game",
  "version": "1.0.0",
  "source": "src",
  "entry": "index.html",
  "jump": { "genre": "arcade", "platform": { "pc": true, "mobile": false } },
  "package": { "format": "zwf", "exclude": [] }
}
```

- `name`: lowercase letters, digits, `_`, and `-`, up to 64 characters.
- `version`: plain `MAJOR.MINOR.PATCH`, for example `1.0.0`.
- `source`: defaults to `src`. You can't use `dist`, because that's where packages are written.
- `entry`: `index.html` (the default) or `index.htm`.
- Unknown fields are rejected, so stick to the fields in the [command reference](../cli/commands.md).

The file must be UTF-8 JSON without a BOM.

A shortcut: run `zuku create my-game`, delete the sample files in `src/`, and copy your game in. You get a valid manifest to start from.

## 2. Make every path relative

The package is served from its own location, so absolute paths break.

```html
<!-- Before -->
<script src="/js/game.js"></script>
<!-- After -->
<script src="js/game.js"></script>
```

Check your HTML, CSS `url(...)` values, and loader calls, such as Phaser's `this.load.image('hero', 'assets/hero.png')`. Match the exact letter case of each file name. Two files whose names differ only by case are rejected.

## 3. Bundle what you load from the network

A ZUKU package declares package-only network access. Download any library you load from a CDN (Phaser, fonts, and so on) into `src/`, and point to the local copy instead. Don't depend on remote APIs or analytics scripts in order to start or play the game.

## 4. Remove build-only files

`package` doesn't run build commands. If your game uses a bundler, build it first and copy the **output** into `src/`, not your raw sources.

While scanning, the CLI skips hidden files and `node_modules` with a warning. It reports an error for symlinks, hard links, special files, and native executables. Only web file types are allowed, such as HTML, JS, CSS, JSON, images, audio, video, fonts, and WASM. You can leave out other paths with `package.exclude`, using exact relative paths (globs aren't supported).

## 5. Validate and package

```sh
cd my-game
zuku run                      # preview locally, stop with Ctrl+C
zuku validate .               # fix every error it reports
zuku package . --format zwf   # writes dist/<name>-<version>.zwf
zuku validate dist/<name>-<version>.zwf
```

Errors point at the exact file or manifest field, for example `ENTRY_MISSING`, `FILE_TYPE_UNSUPPORTED`, or `MANIFEST_UNKNOWN_FIELD`.

## Size limits

Package validation enforces these documented budgets: up to 8,000 entries, a ZIP of up to 500 MiB, up to 128 MiB per file uncompressed, and up to 512 MiB uncompressed in total. Compress large audio and video before packaging.

## Next steps

- [Publishing](../cli/publishing.md) to upload your package as a draft
- [Phaser starter](phaser.md) to compare against a known-good Phaser layout
- Prefer to generate a fresh game? `zuku agent` can build one, but online generation needs authentication and a configured provider. See [Game agent](../cli/agent.md) and [Authentication](../cli/authentication.md).
