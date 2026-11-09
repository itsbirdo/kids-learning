# ADR-002: Language packs and a shared concept bank (Spanish first, German next)

- **Status:** Proposed (2026-11-09). Implemented by issue #26; German course in #27.
- **Research:** [`docs/research/2026-11-09-multilanguage-german.md`](../research/2026-11-09-multilanguage-german.md)

## Context
- The owner would like German too, or at least an app that can add languages later.
- Every planned component has a German equivalent:
  - Vosk small German model
  - Azure Pronunciation Assessment `de-DE`
  - Azure German voices
  - Android system TTS
  - Piper Thorsten/Kerstin
  - Kölner Phonetik for fuzzy matching
- The lesson engine, spaced repetition, rewards, parent area and teaching method are language-neutral.
- Retrofitting a language dimension after Spanish ships would touch the data model, content format, bundle, speech bridge and calibration. Building it in now costs little.

## Decision
1. **Language packs.** Everything language-specific lives in a pack, `content/<lang>/`:
   - `language.yaml`: locale codes for TTS voice, Azure scoring, Vosk model, system TTS and iOS recognizer; phonetic-key strategy; normalisation rules; article list; number-to-words; writing conventions; `hard_sounds` vocabulary; regional variants.
   - units, dialogues, chunks, stories, feedback and parent cards.
   - its own audio manifest, Vosk grammar file and `scoring_config.json`.
2. **Shared concept bank.** `content/concepts/` holds language-neutral concepts: `dog`, `red`, `jump` with image, gesture, category and English gloss. Pack items reference concepts (`es: el perro → concept: dog`, `de: der Hund → concept: dog`). Pictures, gestures, scenes and unit themes are reused. Packs may add culture-specific concepts (taco, Brezel).
3. **Courses in the app.** A child can take one or more *courses* (target languages). Progress, cards, attempts, stickers and calibration are keyed by `(child, course)`. The interface and parent area stay in English.
4. **Strategies, not if-statements.** Code is selected per pack, behind interfaces:
   - phonetic key (`SpanishKey`, `KoelnerPhonetik`)
   - text normaliser
   - number formatter
   - Vosk model
   - scorer locale
   - voices

   Adding a language means adding a pack plus, if needed, one strategy class with tests.
5. **Build selection.** The APK bundles only the packs the family uses (`--dart-define=PACKS=es` or `es,de`). Each pack adds about 75 MB (Vosk model plus audio). Downloadable packs can come later.
6. **Order.** Spanish v1 ships first with the multi-language architecture in place but one pack. German follows as Phase 7 (#27).

## Consequences
- **Content format (#6):** schema, validator and `kl build` work per pack, and validate concept references.
- **Data model (#9):** gains a `course` key. One-time cost, done before any progress data exists.
- **Speech stack (#16, #17):** takes its model, locale and phonetic key from the active pack. Calibration (#19) is per pack.
- **Audio pipeline (#7):** reads its voice and locale from `language.yaml`.
- **Rejected alternatives:**
  - a separate app per language: duplicated engine and progress silos;
  - hard-coding Spanish now and refactoring later: costly migration of progress data.
