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

[한국어 문서](https://docs.zuzunza.com/) · [English documentation](https://docs.zuzunza.com/en/) · [ZUKU CLI source](https://github.com/zukuapp/zukujs-cli)

ZUKU 개발 문서의 공개 소스입니다. 한국어 27페이지와 영어 27페이지, 공통 테마, 검색·내비게이션, 로컬 글꼴과 플레이 가능한 게임 스타터를 포함합니다. `zuku`와 `zukujs`는 [동일한 CLI](docs/ko/cli/index.md)의 두 명령 이름입니다.

This is the public source for ZUKU's developer documentation: 27 Korean pages, 27 English pages, a shared theme, search and navigation, local fonts, and playable game starters. `zuku` and `zukujs` are two command names for [the same CLI](docs/en/cli/index.md).

원스토어 정식 출시 준비부터 등록, 심사, 출시와 업데이트까지는 [한국어 원스토어 배포 가이드](guides/ONEstore.ko.md)를 참고하세요. 현재 공개 APK의 프리뷰 상태와 정식 서명 준비사항도 설명합니다.

See the [English ONEstore release guide](guides/ONEstore.en.md) for production preparation, registration, review, release and updates. It also explains the current public APK's preview status and production signing requirements.

<!-- BEGIN ZUKU NPM DISTRIBUTIONS -->
## 게임 개발용 npm 패키지

2026-10-04 공개 npm 레지스트리에서 아래 이름과 정확한 버전을 확인했습니다. 프로젝트에 필요한 패키지만 선택해 설치하세요.

| 패키지 | 버전 | 용도 |
| --- | --- | --- |
| [@zuku/zwf](https://www.npmjs.com/package/@zuku/zwf/v/0.1.1) | `0.1.1` | ZWF2 HTML5 ZIP 게임 패키지 읽기·쓰기 |
| [@zuku/sdk](https://www.npmjs.com/package/@zuku/sdk/v/0.2.0) | `0.2.0` | ZUKU API·게임 브리지 |
| [zuku-engine-next2d](https://www.npmjs.com/package/zuku-engine-next2d/v/0.1.1) | `0.1.1` | Jump 엔진 연결·게임 패키지 검증 |
| [@zuku/zwf-runtime](https://www.npmjs.com/package/@zuku/zwf-runtime/v/0.1.2) | `0.1.2` | ZWF1 애니메이션 WebAssembly 런타임·호스트 로더 |
| [@zuku/lang](https://www.npmjs.com/package/@zuku/lang/v/0.1.0) | `0.1.0` | 20개 언어의 검증된 JSON 리소스 |
| [@zuku/core](https://www.npmjs.com/package/@zuku/core/v/27.0.1) | `27.0.1` | 명령 파싱·진단·민감정보 가림 |
| [@zuku/player](https://www.npmjs.com/package/@zuku/player/v/0.1.1) | `0.1.1` | 유지보수 중인 Next2D 기반 브라우저 플레이어 |
| [@zuku/editor](https://www.npmjs.com/package/@zuku/editor/v/0.1.1) | `0.1.1` | 브라우저 에디터·임베딩 도우미 |
| [@zuku/cli](https://www.npmjs.com/package/@zuku/cli/v/0.3.1) | `0.3.1` | 동일한 zuku·zukujs 명령 |

```sh
npm install --save-exact @zuku/zwf@0.1.1 @zuku/sdk@0.2.0 zuku-engine-next2d@0.1.1 @zuku/zwf-runtime@0.1.2 @zuku/lang@0.1.0 @zuku/core@27.0.1 @zuku/player@0.1.1 @zuku/editor@0.1.1
```

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

설치와 플랫폼별 확인은 [한국어 설치 안내](docs/ko/installation.md)와 [English installation guide](docs/en/installation.md)를 참고하세요.

| Package | Version | Purpose |
| --- | --- | --- |
| [@zuku/zwf](https://www.npmjs.com/package/@zuku/zwf/v/0.1.1) | `0.1.1` | ZWF2 HTML5 ZIP game package reading and writing |
| [@zuku/sdk](https://www.npmjs.com/package/@zuku/sdk/v/0.2.0) | `0.2.0` | ZUKU API and game bridge |
| [zuku-engine-next2d](https://www.npmjs.com/package/zuku-engine-next2d/v/0.1.1) | `0.1.1` | Jump engine integration and game package validation |
| [@zuku/zwf-runtime](https://www.npmjs.com/package/@zuku/zwf-runtime/v/0.1.2) | `0.1.2` | ZWF1 animation WebAssembly runtime and host loader |
| [@zuku/lang](https://www.npmjs.com/package/@zuku/lang/v/0.1.0) | `0.1.0` | Validated JSON resources for 20 locales |
| [@zuku/core](https://www.npmjs.com/package/@zuku/core/v/27.0.1) | `27.0.1` | Command parsing, diagnostics and redaction |
| [@zuku/player](https://www.npmjs.com/package/@zuku/player/v/0.1.1) | `0.1.1` | Browser player from the maintained Next2D fork |
| [@zuku/editor](https://www.npmjs.com/package/@zuku/editor/v/0.1.1) | `0.1.1` | Browser editor and embedding helper |
| [@zuku/cli](https://www.npmjs.com/package/@zuku/cli/v/0.3.1) | `0.3.1` | Shared zuku and zukujs commands |

The table lists publicly verified npm releases. See the English installation guide for exact install commands and per-package scope.
<!-- END ZUKU NPM DISTRIBUTIONS -->

## 로컬 빌드 / Local build

Python 3.12와 Git을 준비하세요. MkDocs와 관련 의존성은 `requirements-docs.txt`에 버전이 고정되어 있습니다. 별도 작업 폴더에서 소스, 가상 환경과 결과물을 나란히 두면 저장소에 의존성이나 생성 파일이 들어가지 않습니다.

Use Python 3.12 and Git. MkDocs and its dependencies are pinned in `requirements-docs.txt`. Keep the checkout, virtual environment and output beside each other in a dedicated workspace.

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

브라우저에서 `http://localhost:8000/`(한국어) 또는 `http://localhost:8000/en/`(영어)을 여세요. 빌드는 엄격한 MkDocs 검사와 내부 링크·앵커 검사를 수행합니다. `artifact/`가 이미 있으면 덮어쓰지 않으므로 이전 결과를 다른 이름으로 보관한 후 다시 빌드하세요.

Open `http://localhost:8000/` for Korean or `http://localhost:8000/en/` for English. The build runs MkDocs in strict mode and checks internal links and anchors. It refuses to overwrite an existing `artifact/`; preserve the previous output under another name before rebuilding.

```text
zuku-docs-workspace/
├── .venv/       # pinned build environment / 고정된 빌드 환경
├── source/      # this Git checkout / 이 저장소
└── artifact/    # generated website / 생성된 사이트
```

생성된 MkDocs 설정과 `source/.codex/`의 검증 기록은 Git에 넣지 않습니다. 이 저장소는 문서와 공개 에셋만 포함하며 서비스 배포 설정은 포함하지 않습니다.

Generated MkDocs configuration and local verification records in `source/.codex/` are ignored by Git. The repository contains documentation and public assets; service deployment configuration is managed separately.

## 소스 구성 / Source layout

| Path | 내용 / Contents |
| --- | --- |
| `docs/ko/`, `docs/en/` | 한국어·영어 문서 / Korean and English guides |
| `guides/` | 한국어·영어 원스토어 출시 안내 / Korean and English ONEstore release guides |
| `theme/` | 공통 HTML 테마 / Shared HTML theme |
| `assets/` | 스타일, 화면 동작, 글꼴, 로고, 스타터 / Styles, UI behavior, fonts, logos and starters |
| `scripts/build.py`, `scripts/hooks.py` | 빌드·링크 검사·기존 앵커 호환 / Build, link checks and legacy anchor compatibility |
| `requirements-docs.txt` | 고정된 Python 의존성 / Pinned Python dependencies |

## 라이선스 / License

이 저장소의 문서와 자체 코드는 [MIT](LICENSE)입니다. 포함된 외부 자료의 원래 라이선스도 보존합니다.

The documentation and original code in this repository use the [MIT license](LICENSE). Bundled third-party material retains its original license:

- **Wanted Sans**: SIL Open Font License 1.1, [license notice](assets/licenses/Wanted-Sans-OFL.txt).
- **Phaser 3.90.0**: MIT; `assets/starters/zuku-phaser-starter.zip` retains `src/vendor/PHASER-LICENSE.txt` inside the starter.
