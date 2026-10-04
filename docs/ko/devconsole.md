---
title: 개발자 콘솔
description: 개발자 콘솔 API로 앱을 등록하고 앱별 API 키와 웹훅을 관리합니다.
section: API
---

# 개발자 콘솔

ZUKU 개발자 콘솔 API는 앱 등록, 앱별 API 키, 웹훅을 관리합니다. 같은 기능은 Studio의 개발자 콘솔 화면(`/studio/developer`)에서도 사용할 수 있습니다.

**Base URL**: `https://zuzunza.com/api/v1/devconsole`

**인증**: 모든 요청에 `Authorization: Bearer <session_token>`이 필요합니다.

## 빠른 예제

```bash
curl -sS "https://zuzunza.com/api/v1/devconsole/apps" \
  -H "Authorization: Bearer $ACCESS"
```

## 엔드포인트 요약

| Method | Path | 설명 |
|---|---|---|
| `GET` | `/devconsole/apps` | 앱 목록 |
| `POST` | `/devconsole/apps` | 앱 등록 |
| `GET` | `/devconsole/apps/{app_id}` | 앱 상세 |
| `GET` | `/devconsole/apps/{app_id}/keys` | 앱 키 목록 |
| `POST` | `/devconsole/apps/{app_id}/keys` | 앱 키 발급 |
| `DELETE` | `/devconsole/keys/{key_id}` | 키 폐기 |
| `GET` | `/devconsole/apps/{app_id}/webhooks` | 웹훅 목록 |
| `POST` | `/devconsole/apps/{app_id}/webhooks` | 웹훅 등록 |
| `POST` | `/devconsole/webhooks/{webhook_id}/test` | 웹훅 테스트 전송 |
| `GET` | `/devconsole/webhooks/{webhook_id}/deliveries` | 전달 로그 |

## 앱

### POST /devconsole/apps

| 필드 | 설명 |
|---|---|
| `app_name` | 앱 이름 |
| `app_type` | `web` \| `mobile` \| `server` \| `cli` \| `game` |
| `description` | 설명 |
| `redirect_uris` | 리디렉션 URI 배열 |
| `scopes` | 권한 범위 배열(예: `contents:read`, `jump:write`) |

```bash
curl -sS -X POST "https://zuzunza.com/api/v1/devconsole/apps" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "My Game Tool",
    "app_type": "game",
    "description": "Jump 게임 연동 도구",
    "redirect_uris": ["https://example.com/callback"],
    "scopes": ["contents:read", "jump:write"]
  }'
```

### GET /devconsole/apps

내 앱 목록을 반환합니다.

### GET /devconsole/apps/{app_id}

앱 상세를 반환합니다.

## API 키

앱별로 키를 발급합니다. 키 원문은 **발급 응답에서 한 번만** 반환되므로 바로 안전하게 보관하세요.

### POST /devconsole/apps/{app_id}/keys

| 필드 | 설명 |
|---|---|
| `key_name` | 키 이름(예: `Production`) |
| `environment` | 환경(예: `live`) |

```bash
curl -sS -X POST "https://zuzunza.com/api/v1/devconsole/apps/$APP_ID/keys" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{"key_name":"Production","environment":"live"}'
```

### GET /devconsole/apps/{app_id}/keys

앱의 키 목록을 반환합니다(원문 없음).

### DELETE /devconsole/keys/{key_id}

키를 폐기합니다.

```bash
curl -sS -X DELETE "https://zuzunza.com/api/v1/devconsole/keys/$KEY_ID" \
  -H "Authorization: Bearer $ACCESS"
```

## 웹훅

### POST /devconsole/apps/{app_id}/webhooks

| 필드 | 설명 |
|---|---|
| `endpoint_url` | 이벤트를 받을 URL |
| `events` | 구독 이벤트 배열(예: `content.published`, `jump.play`) |

등록 응답에 `secret`이 발급됩니다. 수신 서버는 요청의 `X-Shizuku-Secret` 헤더 값을 이 `secret`과 비교해 검증하세요.

```bash
curl -sS -X POST "https://zuzunza.com/api/v1/devconsole/apps/$APP_ID/webhooks" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{"endpoint_url":"https://example.com/webhook","events":["content.published","jump.play"]}'
```

### GET /devconsole/apps/{app_id}/webhooks

앱의 웹훅 목록을 반환합니다.

### POST /devconsole/webhooks/{webhook_id}/test

테스트 이벤트를 전송합니다.

### GET /devconsole/webhooks/{webhook_id}/deliveries

전달 로그를 반환합니다.

## 사용자 키와의 차이

| | `/developer/keys` ([인증](authentication.md#개발자-api-키)) | `/devconsole/apps/{app_id}/keys` |
|---|---|---|
| 단위 | 사용자 | 앱 |
| 용도 | 간단한 서버 간 호출(콘텐츠 생성) | 앱별 키·웹훅 관리 |
| 권한 범위 | 없음 | `scopes` 배열 |

두 방식은 **함께** 운영됩니다.

## 오류

응답은 공통 형식을 따릅니다. 코드 목록은 [오류](errors.md), 호출 한도는 [요청 한도](rate-limits.md)를 참고하세요.

## 관련 문서

- [인증](authentication.md)
- [콘텐츠](contents.md)
- [문서 홈](README.md)
