---
planned_number: 4
title: "Spike: validate speech recognition, scoring and voices on the real tablet with our kids"
type: Task
labels: [spike, phase-0-foundations, "area: speech"]
parent: 1
---

**Phase 0 · Size M (timebox 3–4 days) · Depends on: #2 · Feeds: #7, #15, #16, #17, #20**

## Why
Research could not answer the questions that decide the speech design:
- How do recognizers and scorers handle *our* children speaking beginner Spanish?
- How do the voices sound to them?

No published benchmark covers children learning Spanish. Answer this before building Phase 3.

## Experiments
**1. Hardware inventory → `docs/hardware.md`**
- Tablet model, Android version, RAM, CPU.
- Are Google services present? Amazon Fire tablets lack them, which changes system TTS and the system recognizer.
- Which TTS engines and voices are installed?

**2. Vosk grammar check**
- Use `vosk-model-small-es-0.42` (~39 MB, Apache-2.0). Only the small models support grammar mode.
- First run Python `vosk` on a laptop over the recordings. Then run the official Android demo on the tablet to measure latency.
- Word set: 20 words from Units 1–4. Each has 2–4 sound-alike distractors plus `[unk]` in the grammar (e.g. `["perro","pero","pelo","[unk]"]`).
- Each child says each target twice, plus some deliberate failures: a distractor, the English word, silence.

| Measure | What it means |
|---|---|
| True accept | Target recognized when it was said |
| Distractor rejection | Distractor not accepted as the target |
| `[unk]` rate | How often nothing in the grammar matched |
| Tablet latency | Time for a 2 s clip |

**3. Azure Pronunciation Assessment** (REST, F0 resource)
- Send the same recordings with `es-MX` and with `es-ES`.
- Confirm the known failure: a wrong single word still scores high.
- Check what `EnableMiscue: true` does.
- Measure round-trip latency on home Wi-Fi.
- Note how much F0 quota the spike used.

**4. Voice audition** (lesson audio)
- 15 lines: single words with an article, a question, a story line, praise lines, and one line with a child's name.
- Candidates:

| Candidate | Notes |
|---|---|
| Azure neural/HD es-MX voices (2–3) | Terms-clean |
| ElevenLabs `eleven_v4` Spanish voices | Listening only; whether we may use it depends on the #24 terms review |
| Android system TTS | Google es-MX / es-US / es-ES voice |
| Piper `es_MX-claude-high` | Via the `piper` CLI on a laptop |

- Gemini TTS is excluded on terms (#24). Kokoro is excluded: ungraded Spanish voices, weak on short words.
- Also render slow variants: Azure SSML `<prosody rate="-15%">` and ffmpeg `atempo=0.85`.
- Kids and a parent rate each sample blind, 1–5.

**5. Spanish variety**
- Confirm the family's choice (default es-MX). It drives voice, scoring locale and vocabulary (#5).

**6. Recording UX**
- Can a 6-year-old use *tap to talk with auto-stop*? Compare with *hold to talk*.
- Note mic distance and room noise.

## Rules
- Record with any recorder app and convert with `ffmpeg -ar 16000 -ac 1`.
- **Kids' recordings stay on the family computer, never in the repo or CI** (#24).
- Spike scripts go in `tools/spike/` (no audio).

## Go / no-go
| Component | Go if | Otherwise |
|---|---|---|
| Vosk word check | ≥ 85% true-accept and ≥ 70% distractor rejection across kids | Try the Android on-device recognizer (API 33+ biasing strings), or Whisper-small with an expected-text prompt plus a length-deviation guard (466 MB) |
| Azure scoring | Scores separate parent-labelled good vs poor attempts on multi-syllable words | MVP ships pass/fail from Vosk plus "listen to yourself" playback |
| Lesson voice | A winner averaging ≥ 4/5, plus a terms-clean fallback | Audition more voices or design one (Azure custom / ElevenLabs Voice Design) |

## Deliverables
- [ ] `docs/hardware.md`
- [ ] `docs/spikes/2026-11-speech-spike.md` with result tables and decisions
- [ ] Comments on #7, #16, #17 and #20 with what changed
- [ ] Owner decisions ticked in #1 (tablet, Spanish variety, voice shortlist)
