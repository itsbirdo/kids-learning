---
planned_number: 6
title: "Content schema, validation and build tooling (`kl` CLI)"
type: Feature
labels: [phase-1-content, "area: content", "area: infra"]
parent: 1
---

**Phase 1 · Size M · Depends on: #3 · Blocks: #7, #8, #9, #16**

## Goal
Lessons live as YAML in `content/`. They are validated in CI and compiled into one bundle the app loads. YAML is the single source of truth: the app never hard-codes lesson data.

## Schema (example)
```yaml
# content/units/04-animales.yaml
id: u04
order: 4
title: { es: "Animales", en: "Animals" }
can_do: { en: "I can name animals and say what I like." }
parent_note: "Point at animals in a picture book and ask ¿Qué es?"
reviewed_by: "…"
reviewed_on: 2026-11-20
items:
  - id: perro
    type: noun            # noun | verb | adjective | number | expression
    es: "el perro."       # what the voice says (TTS text)
    say: ["perro", "el perro"]   # accepted answers for the speech check
    en: "dog"
    gender: m
    image: fluent/dog
    gesture: "hands like paws"
    distractors: [pero, pelo, pez]
    hard_sounds: [rr]
    variants: {}          # e.g. { es-ES: { es: "…" } }
phrases:
  - id: me_gusta_el_perro
    es: "Me gusta el perro."
    en: "I like the dog."
    items: [perro]
stories:
  - id: u04_story
    lines:
      - { id: l1, es: "Mira, un perro.", image: scene/park_dog }
    questions:
      - { id: q1, prompt_es: "¿Dónde está el perro?", options: [fluent/dog, fluent/cat, fluent/fish], answer: fluent/dog }
tpr:
  - { id: toca_el_perro, es: "Toca el perro.", target: perro }
scenarios: []             # conversation role-plays for #21 (optional)
```
- `content/global/` holds `feedback.yaml`, `prompts.yaml` (EN instructions and ES classroom prompts) and `routines.yaml`.
- `content/local/family.yaml` holds kids' names and nicknames. It is **gitignored** and read only at build time (#24).
- `content/schema/*.json` holds JSON Schema for every file type. Document it in `docs/content-format.md`.

## Compiled bundle (`app/assets/content/`)
| File | Contents |
|---|---|
| `content.json` | Units, items, phrases, stories, TPR, prompts; `content_version` (hash) |
| `audio_manifest.json` | Clip id → file, duration, loudness, approval (filled by #7) |
| `images_manifest.json` | Image id → file, license (filled by #8) |
| `grammar.json` | Item id → Vosk grammar list `[say…, distractors…, "[unk]"]`, or `azure_only` (#16) |
| `scoring_config.json` | Thresholds per age band (filled by #19) |

IDs are stable forever: progress in the app is keyed by them (#9). Renaming an ID needs an explicit migration entry.

## CLI (`uv run kl …`)
**`kl validate`** checks, in order:
1. The JSON Schema for every file.
2. Unique IDs.
3. Every image and clip reference resolves (clips only after #7 has run).
4. **Speech-check checks:**
   - every `say` token is in the Vosk model vocabulary;
   - distractors exist and differ from the target.
   - Out-of-vocabulary items are marked `azure_only` and listed as warnings. Find the model's word list file inside its `graph/` folder *(verify the file name)*.
5. Text conventions: ¿¡ punctuation, articles on nouns, numbers written as words, a trailing period on single words.
6. Sanity limits: new items per unit, phrase length for ages 6–8.
7. Optional: a Spanish spell check (hunspell `es`).

**Other commands**
| Command | What it does |
|---|---|
| `kl suggest-distractors [--unit u04]` | Ranks sound-alikes across the whole vocabulary using a Spanish phonetic key (merges b/v, ll/y, c/s/z, silent h, qu/k, g/j, r/rr) plus Levenshtein distance, and adds known confusions. Writes suggestions for the author to accept |
| `kl build` | Compiles the bundle deterministically (stable ordering) and stamps `content_version` |
| `kl stats` | Items per unit, total TTS characters (for cost), audio and image coverage |
| `kl lexicon` | *(Phase 4, optional)* espeak-ng IPA for every word, used by Piper on the device (#20) |

## Tasks
- [ ] JSON Schemas and `docs/content-format.md`
- [ ] Loader and validator, with pytest fixtures for each rule
- [ ] Spanish phonetic key and the distractor suggester. Also used by the matcher in #16; port it to Dart with the same tests
- [ ] Vosk vocabulary check (download the model once into a cache directory)
- [ ] `kl build` and `kl stats`
- [ ] CI job runs `kl validate` and checks that `kl build` output is committed and up to date

## Acceptance criteria
- [ ] The Unit 1 sample passes; deliberately broken fixtures fail with clear messages (file, line, rule)
- [ ] `kl build` produces a byte-identical bundle on repeated runs
- [ ] The phonetic key gives the same results in Python and Dart (shared test table)
