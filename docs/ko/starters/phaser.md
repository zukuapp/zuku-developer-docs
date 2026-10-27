---
title: Phaser 2D 스타터
description: Phaser가 프로젝트 안에 포함된 2D 스타터를 내려받아 실행하고, 검사와 ZWF 패키징까지 진행합니다.
section: Starter
---

# Phaser 2D 스타터

Phaser 스타터는 씬 전환, 스프라이트 애니메이션, 아케이드 물리가 필요한 2D 게임용입니다. Phaser 라이브러리 파일이 프로젝트 안에 포함되어 CDN이나 npm 설치 없이 오프라인에서 동작합니다.

## 시작하기 전에

- `zuku create`는 [Canvas 러너](html5.md)만 만듭니다. Phaser 템플릿을 고르는 옵션은 없으므로 Phaser 스타터는 압축 파일로 받습니다.
- CLI가 설치되어 있어야 합니다. 설치 절차는 [설치](../installation.md)에 있습니다.
- `npm install`이나 빌드 도구는 필요하지 않습니다.

## 1. 내려받고 풀기

[zuku-phaser-starter.zip](/assets/starters/zuku-phaser-starter.zip)을 내려받아 원하는 위치에 풉니다.

```sh
# 압축 해제 후 프로젝트 폴더로 이동
unzip zuku-phaser-starter.zip -d my-phaser-game
cd my-phaser-game
```

압축 파일에는 최상위 폴더 `zuku-phaser-starter/`가 있습니다. `zukujs.json`이 있는 이 폴더가 프로젝트 루트이므로 `cd zuku-phaser-starter`로 한 번 더 이동합니다.

## 2. 구조 확인하기

편집 전에 다음 항목을 확인합니다. 이 규칙은 Phaser를 쓰는 모든 ZUKU 게임에 적용됩니다.

| 확인할 것 | 이유 |
| --- | --- |
| 루트에 `zukujs.json`이 있다 | CLI가 프로젝트를 인식하는 매니페스트입니다 |
| `source` 폴더(기본 `src`) 안에 `entry` 파일(기본 `index.html`)이 있다 | 패키지에는 `source` 폴더만 들어갑니다 |
| Phaser 파일이 `source` 폴더 안에 있고, HTML이 상대 경로로 불러온다 | 게임이 패키지 안의 파일만으로 실행되어야 합니다 |
| Phaser 라이선스 파일이 함께 있다 | 포함한 라이브러리의 고지를 유지합니다 |
| 이미지·사운드도 모두 상대 경로다 | `/`로 시작하는 절대 경로는 패키지 안에서 깨집니다 |

에셋을 추가할 때도 같은 원칙을 적용합니다.

```js
// 좋은 예: 진입 HTML 기준 상대 경로
this.load.image('player', 'assets/player.png');

// 피할 것: 외부 주소나 루트 절대 경로
// this.load.image('player', 'https://cdn.example.com/player.png');
// this.load.image('player', '/assets/player.png');
```

## 3. 매니페스트 다듬기

`zukujs.json`에서 최소한 `name`, `title`, `version`을 내 게임에 맞게 바꿉니다. `name`은 소문자 영문, 숫자, `_`, `-`로 최대 64자이며 패키지 파일 이름에도 쓰입니다.

```json
{
  "schema": "zukujs-project/1",
  "name": "my-phaser-game",
  "title": "나의 Phaser 게임",
  "version": "0.1.0",
  "source": "src",
  "entry": "index.html",
  "jump": {
    "game_id": "game_my_phaser_game",
    "genre": "arcade",
    "platform": { "pc": true, "mobile": true, "tablet": true }
  },
  "package": { "format": "zwf" }
}
```

`platform`에는 실제로 지원하는 기기만 `true`로 표시합니다. 터치 입력을 구현하지 않았다면 `mobile`과 `tablet`을 뺍니다.

## 4. 실행, 검사, 패키지

```sh
# 현재 폴더의 게임을 로컬에서 미리보기 (Ctrl+C로 종료)
zuku run

# 매니페스트와 파일 규칙 검사 (게임 코드는 실행하지 않음)
zuku validate .

# dist/<name>-<version>.zwf 생성
zuku package . --format zwf
```

`zuku run`은 현재 폴더를 기준으로 동작하므로 경로 인수 없이 실행합니다. 출력된 주소를 브라우저로 열면 게임이 실행됩니다.

`validate`에서 오류가 나면 메시지의 코드를 [오류](../errors.md)에서 찾아 고친 뒤 다시 실행합니다. 패키지 단계에서는 심볼릭 링크, 대소문자만 다른 경로, 실행 파일 등이 거부됩니다. 이미 있는 출력 파일을 바꾸려면 `--force`를 붙입니다.

## 에이전트로 Phaser 게임 만들기

CLI 0.3.0에는 Phaser가 포함되어 있지 않습니다. [게임 개발 에이전트](../cli/agent.md)는 CLI 설치본 옆에 `phaser` 패키지가 설치된 경우에만 Phaser를 선택합니다. 이때 에이전트는 Phaser 파일과 라이선스를 프로젝트에 복사하며 CDN에 의존하지 않습니다. 이 페이지의 스타터 압축 파일에는 Phaser가 포함되어 별도 설치가 필요 없습니다. 에이전트의 모델 연결은 [인증](../cli/authentication.md)과 [제공자](../cli/providers.md)에 있습니다.

## 다음 단계

- 완성한 패키지 올리기: [게시](../cli/publishing.md)
- 전체 명령 옵션: [명령 참조](../cli/commands.md)
- 다른 시작점 비교: [스타터](index.md)
