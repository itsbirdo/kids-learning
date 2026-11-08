---
planned_number: 25
title: "Testing strategy, QA checklists and kid playtests"
type: Task
labels: [cross-cutting, "area: app"]
parent: 1
---

**Cross-cutting · Size M (set up once, then ongoing) · Depends on: #3**

## Goal
Bugs caught in CI before they reach the tablet; app design checked against how our kids actually behave.

## Automated tests
| Layer | Tooling | What |
|---|---|---|
| Domain (pure Dart) | `test` | Composer (#11), scheduler (#12), matcher (#16), star decisions (#17), Azure parser (#17). **≥ 80% line coverage** on `domain/` |
| Widgets | `flutter_test` + goldens | Every activity and kid screen at the tablet resolution(s); parent screens |
| Data | drift test utilities | Repositories, migrations, export/import round trip (#14) |
| Integration (device) | `integration_test` (Patrol if permission dialogs need driving) | First run → profile → full session; mic permission; airplane mode; interruptions |
| Native | JUnit (Kotlin) | Vosk bridge with an adult or TTS fixture WAV (#16) |
| Tools | `pytest` | Validator rules, phonetic key, cache keys, post-processing, eval metrics |
| Gateway | `vitest` (Workers pool) | Auth, caps, caching, kill switch, upstream errors (#18) |

**Speech regression without kids' audio**
- Commit recognizer and scorer **JSON outputs** from calibration runs (#19) as fixtures. CI replays them through the Dart matcher and star logic and checks the expected decisions.
- Adult and TTS clips may be committed for end-to-end native tests.

## Content QA
- `kl validate` in CI (#6); the audio QA report and approval gate (#7); every unit reviewed by a Spanish speaker (#5).

## Manual QA checklist (each release, `docs/qa-checklist.md`)
- [ ] Fresh install and upgrade install (progress kept, #22)
- [ ] Session in airplane mode (offline scoring, system TTS fallback)
- [ ] Low volume, headphones, Bluetooth speaker
- [ ] Phone call or notification interruption; backgrounding mid-recording
- [ ] Noisy room (TV on) speaking test
- [ ] Parent gate resists a child; daily limit soft stop
- [ ] Quota exhausted: graceful fallback message (#17)

## Performance budgets (measured on the kids' tablet)
| Measure | Budget |
|---|---|
| Cold start | < 2 s |
| Activity transition | < 300 ms |
| Clip latency | < 150 ms |
| Vosk check | < 500 ms |
| Azure round trip (median) | < 1.5 s |
| Dialogue: end of child's speech → next line | < 1 s |
| APK (arm64) | < 150 MB |
| Memory | < 400 MB |

## Kid playtests
- **When:** after Phase 2 (listening lessons), after Phase 3 (speaking), then monthly.
- **Protocol:**
  - The parent watches **without helping** for the first 5 minutes.
  - Note confusion points, frustration signs (sighs, random tapping, "I don't get it"), delight moments, and time on each activity.
  - Ask three smiley-face questions: fun? easy? want to play again tomorrow?
  - Separate observations for ages 6–7 and 8–10.
- **Record:** written notes in `docs/playtests/YYYY-MM-DD.md`, with **no video, audio or full names**. Turn findings into issues.

## Tasks
- [ ] Test scaffolding and coverage reporting in CI (#3)
- [ ] Golden test setup with fixed fonts
- [ ] Device integration test script for the kids' tablet
- [ ] `docs/qa-checklist.md` and a playtest template

## Acceptance criteria
- [ ] All automated suites run in CI on every PR
- [ ] The first playtest after Phase 2 is recorded and its findings filed
