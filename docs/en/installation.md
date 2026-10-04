---
title: Installation
description: Install the ZukuJS CLI on macOS, Linux, or Windows, verify it, and fix common setup issues.
section: Guide
---

# Installation

The managed installer currently provides the pinned CLI 0.3.0 release. The installer downloads a fixed-version CLI archive over HTTPS, checks its SHA-256 against the pinned release value, and sets up a managed Node.js 22 runtime in your user directory. It never replaces your system Node.js and does not need administrator rights.

Supported platforms: macOS and Linux (x64, arm64) and Windows (x64, arm64).

> Use the exact npm package names in the public release table below. The managed installer continues to provide its existing pinned release.

<!-- BEGIN ZUKU NPM DISTRIBUTIONS -->
## npm packages for game development

These exact names and versions were verified in the public npm registry on 2026-10-04. Install the packages your project needs.

| Package | Version | Purpose |
| --- | --- | --- |
| [@zuku/zwf](https://www.npmjs.com/package/@zuku/zwf/v/0.1.1) | `0.1.1` | ZWF2 HTML5 ZIP game package reading and writing |
| [@zuku/sdk](https://www.npmjs.com/package/@zuku/sdk/v/0.2.0) | `0.2.0` | ZUKU API and game bridge |
| [zuku-engine-next2d](https://www.npmjs.com/package/zuku-engine-next2d/v/0.1.1) | `0.1.1` | Jump engine integration and game package validation |
| [@zuku/zwf-runtime](https://www.npmjs.com/package/@zuku/zwf-runtime/v/0.1.2) | `0.1.2` | ZWF1 animation WebAssembly runtime and host loader |
| [@zuku/lang](https://www.npmjs.com/package/@zuku/lang/v/0.1.0) | `0.1.0` | Validated JSON resources for 20 locales |
| [@zuku/core](https://www.npmjs.com/package/@zuku/core/v/27.0.1) | `27.0.1` | Command parsing, diagnostics and redaction |
| [@zuku/player](https://www.npmjs.com/package/@zuku/player/v/0.1.1) | `0.1.1` | Browser player from the maintained Next2D fork |
| [@zuku/editor](https://www.npmjs.com/package/@zuku/editor/v/0.1.1) | `0.1.1` | Browser editor and embedding helper |
| [@zuku/cli](https://www.npmjs.com/package/@zuku/cli/v/0.3.1) | `0.3.1` | Shared zuku and zukujs commands |

```sh
npm install --save-exact @zuku/zwf@0.1.1 @zuku/sdk@0.2.0 zuku-engine-next2d@0.1.1 @zuku/zwf-runtime@0.1.2 @zuku/lang@0.1.0 @zuku/core@27.0.1 @zuku/player@0.1.1 @zuku/editor@0.1.1
```

Resource exports include JSON such as `@zuku/lang/locales/ko.json` and WebAssembly at `@zuku/zwf-runtime/wasm`. For browser projects, use an ESM bundler and follow each package's host instructions.

ZWF2 packages HTML5 ZIP games; ZWF1 stores animations. Use the package and loader for the appropriate format.

Each package retains its original license notice. The existing `UNLICENSED` declaration for `@zuku/core` is preserved. The Next.js server framework and operational servers are excluded from this game-library release.

### Install the CLI from npm

Use Node.js 22 or later with npm, then run:

```sh
npm install -g @zuku/cli@0.3.1
zuku --version
zukujs --version
```

`zuku` and `zukujs` share the same CLI, login, configuration and Agent Core state. The npm CLI 0.3.1 and the managed installer's pinned 0.3.0 release below have separate distribution paths.
<!-- END ZUKU NPM DISTRIBUTIONS -->

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

The managed installer supplies its own Node.js 22 runtime without changing your system Node.js. On Linux, the system must be able to run the official Node.js binaries. Installing the CLI from npm uses Node.js 22 or later from your own environment.

**Install stops because `zuku` already exists**

The installer won't overwrite a `zuku` or `zukujs` command that belongs to another program. Choose a different location with `--prefix` or `-Prefix`.

**Linux Studio**

Studio on Linux needs a graphical desktop plus the GTK 3 and WebKitGTK 4.1 system libraries. The installer does not install system packages.

## Next steps

- [Getting Started](getting-started.md): create and run the starter game
- [Command reference](cli/commands.md): every command and flag
- [Errors](errors.md): what error codes mean
