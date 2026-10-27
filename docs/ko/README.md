---
title: 첫 게임 만들기
description: curl 또는 wget으로 ZUKU CLI를 설치하고 실행 가능한 Starter로 첫 게임을 만듭니다.
section: 시작하기
---

<span id="첫-게임을-만들어-보세요"></span>

# 첫 게임 만들기

**ZUKU - 내가 불러 일으키는 새로운 창작.**

ZUKU CLI를 설치하고 Starter를 골라 플레이 가능한 게임을 만듭니다.

## ZUKU CLI 설치

설치 도구가 Node.js를 함께 준비합니다. 사용 중인 터미널에 맞는 명령을 실행합니다.

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

`zuku`와 `zukujs`는 같은 CLI입니다. 두 명령은 설정과 로그인 상태를 공유합니다. 다른 설치 방법은 [설치](installation.md)에 있습니다.

<span id="바로-실행해-보기"></span>

## 바로 실행하기

```sh
zuku create my-game
cd my-game
zuku run
```

터미널에 표시된 로컬 주소를 브라우저에서 엽니다. 스페이스바 또는 탭으로 장애물을 피하는 작은 게임이 실행됩니다. 종료는 `Ctrl+C`입니다.

[단계별 빠른 시작](getting-started.md) · [CLI 명령어](cli/commands.md) · [패키징과 게시](cli/publishing.md)
