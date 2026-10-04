---
title: ZUKU Studio
description: The ZUKU Studio desktop app, how it shares the CLI runtime and Agent Core, and its current platform status.
section: Guide
---

# ZUKU Studio

ZUKU Studio is a desktop workspace for making games with the same local Agent Core that `zuku` and `zukujs` use. It isn't a second product. It has no separate CLI, agent or Node.js runtime. Studio is a native window around the renderer that ships inside the CLI package.

## How Studio relates to the CLI

Studio and the CLI are two front ends to one installation:

| Piece | Shared by CLI and Studio |
| --- | --- |
| Runtime | One managed Node.js 22.22.3, installed by the official installer |
| Agent Core | The same per-user Core runs sessions for both |
| Settings and sign-in | The same providers, models, credentials and session history in `~/.config/zukujs/` (Windows: `%LOCALAPPDATA%\ZukuJS\`) |
| Studio UI | Bundled in the CLI package. The native shell only loads these trusted files. |

The native shell starts the Studio host from the installed CLI with the managed runtime. It never runs shell commands, and it never takes file paths from the UI, a game or a link. As a result:

- A provider you add with `zuku provider add` appears in Studio, and the other way round.
- A session started in Studio can be inspected from the CLI, and closing the window doesn't cancel running Core work.
- Signing out with `zuku auth logout` or `zuku account logout` applies everywhere.

Inside Studio you open a project with your operating system's folder picker. Approvals for web connections and provider sign-in appear in separate native dialogs, and they default to **deny**. Experimental sign-in methods are marked `(exp!)`. Game previews show a fixed snapshot from Agent Core in an isolated view that can't reach the native bridge or sign-in dialogs.

The workspace has a project and session list, a game stage with Build, Test, Run, Stop and Preview, tabs for source, changes, logs and providers, and a chat panel for the agent.

## Platform status

Studio's native shell is compiled for six targets:

| Platform | Targets | Native technology |
| --- | --- | --- |
| Linux | `linux-x64`, `linux-arm64` | C with GTK 3 and WebKitGTK 4.1 |
| macOS | `darwin-x64`, `darwin-arm64` | Swift app bundle (`ZUKU Studio.app`) |
| Windows | `win-x64`, `win-arm64` | .NET WPF, self-contained, with WebView2 |

Native builds and self-tests passing doesn't mean the GUI has been checked on every system:

- **Linux**: the real window has been run as a normal desktop user, including folder picking, sessions, events and game preview, with the browser sandbox enabled.
- **macOS and Windows**: full GUI verification hasn't been completed. The macOS build has only an ad-hoc development signature. It isn't Developer ID signed or notarized. The Windows build still needs real-world GUI checks, including systems without .NET and the different WebView2 availability cases.

Linux requires a graphical desktop session and the GTK 3 and WebKitGTK 4.1 system libraries. The x64 build also requires glibc 2.34 or later. The installer doesn't install system packages or ask for administrator rights.

## Getting Studio

Studio is delivered through the official installer, not as a separate download, and not through npm. Install the CLI as described in [Installation](../installation.md). For releases that include Studio, the installer:

1. installs the managed Node.js 22.22.3 runtime (in these releases, `--no-node` / `-NoNode` is an error),
2. downloads the native Studio asset for your platform and checks its SHA-256 against the pinned release values,
3. confirms that Studio matches the installed CLI's version and protocol, and
4. stops before installing if no verified asset exists for your platform.

Your existing CLI and both command names are kept or restored if any step fails.

## Using the CLI with a browser instead

`zuku studio` doesn't open the desktop window. It starts a local browser adapter on `127.0.0.1` for the official local browser frontend at `https://ai.zuzunza.com`, backed by the same Agent Core:

```sh
# Start the local adapter; approve pairing requests in this terminal
zuku studio

# Use a different port
zuku studio --port 43200
```

Pairing, session resume and sign-in requests must be approved in the terminal. Press Ctrl+C to stop the adapter. Running sessions are not cancelled. Hosted web AI access is currently closed. For everyday work, the CLI commands in the [command reference](commands.md) remain the primary, fully supported path.

## Related

- [ZUKU CLI overview](index.md)
- [Game agent](agent.md)
- [Providers](providers.md) and [Authentication](authentication.md)
