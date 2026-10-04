---
title: CLI 인증
description: ZUKU 계정 로그인·게임 OAuth 승인과 AI 제공자 자격 증명을 구분해 설정하고 정리하는 방법입니다.
section: Guide
---

# CLI 인증

ZUKU CLI에는 성격이 다른 인증이 두 가지 있습니다.

| 구분 | 무엇을 위한 것인가 | 주요 명령 |
| --- | --- | --- |
| **1. ZUKU 계정 로그인과 게임 OAuth 승인** | 게임 업로드·초안 생성·공개 배포, ZUKU AI(`zuku/auto`) 네이티브 생성 | `zuku login zuku`, `zuku account ...` |
| **2. AI 제공자 자격 증명** | OpenAI·Anthropic 등 외부 AI 제공자를 에이전트 모델로 쓸 때 | `zuku auth ...` |

두 인증은 서로 대신하지 않습니다. 외부 제공자의 API 키로 게임을 배포할 수 없고, ZUKU 계정 연결이 외부 제공자의 키 역할을 하지도 않습니다.

이 페이지는 CLI 사용자를 위한 안내입니다. 서버 HTTP API의 로그인·세션·개발자 API 키 계약은 [API 인증](../authentication.md)을 보세요.

## `zuku`와 `zukujs`는 같은 인증을 공유합니다

