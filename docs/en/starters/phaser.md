---
title: Phaser 2D starter
description: Download the Phaser starter archive, run it locally, and package it with the ZUKU CLI. No CDN or npm required.
section: Starter
---

# Phaser 2D starter

[Phaser](https://phaser.io) is an open-source framework for 2D browser games, with scenes, sprites, arcade physics, and an asset loader. The ZUKU Phaser starter is a working Phaser project. It uses the same CLI commands as every other ZUKU game to preview, validate, and package.

`zuku create` always scaffolds the [Canvas runner](html5.md), and it has no template option. The Phaser starter is a separate download.

## Download

Download [zuku-phaser-starter.zip](/assets/starters/zuku-phaser-starter.zip) and unzip it wherever you keep your projects:

```sh
unzip zuku-phaser-starter.zip
cd zuku-phaser-starter   # use the folder name the archive extracts to
```

On Windows, right-click the file and choose **Extract All**.

## What's in the archive

The archive contains:

- an `index.html` entry point,
- a bundled Phaser vendor file that ships with the game,
- your game code, which `index.html` loads with relative paths.

Phaser is vendored: the library file sits inside the project and is loaded from there. The starter doesn't load anything from a CDN, and there's no `npm install` step.

Before you run anything, check the project root for a `zukujs.json` manifest. The CLI needs it, along with the `source` folder it points to (`src` by default), where `index.html` must be. If the manifest is missing, `zuku validate` reports `MANIFEST_MISSING`. [Bring an existing game](existing-game.md) explains how to create one.

## Run it

From inside the project folder:

```sh
zuku run
```

This serves a read-only preview on `127.0.0.1` and prints the URL. Press Ctrl+C to stop. `zuku run` always previews the current folder and doesn't take a path argument.

## Edit

Edit the game code files, not the vendor file. Phaser-specific rules:

- Load assets with relative paths. Put images, audio, and atlases inside the source folder and load them with paths such as `assets/hero.png`. Don't use absolute URLs or paths that start with `/`.
- Keep Phaser local. To upgrade Phaser, replace the vendored file with the new build instead of switching to a CDN link. A ZUKU package declares package-only network access, so everything the game needs must be inside the package.
- Support touch if you declare mobile. Set `jump.platform.mobile` or `tablet` to `true` in `zukujs.json` only if every action also works with pointer or touch input.

## Validate and package

```sh
zuku validate .
zuku package . --format zwf
```

`validate` checks the manifest and every file in the source folder: allowed file types, no symlinks, no native executables, and the entry point in place. `package` writes `dist/<name>-<version>.zwf` and refuses to overwrite an existing file unless you pass `--force`. `validate` also checks the finished package:

```sh
zuku validate dist/<name>-<version>.zwf
```

All three commands run offline. Draft uploads are covered in [Publishing](../cli/publishing.md).

<span id="prefer-to-generate-a-phaser-game"></span>

## Generate a Phaser game

CLI 0.3.0 does not include Phaser. The agent selects Phaser only if the `phaser` package is installed separately alongside the CLI. It then copies the build and license into the project's `src/vendor/` folder without relying on a CDN. The downloadable starter on this page already includes Phaser and needs no additional installation. Agent generation requires credentials for the selected provider or a local model. ZUKU AI, uploading, and publishing require a ZUKU account. See [Game agent](../cli/agent.md) and [Authentication](../cli/authentication.md).

## Next steps

- [Command reference](../cli/commands.md)
- [Bring an existing game](existing-game.md) if you already have Phaser code
- [Canvas runner](html5.md) for a dependency-free alternative
