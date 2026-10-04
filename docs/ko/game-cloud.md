---
title: Game Cloud
description: 프로젝트 단위 지갑, 클라우드 변수, 세이브, 결제(IAP), 서버 함수, 요금, 전용 VM, 대시보드 API를 설명합니다.
section: API
---

# Game Cloud

ZUKU Game Cloud는 게임 **프로젝트** 단위로 격리된 지갑, 클라우드 변수, 세이브를 제공하고, 개발 중인 결제·서버 함수 인터페이스를 함께 제공합니다.

> **현재 지원 범위**: Pay confirm은 외부 결제사나 영수증을 검증하지 않습니다. 실제 결제 완료 증빙으로 사용하지 마세요.

**Base URL**: `https://zuzunza.com/api/v1/cloud`

**인증**: 모든 엔드포인트에 `Authorization: Bearer <session_token>`이 필요합니다. ZUKU 세션을 관리하는 신뢰할 수 있는 앱에서 호출하고, 게임 샌드박스에 계정 토큰을 넘기지 마세요. 별도 SDK 설치 없이 HTTP로 호출합니다.

## 빠른 예제

```bash
curl -sS -X POST "https://zuzunza.com/api/v1/cloud/saves/save" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{"projectId":"'"$PROJECT"'","slot":"default","data":{"level":3,"inventory":["sword"]}}'
```

## 엔드포인트 요약

경로는 모두 `/api/v1/cloud` 기준입니다.

| 기능(레거시 이름) | Method | Path | 설명 |
|---|---|---|---|
| 프로젝트 | `POST` | `/projects` | 프로젝트 생성 |
| 프로젝트 | `GET` | `/projects` | 프로젝트 목록 |
| Economy (ZCloud Economy) | `GET` | `/economy/balance` | `POINT` · `CASH_KRW` 지갑 |
| Vars (ZVM) | `POST` | `/vars/get` | 변수 읽기 |
| Vars (ZVM) | `POST` | `/vars/mutate` | 변수 변경 |
| Saves (ZASE) | `POST` | `/saves/save` | 세이브 저장 |
| Saves (ZASE) | `POST` | `/saves/load` | 세이브 불러오기 |
| Saves (ZASE) | `GET` | `/saves/list` | 슬롯 목록 |
| Pay | `GET` | `/pay/products` | 상품 목록 |
| Pay | `POST` | `/pay/session` | 구매 세션 생성 |
| Pay | `POST` | `/pay/confirm` | 결제 확인 |
| Functions (WebFunc) | `POST` | `/functions` | 함수 등록·수정 |
| Functions (WebFunc) | `POST` | `/functions/{id}/publish` | 함수 게시 |
| Functions (WebFunc) | `POST` | `/functions/{id}/invoke` | 함수 호출 |
| Billing | `GET` | `/billing/catalog` | 요금 카탈로그 |
| Billing | `GET` | `/billing/account` | 프로젝트 요금 계정 |
| Billing | `POST` | `/billing/limit` | 지출 한도 설정 |
| VM | `POST` | `/vm` | 전용 VM 요청 |
| VM | `GET` | `/vm` | VM 조회 |
| VM | `POST` | `/vm/start` · `/vm/stop` · `/vm/delete` | VM 수명주기 |
| Dashboard | `GET` | `/dashboard/summary` | 사용량 요약 |

## 프로젝트

Game Cloud 데이터는 프로젝트 단위로 격리됩니다.

### POST /cloud/projects

| 필드 | 설명 |
|---|---|
| `name` | 프로젝트 이름 |
| `description` | 설명 |
| `jump_content_id` | 연결할 JUMP 콘텐츠 id |

```bash
curl -sS -X POST "https://zuzunza.com/api/v1/cloud/projects" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{"name":"내 RPG","description":"온라인 멀티 RPG","jump_content_id":"cnt_jump_abc123"}'
```

### GET /cloud/projects

내 프로젝트 목록을 반환합니다.

## Economy (지갑)

### GET /cloud/economy/balance?projectId={uuid}

```json
{ "success": true, "data": { "POINT": 1500, "CASH_KRW": 0 } }
```

| 필드 | 설명 |
|---|---|
| `POINT` | 게임 내 재화 |
| `CASH_KRW` | 지갑 잔액 필드. 실제 결제·환전·입금이 검증되었다는 뜻은 아닙니다. |

## Vars (클라우드 변수)

`global`(전체 공유) 또는 `user`(플레이어별) 스코프의 변수입니다. 재화(currency) 스코프는 클라이언트에서 변경할 수 없습니다(임의 발행 방지).

### POST /cloud/vars/get

| 필드 | 설명 |
|---|---|
| `projectId` | 프로젝트 UUID |
| `scope` | `global` \| `user` |
| `key` | 변수 이름 |

### POST /cloud/vars/mutate

| 필드 | 설명 |
|---|---|
| `projectId` | 프로젝트 UUID |
| `scope` | `global` \| `user` |
| `key` | 변수 이름 |
| `op` | `set` \| `incr` \| `decr` \| `max` \| `min` \| `cas` |
| `num` | 연산 값 |

```bash
curl -sS -X POST "https://zuzunza.com/api/v1/cloud/vars/mutate" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{"projectId":"'"$PROJECT"'","scope":"user","key":"high_score","op":"max","num":9999}'
```

