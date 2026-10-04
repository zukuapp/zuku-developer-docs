# Publish the ZUKU Android app on ONE store

Verified on October 4, 2026. This guide takes the release owner from production signing through registration, review, publication, and updates. It does not create a developer account or upload an app automatically.

## 1. Identify the app and its current status

The submission is the native Android app. `@zukujs/cli`, its shared-runtime `zuku` and `zukujs` commands, and the game packages produced by the CLI are separate artifacts. A game package is not an Android APK and must not be submitted as one.

The preview APK currently offered on the [ZUKU APK page](https://apk.zuzunza.com/) was independently measured with these values.

| Field | Current preview |
| --- | --- |
| Package / applicationId | `com.zuzunza.zuku` |
| versionName / versionCode | `0.3.0` / `3` |
| minSdk / targetSdk | `24` / `36` |
| Included ABIs | `arm64-v8a`, `x86_64` |
| debuggable | `false` |
| Signing | Android Debug certificate |
| APK SHA-256 | `ee0cc23906ba44681b34ac9542b0f924504dac818ff03b151122c6a04e15647c` |

This preview does not have production release signing. The inspected preview and default Gradle release configuration use `signingConfigs.debug`. The official build script also supports a separate production signing configuration, described in step 5. A successful `assembleRelease` build or `debuggable=false` does not establish that a protected production key was used; verify the actual artifact.

ZUKU AI in the app is currently **Coming soon**. The listing, screenshots, and review instructions must reflect that state. Do not advertise unverified AI access, subscriptions, or purchases as available features.

## 2. Choose the format and signing arrangement

ONE store supports both APK and AAB for Android. For this app's first production release, a **production-signed APK with a developer-managed key** makes it straightforward to align the APK website and store signing certificates. If choosing AAB, also verify the certificate on the final APK generated for users. [Supported formats](https://onestore-dev.gitbook.io/dev/eng/docs/apps)

An app converted from APK to AAB cannot return to APK. Design certificate continuity before distributing the same app through multiple channels. An upload key is distinct from the app signing key used on devices. [Android App Bundle FAQ](https://onestore-dev.gitbook.io/dev/eng/help/faq/apps/one-store-android-app-bundle)

For a developer-managed APK, the console's **Disable app signatures** option still requires a signed APK. It means the developer retains signing-key management. If selecting ONE store key management, follow its official key registration process and verify the final signed APK downloaded from the console. [Binary and signing options](https://onestore-dev.gitbook.io/dev/eng/docs/apps/product/android/binary)

## 3. Prepare the developer account

1. Register or sign in to [ONEconsole](https://dev.onestore.net/) using the app owner's developer account.
2. Supply the correct individual or business identity and working contact information.
3. Assign release access to the responsible people. Complete the required settlement information if planning paid distribution.
4. Decide the launch countries, languages, price, and payment arrangement before registering the product. Follow the current requirements shown for the actual account. [Developer introduction](https://onestore-dev.gitbook.io/dev)

## 4. Prepare production signing and the upgrade path

Use a production keystore controlled by the app owner and configure the release build to use it. If this app already has a production key, start from that key and its distribution history. Android Studio provides **Build → Generate Signed App Bundle or APK → APK**. [Android app signing](https://developer.android.com/studio/publish/app-signing)

Keep the keystore and passwords out of Git, documentation, chat, and build logs. Store them with restricted access and maintain a separate encrypted backup whose recovery has been checked. Record the public certificate's SHA-256 fingerprint in the handoff, rather than private key material.

The current preview certificate has this public fingerprint. Finding it on the production artifact means the preview signer is still in use.

```text
fac61745dc0903786fb9ede62a962b399f7348f0bb6f899b8332667591033b9c
```

The existing Debug-signed preview cannot be updated normally with an app bearing a different production certificate, even when the package name matches. Explain data preservation and migration to preview users first. Transition test devices only after preserving necessary data; do not automate app removal. Future production website and store builds should retain the same package and approved signing arrangement.

## 5. Build the production release

Freeze the release source and `package-lock.json`. Prepare the project's Node, JDK, Android SDK, and Gradle wrapper environment. Retain `com.zuzunza.zuku` as the application ID.

The new `versionCode` must exceed every previously distributed or registered version. The publicly verified preview uses `3`; use at least `4` next if there is no higher registration history. If the console contains a higher value, exceed it. Choose `versionName` separately for the actual release. [Android versioning](https://developer.android.com/studio/publish/versioning)

The project's official build script generates production signing configuration when all four settings are supplied: `ZUKU_ANDROID_KEYSTORE_PATH`, `ZUKU_ANDROID_KEYSTORE_PASSWORD`, `ZUKU_ANDROID_KEY_ALIAS`, and `ZUKU_ANDROID_KEY_PASSWORD`. Inject the key and passwords through a protected local environment or CI secret store. Keep commands containing their values out of documentation, logs, and shell history.

Run the official `build:apk` script on Linux or macOS. On Windows, use Linux Node, JDK, and Android SDK inside WSL2; running this script with native Windows Node is unsupported.

Run these commands at the app project root **after securely providing all four production signing settings**. An APK build with missing settings can use the preview signer, so the certificate verification in the next step is essential.

```bash
npm ci
npm run typecheck
npm test
npm run build:apk
```

The script generates and configures the Android project before building the release. For a direct build of an Android project that already has production signing configured, the wrapper command is:

```bash
cd android
./gradlew :app:assembleRelease
```

On Windows, use `gradlew.bat :app:assembleRelease`. The default app-module output is `app/build/outputs/apk/release/app-release.apk`; select the actual output if the project customizes its name. [Command-line Android builds](https://developer.android.com/build/building-cmdline)

Preserve the preview artifact. Save the production result as a separate release instead of replacing or re-signing the preview in place. Do not modify the APK after signing.

## 6. Verify the exact submission file

At the project root, use an environment where Android SDK `apkanalyzer`, `aapt2`, and `apksigner` are available. These commands assume the default Gradle output path.

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

On macOS, the final command can be `shasum -a 256 "$ZUKU_ANDROID_APK"`. These tools inspect the manifest, included ABIs, signature, and file hash. [APK Analyzer](https://developer.android.com/tools/apkanalyzer), [AAPT2](https://developer.android.com/tools/aapt2), [apksigner](https://developer.android.com/tools/apksigner)

Check the package, increased versionCode, `debuggable=false`, supported ABIs, and expected production certificate fingerprint. Cryptographic signature verification does not establish production key ownership or store approval. Freeze the exact verified file as the submission artifact.

## 7. Test the release on devices

Test a fresh installation and an update from the previous production version. On Android devices that will be supported, exercise startup, login and logout, navigation, game playback, back navigation, the keyboard, denied permissions, and network loss and recovery. Only describe screens and features that actually exist in the release.

Also check narrow screens, larger text, dark mode, and app restart. The AI screen must retain **Coming soon** and must not present a closed backend as available. Confirm that the privacy policy and support links work.

## 8. Register the Android product

In ONEconsole, open **Apps → Applications → Register app**, then select **Official release / Android**. Enter `com.zuzunza.zuku`, matching the verified APK. The package cannot be changed after registration. If the owner already has the same product registered, use its update flow. [Register an app](https://onestore-dev.gitbook.io/dev/docs/apps/register-app)

Calling the current download a preview is different from selecting ONE store's **Beta** product type. A Beta product requires a new product with a different package for official release, so this procedure selects Official release. Resolve ownership if another account is reported as owning the package.

The registration guide recommends separate packages for other Android markets. Treat this as a recommendation, not a mandatory requirement or permission to rename this app's existing package. Plan package separation, existing-user upgrades, and signing continuity before adding another market.

## 9. Supply listing, screenshots, rating, and privacy information

Enter the title, default language, description, appropriate category, support contacts, and launch countries. Use the new ZUKU logo and screenshots from the actual production app. Do not present desktop website captures as mobile app screenshots.

Prepare **2–8 screenshots**, as specified by the official FAQ. Show available features and identify AI as Coming soon. [Product FAQ](https://onestore-dev.gitbook.io/dev/eng/help/faq/apps)

Complete rating information based on actual content and use. Publish an accessible HTTPS privacy policy and link to it inside the app. Describe actual collection, purposes, retention and deletion, third-party processing, and contacts. Align disclosures with the built manifest's permissions and remove unnecessary permissions. [Review guideline](https://onestore-dev.gitbook.io/dev/docs/review/one-store-review-guideline)

For features requiring authentication, provide reproducible review steps and any dedicated review access through private console review materials. Do not put administrator credentials or user passwords in the public listing.

## 10. Upload the binary and set device support

Select the agreed **APK format and signing option**, then upload the verified file. Compare the package, version, SDK, and signing details read by the console with the release record. Base device support on the included ABIs, minSdk, and tested devices. Do not claim unsupported 32-bit ABIs. With store-managed signing, download and verify the final signed APK. [Android binary management](https://onestore-dev.gitbook.io/dev/eng/docs/apps/product/android/binary)

ONE store describes the popup about a missing `assets/adi-registration.properties` file as informational: it does not block registration, review, or launch. Follow the separate official Google verification process when applicable. Store-managed keys may require the final ONE store-signed release APK for that process. [Android developer verification FAQ](https://onestore-dev.gitbook.io/dev/help/faq/apps/developer-verification)

## 11. Match payments to implemented functionality

Decide the external-payment setting from the actual product plan before registration; the official FAQ says it cannot be changed afterward. The release owner should settle this choice before launch. A Coming soon AI feature does not establish that ONE store billing has been integrated. [Payment configuration FAQ](https://onestore-dev.gitbook.io/dev/eng/help/faq/apps)

Prepare a separate billing release before introducing paid AI, credits, or subscriptions. Use the current official SDK guidance and configure products. Keep server billing authentication material in server-side secret storage. [IAP preparation](https://onestore-dev.gitbook.io/dev/tools/billing/v21/pre)

Grant entitlements from server-verified purchase state. Test duplicate processing, cancellations, refunds, and entitlement removal. Handle subscription renewal, cancellation, grace, hold, and expiry, including access to subscription management. [Server API](https://onestore-dev.gitbook.io/dev/tools/billing/v21/serverapi), [Subscriptions](https://onestore-dev.gitbook.io/dev/tools/billing/v21/subs)

For IAP products, register test IDs in the console and complete Android Sandbox payment testing. Verify success, failure, and cancellation, and restart the app when changing test environments. Production tests can charge real money; use Sandbox for initial validation. [Payment testing](https://onestore-dev.gitbook.io/dev/tools/billing/v21/test)

## 12. Request review, resolve rejections, and publish

Finish the required listing and binary information and any required IAP tests, then request review. Retain the file hash, public signing fingerprint, version, listing assets, and reproduction steps in the release record.

Monitor the review status. Address the specific rejection reason and resubmit the corrected configuration, listing, or binary. Check approval and actual distribution separately. [Product and review states](https://onestore-dev.gitbook.io/dev/docs/apps/applications)

Choose immediate, manual, or scheduled application according to the launch plan. Manual application requires the owner to apply the approved release in distribution management. Scheduled application uses the selected date. Compare the submitted sale information with the intended launch information before publication. [Distribution management](https://onestore-dev.gitbook.io/dev/docs/apps/distribution-management)

After publication, install through the normal customer store flow. Check the version, signer, startup, privacy link, and basic functions. Confirm that the production APK website distribution also follows the approved package and signing arrangement.

## 13. Update and recover from problems

Upload a new binary to the existing product. Retain the package and approved signing arrangement and increase `versionCode`. If key management must change, review the supported Android and ONE store procedures first; do not replace the key as if it were an ordinary update.

To restore previous behavior, rebuild the corrected source as a **new release with a higher versionCode**, sign it, verify it, and submit it. Do not attempt recovery by uploading an older APK with a lower versionCode. Adjust the sale state in the console when necessary and explain the impact and replacement version to users. [Android update version rules](https://developer.android.com/studio/publish/versioning)

## 14. Hand off the release record

| Deliverable | Required content |
| --- | --- |
| Release identity | Source revision, package, versionName, versionCode |
| Submission artifact | Production APK, file size, SHA-256 |
| Signature evidence | Public certificate SHA-256 and verification result; no private key |
| Device evidence | Installation, upgrade, mobile UI, permissions, and offline results |
| Listing materials | New logo icon, real screenshots, description, rating and privacy information |
| Billing evidence | When offered: products, Sandbox results, and server verification |
| Review and launch record | Submission time, rejection fixes, approval, publication, and store installation results |

Record the release as complete after the production file is verified, registered, approved, publicly distributed, and successfully installed through the store.
