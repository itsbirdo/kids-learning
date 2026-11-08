---
planned_number: 12
title: "Spaced repetition (Leitner) and progress model"
type: Feature
labels: [phase-2-core-app, "area: app"]
parent: 1
---

**Phase 2 · Size S–M · Depends on: #9 · Blocks: #11, #14 dashboard**

## Goal
Bring each word back at the right time so it sticks, using a model simple enough to explain to a parent.

## Model
- A **Leitner system with 5 boxes**, one card per *(child, item, skill)*.
- **Skills:**
  - `listen`: recognise the word.
  - `say`: produce the word. The `say` card unlocks when `listen` reaches box 2.

| Box | Next review |
|---|---|
| 1 | Later in the same session, or the next session |
| 2 | +1 day |
| 3 | +3 days |
| 4 | +7 days |
| 5 | +14 days |
| Mastered (after box 5 correct) | +30 days |

**Updates**
| Result | Card change |
|---|---|
| First-try correct | Up one box |
| Miss | Back to box 1, with neutral feedback |
| `heard_none`, technical failure, or skipped | No change |

## Rules
- **Backlog brake:** new items pause while more than 25 cards are due; review is capped per session (#11).
- **Missed days:** no penalty and no streak loss. Due cards just wait.
- **Day boundary:** local time with a 3 am cutoff.
- **Encounters:** track them. Aim for 8+ per word across at least 3 sessions; the composer favours items below this.

**Parent-facing definitions** (for #14)
| Label | Means |
|---|---|
| "Recognises" | `listen` box ≥ 3 |
| "Can say" | `say` box ≥ 3 |
| "Needs practice" | 3 or more misses in the last 7 days |

## Tasks
- [ ] `Scheduler` (pure Dart): `due(cards, now)`, `apply(card, result, now)`
- [ ] Simulated-calendar unit tests: missed weeks, first-ever session, all mastered
- [ ] Integrate with the composer (#11) and the progress queries (#14)

## Acceptance criteria
- [ ] Deterministic tests for every box transition and edge case
- [ ] A simulated child using it daily for 30 days ends with a sensible spread across boxes (snapshot test)

## Later
- Swap in a simplified SM-2 if Leitner proves too coarse. The interface already allows it.
