---
planned_number: 22
title: "Android release build, signing, install on family tablets, updates and backup"
type: Task
labels: [phase-6-ship, "area: infra", android]
parent: 1
---

**Phase 6 · Size S–M · Depends on: Phases 0–3 for v1 (can start once #3 is done) · Completes: MVP**

## Goal
Get v1 onto the kids' tablet(s) and keep updating it **without losing progress**, at zero cost.

## Signing
- Create a release keystore with `keytool`. Store it **outside the repo** and back it up in a password manager.
- `android/key.properties` is gitignored.
- **If the key is lost,** updates can't install over the old app. Uninstalling wipes progress unless it was exported (#14).

## Build
- `flutter build apk --release --split-per-abi`. Install `app-arm64-v8a-release.apk` on modern tablets.
- Version as `x.y.z+build` in `pubspec.yaml`, and keep a `CHANGELOG.md`.
- R8/minify keep rules for Vosk/JNA (#16) and any sherpa-onnx classes (#20). Smoke-test the release build itself, not just debug.
- APK budget: under 150 MB (Vosk model ~39 MB, audio ~30 MB, images under 20 MB, Flutter engine and code).

## Install
- On the tablet:
  1. Enable Developer options and USB debugging.
  2. Run `adb install -r app-arm64-v8a-release.apk`. The `-r` keeps app data.
- Wireless option (Android 11+): `adb pair` / `adb connect` with Wireless debugging.
- **Developer verification (verified 2026-11)**
  - **ADB installs are exempt** and skip the 24-hour advanced-flow wait.
  - The Sept 30, 2026 enforcement covers only installs from participating stores in Brazil, Indonesia, Singapore and Thailand. Global rollout is planned for 2027; re-check each year.
- **Optional:** a free limited-distribution developer account (device cap 20 or 50; sources conflict) allows cable-free installs. A full Play Console account is $25.
- **Fire tablets:** no Google services. Vosk and bundled clips work, but the system TTS fallback (#20) uses Amazon's engine; check on the device.

## Tablet setup checklist (`docs/install-android.md`)
- [ ] Kid profile or Family Link, *or* screen pinning to keep the child in the app
- [ ] Spanish voice data installed for system TTS (#20)
- [ ] Mic permission granted during parent setup (#15)
- [ ] Gateway pairing done (#18); online scoring on or off (#14)
- [ ] Auto Backup on (#14); first manual export saved

## Release checklist (each update)
1. `kl validate` → `kl build`. Run the tests; CI must be green.
2. Bump the version and update `CHANGELOG.md`.
3. Build the release APK; smoke-test on one device: start a session, speak, see the parent dashboard.
4. **Export progress**, then `adb install -r` on each tablet. Check that progress is still there.

## Optional CI
- On a `v*` tag, build a signed release APK in GitHub Actions (keystore as a base64 secret) and attach it to a GitHub Release. Only do this if the repo is **private**.

## Acceptance criteria
- [ ] v1.0 installed on the kids' tablet(s)
- [ ] An upgrade install keeps progress (tested once deliberately)
- [ ] `docs/install-android.md` written and followed once end to end
