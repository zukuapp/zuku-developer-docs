---
title: 모델
description: 모델 주소 형식과 모델 목록 확인·선택·정보 조회 명령을 설명합니다.
section: Reference
---

# 모델

에이전트가 사용할 모델은 `<provider>/<model>` 주소로 지정합니다. 기본 모델은 ZUKU AI의 `zuku/auto`입니다.

## 모델 주소

주소는 **첫 번째 `/`에서만** 제공자와 모델로 나뉩니다. 모델 ID 안에 있는 `/`는 그대로 유지됩니다.

```text
zuku/auto
openai/<model>
anthropic/<model>
google/<model>
openrouter/<vendor>/<model>      # 제공자=openrouter, 모델=<vendor>/<model>
ollama/<model>
```

- 제공자 ID: 소문자·숫자·`-`, 최대 64자
- 모델 ID: 최대 256자. 각 `/` 구간에는 영문·숫자와 `. _ : @ + ~ = , -`만 쓸 수 있습니다. 공백·제어 문자·`%`·`\`·빈 구간·`.`/`..` 구간은 `MODEL_ADDRESS_INVALID`로 거부됩니다.

## 명령

```sh
zuku model list [--provider <id>] [--refresh]   # 기본: 현재 제공자
zuku model refresh [--provider <id>]            # 캐시를 무시하고 다시 조회
zuku model use <provider/model>                 # TTY에서 생략하면 목록에서 선택
zuku model info [<provider/model>] [--refresh]  # 기본: 현재 모델
zuku model current
```

`zukujs model ...`도 같은 설정을 바꿉니다. `model use`는 현재 제공자와 모델을 함께 바꿉니다.

### 예

```sh
zuku model current                 # 현재 선택 확인
zuku model list --provider zuku    # ZUKU AI 모델 목록
zuku model use zuku/auto           # 기본값으로 되돌리기
```

## 모델 목록은 동적입니다

CLI는 모델 목록을 미리 정해 두지 않습니다. ZUKU AI의 카탈로그도 서버에서 받아 오므로 시점과 계정에 따라 달라질 수 있습니다. 실제로 사용할 수 있는 모델은 항상 `zuku model list`로 확인하세요.

각 항목의 `source`는 출처를 나타냅니다.

| `source` | 의미 |
| --- | --- |
| `builtin` | 네이티브 별칭(`zuku/auto`) |
| `configured` | `zuku provider add` 또는 `zuku provider configure --model`로 등록한 모델 |
| `discovered` | 제공자의 모델 목록 API가 실제로 돌려준 모델 |

- 모델 목록 API가 있는 제공자는 실제 API로 조회합니다. 없는 경우 CLI가 목록을 지어내지 않고 등록한 모델만 보여 줍니다. 목록에 없는 모델을 선택하면 `MODEL_UNAVAILABLE`로 실패합니다.
- ZUKU AI 목록을 보려면 ZUKU 계정 연결과 생성 권한이 필요합니다([CLI 인증](authentication.md)).

### 조회 상태

| `discovery.status` | 의미 |
| --- | --- |
| `fresh` | 방금 조회함 |
| `cached` | 유효 기간 안의 캐시 |
| `stale` | 조회에 실패해 이전 캐시를 사용 |
| `unavailable` | 조회할 수 없음(`error`에 오류 코드) |
| `unsupported` | 목록 조회를 지원하지 않음 |

### 캐시

- 제공자별로 15분 동안 캐시합니다. 바로 다시 조회하려면 `zuku model refresh` 또는 `--refresh`를 사용합니다.
- 제공자 주소·옵션·인증 방식·ZUKU 계정이 바뀌면 이전 캐시를 쓰지 않습니다.
- 로그아웃, 생성 권한 누락, 인증 실패 시에는 이전 계정의 목록을 보여 주지 않습니다.
- 캐시에는 키·토큰·비밀 헤더가 저장되지 않습니다.
- 실패한 조회는 자동으로 다시 시도하지 않습니다.

## 모델 정보

`zuku model info`는 모델의 기능과 한도를 보여 줍니다. 아래는 형식 예시입니다.

```json
{
  "id": "<model>", "address": "openai/<model>", "name": "<표시 이름>", "provider": "openai",
  "capabilities": { "streaming": null, "tools": true, "vision": null, "reasoning": null, "promptCaching": null },
  "contextWindow": 128000, "maxOutputTokens": null, "inputCost": null, "outputCost": null,
  "source": "discovered"
}
```

토큰 한도·가격·기능은 제공자 API나 사용자가 등록한 값이 있을 때만 채웁니다. 알 수 없는 값은 추측하지 않고 `null`로 둡니다.

## 에이전트가 모델을 고르는 방식

1. 실행 시 지정한 모델
2. 없으면 `zuku model use`로 선택한 모델
3. 그것도 없으면 `zuku/auto`

선택된 제공자가 비활성화되었거나 모델을 알 수 없으면 실행은 실패하며, 다른 제공자나 모델로 바꾸지 않습니다. ZUKU AI 네이티브 연결은 현재 스트리밍과 모델 도구 호출을 제공하지 않습니다.

온라인 생성에는 인증과 설정된 제공자가 필요합니다. 제공자 설정은 [제공자](providers.md), 실행 방법은 [에이전트](agent.md)를 보세요.

## 관련 문서

- [명령 참조](commands.md)
- [CLI 인증](authentication.md)
- [오류](../errors.md)
