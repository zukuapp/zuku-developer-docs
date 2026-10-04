---
title: 오류와 응답 형식
description: ZUKU API의 응답 봉투, HTTP 상태, 오류 코드와 요청 한도 헤더, 그리고 ZukuJS CLI의 출력 형식·종료 코드·오류 코드를 정리합니다.
section: Reference
---

# 오류와 응답 형식

이 문서는 두 부분으로 나뉩니다.

- **ZUKU API**: `/api/v1` 응답 봉투, HTTP 상태, 서버 오류 코드
- **ZukuJS CLI**: `zuku`/`zukujs` 명령의 출력 형식, 종료 코드, CLI 오류 코드

## API 응답 봉투

모든 JSON API 응답은 같은 봉투를 사용합니다.

### 성공

```json
{
  "success": true,
  "data": { },
  "meta": {
    "request_id": "…",
    "timestamp": "2026-08-22T00:00:00Z",
    "version": "v1"
  }
}
```

- `data`: 엔드포인트별 페이로드
- `meta.version`: 현재 고정값 `"v1"`(URL `/api/v1`, 헤더 `X-API-Version`과 같은 세대)

### 실패

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "입력값을 확인해 주세요",
    "details": [
      { "field": "title", "message": "제목은 1~100자여야 합니다" }
    ]
  },
  "meta": {
    "request_id": "…",
    "timestamp": "…",
    "version": "v1"
  }
}
```

- `details`는 **필드 단위 검증** 오류가 있을 때만 포함됩니다.
- 단순 실패는 `code`와 `message`만 담습니다.

### 예외

| 상황 | 본문 |
|---|---|
| `204 No Content` | 빈 본문(댓글 삭제, 일부 폐기 API 등) |
| JUMP `stream` / `swf` 성공 | JSON이 아닌 **바이너리**일 수 있음 |
| CORS preflight | `204` |

## HTTP 상태 코드

| HTTP | 대표 상황 |
|---|---|
| `200 OK` | 조회·갱신·토글 성공 |
| `201 Created` | 생성(콘텐츠·업로드·가입·글 등) |
| `204 No Content` | 본문 없는 성공 / OPTIONS |
| `308 Permanent Redirect` | 레거시 JUMP 경로 → 정규 API 안내 |
| `400 Bad Request` | JSON/multipart 형식 오류(`BAD_REQUEST`) |
| `401 Unauthorized` | 세션·토큰 없음 또는 무효(`UNAUTHORIZED`) |
| `403 Forbidden` | 권한 부족(`FORBIDDEN`) |
| `404 Not Found` | 리소스·경로 없음(코드는 리소스별) |
| `409 Conflict` | 중복·상태 충돌(`EMAIL_EXISTS`, `HANDLE_EXISTS`, `ALREADY_AUTHENTICATED`, `LEGACY_ACCOUNT_EXISTS`, `SELF_ACTION_FORBIDDEN` 등) |
| `413 Payload Too Large` | 업로드 한도 초과(`PAYLOAD_TOO_LARGE`) |
| `415 Unsupported Media Type` | 매직 바이트 기준 미지원 형식(`UNSUPPORTED_MEDIA_TYPE`) |
| `422 Unprocessable Entity` | 필드 검증(`VALIDATION_ERROR`, JUMP ID 검증 코드 등) |
| `429 Too Many Requests` | 요청 한도 초과(`RATE_LIMITED`), CLI 게시 한도 초과(`DEPLOY_QUOTA_EXCEEDED`) |
| `500 Internal Server Error` | 서버·DB 오류(`INTERNAL_ERROR`, `DB_UNAVAILABLE`) |
| `501 Not Implemented` | 범위 밖 기능(`NOT_IMPLEMENTED`, 예: `/auth/oauth/{provider}`) |
| `503 Service Unavailable` | 캡차 미설정(`CAPTCHA_NOT_CONFIGURED`), 한도 카운터 확인 불가(`RATE_LIMIT_UNAVAILABLE`), 저장소·업로드 장애 |

## API 오류 코드

서버가 실제로 반환하는 코드입니다. 위임된 moderation·analytics 모듈도 같은 코드를 쓸 수 있습니다.

### 인증·권한

| code | 전형적 HTTP | 의미 |
|---|---|---|
| `UNAUTHORIZED` | 401 | Bearer 세션 또는 유효한 `access_token` 필요 |
| `FORBIDDEN` | 403 | 권한 없음, 관리자 전용 |
| `ALREADY_AUTHENTICATED` | 409 | 이미 로그인한 상태로 회원가입 시도 |
| `SELF_ACTION_FORBIDDEN` | 409 | 자기 자신에 대한 금지된 관리 조작 |

### 검증·요청 형식

| code | 전형적 HTTP | 의미 |
|---|---|---|
| `BAD_REQUEST` | 400 | 요청 본문·multipart 형식 오류 |
| `VALIDATION_ERROR` | 422 | 필드 검증 실패(`details[]` 동반) |
| `INVALID_CONTENT_ID` | 422 | JUMP play ID 문자·길이 규칙 위반 |
| `CONTENT_ID_MISMATCH` | 422 | JUMP 경로 ID와 본문 `content_id`가 다름 |

### 회원가입·계정

| code | 전형적 HTTP | 의미 |
|---|---|---|
| `EMAIL_EXISTS` | 409 | 이메일 중복 |
| `HANDLE_EXISTS` | 409 | handle 중복 |
| `LEGACY_ACCOUNT_EXISTS` | 409 | 기존 ZUKU 계정과 충돌 — 기존 계정 로그인 유도 |

### 캡차

| code | 전형적 HTTP | 의미 |
|---|---|---|
| `CAPTCHA_FAILED` | (검증 실패) | PoW/캡차 실패 |
| `CAPTCHA_NOT_CONFIGURED` | 503 | 캡차 비밀 값 미설정 — 실패 쪽으로 닫힘(fail-closed) |

### 리소스 없음

| code | 전형적 HTTP | 대상 |
|---|---|---|
| `NOT_FOUND` | 404 | 일반(세션·캡차 경로·업로드 파일 등) |
| `CONTENT_NOT_FOUND` | 404 | 콘텐츠 |
| `COMMENT_NOT_FOUND` | 404 | 댓글 |
| `POST_NOT_FOUND` | 404 | 커뮤니티 글 |
| `CONVERSATION_NOT_FOUND` | 404 | DM 대화 |
| `USER_NOT_FOUND` | 404 | 회원 |
| `NOTIFICATION_NOT_FOUND` | 404 | 알림 |
| `API_KEY_NOT_FOUND` | 404 | 개발자 API 키 |
| `ROUTE_NOT_FOUND` | 404 | 일치하는 API 경로 없음 |

### 미디어·JUMP

| code | 전형적 HTTP | 의미 |
|---|---|---|
| `UNSUPPORTED_MEDIA_TYPE` | 415 | 지원하지 않는 업로드 형식 |
| `PAYLOAD_TOO_LARGE` | 413 | 업로드 크기 한도 초과 |
| `SOURCE_UNAVAILABLE` | (재생 실패) | 재생 가능한 원본 없음 |
| `SWF_PARSE_FAILED` | (재생 실패) | SWF 해석·IR 인코딩 실패 또는 비지원 형식 |

### 게임 패키지 업로드

`zuku upload`가 `POST /api/v1/uploads`·`POST /api/v1/contents`에서 받아 그대로 보고하는 코드입니다. 모든 422가 같은 원인이라고 가정하지 마세요.

| code | 전형적 HTTP | 의미 |
|---|---|---|
| `BAD_REQUEST` / `UNSAFE_PACKAGE` / `INVALID_PACKAGE` | 400 | 요청 형식 오류 / 안전하지 않은 패키지 / 잘못된 패키지 |
| `UNAUTHORIZED` | 401 | 계정 연결 필요 |
| `ACCOUNT_SUSPENDED` / `GAME_UPLOAD_UNSUPPORTED` / `CSRF_REJECTED` | 403 | 계정 정지 / 게임 업로드 미지원 / CSRF 거부 |
| `PAYLOAD_TOO_LARGE` | 413 | 크기 초과(요청 전체 500 MiB 이하) |
| `UNSUPPORTED_MEDIA_TYPE` | 415 | 지원하지 않는 형식 |
| `VALIDATION_ERROR` / `MALWARE_DETECTED` | 422 | 필드 검증 실패 / 악성 코드 검출 |
| `INTERNAL_ERROR` | 500 | 내부 처리 실패 |
| `STORAGE_UNAVAILABLE` / `UPLOAD_UNAVAILABLE` | 503 | 저장소 / 업로드 기능 일시 불가 |

### 요청 한도

| code | 전형적 HTTP | 의미 |
|---|---|---|
| `RATE_LIMITED` | 429 | 요금제·요청 종류별 한도 초과 |
| `RATE_LIMIT_UNAVAILABLE` | 503 | 한도 카운터를 확인할 수 없음 |
| `DEPLOY_QUOTA_EXCEEDED` | 429 | CLI 프로덕션 게시 한도(계정당 6시간 3회) 초과, `Retry-After` 포함 |

### 인프라·기타

| code | 전형적 HTTP | 의미 |
|---|---|---|
| `DB_UNAVAILABLE` | 500 | DB 풀·접속 불가 |
| `INTERNAL_ERROR` | 500 | 내부 처리 실패 |
| `NOT_IMPLEMENTED` | 501 | 미구현(예: OAuth provider) |

> 웹 클라이언트의 `ApiFailure`는 봉투 해석 실패 시 `INVALID_RESPONSE`, 빈 본문 오류 시 `HTTP_ERROR`를 **클라이언트 쪽에서** 만들 수 있습니다. 서버가 보내는 코드가 아닙니다.

## `details[]` 필드 오류

`VALIDATION_ERROR` 등에서 사용합니다.

```json
"details": [
  { "field": "title", "message": "제목은 1~100자여야 합니다" },
  { "field": "tags", "message": "태그는 최대 10개입니다" }
]
```

콘텐츠 생성에서 흔한 `field` 값은 `title`, `description`, `tags`, `age_rating`, `type`입니다. UI는 `details`를 필드별 인라인 오류로 표시하고, 없으면 `error.message`를 토스트나 배너로 보여 주면 됩니다.

## 응답 헤더

제한 대상 요청에는 실제로 측정한 요청 한도 헤더가 붙습니다. 성공 응답은 해당 종류의 기본 구간을, `429`는 실제로 거절한 조건의 구간을 표시합니다.

| 헤더 | 동작 |
|---|---|
| `X-API-Version` | 고정 `v1` |
| `X-RateLimit-Limit` | 표시된 구간의 허용 횟수 |
| `X-RateLimit-Remaining` | 요청 이후 남은 횟수 |
| `X-RateLimit-Reset` | 구간 종료 Unix epoch 초 |
| `X-RateLimit-Window` | 구간 길이(초) |
| `X-RateLimit-Scope` / `X-RateLimit-Plan` | 요청 종류 / 서버가 검증한 요금제(IP 보호에서 인증 전이면 `unknown`) |
| `Retry-After` | `429`의 대기 시간(초) |

`429 RATE_LIMITED`의 `error.details`에는 `plan`, `scope`, `limit`, `remaining`, `window_seconds`, `retry_after_seconds`, `reset_at`, `upgrade_available`이 들어갑니다. `reset_at`은 Unix epoch 초입니다. 카운터를 확인할 수 없으면 `503 RATE_LIMIT_UNAVAILABLE`을 반환합니다. 기존 MFA·채팅·제공자 제한은 각자의 오류 코드와 재시도 안내를 유지합니다.

한도 수치와 운영 적용 조건은 [요청 한도](rate-limits.md)를 보세요. 이전 릴리스의 더미 헤더와 새 정책을 구분하려면 실제 응답과 `GET /api/v1/rate-limits/policy`를 확인합니다. CORS·API 버전 헤더는 기존 계약을 유지하며, 개인 한도 정보나 429 응답은 공유 캐시에 저장하지 않습니다.

## 클라이언트 처리 예시

```ts
class ApiFailure extends Error {
  constructor(
    public code: string,
    message: string,
    public status: number,
    public details?: { field: string; message: string }[],
  ) {
    super(message);
    this.name = 'ApiFailure';
  }
}