`zuku`와 `zukujs`는 같은 CLI의 두 이름입니다. 두 명령은 같은 런타임·설정·인증·상태(`~/.config/zukujs/`(Windows: `%LOCALAPPDATA%\ZukuJS\`))를 사용하므로 한쪽에서 로그인하면 다른 쪽에서도 그대로 적용됩니다. 예를 들어 `zukujs auth ...`와 `zuku auth ...`는 같은 저장소를 읽고 씁니다. 사용자 설정·계정은 위 공유 디렉터리에 있고, 프로젝트 안의 `.zukujs/`에는 실행 기록과 영수증이 저장됩니다.

## 비밀 정보 다루기

- CLI는 비밀번호나 복사한 토큰을 요구하지 않습니다. 비밀 값을 명령 인수로 받지도 않습니다.
- `--api-key`, `--token`, `--secret`, `--password` 같은 옵션이나 키처럼 보이는 인수는 `AUTH_SECRET_ARGUMENT`로 거부되며, 그 값은 오류 메시지에 다시 나오지 않습니다.
- 키와 토큰은 로그, 오류 메시지, `--json` 출력, 배포 영수증에 기록되지 않습니다.
- 키나 토큰을 명령 기록, 프로젝트 파일, 저장소, 이슈, 화면 공유에 남기지 마세요. 문서나 지원 요청에도 붙여 넣지 마세요.

## 1. ZUKU 계정 로그인과 게임 OAuth 승인

```sh
zuku login zuku
```

로그인은 디바이스 승인 방식입니다. CLI가 공식 ZUKU 브라우저 페이지를 열어 주면, 브라우저에서 **로그인한 본인 계정으로** 연결을 확인하고 승인합니다. 승인이 끝나면 CLI가 연결을 저장합니다.

- 브라우저가 자동으로 열리지 않는 환경에서는 `--no-browser`를 붙이세요. CLI가 표시하는 공식 페이지를 직접 열어 승인하면 됩니다.

  ```sh
  zuku login zuku --no-browser
  ```

### 권한(스코프)

공개 클라이언트 ID는 `zuku-cli`이며, 기본으로 요청하는 권한은 다음 세 가지입니다.

| 권한 | 용도 |
| --- | --- |
| `games:upload` | 게임 패키지 업로드 |
| `games:create` | 초안 콘텐츠 생성 |
| `games:publish` | 공개 배포 |

ZUKU AI로 게임을 생성하려면 생성 권한을 **명시적으로** 추가 요청해야 합니다.

```sh
zuku login zuku --generate
```

`--generate`는 위 세 권한에 더해 `games:generate`를 요청합니다. 이 권한은 서버 쪽 네이티브 게임 API와 승인 페이지가 제공될 때 사용할 수 있으며, 실제 모델 가용성과 생성 성공 여부는 별도로 확인됩니다. 생성 권한 없이 연결된 계정은 업로드와 배포에는 계속 쓸 수 있지만, 생성 요청은 `ZUKU_GENERATE_SCOPE_REQUIRED`로 거부되고 `zuku auth list`에는 `scope-required`로 표시됩니다.

일반 웹 로그인, 개발자 API 키, 환경 변수에 둔 다른 인증 정보는 이 연결을 대신할 수 없습니다.

### 계정 상태와 배포 한도

```sh
zuku account --quota
```

서버는 계정당 최근 6시간 동안 성공한 공개 배포를 최대 3회까지 허용합니다. `account --quota`는 사용 수(`used`), 미확정 수(`pending`), 남은 수(`remaining`), 회복 시점(`reset_at`), 대기 시간(`retry_after`)을 보여 줍니다. 초안과 업로드는 이 횟수를 소비하지 않습니다. 배포 흐름은 [배포](publishing.md)를 보세요.

### 로그아웃과 정리

```sh
zuku account logout
```

- 로그아웃하면 토큰이 없는 기록이 남아, 늦게 도착한 로그인이나 갱신 응답이 연결을 되살리지 못합니다.
- 계정이 바뀌면 진행 중이던 기존 작업의 배포는 중단됩니다.
- 갱신 응답이 유실되면 이전 갱신 토큰을 다시 보내지 않고 재로그인을 요구합니다.
- 이전 시험용 서버의 계정 기록은 자동 변환되지 않습니다. `ZUKU_ACCOUNT_MIGRATION_REQUIRED`가 나오면 `zuku login zuku`로 다시 승인하세요. 기존 게임 프로젝트와 CLI 설정은 그대로 유지됩니다.

계정 저장소는 Unix에서 사용자 소유 디렉터리와 권한 `0600` 파일을 사용하고 링크를 거부합니다. Windows에서는 현재 사용자 DPAPI 암호화와 사용자 전용 ACL을 사용하며, 평문 저장으로 대체하지 않습니다.

## 2. AI 제공자 자격 증명

외부 AI 제공자를 쓰려면 해당 제공자의 자격 증명을 등록합니다.

```sh
zuku auth list [--provider <id>]
zuku auth login [--provider <id>] [options]
zuku auth logout [--provider <id>]
```

`--provider`를 생략하면 터미널(TTY)에서는 목록에서 고르고, 비대화형 실행에서는 `zuku`(ZUKU AI)를 사용합니다.

### 키 입력 방법

```sh
zuku auth login --provider openai                                  # 숨김 입력(화면에 표시되지 않음, Ctrl-C로 취소)
printf '%s\n' "$KEY" | zuku auth login --provider openai --api-key-stdin   # 파이프로 한 줄 입력
zuku auth login --provider openai --api-key-env MY_OPENAI_KEY      # 환경 변수 이름만 저장
```

- 비대화형 실행에서 입력 방법을 지정하지 않으면 질문 없이 `AUTH_INPUT_REQUIRED`로 끝납니다.
- `--api-key-stdin`은 한 줄만 받으며 16 KiB, 30초 제한이 있습니다.
- `--api-key-env`는 키 값이 아니라 **환경 변수 이름**만 설정에 저장합니다.
- `auth login --verify`와 `--header`는 현재 Agent Core에서 전달할 수 없어 `CORE_PROTOCOL_GAP`로 실패합니다. 등록 여부는 `zuku auth list --provider <id>`로 확인하세요. 이 명령은 원격 인증 성공을 검사하지 않습니다. `upload --verify`는 별도의 초안 조회 옵션이며 계속 지원됩니다.
- Ollama, LM Studio 같은 로컬 제공자는 저장할 자격 증명이 없어 `not-required`로 표시됩니다. Vertex AI는 Google 기본 자격 증명(ADC), AWS Bedrock은 AWS 자격 증명 체인 또는 Bedrock API 키를 사용합니다.

### 인증 방식과 `(exp!)` 표시

| 인증 방식 | 공식 | 실험적 |
| --- | --- | --- |
| API 키, 환경 변수, 클라우드 자격 증명 체인, Google ADC, 로컬 | 예 | 아니요 |
| ZUKU 게임 CLI OAuth 디바이스 승인 | 예 | 아니요 |
| Codex 로그인(CLI 연동) | 아니요 | 예 `(exp!)` |
| 사용자 지정 엔드포인트 | 아니요 | 예 `(exp!)` |

공식 제공자의 API 키 연결은 정식으로 지원되는 일반 기능입니다. 주황색 `(exp!)` 표시는 **이 CLI의 연동 방식**이 비공식·실험적이라는 뜻이며, 해당 서비스 자체가 실험적이라는 의미가 아닙니다. 색을 쓸 수 없는 출력(`NO_COLOR`, `TERM=dumb`, 파이프, `--json`)에서는 색 없이 표시됩니다.

Codex 로그인은 처음 한 번 `--experimental`로 동의해야 연결됩니다.

```sh
zuku login codex --experimental
```

최초 로그인 동의는 CLI 전용 보호 저장소에 기록됩니다. 이와 별도로 Agent Core에서 Codex나 사용자 지정 제공자로 새 에이전트 세션을 실행할 때는 `--experimental`을 명시해야 합니다. 생략하면 `AUTH_EXPERIMENTAL_OPT_IN`으로 실패합니다. CLI는 다른 도구의 로그인 상태나 키 파일을 가져오지 않습니다.

```sh
zuku agent "ZUKU 점프 게임을 만들어 주세요" --model codex/<model> --experimental
```

### 상태 확인

`zuku auth list`는 값이 아니라 상태만 보여 주며, 네트워크를 사용하지 않습니다.

| 상태 | 의미 |
| --- | --- |
| `configured` | 자격 증명이 등록됨 |
| `scope-required` | ZUKU 계정에 생성 권한이 없음 |
| `environment` | 환경 변수로 설정됨(변수 이름만 표시) |
| `credential-chain` | 클라우드 자격 증명 체인 사용(원격 확인 전) |
| `not-required` | 자격 증명이 필요 없음(로컬 등) |
| `not-configured` | 설정되지 않음 |
| `unknown` | 확인할 수 없음 |

### 제공자 자격 증명 삭제

```sh
zuku auth logout --provider openai
```

ZUKU 계정 연결을 끊으려면 위의 `zuku account logout`을 사용하세요. 제공자 자격 증명 삭제와 계정 로그아웃은 별개입니다.

## 자격 증명을 쓰는 순서

선택한 제공자 하나에 대해서만 다음 순서로 찾습니다. 다른 제공자의 환경 변수나 저장 항목은 읽지 않습니다.

1. 비밀 저장소에 저장한 API 키
2. `--api-key-env`로 지정한 환경 변수
3. 제공자의 공식 환경 변수
4. 클라우드 자격 증명 체인(Bedrock: AWS 체인, Vertex: ADC)
5. 로컬 또는 자격 증명 없는 사용자 지정 엔드포인트

선택된 방식의 인증이 실패해도 다른 방식이나 다른 제공자로 넘어가지 않습니다. ZUKU AI와 Codex는 이 순서에 포함되지 않고 각자의 보호 계정 저장소만 사용합니다.

## 온라인 생성에 필요한 것

에이전트로 게임을 온라인 생성하려면 **인증**과 **설정된 제공자**가 모두 필요합니다.

- 기본 제공자인 ZUKU AI(`zuku/auto`)를 쓰려면 `zuku login zuku --generate`로 생성 권한을 승인합니다.
- 다른 제공자를 쓰려면 `zuku auth login --provider <id>`로 자격 증명을 등록하고 [제공자](providers.md)와 [모델](models.md)을 선택합니다.

## 자주 보는 오류

| 코드 | 의미 |
| --- | --- |
| `AUTH_SECRET_ARGUMENT` | 비밀 값을 명령 인수로 전달함 |
| `AUTH_INPUT_REQUIRED` | 비대화형 실행에서 입력 방법이 없거나 입력 시간이 초과됨 |
| `AUTH_SECRET_INVALID` | 줄바꿈·제어 문자 포함 또는 크기 초과 |
| `AUTH_REQUIRED` | 선택한 제공자의 자격 증명이 없음 |
| `AUTH_SESSION_CHANGED` | 실행 중 인증·연결 설정이나 ZUKU 계정이 바뀜 |
| `AUTH_EXPERIMENTAL_OPT_IN` | Codex 최초 로그인 동의(`--experimental`)가 없음 |
| `ZUKU_GENERATE_SCOPE_REQUIRED` | ZUKU 계정에 생성 권한이 없음 |
| `SECRET_STORE_UNAVAILABLE`, `SECRET_STORE_UNSAFE` | 보호 저장소를 쓸 수 없거나 파일 권한이 안전하지 않음 |

전체 오류 목록은 [오류](../errors.md)를 보세요.

## 다음 단계

- [제공자](providers.md) — 기본 제공자와 외부 제공자 설정
- [모델](models.md) — 모델 목록 확인과 선택
- [에이전트](agent.md) — 게임 생성 실행
- [명령 참조](commands.md)
