# ZUKU Android 앱 원스토어 출시 가이드

확인 기준: 2026년 10월 4일. 이 문서는 ZUKU Android 앱을 정식 서명한 뒤 원스토어에 등록하고, 심사·공개·업데이트하는 담당자용 절차입니다. 계정 생성이나 스토어 업로드를 자동으로 수행하는 문서는 아닙니다.

## 1. 제출 대상과 현재 상태 확인

원스토어에 제출할 대상은 Android 앱입니다. `@zukujs/cli`와 동일 런타임을 사용하는 `zuku`·`zukujs` 명령, CLI가 만드는 게임 패키지는 Android APK가 아닙니다. 게임 패키지를 APK 업로드 화면에 제출하지 않습니다.

현재 [ZUKU APK 페이지](https://apk.zuzunza.com/)에서 제공하는 프리뷰 APK의 실제 측정값은 다음과 같습니다.

| 항목 | 현재 프리뷰 |
| --- | --- |
| 앱 패키지 / applicationId | `com.zuzunza.zuku` |
| versionName / versionCode | `0.3.0` / `3` |
| minSdk / targetSdk | `24` / `36` |
| 포함 ABI | `arm64-v8a`, `x86_64` |
| debuggable | `false` |
| 서명 | Android Debug 인증서 |
| APK SHA-256 | `ee0cc23906ba44681b34ac9542b0f924504dac818ff03b151122c6a04e15647c` |

현재 프리뷰는 정식 출시용 서명 상태가 아닙니다. 확인한 공개 프리뷰와 기본 Gradle 설정에서는 release도 `signingConfigs.debug`를 사용합니다. 공식 빌드 스크립트에는 정식 서명 설정을 받아 별도로 구성하는 경로가 있으며 5단계에서 설명합니다. `assembleRelease` 성공이나 `debuggable=false`만으로 정식 서명 준비가 끝났다고 판단하지 말고 실제 결과물을 검증합니다.

앱의 ZUKU AI는 현재 **오픈 준비중**입니다. 소개·스크린샷·심사용 설명도 이 상태와 일치시킵니다. 아직 검증하지 않은 AI 이용권, 구독, 결제 기능을 사용 가능한 기능으로 설명하지 않습니다.

## 2. APK와 서명 운영 방식 결정

원스토어 Android 등록은 APK와 AAB를 모두 지원합니다. 이 앱의 첫 정식 출시에는 **개발자가 관리하는 정식 키로 서명한 APK**를 기준으로 준비하면 APK 페이지와 스토어 배포의 인증서를 맞추기 쉽습니다. AAB를 선택한다면 스토어가 만드는 최종 배포 APK의 서명까지 별도로 확인합니다. [원스토어 지원 형식](https://onestore-dev.gitbook.io/dev/docs/apps)

APK에서 AAB로 전환한 상품은 다시 APK 형식으로 돌아갈 수 없습니다. 같은 앱을 다른 배포 경로에서도 업데이트하려면 최종 앱 서명 인증서의 연속성을 설계해야 합니다. 업로드 키와 사용자 기기에 설치되는 앱 서명 키를 혼동하지 않습니다. [AAB 공식 FAQ](https://onestore-dev.gitbook.io/dev/help/faq/apps/one-store-android-app-bundle)

개발자 관리 APK 경로는 바이너리 등록의 **앱 서명 사용 안함** 옵션에 해당합니다. 이 옵션도 서명된 APK가 필요합니다. 원스토어 키 관리 방식을 선택하면 공식 내보내기·등록 절차를 따르고, 최종 서명된 APK를 내려받아 검사합니다. [바이너리 및 서명 옵션](https://onestore-dev.gitbook.io/dev/docs/apps/product/android/binary)

## 3. 개발자 계정 준비

1. [ONEconsole](https://dev.onestore.net/)에 앱 소유자의 개발자 계정으로 가입하거나 로그인합니다.
2. 개인·사업자 구분, 연락처와 계정 소유권을 실제 운영 주체에 맞게 등록합니다.
3. 출시 담당자의 접근 권한을 정하고, 유료 판매를 계획한다면 콘솔이 요구하는 정산 정보를 먼저 완료합니다.
4. 상품 등록 전 서비스 국가·언어·유료 여부와 결제 운영 방식을 결정합니다. 요구 서류와 조건은 해당 계정의 현재 콘솔 안내를 따릅니다. [원스토어 개발자 안내](https://onestore-dev.gitbook.io/dev)

## 4. 정식 서명 키와 업데이트 경로 준비

앱 소유자가 관리하는 정식 keystore를 준비하고 release 빌드가 그 키를 사용하도록 설정합니다. 이미 같은 앱의 정식 서명 키를 운영하고 있다면 그 키와 기존 배포 기록을 기준으로 진행합니다. Android Studio의 **Build → Generate Signed App Bundle or APK → APK** 절차를 사용할 수 있습니다. [Android 앱 서명](https://developer.android.com/studio/publish/app-signing)

keystore와 비밀번호는 Git 저장소, 문서, 채팅, 빌드 로그에 넣지 않습니다. 접근을 제한한 비밀 저장소와 암호화한 별도 백업으로 보관하고 복구 가능 여부를 확인합니다. 인계 자료에는 비밀 키 대신 인증서의 공개 SHA-256 지문을 남깁니다.

현재 프리뷰 인증서 지문은 다음과 같습니다. 정식 결과물이 이 인증서로 서명되어 있으면 프리뷰 서명이 남아 있는 상태입니다.

```text
fac61745dc0903786fb9ede62a962b399f7348f0bb6f899b8332667591033b9c
```

같은 패키지라도 현재 Debug 프리뷰에서 다른 정식 인증서로 서명한 앱으로는 일반적인 덮어쓰기 업데이트가 되지 않습니다. 프리뷰 사용자에게 데이터 보존 가능 여부와 전환 방법을 먼저 안내합니다. 테스트 기기에서도 필요한 데이터를 보존한 뒤 별도로 전환하며, 앱 삭제를 자동 실행하지 않습니다. 이후 APK 페이지와 원스토어의 정식 빌드는 같은 패키지와 승인된 서명 체계를 유지하도록 운영합니다.

## 5. 정식 릴리스 빌드

릴리스 대상으로 정한 소스와 `package-lock.json`을 고정하고 프로젝트가 사용하는 Node·JDK·Android SDK·Gradle wrapper 환경을 준비합니다. `applicationId`는 `com.zuzunza.zuku`로 유지합니다.

`versionCode`는 기존에 배포하거나 등록한 모든 대상 버전보다 커야 합니다. 현재 공개 프리뷰에서 확인한 값은 `3`이므로, 다른 등록 이력이 없다면 다음 릴리스에는 최소 `4`를 사용합니다. 콘솔에 더 큰 코드가 있으면 그 값보다 높여야 합니다. `versionName`은 실제 릴리스 이름으로 따로 정합니다. [Android 버전 관리](https://developer.android.com/studio/publish/versioning)

현재 프로젝트의 공식 빌드 스크립트는 `ZUKU_ANDROID_KEYSTORE_PATH`, `ZUKU_ANDROID_KEYSTORE_PASSWORD`, `ZUKU_ANDROID_KEY_ALIAS`, `ZUKU_ANDROID_KEY_PASSWORD` 네 설정이 모두 제공될 때 정식 서명 구성을 생성합니다. 키와 비밀번호는 보호된 로컬 환경 또는 CI 비밀 저장소에서 주입합니다. 값이 들어간 명령을 문서·로그·셸 기록에 남기지 않습니다.

공식 `build:apk` 스크립트는 Linux·macOS에서 실행합니다. Windows에서는 WSL2 안의 Linux Node·JDK·Android SDK 환경을 사용하며, Windows 네이티브 Node로 이 스크립트를 실행하는 방식은 지원하지 않습니다.

아래 명령은 **네 정식 서명 설정을 안전하게 제공한 뒤**, 앱 프로젝트 루트에서 실행합니다. APK 빌드에 설정이 빠지면 프리뷰 서명을 사용할 수 있으므로 다음 단계의 인증서 검사까지 완료해야 합니다.

```bash
npm ci
npm run typecheck
npm test
npm run build:apk
```

스크립트는 Android 프로젝트를 생성·설정한 뒤 Gradle release 빌드를 수행합니다. 이미 정식 서명이 구성된 Android 프로젝트를 직접 빌드할 때의 wrapper 명령은 다음과 같습니다.

```bash
cd android
./gradlew :app:assembleRelease
```

Windows에서는 동일한 wrapper의 `gradlew.bat :app:assembleRelease`를 사용합니다. 기본 app 모듈의 결과 경로는 `app/build/outputs/apk/release/app-release.apk`이며, 프로젝트에서 출력 이름을 바꿨다면 실제 결과물을 선택합니다. [Android 명령줄 빌드](https://developer.android.com/build/building-cmdline)

프리뷰 APK를 덮어쓰거나 서명만 바꾸어 같은 파일로 배포하지 않습니다. 새 정식 결과물을 별도 릴리스로 보존하고, 서명 이후 APK를 수정하지 않습니다.

## 6. 업로드할 파일 자체 검증

프로젝트 루트에서 Android SDK의 `apkanalyzer`, `aapt2`, `apksigner`가 실행 가능한 환경을 사용합니다. 아래 경로는 기본 Gradle 출력 경로를 사용하는 경우입니다.

```bash
ZUKU_ANDROID_APK=android/app/build/outputs/apk/release/app-release.apk
apkanalyzer apk summary "$ZUKU_ANDROID_APK"
apkanalyzer manifest min-sdk "$ZUKU_ANDROID_APK"
apkanalyzer manifest target-sdk "$ZUKU_ANDROID_APK"
apkanalyzer manifest debuggable "$ZUKU_ANDROID_APK"
apkanalyzer manifest permissions "$ZUKU_ANDROID_APK"
aapt2 dump badging "$ZUKU_ANDROID_APK"
apksigner verify --verbose --print-certs "$ZUKU_ANDROID_APK"
sha256sum "$ZUKU_ANDROID_APK"
```

macOS에서는 마지막 줄 대신 `shasum -a 256 "$ZUKU_ANDROID_APK"`를 사용할 수 있습니다. 명령은 파일의 manifest, 포함 ABI, 서명과 해시를 검사합니다. [APK Analyzer](https://developer.android.com/tools/apkanalyzer), [AAPT2](https://developer.android.com/tools/aapt2), [apksigner](https://developer.android.com/tools/apksigner)

결과에서 패키지, 새 versionCode, `debuggable=false`, 실제 지원 ABI와 정식 인증서 지문을 확인합니다. 서명 검증 성공은 정식 키 사용이나 스토어 심사 통과를 대신하지 않습니다. 모든 값이 릴리스 기록과 맞는 **그 파일**을 업로드 대상으로 고정합니다.

## 7. 실제 기기에서 출시 동작 확인

정식 결과물을 설치해 새 설치와 기존 정식 버전에서의 업데이트를 각각 확인합니다. 지원을 선언할 실제 Android 기기에서 시작 화면, 로그인·로그아웃, 기본 탐색, 게임 실행, 뒤로 가기, 키보드, 권한 거절, 네트워크 단절과 복귀를 점검합니다. 해당 화면이나 기능이 릴리스에 없다면 제공한다고 기재하지 않습니다.

좁은 화면과 큰 글자, 다크 모드, 앱 재시작도 확인합니다. AI 화면은 **오픈 준비중** 표시를 유지하며, 닫힌 백엔드를 이미 이용 가능한 기능처럼 보여주지 않아야 합니다. 개인정보처리방침 링크와 사용자 지원 경로가 실제로 열리는지도 점검합니다.

## 8. 원스토어 Android 상품 등록

ONEconsole에서 **Apps → 상품현황 → 신규 상품 등록**으로 이동해 **정식 출시 / Android**를 선택합니다. 패키지 네임은 검증한 APK와 같은 `com.zuzunza.zuku`를 입력합니다. 패키지는 등록 후 변경할 수 없으므로 기존에 소유한 동일 상품이 있으면 그 상품의 업데이트 경로를 사용합니다. [신규 앱 등록](https://onestore-dev.gitbook.io/dev/docs/apps/register-app)

현재 배포 파일을 프리뷰라고 부르는 것과 원스토어의 **베타** 상품 유형은 다릅니다. 원스토어 베타로 등록한 상품을 정식 출시하려면 신규 상품과 다른 패키지가 필요하므로, 이 절차에서는 정식 출시를 선택합니다. 같은 패키지가 다른 소유자의 상품으로 표시되면 소유권을 해결한 뒤 진행합니다.

공식 등록 가이드는 다른 Android 마켓별 패키지 분리를 권장합니다. 이는 강제 요건으로 해석하지 않으며, 이 문서의 실제 앱 패키지를 임의로 변경하지 않습니다. 추가 마켓을 운영하려면 별도 패키지 여부와 기존 사용자 업데이트·서명 경로를 먼저 설계합니다.

## 9. 소개·스크린샷·등급·개인정보 입력

상품명, 기본 언어, 설명, 실제 성격에 맞는 카테고리, 지원 연락처와 판매 국가를 입력합니다. 신 ZUKU 로고를 적용한 실제 앱 아이콘과 현재 정식 빌드의 화면을 사용합니다. 데스크톱 웹 화면을 모바일 앱의 화면으로 대신 제출하지 않습니다.

스크린샷은 공식 안내의 **2~8장** 범위로 준비합니다. 앱이 제공하는 화면과 기능만 소개하고, AI는 오픈 준비중이라고 명시합니다. [상품 등록 FAQ](https://onestore-dev.gitbook.io/dev/help/faq/apps)

실제 콘텐츠와 이용 흐름에 따라 요구되는 이용 등급 정보를 작성합니다. 공개 HTTPS 개인정보처리방침을 준비하고 앱 안에서도 접근할 수 있게 연결합니다. 실제 수집 항목·목적·보관 및 삭제 방법, 제3자 처리와 연락처를 반영하고, 빌드된 manifest의 권한과 설명을 맞춥니다. 불필요한 권한은 제거합니다. [원스토어 검증 가이드라인](https://onestore-dev.gitbook.io/dev/docs/review/one-store-review-guideline)

로그인해야 심사할 수 있는 기능에는 심사 담당자가 재현할 수 있는 순서와 필요한 전용 접근 방법을 콘솔의 비공개 심사 자료로 제공합니다. 운영자 권한이나 일반 사용자의 비밀번호를 공개 설명에 넣지 않습니다.

## 10. 바이너리 등록과 지원 기기 설정

상품의 바이너리 화면에서 결정한 **APK 및 서명 방식**을 선택하고 검증한 파일을 등록합니다. 업로드 후 콘솔이 읽은 패키지·버전·SDK·서명 정보를 릴리스 기록과 대조합니다. 지원 기기는 실제 포함 ABI와 minSdk, 기기 테스트 결과를 기준으로 설정하며, 현재 프리뷰에 없는 32비트 ABI를 지원한다고 주장하지 않습니다. 스토어 키 관리 방식에서는 최종 서명 APK를 내려받아 재검증합니다. [Android 바이너리 관리](https://onestore-dev.gitbook.io/dev/docs/apps/product/android/binary)

`assets/adi-registration.properties`가 없다는 **Android 개발자 인증 안내 팝업**은 원스토어 공식 문서상 정보성 안내이며 등록·검수·출시를 막는 오류가 아닙니다. 별도의 Google 인증 절차가 실제로 요구되는 경우에만 공식 절차로 대응합니다. 원스토어가 키를 관리한다면 인증에 원스토어의 최종 서명된 출시 APK가 필요할 수 있습니다. [Android 개발자 인증 FAQ](https://onestore-dev.gitbook.io/dev/help/faq/apps/developer-verification)

## 11. 유료 기능과 인앱결제는 실제 구현에 맞게

앱 등록 시 외부 결제 사용 여부를 실제 서비스 계획에 맞게 정합니다. 이 선택은 등록 후 바꿀 수 없다는 공식 안내가 있으므로, 공개 전에 운영 책임자가 결제 계획을 확정합니다. 현재 ZUKU AI가 준비중이라는 사실만으로 원스토어 결제 연동이 완료된 것은 아닙니다. [결제 방식 FAQ](https://onestore-dev.gitbook.io/dev/help/faq/apps)

유료 AI·크레딧·구독을 나중에 제공한다면 별도의 결제 릴리스를 준비합니다. 현재 공식 SDK 안내를 기준으로 라이브러리와 상품을 연동하고, 결제용 서버 인증 정보는 서버의 비밀 저장소에서 관리합니다. [IAP 사전준비](https://onestore-dev.gitbook.io/dev/tools/billing/v21/pre)

권한 지급은 서버에서 확인한 구매 결과를 기준으로 구현합니다. 서버 API로 구매 상태를 검증하고, 중복 처리·취소·환불·권한 회수를 테스트합니다. 구독은 갱신·해지·유예·보류·만료 상태와 사용자의 구독 관리 진입을 다룹니다. [서버 API](https://onestore-dev.gitbook.io/dev/tools/billing/v21/serverapi), [정기 결제](https://onestore-dev.gitbook.io/dev/tools/billing/v21/subs)

인앱결제 상품에는 콘솔에 등록한 테스트 ID로 Android Sandbox 결제 테스트를 수행해야 합니다. 성공·실패·취소 결과를 확인하고 앱을 재시작해 계정·결제 환경을 구분합니다. 상용 환경 테스트는 실제 과금이 발생할 수 있으므로 초기 검증은 Sandbox로 진행합니다. [결제 테스트](https://onestore-dev.gitbook.io/dev/tools/billing/v21/test)

## 12. 검증 요청, 반려 대응, 공개

필수 상품 정보와 바이너리를 완료하고, 결제를 사용하는 경우 요구되는 결제 테스트까지 마친 뒤 **검증요청**을 진행합니다. 제출 파일의 해시, 공개 인증서 지문, 버전, 소개 자료와 재현 절차를 릴리스 기록에 남깁니다.

콘솔의 검증 상태를 확인합니다. 반려되면 사유에 해당하는 코드·설정·소개를 수정하고 필요한 새 바이너리로 다시 요청합니다. 심사 승인과 실제 판매·배포 시작은 구분해서 확인합니다. [상품현황과 검증 상태](https://onestore-dev.gitbook.io/dev/docs/apps/applications)

배포 옵션은 **즉시적용**, **직접적용**, **예약적용** 중 실제 공개 계획에 맞게 선택합니다. 직접적용은 승인 후에도 담당자가 배포관리에서 적용해야 공개됩니다. 예약적용은 지정 시점에 반영됩니다. 공개 직전에 제출했던 판매 정보와 실제 공개 정보를 대조합니다. [배포관리](https://onestore-dev.gitbook.io/dev/docs/apps/distribution-management)

공개 후 일반 사용자 경로로 스토어에서 앱을 설치해 버전, 인증서, 시작 화면, 개인정보 링크와 기본 기능을 확인합니다. APK 페이지의 정식 배포본과도 승인된 패키지·서명 체계가 일치하는지 확인합니다.

## 13. 업데이트와 문제 발생 시 복구

업데이트는 기존 상품에 새 바이너리를 등록하는 방식으로 진행합니다. 패키지와 승인된 앱 서명 체계를 유지하고 이전보다 큰 `versionCode`를 사용합니다. 키 관리 방식을 바꿔야 한다면 Android와 원스토어의 지원 절차를 먼저 검토하고 일반 업데이트처럼 임의로 키를 교체하지 않습니다.

문제가 발생해 이전 동작으로 되돌리려면 수정한 소스를 **더 큰 versionCode의 새 릴리스**로 빌드·서명·검증하여 제출합니다. 낮은 versionCode의 과거 APK를 다시 올리는 방법으로 복구하지 않습니다. 필요하면 콘솔에서 판매 상태를 조정하고 사용자에게 영향과 후속 버전을 안내합니다. [Android 업데이트 버전 규칙](https://developer.android.com/studio/publish/versioning)

## 14. 출시 담당자에게 인계할 자료

| 자료 | 포함 내용 |
| --- | --- |
| 릴리스 식별 | 소스 revision, 패키지, versionName, versionCode |
| 제출 바이너리 | 정식 APK 파일, 크기, SHA-256 |
| 서명 검증 | 공개 인증서 SHA-256, 서명 검증 결과; 비밀 키 제외 |
| 기기 검증 | 실제 설치·업데이트·모바일 화면·권한·오프라인 결과 |
| 상품 자료 | 신 로고 아이콘, 실제 스크린샷, 설명, 등급·개인정보 자료 |
| 결제 자료 | 제공하는 경우 상품 설정, Sandbox 결과, 서버 검증 결과 |
| 심사·공개 기록 | 제출 시각, 반려 수정 내역, 승인과 공개 상태, 스토어 설치 결과 |

정식 서명된 파일의 검증, 콘솔 등록, 심사 승인, 실제 스토어 공개 및 설치 확인까지 완료한 시점에 출시 완료로 기록합니다.
