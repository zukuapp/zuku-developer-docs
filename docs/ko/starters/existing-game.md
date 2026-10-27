---
title: 기존 게임 이전하기
description: 이미 만든 HTML5 게임에 매니페스트를 추가하고 경로, 입력, 크기를 점검해 ZWF 패키지로 만듭니다.
section: Starter
---

# 기존 게임 이전하기

브라우저에서 동작하는 기존 HTML5 게임은 매니페스트를 추가하고 아래 규칙을 맞추면 ZUKU 패키지가 됩니다. 아래 항목을 순서대로 진행합니다.

## 1. 폴더 구조 정리

ZUKU 패키지에는 매니페스트의 `source` 폴더 안의 파일만 들어갑니다. 게임 실행에 필요한 파일을 모두 한 폴더(보통 `src`)에 모읍니다.

```text
my-game/
├── zukujs.json        # 새로 추가하는 매니페스트
└── src/               # 패키지에 들어가는 폴더
    ├── index.html     # 진입점
    ├── main.js
    └── assets/
        ├── player.png
        └── jump.ogg
```

번들러를 쓰는 프로젝트는 빌드 결과물을 이 폴더로 출력합니다. CLI는 빌드 명령을 실행하지 않고 폴더 안의 파일을 그대로 묶습니다. 점(`.`)으로 시작하는 항목과 `node_modules`는 패키지에서 제외됩니다.

## 2. 매니페스트 추가

프로젝트 루트에 `zukujs.json`을 만듭니다.

```json
{
  "schema": "zukujs-project/1",
  "name": "my-game",
  "title": "나의 게임",
  "version": "1.0.0",
  "description": "게임을 한두 문장으로 소개합니다.",
  "age_rating": "all",
  "source": "src",
  "entry": "index.html",
  "jump": {
    "game_id": "game_my_game",
    "genre": "arcade",
    "platform": { "pc": true, "mobile": true, "tablet": true }
  },
  "package": { "format": "zwf", "exclude": [] }
}
```

| 필드 | 필수 | 설명 |
| --- | --- | --- |
| `schema` | 예 | 항상 `"zukujs-project/1"` |
| `name` | 예 | 소문자 영문·숫자·`_`·`-`, 최대 64자. 패키지 파일 이름에 쓰입니다 |
| `title` | 예 | 표시 제목 |
| `version` | 예 | 패키지 버전 |
| `source` | 아니요 | 소스 폴더, 기본 `src` |
| `entry` | 아니요 | `source` 기준 진입 파일, 기본 `index.html` |
| `age_rating` | 아니요 | `all`, `12`, `15`, `18` |
| `jump` | 아니요 | 게임 ID, 장르, 지원 플랫폼 |
| `package` | 아니요 | 형식(`zwf` 또는 `zip`)과 제외할 상대 경로 |

비교용 예제는 `zuku create sample`로 만드는 [Canvas 러너](html5.md)입니다.

## 3. 경로를 모두 상대 경로로

패키지 안의 게임은 웹사이트 루트가 아닌 곳에서 실행됩니다. HTML, CSS, JavaScript에 적힌 모든 경로를 진입 파일 기준 상대 경로로 바꿉니다.

```html
<!-- 좋은 예 -->
<script src="main.js"></script>
<img src="assets/player.png" alt="">

<!-- 고쳐야 할 예: 루트 절대 경로와 외부 CDN -->
<!-- <script src="/main.js"></script> -->
<!-- <script src="https://cdn.example.com/lib.js"></script> -->
```

외부 CDN에서 불러오던 라이브러리는 파일을 내려받아 `src` 안에 넣고 라이선스 파일도 함께 둡니다. 게임은 패키지 안의 파일만으로 실행되어야 합니다.

## 4. 입력: 키보드와 터치 모두

PC와 모바일을 함께 지원하려면 두 입력을 모두 처리해야 합니다.

```js
// 키보드: 문자 대신 물리 키 코드(code)로 판별
addEventListener('keydown', e => {
  if (e.code === 'Space') { e.preventDefault(); action(); }
});

// 터치와 마우스: pointerdown 하나로 처리
canvas.addEventListener('pointerdown', e => { e.preventDefault(); action(); });
```

CSS의 `touch-action: manipulation`은 더블 탭 확대를 막습니다. 터치로 모든 동작을 할 수 없다면 매니페스트에서 `mobile`과 `tablet`을 뺍니다.

## 5. 크기와 성능

- 캔버스는 고정 해상도로 그리고 CSS로 화면 크기에 맞춥니다.
- `requestAnimationFrame`의 경과 시간을 사용하고 한 프레임 간격에 상한을 둡니다.
- 이미지와 사운드는 압축해 넣습니다. 패키지 검증에는 파일 수와 압축 해제 크기 한도가 있습니다.
- 소스 맵, 원본 디자인 파일처럼 실행에 필요 없는 파일은 `package.exclude`로 뺍니다.

## 6. 검사하고 고치기

```sh
# 로컬 미리보기 (현재 폴더 기준, Ctrl+C로 종료)
zuku run

# 매니페스트와 파일 규칙 검사
zuku validate .
```

`validate`는 게임 코드를 실행하지 않고 매니페스트와 파일만 검사합니다. 오류가 나오면 코드를 [오류](../errors.md)에서 찾아 고치고 통과할 때까지 다시 실행합니다. 주요 원인은 심볼릭 링크, 하드 링크, 대소문자만 다른 파일 이름, 실행 파일, 허용되지 않은 확장자입니다.

## 7. 패키지와 게시

```sh
# dist/<name>-<version>.zwf 생성
zuku package . --format zwf

# 만들어진 패키지도 다시 검사
zuku validate dist/my-game-1.0.0.zwf
```

같은 입력은 항상 같은 바이트를 만듭니다. 업로드와 공개 방법은 [게시](../cli/publishing.md)에 있습니다.

## 다음 단계

- 명령 옵션 전체: [명령 참조](../cli/commands.md)
- 다른 시작점 비교: [스타터](index.md)
