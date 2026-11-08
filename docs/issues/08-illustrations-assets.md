---
planned_number: 8
title: "Illustrations and visual assets (Fluent Emoji base set, scenes, mascot)"
type: Feature
labels: [phase-1-content, "area: content"]
parent: 1
---

**Phase 1 · Size M · Depends on: #5, #6 · Blocks: #11, #13**

## Goal
Every vocabulary item, story line and scene has a consistent, child-friendly, properly licensed picture.

## Base set: Microsoft Fluent Emoji (MIT)
- Styles: 3D (PNG), Color and Flat (SVG), High Contrast. **Pick one style** for consistency; audition 3D vs Color with the kids.
- It covers animals, food (including taco and tamal), clothes, weather, faces and families with skin-tone variants.
- **Obligation:** include the MIT copyright notice and licence text on an Acknowledgements screen (#14).

| Alternative | Licence | Obligation |
|---|---|---|
| Twemoji (jdecked fork) | Graphics CC BY 4.0 | Credit with a link |
| Noto Emoji | Images Apache 2.0 | Include the licence |
| OpenMoji | CC BY-SA 4.0 | Credit line required; modified graphics must be shared under BY-SA |

## Gaps to fill
Emoji sets don't cover these well:
- **Action verbs** (salta, corre, dibuja, siéntate)
- **Body parts** such as hombros and rodillas
- **Prepositions** (en, debajo)
- **Story scenes** and the "¿Dónde está?" scenes

Options, in order of preference:
1. **Compose scenes in Flutter**: a background plus positioned emoji layers, defined in content (`scene/park_dog` = layout JSON). Cheap and consistent.
2. **Commissioned or hand-drawn art** in a matching style.
3. **AI-generated images** with one fixed style prompt and manual review of every image. Check the provider's terms in #24. Gemini image models fall under the same under-18 clause, so don't use them.

## Mascot
- One simple, **original** guide character (for example a friendly axolotl). It must not resemble any existing franchise character.
- States needed: idle, listening, happy, thinking, wave.
- A few frames or a Rive/Lottie animation is enough.

## Colour unit
- Colour swatches are drawn in code, not taken from emoji, so the colours are accurate.
- Add a parent setting note for colour-blind kids.

## Pipeline (`kl images`)
1. Pin the source repo by commit (download or submodule) and copy only referenced assets.
2. Resize and optimise: PNG 256/512 px through `oxipng`, or SVG through `svgo`.
3. Write `images_manifest.json` with `id → {file, source, licence, attribution}`.
4. `kl validate` fails on any reference that doesn't resolve and on any image with no licence recorded.
5. Generate the Acknowledgements data used by #14.

## Tasks
- [ ] Style audition and decision (record it in `docs/content-format.md`)
- [ ] `kl images` plus manifest and licence data
- [ ] Scene layout format and a Flutter scene renderer (shared with #11)
- [ ] Mascot design (original) and states
- [ ] Assets for Units 1–3, then the rest as #5 lands

## Acceptance criteria
- [ ] All Unit 1–3 references resolve; every image has a licence entry
- [ ] Total image size under 20 MB
- [ ] Acknowledgements data generated and shown in the parent area (#14)
