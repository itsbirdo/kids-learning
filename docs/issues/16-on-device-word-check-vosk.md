---
planned_number: 16
title: "On-device word check: Vosk grammar mode + Spanish phonetic matcher"
type: Feature
labels: [phase-3-speaking, "area: speech", android]
parent: 1
---

**Phase 3 · Size L · Depends on: #4 (go/no-go), #6 (grammar.json), #15 · Blocks: #17, #19**

## Why
We need to know **"Did the child say the expected word?"**:
- **offline**
- **constrained** to the known answer and its sound-alikes
- **small** enough to bundle
- **independent of the tablet maker** (some strip the system recognizer, and Fire tablets have no Google services)

Azure can't answer this alone: single words often score about 100 even when wrong.

## Design
**Kotlin bridge** (local plugin `app/packages/vosk_bridge` or an in-app platform channel)
- **Library:** `com.alphacephei:vosk-android` (latest 0.3.x, *verify*). The stale `vosk_flutter` package is not used.
- **Model:** `vosk-model-small-es-0.42` (~39 MB, Apache-2.0), bundled in assets.
  - Unpack it to `filesDir` on first run (`StorageService.unpack`); load it once and keep it in memory.
  - **Only the small models support grammar mode.**
- **API:**
  ```
  recognize(pcm16: ByteArray, sampleRate: 16000, grammar: List<String>, maxAlternatives: 3)
    → { alternatives: [{text, confidence}], words: [{word, conf, start, end}] }
  ```
  - Implementation: `Recognizer(model, 16000f, grammarJson)`, `setMaxAlternatives(3)`, `setWords(true)`, `acceptWaveForm(...)`, `finalResult`.
  - Runs on a background thread.
- **Release builds:** Vosk uses JNA, so add R8/ProGuard keep rules *(verify)*.

**Grammar per check** (from `grammar.json`, built by #6)
- Target forms with and without the article, plus 2–4 distractors, plus `"[unk]"`. For example: `["perro","el perro","pero","pelo","pez","[unk]"]`.
- Phrases: the full phrase plus 1–2 near-miss phrases.
- **Out-of-vocabulary targets** can't go in a grammar. They are flagged `azure_only` at build time, and Vosk is skipped at runtime.

**Matcher** (pure Dart in `domain/`, shared with the iPad port, same test table as the Python key in #6)
1. **Normalise:** lowercase, strip accents and punctuation, digits → words, optional articles.
2. **Spanish phonetic key:** merge b/v, ll/y, c(e,i)/s/z, silent h, qu/k/c(a,o,u), g(e,i)/j and r/rr. Then normalised Levenshtein distance on the keys.
3. **Decision:**

| Result | Condition |
|---|---|
| `ACCEPT` | Top alternative is the target; or the target is in the top 3 with confidence ≥ τ₁; or key distance ≤ 0.25 (exact key match required for 1–2-syllable words) |
| `RETRY` | Top alternative is a distractor or `[unk]` |
| `NONE` | Empty result or silence |

- τ₁ and the distances come from `scoring_config.json` (#19).

**Forgiving UX**
- At most 3 tries per item; replay the model clip between tries.
- Bias toward acceptance: a false "try again" hurts a child more than a false "great". The research on kids' reading tutors found false rejections were the costly error.

## Fallbacks if the #4 spike says Vosk isn't good enough
- **Android on-device `SpeechRecognizer`:**
  - `createOnDeviceSpeechRecognizer` (API 31+)
  - `EXTRA_BIASING_STRINGS` (API 33+), `RESULTS_ALTERNATIVES` (API 34+)
  - needs a `<queries>` entry for `RecognitionService`
  - `ERROR_LANGUAGE_UNAVAILABLE` means the Spanish model needs downloading
- **Whisper-small** via sherpa-onnx or whisper.cpp, about 466 MB:
  - prompt it with the expected text and add a **length-deviation guard** (fall back to an unprompted transcript if the output length strays);
  - Whisper "smooths" mistakes, which risks false accepts.

## Tasks
- [ ] Kotlin bridge, model unpacking and threading, plus a Kotlin unit test with a fixture WAV (**parent or TTS voice, never a child's**)
- [ ] Dart `WordRecognizer` interface plus Vosk implementation plus fake
- [ ] Matcher plus table-driven tests (shared fixtures with #6 and #19)
- [ ] Decision logging into `attempts.recognizer_json` (no audio)
- [ ] R8 keep rules; check a release build

## Acceptance criteria
- [ ] Meets the #4 thresholds on the #19 calibration set (≥ 85% true-accept, ≥ 70% distractor rejection)
- [ ] Under 500 ms recognition for a 2 s clip on the kids' tablet
- [ ] Works in airplane mode
- [ ] APK size increase about 40 MB or less
