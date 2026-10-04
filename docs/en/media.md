---
title: Media, Uploads, and Jump
description: Upload files, serve them from /uploads, and use the Jump game play, stream, and SWF endpoints.
section: API
---

# Media, Uploads, and Jump

> The upload API prefix is `/api/v1`. **Static files are served only from `/uploads/…`**, which does **not** have the `/api/v1` prefix.

---

## POST `/api/v1/uploads`

**Single-file** upload for the one-drop studio.

| Item | Contract |
|---|---|
| Content-Type | `multipart/form-data` (boundary required) |
| Part field name | `file` |
| Auth | **Required**: `Authorization: Bearer …` |
| MIME detection | The client `Content-Type` is **ignored**. Detection uses **magic bytes** only. |

### Size limits

| Type (`kind`) | Limit | Magic bytes |
|---|---|---|
| `image` | **20MB** | JPEG `FF D8 FF`, PNG, WEBP (RIFF+WEBP), GIF `GIF8` |
| `video` | **500MB** | MP4 (`….ftyp…`), WebM/MKV (EBML `1A 45 DF A3`) |
| `wasm` | **50MB** | `\0asm` |
| `archive` | **500MB** | ZIP `PK\x03\x04` / `PK\x05\x06` |
| `zwf` | **500MB** | `ZWF1` / `ZWF2` (ZUKBOX) |
| `swf` | **500MB** | Flash `FWS` / `CWS` / `ZWS`. **Stored as media only.** The server never executes SWF; Jump plays it with Ruffle. |

Unsupported format → `415` · `UNSUPPORTED_MEDIA_TYPE`.
Over the limit → `413` · `PAYLOAD_TOO_LARGE`.
Not multipart, or no `file` part → `400` · `BAD_REQUEST`.
Not logged in → `401` · `UNAUTHORIZED`.

Files are stored under a month folder with a UUID file name (`/uploads/{yyyy-mm}/{uuid}.{ext}`). The original file name is recorded as metadata only and never used in the path.

### Success response (`201 Created`)

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

| Field | Description |
|---|---|
| `url` | Public path (`/uploads/…`) to use when creating content |
| `kind` | `image` \| `video` \| `wasm` \| `archive` \| `zwf` \| `swf` (and `audio`) |
| `mime` | MIME type mapped by the server |
| `size` | Size in bytes |
| `sha256` | SHA-256 hex of the file |
| `original_name` | Original file name sent by the client |
| `package` | Only for accepted ZIP/ZWF files: the result of the structure scan. Absent for `swf`, `image`, `video`, and others. |

### curl (multipart)

```bash
curl -sS -X POST "https://zuzunza.com/api/v1/uploads" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -F "file=@./demo.mp4"
```

Image example:

```bash
curl -sS -X POST "https://zuzunza.com/api/v1/uploads" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -F "file=@./thumb.png"
```

### JS/TS (`FormData`)

```ts
async function uploadFile(token: string, file: File) {
  const form = new FormData();
  form.append('file', file); // The field name must be "file"

  const res = await fetch('/api/v1/uploads', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
      // Don't set Content-Type yourself; the browser sets the boundary
    },
    body: form,
  });

  const envelope = await res.json();
  if (!envelope.success) {
    throw Object.assign(new Error(envelope.error.message), {
      code: envelope.error.code,
      status: res.status,
    });
  }
  return envelope.data.upload as {
    url: string;
    kind: string;
    mime: string;
    size: number;
    sha256: string;
    original_name: string;
  };
}

// Usage: const up = await uploadFile(token, input.files[0]);
// createContent({ …, media_url: up.url, thumbnail_url: up.url })
```

---

## GET `/uploads/{yyyy-mm}/{file}`

Serves uploaded files statically with their **original MIME type**.

- Path prefix: **`/uploads/…` only** (not `/api/v1/uploads/…`)
- Served without a database connection, so it is isolated from connection pool exhaustion and database outages
- Path traversal outside the upload root is blocked
- Missing or blocked → `404` · `NOT_FOUND` ("Upload file not found")

Example: `GET /uploads/2026-08/a1b2c3….jpg`

In browsers and players, use the content's `media_url` / `thumbnail_url` as is.

---

## Jump game API

Jump category content has its own game listing and execution boundary, separate from the general `/contents/{id}`.

