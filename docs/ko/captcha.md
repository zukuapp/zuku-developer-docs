---
title: 캡차
description: ZUKU 자체 Proof-of-Work 캡차의 챌린지 발급, 토큰 검증, 가입·로그인 게이트 계약을 설명합니다.
section: API
---

# 캡차

ZUKU는 외부 위젯(reCAPTCHA 등) 없이 자체 Proof-of-Work(PoW) 캡차를 사용합니다. 서버가 HMAC 서명된 챌린지를 발급하고, 클라이언트가 계산으로 답을 찾아 토큰으로 제출합니다. 캡차는 가입·로그인 남용을 줄이기 위한 장치입니다.

**Base URL**: `https://zuzunza.com/api/v1`

## 빠른 예제

```bash
# 챌린지 발급
curl -sS -X POST "https://zuzunza.com/api/v1/captcha/challenge" \
  -H "Accept-Language: ko-KR" \
  -H "X-Request-Id: $(uuidgen)"

# 풀이한 토큰 검증
curl -sS -X POST "https://zuzunza.com/api/v1/captcha/verify" \
  -H "Content-Type: application/json" \
  -d '{"token":"'"$TOKEN"'"}'
```

## 프로토콜

1. 서버가 `salt`, `challenge = hex(SHA-256(salt ‖ number))`, `signature = hex(HMAC-SHA256(secret, challenge))`를 발급합니다.
2. 클라이언트가 `0..=maxnumber` 범위에서 `challenge`와 일치하는 `number`를 찾습니다.
3. `base64(JSON{algorithm, challenge, number, salt, signature})` 토큰을 제출합니다.

| 항목 | 기본값 |
|---|---|
| `maxnumber` (탐색 상한) | `100000` |
| 챌린지 유효 시간 | 300초 (`salt`에 만료 시각 포함) |

## POST /captcha/challenge

PoW 챌린지를 발급합니다. 인증이 필요 없고 본문도 없습니다.

### 응답

`200 OK` — `data`:

```json
{
  "algorithm": "SHA-256",
  "challenge": "a1b2…",
  "salt": "zzcp_<hex>.<expiry_unix>",
  "signature": "…",
  "maxnumber": 100000
}
```

| 필드 | 설명 |
|---|---|
| `algorithm` | 해시 알고리즘 (`SHA-256`) |
| `challenge` | 찾아야 할 해시 값(hex) |
| `salt` | 솔트와 만료 시각 |
| `signature` | 서버 서명 |
| `maxnumber` | 탐색 상한 |

### 오류

| HTTP | code | 조건 |
|---|---|---|
| 503 | `CAPTCHA_NOT_CONFIGURED` | 서버에 캡차가 설정되지 않음 |
| 405 | — | `GET` 등 허용되지 않는 메서드 |

## POST /captcha/verify

풀이한 토큰을 검증합니다. 서버 간 호출과 디버그용이며, 가입·로그인 게이트는 본문의 `zcaptcha_token`을 같은 검증기로 확인합니다.

### 요청 본문

| 필드 | 필수 | 설명 |
|---|---|---|
| `token` | 예 | 풀이한 base64 토큰 |
| `dev_host` | 아니요 | 로컬 개발 우회가 켜진 서버에서만 의미가 있으며, 운영에서는 영향이 없습니다. |

```json
{ "token": "<solved-base64-token>" }
```

### 응답

`200 OK` — `data`: `{ "success": true }`

### 오류

| HTTP | code | 조건 |
|---|---|---|
| 503 | `CAPTCHA_NOT_CONFIGURED` | 서버에 캡차가 설정되지 않음 |
| 403 | `CAPTCHA_FAILED` | 서명·만료·number 불일치 또는 재사용 |
| 400 | `BAD_REQUEST` | JSON 파싱 실패 등 |

## 가입·로그인 게이트

`POST /auth/register`, `POST /auth/signup`, `POST /auth/login`에 공통으로 적용됩니다.

| 서버 상태 | 동작 |
|---|---|
| 캡차 비활성 | 게이트가 꺼져 있어 가입·로그인을 막지 않습니다. |
| 캡차 활성 | 본문 `zcaptcha_token`이 필수이며, 실패하면 `403 CAPTCHA_FAILED`입니다. |

가입·로그인 필드 전체는 [인증](authentication.md)을 참고하세요.

## 클라이언트 풀이 흐름

```
POST /captcha/challenge
        │
        ▼
  for n in 0..=maxnumber
    if sha256(salt + n) == challenge → 발견
        │
        ▼
  token = base64(JSON{ algorithm, challenge, number, salt, signature })
        │
        ▼
  POST /auth/register { …, "zcaptcha_token": token }
```

권장 사항:

- 브라우저에서는 UI가 멈추지 않도록 Web Worker에서 탐색하세요.
- 실패(만료·재사용)하면 새 챌린지를 받아 다시 시도하세요.
- 문의할 때 추적할 수 있도록 `X-Request-ID`를 함께 보내세요.

토큰을 포함한 가입 요청 예:

```bash
curl -sS -X POST "https://zuzunza.com/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -H "Accept-Language: ko-KR" \
  -d '{
    "email": "demo@example.com",
    "password": "password1",
    "password_confirm": "password1",
    "handle": "demo_user",
    "zcaptcha_token": "'"$TOKEN"'"
  }'
```

## 오류 코드

| code | HTTP | 의미 |
|---|---|---|
| `CAPTCHA_NOT_CONFIGURED` | 503 | 서버에 캡차가 설정되지 않음(challenge/verify) |
| `CAPTCHA_FAILED` | 403 | 토큰 검증 실패 또는 게이트 거절 |
| `BAD_REQUEST` | 400 | 본문 형식 오류 |

## 관련 문서

- [인증](authentication.md) — 가입·로그인 필드
- [오류](errors.md) — 공통 응답 형식
- [예제](examples.md) — 전체 흐름
