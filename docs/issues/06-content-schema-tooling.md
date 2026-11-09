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

**Multi-language (#26):** content is organised as language packs, `content/<lang>/` with a `language.yaml`, plus a shared concept bank, `content/concepts/` (image, gesture, category, English gloss). Pack items reference a concept. All validator rules and `kl build` run per pack (`--pack es`). Text-convention checks, articles and the phonetic key come from the pack's strategies (`spanish`, later `koelner` for German, #27). The example below shows the Spanish pack.

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
    category: animal      # for mixing new-word sets across categories (#11, methodology R3)
    cognate: false        # true for elefante, tigre… (introduced early as quick wins)
    image: fluent/dog
    gesture: "hands like paws"   # the child copies it (R2); brief for the animator
    distractors: [pero, pelo, pez]
    hard_sounds: [rr]
    variants: {}          # e.g. { es-ES: { es: "…" } }
chunks:                   # reusable phrases with a slot (R1)
  - id: me_gusta
    es: "Me gusta {slot}."
    en: "I like {slot}."
    slot_items: [perro, gato, pez]
phrases:
  - id: me_gusta_el_perro
    es: "Me gusta el perro."
    en: "I like the dog."
    items: [perro]
dialogue:                 # core dialogue, 4–8 lines, two voices (R1, R15)
  id: u04_dialogue
  roles: { a: mascot, b: friend }
  lines:
    - { id: d1, role: a, es: "¿Te gusta el perro?", chunks: [te_gusta] }
    - { id: d2, role: b, es: "Sí, me gusta el perro. ¿Y a ti?", chunks: [me_gusta],
        buildup: ["¿Y a ti?", "me gusta el perro", "Sí, me gusta el perro. ¿Y a ti?"],
        variation: { chunk: me_gusta, slot_items: [gato, pez] } }
tips:                     # ages 8–10 only, shown after use (R7)
  - { id: u04_tip_el_la, min_age: 8, en: "Notice: el perro, el gato — but la vaca.", after: [perro, vaca] }
parent_card:              # grown-up turn (R21, #14)
  chunk_of_week: [me_gusta, te_gusta]
  teach_me: [perro, gato, pez, vaca]
  ideas: ["Point at animals in a picture book and ask ¿Qué es?"]
stories:
  - id: u04_story
    lines:
      - { id: l1, es: "Mira, un perro.", image: scene/park_dog }
    questions:
      - { id: q1, prompt_es: "¿Dónde está el perro?", options: [fluent/dog, fluent/cat, fluent/fish], answer: fluent/dog }
tpr:
  - { id: toca_el_perro, es: "Toca el perro.", target: perro }
roleplays: []             # optional branching role-plays for #21, built on the core dialogue (format in #21)
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
7. **Teaching-rule checks** ([`docs/learning-methodology.md`](../learning-methodology.md)):
   - every item has `category` and `gesture`;
   - every unit has a core `dialogue` of 4–8 lines, a story, chunks and a `parent_card`;
   - every dialogue line's chunks exist;
   - lines over 4 words have a `buildup`;
   - each unit's story and dialogue together use at least half of the unit's items;
   - `tips` have `min_age` ≥ 8.
8. Branching role-play graphs (#21): every node reachable, every non-end node has a hint, every path reaches `success`, every line has audio.
9. Optional: a Spanish spell check (hunspell `es`).

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
