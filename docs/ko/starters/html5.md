---
title: Canvas 러너 스타터
description: zuku create 한 줄로 스페이스바와 탭으로 점프하는 Canvas 장애물 러너를 만들고, 구조를 이해한 뒤 패키지까지 만듭니다.
section: Starter
---

# Canvas 러너 스타터

가장 빠르게 ZUKU 게임을 시작하는 방법입니다. 빌드 도구도, 외부 라이브러리도 없는 순수 Canvas 2D 게임으로, 달려오는 장애물을 점프로 피하는 러너가 바로 만들어집니다.

## 프로젝트 만들기

```sh
# 새 폴더 ./my-runner/ 에 프로젝트 생성
zuku create my-runner
cd my-runner
```

이름은 소문자 영문, 숫자, `_`, `-`만 쓸 수 있고 최대 64자입니다. 같은 이름의 경로가 이미 있으면 아무것도 덮어쓰지 않고 `PROJECT_EXISTS`로 멈춥니다. `create`가 받는 인수는 프로젝트 이름 하나뿐이며 템플릿을 고르는 옵션은 없습니다.

명령을 쓰지 않고 시작하고 싶다면 같은 구조의 압축 파일 [zuku-canvas-starter.zip](/assets/starters/zuku-canvas-starter.zip)을 내려받아 풀어도 됩니다.

## 생성되는 파일

```text
my-runner/
├── zukujs.json      # 프로젝트 매니페스트
├── README.md        # 프로젝트 안내
├── .gitignore       # dist/, *.zwf, .zukujs/ 등 제외
└── src/
    ├── index.html   # 진입점 (640×360 캔버스)
    └── game.js      # 게임 로직
```

| 파일 | 역할 |
| --- | --- |
| `zukujs.json` | 로컬 프로젝트 매니페스트(`zukujs-project/1`). 패키지 안에는 들어가지 않습니다 |
| `src/index.html` | 매니페스트의 `entry`. `id="game"` 캔버스를 두고 `game.js`를 상대 경로로 불러옵니다 |
| `src/game.js` | 점프, 장애물 생성, 충돌, 점수 계산과 그리기 |
| `README.md`, `.gitignore` | 안내 문서와 버전 관리 제외 목록 |

패키지에는 `src/` 폴더만 들어갑니다.

## 매니페스트

`zuku create my-runner`가 만드는 `zukujs.json`은 다음과 같습니다.

```json
{
  "schema": "zukujs-project/1",
  "name": "my-runner",
  "title": "my-runner",
  "version": "0.1.0",
  "description": "ZukuJS로 만든 최소 HTML5 점프 게임입니다.",
  "tags": [],
  "age_rating": "all",
  "source": "src",
  "entry": "index.html",
  "jump": {
    "game_id": "game_my_runner",
    "genre": "arcade",
    "platform": { "pc": true, "mobile": true, "tablet": true }
  },
  "package": { "format": "zwf" }
}
```

`title`과 `description`은 업로드할 때 초안 메타데이터로 쓰이므로 게임에 맞게 바꿔 주세요. `jump.game_id`는 이름의 `-`를 `_`로 바꾸고 앞에 `game_`을 붙여 만들어집니다.

## 게임 구조

`game.js`는 하나의 즉시 실행 함수 안에 상태, 입력, 갱신, 그리기, 프레임 루프를 둡니다.

- **입력** 스페이스바, 위쪽 화살표, 캔버스 탭·클릭(`pointerdown`)이 모두 점프입니다. 게임 오버 상태에서 같은 입력을 하면 다시 시작합니다.
- **갱신** 중력을 적용하고 일정 간격으로 높이가 다른 장애물을 만들며, 시간이 지날수록 속도가 조금씩 빨라집니다.
- **그리기** 바닥, 플레이어, 장애물, 점수(`Score`, `Best`)를 매 프레임 그립니다.
- **프레임 간격** 한 프레임의 경과 시간을 최대 0.05초로 제한해 탭 전환 뒤에도 갑자기 튀지 않습니다.

간단한 수정부터 해 보세요.

```js
// 점프 힘을 키우면 더 높이 뜁니다 (기본 -620)
if (player.y >= GROUND - player.size) player.vy = -700;

// 시작 속도를 낮추면 초반 난이도가 쉬워집니다 (기본 240)
let speed = 180;
```

`speed`는 `reset()` 안에서도 다시 설정되므로 두 곳을 함께 바꿔야 재시작 후에도 같은 값이 적용됩니다.

## 실행, 검사, 패키지

```sh
# 로컬 미리보기 (현재 폴더 기준, Ctrl+C로 종료)
zuku run

# 매니페스트와 파일 규칙 검사
zuku validate .

# dist/my-runner-0.1.0.zwf 생성
zuku package . --format zwf
```

빌드 단계가 없으므로 `src/index.html`을 브라우저에서 직접 열어도 실행됩니다. 이미 있는 출력 파일은 `--force` 없이 덮어쓰지 않습니다. 다른 옵션은 [명령 참조](../cli/commands.md)를 보세요.

## 다음 단계

- 더 복잡한 2D 게임이 필요하면 [Phaser 2D 스타터](phaser.md)
- 완성한 게임 올리기는 [게시](../cli/publishing.md)
- 스타터 비교로 돌아가기: [스타터](index.md)
