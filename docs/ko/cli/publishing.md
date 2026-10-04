---
title: 패키징과 게시
description: ZukuJS CLI로 게임을 ZWF 패키지로 묶고, 초안으로 업로드한 뒤 ZUKU에 게시하는 과정과 계정 권한, 게시 한도, 결과 확인 방법을 안내합니다.
section: Guide
---

# 패키징과 게시

게임을 ZUKU에 올리는 과정은 세 단계로 나뉩니다.

1. **패키지** — 로컬에서 재현 가능한 `.zwf` 파일을 만듭니다. 네트워크를 쓰지 않습니다.
2. **초안 업로드** — 패키지를 올리고 **비공개 초안** JUMP 콘텐츠를 만듭니다.
3. **게시** — 초안을 공개합니다. 명시적인 게시 명령(`--yolo`)이 있을 때만 일어납니다.

`zuku`와 `zukujs`는 같은 명령입니다. 명령 전체는 [명령 참조](commands.md)를 보세요.

## 1. 검사와 패키지

프로젝트 디렉터리 안에서 실행합니다.

```sh
zuku validate .
zuku package . --format zwf
```

- 기본 출력은 `dist/<name>-<version>.zwf`입니다. 이미 있는 파일은 `--force` 없이 덮어쓰지 않습니다. 다른 경로는 `--output <file>`(`-o`)로 지정합니다.
- 같은 입력에서는 항상 같은 바이트가 나옵니다(경로 정렬, 고정 타임스탬프).
- 심볼릭·하드 링크, 경로 탈출, 특수 파일, 네이티브 실행 파일, 대소문자 충돌, 압축 해제 예산을 넘는 아카이브는 거부합니다. 프로젝트 코드나 빌드 명령은 실행하지 않습니다.
- 공개 검증 예산: 항목 8,000개, ZIP 500 MiB, 멤버당 압축 해제 128 MiB, 전체 압축 해제 512 MiB, JSON 2 MiB, 1 MiB 이상 멤버의 압축비 80:1.
- 해시 무결성은 게시자 서명이 아니며, 패키지의 권한 선언은 방화벽 보장이 아닙니다.

만든 패키지는 `zuku validate dist/<파일>.zwf`로 다시 검사할 수 있습니다.

## 2. 계정 연결과 권한

업로드와 게시에는 ZUKU 계정 연결이 필요합니다.

```sh
zuku login zuku
```

공식 ZUKU 브라우저 페이지에서 계정을 확인하고 연결을 승인합니다. CLI는 비밀번호나 복사한 토큰을 요구하지 않습니다. 브라우저를 자동으로 열 수 없으면 `--no-browser`를 붙이고 표시된 공식 페이지를 직접 여세요.

| 승인 범위 | 언제 |
| --- | --- |
| `games:upload games:create games:publish` | 기본 연결. 업로드·초안 생성·게시에 사용합니다. |
| `games:generate` 추가 | `zuku login zuku --generate`로 **명시적으로** 요청할 때만. 에이전트의 네이티브 생성에 필요합니다. |

공개 클라이언트 ID는 `zuku-cli`입니다. 일반 웹 로그인, 개발자 키, 환경 변수의 다른 인증 정보로 게시 권한을 대신할 수 없습니다. 연결 해제는 `zuku account logout`입니다. 자세한 내용은 [인증](authentication.md)을 보세요.

## 3. 초안 업로드

```sh
zuku upload .                                         # 디렉터리: 같은 규칙으로 패키지를 만든 뒤 업로드
zuku upload dist/my-runner-1.0.0.zwf --title "My Runner" --platform pc,mobile --tag arcade --verify
```

- 메타데이터는 `zukujs.json`에서 가져오며, `--title`, `--description`, `--genre`, `--version`, `--age-rating`, `--tag`, `--platform`, `--game-id` 플래그가 있으면 플래그가 우선합니다.
- 서버에서는 `POST /api/v1/uploads`로 파일을 올리고, `POST /api/v1/contents`로 `jump.status: "draft"` 초안을 만듭니다. `--verify`를 붙이면 `GET /api/v1/contents/{id}`로 초안을 다시 확인합니다.
- `upload`는 **게시하지 않습니다**. 초안은 공개 목록에 나오지 않지만, `/uploads/...` 파일 URL 자체는 공개 주소입니다.
- 초안과 업로드는 게시 한도를 쓰지 않습니다.

