---
title: 제공자
description: 기본 ZUKU AI 제공자와 외부 AI 제공자를 확인·선택·설정하는 방법입니다.
section: Guide
---

# 제공자

제공자(provider)는 에이전트가 게임을 만들 때 사용할 AI 서비스입니다. `zuku`와 `zukujs`는 같은 제공자 설정, 비밀 저장소, 모델 캐시를 공유하므로 어느 이름으로 실행해도 결과가 같습니다.

## 기본 제공자: ZUKU AI (`zuku/auto`)

기본 선택은 ZUKU의 네이티브 AI 제공자 **ZUKU AI**이며 모델 주소는 `zuku/auto`입니다.

- `zuku/auto`는 서버가 알맞은 모델로 연결해 주는 라우팅 별칭입니다.
- 모델 카탈로그는 서버에서 동적으로 제공되며 CLI에 고정된 목록이 없습니다.
- 사용하려면 ZUKU 계정을 연결하고 생성 권한을 승인해야 합니다.

  ```sh
  zuku login zuku --generate
  ```

  자세한 내용은 [CLI 인증](authentication.md)을 보세요.

다른 제공자는 사용자가 명시적으로 선택할 때만 사용합니다. 선택한 제공자가 실패해도 다른 제공자로 자동 전환하지 않습니다. 인증 실패, 권한 누락, 서버 일시 장애가 있어도 외부 제공자로 대신 실행하지 않습니다.

