---
title: ZUKU Studio
description: CLI와 같은 런타임과 Agent Core를 사용하는 데스크톱 Studio의 실행 방법과 현재 지원 상태입니다.
section: Guide
---

# ZUKU Studio

ZUKU Studio는 CLI의 기능을 그래픽 화면에서 사용하는 데스크톱 앱입니다. 별도의 제품이 아니며 두 번째 CLI, 에이전트, Node.js 런타임을 따로 갖고 있지 않습니다. Studio는 설치된 CLI와 같은 관리형 Node.js 22.22.3 런타임, 같은 Agent Core, 같은 설정과 로그인 상태(`~/.config/zukujs/`(Windows: `%LOCALAPPDATA%\ZukuJS\`))를 사용합니다.

## 실행

다음 명령은 공식 로컬 브라우저 화면(`https://ai.zuzunza.com`)을 같은 Agent Core에 연결하는 루프백 어댑터를 시작합니다. 네이티브 데스크톱 창을 여는 명령은 아닙니다.

```sh
zuku studio
```

`zukujs studio`도 같은 어댑터와 Agent Core를 사용합니다. `--port <n>`으로 기본 포트 `43127`을 바꿀 수 있습니다. 연결, 세션 재개, 로그인 요청은 실행 중인 터미널에서 승인합니다. `Ctrl+C`는 어댑터를 종료하며 진행 중인 Core 세션을 취소하지 않습니다.

네이티브 Studio는 설치된 플랫폼 앱을 실행하는 별도 화면입니다. 프로젝트 폴더는 운영체제의 선택 창에서 승인합니다. 브라우저 연결도 같은 로컬 Agent Core를 사용하며, 호스팅 웹 AI는 현재 공개되어 있지 않습니다.

## 설치 방식

Studio는 공식 설치 스크립트로 설치합니다. 설치 방법은 [설치](../installation.md)를 참고하세요.

- Studio는 CLI 패키지와, 플랫폼별로 컴파일된 작은 네이티브 셸로 구성됩니다.
- 설치 스크립트는 네이티브 파일의 SHA-256을 고정된 릴리스 값과 비교하고, 설치된 CLI와 소스·프로토콜 버전이 맞는지 확인한 뒤 설치합니다.
- 해당 플랫폼에 검증된 Studio 파일이 없으면 설치 전에 오류를 표시합니다.
- Studio가 포함된 릴리스에서는 관리형 런타임을 항상 함께 설치하므로 `--no-node`(PowerShell `-NoNode`)를 사용할 수 없습니다.

네이티브 셸은 설치된 릴리스의 관리형 Node.js로 CLI의 Studio 호스트만 실행하고, 같은 릴리스에 포함된 신뢰된 화면 파일만 불러옵니다. 셸 명령을 실행하거나 게임·`zuku://` 주소에서 받은 경로를 사용하지 않습니다.

## 플랫폼과 요구 사항

| 플랫폼 | 네이티브 셸 | 요구 사항 |
| --- | --- | --- |
| Linux x64, arm64 | C, GTK 3 + WebKitGTK 4.1 | 그래픽 데스크톱과 GTK 3, WebKitGTK 4.1 시스템 라이브러리 |
| macOS x64, arm64 | Swift (`ZUKU Studio.app`) | |
| Windows x64, arm64 | .NET 10 WPF (자체 포함) | WebView2 Evergreen 런타임(별도) |

설치 스크립트는 시스템 패키지를 설치하거나 관리자 권한을 요청하지 않습니다. Linux에서 GTK나 WebKitGTK 라이브러리가 없다면 직접 설치해야 합니다.

## 현재 상태

Studio 네이티브 셸은 위 여섯 플랫폼용으로 컴파일되었습니다. 다만 검증 범위는 플랫폼마다 다릅니다.

- **Linux**: 실제 GTK/WebKit 화면, 공유 Agent Core, 설치 위치 확인, 미리보기 동작을 확인했습니다.
- **macOS**: 개발용 임시(ad-hoc) 서명만 되어 있으며 Developer ID 서명과 공증(notarization)은 되어 있지 않습니다. 실제 GUI 동작 전체 검증은 아직 완료되지 않았습니다.
- **Windows**: 실제 GUI 동작 전체 검증은 아직 완료되지 않았습니다. .NET이 미리 설치되지 않은 환경과 WebView2 유무에 따른 동작도 별도로 확인해야 합니다.

`zuku://ai/connect` 주소 등록, 단일 인스턴스 실행, 자동 업데이트, 제거는 운영체제별 설치 작업으로 남아 있습니다.

macOS나 Windows에서 Studio가 실행되지 않으면 같은 기능을 CLI로 사용할 수 있습니다. 기본 명령은 [CLI 개요](index.md)와 [명령 참조](commands.md)를, 게임 개발 에이전트는 [에이전트](agent.md)를 보세요.
