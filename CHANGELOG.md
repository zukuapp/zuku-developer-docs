# 변경 이력 / Changelog

ZUKU CLI와 ZUKU API의 변경 이력은 [한국어](docs/ko/changelog.md)·[English](docs/en/changelog.md) 문서에 있습니다.

ZUKU CLI and ZUKU API changes are in the [Korean](docs/ko/changelog.md) and [English](docs/en/changelog.md) changelog pages.

## Unreleased

- 문서 정리: 독자에게 필요하지 않은 범위 밖 안내, 내부 운영 정보, 작성 과정 메모, 자기 설명, 중복 문장을 제거했습니다. / Documentation: removed out-of-scope notes, internal operations details, writing-process notes, self-descriptions, and duplicate statements.
- README 구조: 개요, 요구 사항, 설치, 사용법, 소스 구성, 문제 해결, 변경 이력 순서입니다. / README structure: overview, requirements, installation, usage, source layout, troubleshooting, and changelog.

## v27.26102701 - 2026-10-27

- 문서 정비: README, 한국어·영어 문서, 원스토어 가이드, 브랜드 문서의 문체를 평서문 단정형으로 통일하고 불확실성 면책, 대화체, 과장 표현, 불필요한 굵은 글씨를 제거했습니다. / Documentation: normalized the style of the README, Korean and English pages, ONEstore guides, and brand notes; removed hedges, conversational phrasing, hype, and excess bold text.
- README 구조를 개요, 요구 사항, 설치, 사용법, 설정, 문제 해결, 변경 이력 순서로 정리했습니다. / Reorganized the README into overview, requirements, installation, usage, configuration, troubleshooting, and changelog sections.
- 버전 표기 통일: README 버전 배지와 문서 사이트 사이드바 버전 표기를 `v27.26102701`로 맞췄습니다. / Version: set the README badge and the documentation sidebar label to `v27.26102701`.
- 루트 `CHANGELOG.md`를 추가했습니다. / Added the root `CHANGELOG.md`.

### 기존 누적 변경 사항 / Prior changes

- 2026-10-04: 한국어·영어 개발 문서 각 27페이지, 공통 테마, 검색·내비게이션, 로컬 글꼴, Canvas·Phaser 게임 스타터를 공개했습니다. / Published 27 Korean and 27 English pages, the shared theme, search and navigation, local fonts, and Canvas and Phaser starters.
- 2026-10-04: 한국어·영어 원스토어 출시 가이드를 추가했습니다. / Added Korean and English ONEstore release guides.
- 2026-10-04: ZUKU 로고와 한국어·영어 브랜드 안내를 적용했습니다. / Adopted the ZUKU logos and bilingual brand guidance.
- 2026-10-04: 게임 개발용 npm 패키지 설치 안내를 README와 설치 문서에 추가했습니다. / Added npm game-development package installation guides to the README and installation pages.
- 2026-10-04: 404 페이지 제목에 공식 슬로건을 유지하도록 빌드 스크립트를 수정했습니다. / Kept the official slogan in the missing-page title in the build script.
- 2026-10-05: `@zuku/player` 고정 버전을 0.1.2로 올리고 렌더러 복구 동작을 문서화했습니다(PR #1). / Pinned `@zuku/player` 0.1.2 and documented bounded renderer recovery (PR #1).
