# Spanish kids app research: content, pedagogy and pre-generated audio

> Verification report produced on 2026-11-08 while planning this project. Some primary sites were unreachable from the research environment, so several facts come from search-engine extracts of official pages; confidence ratings reflect that. Re-check anything rated medium/low (M/L) before relying on it.

**How I checked.** Most direct page fetches were blocked in the research environment (elevenlabs.io, ai.google.dev, actfl.org, coe.int, arxiv.org, cambridgeenglish.org and depts.washington.edu). For those sites I relied on search-engine summaries of the pages. GitHub was reachable, so the ElevenLabs Python SDK, the `elevenlabs/skills` repo, the Gemini cookbook and the emoji repos are first-hand. The confidence ratings below take this into account.

## Verified facts

**ElevenLabs**
- **Models.**
  - `eleven_v4` is now the default flagship: 90+ languages, audio tags, no SSML.
  - `eleven_v4_turbo` is the real-time option (about 100 ms).
  - `eleven_flash_v2_5`: 32 languages, about 75 ms.
  - `eleven_multilingual_v2` (29 languages) and `eleven_v3` (70+) are now the previous generation.
  - The turbo_v2/v2_5 models have been replaced by Flash.
  - v4 launched about 28 Sep 2026.
  - Sources: https://github.com/elevenlabs/skills/blob/main/text-to-speech/SKILL.md and https://elevenlabs.io/docs/overview/models. **High** (the date is **med**).
- **`language_code`.** Takes a two-letter ISO 639-1 code (`"es"`) and forces the language and text normalisation. It is ignored by models that don't support it, and is **not supported on `eleven_multilingual_v2`**. The accent comes from the chosen voice, not from this code. Also available: `seed` (best-effort repeatability), `previous_text`/`next_text`, `apply_text_normalization` (auto/on/off), and up to 3 pronunciation dictionaries per request. Source: https://github.com/elevenlabs/elevenlabs-python/blob/main/src/elevenlabs/text_to_speech/raw_client.py. **High.**
- **Voice settings.**
  - **v4 accepts only `stability` and `similarity_boost`.** It has no `speed`, no `style` and no SSML; pacing comes from punctuation and tags.
  - `speed` (default 1.0) works on v2 and v3. The documented range is 0.7–1.2.
  - Recommended narration preset: stability 0.7, similarity 0.5.
  - Sources: https://github.com/elevenlabs/skills/blob/main/text-to-speech/references/voice-settings.md and https://elevenlabs.io/docs/overview/capabilities/text-to-speech/eleven-v4. **High/med.**
- **Output formats.** `mp3_22050_32`…`mp3_44100_192`, `opus_48000_32`–`192`, `pcm_8000`–`48000`, `wav_8000`–`48000`, plus μ-law and A-law. 44.1 kHz PCM/WAV and 192 kbps MP3 need higher plans. Source: the SDK's output-format type file. **High.**
- **Pronunciation.** Dictionaries are uploaded as PLS files. Alias rules work in any language. Phoneme rules (IPA or CMU) are limited by model and lean English. The v4 best-practices page says inline IPA between slashes works. Source: https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices. **Med.**
- **Picking a Spanish voice by accent.**
  - `GET /v1/shared-voices` filters by `language`, `accent`, `locale`, `gender`, `age`, `use_cases` and `min_notice_period_days`.
  - Each voice lists verified languages as `{language, accent, locale, preview_url}`.
  - Accent labels seen on third-party catalogues: mexican, peninsular, latin american, colombian.
  - **High** for the endpoint, **low** for the exact label strings.
- **Prices.** After the v4 price cut, the API costs **$0.08 per 1,000 characters** for v4, v3 and Multilingual v2, and **$0.04** for v4 Turbo and Flash.

  | Plan | Price / month | Credits / month |
  |---|---|---|
  | Free | $0 | 10k |
  | Starter | $6 | 30k |
  | Creator | $22 | 121k |
  | Pro | $99 | 600k |

  Flash uses 0.5 credits per character; Multilingual v2 uses 1. Sources: https://elevenlabs.io/pricing/api and https://www.eesel.ai/blog/eleven-v4-pricing. **Med** (I couldn't open the official page).
- **Licence.** The free plan is non-commercial and requires attribution. Paid plans allow commercial use, including audio made while subscribed after you cancel. The account holder must be 18+. Sources: https://elevenlabs.io/docs/help-center/legal/can-i-publish-the-content-i-generate-on-the-platform and https://elevenlabs.io/terms-of-use. **Med-high.**

