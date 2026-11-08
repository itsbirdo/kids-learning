---
planned_number: 7
title: "Audio pipeline: pre-generate, QA, approve and bundle all lesson audio"
type: Feature
labels: [phase-1-content, "area: content", "area: speech"]
parent: 1
---

**Phase 1 · Size L · Depends on: #4 (voice choice), #5, #6, #24 (terms review) · Blocks: #10, #11**

## Goal
Every fixed clip (words, phrases, stories, prompts, feedback, name lines, dialogue lines) is generated once in the best acceptable voice. Each clip is then trimmed, loudness-normalised, checked by machine, approved by a parent, and bundled. Only parent-added custom words (#20) need live TTS.

## Choosing the provider
The final pick comes from the audition in #4 and the terms review in #24.

| Provider | Status | Notes |
|---|---|---|
| **Azure Neural/HD TTS** | **Default, terms-clean** | No minors clause found in Microsoft's terms. The F0 tier includes 0.5M characters/month, and one full pass is about 35k characters. The same voice can be used at runtime for parent-added custom words (#20), so the app sounds consistent |
| ElevenLabs `eleven_v4` | Quality option, only if #24 clears it | The usage policy bars apps "directed at individuals under 18… unless approved in writing". Use it only if #24 concludes pre-generated offline clips are fine, or we get written approval. The free plan is non-commercial and requires attribution |
| Gemini TTS (`gemini-3.8-flash-tts`) | **Excluded** | Gemini API terms bar apps "likely to be accessed by individuals under the age of 18". Google hasn't said whether that covers offline clips |
| Kokoro | Not used | Spanish voices are ungraded and weak on short utterances; needs GPL espeak-ng |

The pipeline hides the provider behind `synthesize(text, voice, settings) -> wav`, with adapters `azure` and `elevenlabs`.

### Azure details *(verify voice names and styles against the live voice list)*
- **Voice list:** `GET https://{region}.tts.speech.microsoft.com/cognitiveservices/voices/list`
- **Synthesize:** `POST https://{region}.tts.speech.microsoft.com/cognitiveservices/v1` with these headers:
  - `Ocp-Apim-Subscription-Key`
  - `Content-Type: application/ssml+xml`
  - `X-Microsoft-OutputFormat: riff-24khz-16bit-mono-pcm`
- **SSML:** `<speak version="1.0" xml:lang="es-MX"><voice name="es-MX-DaliaNeural"><prosody rate="-15%">el perro.</prosody></voice></speak>`
  - The `prosody rate` attribute makes the slow variants.
  - Use `<phoneme alphabet="ipa">` or `<sub>` to fix single words.
  - Audition the HD voices and `mstts:express-as` styles where a voice offers them.

### ElevenLabs details (only if allowed)
- **Request:** `POST /v1/text-to-speech/{voice_id}?output_format=wav_24000` with body `{model_id: "eleven_v4", language_code: "es", voice_settings: {stability: 0.7–0.8, similarity_boost: 0.5–0.75}, seed, apply_text_normalization: "off"}`. Use `previous_text`/`next_text` for story lines.
- **Slow variants:** v4 has no `speed`. Either use `eleven_v3` / `eleven_multilingual_v2` with `speed: 0.8–0.85` (the voice may differ slightly), or slow the v4 take with ffmpeg `atempo=0.85`. Compare by ear.
- **Accent:** comes from the voice, not `language_code`. Filter shared voices by `language=es`, accent and a long `min_notice_period_days`, or design our own voice.

## Clip inventory
Roughly 1,500 clips, 35k characters and 60 minutes of audio:
- each item: normal + slow
- each phrase: normal + slow
- story lines
- prompts (ES classroom + EN instructions)
- feedback lines
- routines
- dialogue lines for #21, if built
- name lines, generated from `content/local/family.yaml`, which is never committed

## Cache key and manifest
- **Cache key:** `sha256` of canonical JSON containing `{provider, model, voice_id, text (Unicode NFC), language, sorted settings, ssml_template_version, dictionary_version, output_format, seed, postproc_version}`. Re-running costs nothing for unchanged clips.
- **Manifest (`audio_manifest.json`):** `clip_id → {hash, file, duration_ms, lufs, take, approved_by, approved_at}`.
- **Masters:** keep lossless WAV masters **outside git** (family cloud drive). Regenerating isn't reproducible: seeds are best-effort, models retire and library voices can be withdrawn.
- **In the repo:** compressed clips go through **Git LFS**.

## Post-processing (ffmpeg + `pyloudnorm`)
1. Trim leading and trailing silence: `silenceremove` at −50 dB, then `areverse`, `silenceremove` again, and `areverse` back.
2. Pad 60 ms before and 250 ms after; 10 ms fade-in.
3. Loudness −16 LUFS, −1.5 dBTP. Measure with `pyloudnorm` and apply a fixed gain plus `alimiter`. ffmpeg `loudnorm` is unreliable on clips under ~3 s.
4. Encode **AAC-LC `.m4a`, mono, 24 kHz, 48 kbps**. That is about 22 MB for the whole set, about 30 MB with slow variants. It plays natively on Android and iOS; Opus on iOS is fragile.

## QA and approval
- **Automatic checks:**
  - transcribe every clip with `faster-whisper` (small/medium, `language="es"`) and compare to the normalised text;
  - flag mismatches, odd characters-per-second, duration outliers and clipping.
- **`kl review`:** a local web page listing clips with play buttons and Approve / Regenerate (new seed or take) / Note. Decisions are written to the manifest.
- **Gate:** `kl build` bundles approved clips only. Unapproved clips fall back to system TTS in dev builds only.

## Cost per full pass (about 35k characters)
| Provider | Cost |
|---|---|
| Azure | $0 inside F0 (about $0.80 at the HD list price, verify) |
| ElevenLabs v4 | About $2.80 per pass; about $10 with retakes and slow variants (one month of Creator at $22 covers it) |

## Tasks
- [ ] Provider interface plus the Azure adapter (ElevenLabs adapter only if #24 allows)
- [ ] Clip inventory generated from `content.json`, with the cache and manifest
- [ ] Post-processing chain, with unit tests on sample clips
- [ ] Whisper QA report
- [ ] `kl review` approval UI
- [ ] Generate, review and approve Units 1–3, then the rest as #5 lands
- [ ] Document the masters archive location and restore steps in `docs/audio-pipeline.md`

## Acceptance criteria
- [ ] `kl audio generate --unit u01` → `kl review` → `kl build` produces bundled, approved clips; running it again makes no API calls
- [ ] All clips measure −16 ± 1 LUFS and have no clipping
- [ ] The app plays the clips (#10)
- [ ] API keys come only from environment or `.env` (gitignored)
