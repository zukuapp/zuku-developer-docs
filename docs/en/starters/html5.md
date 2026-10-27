---
title: Canvas runner starter
description: Scaffold a playable Canvas jump game with zuku create, learn how it works, and package it.
section: Starter
---

# Canvas runner starter

`zuku create` scaffolds a small, playable Canvas game. A square runner jumps over incoming blocks. The game speeds up over time, and one hit ends the run. It's plain HTML and JavaScript, with no engine and no dependencies.

## Create the project

```sh
zuku create my-game
cd my-game
```

The name contains lowercase letters, digits, `_`, and `-`, starts with a letter or digit, and is up to 64 characters long. `create` only makes a new folder and fails if `my-game/` already exists.

The same starter is available as an archive: [zuku-canvas-starter.zip](/assets/starters/zuku-canvas-starter.zip).

## What's inside

```text
my-game/
├── zukujs.json      # project manifest (stays local, is not packaged)
├── README.md
├── .gitignore
└── src/             # everything in here gets packaged
    ├── index.html   # entry point: a 640x360 canvas plus a script tag
    └── game.js      # the whole game
```

`zukujs.json` comes pre-filled. It sets `source` to `src`, `entry` to `index.html`, version `0.1.0`, genre `arcade`, PC, mobile, and tablet support, and `zwf` as the package format. Change the title, description, and tags to match your game.

## How the game works

`game.js` has four parts.

- State: a `player` object (position, size, vertical speed), a list of `obstacles`, plus `score`, `best`, `speed`, and an `over` flag.
- Input: Space or the Up arrow on the keyboard, or a pointer press on the canvas, calls `jump()`. During a game over, the same input resets the game.
- Update: `update(dt)` applies gravity, spawns blocks at random intervals, moves them left, slowly raises the speed, adds to the score, and checks for collisions.
- Draw and loop: `draw()` paints the background, ground, player, blocks, and score. `requestAnimationFrame` drives the loop, and `dt` is capped at 50 ms so a background tab doesn't cause a huge jump in time.

```js
// Input from game.js: keyboard and pointer both call jump()
addEventListener('keydown', event => {
  if (event.code === 'Space' || event.code === 'ArrowUp') { event.preventDefault(); jump(); }
});
canvas.addEventListener('pointerdown', event => { event.preventDefault(); jump(); });
```

## Make it yours

Common edits:

- Feel: change the jump velocity (`-620`) or gravity (`1800`) in `game.js`.
- Difficulty: change the starting `speed`, how fast it increases, or the spawn interval.
- Look: swap the `fillStyle` colors, or draw images instead of rectangles.
- Assets: put images and sounds inside `src/` and load them with relative paths such as `assets/player.png`.

Keep everything the game needs inside `src/`. Only that folder is packaged.

## Run, validate, package

From inside the project folder:

```sh
zuku run                      # local preview on 127.0.0.1, stop with Ctrl+C
zuku validate .               # check zukujs.json and the files in src/
zuku package . --format zwf   # writes dist/my-game-0.1.0.zwf
zuku validate dist/my-game-0.1.0.zwf
```

`zuku run` works on the current folder and doesn't take a path. `package` doesn't overwrite an existing output file unless you add `--force`. Increase `version` in `zukujs.json` for each new build. `--format zip` builds a ZIP instead.

Creating a draft on ZUKU is covered in [Publishing](../cli/publishing.md).

## Next steps

- [Command reference](../cli/commands.md) for every flag
- [Phaser starter](phaser.md) if you outgrow plain Canvas
- [Getting started](../getting-started.md) for the full workflow
