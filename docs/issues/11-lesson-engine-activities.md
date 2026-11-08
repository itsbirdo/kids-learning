---
planned_number: 11
title: "Lesson engine: session composer and activity types"
type: Feature
labels: [phase-2-core-app, "area: app"]
parent: 1
---

**Phase 2 · Size L · Depends on: #5, #7, #8, #9, #10, #12 · Blocks: #13, speaking activities in #16/#17**

## Goal
Turn content plus a child's progress into a 10–15 minute session of varied, gentle activities. The session ends cleanly and doesn't hook the child into "one more".

## Session shape (default 12 min, configurable per child: 10/12/15)
| Step | Time | Content |
|---|---|---|
| 1. Hello routine | 1 min | Greeting chant; child taps a face for "¿Cómo estás?" |
| 2. Review | 3–4 min | Due cards (#12) as listen-and-tap and TPR |
| 3. New words | 3–4 min | 4–6 items (3–4 for age 6). Each new item is quizzed again 2–3 items later |
| 4. Use it | 2–3 min | Picture story with questions, chant, or TPR scene |
| 5. Speak | 1–2 min | Production cards. Until #16/#17 land: "repeat and listen to yourself" |
| 6. Wrap-up | 1 min | Recap 3 words, sticker, "¡Hasta mañana!". **Ends. No autoplay** |

## Session composer (pure Dart, `domain/`)
**Inputs:** child profile and settings, cards, catalog, time budget, `now`, random seed.

**Rules**
- **Mix:** about 60% review / 40% new.
- **Backlog brake:** no new items when more than 25 cards are due (configurable).
- **New items:** come from the current unit in authored order. A unit completes when all its items reach `listen` box ≥ 2.
- **Variety:** never the same item twice in a row; mix activity types.
- **Ending:** finish on an easy item so the session ends on a success.
- **Time estimates:** each activity has an estimated duration. Stop adding activities when the budget is used; the wrap-up always runs.
- **Deterministic:** the same seed and inputs give the same session (tests rely on this).

## Activity types
| Activity | Skill | MVP | Notes |
|---|---|---|---|
| Introduce | none | ✅ | Picture, normal and slow audio, gesture animation, mascot points |
| Listen & tap | listen | ✅ | 2–4 pictures; count scales with age band and box |
| TPR "Toca…" | listen | ✅ | Tap the body part or object in a scene ("Toca tu nariz") |
| Story time | listen | ✅ | 3–6 lines with pictures, then tap-the-picture questions |
| Repeat after me | say | ✅ | Model clip → record → play back child, then model. Unscored until #16/#17 |
| Say it | say | after #16/#17 | Picture → child says the word → stars (#17) |
| Chant / song | none | stretch | Animated lyrics; not graded |
| Drag & build | listen | stretch | "Dress the character", "¿Dónde está?" placement |

## Feedback rules
- **Never fail.** A wrong tap gets a gentle "¡Otra vez!", a highlight and a replay. A second miss shows the answer and moves on.
- **Only first-try correctness** is reported to the SRS (#12).
- **Instructions:** English audio early on, faded to the Spanish classroom words from Unit 1 according to progress and the parent setting. Captions are optional (age 8+).

## Interfaces
- `ActivitySpec` (domain): type, items, distractors, prompt clips.
- `ActivityWidget` (UI): the screen for one activity.
- `ActivityResult`: `{itemId, skill, firstTryCorrect, attempts, stars?, durationMs}`. Sent to the SRS (#12) and rewards (#13).

## Tasks
- [ ] Composer plus property-style unit tests: no repeats, caps respected, deterministic, always ends with wrap-up
- [ ] Activity framework (spec, widget, result) and session runner (pause, resume, quit to home)
- [ ] MVP activity widgets, with widget and golden tests at tablet size
- [ ] Scene renderer shared with #8
- [ ] Hook up "Say it" when #16/#17 are ready

## Acceptance criteria
- [ ] A full 12-minute session runs on the tablet from Unit 1–3 content with no adult help (checked in a #25 playtest)
- [ ] Composer tests cover new-child, backlog-heavy and all-mastered cases
