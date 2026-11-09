# Can the same stack teach other languages? German as the test case

Date: 2026-11-09. This is a component-by-component check of whether the planned speech and content stack carries over to German, and what has to change to make the app multi-language. Items marked *(verify)* come from secondary sources or memory and should be checked when implementing.

## Verdict
**Yes.** Every component in the plan has a German equivalent. No new providers or terms questions arise, because Microsoft Azure Speech remains the only cloud provider (#24).

What does *not* carry over automatically:
- the **content** (written per language);
- the **word-matching rules** (Spanish phonetic key vs a German one);
- the **calibration** (thresholds per language, #19);
- a few **German-specific teaching points**: noun gender, umlauts and the "ch" sound.

So the plan should make **language a first-class dimension now**, while there is no code. Then add German as a second "language pack" after Spanish v1.

## Component by component
| Component (issue) | Spanish (planned) | German equivalent | Notes |
|---|---|---|---|
| On-device word check (#16) | Vosk `vosk-model-small-es-0.42` (~39 MB) | Vosk `vosk-model-small-de-0.15` (~45 MB, *verify*) | Grammar mode is a property of Vosk *small* models in general, so it should work the same; check it in a German spike. Apache-2.0 *(verify for the German model)*. [rhasspy mirror](https://huggingface.co/rhasspy/vosk-models/commit/87f72f6f0cde532e67aaf8db34bf201defd17842) |
| Pronunciation scoring (#17) | Azure PA `es-MX` / `es-ES` | Azure PA `de-DE` | German was among the first generally available Pronunciation Assessment languages. Expect the same Spanish-style limits (no prosody or phoneme labels); *verify* on the per-locale table. [Microsoft announcement](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/speech-pronunciation-assessment-is-generally-available/3740894), [language support](https://learn.microsoft.com/azure/ai-services/speech-service/language-support) |
| Lesson audio (#7) | Azure neural/HD es-MX voices | Azure neural/HD `de-DE` voices (e.g. Katja, Conrad, *verify*), plus `de-AT` and `de-CH` | The same SSML pipeline with `xml:lang="de-DE"`. ElevenLabs also supports German, with the same terms caveat (#24) |
| Offline voice (#20) | Android system TTS; optional Piper `es_MX-claude-high` | Android system TTS (German is standard); optional Piper `de_DE-thorsten` (low/medium/high, male) or `de_DE-kerstin` (low, female) | Thorsten-Voice is released as CC0 *(verify per model card)*. sherpa-onnx packages both as `vits-piper-de_DE-*`. They need the same lexicon/phoneme approach as Spanish, because sherpa-onnx 2.0 removed espeak-ng. [sherpa-onnx kerstin](https://k2-fsa.github.io/sherpa/onnx/tts/all/German/vits-piper-de_DE-kerstin-low.html), [Thorsten model card](https://huggingface.co/rhasspy/piper-voices/blob/main/de/de_DE/thorsten/medium/MODEL_CARD) |
| Kokoro (not used) | Ungraded Spanish voices | **No German voices** in Kokoro v1.0 *(verify)* | Another reason Kokoro stays out |
| iPad later (#23) | `SFSpeechRecognizer` es-MX | `SFSpeechRecognizer` de-DE, on-device *(verify)* | Same bridge, different locale |
| Fuzzy matching (#6, #16) | Spanish phonetic key (merges b/v, ll/y, c/s/z, silent h…) | **Kölner Phonetik** (Cologne phonetics; Postel 1969), designed for German | Many open-source implementations; Apache Solr includes it. Needs a small Dart port with the same shared test table. [Solr phonetic matching](https://solr.apache.org/guide/phonetic-matching.html), [overview](https://wiki.riteme.site/wiki/Cologne_phonetics) |
| Text normalisation (#16) | Accents, ¿¡, articles el/la/los/las/un/una | Umlauts and ß (`ä/ae`, `ß/ss`), noun capitalisation, articles der/die/das/den/dem/des/ein/eine/einen…, number words such as *einundzwanzig* | Per-language rules |
| Images, gestures, scenes (#8) | Fluent Emoji + composed scenes | **Same assets** | Concepts (dog, red, jump) are shared across languages; only culture-specific items differ (taco vs Brezel) |
| Lesson engine, SRS, rewards, parent area (#11–#14) | — | **Language-neutral** | Only the data model needs a language/course key |
| Teaching method ([`learning-methodology.md`](../learning-methodology.md)) | — | **Language-neutral** | The research is about learning in general. Add German notes (below) |
| Calibration (#19) | Thresholds for es | **Separate thresholds for de** | A recognizer's confidence and Azure scores aren't comparable across languages |

## German-specific teaching notes
- **Difficulty.** The US Foreign Service Institute rates German Category II, about 36 weeks or 900 class hours for adults. Older listings give 30 weeks or 750 hours. Spanish is Category I, about 24–30 weeks or 600–750 hours. All secondary sources; *verify* on state.gov.
  - Expect somewhat slower progress, mostly in grammar (gender, case). The many Germanic cognates help vocabulary early: Hand, Finger, Arm, Ball, Banane, Maus, Haus, Apfel, Fisch. This is inference, not a measured result for children.
- **Noun gender (der/die/das) is the big new thing.**
  - Teach every noun with its article as one chunk ("der Hund", never "Hund"). This is already a rule for Spanish.
  - Input-focused "processing instruction", where learners must notice the article to understand, beat colour-coding for gender assignment in adult learners of German ([Henry et al., *Language Teaching Research*, 2022](https://utexas.academia.edu/NickHenry/Papers); *verify the citation*).
  - Colour-coding still showed a delayed benefit at almost no cost (Arzt & Kost 2016, adults; [scite record](https://scite.ai/authors/jessica-arzt-zxdy6Q)).
  - I found **no study with children** learning German gender.
  - Design consequence: always show the noun with its article; optionally use a consistent subtle colour cue per gender on picture frames; for ages 8–10, add listening tasks where the article matters.
- **Cases** (den/dem): no explanations. Fixed chunks only ("Ich habe einen Hund", "Ich möchte einen Apfel"), unpacked later as children grow.
- **Pronunciation focus:** ü, ö, ä, ich/ach "ch", the German r, final devoicing. These become per-language `hard_sounds` tags.
- **Variety:** Standard German (`de-DE`) by default; Austrian or Swiss voices are available from Azure if the family prefers them.
- **Young-learner frameworks:** the same CEFR Pre-A1/A1 young-learner descriptors apply. Goethe-Institut's young-learner exams can serve as a cross-check for word lists *(not reviewed here)*.

## What changes in the plan
- **New ADR-002** ([`docs/adr/0002-language-packs.md`](../adr/0002-language-packs.md)): language packs and a shared concept bank.
- **New issue #26:** language-pack architecture, built in Phase 2 so nothing is Spanish-only.
- **New issue #27:** German course, Phase 7, after Spanish v1.
- **Small updates** to #6, #7, #9 and #16 so they are language-aware.

## Cost impact
- Running cost stays near $0, but German scoring shares the Azure F0 quota of 5 audio hours/month.
- Scoring uses about 1.7 hours per child per language, so 2 children doing 2 languages (about 6.8 hours) would exceed F0. Paid S0 is about $1 per audio hour *(verify)*.
- One-off German lesson audio is $0 on F0.
- APK size grows by about 75 MB per bundled language (Vosk model plus audio), so ship only the languages the family uses (#26).
