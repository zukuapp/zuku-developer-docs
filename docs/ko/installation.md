---
title: 설치
description: Linux, macOS, Windows에 ZUKU CLI 0.3.0을 설치하고 확인하는 방법입니다.
section: Starter
---

# 설치

ZukuJS CLI 0.3.0은 공식 설치 도구로 설치합니다. 설치 도구는 CLI와 관리형 Node.js 22 런타임을 사용자 디렉터리에 설치하며, 관리자 권한이 필요하지 않습니다.

> `@zukujs/cli`는 npm에 게시되지 않았습니다. `npm install`로는 설치할 수 없습니다.

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

CLI는 설치 도구가 함께 설치한 관리형 Node.js 22 런타임으로 실행됩니다. 시스템에 설치된 Node.js 버전과 관계없으며, 시스템 Node.js를 바꾸지도 않습니다. Linux에서는 공식 Node.js 바이너리를 실행할 수 있는 환경이어야 합니다.

### 지원 플랫폼

Linux와 macOS(x64, arm64), Windows(x64, arm64)를 대상으로 합니다.

## 다음 단계

- [시작하기](getting-started.md): 첫 게임 만들기
- [CLI 명령 참조](cli/commands.md)
- [오류 코드](errors.md)
