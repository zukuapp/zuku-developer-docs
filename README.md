<!-- BEGIN ZUKU OFFICIAL BRAND -->
<!-- markdownlint-disable MD033 MD041 -->
<p align="center">
  <a href="https://docs.zuzunza.com/">
    <picture>
      <source media="(prefers-color-scheme: dark)"
        srcset="docs/branding/zuku-logo-dark.png">
      <img src="docs/branding/zuku-logo-light.png"
        alt="ZUKU" width="320">
    </picture>
  </a>
</p>
<p align="center">ZUKU - 내가 불러 일으키는 새로운 창작.</p>
<!-- markdownlint-enable MD033 MD041 -->
<!-- END ZUKU OFFICIAL BRAND -->

# ZUKU Developer Docs

![version](https://img.shields.io/badge/version-v27.26102701-informational)

[한국어 문서](https://docs.zuzunza.com/) · [English documentation](https://docs.zuzunza.com/en/) · [ZUKU CLI source](https://github.com/zukuapp/zukujs-cli)

## 개요 / Overview

ZUKU 개발 문서의 공개 소스입니다. 한국어 27페이지와 영어 27페이지, 공통 테마, 검색·내비게이션, 로컬 글꼴과 플레이 가능한 게임 스타터를 포함합니다. `zuku`와 `zukujs`는 [동일한 CLI](docs/ko/cli/index.md)의 두 명령 이름입니다.

This is the public source for ZUKU's developer documentation: 27 Korean pages, 27 English pages, a shared theme, search and navigation, local fonts, and playable game starters. `zuku` and `zukujs` are two command names for [the same CLI](docs/en/cli/index.md).

원스토어 정식 출시 준비, 등록, 심사, 출시와 업데이트 절차는 [한국어 원스토어 배포 가이드](guides/ONEstore.ko.md)에 있습니다.

The [English ONEstore release guide](guides/ONEstore.en.md) covers production preparation, registration, review, release and updates.

## 요구 사항 / Requirements

| 용도 / Purpose | 요구 사항 / Requirement |
| --- | --- |
| npm 패키지·CLI / npm packages and CLI | Node.js 22 이상, npm / Node.js 22 or later, npm |
| 문서 로컬 빌드 / Local docs build | Python 3.12, Git, `requirements-docs.txt` (MkDocs 1.6.1 고정 / pinned) |

<!-- BEGIN ZUKU NPM DISTRIBUTIONS -->
## 설치 / Installation

### 게임 개발용 npm 패키지

아래 표는 정확한 설치 버전입니다. 프로젝트에 필요한 패키지만 설치합니다.

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

패키지는 `@zuku/lang/locales/ko.json` 같은 JSON 내보내기와 `@zuku/zwf-runtime/wasm` 같은 리소스 내보내기를 제공합니다. 브라우저 프로젝트는 ESM 번들러와 각 패키지의 호스트 안내를 따릅니다.

ZWF2는 HTML5 ZIP 게임 패키지 형식입니다. ZWF1은 애니메이션 형식입니다. 각 형식에 맞는 패키지와 로더를 사용합니다.

라이선스는 각 패키지에 포함된 원래 고지를 따릅니다. `@zuku/core`는 `UNLICENSED`입니다.

### npm CLI 설치

```sh
npm install -g @zuku/cli@0.3.1
zuku --version
zukujs --version
```

`zuku`와 `zukujs`는 같은 CLI와 로그인·설정·Agent Core 상태를 공유합니다. npm의 CLI 0.3.1과 관리형 설치 도구의 고정 릴리스 0.3.0은 배포 경로가 다릅니다.

플랫폼별 설치 절차는 [한국어 설치 안내](docs/ko/installation.md)와 [English installation guide](docs/en/installation.md)에 있습니다.

| Package | Version | Purpose |
| --- | --- | --- |
| [@zuku/zwf](https://www.npmjs.com/package/@zuku/zwf/v/0.1.1) | `0.1.1` | ZWF2 HTML5 ZIP game package reading and writing |
| [@zuku/sdk](https://www.npmjs.com/package/@zuku/sdk/v/0.2.0) | `0.2.0` | ZUKU API and game bridge |
| [zuku-engine-next2d](https://www.npmjs.com/package/zuku-engine-next2d/v/0.1.1) | `0.1.1` | Jump engine integration and game package validation |
| [@zuku/zwf-runtime](https://www.npmjs.com/package/@zuku/zwf-runtime/v/0.1.2) | `0.1.2` | ZWF1 animation WebAssembly runtime and host loader |
| [@zuku/lang](https://www.npmjs.com/package/@zuku/lang/v/0.1.0) | `0.1.0` | Validated JSON resources for 20 locales |
| [@zuku/core](https://www.npmjs.com/package/@zuku/core/v/27.0.1) | `27.0.1` | Command parsing, diagnostics and redaction |
| [@zuku/player](https://www.npmjs.com/package/@zuku/player/v/0.1.2) | `0.1.2` | Browser player from the maintained Next2D fork |
| [@zuku/editor](https://www.npmjs.com/package/@zuku/editor/v/0.1.1) | `0.1.1` | Browser editor and embedding helper |
| [@zuku/cli](https://www.npmjs.com/package/@zuku/cli/v/0.3.1) | `0.3.1` | Shared zuku and zukujs commands |

The English installation guide lists the exact install commands and per-package scope.
<!-- END ZUKU NPM DISTRIBUTIONS -->

## 사용법: 로컬 빌드 / Usage: local build

소스, 가상 환경, 결과물은 별도 작업 폴더에 나란히 둡니다.

Keep the checkout, virtual environment and output beside each other in a dedicated workspace.

### Linux / macOS

```sh
mkdir zuku-docs-workspace
cd zuku-docs-workspace
git clone https://github.com/zukuapp/zuku-developer-docs.git source
python3 -m venv .venv
.venv/bin/python -m pip install -r source/requirements-docs.txt
.venv/bin/python source/scripts/build.py
.venv/bin/python -m http.server 8000 --directory artifact
```

### Windows PowerShell

```powershell
mkdir zuku-docs-workspace
cd zuku-docs-workspace
git clone https://github.com/zukuapp/zuku-developer-docs.git source
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r source\requirements-docs.txt
.\.venv\Scripts\python.exe source\scripts\build.py
.\.venv\Scripts\python.exe -m http.server 8000 --directory artifact
```

한국어 문서는 `http://localhost:8000/`, 영어 문서는 `http://localhost:8000/en/`에서 열립니다. 빌드는 MkDocs strict 모드 검사와 내부 링크·앵커 검사를 수행합니다.

Open `http://localhost:8000/` for Korean or `http://localhost:8000/en/` for English. The build runs MkDocs in strict mode and checks internal links and anchors.

```text
zuku-docs-workspace/
├── .venv/       # pinned build environment / 고정된 빌드 환경
├── source/      # this Git checkout / 이 저장소
└── artifact/    # generated website / 생성된 사이트
```

## 소스 구성 / Source layout

| Path | 내용 / Contents |
| --- | --- |
| `docs/ko/`, `docs/en/` | 한국어·영어 문서 / Korean and English guides |
| `guides/` | 한국어·영어 원스토어 출시 안내 / Korean and English ONEstore release guides |
| `theme/` | 공통 HTML 테마 / Shared HTML theme |
| `assets/` | 스타일, 화면 동작, 글꼴, 로고, 스타터 / Styles, UI behavior, fonts, logos and starters |
| `scripts/build.py`, `scripts/hooks.py` | 빌드·링크 검사·기존 앵커 호환 / Build, link checks and legacy anchor compatibility |
| `requirements-docs.txt` | 고정된 Python 의존성 / Pinned Python dependencies |

## 문제 해결 / Troubleshooting

| 증상 / Symptom | 원인 / Cause | 조치 / Action |
| --- | --- | --- |
| `Refuse overwriting an existing documentation artifact` | `artifact/`가 이미 있습니다. / `artifact/` already exists. | 이전 결과를 다른 이름으로 옮긴 뒤 다시 빌드합니다. / Move the previous output to another name, then rebuild. |

## 변경 이력 / Changelog

저장소 변경 이력은 [CHANGELOG.md](CHANGELOG.md)에 있습니다. CLI와 API 변경 이력은 [한국어](docs/ko/changelog.md)·[English](docs/en/changelog.md) 문서에 있습니다.

The repository changelog is in [CHANGELOG.md](CHANGELOG.md). CLI and API changes are in the [Korean](docs/ko/changelog.md) and [English](docs/en/changelog.md) changelog pages.

## 라이선스 / License

이 저장소의 문서와 자체 코드는 [MIT](LICENSE)입니다. 포함된 외부 자료의 원래 라이선스도 보존합니다.

The documentation and original code in this repository use the [MIT license](LICENSE). Bundled third-party material retains its original license:

- **Wanted Sans**: SIL Open Font License 1.1, [license notice](assets/licenses/Wanted-Sans-OFL.txt).
- **Phaser 3.90.0**: MIT; `assets/starters/zuku-phaser-starter.zip` retains `src/vendor/PHASER-LICENSE.txt` inside the starter.
