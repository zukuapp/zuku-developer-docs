---
title: 인증
description: ZUKU API의 회원가입, 로그인, 세션, 브라우저 공통 로그인, 개발자 API 키 계약을 설명합니다.
section: API
---

# 인증

ZUKU API는 로그인 세션의 **Bearer 토큰**과 개발자 포털에서 발급하는 **API 키**(`X-API-Key`)로 요청을 인증합니다. 이 페이지에서는 가입, 로그인, 토큰 갱신, 프로필, 세션 관리, 브라우저 공통 로그인, 개발자 API 키를 다룹니다.

> **API 인증과 CLI 로그인은 다릅니다.** 이 페이지는 HTTP API를 직접 호출할 때 쓰는 토큰과 키를 설명합니다. `zuku` CLI의 로그인 방법과 저장 위치는 [CLI 인증](cli/authentication.md)을 참고하세요.

**Base URL**: `https://zuzunza.com/api/v1`

## 빠른 예제

```bash
# 1) 로그인해 토큰 받기
curl -sS -X POST "https://zuzunza.com/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"identifier":"demo@example.com","password":"password1"}'

# 2) 받은 access_token으로 내 정보 조회
curl -sS "https://zuzunza.com/api/v1/auth/me" \
  -H "Authorization: Bearer $ACCESS"
```

## 인증 방식