> 로컬 CLI는 사용자가 연결한 외부 제공자나 로컬 모델로 실행할 수 있습니다. ZUKU AI 모델의 실제 가용성은 서버 권한과 카탈로그에 따릅니다. 웹의 호스팅 AI와 앱 내 AI는 현재 공개되어 있지 않으며 개시 일정은 미정입니다. Android 앱 미리보기는 [다운로드 페이지](https://apk.zuzunza.com/)에서 제공됩니다.

## 명령

```sh
zuku provider list                     # 전체 목록(● = 현재 선택)
zuku provider show <id>
zuku provider use <id>                 # TTY에서 <id>를 생략하면 목록에서 선택
zuku provider add [options]            # 사용자 지정 엔드포인트 추가
zuku provider configure <id> [options]
zuku provider enable <id>
zuku provider disable <id>             # 현재 선택된 제공자는 비활성화할 수 없음
zuku provider remove <id> --yes        # 사용자 지정 제공자만 삭제(저장된 키 포함)
```

- 모든 명령은 `--json`을 지원하며, 결과에 자격 증명 값은 들어가지 않습니다.
- 질문은 stdin과 stderr가 모두 터미널일 때만 합니다. 파이프나 CI에서는 필요한 값이 빠지면 질문 없이 `INVALID_INPUT`(종료 코드 2)으로 끝납니다.

### 예: OpenAI로 전환하기

```sh
zuku auth login --provider openai      # 키를 숨김 입력으로 등록
zuku provider use openai
zuku model list                        # 사용 가능한 모델 확인
```

모델 선택은 [모델](models.md)을 보세요.

## 지원 제공자

공식 API 키나 공식 자격 증명을 사용하는 제공자는 정식으로 지원됩니다. 실험 기능이 아닙니다.

| ID | 이름 | 인증 |
| --- | --- | --- |
| `zuku` | ZUKU AI (기본) | ZUKU 게임 CLI OAuth 승인, `zuku login zuku --generate` |
| `openai` | OpenAI | API 키, `OPENAI_API_KEY` |
| `anthropic` | Anthropic | API 키, `ANTHROPIC_API_KEY` |
| `google` | Google Gemini | API 키, `GEMINI_API_KEY`·`GOOGLE_GENERATIVE_AI_API_KEY` |
| `openrouter` | OpenRouter | API 키, `OPENROUTER_API_KEY` |
| `amazon-bedrock` | AWS Bedrock | AWS 자격 증명 체인 또는 Bedrock API 키(`AWS_BEARER_TOKEN_BEDROCK`), `--region` 필수 |
| `google-vertex` | Vertex AI | Google ADC. 프로젝트 설정은 현재 CLI의 Agent Core 프로토콜에서 전달할 수 없음 |
| `azure` | Azure OpenAI | API 키, `AZURE_OPENAI_API_KEY`·`AZURE_API_KEY` |
| `mistral` | Mistral | `MISTRAL_API_KEY` |
| `deepseek` | DeepSeek | `DEEPSEEK_API_KEY` |
| `groq` | Groq | `GROQ_API_KEY` |
| `xai` | xAI | `XAI_API_KEY` |
| `alibaba` | Qwen(DashScope) | `DASHSCOPE_API_KEY`·`ALIBABA_API_KEY` |
| `togetherai` | Together AI | `TOGETHER_API_KEY` |
| `fireworks` | Fireworks AI | `FIREWORKS_API_KEY` |
| `cerebras` | Cerebras | `CEREBRAS_API_KEY` |
| `sambanova` | SambaNova | `SAMBANOVA_API_KEY` |
| `huggingface` | Hugging Face | `HF_TOKEN`·`HUGGINGFACE_API_KEY` |
| `vercel` | Vercel AI Gateway | `AI_GATEWAY_API_KEY` |
| `cloudflare-ai-gateway` | Cloudflare AI Gateway | API 키. 필요한 accountId·gatewayId는 현재 CLI에서 설정할 수 없음 |
| `ollama` | Ollama | 로컬(자격 증명 없음), `http://127.0.0.1:11434` |
| `lmstudio` | LM Studio | 로컬(자격 증명 없음), `http://127.0.0.1:1234/v1` |
| `codex` | Codex | CLI 연동 Codex 로그인 `(exp!)`(터미널에서 주황색) |

### Codex 로그인 연동 `(exp!)`

Codex는 이 CLI의 **비공식·실험적 연동**으로 연결됩니다. 목록에서는 주황색 `(exp!)` 표시가 붙습니다. 이 표시는 CLI 연동 방식이 실험적이라는 뜻이며, Codex 서비스 자체에 대한 평가가 아닙니다.

```sh
zuku login codex --experimental        # 최초 1회 동의
zuku provider use codex
```

Codex는 명시적으로 선택할 때만 사용되며, 다른 제공자가 실패했을 때 대신 쓰이지 않습니다.

## 공식 제공자 설정 바꾸기

```sh
zuku provider configure azure --base-url https://<resource>.openai.azure.com/openai/v1
zuku provider configure amazon-bedrock --region us-east-1 --model <model-id>
zuku provider configure openrouter --model <vendor>/<model> --default-model <vendor>/<model>
```

`configure`는 `--model`(추가), `--remove-model`, `--default-model`, `--api-key-env`와 제공자가 허용하는 설정을 전달합니다. 현재 Agent Core로 전달할 수 있는 옵션 객체의 키는 `region`과 `location`뿐입니다. 기본 모델은 `--default-model`로 설정하세요.

`--project`, `--option accountId=...`, `--option gatewayId=...`, `--option project=...`·`--option catalog=...`, `--clear-api-key-env`, `--header-env`, `--header-secret`, `--remove-header`는 파서에 남아 있지만 현재 CLI에서는 `CORE_PROTOCOL_GAP`로 실패하며 설정을 바꾸지 않습니다. 따라서 Vertex 프로젝트와 Cloudflare 게이트웨이 ID를 CLI로 설정하는 사용 예제는 현재 제공하지 않습니다.

공식 제공자의 고정 주소는 바꿀 수 없습니다(`PROVIDER_ENDPOINT_FIXED`). Azure는 공식 리소스 도메인만 허용합니다. Cloudflare 어댑터는 공식 accountId·gatewayId로 주소를 구성하지만, 현재 CLI의 설정 전달 제한 때문에 두 ID를 등록할 수 없습니다.

## 사용자 지정 엔드포인트 `(exp!)`

OpenAI·Anthropic 호환 API를 제공하는 다른 주소를 직접 등록할 수 있습니다.

```sh
zuku provider add --id local-ai --name "Local AI" --type openai-chat \
  --base-url http://localhost:8000/v1 --model my-model --api-key-env LOCAL_AI_KEY
```

| 옵션 | 설명 |
| --- | --- |
| `--id` | 소문자·숫자·`-`, 최대 64자. 기본 제공자 ID와 겹칠 수 없음 |
| `--name` | 표시 이름 |
| `--type` | `openai-chat`(Chat Completions), `openai-responses`(Responses), `anthropic`(Messages) |
| `--base-url` | `https://` 주소 또는 루프백 `http://127.0.0.1`·`localhost`·`[::1]` |
| `--model` | 여러 번 지정 가능. 첫 모델이 기본 모델 |
| `--api-key-env` | 키를 담은 환경 변수 **이름**만 저장 |
| `--api-key-stdin` | 키를 파이프로 한 줄 입력 |
| `--disabled`, `--non-interactive` | 비활성 상태로 추가 / 질문하지 않음 |

터미널에서 옵션 없이 `zuku provider add`를 실행하면 형식 → 이름 → ID → Base URL → 모델 → (선택) API 키 순서로 묻습니다.

사용자 지정 엔드포인트는 서비스의 공식 인증인지 CLI가 확인할 수 없으므로 항상 `(exp!)`·비공식으로 표시합니다. 이 제공자로 에이전트를 실행할 때는 `--experimental`을 명시하세요. 추가 헤더 설정은 현재 Agent Core에 전달할 수 없어 `CORE_PROTOCOL_GAP`로 실패합니다. 모델 목록은 기본적으로 등록한 모델만 보입니다. 사용자 지정·로컬 모델을 써도 에이전트의 작업 범위와 도구 제한은 그대로 적용됩니다.

## 저장 위치

제공자 설정은 사용자 전용 디렉터리에 저장됩니다.

| 플랫폼 | 경로 |
| --- | --- |
| Linux/macOS | `~/.config/zukujs/providers/` (디렉터리 0700, 파일 0600) |
| Windows | `%LOCALAPPDATA%\ZukuJS\providers\` |

- `config.json`: 제공자·모델·환경 변수 이름 같은 공개 설정. 키나 토큰이 들어 있으면 읽기와 쓰기를 모두 거부합니다(`PROVIDER_SECRET_IN_CONFIG`).
- `secrets.json`(POSIX) / `secrets.dpapi`(Windows): API 키와 비밀 헤더 값.
- `models/<id>.json`: 자격 증명이 없는 모델 정보 캐시.

이 파일을 직접 편집하거나 공유하지 마세요. 키 등록과 삭제는 [CLI 인증](authentication.md)의 `zuku auth` 명령을 사용합니다.

## 다음 단계

- [모델](models.md) — 모델 목록과 선택
- [에이전트](agent.md) — 선택한 제공자로 게임 생성
- [명령 참조](commands.md)
- [오류](../errors.md)
