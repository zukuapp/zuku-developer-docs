---
title: Build your first game
description: Install the ZUKU CLI with curl or wget, choose a playable starter, and build your first game.
section: Get started
---

<span id="your-next-game-starts-here"></span>

# Build your first game

**ZUKU - 내가 불러 일으키는 새로운 창작.**

Install the ZUKU CLI and choose a starter to build a playable game.

## Install the ZUKU CLI

The installer includes Node.js. Run the command for your terminal.

=== "curl"

    ```sh
    curl -fsSL --proto '=https' --tlsv1.2 https://zuzunza.com/install.sh -o install-zuku-cli.sh && bash install-zuku-cli.sh
    export PATH="$HOME/.local/bin:$PATH"
    ```

=== "wget"

    ```sh
    wget --https-only -O install-zuku-cli.sh https://zuzunza.com/install.sh && bash install-zuku-cli.sh
    export PATH="$HOME/.local/bin:$PATH"
    ```

=== "PowerShell"

    ```powershell
    & ([scriptblock]::Create((irm 'https://zuzunza.com/install.ps1')))
    ```

`zuku` and `zukujs` are the same CLI. Both share configuration and authentication. Other installation methods are in [Installation](installation.md).

## Run your first game

```sh
zuku create my-game
cd my-game
zuku run
```

Open the local URL printed in your terminal. Press Space or tap to jump over obstacles. Stop the preview with `Ctrl+C`.

[Step-by-step quickstart](getting-started.md) · [CLI commands](cli/commands.md) · [Package and publish](cli/publishing.md)