**Gemini TTS**
- **Model names.** "Gemini 3.1 Flash TTS" is actually `gemini-3.1-flash-tts-preview`, a preview model from about April 2026 (one source says February). It is now marked **legacy**. The replacements are `gemini-3.8-flash-tts` and `gemini-3.8-flash-lite-tts`. Google Cloud lists 3.8 Flash TTS as generally available from 28 Oct 2026. Trackers give the earliest 3.1 shutdown as 17 Nov 2026; an official snapshot says no date is set. Sources: https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash-tts and https://ai.google.dev/gemini-api/docs/deprecations. **High** for the names, **med** for the dates.
- **How 3.8 is called.** Source: https://github.com/google-gemini/cookbook/blob/main/quickstarts/Get_started_TTS.ipynb. **High.**
  - It uses the Interactions API and needs `google-genai>=2.24.0`.
  - The `text` field is **spoken word for word**. Persona, pace and accent go in a separate `speech_metadata` `style` field.
  - Inline tags such as `<short pause>`, `<long pause>` and `<laugh>` are supported.
  - There are 30 prebuilt voices (Kore, Puck, Charon, Aoede, Enceladus…), plus a Voices API for designing or cloning voices.
  - A normal call returns a **WAV file, 24 kHz, mono, 16-bit**. Version 3.1 returned raw PCM with no header.
