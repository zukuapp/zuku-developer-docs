---
title: 명령 참조
description: ZUKU CLI 0.3.0의 모든 명령, 인수, 플래그, 출력 형식과 종료 코드입니다.
section: Reference
---

# 명령 참조

`zuku`와 `zukujs`는 같은 CLI입니다(`@zukujs/cli` 0.3.0). 두 이름은 같은 런타임, 설정, 인증, 상태(`~/.config/zukujs/`(Windows: `%LOCALAPPDATA%\ZukuJS\`))를 공유하므로 아래 예시의 `zuku`를 `zukujs`로 바꿔 써도 결과가 같습니다.

대부분의 명령은 `--json`을 붙이면 `zuku-command/1` 형식으로 출력합니다. [출력 형식](#출력-형식-zuku-command1)을 참고하세요.

## 명령 요약

| 명령 | 네트워크 | 설명 |
| --- | --- | --- |
| `zuku help` (`--help`, `-h`) | 없음 | 명령 안내 |
| `zuku version` (`--version`, `-v`) | 없음 | ZukuJS 런타임 버전과 CLI 버전 |
| `zuku status`, `zuku diagnostics` | 없음 | 로컬 설정과 자격 증명 상태 |
| `zuku status --check-api` | 읽기 전용 GET | 공개 목록과 (토큰이 있으면) 사용자 인증 확인 |
| `zuku create <name>` | 없음 | 새 프로젝트 만들기 |
| `zuku run` | 없음 (로컬 루프백만) | 현재 폴더의 게임을 로컬에서 미리보기 |
| `zuku validate <path>` | 없음 | 프로젝트 디렉터리 또는 `.zwf`/`.zip` 검사 |
| `zuku package <dir>` | 없음 | 재현 가능한 `.zwf`/`.zip` 만들기 |
| `zuku upload <path>` | 업로드, 초안 생성 | 패키지를 올리고 초안 JUMP 콘텐츠 만들기 |

에이전트, 계정, 제공자, 모델, Studio 명령은 [그 밖의 명령](#그-밖의-명령)에 정리했습니다.

## help

```sh
zuku help
zuku --help
zuku -h
```

사용할 수 있는 명령을 안내합니다.

## version

```sh
zuku version
zuku --version
zuku -v
```

ZukuJS 런타임 버전과 CLI 버전을 출력합니다.

## create

```sh
zuku create <name>
```

현재 디렉터리 아래에 새 프로젝트 디렉터리 `<name>/`을 만듭니다.

| 인수 | 설명 |
| --- | --- |
| `<name>` | 소문자 영문, 숫자, `_`, `-`만 사용, 최대 64자 |

`create`는 `<name>` 외의 옵션을 받지 않습니다. 템플릿을 고르는 플래그는 없습니다.

만들어지는 결과물은 바로 플레이할 수 있는 **Canvas JUMP 장애물 러너** 게임입니다. 스페이스 키나 화면 탭으로 점프해 장애물을 피합니다.

| 파일 | 내용 |
| --- | --- |
| `zukujs.json` | 프로젝트 매니페스트(`zukujs-project/1`) |
| `src/index.html` | 진입점 |
| `src/game.js` | 게임 코드 |
| `README.md` | 프로젝트 안내 |
| `.gitignore` | 출력물과 로컬 파일 제외 |

생성된 `zukujs.json`의 기본값은 버전 `0.1.0`, 패키지 형식 `zwf`, 소스 디렉터리 `src`, 진입 파일 `index.html`, 지원 플랫폼 PC·모바일·태블릿입니다.

같은 이름의 경로가 이미 있으면 아무것도 덮어쓰지 않고 `PROJECT_EXISTS`로 실패합니다. 이름 규칙에 맞지 않으면 `INVALID_INPUT`으로 실패합니다.

```sh
zuku create my-game
```

## run

```sh
zuku run [--port <n>] [--once]
```

현재 폴더의 ZUKU 게임을 읽기 전용 스냅숏으로 만들어 `127.0.0.1`에서 미리보기로 제공합니다. Ctrl+C를 누를 때까지 실행되며, 미리보기 주소는 stderr에 표시됩니다.

| 플래그 | 기본값 | 설명 |
| --- | --- | --- |
| `--port <n>` | `0` (임의 포트) | 미리보기 서버 포트, `0`–`65535` |
| `--once` | 꺼짐 | 서버를 띄우지 않고 미리보기 메타데이터(프로젝트·미리보기 핸들, 버전, 진입 파일, 소스 SHA-256)만 반환 |

포트 값이 숫자가 아니거나 범위를 벗어나면 `INVALID_INPUT`으로 실패합니다.

```sh
cd my-game
zuku run
zuku run --port 8080
zuku run --once --json
```

## validate

```sh
zuku validate <dir | file.zwf | file.zip>
```

- **디렉터리**: `zukujs.json`을 정규화하고 소스 파일을 패키지 규칙으로 검사합니다.
- **`.zwf`/`.zip`**: 공개 ZWF 검증 규칙으로 패키지를 검사합니다.
- 프로젝트 코드를 실행하지 않습니다.

```sh
zuku validate .                 # 프로젝트 디렉터리
zuku validate dist/game.zwf     # 패키지 파일
```

## package

```sh
zuku package <dir> [--format zwf|zip] [--output <file> | -o <file>] [--force]
```

| 플래그 | 기본값 | 설명 |
| --- | --- | --- |
| `--format` | 매니페스트 값, 없으면 `zwf` | 출력 형식(`zwf` 또는 `zip`). 명시한 플래그가 매니페스트의 `package.format`보다 우선합니다 |
| `--output`, `-o` | `dist/<name>-<version>.<format>` | 출력 파일 경로 |
| `--force` | 꺼짐 | 기존 출력 파일 덮어쓰기 |

경로를 정렬하고 고정 타임스탬프를 사용하므로 같은 입력에서 항상 같은 바이트가 나옵니다. 심볼릭 링크, 하드 링크, 경로 탈출, 특수 파일, 네이티브 실행 파일, 대소문자 충돌, 압축 해제 한도를 넘는 아카이브는 거부합니다. 프로젝트 코드나 빌드 명령은 실행하지 않습니다.

```sh
zuku package . --format zwf
zuku package . --format zip -o build/game.zip --force
```

## upload

```sh
zuku upload <dir | file.zwf | file.zip> [옵션]
```

| 플래그 | 설명 |
| --- | --- |
| `--title <text>` | 제목(1–100자) |
| `--description <text>` | 설명(500자 이하) |
| `--game-id <id>` | `jump.game_id`(클라이언트 메타데이터이며 콘텐츠 ID가 아님) |
| `--genre <genre>` | `jump.genre` |
| `--version <version>` | 패키지 버전(`jump.package.version`) |
| `--age-rating all\|12\|15\|18` | 연령 등급 |
| `--tag <tag>` | 태그. 여러 번 지정 가능, 최대 10개 |
| `--platform pc,mobile,tablet` | 실제로 지원하는 플랫폼(쉼표로 구분) |
| `--receipt-dir <dir>` | 영수증 디렉터리(기본 `.zukujs/receipts`) |
| `--verify` | 생성 후 소유자 권한으로 초안을 다시 조회해 확인 |

- 디렉터리를 주면 `package`와 같은 코어로 패키지를 만든 뒤 업로드합니다. 메타데이터는 정규화된 `zukujs.json`에서 가져오며, 플래그가 있으면 플래그가 우선합니다.
- `upload`는 **초안만** 만들고 공개하지 않습니다. 초안은 공개 목록에 나타나지 않지만 업로드된 `/uploads/...` 파일 URL은 공개 주소이므로, 공개되어도 괜찮은 파일만 올리세요.
- 업로드에는 ZUKU 계정 로그인이 필요합니다. [인증](authentication.md)을 참고하세요.
- 변경 요청은 자동으로 재시도하지 않습니다. 결과가 불확실하면 영수증에 기록되므로, 다시 실행하기 전에 초안이 이미 만들어졌는지 확인하세요.

```sh
zuku upload .
zuku upload dist/my-game-0.1.0.zwf --title "My Game" --platform pc,mobile --tag arcade --verify
```

게시 흐름은 [게시](publishing.md)에서 설명합니다.

## status / diagnostics

```sh
zuku status [--check-api]
zuku diagnostics
```

기본 실행은 네트워크 없이 런타임과 CLI 버전, API 주소, 자격 증명 설정 여부를 보여 줍니다. 네트워크는 쓰지 않지만 자격 증명 파일은 읽으므로, 지정한 자격 증명 파일이 없거나 규칙에 맞지 않으면 오프라인에서도 실패합니다.

| 플래그 | 설명 |
| --- | --- |
| `--check-api` | `GET /billing/catalog`(익명)과, 토큰이 있으면 `GET /auth/me`를 호출해 연결과 인증을 확인 |

계정 ID, 이메일, 토큰은 출력하지 않습니다.

## 그 밖의 명령

아래 명령은 각 문서에서 자세히 설명합니다.

### 게임 개발 에이전트

```sh
zuku agent "<요청>" [--name <name>] [--model <id>] [--experimental] [--draft | --yolo]
zuku agent --resume <run_id> [--yolo | --draft]
```

`--browser`는 현재 Agent Core에 전달할 수 없어 `CORE_PROTOCOL_GAP`로 실패합니다. Codex나 사용자 지정 제공자를 사용하는 세션에는 `--experimental`을 명시하세요.

기본 실행은 패키지까지 만들고 게시하지 않습니다. `--draft`는 초안만 업로드하고, `--yolo`는 명시적으로 한 번 프로덕션 게시까지 진행합니다. `--draft`와 `--yolo`는 함께 쓸 수 없습니다. [에이전트](agent.md)

### 계정 로그인과 게시

```sh
zuku login zuku
zuku login codex --experimental
zuku account --quota
zuku account logout
zuku deploy <dir> --yolo
```

`zuku login codex --experimental`은 CLI의 Codex 로그인 연동으로, **실험적(Experimental)이며 비공식** 연동입니다. 이 표시는 CLI 연동에 대한 것이며 Codex 서비스 자체를 말하는 것이 아닙니다. 게시는 ZUKU 계정당 최근 6시간 동안 성공한 프로덕션 게시 3회로 제한됩니다. [인증](authentication.md), [게시](publishing.md)

### 모델 제공자 인증

```sh
zuku auth list [--provider <id>]
zuku auth login [--provider <id>] [옵션]
zuku auth logout [--provider <id>]
```

[인증](authentication.md)

### 제공자

```sh
zuku provider list
zuku provider show <id>
zuku provider use <id>
zuku provider add [옵션]
zuku provider configure <id> [옵션]
zuku provider enable <id>
zuku provider disable <id>
zuku provider remove <id> --yes
```

[제공자](providers.md)

### 모델

```sh
zuku model list [--provider <id>] [--refresh]
zuku model refresh [--provider <id>]
zuku model use <provider/model>
zuku model info [<provider/model>] [--refresh]
zuku model current
```

공식 ZUKU AI 제공자의 기본 모델은 `zuku/auto`이며 모델 목록은 동적으로 조회됩니다. [모델](models.md)

### Studio

```sh
zuku studio
```

`127.0.0.1`에서 공식 로컬 브라우저 화면(`https://ai.zuzunza.com`)용 어댑터를 시작합니다. 네이티브 데스크톱 창을 여는 명령은 아닙니다. [Studio](studio.md)

## 웹 프레임워크 명령

프로젝트에 프레임워크 패키지 `zukujs`가 설치되어 있으면 `dev`, `build`, `start`, `info`, `analyze`, `typegen`, `telemetry`, `upgrade`와 프레임워크의 나머지 등록 명령을 그 패키지의 실행 파일로 넘깁니다. CLI는 프레임워크를 자동으로 설치하지 않습니다.

```sh
zuku dev --help
zuku build --webpack
zuku start
```

인수, 출력, 종료 상태를 그대로 전달하므로 이 명령들의 `--json` 지원은 프레임워크 자체 규칙을 따르며 `zuku-command/1` 형식이 적용되지 않습니다. 프레임워크가 없는 경우에도 현재 폴더가 ZUKU 게임이면 인수 없는 `zuku build`는 Agent Core로 게임을 빌드합니다. 그 밖의 프레임워크 전용 명령이나 게임이 아닌 폴더에서는 `FRAMEWORK_UNAVAILABLE`로 실패합니다.

## 출력 형식 (`zuku-command/1`)

| 경우 | 스트림 | 형식 |
| --- | --- | --- |
| 성공, `--json` | stdout | `{"success":true,"data":...,"meta":{...}}` 한 줄 |
| 성공, 일반 | stdout | 일반 출력 |
| 실패, `--json` | stderr | `{"success":false,"error":{"code","message"},"meta":{...}}` 한 줄 |
| 실패, 일반 | stderr | `CODE: message` |

## 종료 코드

| 코드 | 의미 |
| --- | --- |
| `0` | 성공 |
| `1` | 실패(검증, 패키지, 자격 증명, API 오류 등) |
| `2` | 인수 오류(`INVALID_INPUT`), 알 수 없는 명령(`UNKNOWN_COMMAND`) |
| `130` | 사용자 취소(`COMMAND_CANCELLED`, Ctrl+C) |

서버 오류는 HTTP 상태와 API 오류 코드(예: `UNAUTHORIZED`, `INVALID_PACKAGE`, `PAYLOAD_TOO_LARGE`, `VALIDATION_ERROR`)로 보고하며, 원격 응답 전문이나 헤더는 출력하지 않습니다. 오류 코드별 해결 방법은 [오류](../errors.md)를 보세요.
