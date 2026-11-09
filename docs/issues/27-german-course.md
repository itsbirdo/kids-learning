---
planned_number: 27
title: "German course: content, voices, word check and calibration (second language pack)"
type: Feature
labels: [phase-7-german, "area: content", "area: speech"]
parent: 1
---

**Phase 7 (after Spanish v1, #22) · Size L · Depends on: #26 (language packs), and the Spanish pipeline proven end to end (#5–#19)**
Research: [`docs/research/2026-11-09-multilanguage-german.md`](../research/2026-11-09-multilanguage-german.md) · Teaching rules: [`docs/learning-methodology.md`](../learning-methodology.md)

## Goal
Add German as a second course, reusing the engine, concept bank, images, gestures and teaching method. Only the German-specific parts are new.

## What's reused vs new
| Reused unchanged | New for German |
|---|---|
| Lesson engine, spaced repetition, rewards, parent area, teaching rules (R1–R22) | `content/de/` units, dialogues, chunks, stories, parent cards |
| Concept bank: images, gestures, scenes, unit themes | German lesson voice(s) and audio pass (#7) |
| Speech pipeline: recorder, Vosk bridge, Azure client, gateway | Vosk `vosk-model-small-de-0.15` (~45 MB, *verify*) and grammar build |
| Calibration *procedure* (#19) | German calibration run and `scoring_config.json` |
| | `KoelnerPhonetik` strategy (Kölner Phonetik; Postel 1969) and German normaliser (umlauts/ß, noun capitals, articles, number words) |

## Language pack (`content/de/language.yaml`)
- **Variety:** Standard German, `de-DE`. Austrian or Swiss voices are possible if preferred.
- **TTS:** Azure `de-DE` neural/HD voices. Audition Katja, Conrad and others in a short #4-style listening test. ElevenLabs only if #24 clears it.
- **Scoring:** Azure Pronunciation Assessment `de-DE`. Expect the same limits as Spanish (no prosody or phoneme labels); *verify* the per-locale feature table.
- **Recognizer:** Vosk small German model in grammar mode. **Spike first:** repeat the #4 Vosk test with 20 German words and the kids. Go/no-go thresholds as for Spanish.
- **Offline voice (optional):** Piper `de_DE-thorsten` (CC0, *verify*) or `de_DE-kerstin` via sherpa-onnx, with a build-time lexicon (#20).
- **`hard_sounds`:** `ü`, `ö`, `ä`, `ch-ich`, `ch-ach`, `r`, `final-devoicing`.

## German-specific teaching rules (in addition to R1–R22)
1. **Every noun is taught with its article as one chunk** ("der Hund", "die Katze", "das Haus"), in audio, captions and parent cards. Never a bare noun.
2. **Optional gender colour cue:** a consistent, subtle frame colour per gender on noun pictures (e.g. der = blue, die = red, das = green). It costs nothing and showed a delayed benefit for adult beginners (Arzt & Kost 2016). Make it a parent setting, default on. No children's studies exist.
3. **For ages 8–10: tasks where the article carries the meaning**, so it must be noticed. Example: "Zeig mir *die* Maus" vs "*den* Ball" in a scene. Input-focused processing instruction beat colour-coding in adult German learners (Henry et al. 2022, *verify*).
4. **No case explanations.** Accusative and dative appear only inside fixed chunks ("Ich habe einen Hund", "Ich möchte einen Apfel, bitte").
5. **Cognates first:** Hand, Finger, Arm, Ball, Banane, Maus, Haus, Apfel, Fisch, Hallo.
6. **Pronunciation:** model clips include slow versions for ü/ö/ch. Feedback tips come from `hard_sounds`, as in #17.
7. **Expect slower grammar progress than Spanish.** The Foreign Service Institute rates German Category II (about 900 adult class hours vs 600–750 for Spanish; *verify*). Keep the vocabulary and dialogue targets, and lower expectations for free production.

## Units
The same 12 themes, from the concept bank. Example core dialogues:

| # | Theme | Core dialogue (gist) |
|---|---|---|
| 1 | Hallo! | "Hallo! Wie heißt du?" / "Ich heiße … Und du?" / "Wie geht's?" / "Gut, danke!" |
| 2 | Zahlen | "Wie alt bist du?" / "Ich bin sieben. Und du?" |
| 3 | Farben | "Welche Farbe ist das?" / "Das ist rot." |
| 4 | Tiere | "Magst du Hunde?" / "Ja, ich mag Hunde!" |
| 6 | Essen | "Was möchtest du?" / "Ich möchte einen Apfel, bitte." / "Bitte schön!" / "Danke!" |
| 7 | Körper | "Simon sagt: Zeig auf deine Nase!" |
| 10 | Schule | "Wo ist mein Bleistift?" / "Im Rucksack." |

## Tasks
- [ ] German Vosk spike with the kids (repeat the #4 protocol); go/no-go recorded
- [ ] `KoelnerPhonetik` and German normaliser strategies, with shared Python/Dart tests (#26)
- [ ] `content/de/language.yaml`, plus the voice audition and choice
- [ ] Units 1–3 in German: written, reviewed by a German speaker, validated, voiced and approved (#5–#7 process). Then the rest
- [ ] German calibration run (#19) and `scoring_config.json`
- [ ] Gender colour cue setting and the article-noticing activity (ages 8–10)
- [ ] Build with `PACKS=es,de`; playtest with both courses on one child and on two children

## Acceptance criteria
- [ ] A child can switch between Spanish and German courses, each with separate progress
- [ ] German Units 1–3 meet the same acceptance criteria as Spanish in #5, #7, #11 and #16
- [ ] German calibration done; stars agree with the parent on at least 80% of items (#19 spot check)
- [ ] No engine code changes were needed beyond German strategy classes (confirms #26)