- **Limits.** 8,192 input tokens and 16,384 output tokens per request; Batch and Flex modes are supported. **Med.**
- **Spanish support.** Google Cloud's Gemini-TTS docs list es-MX and es-419. Spain and US Spanish (es-ES, es-US) appear only on third-party pages. Source: https://docs.cloud.google.com/text-to-speech/docs/gemini-tts. **Med-low.**
- **Pricing.** Audio is billed at 25 tokens per second. **Med** (secondary sources: https://www.eesel.ai/blog/gemini-3-8-flash-tts-pricing).

  | Model | Text in, per M tokens | Audio out, per M tokens | Notes |
  |---|---|---|---|
  | 3.8 Flash TTS | $0.50 | $9 | Batch/Flex about half; reported to double on 1 Jan 2027 |
  | 3.8 Flash-Lite TTS | $0.50 | $6 | Batch/Flex about half; reported to double on 1 Jan 2027 |
  | 3.1 preview | $1 | $20 | |

- **Watermark.** SynthID is applied to all Gemini TTS audio. It is inaudible and you can't turn it off. **Med.**
- **Age clause in the terms.** Gemini API users must be 18+. The terms also say the Services may not be used in an app "directed towards or … likely to be accessed by individuals under the age of 18". Several developers have asked on Google's forum whether **pre-generated, offline clips** are allowed, and none has had an official answer. Sources: https://ai.google.dev/gemini-api/terms and https://discuss.ai.google.dev/t/gemini-api-terms-pre-generated-tts-audio-in-an-app-whose-audience-includes-under-18s/196200. **High** that the clause exists; how it applies here is **unresolved**.

**Pedagogy**
- **ACTFL.** These are the 2017 Novice benchmarks:
  - Novice Low (talking with someone): "communicate on some very familiar topics using single words and phrases… practiced and memorized".
  - Novice Mid: "…a variety of words and phrases…".

  A **2026 revision** exists, aligned to the 2024 Proficiency Guidelines, but I couldn't read its wording. Use is restricted to educational and non-profit purposes, with attribution. Source: https://www.actfl.org/educator-resources/ncssfl-actfl-can-do-statements. **Med.**
- **CEFR Pre-A1 (Companion Volume 2020).** Descriptors include:
  - Understands short, very simple questions and statements "delivered slowly and clearly and accompanied by visuals or manual gestures".
  - Follows short instructions such as "Stop" or "Close the door".
  - "Can produce short phrases about themselves" (name, family…).

  There is also a Council of Europe collection of descriptors for ages 7–10: https://rm.coe.int/16808b1688. **Med-high.**
- **Pictures and gestures.** Eight-year-olds who learned with pictures or with gestures (20 minutes a day for 5 days) remembered L2 words better than listening-only learners **six months later**; pictures and gestures worked equally well. Source: Andrä et al. 2020, *Educational Psychology Review*, doi 10.1007/s10648-020-09527-z. **High.**
- **Songs.** Songs built receptive vocabulary in 5-year-olds, but production stayed limited for most children. Source: Coyle & Gómez Gracia 2014, *ELT Journal* 68(3). **Med-high.**
- **Stories.** 7–8-year-olds learned some words from hearing a story three times, and gained more when the words were explained. Source: Elley 1989, *Reading Research Quarterly* 24. **Med.**
- **Spacing and retrieval practice.**
  - Spacing sessions a week apart beat cramming by about 3× at 5 weeks (fifth graders, 8 words). Source: Sobel, Cepeda & Kapler 2011.
  - A Dutch classroom study found a spacing effect in 2012, but a multi-classroom follow-up in 2016 found no extra benefit, so effects in real classrooms are smaller (Goossens et al.).
  - Retrieval practice works for elementary-age children. Source: Karpicke et al. 2016, https://pmc.ncbi.nlm.nih.gov/articles/PMC4786565.
  - **High.**
- **Repetition.** A meta-analysis found a medium effect of repetition (r = .34); studies put the useful number of encounters anywhere from about 2 to 20+. Source: Uchihara, Webb & Yanagisawa 2019. **Med.**
- **New words per lesson.** The common rule of thumb is 8–12 productive items per 60-minute lesson (Gairns & Redman 1986). It comes from teaching experience, not experiments. **Med.**
- **Rewards and manipulative design.**
  - Expected, tangible rewards undermine children's own motivation; informational positive feedback increases it. Source: Deci, Koestner & Ryan 1999. **High.**
  - Only 20% of apps used by 3–5-year-olds had no manipulative design. Source: Radesky et al. 2022, *JAMA Network Open*, e2217641. **High.**
  - The UK ICO Children's Code (standard 5) flags reward loops, notifications and autoplay used to keep children engaged. Source: https://ico.org.uk/…/5-detrimental-use-of-data/. **High.**
- **Attention span.** Sustained attention improves steeply from ages 5–6 to 8–9. 5–7-year-olds get slower the longer a task runs. There is **no research-based "minutes per age" number**. **Med.**
- **Using Spanish vs English.** ACTFL recommends using the target language 90%+ of the time, made understandable with gestures and visuals. **High.**
- **Children's usability.** Nielsen Norman Group splits children into pre-readers (3–5), beginning readers (6–8) and more skilled readers (9–12). Pre-readers rely on audio and visuals, and audio instructions must actually play. Source: https://www.nngroup.com/articles/kids-cognition/. **Med.**

**Tools**
- ffmpeg's `loudnorm` filter is unreliable on clips under about 3 seconds and may silently switch to dynamic mode (https://trac.ffmpeg.org/ticket/6071). **Med-high.**
- `pyloudnorm` implements the BS.1770-4 loudness standard with 400 ms blocks. **High.**
- iOS plays Opus only inside a CAF container, and ffmpeg-made CAF files have had playback bugs. **Med.**

## Corrections to the research doc
1. **§3.3, ElevenLabs.** The prices are out of date: now $0.04 per 1,000 characters for Flash and $0.08 for v3/v4, not $0.05/$0.10. `eleven_v4` is the current model. **v4 cannot slow speech down**, so slow child-friendly clips need v2/v3 with `speed`, or slowing the audio afterwards.
2. **§3.3, Gemini.** The ID is `gemini-3.1-flash-tts-preview`. It is a legacy preview that may be retired soon, so use `gemini-3.8-flash-tts` or `-lite-tts` instead. The doc's $36.6 per million characters matches 3.1's price. At introductory prices, 3.8 works out to about $16 per million characters (Flash) or about $11 (Flash-Lite); these are my estimates. The 3.8 API speaks any instructions placed in the text aloud, so the doc's style-prompt approach won't work.
3. **§3.4 and §9 step 3 ("ElevenLabs or Gemini").** Gemini's terms bar apps aimed at under-18s, and it is unclear whether that covers clips generated offline. **Use ElevenLabs for the clips that ship**, unless Google confirms in writing. The ElevenLabs free plan requires attribution and is non-commercial; any publication needs a paid plan.
4. **§3.3, "Regional Spanish voices".** Accent is set by choosing a voice, not by the language code. Peninsular and Colombian voices also exist, and `language_code` doesn't work with Multilingual v2.

## Recommended curriculum outline
Choose **one Spanish variety**. For a US home, Mexican or Latin American is the usual choice. Store regional alternatives in the data, such as jugo/zumo, playera/camiseta, chamarra/chaqueta and papa/patata.

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
| 11 | Tiempo + días (≈20; months only to recognise) | hace sol, llueve, hace frío; lunes…domingo; hoy | I can say today's day and the weather |
| 12 | Sentimientos + review story (10) | feliz, triste, enojado, cansado, tengo hambre/sed | I can say how I feel, then understand a short illustrated story |

**Year-end target** (about 180 sessions of 12 minutes, roughly 35 hours): ACTFL **Novice Mid**, CEFR **Pre-A1**, with listening near A1.
- Recognise about 250–300 words when spoken slowly with pictures.
- Produce about 120–180 single words plus about 40 memorised phrases.
- Answer name, age, feelings and likes questions.
- Follow one-step instructions.
- Children aged 8–10 can also recognise familiar written words next to pictures.

These numbers are my design estimates and can be tuned.

## Recommended lesson/session design
**Session shape (10–15 min)**
1. **Hello routine, 1 min.** A short greeting song; the child taps a face to answer "¿Cómo estás?".
2. **Review, 3–4 min.** Items due for spaced review, using listen-and-tap with 2–4 pictures and TPR commands (the child acts out "Toca tu nariz").
3. **New words, 3–4 min.** Introduce **4–6 items** (3–4 for 6-year-olds). Each gets a picture, a gesture animation, audio at normal and slow speed, and a repeat step where the child records and plays back. Quiz each item again 2–3 items later.
4. **Use it, 2–3 min.** A 3–6-line picture story or a song or chant, then comprehension questions. Or a build activity such as "dress the character" or "¿Dónde está?" scenes.
5. **Speak, 1–2 min.** The child names a picture. The child's recording is played beside the model voice; any recogniser check should be forgiving and never fail the child.
6. **Wrap-up, 1 min.** Recap 3 words, then "¡Hasta mañana!". The session ends there with no autoplay.

**Spaced repetition**
- Use a Leitner system with 5 boxes. Intervals: same session, then 1, 3, 7, 14 and 30 days.
- A correct answer on the first try moves the item up one box. A miss sends it back to box 1, with a neutral "¡Otra vez!" and no penalty sound.
- Sessions are about 60% review and 40% new words. Pause new words if the review backlog grows too large.
- Aim for 8 or more encounters per word across at least 3 sessions.

**Rewards and gamification**
- Use completion stickers on a unit map and messages that tell the child what they learned ("You learned 5 animals!").
- Give occasional surprise rewards instead of rewards tied to performance.
- Avoid: lives or hearts, timers, streaks that can be lost, leaderboards, push notifications to the child, and autoplaying the next lesson.
- Progress and limits belong in a parent view.

**Pre-readers**
- Every prompt is spoken, with a large replay button; navigation uses icons only, with big tap targets.
- Spoken English gives the instructions at first. It is then faded out and replaced by Spanish classroom words taught in Unit 1 (escucha, toca, repite).
- Spanish text is an optional caption for ages 8 and up.
- Everything else is in Spanish, explained by pictures, in line with ACTFL's 90% guidance.

## Audio pipeline details
**Content.** Store lessons as YAML or JSON. Each clip has: `id`, `unit`, `type` (word, phrase, prompt, feedback, instruction_en, story_line), `text_es`, `variant_regional`, `speed` (normal or slow), `image`, `voice_role`.

**Writing conventions**
- Put the article on nouns: "el perro."
- End single words with a period.
- Write numbers out as words.
- Use ¿ and ¡.
- Set `apply_text_normalization: "off"` once the text is already normalised.
- Use `previous_text`/`next_text` for story lines.

**Cache key**
- `sha256` of canonical JSON containing: provider, model, voice_id, text normalised to Unicode NFC (so "niño" always hashes the same way), language_code, sorted settings, style prompt, pronunciation dictionary ID and version, output format, seed, and post-processing version.
- The manifest maps each clip ID to its hash, the approved take, duration and measured loudness.
- **Archive the approved master files.** Regenerating them isn't reliably the same: seeds are only best-effort, models get retired, and library voices can be withdrawn after their notice period.

**ElevenLabs request (recommended for audio that ships)**
- Endpoint: `POST /v1/text-to-speech/{voice_id}?output_format=wav_24000` (or `pcm_24000`).
- Body: `{model_id: "eleven_v4", language_code: "es", voice_settings: {stability: 0.7–0.8, similarity_boost: 0.5–0.75}, seed}`.
- **Slow versions:** either use `eleven_v3` or `eleven_multilingual_v2` with `speed: 0.8–0.85` (the voice may sound slightly different), or keep the v4 recording and slow it with ffmpeg `atempo=0.85`. Compare both by ear.
- **Choosing the voice:** filter shared voices with `language=es&accent=mexican` and a long `min_notice_period_days`, or design your own voice with Voice Design so you own it.

**Gemini request (only if the terms question is resolved)**
- `client.interactions.create(model="gemini-3.8-flash-tts", input=[{type:"text", text:"el perro.", annotations:[{type:"speech_metadata", style:"Warm, patient teacher speaking to a 6-year-old. Accent: Mexican Spanish (Mexico City). Pace: slow and clear."}]}], response_format={type:"audio"}, generation_config={speech_config:[{voice:"Kore"}]})`
- Run the whole set through the Batch API.

**Post-processing**
1. Trim silence: `silenceremove` (−50 dB), then `areverse`, `silenceremove` again, and `areverse` back.
2. Add consistent padding: about 60 ms before and 250 ms after.
3. Add a 10 ms fade-in.
4. Normalise loudness to **−16 LUFS, −1.5 dBTP**. Because `loudnorm` misbehaves on clips under 3 seconds, measure each clip with `pyloudnorm` and apply a fixed `volume` plus `alimiter`.
5. Automatic QA: transcribe each clip with Whisper and compare to the text, and check characters per second, to catch wrong language or garbled clips.
6. A parent then listens and approves each clip.

**Format and size.** Use **AAC-LC in .m4a, mono, 24 kHz, 48 kbps**. It plays natively on iOS and Android; Opus on iOS is fragile. Estimated content:
- About 1,500 clips: 600 words × 8 characters, 600 phrases × 25, and 300 lines × 50.
- That is about 35,000 characters and about 60 minutes of audio.
- At 48 kbps that is about 6 KB per second, so **about 22 MB**. With slow versions, about 30 MB.
- Keep lossless 24 kHz WAV or FLAC masters outside the app.

**Cost per full pass (about 35,000 characters)**
- **ElevenLabs v4:** about $2.80. With 3 takes plus slow versions (about 120,000 characters), about $10, which one month of Creator ($22, 121k credits) covers. Starter ($6) covers about one pass. Flash costs half as much.
- **Gemini 3.8 Flash TTS:** 60 minutes is about 90,000 audio tokens, so about $0.81 plus about $0.08 input, roughly $0.90 per pass. Batch is about $0.45; Flash-Lite is about two-thirds of that. These roughly double from 2027.

## Asset sourcing
**Recommended base set: Microsoft Fluent Emoji** (MIT licence; I believe it comes in 3D, Color, Flat and High Contrast styles). It is consistent and child-friendly, and covers animals, food (including taco and tamal), clothes, weather, faces and families.

| Set | Licence | What you must do |
|---|---|---|
| Fluent Emoji (MIT) | MIT | Include the copyright notice and licence text on an Acknowledgements screen |
| Twemoji, jdecked fork (Emoji 17) | Graphics CC BY 4.0, code MIT | Credit it with a link |
| Noto Emoji | Images Apache 2.0, font OFL, flags public domain | Include the licence |
| OpenMoji | CC BY-SA 4.0 | Credit with "All emojis designed by OpenMoji – the open-source emoji and icon project. License: CC BY-SA 4.0"; any modified graphics must be shared under BY-SA |

Sources: https://github.com/microsoft/fluentui-emoji, https://github.com/jdecked/twemoji, https://github.com/googlefonts/noto-emoji, https://github.com/hfg-gmuend/openmoji. **High.**

- **Gaps in emoji sets:** many action verbs, shoulders and knees, and prepositions. Fill these with a matched style (OpenMoji extras, commissioned art, or AI images).
- **If using AI images:** fix one style prompt, review every image by hand, and check cultural accuracy. Gemini image models fall under the same under-18 clause. This advice is **low** confidence.

## Open questions / could not verify
- I couldn't open the official ElevenLabs or Google pricing pages, so all prices come from secondary sources. The v4 credit rate on subscription plans is unconfirmed.
- Whether Gemini's under-18 clause covers offline clips; this needs a written answer from Google.
- Whether Gemini 3.8 TTS supports es-ES and es-US, and whether accent prompts reliably tell Mexican from Castilian Spanish.
- The exact wording of the 2026 ACTFL Can-Do statements, and the size of the Cambridge Pre-A1 Starters word list.
- ElevenLabs accent label strings, and whether a library voice must be added to "My Voices" before API use.
- How well v4 handles single-word inputs; this needs listening tests.
- Which ffmpeg version fixes the short-clip `loudnorm` bug.
- Claims that iOS 17+ plays Opus more widely.
- The 10–15 minute session length and the 4–6 new words per session are practical rules of thumb, not research findings.
