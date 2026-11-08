---
planned_number: 23
title: "iPad port (later): Apple speech bridge, system voices, build and install paths"
type: Feature
labels: [phase-6-ship, ios]
parent: 1
---

**Phase 6 · Size L · Depends on: Android v1 (#22) · Optional / later**

## Goal
Bring the same app to iPad. Because of the Flutter architecture (#2, #9), this mostly means new `platform/` implementations, re-calibration and a build pipeline.

## Platform swaps
| Interface | iOS implementation |
|---|---|
| `WordRecognizer` (#16) | A Swift bridge to **`SFSpeechRecognizer`** (es-MX / es-ES) with:<ul><li>`requiresOnDeviceRecognition = true` after checking `supportsOnDeviceRecognition`</li><li>`contextualStrings = [target] + distractors` (up to 100 phrases of 1–2 words)</li><li>the n-best `transcriptions` list fed to the shared Dart matcher</li></ul>On iOS 26, **`DictationTranscriber`** also supports contextual strings; `SpeechTranscriber` has no documented phrase biasing, so don't use it here. On-device Spanish needs the dictation assets downloaded, and Apple says on-device is "less accurate". Alternative: Vosk's iOS build, for parity with Android grammar mode; evaluate both |
| `SystemTts` (#20) | `AVSpeechSynthesizer` through `flutter_tts`. Defaults: Paulina (es-MX) and Mónica (es-ES). Enhanced and premium voices must be downloaded by a parent in Settings › Accessibility › Spoken Content › Voices; apps can't trigger the download |
| `Recorder` (#15) | `record` on iOS; `AVAudioSession` category `playAndRecord` |
| `ClipPlayer` (#10) | `just_audio`. The `.m4a` AAC clips play natively |

- **Kokoro on iOS** (`soniqo/speech-swift`) is **not recommended**:
  - needs iOS 18; downloads about 170 MB of weights at runtime;
  - its Spanish rule-based phonemizer always stresses the first syllable, taps the initial r, and has no soft b/d/g.

## Re-calibration
- Apple's recognizer behaves differently from Vosk. Re-run #19 on the iPad and keep a separate `scoring_config` per platform.

## Build and install paths (verified 2026-11; re-check)
| Situation | Path |
|---|---|
| **Mac + iPad** | Prototype with the free Personal Team: builds expire after **7 days**, max 3 devices and 3 apps per device. Then the **$99/year** Apple Developer Program gives development / Ad Hoc builds valid for about a year, installed via Xcode or Finder with **Developer Mode** on the iPad. TestFlight not needed |
| **No Mac** | $99/year, then GitHub Actions on `macos-26`: `flutter build ipa`, sign with an App Store Connect API key (fastlane or `xcodebuild -allowProvisioningUpdates`), upload to **TestFlight**. Builds expire after **90 days**, so schedule a monthly rebuild. **TestFlight terms don't allow users under 13**: install under a **parent's** Apple Account on the iPad. Xcode Cloud needs a Mac for its first setup. macOS runners are free for public repos and about $0.062/min for private ones *(verify)* |

- All App Store Connect uploads must be built with **Xcode 26 / the iOS 26 SDK** (required since 2026-04-28).

## Tasks
- [ ] Decide the build path (Mac or no Mac); set up signing
- [ ] Swift recognizer bridge plus a Dart implementation; compare it with Vosk iOS
- [ ] iOS audio session, permissions (`NSMicrophoneUsageDescription`, `NSSpeechRecognitionUsageDescription`), backup settings
- [ ] Re-calibrate (#19) and write the iOS `scoring_config`
- [ ] `docs/install-ios.md`

## Acceptance criteria
- [ ] Feature parity with Android v1 on the iPad
- [ ] Recognition decisions within the calibration targets
- [ ] Progress export/import works between Android and iPad (shared JSON format, #14)
