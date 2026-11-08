---
planned_number: 17
title: "Pronunciation scoring with Azure + kid-friendly star feedback"
type: Feature
labels: [phase-3-speaking, "area: speech"]
parent: 1
---

**Phase 3 · Size M · Depends on: #15, #16, #18 (tokens) · Tuned by: #19**

## Goal
After #16 confirms the right word, Azure Pronunciation Assessment tells us *how well* it was said. That becomes 1–3 stars and one gentle tip. No numbers are ever shown to the child.

## What Azure gives for Spanish (verified 2026-11; re-check before freezing)
- **Spanish locales:** `es-MX` and `es-ES`. Microsoft says to test both; #19 picks one.
- **Available:** accuracy, fluency, completeness and PronScore, at full-text and word level, plus the word `ErrorType` (None, Omission, Insertion, Mispronunciation).
- **en-US only, so not usable here:** prosody, phoneme *names* (Spanish phoneme entries come back with empty labels), syllables, N-best phonemes, content score.
- **Known failure:** short phrases and single words often score about 100 whatever is said. That's why #16 gates first, and `EnableMiscue` is on.
- **Children:** Microsoft's transparency note says grading for children's learning "might not be as strict" as for adults, and leaves thresholds to the developer. There is no benchmark for child L2 Spanish, so calibrate on our kids (#19).

## Transport: REST short audio (plain Dart `http`)
**Request**
```
POST https://{region}.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?language=es-MX&format=detailed
Authorization: Bearer {token from #18}
Content-Type: audio/wav; codecs=audio/pcm; samplerate=16000
Accept: application/json
Pronunciation-Assessment: base64({"ReferenceText":"el perro","GradingSystem":"HundredMark","Granularity":"Word","Dimension":"Comprehensive","EnableMiscue":true})
```
- **Limits:** at most 30 s of audio for assessment; final results only. Our clips are 1–5 s.
- **Omit** `EnableProsodyAssessment`, `PhonemeAlphabet` and `NBestPhonemeCount` (en-US only).
- **Why REST, not the SDK:** there is no official Flutter SDK. The community packages have quality warnings, or are GPL.

**Response** (parse defensively; the REST and SDK JSON layouts differ)
- `RecognitionStatus`: Success, NoMatch, InitialSilenceTimeout or BabbleTimeout.
- `NBest[0]`: `Lexical`, `AccuracyScore`, `FluencyScore`, `CompletenessScore`, `PronScore`, and `Words[] {Word, AccuracyScore, ErrorType}`. Scores may sit under a nested `PronunciationAssessment{}`.

## Decision pipeline (pure Dart, `domain/`)
1. **Gate.** If Azure status isn't Success *and* #16 says `NONE`, say "No te escuché" and retry. This is not an attempt.
2. **Right word?**
   - Accept if #16 `ACCEPT`, *or* the normalised `Lexical` contains the target.
   - If #16 says `RETRY` and `Lexical` lacks the target: retry with the model clip.
   - If the target's `ErrorType` is `Omission`, that word scores 0.
3. **Score.**
   - Word score = the word's `AccuracyScore`.
   - Phrase score = mean over the reference words (omissions = 0). Insertions such as "eh" are ignored.
   - Ignore fluency and completeness for 1–3-word items. Fluency may only *add* a bonus.
4. **Stars** (starting values; #19 replaces them):

   | Score | Stars |
   |---|---|
   | ≥ 75 | 3★ |
   | ≥ 50 | 2★ |
   | Right word heard | 1★ |

   - Age-band offsets: −5 for ages 6–7, +5 for ages 9–10. Add the per-child strictness offset (#14).
   - Hysteresis: show the best attempt, and never lower stars already shown.
5. **Feedback.**
   - Praise first.
   - At most **one** word to retry (the lowest one under 50), with its model clip.
   - Tips come from content `hard_sounds` (rr, j, ñ), not from phoneme scores.
6. **Retries.** At most 3. Then play the model, award the best score, move on, and re-queue the item through the SRS (#12).
7. **Auto-tune** (weekly, bounded ±10): if a child gets more than 85% 3★, raise the threshold by 3; under 40%, lower it by 3.

## Offline or quota-exhausted mode
- Vosk only: `ACCEPT` gives 2★, or 3★ if confidence ≥ τ_high; otherwise retry.
- The UI is identical; the parent dashboard notes "offline scoring".

## Quota, cost and privacy
- **Free tier:** F0 gives 5 audio hours per month, and its quota can't be raised.
- **Expected use:** 50 attempts a day × about 4 s ≈ **1.7 h per child per month**, so F0 covers up to 2 kids. Paid S0 is about $1 per audio hour *(verify)*.
- **Tracking:** count seconds locally (`usage` table) and in the gateway (#18). Warn the parent at 80%; fall back to offline mode at 100%.
- **Privacy:**
  - never set `storeAudio` or enable audio logging (Azure doesn't log by default);
  - store JSON results only, never audio (#9, #24).

## Tasks
- [ ] `AzureScorer` REST client with timeout (3 s), one retry with backoff, and token refresh
- [ ] Parser plus fixtures for es-MX and es-ES responses, including NoMatch, Omission and Insertion
- [ ] Decision pipeline plus star mapping plus table-driven tests
- [ ] "Say it" activity UI and the star animation (#11, #13)
- [ ] Offline mode and quota handling
- [ ] Dev shortcut: an **F0** key through `--dart-define-from-file` until #18 is deployed (F0 can't create charges). **Never put an S0 key in an APK**

## Acceptance criteria
- [ ] On the #19 calibration set, stars agree with parent labels within the target set there
- [ ] Median round trip under 1.5 s on home Wi-Fi; the offline fallback works in airplane mode
- [ ] No audio persisted with default settings
