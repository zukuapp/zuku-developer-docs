---
title: ZUKU Studio
description: CLI와 같은 런타임과 Agent Core를 사용하는 데스크톱 Studio의 실행 방법과 플랫폼별 요구 사항입니다.
section: Guide
---

# ZUKU Studio

ZUKU Studio는 CLI의 기능을 그래픽 화면에서 사용하는 데스크톱 앱입니다. Studio는 설치된 CLI와 같은 관리형 Node.js 22.22.3 런타임, 같은 Agent Core, 같은 설정과 로그인 상태(`~/.config/zukujs/`(Windows: `%LOCALAPPDATA%\ZukuJS\`))를 사용합니다.

## 실행

다음 명령은 공식 로컬 브라우저 화면(`https://ai.zuzunza.com`)을 같은 Agent Core에 연결하는 루프백 어댑터를 시작합니다. 네이티브 데스크톱 창을 여는 명령은 아닙니다.

```sh
zuku studio
```

`zukujs studio`도 같은 어댑터와 Agent Core를 사용합니다. `--port <n>`은 기본 포트 `43127`을 바꿉니다. 연결, 세션 재개, 로그인 요청은 실행 중인 터미널에서 승인합니다. `Ctrl+C`는 어댑터를 종료하며 진행 중인 Core 세션을 취소하지 않습니다.

네이티브 Studio는 설치된 플랫폼 앱을 실행하는 별도 화면입니다. 프로젝트 폴더는 운영체제의 선택 창에서 승인합니다.

## 설치 방식

Studio는 공식 설치 스크립트로 설치합니다. 설치 절차는 [설치](../installation.md)에 있습니다.

- Studio는 CLI 패키지와, 플랫폼별로 컴파일된 작은 네이티브 셸로 구성됩니다.
- 설치 스크립트는 네이티브 파일의 SHA-256을 고정된 릴리스 값과 비교하고, 설치된 CLI와 소스·프로토콜 버전이 맞는지 확인한 뒤 설치합니다.
- 해당 플랫폼에 검증된 Studio 파일이 없으면 설치 전에 오류를 표시합니다.
- Studio가 포함된 릴리스에서는 관리형 런타임을 항상 함께 설치하므로 `--no-node`(PowerShell `-NoNode`)를 사용할 수 없습니다.

## 플랫폼과 요구 사항

| 플랫폼 | 네이티브 셸 | 요구 사항 |
| --- | --- | --- |
| Linux x64, arm64 | C, GTK 3 + WebKitGTK 4.1 | 그래픽 데스크톱과 GTK 3, WebKitGTK 4.1 시스템 라이브러리 |
| macOS x64, arm64 | Swift (`ZUKU Studio.app`) | |
| Windows x64, arm64 | .NET 10 WPF (자체 포함) | WebView2 Evergreen 런타임(별도) |

Linux에서는 GTK 3와 WebKitGTK 4.1 시스템 라이브러리를 직접 설치합니다. macOS 빌드는 개발용 임시(ad-hoc) 서명만 되어 있으며 Developer ID 서명과 공증(notarization)이 없습니다.

Studio의 기능은 CLI에서도 제공됩니다. 기본 명령은 [CLI 개요](index.md)와 [명령 참조](commands.md)에, 게임 개발 에이전트는 [에이전트](agent.md)에 있습니다.
