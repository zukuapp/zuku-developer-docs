---
title: 미디어
description: 파일 업로드, 업로드 파일 제공, JUMP 게임 목록·실행·스트림 API를 설명합니다.
section: API
---

# 미디어

이미지, 영상, 게임 패키지 같은 파일은 먼저 업로드 API로 올리고, 응답의 `url`을 [콘텐츠](contents.md) 생성에 사용합니다. 이 페이지는 업로드, 업로드 파일 제공, JUMP 게임 API를 다룹니다.

**Base URL**: `https://zuzunza.com/api/v1`

> 업로드된 파일은 `/uploads/…` 경로로 제공되며 `/api/v1` 접두사가 **붙지 않습니다**.

## 빠른 예제

```bash
curl -sS -X POST "https://zuzunza.com/api/v1/uploads" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -F "file=@./demo.mp4"
```

## 엔드포인트 요약

| Method | Path | 인증 | 설명 |
|---|---|---|---|
| `POST` | `/api/v1/uploads` | Bearer | 단일 파일 업로드 → `201` |
| `GET` | `/uploads/{yyyy-mm}/{file}` | 없음 | 업로드 파일 제공 |
| `GET` | `/api/v1/jump/games` | 없음 | JUMP 게임 목록 |
| `GET` | `/api/v1/jump/games/{id}` | 없음 | JUMP 게임 상세 |
| `POST` | `/api/v1/jump/games/{id}/play` | Bearer | 실행 경계 확인 |
| `POST` | `/api/v1/jump/games/{id}/stream` | Bearer | IR 바이너리 스트림 |
| `POST` | `/api/v1/jump/games/{id}/swf` | Bearer | 원본 SWF 프록시 |
| `GET` | `/api/v1/contents/{id}/conversion` | 없음 | 변환 상태 |

## POST /api/v1/uploads

단일 파일을 업로드합니다.

| 항목 | 계약 |
|---|---|
| Content-Type | `multipart/form-data` (boundary 필수) |
| 파트 이름 | `file` |
| 인증 | `Authorization: Bearer …` 필수 |
| 형식 판정 | 클라이언트가 보낸 `Content-Type`은 무시하고 파일 시그니처(매직 바이트)로만 판정 |

브라우저에서 `FormData`를 보낼 때는 `Content-Type`을 직접 지정하지 마세요. boundary는 브라우저가 설정합니다.

### 형식과 크기 한도

| `kind` | 한도 | 시그니처 예 |
|---|---|---|
| `image` | 20MB | JPEG `FF D8 FF`, PNG, WEBP(RIFF+WEBP), GIF `GIF8` |
| `video` | 500MB | MP4(`….ftyp…`), WebM/MKV(EBML `1A 45 DF A3`) |
| `wasm` | 50MB | `\0asm` |
| `archive` | 500MB | ZIP `PK\x03\x04` / `PK\x05\x06` |
| `zwf` | 500MB | `ZWF1` / `ZWF2` |
| `swf` | 500MB | Flash `FWS` / `CWS` / `ZWS` — 저장만 합니다. 서버에서 실행하지 않으며, JUMP에서는 Ruffle로 재생합니다. |

원본 파일명은 저장 경로에 쓰지 않고 메타데이터로만 기록합니다.

### 응답

`201 Created`:

```json
{
  "success": true,
  "data": {
    "upload": {
      "url": "/uploads/2026-08/{uuid}.mp4",
      "kind": "video",
      "mime": "video/mp4",
      "size": 1234567,
      "sha256": "…hex…",
      "original_name": "clip.mp4"
    }
  },
  "meta": { "request_id": "…", "timestamp": "…", "version": "v1" }
}
```

| 필드 | 설명 |
|---|---|
| `url` | 콘텐츠 생성에 넣을 공개 경로(`/uploads/…`) |
| `kind` | `image` \| `video` \| `wasm` \| `archive` \| `zwf` \| `swf` (및 `audio`) |
| `mime` | 서버가 판정한 MIME |
| `size` | 바이트 수 |
| `sha256` | 파일 SHA-256(hex) |
| `original_name` | 클라이언트가 보낸 원본 파일명 |
| `package` | ZIP/ZWF일 때만 포함되는 패키지 구조 검사 결과 |

### 오류

| HTTP | code | 상황 |
|---|---|---|
| 400 | `BAD_REQUEST` | multipart가 아니거나 `file` 파트 없음 |
| 401 | `UNAUTHORIZED` | 로그인하지 않음 |
| 413 | `PAYLOAD_TOO_LARGE` | 크기 한도 초과 |
| 415 | `UNSUPPORTED_MEDIA_TYPE` | 지원하지 않는 형식 |

## GET /uploads/{yyyy-mm}/{file}

업로드된 파일을 원래 MIME으로 제공합니다.

- 경로는 `/uploads/…`이며 `/api/v1/uploads/…`가 아닙니다.
- 업로드 디렉터리 밖으로 나가는 경로는 차단됩니다.
- 파일이 없거나 차단되면 `404 NOT_FOUND`(«업로드 파일을 찾을 수 없습니다»).

```bash
curl -sS -O "https://zuzunza.com/uploads/2026-08/a1b2c3….jpg"
```

브라우저나 플레이어에서는 콘텐츠의 `media_url`, `thumbnail_url`을 그대로 쓰면 됩니다.

## JUMP 게임 API

JUMP 카테고리 콘텐츠는 일반 `/contents/{id}`와 별도로 게임 목록과 실행 API를 제공합니다.

### GET /api/v1/jump/games

