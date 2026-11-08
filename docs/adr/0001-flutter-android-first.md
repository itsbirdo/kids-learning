# ADR-001: Flutter app, Android first, iPad-ready

- **Status:** Proposed. The owner chose "Android first" on 2026-11-08; the framework choice awaits confirmation in issue #2.
- **Date:** 2026-11-08

## Context
- The research notes ([original](../research/2026-11-08-original-research-notes.md)) prefer iPad. They say the deciding question is whether we own a Mac.
- The owner decided to build for **Android first**.
- Verification on 2026-11-08 ([reports](../research/)) found:
  - **Recognition:** no maintained Flutter package does Spanish grammar-constrained speech recognition on both platforms. Each platform needs a small native recognizer bridge anyway: Vosk on Android, Apple Speech on iOS.
  - **sherpa-onnx:** there is an official Flutter package (2.0.1; Android minSdk 21, iOS 13). Version 2.0.0 removed espeak-ng, so Spanish TTS needs phonemes or a lexicon from us.
  - **Scoring:** Azure Pronunciation Assessment works over plain REST, so the scoring client can be platform-neutral Dart. There is no official Azure Flutter SDK.
  - **Lesson audio** is pre-generated, so on-device TTS speed differences between iPad (CoreML) and Android (CPU) hardly matter.
  - **Installs:** ADB installs on Android are free and exempt from Google's developer verification.

## Decision
- Build the app in **Flutter**, using the current stable release (3.47.x / Dart 3.13 at the time of writing).
- **Target Android first.** The iOS folder exists from day one but isn't built until issue #23.
- Platform-specific code lives only behind small interfaces in `app/lib/platform/`:
  - recognizer
  - recorder
  - clip player
  - system TTS
  - secure storage
  - gateway client

## Options considered
| Option | Pros | Cons |
|---|---|---|
| **Flutter (chosen)** | One codebase for UI, lesson engine, SRS, scoring and networking; the iPad port is mostly a speech bridge plus build setup | Platform channel for the recognizer; slightly larger APK |
| Native Kotlin + Jetpack Compose | Direct native libraries; simplest debugging | iPad means a rewrite |
| Kotlin Multiplatform + Compose Multiplatform | Native Android, shared code with iOS | Smaller iOS audio ecosystem; more build complexity |
| Native Swift, iPad first | Best on-device AI | Needs a Mac; not the owner's choice |

## Consequences
- **Tooling:** development works on any OS with Android Studio, the Flutter SDK and a USB cable.
- **iOS port** (#23): implement the `platform/` interfaces in Swift and re-calibrate scoring.
- **Pure Dart domain:** the domain layer (composer, SRS, matcher, star decisions) has no Flutter imports. It's shared and unit-tested on both platforms.
