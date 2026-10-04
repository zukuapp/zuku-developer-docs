---
title: Captcha
description: Self-hosted proof-of-work captcha for ZUKU sign-up and login.
section: API
---

# Captcha

ZUKU uses a self-hosted proof-of-work captcha. Challenges are issued and verified with an HMAC based on `CAPTCHA_HMAC_SECRET`, with no third-party widget (such as reCAPTCHA).
This page covers the sign-up and login gate and the debug verification API.

**Base URL**: `https://zuzunza.com/api/v1` (local: `http://localhost:3001/api/v1`)

## Contents

1. [Overview and environment variables](#1-overview-and-environment-variables)
2. [Challenge](#2-challenge)
3. [Verify](#3-verify)
4. [Auth gate (`zcaptcha_token`)](#4-auth-gate-zcaptcha_token)
5. [Client solving flow](#5-client-solving-flow)
6. [curl and JS/TS examples](#6-curl-and-jsts-examples)
7. [Error codes](#7-error-codes)
8. [Related pages](#8-related-pages)

---

## 1. Overview and environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `CAPTCHA_HMAC_SECRET` | (empty string) | **Required in production.** When empty, challenge/verify fail closed with **503**. |
| `CAPTCHA_MAX_NUMBER` | `100000` | Upper bound of the proof-of-work search (0..=maxnumber) |
| `CAPTCHA_TTL_SECS` | `300` | Expiry (seconds) embedded in the salt |
| `CAPTCHA_DEV_BYPASS` | off | When `1`, allows local hosts plus a fixed bypass token |

Protocol (compatible with the legacy gate):

1. The server issues `salt`, `challenge=hex(SHA-256(salt‖number))`, and `signature=hex(HMAC-SHA256(secret, challenge))`.
2. The client searches `0..=maxnumber` for the `number` that matches `challenge`.
3. The client submits the token `base64(JSON{algorithm,challenge,number,salt,signature})`.

The captcha is unrelated to internal filters or sandboxes. Its purpose is **mitigating authentication abuse**.

---

## 2. Challenge

### `POST /captcha/challenge`

No authentication. No body.

**Success `200`**: `data`:

```json
{
  "algorithm": "SHA-256",
  "challenge": "a1b2…",
  "salt": "zzcp_<hex>.<expiry_unix>",
  "signature": "…",
  "maxnumber": 100000
}
```

| HTTP | code | Condition |
|------|------|-----------|
| 503 | `CAPTCHA_NOT_CONFIGURED` | `CAPTCHA_HMAC_SECRET` not set |
| 405 | — | Disallowed method such as GET |

---

## 3. Verify

### `POST /captcha/verify`

For server-to-server use and debugging. The sign-up and login gate uses the same verifier through the body field `zcaptcha_token`.

**Request**

```json
{
  "token": "<solved-base64-token>",
  "dev_host": "localhost"
}
```

`dev_host` only matters when `CAPTCHA_DEV_BYPASS=1`.

**Success `200`**: `data`: `{ "success": true }`

| HTTP | code | Condition |
|------|------|-----------|
| 503 | `CAPTCHA_NOT_CONFIGURED` | No secret |
| 403 | `CAPTCHA_FAILED` | Signature, expiry, number, or replay check failed |
| 400 | `BAD_REQUEST` | JSON parse failure and similar |

---

## 4. Auth gate (`zcaptcha_token`)

Applies to `POST /auth/register`, `POST /auth/signup`, and `POST /auth/login`:

| Server state | Behavior |
|--------------|----------|
| Secret **not set** | Gate disabled. Sign-up and login are not blocked. |
| Secret **set** | `zcaptcha_token` is required in the body. On failure, **403** `CAPTCHA_FAILED`. |
| `CAPTCHA_DEV_BYPASS=1` + allowed token/host | Development bypass |

Development bypass token (fixed): `__zuzunza_captcha_localhost_bypass__`
(Never enable `CAPTCHA_DEV_BYPASS` in production.)

For the full sign-up and login fields, see [Authentication](authentication.md).

---

## 5. Client solving flow

```
POST /captcha/challenge
        │
        ▼
  worker: for n in 0..=maxnumber
            if sha256(salt + n) == challenge → found
        │
        ▼
  token = btoa(JSON.stringify({ algorithm, challenge, number, salt, signature }))
        │
        ▼
  POST /auth/register { …, zcaptcha_token: token }
```

Recommendations:

- Run the search in a Web Worker so it doesn't block the UI thread.
- On failure (expiry or replay), fetch a new challenge and retry.
- Keep an `X-Request-ID` so support requests can be correlated.

---

## 6. curl and JS/TS examples

### curl: challenge

```bash
curl -sS -X POST "https://zuzunza.com/api/v1/captcha/challenge" \
  -H "Accept-Language: ko-KR" \
  -H "X-Request-Id: $(uuidgen)"
```

### curl: verify

```bash
curl -sS -X POST "https://zuzunza.com/api/v1/captcha/verify" \
  -H "Content-Type: application/json" \
  -d '{"token":"'"$TOKEN"'"}'
```

### JS/TS: challenge → register

```ts
const API = "https://zuzunza.com/api/v1";

type Challenge = {
  algorithm: string;
  challenge: string;
  salt: string;
  signature: string;
  maxnumber: number;
};

async function fetchChallenge(): Promise<Challenge> {
  const res = await fetch(`${API}/captcha/challenge`, { method: "POST" });
  const env = await res.json();
  if (!env.success) throw new Error(`${env.error.code}: ${env.error.message}`);
  return env.data as Challenge;
}

/** Synchronous solver for demo purposes; move it to a Worker in production. */
function solvePoW(c: Challenge): string {
  // A real implementation increments n until hex(SHA-256(salt + String(n))) === c.challenge
  throw new Error("implement PoW solver (see the protocol above)");
}

async function registerWithCaptcha(input: {
  email: string;
  password: string;
  handle: string;
}) {
  const challenge = await fetchChallenge();
  const zcaptcha_token = solvePoW(challenge);
  const res = await fetch(`${API}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json", "Accept-Language": "ko-KR" },
    body: JSON.stringify({ ...input, password_confirm: input.password, zcaptcha_token }),
  });
  const env = await res.json();
  if (!env.success) throw new Error(`${env.error.code}: ${env.error.message}`);
  return env.data;
}
```

For more end-to-end scenarios, see [Examples](examples.md).

---

## 7. Error codes

| code | HTTP | Meaning |
|------|------|---------|
| `CAPTCHA_NOT_CONFIGURED` | 503 | HMAC secret not set (challenge/verify) |
| `CAPTCHA_FAILED` | 403 | Token verification failed or the gate rejected the request |
| `BAD_REQUEST` | 400 | Malformed body |

---

## 8. Related pages

- [Authentication](authentication.md): register/login fields
- [Errors](errors.md): the common envelope
- [Rate limits](rate-limits.md): request limits
- [Examples](examples.md): integrated scenarios
