---
planned_number: 5
title: "Curriculum and lesson content: 12 units for ages 6–10"
type: Feature
labels: [phase-1-content, "area: content"]
parent: 1
---

**Phase 1 · Size L (ongoing; Units 1–3 first) · Depends on: #4 (Spanish variety) · Blocks: #7, #8, #11, #21 scenarios**

## Goal
Write the learning content. This is the biggest human task in the project. Units 1–3 unblock the app; the rest follow while Phase 2 is built.

## Targets
Year-end targets, after about 180 sessions of 12 minutes (roughly 35 hours). These are design estimates; tune them.
- **ACTFL Novice Mid / CEFR Pre-A1**, with listening near A1.
- Recognise about **250–300 words** when spoken slowly with pictures.
- Say about **120–180 words** plus about **40 memorised phrases**.
- Answer questions about name, age, feelings and likes.
- Follow one-step instructions.
- Ages 8–10 can also recognise familiar written words next to pictures.

## Spanish variety
- Pick **one** variety. Default: Latin American / Mexican (`es-MX`).
- Store regional alternatives in the data (`jugo/zumo`, `playera/camiseta`, `chamarra/chaqueta`, `papa/patata`); the app shows only the chosen one.
- The choice drives the voice (#7), the scoring locale (#17, confirmed by calibration in #19) and the vocabulary.

## Units
| # | Unit (≈ items) | Example vocabulary | Can-do goal |
|---|---|---|---|
| 1 | ¡Hola! + classroom words (20) | hola, adiós, me llamo, ¿cómo estás?, bien, gracias, por favor; escucha, mira, repite, toca | I can greet someone, say my name and follow the app's commands |
| 2 | Números 0–10, later 11–20 (21) | uno…veinte, ¿cuántos?, tengo seis años | I can count objects and say my age |
| 3 | Colores (11) | rojo, azul, amarillo, verde, morado, rosa, café | I can name the colour of things |
| 4 | Animales (20) | perro, gato, pez, pájaro, vaca, cerdo, león, mono, oso, rana | I can name animals and say "me gusta el…" |
| 5 | La familia (12) | mamá, papá, hermano/a, abuelo/a, bebé, tío/a | I can introduce my family from a photo |
| 6 | Comida (20) | manzana, plátano, pan, leche, agua, jugo, huevo, queso, helado, taco | I can ask for food politely and say what I like or don't like |
| 7 | El cuerpo (14) | cabeza, ojos, nariz, boca, mano, pie, rodillas, hombros | I can point to and name body parts ("Toca tu nariz") |
| 8 | Acciones (15) | salta, corre, baila, canta, come, duerme, dibuja, siéntate | I can follow action commands and say what I like doing |
| 9 | La ropa + colours (12) | camisa, pantalones, vestido, zapatos, gorra, chamarra | I can describe what I'm wearing ("una camisa roja") |
| 10 | La escuela (14) | libro, lápiz, mochila, mesa, silla, maestra, ¿dónde está?, en/debajo | I can name school things and ask where something is |
| 11 | Tiempo + días (≈ 20; months recognition only) | hace sol, llueve, hace frío; lunes…domingo; hoy | I can say today's day and the weather |
| 12 | Sentimientos + review story (10) | feliz, triste, enojado, cansado, tengo hambre/sed | I can say how I feel and understand a short picture story |

## What each unit contains
The format is defined in #6.
- **Vocabulary items**, each with:
  - the article (`el perro`) and gender
  - an English gloss and an image reference (#8)
  - a gesture or TPR hint
  - 2–4 sound-alike **distractors** for the speech check (suggested by the tools in #6, approved by the author)
  - `hard_sounds` tags: `rr`, `j`, `ñ`, `ll/y`, vowels
- **3–8 key phrases** ("me llamo…", "tengo seis años", "me gusta el…"), linked to the items they use.
- **One picture story**, 3–6 lines, with 2–3 tap-the-picture comprehension questions.
- **TPR commands** that reuse the Unit 1 classroom words (escucha, mira, repite, toca).
- **A chant or song (optional).** Use original lyrics or public-domain traditional songs, e.g. "Cabeza, hombros, rodillas y pies". Check public-domain status. A parent records it, or it's a TTS chant.
- **A scripted dialogue** for #21 (optional, later): a short branching role-play (6–12 nodes) with expected answers, hints and pre-generated character lines.
- **A can-do statement**, plus a parent note with offline practice ideas.

## Global content (`content/global/`)
- **Feedback phrases**, varied: "¡Muy bien!", "¡Excelente!", "¡Casi! Otra vez", "¡Lo lograste!". Never negative.
- **Instructions in English**, used for scaffolding at first and faded out.
- **Spanish classroom prompts.**
- **Routines:** hello and wrap-up.
- **Name lines** ("¡Muy bien, {name}!"). They are generated from `content/local/family.yaml`, which is gitignored (#24).

## Pedagogy rules
The validator in #6 enforces these where it can.
- **New words:** 4–6 per session (3–4 for age 6). Aim for 8+ encounters per word across at least 3 sessions.
- **Writing conventions:**
  - nouns carry their article
  - numbers are written as words
  - use ¿ and ¡
  - single words end with a period (helps TTS)
- **About 90% Spanish**, made clear with pictures and gestures (ACTFL guidance). English only for early instructions, then faded.
- **Cultural notes** where they fit naturally (foods, celebrations).
- **ACTFL Can-Do wording** is restricted to educational and non-profit use with attribution. Paraphrase it; don't copy it.

## Process
1. Draft each unit with AI help, following the schema.
2. A Spanish speaker reviews it (native speaker or teacher friend if possible). Record this as `reviewed_by` / `reviewed_on` in the unit file.
3. `kl validate` passes (#6). Generate audio (#7) and listen to every clip.

## Tasks
- [ ] Unit 1 (also defines the classroom words used everywhere)
- [ ] Units 2–3
- [ ] Global feedback, prompts and routines
- [ ] Units 4–8
- [ ] Units 9–12
- [ ] Scripted dialogues for Units 1, 2, 6, 8 and 9 (only if #21 goes ahead)

## Acceptance criteria
- [ ] Units 1–3 authored, reviewed and passing `kl validate`, so #7 and #11 are unblocked
- [ ] All 12 units done by the end of Phase 2
- [ ] Every item has an image reference, distractors and an approved audio clip (#7)
