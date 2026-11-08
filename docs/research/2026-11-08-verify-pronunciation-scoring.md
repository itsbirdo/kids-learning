# Pronunciation scoring: verification report (as of 2026-11-08)

> Verification report produced on 2026-11-08 while planning this project. Some primary sites were unreachable from the research environment, so several facts come from search-engine extracts of official pages; confidence ratings reflect that. Re-check anything rated medium/low (M/L) before relying on it.

## Verified facts

**Azure Pronunciation Assessment (PA)**
- **Spanish locales:** es-ES and es-MX are the Spanish PA locales. Microsoft says to try both and keep whichever scores better. About 33 PA locales exist in total. (high) https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support?tabs=pronunciation-assessment, https://learn.microsoft.com/en-us/azure/ai-services/speech-service/how-to-pronunciation-assessment
- **Available for Spanish:** accuracy, fluency, completeness and PronScore. Scores come at full-text, word and phoneme level, and word ErrorType is returned. (med-high, same URL)
- **en-US only (per the "Supported features per locale" table):**
  - Phoneme names: IPA en-US only; SAPI en-US and zh-CN.
  - Syllable groups: en-US only.
  - Spoken-phoneme N-best (`NBestPhonemeCount`): en-US only.
  - Prosody assessment: en-US only, needs SDK ≥1.35.
  - Content score (vocabulary/grammar/topic, unscripted only): en-US only.
  - For es-ES you get per-phoneme scores with empty `"Phoneme": ""` labels. Users report the same for fr, ja and en-GB.
  - (high for prosody and phoneme names; med for the content score) Same URL, plus https://learn.microsoft.com/en-us/azure/ai-services/speech-service/pronunciation-assessment-tool and https://github.com/Azure-Samples/cognitive-services-speech-sdk/issues/2237
- **Unscripted mode:** you get it by leaving ReferenceText empty, and it uses a different STT model. I could not find Spanish-specific confirmation. (low-med)
- **Miscue:** With `EnableMiscue=false`, the recognized text is treated as the reference text. With `true`, words are marked Omission or Insertion. Miscue is not supported in continuous mode, where you diff against the reference yourself. (high) https://learn.microsoft.com/en-us/objectivec/cognitive-services/speech/spxpronunciationassessmentconfiguration
- **Known failure mode:** short phrases and single words often score 100 regardless of what is said ("citizen", "good morning"). Wrong words are not flagged. (med, several user reports) https://learn.microsoft.com/en-us/answers/questions/1680083/, https://learn.microsoft.com/en-us/answers/questions/1857506/
- **REST short audio:**
  - Max 60 s of audio, and **≤30 s for PA**.
  - Formats: `audio/wav; codecs=audio/pcm; samplerate=16000` or `audio/ogg; codecs=opus`.
  - Final results only, no partials.
  - Streaming/continuous mode (>30 s) is SDK-only. Pronunciation assessment on the fast-transcription API is reported as unsupported. (high) https://learn.microsoft.com/en-us/azure/ai-services/speech-service/rest-speech-to-text-short
- **iOS SDK:**
  - Swift Package Manager: https://github.com/microsoft/speech-sdk-spm, product `MicrosoftCognitiveServicesSpeech-iOS`, available from 1.51 (released 2026-07).
  - CocoaPods (`MicrosoftCognitiveServicesSpeech-iOS`) is **no longer published from 1.53 onward**.
  - Import with `import MicrosoftCognitiveServicesSpeech`.
  - Min iOS 11.0, per the setup page. (med-high) https://learn.microsoft.com/en-us/azure/ai-services/speech-service/releasenotes, https://learn.microsoft.com/en-us/azure/ai-services/speech-service/quickstarts/setup-platform
- **Android SDK:** Maven `com.microsoft.cognitiveservices.speech:client-sdk:<ver>` (AAR). Use **≥1.48.2**: older versions have a CRL-caching bug that breaks Android connections (Microsoft asked for updates by 2026-07-01). x86 was dropped in 1.49. (high) https://github.com/Azure-Samples/cognitive-services-speech-sdk/issues/3029. I could not verify minSdk.
- **Flutter:** there is no official plugin. The community package `azure_speech_recognition_null_safety` 0.9.6 (Android/iOS) added assessment in 0.9.2 and continuous assessment in 0.9.6, but has quality warnings. `azure_speech_assessment` is GPL-3.0. (med) https://pub.dev/packages/azure_speech_recognition_null_safety
- **Pricing:**
  - Official docs: "As a baseline, usage of pronunciation assessment costs the same as speech to text" (pay-as-you-go or commitment tier). (high) how-to URL above.
  - Standard real-time STT is about $1/audio-hour, reportedly billed per second.
  - Prosody (and the content features) are listed as "enhanced add-on, per hour per feature". Third parties quote about $0.30/h, but the official page rendered "$-" so I could not confirm it. Irrelevant for Spanish anyway.
  - The F0 free tier gives 5 audio hours/month and F0 quotas are not adjustable. Whether PA counts against F0 is not explicitly stated (med). https://azure.microsoft.com/en-us/pricing/details/speech/
