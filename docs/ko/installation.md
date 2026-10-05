---
title: 설치
description: 게임 개발용 npm 패키지와 Linux, macOS, Windows용 ZUKU CLI 설치 안내입니다.
section: Starter
---

# 설치

관리형 설치 도구의 현재 고정 CLI 릴리스는 0.3.0입니다. 설치 도구는 CLI와 관리형 Node.js 22 런타임을 사용자 디렉터리에 설치하며, 관리자 권한이 필요하지 않습니다.

> npm 패키지 이름은 아래의 공개 배포 표를 기준으로 선택하세요. 관리형 설치 도구는 기존 고정 릴리스를 계속 제공합니다.

<!-- BEGIN ZUKU NPM DISTRIBUTIONS -->
## 게임 개발용 npm 패키지

아래 표는 정확한 설치 버전을 안내합니다. `@zuku/player`는 `0.1.2`로 갱신했으며, 나머지 8개 패키지는 2026-10-04 공개 npm 레지스트리에서 확인한 버전을 유지합니다. 프로젝트에 필요한 패키지만 선택해 설치하세요.

| 패키지 | 버전 | 용도 |
| --- | --- | --- |
| [@zuku/zwf](https://www.npmjs.com/package/@zuku/zwf/v/0.1.1) | `0.1.1` | ZWF2 HTML5 ZIP 게임 패키지 읽기·쓰기 |
| [@zuku/sdk](https://www.npmjs.com/package/@zuku/sdk/v/0.2.0) | `0.2.0` | ZUKU API·게임 브리지 |
| [zuku-engine-next2d](https://www.npmjs.com/package/zuku-engine-next2d/v/0.1.1) | `0.1.1` | Jump 엔진 연결·게임 패키지 검증 |
| [@zuku/zwf-runtime](https://www.npmjs.com/package/@zuku/zwf-runtime/v/0.1.2) | `0.1.2` | ZWF1 애니메이션 WebAssembly 런타임·호스트 로더 |
| [@zuku/lang](https://www.npmjs.com/package/@zuku/lang/v/0.1.0) | `0.1.0` | 20개 언어의 검증된 JSON 리소스 |
| [@zuku/core](https://www.npmjs.com/package/@zuku/core/v/27.0.1) | `27.0.1` | 명령 파싱·진단·민감정보 가림 |
| [@zuku/player](https://www.npmjs.com/package/@zuku/player/v/0.1.2) | `0.1.2` | 유지보수 중인 Next2D 기반 브라우저 플레이어 |
| [@zuku/editor](https://www.npmjs.com/package/@zuku/editor/v/0.1.1) | `0.1.1` | 브라우저 에디터·임베딩 도우미 |
| [@zuku/cli](https://www.npmjs.com/package/@zuku/cli/v/0.3.1) | `0.3.1` | 동일한 zuku·zukujs 명령 |

```sh
npm install --save-exact @zuku/zwf@0.1.1 @zuku/sdk@0.2.0 zuku-engine-next2d@0.1.1 @zuku/zwf-runtime@0.1.2 @zuku/lang@0.1.0 @zuku/core@27.0.1 @zuku/player@0.1.2 @zuku/editor@0.1.1
```

`@zuku/player` 0.1.2는 WebGPU 어댑터와 장치 획득 대기를 각각 2초로 제한합니다. 렌더러 초기화 실패나 장치 손실 시 새 캔버스에서 WebGL로 복구할 수 있습니다. 복구는 최대 2회 시도하며, 렌더링을 초기화하지 못하면 오류를 알립니다.

`@zuku/lang/locales/ko.json` 같은 JSON 내보내기와 `@zuku/zwf-runtime/wasm` 같은 리소스 내보내기를 사용할 수 있습니다. 브라우저 프로젝트에서는 ESM 번들러와 각 패키지의 호스트 안내를 따르세요.

ZWF2는 HTML5 ZIP 게임 패키지이고 ZWF1은 애니메이션 형식입니다. 각 형식에 맞는 패키지와 로더를 사용하세요.

라이선스는 각 패키지에 포함된 원래 고지를 따릅니다. `@zuku/core`의 기존 `UNLICENSED` 표기는 유지됩니다. Next.js 서버 프레임워크와 운영 서버는 이번 게임 개발 라이브러리 배포 범위에서 제외합니다.

### npm CLI 설치

Node.js 22 이상과 npm을 준비한 뒤 실행하세요.

```sh
npm install -g @zuku/cli@0.3.1
zuku --version
zukujs --version
```

`zuku`와 `zukujs`는 같은 CLI와 로그인·설정·Agent Core 상태를 공유합니다. npm의 CLI 0.3.1과 아래 관리형 설치 도구의 고정 릴리스 0.3.0은 배포 경로가 다릅니다.
<!-- END ZUKU NPM DISTRIBUTIONS -->

## Linux와 macOS

curl 또는 wget으로 설치 스크립트를 받아 Bash로 실행합니다.

```sh
# curl 사용
curl -fsSL --proto '=https' --tlsv1.2 https://zuzunza.com/install.sh -o install-zuku-cli.sh && bash install-zuku-cli.sh
```

```sh
# wget 사용
wget --https-only -O install-zuku-cli.sh https://zuzunza.com/install.sh && bash install-zuku-cli.sh
```

기본 설치 경로는 `~/.local/share/zukujs`이고, 실행 파일은 `~/.local/bin/zuku`와 `~/.local/bin/zukujs`입니다.

## Windows (PowerShell)

```powershell
# 설치 스크립트 실행
& ([scriptblock]::Create((irm 'https://zuzunza.com/install.ps1')))
```

기본 설치 경로는 `%LOCALAPPDATA%\ZukuJS`이고, 실행 파일은 `bin\zuku.cmd`와 `bin\zukujs.cmd`입니다. 설치 도구는 현재 PowerShell 세션의 PATH에 `bin` 디렉터리를 추가합니다.

## 설치 확인

```sh
# 버전 확인 (zukujs --version도 같은 결과)
zuku --version
```

`zuku`와 `zukujs`는 같은 런타임, 설정, 로그인 상태(`~/.config/zukujs/`(Windows: `%LOCALAPPDATA%\ZukuJS\`))를 공유하므로 어느 이름을 써도 됩니다.

## 설치 옵션

| Bash | PowerShell | 설명 |
| --- | --- | --- |
| `--prefix /절대/경로` | `-Prefix 'C:\절대\경로'` | 다른 사용자 디렉터리에 설치 |
| `--dry-run` | `-DryRun` | 다운로드나 파일 쓰기 없이 설치 계획만 확인 |
| `--help` | `-Help` | 옵션 안내 |

```sh
# 공백이나 한글이 있는 경로는 따옴표로 감쌉니다
bash install-zuku-cli.sh --prefix "$HOME/도구/ZukuJS CLI" --dry-run
```

## 업데이트와 재설치

같은 설치 명령을 다시 실행하면 같은 경로에 다시 설치합니다. 다운로드 검증이나 설치 확인이 실패하면 이전 설치와 두 별칭을 그대로 두거나 복원합니다. 설치 경로에 다른 프로그램의 `zuku` 또는 `zukujs`가 있으면 덮어쓰지 않으므로, 이 경우 `--prefix`(`-Prefix`)로 다른 경로를 지정하세요.

## 다운로드와 무결성

설치 도구는 HTTPS로 고정 버전 아카이브를 받습니다.

```text
https://zuzunza.com/downloads/zukujs/cli/0.3.0/zukujs-cli-0.3.0.tgz
```

CLI 아카이브와 공식 Node.js 아카이브의 SHA-256을 릴리스에 고정된 값과 비교한 뒤 설치하고, 값이 다르면 설치하지 않습니다. CLI 의존성은 아카이브에 포함되어 있어 별도 패키지 다운로드 없이 설치됩니다. Studio가 포함된 릴리스는 플랫폼별 검증된 파일을 [공식 GitHub 릴리스](https://github.com/zukuapp/zukujs-cli/releases)에서 받습니다.

## 문제 해결

### `zuku: command not found`

Linux와 macOS의 설치 도구는 셸 설정 파일을 수정하지 않습니다. 현재 터미널에 PATH를 추가하세요.

```sh
# 현재 세션에만 적용
export PATH="$HOME/.local/bin:$PATH"
zuku --version
```

새 터미널에서도 쓰려면 같은 줄을 사용 중인 셸 설정 파일(예: `~/.bashrc`, `~/.zshrc`)에 추가하세요. `--prefix`로 설치했다면 그 경로 아래 `bin`을 추가합니다.

Windows에서는 **사용자 환경 변수 → Path**에 `%LOCALAPPDATA%\ZukuJS\bin`을 추가한 뒤 새 터미널을 여세요.

### Node.js 버전

관리형 설치 도구로 설치한 CLI는 함께 설치된 Node.js 22 런타임으로 실행됩니다. 시스템 Node.js를 바꾸지 않으며 Linux에서는 공식 Node.js 바이너리를 실행할 수 있어야 합니다. npm으로 CLI를 설치할 때는 사용자 환경의 Node.js 22 이상을 사용합니다.

### 지원 플랫폼

Linux와 macOS(x64, arm64), Windows(x64, arm64)를 대상으로 합니다.

## 다음 단계

- [시작하기](getting-started.md): 첫 게임 만들기
- [CLI 명령 참조](cli/commands.md)
- [오류 코드](errors.md)
