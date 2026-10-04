---
title: 첫 게임을 만들어 보세요
description: curl 또는 wget으로 ZUKU CLI를 설치하고, 실행 가능한 Starter로 첫 게임을 만드세요.
section: 시작하기
---

# 첫 게임을 만들어 보세요.

**ZUKU - 내가 불러 일으키는 새로운 창작.**

아이디어에서 플레이 가능한 게임까지. ZUKU CLI를 설치하고, 마음에 드는 Starter를 골라 바로 시작하세요.

## ZUKU CLI 설치

Node.js는 설치 도구가 함께 준비합니다. 사용 중인 터미널의 명령을 복사해 실행하세요.

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

`zuku`와 `zukujs`는 같은 CLI입니다. 설정과 로그인 상태도 함께 사용합니다. [다른 설치 옵션](installation.md)을 확인하세요.

## 바로 실행해 보기

```sh
zuku create my-game
cd my-game
zuku run
```

터미널에 표시된 로컬 주소를 브라우저에서 열어 보세요. 스페이스바 또는 탭으로 장애물을 피하는 작은 게임이 준비됩니다. 종료는 `Ctrl+C`입니다.

[단계별 빠른 시작](getting-started.md) · [CLI 명령어](cli/commands.md) · [패키징과 게시](cli/publishing.md)
