---
planned_number: 11
title: "Lesson engine: session composer and activity types"
type: Feature
labels: [phase-2-core-app, "area: app"]
parent: 1
---

**Phase 2 · Size L · Depends on: #5, #7, #8, #9, #10, #12 · Blocks: #13, speaking activities in #16/#17**
Teaching rules: [`docs/learning-methodology.md`](../learning-methodology.md). Rule numbers (R1–R22) below refer to it.

## Goal
Turn content plus a child's progress into a 10–15 minute session that follows the research-based loop: **hear it → do it → say it → use it → review it**. The session ends cleanly and doesn't hook the child into "one more".

## Session shape (default 12 min, configurable per child: 10/12/15)
Balances Nation's four strands (R19):

| Step | Min | Strand | Content |
|---|---|---|---|
| 1. Hello + warm-up | 1–2 | Fluency | Greeting routine, then fast, easy replay of well-known chunks |
| 2. Review | 3 | Language-focused | Due cards (#12) as retrieval: tap, act, say. Mixed across topics |
| 3. New | 3 | Language-focused | New items introduced 2–3 at a time (age caps in R13). Each is **shown 2–3× with picture, gesture and model audio before any test** (R9). Then tap retrieval, with a re-quiz after 2–3 other items (R11) |
| 4. Use it | 3 | Meaning-focused input | One of: the next **core-dialogue stage** (below), a story re-hear (re-heard on 3+ days), or a TPR scene |
| 5. Say it | 1–2 | Meaning-focused output | Production only for items whose `listen` card is at box ≥ 2 (R8, R14). Until #16/#17 land: "repeat and listen to yourself" |
| 6. End check | 1 | Retrieval | Today's new items and today's misses, once more (R11, R16) |
| 7. Wrap-up | 1 | — | Informational recap ("Today: *perro, gato, pez*"), the **grown-up turn card** (R21), "¡Hasta mañana!". **Ends. No autoplay** |

## Session composer (pure Dart, `domain/`)
**Inputs:** child profile and settings (age band), cards, catalog, time budget, `now`, random seed, recent review accuracy.

**New items**
- **Count:** ages 6–7 get 3–4, ages 8–10 get 4–6. A multi-word chunk counts as 2 (R13).
- **Order:** they come from the current unit in authored order. When a unit is a single category, mix in items from the neighbouring unit or story scene. **No more than 2 new items from the same semantic category in one batch** (R3).
- **Unit completion:** a unit completes when all its items reach `listen` box ≥ 2.

**Mix and brakes**
- About 60% review and 40% new.
- **No new items** when any of these holds (R18):
  - more than 25 cards are due;
  - review accuracy over the last 2 sessions is below ~75%;
  - the child is in their first 3 sessions of a unit with a speaking backlog.

**Ordering**
- **Within-session spacing:** each new item is re-quizzed after 2–3 other items, and again in the end check (R11). That gives at least 3 retrievals today and 2 or more tomorrow (R10).
- **Variety:** never the same item twice in a row; mix activity types and topics in review.
- **Ending:** the last item before the wrap-up is an easy, known item, so the session ends on a success.

**Timing and determinism**
- Each activity has an estimated duration. The composer stops adding activities when the budget is used; the end check and wrap-up always run.
- The same seed and inputs give the same session (tests rely on this).

## Activity types
| Activity | Skill | MVP | Notes |
|---|---|---|---|
| Introduce | none | ✅ | Picture, normal and slow audio, gesture animation **the child copies** (R2), mascot points. Shown 2–3× before any test |
| Listen & tap | listen | ✅ | 2–4 pictures; the count scales with age band and box |
| TPR "Toca… / Salta…" | listen | ✅ | Tap the body part or object in a scene, or act it out |
| Story time | listen | ✅ | 3–6 lines with pictures and tap-the-picture questions. The same story returns on 3+ days (R5) |
| **Core dialogue** | listen → say | ✅ | 4–8 line, two-voice unit dialogue (#5). It moves forward one stage per session (R15). See below |
| Repeat after me | say | ✅ | Model → record → play back the child, then the model. **Backward build-up** for lines over 4 words ("…la escuela" → "a la escuela" → "Voy a la escuela") |
| Say it | say | after #16/#17 | Picture → child says the word → stars (#17). Hint-first feedback (below) |
| Pattern swap | say | after #16 | One slot changes with the picture: "Quiero **un taco**" → "Quiero **agua**". The answer depends on meaning; never mechanical substitution. Bursts of 2 min or less |
| Explicit tip | none | ✅ (ages 8–10 only) | Optional 10–15 s English "notice the pattern" card (*el* perro / *la* casa), shown only after the child has used the chunk (R7) |
| Chant / song | none | stretch | Fixed melody per chant; animated lyrics; not graded (R6) |
| Drag & build | listen | stretch | "Dress the character", "¿Dónde está?" placement |

### Core-dialogue stages (one stage per session, then revisited by the SRS)
1. **Listen:** the whole dialogue with pictures, twice (normal, then slow).
2. **Repeat:** line by line, with build-up for long lines.
3. **Take a role:** the app voices role A and the child says role B.
4. **Swap roles.**
5. **Variation:** a picture changes one slot; the child adapts the line.

The scripted, branching role-plays in #21 (optional) build on these same dialogues.

## Feedback rules (R16, R17)
- **Never fail.** No buzzers, no lives, no "wrong" sounds.
- **Tap activities:** a wrong tap gets a gentle "¡Otra vez!" and a replay. A second miss shows the answer, and the item comes back in the end check.
- **Say activities: hint first, then the model.**
  1. "¿Cómo se dice…?" with the picture and the first syllable.
  2. The model clip, then a retry that succeeds.
  3. Move on. The item returns in the end check.
- **Credit:** only *first-try* correctness is reported to the SRS (#12). Retries after the model count as learning, not promotion.
- **Uncertain results:** a speech-recognition rejection for ages 6–7 is reported as `uncertain` (no box change), not a miss.
- **Praise is specific and informational** ("You remembered *perro*!"), not generic ("You're so smart") (R20).
- **Instructions:** English audio early on, faded to the Spanish classroom words from Unit 1 according to progress and the parent setting. Captions are optional (ages 8+).

## Interfaces
- `ActivitySpec` (domain): type, items, distractors, prompt clips, stage (for dialogues).
- `ActivityWidget` (UI): the screen for one activity.
- `ActivityResult`: `{itemId, skill, firstTryCorrect, outcome (correct | retry | shown | uncertain | heard_none), attempts, stars?, durationMs}`. Sent to the SRS (#12) and rewards (#13).

## Optional: "Listen again" mode (R22)
- **Started by a parent** from the parent area.
- **Plays audio only:** this week's dialogues, story and chants, in a loop with gaps. For the car, bath or bedtime.
- **Doesn't change SRS progress.** No screen interaction is needed.

## Tasks
- [ ] Composer plus property-style unit tests:
  - no repeats in a row
  - age caps respected
  - at most 2 same-category items in a new batch
  - re-quiz positions
  - accuracy and backlog brakes
  - deterministic
  - always ends with end check and wrap-up
- [ ] Activity framework (spec, widget, result) and session runner (pause, resume, quit to home)
- [ ] MVP activity widgets, including the core-dialogue stages and build-up, with widget and golden tests at tablet size
- [ ] Scene renderer, shared with #8
- [ ] Hook up "Say it" and "Pattern swap" when #16/#17 are ready
- [ ] "Listen again" mode (stretch)

## Acceptance criteria
- [ ] A full 12-minute session runs on the tablet from Unit 1–3 content with no adult help (checked in a #25 playtest)
- [ ] Each new item gets at least 3 retrievals in its first session and at least 2 the next day (log check)
- [ ] Composer tests cover new-child, backlog-heavy, low-accuracy and all-mastered cases
