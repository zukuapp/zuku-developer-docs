---
title: ZUKU Game Cloud
description: Per-project cloud variables, saves, and wallets, plus in-development payment and server function interfaces.
section: API
---

# ZUKU Game Cloud

Game Cloud provides per-project variables, saves, and wallets, along with payment and server function interfaces that are still in development.

> **Warning: current scope.** Separately from the variables and saves APIs, Pay confirm does not verify anything with an external payment provider or receipt. Don't use it as proof that a real payment was completed.

This page covers the Game Cloud HTTP API only. The newer native AI APIs are not covered here.

## Contents

1. [Overview](#1-overview)
2. [Projects](#2-projects)
3. [Economy (wallet)](#3-economy-wallet)
4. [Vars (cloud variables)](#4-vars-cloud-variables)
5. [Saves (cloud saves)](#5-saves-cloud-saves)
6. [Pay (IAP)](#6-pay-iap)
7. [Functions (server functions)](#7-functions-server-functions)
8. [Cloud Billing](#8-cloud-billing)
9. [Dedicated game VMs](#9-dedicated-game-vms)
10. [Dashboard](#10-dashboard)
11. [HTTP integration example](#http-integration-example)

---

## 1. Overview

| Legacy | zuku v1 | Description |
|--------|---------|-------------|
| ZCloud Economy | `/cloud/economy/balance` | POINT · CASH_KRW wallet |
| ZVM | `/cloud/vars/*` | Global/user scoped variables |
| ZASE | `/cloud/saves/*` | Versioned save slots |
| Pay | `/cloud/pay/*` | IAP products, sessions, confirmation |
| WebFunc | `/cloud/functions/*` | Server function CRUD and invoke |

**Authentication**: every endpoint requires `Authorization: Bearer <session_token>`.

**Base URL**: `https://zuzunza.com/api/v1/cloud`

---

## 2. Projects

Game Cloud is isolated per **project**.

### Create a project

```http
POST /api/v1/cloud/projects
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "My RPG",
  "description": "Online multiplayer RPG",
  "jump_content_id": "cnt_jump_abc123"
}
```

### List projects

```http
GET /api/v1/cloud/projects
Authorization: Bearer <token>
```

---

## 3. Economy (wallet)

```http
GET /api/v1/cloud/economy/balance?projectId=<uuid>
Authorization: Bearer <token>
```

**Response**:

```json
{
  "success": true,
  "data": {
    "POINT": 1500,
    "CASH_KRW": 0
  }
}
```

- `POINT`: in-game currency
- `CASH_KRW`: wallet balance field. It does not mean that any real payment, exchange, or deposit has been verified.

---

## 4. Vars (cloud variables)

Same concept as the legacy ZVM. **The currency scope cannot be changed from the client** (to prevent self-minting).

### Read

```http
POST /api/v1/cloud/vars/get
Content-Type: application/json

{
  "projectId": "<uuid>",
  "scope": "user",
  "key": "high_score"
}
```

### Mutate

```http
POST /api/v1/cloud/vars/mutate
Content-Type: application/json

{
  "projectId": "<uuid>",
  "scope": "user",
  "key": "high_score",
  "op": "max",
  "num": 9999
}
```

**op**: `set` · `incr` · `decr` · `max` · `min` · `cas`

**scope**: `global` (shared by everyone) · `user` (per player)

---

## 5. Saves (cloud saves)

The legacy ZASE. Inline JSON, with a limit of **256KB** per slot.

### Save

```http
POST /api/v1/cloud/saves/save

{
  "projectId": "<uuid>",
  "slot": "slot1",
  "data": { "level": 5, "inventory": ["sword", "potion"] }
}
```

### Load

```http
POST /api/v1/cloud/saves/load

{
  "projectId": "<uuid>",
  "slot": "slot1"
}
```

### List slots

```http
GET /api/v1/cloud/saves/list?projectId=<uuid>
```

---

## 6. Pay (IAP)

### List products

```http
GET /api/v1/cloud/pay/products?projectId=<uuid>
```

### Create a purchase session

```http
POST /api/v1/cloud/pay/session

{
  "projectId": "<uuid>",
  "productId": "<product-uuid>"
}
```

Session TTL: **10 minutes**. `status: pending` → `paid` (after confirm).

### Confirm payment

```http
POST /api/v1/cloud/pay/confirm

{
  "sessionId": "<session-uuid>"
}
```

---

## 7. Functions (server functions)

Register function source code and run it on a real Deno runtime. Each function gets its own isolated network and a minimal read-only filesystem, with a 2-second execution time limit, a 128MiB memory limit, and a cap of 64 processes. If the required sandbox isn't available, execution is refused.

### Register or update a function

```http
POST /api/v1/cloud/functions

{
  "projectId": "<uuid>",
  "name": "grantReward",
  "sourceCode": "export default async function(input) { return { ok: true, input }; }"
}
```

### Publish a function

```http
POST /api/v1/cloud/functions/<id>/publish

{ "projectId": "<uuid>" }
```

### Invoke a function (published state)

```http
POST /api/v1/cloud/functions/<id>/invoke

{
  "projectId": "<uuid>",
  "input": { "amount": 100 }
}
```

---

## 8. Cloud Billing

```http
GET /api/v1/cloud/billing/catalog
GET /api/v1/cloud/billing/account?projectId=<uuid>
```

API requests, CPU-ms, RAM MB-ms, disk GB-hours, disk reads and writes, concurrent connection minutes, KT/KR egress, and Global egress are each metered separately. Costs are calculated from the catalog's `rate_card_version`, `billing_unit`, and `rate_krw`. Browsers cannot submit meter values.

On a paid plan, you must set a per-project limit before usage can exceed the included amount. `0` blocks any overage.

```http
POST /api/v1/cloud/billing/limit

{ "projectId": "<uuid>", "spendLimitKrw": 50000 }
```

On Cloud Free, gentle QoS applies once any single meter reaches 80%, strong QoS from 90%, and requests are blocked starting with the next request after 100% is used.

## 9. Dedicated game VMs

Cloud Scale and Game Dedicated can request isolated KVM servers with a fixed shape. Requests first go into a dry-run review queue.

```http
POST /api/v1/cloud/vm

{ "projectId": "<uuid>", "idempotencyKey": "create-attempt-1" }
```

```http
GET /api/v1/cloud/vm?projectId=<uuid>
POST /api/v1/cloud/vm/start
POST /api/v1/cloud/vm/stop
POST /api/v1/cloud/vm/delete
```

Lifecycle POST bodies use `projectId` and a unique `idempotencyKey`. With an expired VM plan, you can't create a new VM or restart a stopped one.

## 10. Dashboard

```http
GET /api/v1/cloud/dashboard/summary?projectId=<uuid>&days=30
```

Only the project owner can view it. Returns a usage breakdown per event.

---

<span id="jump-sdk-integration"></span>

## HTTP integration example

Call these APIs from a trusted app that manages the ZUKU session. Never pass account tokens into the game sandbox. The example below uses the HTTP API directly and does not assume any npm SDK installation.

```javascript
await fetch("/api/v1/cloud/saves/save", {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${accessToken}`,
    "Content-Type": "application/json"
  },
  body: JSON.stringify({ projectId, slot: "default", data: gameState })
});
```

See [Errors](errors.md) and [Rate limits](rate-limits.md) for shared behavior, and [Examples](examples.md) for an end-to-end Game Cloud scenario.
