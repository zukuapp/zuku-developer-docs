---
title: Starters
description: Three ways to start a ZUKU game - the built-in Canvas runner, a Phaser 2D starter, or a game you already have.
section: Starter
---

# Starters

Every ZUKU game ends up the same way: a folder with a `zukujs.json` manifest and a `src/` directory holding an `index.html` entry point. The ZUKU CLI checks that folder with `zuku validate` and turns it into a package with `zuku package`.

The three recipes below create that folder in different ways.

CLI installation is covered in [Installation](../installation.md).

## Canvas runner

Use for: a first ZUKU game, learning the workflow, and small arcade games.

`zuku create my-game` scaffolds a small, playable Canvas jump game. The player jumps over incoming blocks with Space, the Up arrow, a click, or a tap. It uses no engine and no dependencies: one HTML file and one JavaScript file.

[Start with the Canvas runner →](html5.md)

## Phaser 2D

Use for: sprite-based 2D games with scenes, physics, and asset loading.

Download the Phaser starter archive. Phaser is bundled in the archive as a local vendor file, so the game never loads it from a CDN and there's nothing to install with npm.

[Start with Phaser →](phaser.md)

## Bring an existing game

Use for: an HTML5, Canvas, or Phaser game that already runs in a browser.

Add a `zukujs.json` manifest, move your files under `src/`, make every asset path relative, bundle anything you currently load from the network, and validate.

[Migrate an existing game →](existing-game.md)

## Which should I pick?

| If you... | Pick | First command |
| --- | --- | --- |
| Are new to ZUKU | [Canvas runner](html5.md) | `zuku create my-game` |
| Want plain JavaScript and full control over the game loop | [Canvas runner](html5.md) | `zuku create my-game` |
| Want built-in sprites, scenes, and arcade physics | [Phaser 2D](phaser.md) | Download `zuku-phaser-starter.zip` |
| Already have a working browser game | [Existing game](existing-game.md) | `zuku validate .` |
| Would rather describe a game and have it generated | [Game agent](../cli/agent.md) | `zuku agent "..."` |

## The same workflow for every recipe

Once your project folder exists, each recipe uses the same commands:

```sh
zuku run                      # preview locally (run inside the project folder)
zuku validate .               # check the manifest and source files
zuku package . --format zwf   # build dist/<name>-<version>.zwf
```

`zuku run` previews the project in the current folder, so `cd` into it first. `validate` and `package` take a path, and `.` means the current folder. None of the three needs a network connection. Sharing a game is covered in [Publishing](../cli/publishing.md). Every flag is listed in the [command reference](../cli/commands.md).

## Generating a game instead

`zuku agent` generates a game from a one-line request. It designs, implements, playtests in a real browser, and packages the result. CLI 0.3.0 does not bundle Phaser. The agent selects Phaser only when it is installed separately alongside the CLI. The agent only builds games and needs credentials for the selected model provider or a local model. A ZUKU account is needed for ZUKU AI, draft uploads and publishing. See [Game agent](../cli/agent.md) and [Authentication](../cli/authentication.md).
