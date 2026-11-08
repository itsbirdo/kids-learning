---
planned_number: 19
title: "Calibration toolkit: our kids' speech test set, thresholds and locale choice"
type: Task
labels: [phase-3-speaking, "area: speech"]
parent: 1
---

**Phase 3 · Size M · Depends on: #15, #16, #17 · Re-run: every ~3 months**

## Why
- No published evaluation covers Azure scoring, or any recognizer, on **children learning Spanish**. Thresholds must come from our own kids.
- Even purpose-built systems disagree with experts by about ±½ star on children's single words (NOCASA 2025 baseline).
- False rejections are the costly error for children.

## In-app calibration mode (parent area)
1. Choose 40 items across units, mixing easy items with hard sounds (rr, j, ñ, ll/y, vowels).
2. The child says each item **twice**; a parent records each item once as a reference.
3. Deliberate failure cases: an English word, a wrong Spanish word, silence.
4. Right after each attempt, the parent labels it *good / OK / needs work*, with playback.
5. Export a zip (16 kHz WAVs, `labels.json`, device info, app and model versions) through the share sheet to the family computer.

**Kids' recordings never go to GitHub or CI.** Keep them under a gitignored path, e.g. `~/kids-learning-private/` (#24).

## `kl eval` (Python, on the family computer)
**What it runs**
- Python `vosk` with the **same model and grammars** as the app (`grammar.json`).
- The Dart matcher logic, through the shared fixtures; or a Python mirror with identical tests.
- Azure Pronunciation Assessment in **both es-MX and es-ES**.

**What it computes**
- Vosk true-accept and distractor-rejection rates.
- For each locale: score distributions per label and the **separation** between labels (e.g. AUC good-vs-needs-work). **Choose the locale with the best separation, not the higher mean.**
- Test-retest spread between the two attempts. If it's above 10 points, widen the star bands.

**Proposed thresholds**
- 3★ at about the 25th percentile of "good" scores.
- 2★ set so that under 5% of good-or-OK attempts fall below it.
- Vosk τ values for the matcher.

**Outputs**
- `content/scoring_config.json`: per age band, plus locale, VAD constants, τ values. It's bundled by `kl build`.
- An HTML report, kept privately.

## Regression fixtures (safe to commit)
- Recognizer **JSON outputs** (not audio) from calibration runs, plus clips recorded by adults and TTS voices.
- Used in CI to test the Dart matcher and star decisions (#25).

## Tasks
- [ ] Calibration mode UI and export (#14, #15)
- [ ] `kl eval` with the Vosk and Azure runners, metrics and report
- [ ] Write `scoring_config.json` and wire it through `kl build` → app
- [ ] First calibration run for each child; record a summary (no audio, no names) in `docs/spikes/`

## Acceptance criteria
- [ ] Thresholds and locale chosen from data and committed
- [ ] Re-run procedure documented in `docs/calibration.md`
- [ ] Spot check: on a fresh 10-item session, the parent agrees with the stars on at least 80% of items
