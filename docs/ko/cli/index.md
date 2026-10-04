---
title: ZUKU CLI 개요
description: zuku 명령으로 터미널에서 게임을 만들고, 실행하고, 검사하고, 패키지로 만드는 방법을 소개합니다.
section: Guide
---

# ZUKU CLI 개요

ZUKU CLI는 터미널에서 ZUKU 게임을 만들고, 로컬에서 실행해 보고, 검사하고, 업로드할 수 있는 패키지로 만드는 도구입니다. 현재 버전은 `0.3.0`입니다.

## `zuku`와 `zukujs`

CLI는 `zuku`와 `zukujs` 두 이름으로 설치됩니다. 두 이름은 별칭일 뿐이며 같은 런타임, 같은 설정, 같은 로그인 정보, 같은 상태(`~/.config/zukujs/`(Windows: `%LOCALAPPDATA%\ZukuJS\`))를 공유합니다. 한쪽에서 로그인하면 다른 쪽에서도 로그인된 상태입니다.

처음 시작한다면 짧은 `zuku`를 사용하세요. 이 문서도 `zuku`를 기준으로 설명합니다.

```sh
zuku --version
zukujs --version   # 같은 CLI입니다
```

## 설치

공식 설치 스크립트로 설치합니다. 설치 스크립트가 CLI와 관리형 Node.js 22.22.3 런타임을 사용자 디렉터리에 함께 설치합니다. 자세한 방법은 [설치](../installation.md)를 참고하세요.

> `@zukujs/cli`는 npm 레지스트리에 게시되어 있지 않습니다. `npm install -g @zukujs/cli`로는 설치할 수 없습니다.

## 기본 흐름

게임 하나를 만드는 기본 흐름은 `create` → `run` → `validate` → `package`입니다.

```sh
zuku create my-game          # 새 프로젝트 만들기
cd my-game
zuku run                     # 로컬 미리보기 (Ctrl+C로 종료)
zuku validate .              # 프로젝트 검사
zuku package . --format zwf  # dist/에 .zwf 패키지 만들기
```

- `create`는 바로 플레이할 수 있는 Canvas JUMP 장애물 러너 게임을 만듭니다. 스페이스 키나 화면 탭으로 점프합니다.
- `run`은 현재 폴더의 게임을 `127.0.0.1`에서 미리보기로 띄웁니다.
- `validate`와 `package`는 네트워크를 사용하지 않습니다.

처음부터 따라 해 보려면 [시작하기](../getting-started.md)를, 모든 명령과 플래그는 [명령 참조](commands.md)를 보세요. 다른 시작 예제는 [스타터](../starters/index.md)에 있습니다.

## 인증: 계정과 모델 제공자

CLI에는 두 종류의 인증이 있습니다. 서로 다른 목적이므로 구분해 두세요.

| 종류 | 용도 | 문서 |
| --- | --- | --- |
| ZUKU 계정 | 업로드, 게시, 게시 한도 확인 | [인증](authentication.md) |
| 모델 제공자 | 게임 개발 에이전트가 사용할 AI 모델 연결 | [제공자](providers.md), [모델](models.md) |

공식 ZUKU AI 제공자는 `zuku/auto`이며, 사용할 수 있는 모델 목록은 동적으로 바뀝니다.

## 게임 개발 에이전트

`zuku agent`는 한 줄 요청으로 게임을 설계하고 구현한 뒤, 실제 브라우저에서 플레이테스트하고 패키지까지 만드는 로컬 에이전트입니다. 기본 실행은 패키지에서 멈추며 게시하지 않습니다. `--draft`는 초안만 업로드하고, `--yolo`를 명시해야 한 번에 프로덕션 게시까지 진행합니다. 자세한 내용은 [에이전트](agent.md)를 보세요.

## 업로드와 게시

- `zuku upload`는 패키지를 올리고 **초안**을 만듭니다. 공개하지 않습니다.
- 프로덕션 게시는 명시적으로 요청해야 하며, ZUKU 계정당 최근 6시간 동안 성공한 게시 3회로 제한됩니다.

자세한 내용은 [게시](publishing.md)를 보세요.

## 데스크톱 Studio

같은 런타임과 Agent Core를 그래픽 화면에서 사용하는 데스크톱 앱입니다. 현재 상태와 실행 방법은 [Studio](studio.md)를 보세요.

## 문제가 생겼을 때

명령이 실패하면 오류 코드를 확인하고 [오류](../errors.md) 문서를 참고하세요. 로컬 설정 상태는 다음 명령으로 확인할 수 있습니다.

```sh
zuku status
```
