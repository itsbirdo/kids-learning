# Building a Spanish Learning App for Kids: Research Notes

Compiled November 8, 2026. Goal: a good-quality, personal (non-commercial) Spanish tool for kids aged 6 to 10, preferably on iPad, with voice interaction and no subscription.

Prices, model rankings and platform rules change quickly. Most ranking figures below come from blog roundups and vendor claims, not independent Spanish-specific benchmarks. Verify anything you depend on before you build.

---

## 1. Summary

- Open-source voice models now compete with ElevenLabs on quality, and Spanish is supported. Voice output (TTS) is the easy part of this project.
- The hard parts are hearing the child (kids' speech is harder for recognizers) and scoring pronunciation.
- On-device processing is the best fit: it is fast, private, avoids per-minute cloud bills, and sidesteps most children's-privacy issues.
- Recommended pipeline: bundled pre-generated lesson audio, on-device Kokoro for dynamic phrases, Azure Pronunciation Assessment for scoring, and optional live conversation later via Gemini Live or gpt-realtime mini.
- iPad gives the smoothest on-device AI. Android gives the easiest and cheapest distribution. The deciding question is whether you own a Mac.

---

## 2. Existing apps (free or one-time payment, ages 6 to 10)

Free and one-time options are strong for maths. Spanish apps with good speech feedback are mostly subscription-based.

**Maths and general learning**

| App | Notes |
|---|---|
| Khan Academy Kids | Free, ad-free, no in-app purchases. Tops out around age 8, so it suits the younger end. |
| Khan Academy (main app) | Aimed at ages 10 and up, free lessons. A step up for 9 and 10 year olds. |
| Prodigy Math | Battle-game style, ages 6 and up. Learning content is free, with optional paid extras and upgrade prompts. |
| Mathland | Pirate adventure for ages 5 to 10, one-time purchase of about $6. |

**Spanish with speaking practice**

| App | Notes |
|---|---|
| Duolingo | Free, described as the best free option for kids 7 and older. Has speaking exercises but pushes its paid tier. |
| Speak Pocket | Free download, listen-repeat-speak design, no ads, works offline. A $9.99 premium is listed. Confirm it is a one-time unlock before buying. |
| Gus on the Go | One-time purchase, no ads or subscriptions, but aimed at preschoolers. |

**Skip given a no-subscription rule:** Pili Pop (strong kid-tuned voice recognition, but a significant subscription price) and Studycat (about $14.99 a month after a 7-day trial).

**Voice conversation gap:** No one-time-purchase kids app was found that offers free-form voice conversation. A parent can use voice mode in the Claude app alongside the child to practise phrases and pronunciation together.

---

## 3. Voice output (text-to-speech)

### 3.1 On-device (iPhone and iPad)

- **Kokoro (82M parameters, Apache 2.0).** A CoreML port runs on the Neural Engine at roughly 80MB quantized. A Swift package reports about 0.08 real-time factor on an iPhone 16 Pro. One review calls its Spanish clean and well paced. The Spanish voice list looks short, so audition it.
- **NVIDIA Magpie (357M, 9 languages including Spanish).** Has an iOS port, but only 5 fixed speakers.

### 3.2 Self-hosted server

- Strongest open models in an August 2026 roundup: Breeze TTS 2, Fish Audio S2 Pro, Voxtral TTS. All three have non-commercial licenses. Breeze's model card documents only English and Chinese.
- Because this is for your own kids, non-commercial licenses do not matter. They only bite if you ever sell the app.
- Permissive-license options if you ever commercialise: Qwen3-TTS (Apache 2.0, 10 languages, users report it defaults to Latin American Spanish), VoxCPM2 (Apache 2.0, 30 languages) and Chatterbox (MIT, 23 languages).
- Top models want roughly 12 to 16GB of GPU memory.
- There is no Ollama-style tool for TTS yet. The serving layer (for example vLLM-Omni or LocalAI) is the real work.

### 3.3 Cloud APIs

| Service | Notes |
|---|---|
| ElevenLabs | Regional Spanish voices (Mexican, Argentine, Latin American). Pay-as-you-go list rates of about $0.05 per 1,000 characters on Flash and $0.10 on v3, roughly 5 to 10 cents per minute of generated speech. |
| Gemini 3.1 Flash TTS | Ranked above Eleven v3 on one leaderboard at about $36.6 per million characters. A reviewer found its Mexican and Castilian output convincing. |
| Azure HD voices | About $22 per million characters. |

Only the spoken replies are billed, not the child's speech.

### 3.4 Money-saving idea

Lesson vocabulary is fixed. Generate those clips once with the best voice (ElevenLabs or Gemini) and bundle them in the app. Only free-form replies need live TTS.

---

## 4. Hearing and scoring the child (the key part)

- **Azure Pronunciation Assessment** supports Spanish. It scores accuracy, fluency and prosody down to phoneme level, costs the same as Azure speech-to-text, and Microsoft suggests testing es-ES against es-MX to see which scores better.
- **SpeechAce** also covers es-ES and es-MX with phoneme feedback, from $40 a month.
- **Kids are a weak spot for recognizers.** Models trained on adult speech do not transfer well to children. In English child corpora, zero-shot Whisper medium had about 32% word error rate on one kids' test set and about 30% on non-native kids' read speech. Expect noise with children learning Spanish.
- **Design around it:** word-level checks of known phrases, forgiving matching, and no free-form grading.

---

## 5. Live voice conversation (speech-to-speech)

| Option | Pricing notes |
|---|---|
| OpenAI gpt-realtime-2.1 | $32 / $64 per million audio tokens in / out. A mini version is $10 / $20. |
| OpenAI GPT-Live 1 | About $0.05 per minute. |
| Gemini 3.8 Live | Roughly half a cent per minute in and under two cents out, but it bills accumulated context on every turn. |

One estimate puts uncached voice agents at $0.18 to $0.46 per minute. A daily 10 minute chat adds up, so treat live conversation as an optional add-on, not the core of the app.

---

## 6. Kids and privacy

This matters mainly if you ever publish. For personal family use it is not a concern.

- If you publish in the US for under-13s, the amended COPPA rule (compliance date April 22, 2026) treats audio recordings of a child's voice as personal information.
- There is a narrow exception for audio used only to answer the child's request and deleted right away.
- On-device processing sidesteps most of this.
- This is not legal advice. Check before launching anything publicly.

---

## 7. Server plus website vs native app

- A website avoids App Store review and fees, but on-device keeps latency low and keeps the child's audio private.
- A self-hosted server needs a GPU for the best models, plus the serving layer work described above.
- Conclusion: a native app with on-device models fits this project best.

---

## 8. Android vs iOS

The same stack runs on both. One codebase can cover both platforms.

### What carries over

- A Flutter plugin runs Kokoro fully on-device on both Android and iOS.
- Whisper speech recognition and sherpa-onnx speech synthesis run on Android too. One SDK reports Whisper-tiny about 7 times faster than real time on a mid-range phone.
- Azure pronunciation scoring is cloud-based and behaves the same on either platform. Azure's Speech SDK should support both, but confirm before committing.

### Comparison

| | iPad / iOS | Android |
|---|---|---|
| On-device voice speed | Fast. Kokoro on the Neural Engine (about 0.08 real-time factor on iPhone 16 Pro). | Varies a lot. Kokoro runs on CPU or NNAPI via ONNX Runtime. |
| Hardware consistency | High. One or two iPad models to test. | Low. You test on whichever tablet your kids have. |
| Built-in speech recognition | Reliable. | Inconsistent. Some manufacturers strip the system service, so check support first. Bundling Whisper avoids this. |
| Dev machine | Needs a Mac with Xcode. | Any OS. Android Studio is free. |
| Installing on your own devices | Free Apple ID builds expire after 7 days and must be rebuilt. $99/year extends to a year. TestFlight builds last 90 days. Tools like Sideloadly can auto re-sign but need a computer on your network. | ADB installs on your own devices remain supported. A free limited-distribution account allows up to 20 devices with no ID or fee. Full account is $25 one-time. |

### Android speed detail

One hobby app reports roughly 20 to 40 seconds to generate a minute of Kokoro audio on a flagship, 60 to 90 seconds on mid-range, and 2 to 3 minutes on budget phones. Piper voices were several times faster on the same hardware. This is one app's rough numbers, not a benchmark, but the gap versus iPhone is real. Mitigations: pre-generate lesson audio, and use Piper or smaller voices for live phrases.

### Android sideloading rule changes

Google's developer verification protections start September 30, 2026 in Brazil, Indonesia, Singapore and Thailand. Check whether your country is affected. Hobbyist limited-distribution accounts and ADB installs remain the personal-use routes.

### Recommendation

- Already have a Mac and an iPad: go iOS and budget the $99/year so the app does not lock itself every week.
- No Mac: Android is the practical route and costs nothing.
- A Flutter plus sherpa-onnx build keeps both options open, though it may give up the CoreML speed boost on iPad. iOS speed for that route was not verified.

---

## 9. Suggested build plan

1. Pick the platform (Mac and iPad: iOS. No Mac: Android).
2. Write the lesson content: vocabulary, phrases and short dialogues.
3. Pre-generate all fixed lesson audio with ElevenLabs or Gemini and bundle it in the app.
4. Add on-device Kokoro (or Piper on weaker Android devices) for dynamic phrases.
5. Add Azure Pronunciation Assessment for scoring, using forgiving word-level checks of known phrases. Test es-ES against es-MX.
6. Optional later: live conversation via Gemini Live or gpt-realtime mini, with a budget cap.
7. If you want top-end voices and have a GPU, self-host Voxtral or Fish S2 Pro for personal use.

---

## 10. Caveats

- Most rankings come from one roundup of English-weighted blind listening tests, plus vendor claims. No Spanish-specific benchmark was found. Listen to Spanish samples before committing.
- Android speed figures come from a single hobby app.
- Pricing and platform policies (especially Android developer verification) were changing at the time of writing.
- Some app pricing details (for example Speak Pocket's premium) need confirming in the App Store.

---

## 11. Sources

**Voice models and on-device**
- Open-source self-hosted TTS roundup: https://pinggy.io/blog/best_open_source_self_hosted_text_to_speech_models/
- Kokoro on iOS (CoreML): https://soniqo.audio/guides/kokoro
- speech-swift (Kokoro and Magpie ports): https://github.com/soniqo/speech-swift
- Spanish TTS comparison: https://dev.to/tarunyadav1/spanish-text-to-speech-best-voices-and-models-204b
- Best Spanish TTS tools (Sept 2026): https://freetts.org/best-spanish-text-to-speech-tools

**Pricing**
- ElevenLabs pricing: https://dev.to/techsifted/elevenlabs-pricing-2026-plans-credits-and-api-costs-explained-1549
- TTS pricing compared (Aug 2026): https://invideo.io/blog/ai-voice-model-pricing/
- OpenAI Realtime pricing: https://www.forasoft.com/blog/article/openai-realtime-api-pricing
- GPT-Live pricing: https://www.eesel.ai/blog/gpt-live-pricing

**Pronunciation scoring and kids' speech**
- Azure pronunciation assessment: https://learn.microsoft.com/en-ca/azure/ai-services/speech-service/how-to-pronunciation-assessment
- SpeechAce Spanish notation: https://api-docs.speechace.com/guides-on-common-topics/phonetic-notation/spanish-es-es-es-mx
- Kid-Whisper paper: https://arxiv.org/abs/2309.07927v3

**Privacy**
- Amended COPPA overview: https://www.mondaq.com/unitedstates/privacy-protection/1814308/the-amended-childrens-online-privacy-protection-act-coppa-regulations-what-your-business-needs-to-know

**Android**
- Flutter Kokoro plugin: https://pub.dev/documentation/flutter_kokoro_tts/latest/
- VoxSherpa (Kokoro and Piper on Android): https://github.com/CodeBySonu95/VoxSherpa-TTS
- On-device AI SDK (Whisper, sherpa-onnx): https://klibs.io/project/deviceai-labs/deviceai
- Android on-device speech recognition: https://xckevin.github.io/en/blog/android-on-device-speech-recognition/
- Android developer verification FAQ: https://support.google.com/android-developer-console/answer/16561738
- Verification timeline: https://www.androidauthority.com/android-sideloading-changes-timeline-3679204/
- Verification rollout markets: https://www.helpnetsecurity.com/2026/06/19/android-developer-verification-rollout-markets/

**iOS**
- Apple free vs paid signing: https://expo.dev/blog/apple-developer-program-explained-free-vs-paid.md
- Free Apple ID sideloading guide: https://larsboes.github.io/mach-mono/guides/sideloading
- Xcode pricing and TestFlight: https://theswiftk.it.com/blog/is-xcode-free-pricing-2026
- Sideloadly: https://sideloadly.io/