- **Auth:**
  - Request: `POST https://{region}.api.cognitive.microsoft.com/sts/v1.0/issueToken` with header `Ocp-Apim-Subscription-Key`. The body is a JWT.
  - **Valid 10 minutes**; Microsoft recommends reusing a token for 9. Send it as `Authorization: Bearer`. (high)
  - `disableLocalAuth=true` kills keys and issueToken.
  - Entra alternative: assign the role "Cognitive Services Speech User", use scope `https://cognitiveservices.azure.com/.default`, and the SDK token format `aad#{resourceId}#{entraToken}`. It needs a custom subdomain. (med) https://learn.microsoft.com/en-us/azure/ai-services/speech-service/how-to-configure-azure-ad-auth
- **Data handling:**
  - "By default, requests aren't logged (neither audio nor transcription)."
  - Logging is opt-in through `EnableAudioLogging()` (SDK) or `storeAudio=true` (REST). (high) https://learn.microsoft.com/en-us/azure/ai-services/speech-service/faq-stt, https://learn.microsoft.com/en-us/azure/ai-services/speech-service/logging-audio-transcription
  - The data-privacy page reportedly says real-time STT and PA data are not retained (med, quoted second-hand).
- **Children:**
  - Microsoft's transparency note: grading "for children's learning might not be as strict as that for adult learning". Thresholds are left to the developer. (high)
  - Microsoft claims >0.5 Pearson correlation with human judges, with no child data. (high that it's claimed) https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/speech-service/pronunciation-assessment/transparency-note-pronunciation-assessment
  - Microsoft recommends ≥16 kHz input.

**Alternatives**
- **SpeechAce:**
  - Dialect codes `es-es` and `es-mx`.
  - Endpoint `POST https://api.speechace.co/api/scoring/text/v9/json?key=…&dialect=…`, multipart text plus audio.
  - For Spanish: word and sentence pronunciation, and fluency with `include_fluency=1`. Grammar, vocabulary and relevance are English-only.
  - Spanish was announced as **beta**, trained on non-native speakers.
  - Plans: Basic $40/mo (5,000 15-second requests, phoneme feedback), Pro $80/mo (fluency). Overage about $0.008 per 15 s. A free trial exists but its length conflicts between sources (14 vs 30 days).
  - The Score Text reference page still lists only en-us/en-gb, which conflicts with the Spanish guide.
  - (med) https://api-docs.speechace.com/getting-started/supported-languages, https://api-docs.speechace.com/use-cases/speaking-practice-in-spanish-and-french, https://www.speechace.com/api-plans/
- **SpeechSuper:**
  - Spanish word, sentence and paragraph assessment with phoneme scores.
  - About $0.004/word request (≤20 s), $0.006/sentence (≤90 s), $0.008/paragraph. $20/month minimum. You must contact them for keys.
  - The offline SDK covers English and Mandarin only.
  - (low-med, mostly third-party sources) https://www.speechsuper.com/pricing.html, https://rapidapi.com/qiusidong/api/speechsuper
- **On-device phoneme models:**
  - `facebook/wav2vec2-xlsr-53-espeak-cv-ft`: Apache-2.0, about 315M parameters, 392 IPA tokens at 20 ms frames. Community int8 ONNX exports exist (MaceWindu/SpeechModels; allan-valin, PER 50.6 vs 49.8 fp32 on VoxAngeles). A distilled 8-layer student is 77 MB vs 241 MB (air-air/xlsr-53-espeak-student-ONNX). (med) https://huggingface.co/facebook/wav2vec2-xlsr-53-espeak-cv-ft, https://huggingface.co/allan-valin/wav2vec2phoneme-onnx
  - ZIPA (ACL 2025): 64M-parameter Zipformer phone recognizers that beat earlier 300M models. Licence promised "permissive" but unverified. (med) https://arxiv.org/abs/2505.23170
  - An open GOP+CTC reference implementation reaches r=0.431 on speechocean762 (English adults). (med) https://github.com/Victus0904/phoneme-mispronunciation-detection, https://arxiv.org/pdf/2506.12067

**Kids' speech**
- **Kid-Whisper** (Attia et al., AIES 2024):
  - Fine-tuning on MyST cut WER from **13.93%→9.11% (Whisper-Small)** and **13.23%→8.61% (Medium)**.
  - CSLU spontaneous: Small went from 32.00% to 27.16%. The best model reached 16.53%, about half of zero-shot.
  - Zero-shot WER on CSLU-scripted is 6–10× LibriSpeech; on MyST, 3–5×.
  - Gains came largely from data cleaning, generalized to unseen child sets, and cost about 1% on adult speech.
  - Every dataset is **native English-speaking children**. (high) https://arxiv.org/abs/2309.07927, https://ojs.aaai.org/index.php/AIES/article/view/31618
- **Zero-shot Whisper-large-v3:** 12.6% WER on MyST and 19.9% on OGI. Tiny is at 53.8% on OGI. (med) https://arxiv.org/abs/2406.10507
- **NOCASA 2025:** L2 Norwegian children scoring single words as 1–5 game stars. Best baseline UAR 36.4% (MAE 0.55); best entry, using GOP-CTC, 44.8% UAR (MAE 0.505). Expect about ±½ star of noise even from purpose-built systems. (high) https://arxiv.org/abs/2504.20678, https://arxiv.org/abs/2509.03256
- **"Say It Again, Kid!"** (ages 6–12): 0–5 stars, r=0.59 against an expert; EEG showed improved perception of speech sounds. (high) https://www.isca-archive.org/slate_2023/karhila23_slate.pdf
- **Ages 5–7 study:** humans agreed with each other well, but automatic detection agreed with humans only at low levels. (med) https://par.nsf.gov/servlets/purl/10647025
- **Project LISTEN:** its reading tutor rejected too many correct readings, and the same word was repeatedly rejected for children. False rejections are the costly error. (med) https://www.isca-archive.org/eurospeech_2003/banerjee03_eurospeech.pdf

## Corrections to the research doc
1. "Scores … prosody down to phoneme level" is wrong for Spanish. Prosody, phoneme names, syllables and N-best phonemes are en-US only. For Spanish you get word scores plus unlabeled phoneme scores.
2. "Costs the same as STT" is correct for the baseline. Prosody and content are billed add-ons (rate unverified), but they are unavailable for Spanish anyway.
3. The "32% … zero-shot Whisper medium" figure is actually **Whisper-Small** zero-shot on CSLU spontaneous (32.00%). The "~30% on non-native kids' read speech" figure is **not in Kid-Whisper**, which uses native English children only; I couldn't find its source. These are also English ASR numbers, not pronunciation-scoring results.
4. Section 8, "Azure SDK should support both": confirmed. Note the SPM move, the end of CocoaPods at 1.53, Android ≥1.48.2, and no official Flutter plugin.
5. SpeechAce: "$40/month" is right, but Spanish is beta and fluency needs Pro ($80).
6. Add the known risk: single words and short phrases often score ~100 unless `EnableMiscue=true` and the recognized text is checked.

## Concrete implementation details
**Recommended transport:** REST short audio for all platforms. It is plain HTTPS, works from Dart, Swift and Kotlin, and suits 2–3 s clips. Use the SDK only if you want live streaming.
- Endpoint: `POST https://{region}.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?language=es-MX&format=detailed`
- Headers:
  - `Authorization: Bearer {token}`
  - `Content-Type: audio/wav; codecs=audio/pcm; samplerate=16000`
  - `Accept: application/json`
  - `Pronunciation-Assessment: base64(JSON)`
  - Optionally `Transfer-Encoding: chunked`
- JSON for the header:
  `{"ReferenceText":"el perro","GradingSystem":"HundredMark","Granularity":"Word","Dimension":"Comprehensive","EnableMiscue":true}`
  - GradingSystem is FivePoint or HundredMark (default FivePoint).
  - Granularity is Phoneme, Word or FullText (default Phoneme).
  - Dimension is Basic or Comprehensive.
  - Omit `EnableProsodyAssessment`, `PhonemeAlphabet` and `NBestPhonemeCount` because they are en-US only.
- Response:
  - `RecognitionStatus` is Success, NoMatch, InitialSilenceTimeout or BabbleTimeout.
  - `NBest[0]` holds `Lexical` and `Display`, the Accuracy, Fluency, Completeness and PronScore values, and `Words[]` with `Word`, `AccuracyScore` and `ErrorType` (None, Omission, Insertion or Mispronunciation).
  - With the SDK's JSON the scores are nested under `PronunciationAssessment{}`. Parse both layouts defensively (med).
- Audio: 16 kHz, 16-bit, mono PCM WAV, ≤30 s. Trim leading and trailing silence on the device to cut billing.
- SDK path (iOS):
  - `SPXPronunciationAssessmentConfiguration(referenceText, gradingSystem: .hundredMark, granularity: .word, enableMiscue: true)`, then `applyTo(recognizer)` and `recognizeOnce`.
  - Build the config with `SPXSpeechConfiguration(authorizationToken:region:)`.
  - Consider raising the initial-silence and segmentation-silence timeouts for hesitant kids. The property names are from memory, so verify them.
- Token vending (Cloudflare Worker or Azure Function, about 30 lines):
  - Store the key as a Worker secret.
  - `GET /token` checks an app secret header and rate-limits.
  - It calls issueToken, caches the token for 9 minutes, and returns `{token, region, expiresIn: 540}`.
  - The client refreshes the token before expiry.
- Risk of embedding the key in a personal, sideloaded app: the key can be pulled from the IPA or APK and grants every Speech feature on that resource. On S0 there is no hard spend cap; budgets only alert.
  - **Mitigation: use an F0 resource.** A leak can then only burn the free 5 hours and cannot cost money.
  - Keep Key1/Key2 rotation available.
  - For a family app this is acceptable. The Worker is cheap insurance.
- Privacy: never call `EnableAudioLogging` and never set `storeAudio`. Store raw JSON only on the device, not the audio.
- **Cost:** 50 attempts/day × about 4 s billed ≈ 200 s/day ≈ **1.7 h/month per child**. That fits in F0 for up to 2 children (5 h cap). On S0 it is about $1.70–2.25/child/month. Add a graceful mode for when the quota runs out.

## Recommended scoring design
1. **Gate first, don't score.** If the status is not Success, or nothing was heard, say "I couldn't hear you, try again." It doesn't count as an attempt.
2. **Check the right word was said.** Normalize case and accents in `NBest[0].Lexical`. If no target content word is present, or its ErrorType is Omission, give that word 0. Ignore Insertions such as "eh" or "um".
3. **Word score** = word `AccuracyScore`. **Phrase score** = mean over reference words, with omissions counted as 0. Ignore Fluency, Completeness and PronScore for 1–3 word items. Fluency can only ever add a bonus, never subtract.
4. **Stars (starting thresholds):** ≥75 → 3★, ≥50 → 2★, anything heard → 1★, so trying always earns a star.
   - Profile offsets: about −5 for age 6–7, about +5 for age 9–10.
   - Use hysteresis: show the best attempt, and never lower stars already shown.
5. **Feedback:** no numbers for the child. Praise first, then name at most one word to retry (the lowest word below 50) and play the model audio for that word. No phoneme-level feedback for Spanish, because the labels are empty. Lesson metadata can drive tips for hard sounds (rr, j, ñ, vowels).
6. **Retries:** at most 3 per item. After the third, play the model audio, give the best score, move on, and re-queue the item later. Bias toward acceptance, because false "try again" is worse for kids than a false "great".
7. **Calibration on your own kids (about one evening):**
   - Each child says 40 items twice, and the parent records the same items.
   - A parent labels each child attempt good, OK or needs-work.
   - Run everything through **both es-ES and es-MX**. Pick the locale with the best *separation* between label groups, not just the higher mean.
   - Set the 3★ threshold at about the 25th percentile of "good" items. Set 2★ so that under 5% of "good" or "OK" items fall below it.
   - Measure test-retest spread. If it is above 10 points, widen the bands.
   - Test failure cases: an English word, a wrong Spanish word, silence.
   - Afterwards auto-tune: if a child earns over 85% 3★ for a week, raise the threshold by 3; under 40%, lower it by 3.
8. **Offline fallback, later:** realistic only as a coarse pass/fail.
   - Run an int8 xlsr-espeak model (about 300 MB) or ZIPA-small through ONNX Runtime Mobile.
   - Precompute the reference IPA at build time, so espeak-ng (GPL) is not shipped.
   - CTC forced alignment, then logit-based GOP, mapped to stars using the same calibration set.
   - Child-speech performance is unvalidated; expect a week or more of work.
   - A simpler fallback is on-device ASR keyword matching (iOS on-device Spanish recognition, or a bundled Whisper).

## Open questions / could not verify
- I could not read learn.microsoft.com or arxiv.org directly. Re-check the per-locale feature table, the exact REST JSON field nesting, and whether prosody is still en-US-only as of November 2026.
- Exact current prices: whether PA counts against F0, the per-second billing granularity, the add-on rate, and F0 concurrency.
- Android minSdk, the iOS minimum for SDK 1.5x, and the current Maven version.
- SpeechAce: whether `es-es` and `es-mx` are accepted on score/text v9 (the docs conflict) and whether Spanish has left beta. SpeechSuper's Spanish `coreType` names and official prices.
- No published evaluation of Azure PA (or any vendor) on **child L2 Spanish**, so the thresholds must come from your own calibration.
- ZIPA licence, the Spanish phone error rate of the xlsr-espeak model, and on-device latency.
- The source of the doc's "~30% non-native kids" figure.