async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`/api/v1${path}`, {
    ...init,
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers ?? {}),
    },
  });

  if (res.status === 204) return undefined as T;

  const envelope = await res.json();
  if (!envelope.success) {
    throw new ApiFailure(
      envelope.error.code,
      envelope.error.message,
      res.status,
      envelope.error.details,
    );
  }
  return envelope.data as T;
}

try {
  await apiFetch('/contents', { method: 'POST', body: JSON.stringify(payload), headers: {
    Authorization: `Bearer ${token}`,
  }});
} catch (e) {
  if (e instanceof ApiFailure) {
    switch (e.code) {
      case 'UNAUTHORIZED':
        // 로그인 유도
        break;
      case 'VALIDATION_ERROR':
        // e.details로 폼 필드 표시
        break;
      case 'EMAIL_EXISTS':
      case 'HANDLE_EXISTS':
        // 가입 폼 전용 메시지
        break;
      case 'CAPTCHA_FAILED':
        // 캡차 다시 풀기
        break;
      case 'RATE_LIMITED':
        // Retry-After 만큼 대기
        break;
      case 'DB_UNAVAILABLE':
      case 'INTERNAL_ERROR':
        // 조회 요청만 잠시 후 재시도
        break;
      default:
        console.error(e.code, e.message, e.status);
    }
  }
}
```

POST·업로드·결제·AI 생성 같은 변경 요청은 자동으로 반복하지 말고, 작업 상태를 먼저 확인하세요.

## CLI 오류

### 출력 형식 (`zuku-command/1`)

| 경우 | 스트림 | 형식 |
|---|---|---|
| 성공, `--json` | stdout | `{"success":true,"data":...,"meta":{...}}` 한 줄 |
| 성공, 일반 | stdout | 봉투 없는 출력 |
| 실패, `--json` | stderr | `{"success":false,"error":{"code","message"},"meta":{...}}` 한 줄 |
| 실패, 일반 | stderr | `CODE: message` |

서버 오류는 HTTP 상태와 검증된 API 오류 코드로 보고하며, 원격 응답 전문이나 헤더, 토큰은 출력하지 않습니다. `dev`·`build` 같은 웹 프레임워크 전달 명령은 이 봉투를 쓰지 않고 프레임워크 자체 규칙을 따릅니다.

### 종료 코드

| 코드 | 의미 |
|---|---|
| 0 | 성공 |
| 1 | 실패(검증·패키지·자격 증명·API 오류 등) |
| 2 | 인수 오류(`INVALID_INPUT`), 알 수 없는 명령(`UNKNOWN_COMMAND`) |
| 130 | 사용자 취소(`COMMAND_CANCELLED`, Ctrl+C) |

### 공통·계정

| code | 의미 |
|---|---|
| `INVALID_INPUT` | 잘못되거나 알 수 없는 옵션·값. 파일·네트워크를 건드리기 전에 거부 |
| `UNKNOWN_COMMAND` | 알 수 없는 명령 |
| `COMMAND_CANCELLED` | 사용자가 취소함 |
| `FRAMEWORK_UNAVAILABLE` | 웹 프레임워크 명령을 전달할 `zukujs` 프레임워크 패키지가 없음 |
| `ZUKU_ACCOUNT_MIGRATION_REQUIRED` | 이전 시험용 서버의 계정 기록. `zuku login zuku`로 다시 승인 |

### 제공자 인증

| code | 의미 |
|---|---|
| `AUTH_SECRET_ARGUMENT` | 비밀 값을 명령 인수로 전달함(값은 오류에 다시 나오지 않음) |
| `AUTH_INPUT_REQUIRED` | 비대화형에서 입력 방법이 없음 / 입력 시간 초과 |
| `AUTH_SECRET_INVALID` | 줄바꿈·제어 문자·크기 초과 |
| `AUTH_REQUIRED` | 선택한 제공자의 자격 증명이 없음 |
| `AUTH_SESSION_CHANGED` | 시작 후 인증·연결 설정이나 계정이 바뀜 |
| `AUTH_EXPERIMENTAL_OPT_IN` | Codex 최초 연결 동의와 `--experimental`이 없음 |
| `ZUKU_GENERATE_SCOPE_REQUIRED` | ZUKU 계정에 명시적 생성 권한(`games:generate`)이 없음 |
| `AUTH_DELEGATE_UNAVAILABLE` | 계정 명령·로그아웃 연동을 이 설치본에서 쓸 수 없음 |
| `SECRET_STORE_UNAVAILABLE` / `SECRET_STORE_UNSAFE` | 보호 저장소 없음 / 파일 권한·소유자·링크 안전성 위반 |

### 게임 에이전트·게시

| code | 의미 |
|---|---|
| `AGENT_REQUEST_REQUIRED` | 비대화형 실행에 요청이 없음 |
| `AGENT_BUSY` | 같은 디렉터리에서 다른 에이전트 실행이 진행 중 |
| `AGENT_SKILL_INTEGRITY` | 함께 배포된 게임 스킬 팩이 고정값과 다름. 모델 호출 전에 중단 |
| `AGENT_GATE_FAILED` | 생성 결과가 코드 게이트를 통과하지 못함 |
| `AGENT_ARTIFACT_UNSAFE` | 경로 탈출·명령 실행·네트워크·비밀 값 감지. 아무것도 쓰지 않음 |
| `AGENT_PLAYTEST_FAILED` | 실제 브라우저 플레이테스트 실패. 패키지·업로드·게시하지 않음 |
| `AGENT_PLAYTEST_UNAVAILABLE` | 플레이테스트용 브라우저를 쓸 수 없음 |
| `AGENT_PLAYTEST_SANDBOX` | Chromium 샌드박스를 시작할 수 없음(root 실행 등) |
| `AGENT_SOURCE_CHANGED` | `--resume` 대상의 소스가 기록과 다름 |
| `AGENT_PUBLISH_OUTCOME_UNKNOWN` | 게시 결과 불명. 자동 재시도하지 않음 |
| `AGENT_RECOVERY_REQUIRED` | 게시 상태를 서버에서 조회할 수 없어 멈춤 |
| `DEPLOY_QUOTA_EXCEEDED` | 계정당 6시간 3회 게시 한도 초과(`retry_after` 포함) |

에이전트 오류 메시지에는 모델·제공자·API·브라우저 원문이나 토큰이 들어가지 않습니다. 대처 방법은 [게임 개발 에이전트](cli/agent.md)와 [패키징과 게시](cli/publishing.md)를 보세요.

## 관련 문서

- [요청 한도](rate-limits.md)
- [변경 이력](changelog.md) — `meta.version`, `X-API-Version`
- [인증](authentication.md)
- [명령 참조](cli/commands.md)
