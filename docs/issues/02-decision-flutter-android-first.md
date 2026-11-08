---
planned_number: 2
title: "Decision: Flutter app, Android first, iPad-ready (ADR-001)"
type: Task
labels: [decision, phase-0-foundations]
parent: 1
---

**Phase 0 · Size S · Depends on: none · Blocks: #3 and everything after**
Decision record: [`docs/adr/0001-flutter-android-first.md`](../adr/0001-flutter-android-first.md)

## Context
- The owner decided on 2026-11-08 to build for **Android first**. The research notes still list iPad as the long-term preference.
- The research said the deciding question was owning a Mac. Android needs only a computer on any OS and the free Android Studio. Installs over ADB cost nothing and are exempt from Google's developer verification (#22).
- Constraints found during verification:
  - No maintained Flutter package does Spanish *grammar-constrained* recognition on both platforms. Each platform needs a small native bridge for recognition anyway (#16, #23).
  - `sherpa_onnx` (official Flutter package, 2.0.1) supports Android (minSdk 21) and iOS 13+. Version 2.0.0 removed espeak-ng, so Spanish TTS needs phonemes or a lexicon supplied by us (#20).
  - Azure Pronunciation Assessment works over plain REST, so the scoring client is platform-neutral Dart (#17). There is no official Azure Flutter SDK.
  - Lesson audio is pre-generated (#7), so on-device TTS speed (CoreML on iPad vs CPU on Android) barely matters.

## Decision
- **Flutter** (stable 3.47.x / Dart 3.13 at the time of writing; use the current stable).
- **Android first.** Create the iOS folder from day one but don't build it until #23.
- Native code only behind small platform channels:
  - Kotlin bridge for Vosk on Android (#16)
  - Swift bridge for Apple speech recognition later (#23)

## Options considered
| Option | Pros | Cons |
|---|---|---|
| **Flutter (chosen)** | One codebase for UI, lesson engine, spaced repetition, scoring and networking. The iPad port is mostly a speech bridge plus build setup. Mature audio and recording packages | Needs a platform channel for the recognizer; slightly larger APK |
| Native Kotlin + Jetpack Compose | Direct access to Vosk, sherpa-onnx and Media3; simplest debugging | iPad later means a rewrite |
| Kotlin Multiplatform + Compose Multiplatform | Native Android, shared logic and UI with iOS | Smaller ecosystem for iOS audio and recording; more build complexity for a hobby project |
| Native Swift (iPad first) | Best on-device AI on iPad | Needs a Mac; owner chose Android first |

## Consequences
- Development works on any OS: Android Studio, the Flutter SDK and a USB cable.
- Speech recognition, mic capture, system TTS and secure storage sit behind Dart interfaces. The iOS port then swaps implementations, and tests use fakes (#9).
- Starting package set (check current versions when scaffolding in #3):

| Package | Used for |
|---|---|
| `flutter_riverpod` | State |
| `go_router` | Navigation |
| `drift` + `sqlite3_flutter_libs` | Progress database |
| `just_audio` | Clip playback |
| `record` | Mic, PCM stream |
| `permission_handler` | Mic permission |
| `flutter_secure_storage` | Device token |
| `http` | Network calls |
| `flutter_tts` | System TTS fallback |
| `freezed` + `json_serializable` | Data models |
| `sherpa_onnx` (optional, #20) | On-device voice |

## Tasks
- [ ] Merge `docs/adr/0001-flutter-android-first.md`
- [ ] Owner confirms the choice, or comments with another one, before #3 starts

## Acceptance criteria
- [ ] ADR merged and linked from the epic (#1)
- [ ] Issue closed by the owner as accepted