## Saves (클라우드 세이브)

인라인 JSON 세이브이며 슬롯당 **256KB**까지 저장할 수 있습니다.

| Method | Path | 본문 / 쿼리 |
|---|---|---|
| `POST` | `/cloud/saves/save` | `{ projectId, slot, data }` |
| `POST` | `/cloud/saves/load` | `{ projectId, slot }` |
| `GET` | `/cloud/saves/list` | `?projectId={uuid}` |

```bash
curl -sS -X POST "https://zuzunza.com/api/v1/cloud/saves/load" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{"projectId":"'"$PROJECT"'","slot":"slot1"}'
```

## Pay (IAP)

| Method | Path | 본문 / 쿼리 | 설명 |
|---|---|---|---|
| `GET` | `/cloud/pay/products` | `?projectId={uuid}` | 상품 목록 |
| `POST` | `/cloud/pay/session` | `{ projectId, productId }` | 구매 세션 생성. TTL 10분, `status: pending` |
| `POST` | `/cloud/pay/confirm` | `{ sessionId }` | 세션을 `paid`로 확인 |

confirm은 외부 결제사나 영수증을 검증하지 않으므로 실제 결제 증빙으로 쓰지 마세요.

## Functions (서버 함수)

함수 소스를 등록하고 Deno 런타임에서 실행합니다. 함수마다 네트워크가 분리되고 파일시스템은 최소 읽기 전용입니다. 격리 환경을 갖추지 못하면 실행을 거부합니다.

| 한도 | 값 |
|---|---|
| 실행 시간 | 2초 |
| 메모리 | 128MiB |
| 프로세스 | 64개 |

| Method | Path | 본문 |
|---|---|---|
| `POST` | `/cloud/functions` | `{ projectId, name, sourceCode }` |
| `POST` | `/cloud/functions/{id}/publish` | `{ projectId }` |
| `POST` | `/cloud/functions/{id}/invoke` | `{ projectId, input }` — 게시(published)된 함수만 |

```bash
curl -sS -X POST "https://zuzunza.com/api/v1/cloud/functions" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{"projectId":"'"$PROJECT"'","name":"grantReward","sourceCode":"export default async function(input) { return { ok: true, input }; }"}'
```

## Cloud Billing

| Method | Path | 설명 |
|---|---|---|
| `GET` | `/cloud/billing/catalog` | 요금 카탈로그(`rate_card_version`, `billing_unit`, `rate_krw`) |
| `GET` | `/cloud/billing/account?projectId={uuid}` | 프로젝트 요금 계정 |
| `POST` | `/cloud/billing/limit` | `{ projectId, spendLimitKrw }` — 프로젝트 지출 한도 |

- 계량 항목: API 요청, CPU-ms, RAM MB-ms, 디스크 GB-hours·읽기·쓰기, 동시 접속 분, KT/KR egress, Global egress. 브라우저는 계량값을 제출할 수 없습니다.
- 유료 플랜에서 포함량을 넘기려면 프로젝트별 한도를 먼저 설정해야 합니다. `spendLimitKrw: 0`은 초과 사용 차단입니다.
- Cloud Free는 계량 항목 하나라도 80%에 도달하면 완만한 QoS, 90%부터 강한 QoS가 적용되며, 100% 소진 후 다음 요청부터 차단됩니다.

```bash
curl -sS -X POST "https://zuzunza.com/api/v1/cloud/billing/limit" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{"projectId":"'"$PROJECT"'","spendLimitKrw":50000}'
```

## 게임 전용 VM

Cloud Scale과 Game Dedicated 요금제는 고정 사양의 격리 KVM 서버를 요청할 수 있습니다. 요청은 먼저 dry-run 검토 대기열에 들어갑니다.

| Method | Path | 본문 / 쿼리 |
|---|---|---|
| `POST` | `/cloud/vm` | `{ projectId, idempotencyKey }` |
| `GET` | `/cloud/vm` | `?projectId={uuid}` |
| `POST` | `/cloud/vm/start` | `{ projectId, idempotencyKey }` |
| `POST` | `/cloud/vm/stop` | `{ projectId, idempotencyKey }` |
| `POST` | `/cloud/vm/delete` | `{ projectId, idempotencyKey }` |

요청마다 고유한 `idempotencyKey`를 사용하세요. VM 요금제가 만료되면 새 VM을 만들거나 중지된 VM을 다시 시작할 수 없습니다.

```bash
curl -sS -X POST "https://zuzunza.com/api/v1/cloud/vm" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{"projectId":"'"$PROJECT"'","idempotencyKey":"create-attempt-1"}'
```

## 대시보드

### GET /cloud/dashboard/summary?projectId={uuid}&days=30

프로젝트 소유자만 조회할 수 있으며, 이벤트별 사용량 내역을 반환합니다.

## 오류

응답은 공통 형식 `{ success, data | error, meta }`를 따릅니다. 오류 코드 목록은 [오류](errors.md), 호출 한도는 [요청 한도](rate-limits.md)를 참고하세요.

## 관련 문서

- [콘텐츠](contents.md) — JUMP 게임 등록
- [인증](authentication.md)
- [예제](examples.md)
