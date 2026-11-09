---
planned_number: 12
title: "Spaced repetition (Leitner) and progress model"
type: Feature
labels: [phase-2-core-app, "area: app"]
parent: 1
---

**Phase 2 · Size S–M · Depends on: #9 · Blocks: #11, #14 dashboard**
Teaching rules: [`docs/learning-methodology.md`](../learning-methodology.md) (R10–R14, R17, R18).

## Goal
Bring each word back at the right time so it sticks, using a model simple enough to explain to a parent.

## Why this model
- Spaced retrieval is one of only two "high utility" learning techniques (Dunlosky et al. 2013).
- Spacing helped primary-school vocabulary (Sobel, Cepeda & Kapler 2011; Goossens et al. 2012).
- Expanding vs fixed intervals makes little difference to final recall (Latimier et al. 2021, g ≈ 0.03). But expanding intervals keep practice success high (Kang et al. 2014), which matters for young children.
- Children's word memory improves after sleep (Henderson et al. 2012), so the first review is the next day.
- Intervals that run too long cost less than ones that are too short (Cepeda et al. 2008), so the schedule extends past 30 days.

## Model
- A **Leitner system** with one card per *(child, item, skill)*.
- **Skills:**
  - `listen`: recognise the word or phrase.
  - `say`: produce it. The `say` card unlocks when `listen` reaches box 2. Speaking practice is separate because it only improves with speaking (DeKeyser 1997).
- Whole **core-dialogue stages** (#11) are scheduled with the same intervals as one card per dialogue.

| Box | Next review |
|---|---|
| 1 | Later in the same session (re-quiz and end check, #11), then the next day |
| 2 | +1 day (after sleep) |
| 3 | +3 days |
| 4 | +7 days |
| 5 | +14 days |
| 6 | +30 days |
| 7 | +60 days |
| Mastered | +120 days, then stays at 120 |

**Updates**
| Result | Card change |
|---|---|
| First-try correct | Up one box |
| Miss | Down to box 1, with neutral feedback. Later retries after the model count as learning, not promotion |
| `uncertain` (speech-recognition rejection for ages 6–7, #11/#17) | No change |
| `heard_none`, technical failure, skipped | No change |

Whether a miss should drop a card one box or reset it to box 1 is untested; reset is the simpler choice. Make it configurable and revisit after the #19 calibration data.

## Rules
- **Slack:** a card counts as due from 1 day early (for intervals of 3 days or more) to any time late. Missed days carry no penalty and no streak loss; due cards just wait.
- **Brakes:** new items pause when either is true. Review is capped per session (#11).
  - more than 25 cards are due;
  - review accuracy over the last 2 sessions is below about 75% (heuristic; R18).
- **Day boundary:** local time with a 3 am cutoff.
- **Encounters:** track them. Aim for about 8–12 meaningful encounters per word across its first 2 weeks, in different activities (tap, TPR, story, dialogue). The composer favours items below this. There is no proven magic number (Uchihara, Webb & Yanagisawa 2019).

**Parent-facing definitions** (for #14)
| Label | Means |
|---|---|
| "Recognises" | `listen` box ≥ 3 |
| "Can say" | `say` box ≥ 3 |
| "Needs practice" | 3 or more misses in the last 7 days |

## Tasks
- [ ] `Scheduler` (pure Dart): `due(cards, now)` and `apply(card, result, now)`, with configurable intervals and miss policy
- [ ] Simulated-calendar unit tests: missed weeks, first-ever session, uncertain results, all mastered
- [ ] Integrate with the composer (#11) and the progress queries (#14)

## Acceptance criteria
- [ ] Deterministic tests for every box transition, slack and edge case
- [ ] A simulated child using it daily for 30 days ends with a sensible spread across boxes (snapshot test)
- [ ] An uncertain result never changes a box (test)

## Later
- Swap in a simplified SM-2 if Leitner proves too coarse. The interface already allows it.