JUMP 콘텐츠 목록입니다. 공통 페이지네이션 쿼리 `page`, `per_page`를 받으며, 정렬(`sort`)과 필터 쿼리는 [피드](feeds.md#jump-게임-목록-정렬)를 참고하세요.

응답 `data`: `{ "games": Content[], "pagination": … }`. 변환 정보가 있으면 각 항목에 `conversion`이 포함될 수 있습니다.

```bash
curl -sS "https://zuzunza.com/api/v1/jump/games?page=1&per_page=20"
```

### GET /api/v1/jump/games/{id}

JUMP 게임 상세입니다. 응답 `data`: `{ "content": Content }`. `category`가 `jump`가 아니면 `404 CONTENT_NOT_FOUND`입니다. `?include=related,popular`로 추천 목록을 함께 받을 수 있습니다.

### POST /api/v1/jump/games/{id}/play

샌드박스 실행 경계를 확인합니다. Bearer가 필요합니다.

| 필드 | 필수 | 규칙 |
|---|---|---|
| `content_id` | 예 | 경로의 `{id}`와 바이트 단위로 같아야 합니다. ASCII 영숫자, `_`, `-`만 허용, 최대 128자 |

```bash
curl -sS -X POST "https://zuzunza.com/api/v1/jump/games/$GAME_ID/play" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"content_id\":\"$GAME_ID\"}"
```

성공 `data`:

```json
{
  "ok": true,
  "sandbox": {
    "boundary": "OS-unprivileged; syscall_filter(proprietary)",
    "memory_cap_mb": 512,
    "pids_max": 512
  }
}
```

클라이언트는 위 경계와 한도 값만 사용하세요. 샌드박스 내부 구현은 공개하지 않습니다.

| code | 상황 |
|---|---|
| `UNAUTHORIZED` | Bearer 없음 또는 무효 |
| `INVALID_CONTENT_ID` | 허용되지 않는 ID 형식 |
| `CONTENT_ID_MISMATCH` | 경로와 본문 ID 불일치 |
| `CONTENT_NOT_FOUND` | JUMP 콘텐츠 없음 |
| `BAD_REQUEST` | JSON 파싱 실패 |

### POST /api/v1/jump/games/{id}/stream

서버가 SWF 등을 해석해 ZUKU IR(`ZIR\0` 계열) 바이너리로 스트리밍합니다. 클라이언트에 SWF 파서가 없어도 됩니다. Bearer가 필요합니다.

- 성공 응답은 JSON이 아닌 바이너리(`application/octet-stream`)일 수 있습니다. 오류는 JSON 형식으로 올 수 있으니 상태 코드를 먼저 확인하세요.
- 원본 없음: `SOURCE_UNAVAILABLE`
- 해석·인코딩 실패: `SWF_PARSE_FAILED`

```bash
curl -sS -X POST "https://zuzunza.com/api/v1/jump/games/$GAME_ID/stream" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -o game.zir
```

### POST /api/v1/jump/games/{id}/swf

키 입력 등 AVM이 필요한 JUMP를 위해 원본 SWF 바이트를 그대로 전달합니다. 변환하거나 캐시에 쓰지 않습니다. 인증된 클라이언트만 사용할 수 있습니다.

- 원본 없음: `SOURCE_UNAVAILABLE`
- 지원하지 않는 형식: `SWF_PARSE_FAILED`

## GET /api/v1/contents/{id}/conversion

콘텐츠의 변환 상태만 조회합니다. 필드는 [콘텐츠](contents.md#get-contentsidconversion)와 같으며, JUMP 목록·상세에 포함되는 `conversion`과 같은 형식입니다.

```bash
curl -sS "https://zuzunza.com/api/v1/contents/$CONTENT_ID/conversion"
```

## 권장 작업 흐름

1. `POST /api/v1/uploads`로 썸네일, 미디어, ZIP/ZWF/SWF/WASM을 올리고 `upload.url`을 받습니다.
2. `POST /api/v1/contents`에 URL과 카테고리 메타를 넣어 등록합니다([콘텐츠](contents.md)).
3. JUMP는 `play`로 실행 경계를 확인하고, SWF는 클라이언트 Ruffle 또는 필요 시 `stream`/`swf`를 사용합니다.
4. 레거시 변환 상태는 `GET …/conversion`으로 확인합니다.

> 기존 콘텐츠 id의 패키지 파일을 교체하는 API는 **없습니다**. 새 버전은 새 JUMP 초안으로 등록하세요.

## 오류

| code | HTTP | 의미 |
|---|---|---|
| `BAD_REQUEST` | 400 | 요청 형식 오류 |
| `UNAUTHORIZED` | 401 | 인증 필요 |
| `NOT_FOUND` | 404 | 업로드 파일 없음 |
| `CONTENT_NOT_FOUND` | 404 | JUMP 콘텐츠 없음 |
| `PAYLOAD_TOO_LARGE` | 413 | 크기 한도 초과 |
| `UNSUPPORTED_MEDIA_TYPE` | 415 | 지원하지 않는 형식 |
| `INVALID_CONTENT_ID` / `CONTENT_ID_MISMATCH` | — | play 요청 ID 오류 |
| `SOURCE_UNAVAILABLE` / `SWF_PARSE_FAILED` | — | stream/swf 원본·해석 오류 |

## 관련 문서

- [콘텐츠](contents.md) — 생성, 수정, 추천, 게시
- [피드](feeds.md) — JUMP 목록 정렬
- [오류](errors.md) · [변경 이력](changelog.md)
