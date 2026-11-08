# On-device speech research for the Spanish kids app

> Verification report produced on 2026-11-08 while planning this project. Some primary sites were unreachable from the research environment, so several facts come from search-engine extracts of official pages; confidence ratings reflect that. Re-check anything rated medium/low (M/L) before relying on it.

Two findings change the plan:
- **sherpa-onnx removed espeak-ng in v2.0.0 (October 2026).** Spanish Piper and Kokoro voices no longer work from plain text in the current version.
- **Kokoro's Spanish voices are ungraded, and the only Flutter Kokoro plugin is English-only.**

Several sites were blocked from the research environment: huggingface.co, k2-fsa.github.io, soniqo.audio, apple.com, alphacephei.com, arxiv.org and isca-archive.org. I read model cards and docs through GitHub copies (git clones, raw files) and Apple's documentation JSON. On Linux I installed espeak-ng 1.51 and ported speech-swift's Spanish rules to compare their output.

## Verified facts

**Text-to-speech**
- **Kokoro Spanish voices** are `ef_dora` (female), `em_alex` (male) and `em_santa` (male), with lang_code `'e'` and espeak-ng `es` as the phonemizer.
  - The Spanish table has **no quality grades**, only name, traits and SHA256.
  - The file's header says: "Support for non-English languages may be absent or thin due to weak G2P and/or lack of training data."
  - It also notes "Weakness on short utterances, especially less than 10-20 tokens." Single-word prompts are exactly that case.
  - Source: https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md, read via byte-identical 7,625-byte GitHub copies (e.g. https://github.com/clayrosenthal/epub2audio/blob/main/VOICES.md). **High.**
- **The official Kokoro pipeline runs Spanish through espeak-ng** (`EspeakG2P(language='es')`): https://github.com/hexgrad/kokoro/blob/main/kokoro/pipeline.py. **High.**
  - espeak-ng `es` is Castilian. I checked it locally: gracias → `ɡɾˈaθjas` with `es`, but `ɡɾˈasjas` with `es-419`; lluvia → `ʎˈuβja` vs `ʝˈuβja`.
  - So the Spanish voices learned Castilian-style phonemes. Feeding them `es-419` phonemes for a Latin American accent is untested. **Medium.**
- **Licenses:** Kokoro code and weights are Apache-2.0, misaki is Apache-2.0, espeak-ng is GPL-3.0.
  - A Spanish-only espeak-ng adds about 1–1.5 MB (es_dict 48 KB, phondata 551 KB, library about 0.5 MB). The full data folder is 13 MB.
  - GPL obligations start when you distribute the app. Installing on your own family's devices is effectively a non-issue; a public App Store release is where GPL conflicts arise. This is not legal advice. **Medium.**
- **soniqo/speech-swift does speak Spanish without espeak**, using its own Swift code: a 125-word hand-made dictionary plus rule-based fallback (`Sources/KokoroTTS/LatinPhonemizer.swift`, `PronunciationDicts.swift`, commit a57702e, 2026-10-31).
  - I reproduced these fallback errors:
    - It always stresses the first syllable: zapato → `ˈθapato` (espeak gives `θapˈato`), mariposa → `ˈmaɾiposa`.
    - A word-initial r becomes a tap: rojo → `ˈɾoxo` (espeak gives a trill, `rˈoxo`).
    - It has no soft b/d/g sounds (verde → `ˈbeɾde`, espeak `bˈeɾðe`).
    - It lengthens accented vowels.
  - `addPronunciations()` is documented as English-only, so fixing Spanish means forking the package. **High.**
  - Its 54 voices match Kokoro v1.0's full voice count, so the Spanish voices are presumably included. I could not open the Hugging Face listing to confirm. **Medium.**
- **sherpa-onnx v2.0.0 removed espeak-ng and piper-phonemize** to become GPL-free (PR #4055, merged 2026-10-20; changelog https://github.com/k2-fsa/sherpa-onnx/blob/master/CHANGELOG.md, PR https://github.com/k2-fsa/sherpa-onnx/pull/4055).
  - The `data_dir` and `--kokoro-lang` settings are now ignored (`sherpa-onnx/csrc/offline-tts-kokoro-model-config.cc`).
  - Text input now needs either a lexicon file or phonemes you pass in yourself (`GenerationConfig.phoneme_codepoints` or `tokens`).
  - Open issue #4139 says the Kokoro lexicon path drops numbers and unknown words.
  - Latest is 2.0.1. The last version with espeak-ng is **1.13.8**. **High.**
- **sherpa-onnx's Kokoro model** (`kokoro-multi-lang-v1_0`) is model.onnx 310 MB plus voices.bin 26 MB, with 53 speakers. Spanish voices are **`ef_dora`=28 and `em_alex`=29; there is no `em_santa`**. The v1_1 model is Chinese/English only. Source: sherpa docs `tts/pretrained_models/kokoro.rst` in https://github.com/k2-fsa/sherpa. **High.**
- **Speed:** on a Raspberry Pi 4, Kokoro runs at real-time factor 3.2–7.6 against 0.35–0.8 for Piper medium. Piper is roughly 9× faster (`rtf.rst`, same repo). **High.**
- **Spanish Piper voices packaged by sherpa-onnx** (`scripts/piper/generate.py`), named `vits-piper-es_*`:
  - Spain: carlfm (x_low), davefx (medium), sharvard (medium, 2 speakers), glados (medium), miro (high).
  - Mexico: ald (medium), claude (high).
  - Argentina: daniela (high).
  - The upstream list is https://github.com/rhasspy/piper/blob/master/VOICES.md. Medium voices are about 60–75 MB. **High for names, Medium for sizes.**
- **Flutter `sherpa_onnx` 2.0.1** supports Android, iOS, macOS, Linux, Windows and Web, needs iOS 13.0 (podspec) and Android minSdk 21.
  - The official Dart example gets phonemes from `piper_phonemize` ^1.5.9 and passes them as `phonemeCodepoints`.
  - `piper_phonemize` is GPL-3.0, bundles espeak-ng data and supports Android and iOS (https://pub.dev/packages/piper_phonemize). **High.**
- **`flutter_kokoro_tts` is not usable for Spanish.** It is version 0.0.1, published about 8 months ago, with 4 likes, and the repo was last committed 2026-03-03.
  - Its espeak voice is hard-coded to `'en-us'` (`lib/src/espeak_ffi.dart`), and it lists English voices only.
  - On first run it downloads about 50 MB from Hugging Face (https://pub.dev/packages/flutter_kokoro_tts). **High.**
- **Apple AVSpeechSynthesizer** voice qualities are `.default` (on the device), `.enhanced` ("must download", iOS 9+) and `.premium` ("must download", iOS 16+).
  - There is no API for an app to list or trigger downloadable voices (https://developer.apple.com/forums/thread/758460). A parent installs them in Settings › Accessibility › Spoken Content › Voices.
  - `AVSpeechSynthesisIPANotationAttribute` (iOS 10+) lets you force a pronunciation. **High.**
  - The default Spanish voices are Mónica (es-ES) and Paulina (es-MX). **Medium.**

**Speech recognition**
- **SFSpeechRecognizer:** `supportsOnDeviceRecognition` and `requiresOnDeviceRecognition` exist from iOS 13. Apple's docs say "on-device requests won't be as accurate."
  - `contextualStrings` (iOS 10+) takes up to 100 phrases of 1–2 words.
  - `SFSpeechRecognitionResult.transcriptions` returns an n-best list sorted by confidence, and `SFTranscriptionSegment` has `confidence` and `alternativeSubstrings`.
  - Source: developer.apple.com/documentation/speech. **High.**
  - On-device locales match keyboard-dictation locales and need the Spanish dictation assets downloaded (https://developer.apple.com/forums/thread/119940). **Medium.**
- **SpeechTranscriber (iOS 26):** `supportedLocales` is async and includes downloadable locales, `isAvailable` is a hardware check, and models install through `AssetInventory`.
  - Result `alternatives` need the `alternativeTranscriptions` option; there is also a `transcriptionConfidence` attribute. **High.**
  - Spanish (es_ES, es_MX, es_US, es_CL) is in `supportedLocales` according to a third-party guide. **Medium.**
  - **Phrase biasing (`AnalysisContext.contextualStrings`) is documented only for DictationTranscriber.** DictationTranscriber (iOS 26) uses the same models as on-device SFSpeechRecognizer and also supports custom language models and a `farField` content hint. **High.**
- **WhisperKit has been renamed `argmaxinc/argmax-oss-swift`.** The product is `WhisperKit`, it needs iOS 16, and the latest tag is v1.1.1.
  - `DecodingOptions` has `language`, `usePrefillPrompt`, `promptTokens` and `prefixTokens`.
  - Argmax recommends `large-v3-v20240930_626MB`. **High.**
- **whisper.cpp** model sizes on disk are tiny 75 MiB, base 142 MiB and small 466 MiB.
  - It supports `initial_prompt`, GBNF grammar constraints (`grammar_rules`, `grammar_penalty`), and a `whisper-command` "guided mode" that picks one phrase from a list.
  - It can run the encoder on the Neural Engine via Core ML (https://github.com/ggml-org/whisper.cpp). **High.**
- **Whisper Spanish accuracy:** large-v2 is about 3% WER on the FLEURS benchmark per the Whisper paper. I could not open the paper to confirm.
  - A 2025 re-evaluation using a different scoring method (arXiv 2503.23542) gives tiny 27.7, base 22.0, small 17.5, large-v3 15.0. Treat **small as the floor for Spanish**. **Medium.**
- **Android:**
  - `createOnDeviceSpeechRecognizer` and `isOnDeviceRecognitionAvailable` are API 31; the first throws an exception if on-device recognition is unavailable.
  - `checkRecognitionSupport` and `triggerModelDownload` are API 33; the download "might trigger user interaction". `ModelDownloadListener` is API 34.
  - `ERROR_LANGUAGE_UNAVAILABLE` (13) means the language is supported but not downloaded.
  - `EXTRA_BIASING_STRINGS` is API 33. `EXTRA_PREFER_OFFLINE` is API 23 and "may have no effect". `EXTRA_MAX_RESULTS` and `CONFIDENCE_SCORES` (optional) are also available, and `RESULTS_ALTERNATIVES` is API 34.
  - Apps targeting API 30+ need a `<queries>` entry for RecognitionService (https://developer.android.com/reference/android/speech/SpeechRecognizer). **High.**
  - Devices without Google services, such as Amazon Fire tablets, are a likely gap. **Medium.**
- **Vosk grammar mode** restricts recognition to a JSON list of phrases such as `["gato","perro","[unk]"]`, via `vosk_recognizer_new_grm` or `Recognizer(model, rate, grammar)`, and `setGrammar()` swaps it at runtime.
  - The docs say it will "improve recognizer speed and accuracy but might return [unk]".
  - **Only the small models support it, not the large precompiled-graph models.** You can also request n-best (`set_max_alternatives`) and per-word confidence (`set_words`) (https://github.com/alphacep/vosk-api/blob/master/src/vosk_api.h). **High.**
  - `vosk-model-small-es-0.42` is about 39 MB (WER 16.0 on Common Voice, 11.2 on MLS); `vosk-model-es-0.42` is 1.4 GB and has no grammar support; both Apache-2.0. **Medium** (from Vosk's own table via search).
  - `vosk_flutter` 0.3.48 supports Android, Linux and Windows only (no iOS) and was last published about 3 years ago. **High.**
- **sherpa-onnx speech recognition with Spanish:**
  - Offline models: `nemo-parakeet-tdt-0.6b-v3-int8` (25 European languages) and `nemo-canary-180m-flash-en-es-de-fr-int8` (encoder 127 MB + decoder 71 MB), plus Whisper.
  - Phrase boosting ("hotwords") works only with transducer models using `modified_beam_search`.
  - The keyword-spotting models are Chinese/English only. **High.**
  - A streaming Spanish model, `streaming-zipformer-es-kroko-2025-08-06`, is mentioned by third parties only. **Low.**
- **Children's speech:** I found no benchmark of Whisper on Spanish child speech.
  - English: Kid-Whisper fine-tuning took Whisper-small from 13.93% to 9.11% WER on the MyST corpus (https://arxiv.org/abs/2309.07927).
  - Dutch child read speech: prompting Whisper with the expected text cut WER from 9.4% to 5.1% and raised reading-mistake detection F1 from 0.39 to 0.73. It needed a guard: if the prompted output's length strays from the target, fall back to an unprompted transcript (Gao et al., Interspeech 2025, https://arxiv.org/abs/2506.11079). **Medium.**
  - Whisper "smooths" mistakes, which risks marking wrong answers as correct. **Medium.**

## Corrections to the research doc
1. **§3.1 "Kokoro Spanish clean":** the Spanish voices are ungraded and the model is officially weak on short utterances. Its reference Spanish phonemizer is espeak-ng (GPL), with Castilian sounds.
2. **§3.1 "CoreML port about 80MB quantized":** speech-swift's docs list about 170 MB of weights (one decoder) and 676 MB peak memory on iPhone 16 Pro. It needs iOS 18 and downloads the weights from Hugging Face at runtime. The 0.08 real-time factor figure is confirmed (`docs/benchmarks/ios-coreml.md`).
3. **§8 "A Flutter plugin runs Kokoro on both platforms":** that plugin is English-only, version 0.0.1, with a single release. It is not viable for Spanish.
4. **§8 "sherpa-onnx speech synthesis":** since v2.0.0 (October 2026), Spanish Piper and Kokoro voices need `piper_phonemize` (GPL), a lexicon file, or pinning to 1.13.8. Its Kokoro model also has only two Spanish voices.
5. **§8 "iOS built-in recognition: reliable":** on-device Spanish needs downloaded dictation assets and is officially less accurate. The iOS 26 SpeechTranscriber has no documented phrase biasing; use DictationTranscriber or SFSpeechRecognizer instead.
6. **§8 "Bundling Whisper avoids this":** true, but for checking known words, Vosk's grammar mode (39 MB) is constrained and far smaller than Whisper-small (466 MB). Tiny and base are weak for Spanish.

## Concrete implementation details
- **speech-swift:**
  - SPM `.package(url:"https://github.com/soniqo/speech-swift", branch:"main")`; tags exist, latest v0.0.29. Product `KokoroTTS`; needs iOS 18 and Swift 6.
  - `let tts = try await KokoroTTSModel.fromPretrained()` (default model `aufklarer/Kokoro-82M-CoreML`).
  - `tts.synthesize(text:, voice:"ef_dora", language:"es", speed:1.0) -> [Float]` returns 24 kHz audio, chunked into 5-second graphs.
  - The first CoreML compile took about 20.5 s on a Mac.
- **WhisperKit:** SPM `https://github.com/argmaxinc/argmax-oss-swift`, product `WhisperKit`, iOS 16. Use `DecodingOptions(language:"es", promptTokens: …)`.
- **Apple recognizer:** `SFSpeechRecognizer(locale: Locale(identifier:"es-MX"))`, then check `supportsOnDeviceRecognition`, then set `request.requiresOnDeviceRecognition = true` and `request.contextualStrings = [target] + distractors`, and read `result.transcriptions`.
- **sherpa-onnx:**
  - Android: Maven/JitPack AAR 2.0.1. Flutter: `sherpa_onnx: ^2.0.1`.
  - Kokoro: `sid=28` for ef_dora. Piper: `vits-piper-es_MX-claude-high`.
  - Feed text through the lexicon or `phonemeCodepoints`.
- **Avoid shipping espeak-ng at all:** the vocabulary is fixed, so run espeak-ng (`es` or `es-419`) on the dev machine, generate a lexicon or phoneme strings for every lesson word and phrase, and ship only that data. Kokoro needs misaki's symbol adjustments (e.g. tʃ→ʧ, dʒ→ʤ).
- **Vosk:** Android `com.alphacephei:vosk-android` with `vosk-model-small-es-0.42`; use `setGrammar("[\"gato\",\"pato\",\"gorro\",\"[unk]\"]")` and `setMaxAlternatives(3)`.
- **Matching tactics for "did the child say it":**
  - Constrain recognition: grammar or bias lists with the target plus 2–4 sound-alike distractors plus `[unk]`. Pass only if the target wins; if a distractor or `[unk]` wins, ask the child to retry.
  - Use the n-best list; accept if the target is in the top 3 with acceptable confidence.
  - Normalize text: lowercase, strip accents and punctuation, convert digits to words, make articles optional.
  - Compare phonetically: convert both the expected text and the recognizer output to phonemes using the precomputed lexicon or Spanish Metaphone (https://github.com/amsqr/Spanish-Metaphone, Python port in abydos). Merge b/v, ll/y, c/s/z, silent h, and r/rr.
  - Accept if the normalized Levenshtein distance is about 0.25 or less; require exact matches for 1–2-syllable words.
  - Set thresholds from 50–100 recordings of your own kids; platform confidence scores are uncalibrated.
  - If you prompt Whisper with the expected text, add the length-deviation hallucination guard.
  - Always be forgiving: 3 tries, replay the model audio, and allow a parent override.

## Recommended on-device stack
- **(a) Native iPadOS:**
  - Speech output: bundled pre-generated lesson clips; AVSpeechSynthesizer (es-MX or es-ES, enhanced/premium if installed, IPA attribute for fixes) for dynamic phrases. Kokoro via a forked speech-swift with lexicon entries generated by espeak-ng is optional.
  - Hearing: on-device SFSpeechRecognizer, or DictationTranscriber on iOS 26, with contextual strings, n-best and phonetic matching. Fall back to WhisperKit small.
  - Rationale: no model download, Apple's recognizer supports phrase biasing, and Kokoro is only worth it after an audition.
- **(b) Native Android:**
  - Speech output: sherpa-onnx 2.0.1 with Piper es_MX-claude-high or es_ES-davefx-medium, fed by an offline-generated lexicon, plus pre-generated lesson audio.
  - Hearing: Vosk small-es with a grammar per exercise. Use the system on-device recognizer (API 33+ support check) only as a second opinion.
  - Rationale: Piper is about 9× faster than Kokoro on CPU, and Vosk's grammar mode is small and constrained and doesn't depend on the manufacturer.
- **(c) Flutter, both platforms:**
  - Speech output: `sherpa_onnx` 2.0.1 with Piper and an offline lexicon (or `piper_phonemize` at runtime, which is GPL-3.0).
  - Hearing on Android: Vosk via `vosk_flutter` (stale) or a small method channel.
  - Hearing on iOS: a method channel to SFSpeechRecognizer with contextual strings.
  - Shared Dart code for normalization and phonetic matching. sherpa-onnx Whisper-small or Canary-180M is the uniform fallback.
  - Rationale: no maintained cross-platform Flutter package does Spanish grammar-constrained recognition on iOS, so platform recognizers plus shared matching is the most reliable route.

## Open questions / could not verify
- How the Kokoro Spanish voices actually sound (they are ungraded), and whether `es-419` phonemes give a usable Latin American accent. Listen before committing.
- Which Spanish locales are actually on-device on the target iPad and iOS version, and SpeechTranscriber's hardware requirements. Run `SFSpeechRecognizer.supportedLocales()`, `SpeechTranscriber.supportedLocales` and `installedLocales` on the device.
- Whether Apple's custom language models (`SFCustomLanguageModelData`) support Spanish.
- WhisperKit size and latency on iPad: Argmax's benchmarks are on Hugging Face, which was blocked. The whisper.cpp FLEURS Spanish figures per model size are unconfirmed (arXiv blocked).
- Whether sherpa-onnx ships the Spanish Kroko streaming model, and exact Piper Spanish file sizes (the release page was truncated).
- Names of Apple's premium/enhanced Spanish voices.
- No children's Spanish (or child second-language) recognizer benchmarks exist that I could find. Plan to build your own small test set.
- Whether the `speech_to_text` Flutter plugin (7.5.0) exposes on-device mode and alternatives; its pub.dev page doesn't say.
