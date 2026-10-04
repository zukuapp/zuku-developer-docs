---
title: Installation
description: Install the ZukuJS CLI on macOS, Linux, or Windows, verify it, and fix common setup issues.
section: Guide
---

# Installation

The ZukuJS CLI 0.3.0 installs with a single command. The installer downloads a fixed-version CLI archive over HTTPS, checks its SHA-256 against the pinned release value, and sets up a managed Node.js 22 runtime in your user directory. It never replaces your system Node.js and does not need administrator rights.

Supported platforms: macOS and Linux (x64, arm64) and Windows (x64, arm64).

> The CLI is **not** published on npm. `npm install -g @zukujs/cli` will not work. Use the installer below.

## macOS and Linux

Download the installer with curl or wget, then run it with Bash.

**curl**

```sh
curl -fsSL --proto '=https' --tlsv1.2 https://zuzunza.com/install.sh -o install-zuku-cli.sh && bash install-zuku-cli.sh
```

**wget**

```sh
wget --https-only -O install-zuku-cli.sh https://zuzunza.com/install.sh && bash install-zuku-cli.sh
```

By default the CLI is installed to `~/.local/share/zukujs`, with the commands `~/.local/bin/zuku` and `~/.local/bin/zukujs`.

## Windows (PowerShell)

```powershell
& ([scriptblock]::Create((irm 'https://zuzunza.com/install.ps1')))
```

By default the CLI is installed to `%LOCALAPPDATA%\ZukuJS`, with `bin\zuku.cmd` and `bin\zukujs.cmd`. The installer adds that `bin` folder to the PATH of the current PowerShell session. No PowerShell profile changes are made.

## Verify the install

```sh
zuku --version
```

Then try the full local flow:

```sh
zuku create my-game
zukujs validate my-game
```

`zuku` and `zukujs` are the same CLI. Both names share one runtime, configuration, and login state in `~/.config/zukujs/` (Windows: `%LOCALAPPDATA%\ZukuJS\`).

## Installer options

| Bash | PowerShell | What it does |
| --- | --- | --- |
| `--prefix /absolute/path` | `-Prefix 'C:\absolute\path'` | Install into a directory you own; commands go in its `bin` folder |
| `--no-node` | `-NoNode` | Use an existing Node.js 22+ and npm (CLI-only releases) |
| `--dry-run` | `-DryRun` | Show the install plan without downloading or writing anything |
| `--help` | `-Help` | Show installer help |

Quote paths that contain spaces:

```sh
bash install-zuku-cli.sh --prefix "$HOME/Tools/ZukuJS CLI" --dry-run
```

```powershell
& ([scriptblock]::Create((irm 'https://zuzunza.com/install.ps1'))) -Prefix "$env:LOCALAPPDATA\Tools\ZukuJS CLI" -DryRun
```

Releases that include Studio always use the bundled Node.js 22 runtime; passing `--no-node` or `-NoNode` with them stops with an error before anything is installed.

For manual inspection, the fixed release archive is available at `https://zuzunza.com/downloads/zukujs/cli/0.3.0/zukujs-cli-0.3.0.tgz`. The installer is the supported way to set it up.

## Updating or reinstalling

Run the same install command again. It reuses the same install location. If a download check or the post-install check fails, your previous install and both command names are kept or restored.

## Troubleshooting

**`zuku: command not found` (macOS/Linux)**

The installer does not edit your shell configuration. Add the `bin` folder to PATH for the current terminal:

```sh
export PATH="$HOME/.local/bin:$PATH"
zuku --version
```

To make it permanent, add the same `export` line to your shell's startup file (for example `~/.bashrc` or `~/.zshrc`). If you used `--prefix`, add `<prefix>/bin` instead.

**`zuku` not found in a new Windows terminal**

Add `%LOCALAPPDATA%\ZukuJS\bin` to **User environment variables > Path**, then open a new terminal.

**Node.js version conflicts**

You don't need to install or upgrade Node.js yourself. The CLI uses its own managed Node.js 22 runtime, independent of any system or version-manager Node.js. On Linux, your system must be able to run the official Node.js binaries.

**Install stops because `zuku` already exists**

The installer won't overwrite a `zuku` or `zukujs` command that belongs to another program. Choose a different location with `--prefix` or `-Prefix`.

**Linux Studio**

Studio on Linux needs a graphical desktop plus the GTK 3 and WebKitGTK 4.1 system libraries. The installer does not install system packages.

## Next steps

- [Getting Started](getting-started.md): create and run the starter game
- [Command reference](cli/commands.md): every command and flag
- [Errors](errors.md): what error codes mean