| 방식 | 헤더 | 용도 |
|---|---|---|
| Bearer 세션 | `Authorization: Bearer <access_token>` | 로그인 세션입니다. 대부분의 쓰기 API, 프로필, 세션, 개발자 키 관리에 필요합니다. |
| API 키 | `X-API-Key: sk_live_…` | 개발자 포털에서 발급한 키로, `sk_live_` 접두사가 필수입니다. Bearer가 없을 때 일부 서버 간 경로(예: 콘텐츠 생성)에서 발급자를 식별합니다. |
| 브라우저 공통 쿠키 | (HttpOnly 쿠키) | ZUKU 공식 도메인 사이의 공통 로그인입니다. [브라우저 공통 로그인](#브라우저-공통-로그인)을 참고하세요. |

- 세션 토큰은 `POST /auth/login` 또는 `POST /auth/register` 응답의 `tokens.access_token`과 `tokens.refresh_token`입니다.
- `token_type`은 항상 `"Bearer"`입니다.
- 개발자 키 원문(`key`)은 **발급 직후 한 번만** 반환됩니다. 이후 `GET /developer/keys`에서는 메타데이터만 볼 수 있습니다.
- 소셜, 알림, DM, 세션 관리 등 대부분의 경로는 **Bearer 세션만** 허용합니다.

## 응답 형식

성공 응답:

```json
{
  "success": true,
  "data": { },
  "meta": { "request_id": "…", "timestamp": "2026-08-22T04:00:00Z", "version": "v1" }
}
```

실패 응답:

```json
{
  "success": false,
  "error": {
    "code": "UNAUTHORIZED",
    "message": "…",
    "details": [{ "field": "password", "message": "…" }]
  },
  "meta": { "request_id": "…", "timestamp": "…", "version": "v1" }
}
```

`details`는 `VALIDATION_ERROR` 같은 검증 오류에서만 포함됩니다. 로그아웃, 세션 폐기, API 키 삭제는 본문 없이 `204 No Content`를 반환합니다.

## 엔드포인트 요약

| Method | Path | 인증 | 설명 |
|---|---|---|---|
| `POST` | `/auth/register` | 없음* | 회원가입 |
| `POST` | `/auth/signup` | 없음* | `/auth/register`의 별칭 |
| `POST` | `/auth/login` | 없음* | 로그인과 세션 발급 |
| `POST` | `/auth/logout` | Bearer | 현재 세션 종료 → `204` |
| `POST` | `/auth/refresh` | 없음(본문 토큰) | access 토큰 갱신 |
| `GET` | `/auth/me` | Bearer 또는 쿠키 | 현재 사용자 |
| `PATCH` | `/auth/me` | Bearer | 프로필 부분 수정 |
| `POST` | `/auth/session` | Bearer | 브라우저 공통 세션 계정 전환 |
| `GET` | `/auth/sessions` | Bearer | 활성 세션 목록 |
| `DELETE` | `/auth/sessions/{id}` | Bearer | 세션 하나 폐기 → `204` |
| `POST` | `/auth/oauth/{provider}` | — | 항상 `501 NOT_IMPLEMENTED` |
| `POST` | `/captcha/challenge` | 없음 | PoW 챌린지 발급 |
| `POST` | `/captcha/verify` | 없음 | 캡차 토큰 검증 |
| `POST` | `/developer/keys` | Bearer | API 키 발급 → `201` |
| `GET` | `/developer/keys` | Bearer | 내 키 목록 |
| `DELETE` | `/developer/keys/{id}` | Bearer | 키 폐기 → `204` |

\* 서버에서 캡차가 활성화되어 있으면 register·signup·login 본문에 유효한 `zcaptcha_token`이 필요합니다.

## 캡차

`POST /captcha/challenge`와 `POST /captcha/verify`의 전체 계약과 풀이 방법은 [캡차](captcha.md)에 있습니다.

| 서버 상태 | register / signup / login 동작 |
|---|---|
| 캡차 비활성 | 게이트가 꺼져 있어 가입·로그인을 막지 않습니다. |
| 캡차 활성 | 본문 `zcaptcha_token`이 필수이며, 실패하면 `403 CAPTCHA_FAILED`입니다. |

챌린지·검증 API는 캡차가 설정되지 않은 서버에서 `503 CAPTCHA_NOT_CONFIGURED`를 반환합니다.

## POST /auth/register

회원가입합니다. `POST /auth/signup`은 같은 동작을 하는 별칭입니다.

### 요청 본문

| 필드 | 필수 | 규칙 |
|---|---|---|
| `email` | 예 | `@`를 포함해야 합니다. |
| `password` | 예 | 최소 8자 |
| `password_confirm` | 예 | `password`와 같아야 합니다. |
| `handle` | 예 | 비어 있으면 안 됩니다. |
| `display_name` | 아니요 | 생략하면 `handle`을 표시 이름으로 씁니다. |
| `zcaptcha_token` | 조건부 | 캡차가 활성화된 서버에서 필수 |

```bash
curl -sS -X POST "https://zuzunza.com/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "demo@example.com",
    "password": "password1",
    "password_confirm": "password1",
    "handle": "demo_user",
    "zcaptcha_token": "OPTIONAL_WHEN_CAPTCHA_SET"
  }'
```

### 응답

`201 Created` — `data.user`와 `data.tokens`(`access_token`, `refresh_token`, `token_type`, `expires_in`).

### 오류

| HTTP | code | 상황 |
|---|---|---|
| 409 | `ALREADY_AUTHENTICATED` | 유효한 Bearer로 이미 로그인한 상태에서 가입 시도 |
| 409 | `EMAIL_EXISTS` | 이메일 중복 |
| 409 | `LEGACY_ACCOUNT_EXISTS` | 기존 ZUKU 계정에 같은 이메일·handle이 있음 → 로그인으로 안내하세요 |
| 409 | `HANDLE_EXISTS` | handle 중복 |
| 422 | `VALIDATION_ERROR` | 비밀번호·이메일·handle 검증 실패 |
| 403 | `CAPTCHA_FAILED` | 캡차 게이트 실패 |

## POST /auth/login

로그인하고 세션 토큰을 발급합니다.

### 요청 본문

| 필드 | 필수 | 설명 |
|---|---|---|
| `identifier` 또는 `email` | 둘 중 하나 | `identifier`가 우선합니다. 이메일, 아이디, 닉네임을 받습니다. |
| `password` | 예 | |
| `device_id` | 아니요 | 세션 메타데이터 |
| `zcaptcha_token` | 조건부 | 캡차가 활성화된 서버에서 필수 |

기존(레거시) ZUKU 계정으로도 로그인할 수 있으며, 처음 성공하면 현재 계정 체계로 연결됩니다.

```bash
curl -sS -X POST "https://zuzunza.com/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"identifier":"demo@example.com","password":"password1"}'
```

### 응답

`200 OK` — `data.user`와 `data.tokens`.

### 오류

| HTTP | code |
|---|---|
| 401 | `INVALID_CREDENTIALS` |
| 403 | `ACCOUNT_SUSPENDED` |
| 403 | `CAPTCHA_FAILED` |

## POST /auth/logout

현재 세션을 종료합니다. `Authorization: Bearer <access_token>`이 필요합니다.

- 성공: `204` (본문 없음). 브라우저 공통 세션도 종료되고 쿠키가 삭제됩니다. 반복 호출해도 `204`입니다.
- 헤더가 없거나 형식이 잘못됨: `401 UNAUTHORIZED`

```bash
curl -sS -X POST "https://zuzunza.com/api/v1/auth/logout" \
  -H "Authorization: Bearer $ACCESS"
```

## POST /auth/refresh

access 토큰을 갱신합니다.

| 필드 | 필수 | 설명 |
|---|---|---|
| `refresh_token` | 예 | 로그인·가입 때 받은 refresh 토큰 |

```bash
curl -sS -X POST "https://zuzunza.com/api/v1/auth/refresh" \
  -H "Content-Type: application/json" \
  -d "{\"refresh_token\":\"$REFRESH\"}"
```

- 성공: `data.tokens` — 새 `access_token`, 기존 `refresh_token` 유지, `expires_in`은 약 7일. 같은 브라우저 세션도 유지됩니다.
- 실패: `401 INVALID_REFRESH_TOKEN`

## GET /auth/me

현재 사용자를 `data.user`로 반환합니다. Bearer 또는 브라우저 공통 쿠키가 필요합니다.

공개 사용자 필드: `id`(`usr_…`), `email`, `display_name`, `handle`, `role`, `avatar_url`, `is_verified`, `created_at`, `profile_completion_status`, `bio`, `website_url`, `location`, `cover_url`, `banner_tone`

```bash
curl -sS "https://zuzunza.com/api/v1/auth/me" \
  -H "Authorization: Bearer $ACCESS"
```

## PATCH /auth/me

전달한 필드만 수정합니다. Bearer가 필요합니다.

| 필드 | 설명 |
|---|---|
| `display_name` | 표시 이름 |
| `bio` | 소개 |
| `website_url` | 웹사이트 |
| `location` | 위치 |
| `banner_tone` | `cyan` \| `swipe` \| `jump` \| `slate` |
| `cover_url` | 커버 이미지 URL |
| `avatar_url` | 아바타 이미지 URL |

```bash
curl -sS -X PATCH "https://zuzunza.com/api/v1/auth/me" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{"display_name":"데모","banner_tone":"jump"}'
```

## 세션 관리

전체 로그아웃 대신 낯선 세션만 골라 끊을 수 있습니다.

### GET /auth/sessions

`data.sessions[]` 항목: `id`, `device_label`, `created_at`, `last_seen_at`, `is_current`. 토큰 원문은 절대 반환하지 않습니다.

### DELETE /auth/sessions/{id}

- `{id}`는 숫자 세션 id입니다.
- 본인 세션만 폐기할 수 있으며, 없거나 다른 사용자의 세션이면 `404 NOT_FOUND`입니다.
- 성공: `204`

```bash
curl -sS -X DELETE "https://zuzunza.com/api/v1/auth/sessions/42" \
  -H "Authorization: Bearer $ACCESS"
```

## 브라우저 공통 로그인

ZUKU 공식 도메인 사이에서는 공통 HttpOnly 세션 쿠키를 사용합니다.

- 브라우저에서 API를 호출할 때는 `credentials: 'include'`를 지정하세요.
- 유효한 공통 쿠키가 있으면 오래 저장된 Bearer 토큰보다 쿠키의 계정이 우선합니다.
- 쿠키가 없는 서버 클라이언트는 기존 Bearer 방식을 그대로 사용합니다.
- `GET /auth/me`가 성공하면 같은 브라우저 세션의 만료가 7일로 연장됩니다. 기존 쿠키는 정상 세션 확인 과정에서 새 브라우저 세션으로 전환됩니다.
- 쿠키는 HttpOnly이므로 문서 페이지나 게임 코드에서 읽을 수 없으며, 브라우저 세션용 자격 증명은 응답 JSON에 포함되지 않습니다.

### POST /auth/session

저장된 다른 계정을 **명시적으로 선택**할 때 사용합니다. 선택한 계정의 `Authorization: Bearer <access_token>`이 필수이며 본문은 없습니다.

- 성공: `200` · `data.user`. 브라우저 공통 쿠키가 선택한 계정으로 바뀝니다.
- 쿠키만 보내면 `401`입니다.

```bash
curl -sS -X POST "https://zuzunza.com/api/v1/auth/session" \
  -H "Authorization: Bearer $SELECTED_ACCOUNT_ACCESS"
```

## POST /auth/oauth/{provider}

항상 `501 Not Implemented`, code `NOT_IMPLEMENTED`를 반환합니다. OAuth 로그인은 아직 제공되지 않습니다.

## 개발자 API 키

모든 경로에 Bearer가 필요합니다. 발급한 키는 `X-API-Key: sk_live_…` 형태로 일부 API에서 Bearer 대신 사용할 수 있습니다. 앱 단위 키와 웹훅은 [개발자 콘솔](devconsole.md)을 참고하세요.

### POST /developer/keys

| 필드 | 필수 | 규칙 |
|---|---|---|
| `name` | 예 | 1~50자 |

`201 Created` — `data.api_key`(메타데이터)와 `data.key`(평문 키, **이 응답에서만** 제공). 평문 키는 바로 안전하게 보관하세요.

```bash
curl -sS -X POST "https://zuzunza.com/api/v1/developer/keys" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{"name":"my-integration"}'
```

### GET /developer/keys

`data.api_keys` 배열을 반환합니다(평문 키 없음).

### DELETE /developer/keys/{id}

성공 `204`. 없거나 다른 사용자의 키이면 `404 API_KEY_NOT_FOUND`.

## 오류 코드

| code | HTTP | 의미 |
|---|---|---|
| `ALREADY_AUTHENTICATED` | 409 | 로그인 상태에서 가입 |
| `EMAIL_EXISTS` | 409 | 이메일 중복 |
| `LEGACY_ACCOUNT_EXISTS` | 409 | 기존 계정 존재 → 로그인 |
| `HANDLE_EXISTS` | 409 | handle 중복 |
| `VALIDATION_ERROR` | 422 | 필드 검증 실패 |
| `INVALID_CREDENTIALS` | 401 | 로그인 실패 |
| `ACCOUNT_SUSPENDED` | 403 | 정지된 계정 |
| `UNAUTHORIZED` | 401 | Bearer 없음 또는 무효 |
| `INVALID_REFRESH_TOKEN` | 401 | refresh 토큰 무효 |
| `CAPTCHA_NOT_CONFIGURED` | 503 | 서버에 캡차가 설정되지 않음(challenge/verify) |
| `CAPTCHA_FAILED` | 403 | 캡차 실패 |
| `NOT_IMPLEMENTED` | 501 | OAuth |
| `API_KEY_NOT_FOUND` | 404 | 삭제할 키 없음 |
| `NOT_FOUND` | 404 | 세션 등 대상 없음 |

전체 목록은 [오류](errors.md)를 참고하세요.

## 관련 문서

- [캡차](captcha.md)
- [CLI 인증](cli/authentication.md)
- [개발자 콘솔](devconsole.md)
- [오류](errors.md) · [요청 한도](rate-limits.md)
- [예제](examples.md)
