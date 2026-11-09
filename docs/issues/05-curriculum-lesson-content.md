---
planned_number: 5
title: "Curriculum and lesson content: 12 units for ages 6–10"
type: Feature
labels: [phase-1-content, "area: content"]
parent: 1
---

**Phase 1 · Size L (ongoing; Units 1–3 first) · Depends on: #4 (Spanish variety) · Blocks: #7, #8, #11, #21 dialogues**
Teaching rules: [`docs/learning-methodology.md`](../learning-methodology.md). Rule numbers (R1–R22) below refer to it.

## Goal
Write the learning content. This is the biggest human task in the project. Units 1–3 unblock the app; the rest follow while Phase 2 is built.

The content follows the research-based method:
- **Lots of understandable, repeated listening.**
- **Ready-made phrases ("chunks") in short dialogues,** learned by imitating a native-speaker voice. This is the useful core of the WWII "Army Method" and of the Foreign Service Institute's (FSI) "basic sentences".
- **Pictures plus gestures.**
- **Retrieval spaced over days** (handled by #11/#12).

## Targets (methodology §6)
Year-end targets, after about 180 sessions of 12 minutes (roughly 35–45 hours). These are design estimates; tune them.
- **ACTFL Novice Mid / CEFR Pre-A1**, with listening near A1.
- Recognise about **250–300 words** when spoken slowly with pictures.
- Say about **120–180 words** plus about **40 memorised chunks**.
- Perform all 12 **core dialogues**.
- Answer questions about name, age, feelings and likes; follow one-step instructions.
- Ages 8–10 can also recognise familiar written words next to pictures.
- **Not a goal:** accurate grammar in free speech. In low-input settings it doesn't develop yet (Muñoz 2006; Hartshorne, Tenenbaum & Pinker 2018 found the early-start advantage only with immersion).

## Spanish variety
- Pick **one** variety. Default: Latin American / Mexican (`es-MX`).
- Store regional alternatives in the data (`jugo/zumo`, `playera/camiseta`, `chamarra/chaqueta`, `papa/patata`); the app shows only the chosen one.
- The choice drives the voice (#7), the scoring locale (#17, confirmed by calibration in #19) and the vocabulary.

## Units
| # | Unit (≈ items) | Example vocabulary | Core dialogue (gist) | Can-do goal |
|---|---|---|---|---|
| 1 | ¡Hola! + classroom words (20) | hola, adiós, me llamo, ¿cómo estás?, bien, gracias, por favor; escucha, mira, repite, toca | "¡Hola! ¿Cómo te llamas?" / "Me llamo… ¿Y tú?" / "¿Cómo estás?" / "¡Bien, gracias!" | I can greet someone, say my name and follow the app's commands |
| 2 | Números 0–10, later 11–20 (21) | uno…veinte, ¿cuántos?, tengo seis años | "¿Cuántos años tienes?" / "Tengo siete años. ¿Y tú?" | I can count objects and say my age |
| 3 | Colores (11) | rojo, azul, amarillo, verde, morado, rosa, café | "¿De qué color es?" / "Es rojo." / "¿Te gusta el rojo?" | I can name the colour of things |
| 4 | Animales (20) | perro, gato, pez, pájaro, vaca, cerdo, león, mono, oso, rana (+ cognates: elefante, tigre, jirafa) | "¿Te gusta el perro?" / "Sí, me gusta el perro. ¿Y a ti?" | I can name animals and say "me gusta el…" |
| 5 | La familia (12) | mamá, papá, hermano/a, abuelo/a, bebé, tío/a | "¿Quién es?" / "Es mi abuela." | I can introduce my family from a photo |
| 6 | Comida (20) | manzana, plátano, pan, leche, agua, jugo, huevo, queso, helado, taco (+ cognates: chocolate, tomate) | At the taquería: "¿Qué quieres?" / "Quiero un taco, por favor." / "¡Aquí tienes!" / "¡Gracias!" | I can ask for food politely and say what I like or don't like |
| 7 | El cuerpo (14) | cabeza, ojos, nariz, boca, mano, pie, rodillas, hombros | "Simón dice: toca tu nariz." / "¿Dónde está tu boca?" | I can point to and name body parts |
| 8 | Acciones (15) | salta, corre, baila, canta, come, duerme, dibuja, siéntate | "¿Qué te gusta hacer?" / "Me gusta bailar. ¿Y a ti?" | I can follow action commands and say what I like doing |
| 9 | La ropa + colours (12) | camisa, pantalones, vestido, zapatos, gorra, chamarra | "¿Qué llevas hoy?" / "Llevo una camisa roja." | I can describe what I'm wearing |
| 10 | La escuela (14) | libro, lápiz, mochila, mesa, silla, maestra, ¿dónde está?, en/debajo | "¿Dónde está mi lápiz?" / "Está en la mochila." | I can name school things and ask where something is |
| 11 | Tiempo + días (≈ 20; months recognition only) | hace sol, llueve, hace frío; lunes…domingo; hoy | "¿Qué tiempo hace hoy?" / "Hace sol. Hoy es lunes." | I can say today's day and the weather |
| 12 | Sentimientos + review story (10) | feliz, triste, enojado, cansado, tengo hambre/sed | "¿Cómo estás?" / "Estoy cansado. Tengo hambre." / "¿Quieres pan?" | I can say how I feel, and understand and retell a short picture story |

**Mixing words across categories (R3).** Units 2 and 3 are single categories (numbers, colours). The composer (#11) mixes their new words with items from neighbouring units, using each item's `category` tag. Authors don't need to restructure units, but must tag categories.

## What each unit contains
The format is defined in #6.

**1. Core dialogue (R1, R15)**
- 4–8 lines, two voices (e.g. the mascot and a friend), in everyday language.
- Recorded by the lesson voice(s) (#7) at normal and slow speed.
- Every line is made from the unit's chunks and reuses chunks from earlier units.
- Long lines include a **backward build-up** split ("…la escuela" / "a la escuela" / "Voy a la escuela").
- Includes 1–2 **variation** slots: a picture changes one word.

**2. Chunks with slots (R1)**
- 3–8 reusable phrases ("Me llamo __", "Tengo __ años", "Me gusta __", "Quiero __, por favor", "¿Dónde está __?").
- Each lists the items that fit its slot.

**3. Vocabulary items, each with:**
- the article (`el perro`) and gender
- English gloss and image reference (#8)
- a **gesture the child copies** (R2): a short description for the animator, e.g. "hands like paws"
- `category` tag (animal, food, colour…) for mixing (R3)
- `cognate: true` where the Spanish is close to English (R4). Cognates go early in a unit as quick wins.
- 2–4 sound-alike **distractors** for the speech check (suggested by #6 tools, approved by the author)
- `hard_sounds` tags: `rr`, `j`, `ñ`, `ll/y`, vowels

**4. One picture story (R5)**
- 3–6 short, repetitive lines that recycle the unit's chunks.
- 2–3 tap-the-picture questions.
- Designed to be re-heard on at least 3 days.

**5. TPR commands**
- Reuse the Unit 1 classroom words (escucha, mira, repite, toca) plus the unit's action words.

**6. A chant or song (R6)**
- Original lyrics or a public-domain traditional song (e.g. "Cabeza, hombros, rodillas y pies"; check public-domain status).
- One fixed melody, reused every time.
- A parent records it, or it's a rhythmic TTS chant.

**7. Explicit tips (ages 8–10 only, R7)**
- 0–2 one-line English "notice the pattern" cards per unit (*el/la*, plural *-s*, *me gusta*).
- Shown only after the child has used the chunk.

**8. Parent card (R21)**
- The can-do goal.
- The chunk of the week (2–3 phrases for daily routines).
- The dialogue script for "Dialogue swap".
- A "Teach me" word list.
- 2–3 offline ideas.
- In plain English, with audio for every Spanish line.

**9. Optional branching role-play** for #21, built on the core dialogue.

## Global content (`content/global/`)
- **Feedback phrases,** varied and specific: "¡Muy bien!", "¡Excelente!", "¡Casi! Otra vez", "¡Lo lograste!". Plus **hint prompts** ("¿Cómo se dice…?"). Never negative.
- **Instructions in English,** used for scaffolding at first and faded out.
- **Spanish classroom prompts.**
- **Routines:** hello, warm-up and wrap-up.
- **Grown-up turn card templates** (#14).
- **Name lines** ("¡Muy bien, {name}!"), generated from `content/local/family.yaml`, which is gitignored (#24).

## Pedagogy rules (the validator in #6 enforces these where it can)
- **New items per session:** 3–4 for ages 6–7, 4–6 for ages 8–10. A multi-word chunk counts as about 2 (R13). The unit's authored order should introduce cognates and high-frequency items first.
- **Encounters:** aim for about 8–12 meaningful encounters per word in its first 2 weeks, across tap, TPR, story, dialogue and review. The story and dialogue must actually use the unit's words several times.
- **Order of skills:** listen and do before say (R8). Content must make every item usable in a tap or act activity before it appears in a speaking activity.
- **Writing conventions:**
  - nouns carry their article
  - numbers are written as words
  - use ¿ and ¡
  - single words end with a period (helps TTS)
- **About 90% Spanish,** made clear with pictures and gestures (ACTFL guidance). English only for early instructions, tips (ages 8–10) and parent cards.
- **Cultural notes** where they fit naturally (foods, celebrations).
- **ACTFL Can-Do wording** is restricted to educational and non-profit use with attribution. Paraphrase it; don't copy it.

## Process
1. Draft each unit with AI help, following the schema and the rules above.
2. A Spanish speaker reviews it (native speaker or teacher friend if possible), especially the dialogue's naturalness. Record this as `reviewed_by` / `reviewed_on` in the unit file.
3. `kl validate` passes (#6). Generate audio (#7) and listen to every clip.

## Tasks
- [ ] Unit 1 (also defines the classroom words and the first dialogue pattern)
- [ ] Units 2–3
- [ ] Global feedback, hint prompts, routines and grown-up turn templates
- [ ] Units 4–8
- [ ] Units 9–12
- [ ] Optional branching role-plays for Units 1, 2, 6, 8 and 9 (only if #21 goes ahead)

## Acceptance criteria
- [ ] Units 1–3 authored, reviewed and passing `kl validate`, so #7 and #11 are unblocked
- [ ] Every unit has a core dialogue, chunks with slots, a story, a parent card, and gestures and category tags on every item
- [ ] All 12 units done by the end of Phase 2
- [ ] Every item has an image reference, distractors and an approved audio clip (#7)
