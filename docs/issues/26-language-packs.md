---
planned_number: 26
title: "Multi-language architecture: language packs, shared concept bank, per-child courses"
type: Feature
labels: [phase-2-core-app, "area: app", "area: content"]
parent: 1
---

**Phase 2 · Size M · Depends on: #3, #6, #9 · Blocks: #27 (German) · Build it before any progress data exists**
Decision record: [`docs/adr/0002-language-packs.md`](../adr/0002-language-packs.md) · Research: [`docs/research/2026-11-09-multilanguage-german.md`](../research/2026-11-09-multilanguage-german.md)

## Goal
Spanish ships first, but nothing in the app, content tools or speech stack is Spanish-only. Adding German (#27) or another language means adding a **language pack** plus, at most, one small strategy class. No engine changes.

## Why now
Every component has a German equivalent:
- Vosk small German model
- Azure Pronunciation Assessment `de-DE`
- Azure German voices
- Android system TTS
- Piper Thorsten/Kerstin
- Kölner Phonetik

The engine, spaced repetition, rewards, parent area and teaching method are language-neutral. Adding a `course` key before any progress data exists is cheap; migrating it in later is not.

## Spec
### 1. Content layout (#6)
```
content/
  concepts/              shared, language-neutral: id, image, gesture, category, en gloss
    concepts.yaml        e.g. { id: dog, image: fluent/dog, gesture: "hands like paws", category: animal, en: "dog" }
  es/
    language.yaml        the pack definition (below)
    units/ global/ ...   items reference concepts: { id: perro, concept: dog, es: "el perro.", say: [...] }
  de/
    language.yaml
    units/ global/ ...   { id: hund, concept: dog, de: "der Hund.", say: ["Hund", "der Hund"], gender: m }
  local/family.yaml      (gitignored) names, nicknames
```
- Images, gestures, scenes and unit themes come from the concept bank and are reused across packs.
- Packs may add culture-specific concepts (taco, Brezel) in their own `concepts.yaml`.

### 2. `language.yaml` (one per pack)
```yaml
id: es
name: { en: "Spanish", native: "Español" }
variety: es-MX                    # chosen in #5
tts: { provider: azure, voice: es-MX-DaliaNeural, ssml_lang: es-MX, slow_rate: "-15%" }
scoring: { azure_locale: es-MX, calibrated: false }   # set by #19
recognizer: { vosk_model: vosk-model-small-es-0.42, ios_locale: es-MX }
system_tts_locale: es-MX
phonetic_key: spanish             # spanish | koelner | … (strategy class)
normaliser: spanish               # accents, ¿¡, articles
articles: [el, la, los, las, un, una, unos, unas]
number_words: spanish
conventions: [inverted_punctuation, article_on_nouns, numbers_as_words]
hard_sounds: [rr, j, ñ, "ll/y", vowels]
regional_variants: { es-ES: { jugo: zumo, playera: camiseta } }
```

### 3. Build and bundle
- **`kl build --pack es`** (or `--pack all`) writes `app/assets/content/<lang>/`: `content.json`, `audio_manifest.json`, `grammar.json`, `scoring_config.json`. Concepts and images go to `app/assets/content/shared/`.
- **Choosing packs:** the APK bundles only the packs the family uses, chosen with `--dart-define=PACKS=es` (later `es,de`) and Gradle asset filtering. Each pack adds about 75 MB (Vosk model ~40–45 MB plus audio ~30 MB).
- **Vosk models** are stored per pack and unpacked on first use of that course.

### 4. App (#9, #11–#14)
- **Courses:** a child profile has one or more courses (`es`, `de`). The home screen shows a course switcher (flags or mascot outfits) when there is more than one. Each course has its own unit map and sticker book.
- **Data model:** `cards`, `attempts`, `sessions`, `stickers` and `usage` gain a `course` column in the first schema version.
- **Parent area:** courses per child; per-course progress and calibration.
- **What stays English:** the UI and parent area. All target-language audio comes from the active pack.
- **Session length is per child,** not per course. A child doing two courses alternates days, or splits the session; parent setting, default alternate.

### 5. Speech and text strategies (#16, #17, #19, #20)
- **Interfaces in `domain/`,** chosen by the active pack:
  - `PhoneticKey`: `SpanishKey`, `KoelnerPhonetik`
  - `TextNormaliser`
  - `NumberWords`
  - `ArticleRules`

  Each comes with shared table tests used by both Python (`kl`) and Dart.
- **Per-pack resources:** `WordRecognizer` loads the pack's Vosk model; `AzureScorer` uses `scoring.azure_locale`; `SystemTts` uses `system_tts_locale`.
- **Calibration (#19)** writes a separate `scoring_config.json` per pack. Thresholds are not shared across languages.

### 6. Gateway (#18)
- `/v1/tts` accepts `lang` and only allows voices listed in an env-var voice list per pack.
- Usage counters are tracked per course.

## Tasks
- [ ] Concept bank format and migration of the Spanish unit format to reference concepts (#6)
- [ ] `language.yaml` schema plus validator; `kl build --pack`
- [ ] Strategy interfaces plus `SpanishKey`; shared Python/Dart test tables
- [ ] `course` key in the first drift schema; course switcher UI; per-course unit map and sticker book
- [ ] Pack selection at build time (dart-define plus Gradle asset filtering) and per-pack Vosk unpacking
- [ ] A **fake "test" pack** (two units, TTS-generated audio, English-as-target is fine) in CI. It proves nothing assumes Spanish

## Acceptance criteria
- [ ] A grep for Spanish locale codes, `ñ`, `¿` or Spanish articles outside `content/es/` and the `SpanishKey` / `SpanishNormaliser` classes finds nothing (CI check)
- [ ] The app builds and runs with the test pack alone, and with `es` plus the test pack (two courses on one child)
- [ ] Adding a pack needs no engine code changes beyond optional strategy classes (documented in `docs/adding-a-language.md`)