### GET `/api/v1/jump/games`

Lists Jump content (`category=jump`). Query: `page` / `per_page` (common pagination). See [Feeds](feeds.md#jump-game-list-sorting) for sorting and additional list queries.

**Response `data`**: `{ "games": Content[], "pagination": … }`
Each item may include `conversion` when conversion information exists.

### GET `/api/v1/jump/games/{id}`

A single Jump item. If `category` is not `jump`, it is treated as not found → `404` · `CONTENT_NOT_FOUND`.

**Response `data`**: `{ "content": Content }`

### POST `/api/v1/jump/games/{id}/play` (authentication required)

Checks the sandbox execution boundary. Body:

```json
{ "content_id": "{id}" }
```

The path `{id}` and the body `content_id` must be **byte-for-byte identical**, use only ASCII letters, digits, `_`, and `-`, and be at most 128 characters long.

| Failure code | Condition |
|---|---|
| `UNAUTHORIZED` | Missing or invalid Bearer token |
| `INVALID_CONTENT_ID` | Unsafe ID |
| `CONTENT_ID_MISMATCH` | Path ≠ body |
| `CONTENT_NOT_FOUND` | No Jump content |
| `BAD_REQUEST` | JSON parse failure |

Example success (`data`):

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

> The **internal logic** of the syscall filter and memory accounting is **not public**. Docs and clients should rely only on the boundary and limit contract above.

### POST `/api/v1/jump/games/{id}/stream` (authentication required)

The server interprets SWF and similar sources and streams them as **zuku IR** (`ZIR\0` family) binary. This assumes the client has no SWF parser.

- The response may be **binary** (`application/octet-stream`) rather than a JSON envelope
- No source → `SOURCE_UNAVAILABLE`
- Interpretation or encoding failure → `SWF_PARSE_FAILED`

### POST `/api/v1/jump/games/{id}/swf` (authentication required)

An **original SWF byte proxy** for Jump games that need an AVM, for example for keyboard controls. No conversion or cache write-back.

- Authenticated clients only
- No source → `SOURCE_UNAVAILABLE`
- Unsupported format → `SWF_PARSE_FAILED`

### curl: play

```bash
curl -sS -X POST "https://zuzunza.com/api/v1/jump/games/{id}/play" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"content_id\":\"{id}\"}"
```

### JS/TS: stream (binary)

```ts
async function fetchJumpIr(token: string, gameId: string): Promise<ArrayBuffer> {
  const res = await fetch(`/api/v1/jump/games/${gameId}/stream`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) {
    // Errors may come back as a JSON envelope
    const text = await res.text();
    try {
      const env = JSON.parse(text);
      throw Object.assign(new Error(env.error?.message ?? text), {
        code: env.error?.code,
        status: res.status,
      });
    } catch (e) {
      if ((e as { code?: string }).code) throw e;
      throw new Error(text || `HTTP ${res.status}`);
    }
  }
  return res.arrayBuffer();
}
```

---

## GET `/api/v1/contents/{id}/conversion`

Returns only the content's conversion status. The fields and meanings are the same as in [Contents](contents.md#get-apiv1contentsidconversion).

It uses the same `ConversionInfo` schema as the `conversion` object inlined in Jump list and detail responses.

```bash
curl -sS "https://zuzunza.com/api/v1/contents/{id}/conversion"
```

---

## Recommended workflow (studio)

1. Upload thumbnails, media, and ZIP/ZWF/SWF/WASM files with `POST /api/v1/uploads` → get `upload.url`
2. Publish with `POST /api/v1/contents`, including the URL and category metadata ([Contents](contents.md))
3. For Jump, check the sandbox boundary with `play`. For SWF, play it on the client with Ruffle, and use the `stream`/`swf` proxies when needed
4. Track legacy conversion with `GET …/conversion`

> **Replacing a package**: there is **no** API for replacing the package bytes of an existing content id. Register a new version as a new Jump draft.

---

## Related pages

- [Contents](contents.md): content CRUD and recommendations
- [Errors](errors.md): `UNSUPPORTED_MEDIA_TYPE`, `PAYLOAD_TOO_LARGE`, `SOURCE_UNAVAILABLE`, and more
- [Rate limits](rate-limits.md)
- [Changelog](changelog.md)