에이전트에서는 `zuku agent "..." --draft`가 같은 업로드 경로로 초안을 만듭니다([게임 개발 에이전트](agent.md)).

### 재시도 주의

업로드와 초안 생성은 원자적이지 않습니다. CLI는 변경 요청을 자동으로 재시도하지 않으며, 결과가 모호한 경우(5xx, 408, 전송 실패)는 그대로 영수증에 기록합니다. **다시 실행하기 전에 초안이 이미 생겼는지 확인하세요.** 영수증은 기본 `.zukujs/receipts`(또는 `--receipt-dir`)에 권한 `0600`으로 저장되며 토큰은 담지 않습니다. `.zukujs/`는 저장소에 커밋하지 마세요.

## 4. 게시 (`--yolo`)

```sh
zuku account --quota          # 남은 게시 횟수 확인
zuku deploy ./my-runner --yolo
```

또는 에이전트로 만들고 바로 게시합니다.

```sh
zuku agent "..." --yolo
```

- `--yolo`는 검증된 게임을 **즉시 공개 게시**하겠다는 명시적 의사 표시입니다. 추가 단계별 승인 질문은 없습니다. `--yolo`가 없으면 게시하지 않습니다.
- 서버는 **계정당 최근 6시간(롤링) 동안 성공한 공개 게시를 최대 3회** 허용합니다. 결과가 확정되지 않은 예약도 한도를 차지하며, 다른 장치나 동시 실행에도 같은 한도가 적용됩니다. 초과하면 `429 DEPLOY_QUOTA_EXCEEDED`와 `Retry-After`를 받습니다.
- `zuku account --quota`는 성공 수 `used`, 미확정 수 `pending`, 남은 수 `remaining`, 회복 시점 `reset_at`, 대기 시간 `retry_after`를 보여 줍니다.
- 게시 전에 계정·작업 키·패키지 전체 SHA-256·크기를 묶은 복구 기록을 `.zukujs/receipts`(또는 `--receipt-dir`)에 저장합니다. 초안 생성과 게시가 같은 `Idempotency-Key`를 쓰므로, 같은 소스의 확인된 완료 결과를 조회하는 재실행은 다시 게시하거나 한도를 추가로 쓰지 않습니다.

## 게시 결과 확인

응답이 끊기면 CLI는 같은 작업 키로 서버 상태를 조회합니다. 현재 소스·크기가 일치하고 `source_verified: true`인 완료 상태만 성공으로 인정합니다. `publishing`이나 `uncertain` 상태는 **자동으로 다시 게시하지 않습니다**.

저장된 배포는 다음처럼 확인합니다.

```sh
zuku deploy --content cnt_EXAMPLE --yolo --receipt-dir .zukujs/receipts
```

- 같은 설치에서 보존한 복구 기록과 원래 계정 연결이 필요합니다. 에이전트 실행은 `zuku agent --resume <run_id> --yolo`가 같은 방식으로 조회부터 수행합니다.
- 소스가 확인된 초안이라도 예약이 미확정이면 운영 측의 명확한 상태 정리가 필요합니다. 다른 키를 만들거나 로컬 기록을 지워 이 상태를 우회하지 마세요.

## 되돌리기

CLI에는 게시를 취소하는 명령이 없습니다. 문서화된 방법은 다음뿐입니다.

- 아직 게시하지 않았다면 게시 명령을 실행하지 않으면 됩니다. 초안은 공개 목록에 나타나지 않습니다.
- 콘텐츠 작성자는 API `DELETE /api/v1/contents/{id}`(Bearer 인증)로 콘텐츠를 **아카이브**할 수 있습니다. 하드 삭제가 아니며 복구·완전 삭제 계약은 별도입니다.
- 게시 한도는 **성공한** 게시 횟수로 계산합니다. 실패하거나 거부된 게시는 한도를 쓰지 않습니다.

## 관련 문서

- [게임 개발 에이전트](agent.md)
- [명령 참조](commands.md)
- [오류](../errors.md)
- [요청 한도](../rate-limits.md)
