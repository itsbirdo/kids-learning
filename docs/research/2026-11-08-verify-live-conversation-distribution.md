# Live voice and distribution: verification report (as of 2026-11-08)

> Verification report produced on 2026-11-08 while planning this project. Some primary sites were unreachable from the research environment, so several facts come from search-engine extracts of official pages; confidence ratings reflect that. Re-check anything rated medium/low (M/L) before relying on it.

**How sources were read.** The research environment's network policy blocked direct fetches of ai.google.dev, firebase.google.com, platform.openai.com, developers.openai.com, openai.com, learn.microsoft.com, support.google.com, docs.flutter.dev, docs.github.com, elevenlabs.io and apple.com/legal. Facts from those sites came through search-engine extracts of the official pages and are rated **M**. Pages fetched and read directly are rated **H**: developer.apple.com, developer.android.com, cloud.google.com/terms, anthropic.com, support.claude.com, platform.claude.com, microsoft.com/licensing and Flutter's release manifest. Forum and blog material is rated **L**.

## Verified facts

### (A) Live conversation

**Gemini Live**
- "Gemini 3.8 Live" is real. The model ID is `gemini-3.8-live`, and there is also `gemini-3.8-live-extended-thinking`. Both reached general availability on Sept 15, 2026. Input limit is 131,072 tokens. **M** — https://ai.google.dev/gemini-api/docs/models/gemini-3.8-live, https://ai.google.dev/gemini-api/docs/changelog
- The older `gemini-3.1-flash-live-preview` and `gemini-2.5-flash-native-audio-preview-12-2025` are deprecated, with an earliest shutdown of **Nov 17, 2026**. **M** — https://ai.google.dev/gemini-api/docs/deprecations
- Paid pricing per 1M tokens: audio in $3.00 (about $0.005/min), audio out $12.00 (about $0.018/min, thinking tokens included), text in $0.75, text out $4.50. Audio counts as 25 tokens per second. On the free tier, your data may be used to improve Google's products. **M** — https://ai.google.dev/gemini-api/docs/pricing
- Each turn re-bills the accumulated context. **L** (forum only)
- Session limits: audio-only sessions stop at 15 minutes unless context-window compression is on. Individual connections reset after about 10 minutes, and session resumption carries the session across them (resumption tokens last 2 hours). Compression triggers at 80% of the context window by default. **M** — https://ai.google.dev/gemini-api/docs/live-api/session-management
- Ephemeral tokens (Preview, Live API only): by default a token allows 1 minute to start a session and 30 minutes of messaging. A token can lock the model and system instructions on the server. **M** — https://ai.google.dev/gemini-api/docs/live-api/ephemeral-tokens
- Spanish: native-audio models pick the language automatically ("es" is in the list); Cloud docs list es-US. I found no official Castilian voice. **M** — https://ai.google.dev/gemini-api/docs/live-api/capabilities
- Firebase AI Logic supports the Live API on Apple (SDK 12.4.0+), Android (17.1.0+), Flutter (`firebase_ai` 3.1.0+), Web and Unity, so no backend is needed. The feature is still **Preview**. **M** — https://firebase.google.com/docs/ai-logic/live-api, https://firebase.google.com/support/release-notes/ios
  - Firebase's model list still shows only `gemini-3.1-flash-live-preview`; I could not confirm 3.8 Live support there. **M**
  - App Check is auto-enforced from **Nov 2, 2026** and can be delayed until Jan 21, 2027 at the latest. **M** — https://firebase.google.com/docs/ai-logic/app-check
- Spend controls: AI Studio offers a per-project monthly spend cap, but it lags by about 10 minutes and live sessions can overshoot it. **M** — https://ai.google.dev/gemini-api/docs/billing, https://blog.google/innovation-and-ai/technology/developers-tools/more-control-over-gemini-api-costs/

**OpenAI Realtime and GPT-Live**
- `gpt-realtime-2.1`: audio $32 in / $64 out per 1M tokens ($0.40 cached). `gpt-realtime-2.1-mini`: $10 / $20 ($0.30 cached), 128k context. The older `gpt-realtime-mini` is deprecated. **M** — https://developers.openai.com/api/docs/pricing, https://developers.openai.com/api/docs/models/gpt-realtime-2.1-mini
- Audio token rates: user audio is 1 token per 100 ms (600/min) and assistant audio is 1 token per 50 ms (1,200/min). **M** — https://developers.openai.com/api/docs/guides/voice-latency-cost
- GPT-Live-1 (`gpt-live-1`) costs $0.05/min, billed per second. **Backend model and tool tokens are billed on top.** The free tier is not supported. Custom voices are English-only. **M** — https://developers.openai.com/api/docs/models/gpt-live-1, https://openai.com/index/introducing-gpt-live-1-in-the-api/
- Connections: WebRTC is for browser and mobile clients, WebSocket for servers. `POST /v1/realtime/client_secrets` mints `ek_` client secrets with a TTL of 10 seconds to 2 hours (default 10 minutes). The TTL only limits session creation. Send `OpenAI-Safety-Identifier` when minting. Sessions max out at 60 minutes. **M** — https://developers.openai.com/api/docs/guides/voice-webrtc, https://platform.openai.com/docs/api-reference/realtime-sessions/create-realtime-client-secret, https://developers.openai.com/api/docs/guides/realtime-conversations
- Voices: built-ins include marin and cedar (recommended). I found no official Spanish language or voice list for the API. ChatGPT has Mexican-Spanish Live voices, but GPT-Live 1.1 is "coming soon" to the API. **M/L**
- Hard spend limits exist at organization and project level: requests get a 429 once the limit is hit, with some overshoot. Prepaid credit with auto-recharge turned off stops usage when the balance runs out. **M** — https://developers.openai.com/api/docs/guides/spend-limits

**Azure OpenAI**
- Azure Foundry offers `gpt-realtime-2.1` and `gpt-realtime-2.1-mini` over WebRTC, with a generally available ephemeral-token endpoint. **M** — https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/realtime-audio-webrtc, https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/realtime-2
- Classic docs exclude audio models from Azure content filters, so don't count on them for realtime. **M** — https://learn.microsoft.com/en-us/azure/foundry-classic/foundry-models/concepts/content-filter
- Azure budgets only send alerts; they do not stop usage. **M** — https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/tutorial-acm-create-budgets
- The free F0 Speech tier gives 5 audio hours of speech-to-text and 0.5M neural TTS characters per month. **M** — https://azure.microsoft.com/en-us/pricing/details/cognitive-services/speech-services/

**Anthropic**
- There is no realtime speech-to-speech API; voice means a speech-to-text → Claude → text-to-speech chain. **M**
- Claude Haiku 5.5 costs $0.10 / $0.50 per 1M tokens (prompts up to 100k). **H** — https://platform.claude.com/docs/en/about-claude/pricing
- The Console spend limit stops requests at the cap. **H** — https://platform.claude.com/docs/en/api/rate-limits

### (B) Build and distribution

**iOS (all H unless marked)**
- Free Personal Team, quoting Apple: "up to 10 App IDs, which expire after 7 days… up to 3 devices… up to 3 apps per device. Provisioning profiles… expire 7 days from issuance." — https://developer.apple.com/support/compare-memberships/
- The Apple Developer Program is US$99 per year and includes 25 Xcode Cloud compute hours per month. — https://developer.apple.com/programs/whats-included/, https://developer.apple.com/xcode-cloud/
- TestFlight: up to 100 internal testers (App Store Connect users) and 10,000 external testers (first build needs review). Builds become unavailable after 90 days. — https://developer.apple.com/help/app-store-connect/test-a-beta-version/testflight-overview/
- **TestFlight terms say children under 13 may not use TestFlight.** **M** — https://www.apple.com/legal/internet-services/itunes/testflight/sren/terms.html
- Ad Hoc / registered devices: 100 devices per product family per membership year. The count only restores at renewal; disabling a device doesn't free a slot. — https://developer.apple.com/help/account/devices/devices-overview/
- Installing an .ipa requires Developer Mode on the device. Apple's documented ways to collect device IDs and install use Device Hub, Finder or Apple Configurator, all Mac tools. — https://developer.apple.com/documentation/xcode/distributing-your-app-to-registered-devices
- Xcode Cloud quote: "You need to configure your first Xcode Cloud workflow in Xcode." So it needs a Mac at least once. — https://developer.apple.com/documentation/xcode/configuring-your-first-xcode-cloud-workflow
- Since Apr 28, 2026, uploads must be built with Xcode 26 / the iOS 26 SDK. — https://developer.apple.com/news/upcoming-requirements/
- xcodebuild can sign and upload using an App Store Connect API key (`-authenticationKeyPath/ID/IssuerID` plus `-allowProvisioningUpdates`). — https://developer.apple.com/videos/play/wwdc2021/10204/
- GitHub-hosted macOS runners: about $0.062/min. The Free plan includes $12/month of runner usage (about 190 macOS minutes) for private repos. Standard runners are free for public repos. A `macos-26` label exists. **M** — https://docs.github.com/en/billing/reference/actions-runner-pricing, https://docs.github.com/en/billing/reference/product-usage-included

**Android (all H unless marked)**
- Sept 30, 2026: protections begin only for installs **from participating stores** in Brazil, Indonesia, Singapore and Thailand, on certified devices running Android 7+. Global expansion is planned for **2027**. — https://developer.android.com/developer-verification
- ADB is exempt. Quote: "Unregistered apps can be sideloaded with Android Debug Bridge (adb) or advanced flow." The FAQ adds that the 24-hour advanced-flow wait does not apply to ADB. — https://developer.android.com/blog/posts/android-developer-verification-building-a-safer-ecosystem-together, https://developer.android.com/developer-verification/guides/faq
- Advanced flow: a 24-hour delay, then you choose to keep it on for 7 days or indefinitely. **M** — https://support.google.com/android/answer/17588095
- Limited-distribution accounts are free with no ID check, but the device cap conflicts: the guide says **50**, while the FAQ and blog say **20**. A full Android Developer Console account is $25. — https://developer.android.com/developer-verification/guides/limited-distribution

**Flutter**
- Current stable is **3.47.9** (Oct 29, 2026, Dart 3.13.7). 3.50 is in beta (3.50.0-0.4.pre). **H** — https://storage.googleapis.com/flutter_infra_release/releases/releases_macos.json
- `flutter build ipa` on GitHub macOS runners with an App Store Connect API key or fastlane, then a TestFlight upload, is a well-established pattern. **M/L** — e.g. https://github.com/marketplace/actions/upload-app-to-testflight

## Corrections to the research doc
1. **Section 1 and step 9.6:** recommending Gemini Live breaks Google's terms. Both Gemini API and Google Cloud generative-AI terms forbid apps "directed towards or likely to be accessed by individuals under the age of 18". Firebase AI Logic inherits those terms. Drop Gemini for the kids' conversation feature.
2. **Section 6** ("for personal family use it is not a concern"): wrong for provider terms. They apply no matter whether the app is published. OpenAI also asks for zero data retention before processing under-13 personal data, and ElevenLabs bars minor-directed apps.
3. **Section 5:** GPT-Live 1 at $0.05/min is real, but backend model tokens are extra, so it is not the cheapest option. The correct mini ID is `gpt-realtime-2.1-mini`. The $0.18–0.46/min estimate is unverified.
4. **Section 8:** TestFlight cannot be used by a child under 13's Apple Account. Free provisioning also caps you at 3 devices and 3 apps per device. "Needs a Mac" is only partly true: GitHub macOS runners can build and upload to TestFlight, but Xcode Cloud's first setup needs a Mac.
5. **Android:** enforcement covers only participating-store installs in the four countries. The limited-distribution cap may now be 50, not 20.
6. **Section 2** (parent using Claude app voice mode with the child): Anthropic's consumer apps are restricted to users 18 and over, so present this as parent-led only.
7. **Sections 3 and 9.3:** pre-generating audio with ElevenLabs or Gemini for a kids' app is a terms gray area. Azure TTS or on-device voices avoid the question.

## Provider terms for minors

| Provider | Allows an app used by under-13s? | Conditions | Quote | URL |
|---|---|---|---|---|
| Google Gemini API / Firebase AI Logic | **No**, and not under-18s either | Parental supervision doesn't change this | "You must be 18 years of age or older to use the APIs… won't use the Services as part of a website, application… directed towards or is likely to be accessed by individuals under the age of 18" (M) | https://ai.google.dev/gemini-api/terms |
| Google Cloud / Vertex | **No** | Same rule | §20(d): "Customer will not, and will not allow End Users to, use a Generative AI Service as part of a website, Customer Application, or other online service that is directed towards or is likely to be accessed by individuals under the age of 18." (H) | https://cloud.google.com/terms/service-terms |
| OpenAI API | **Conditionally**; impractical for a hobbyist | Parental consent. For under-13 data, zero data retention first (needs Sales approval; the realtime endpoint is eligible). Add filters, monitoring and an AI disclosure | Agreement: customer won't "allow minors to use our Services without consent from their parent or guardian". Guidance: "should not use OpenAI services to process any personal data of children under 13… without first implementing zero data retention" (M). A usage-policy update takes effect Nov 20, 2026 | https://openai.com/policies/services-agreement/, https://developers.openai.com/api/docs/guides/safety-checks/under-18-api-guidance |
| Anthropic API | **Yes, with safeguards** | Age verification, moderation, monitoring, a child-safety system prompt, AI disclosure, COPPA compliance. No voice API | "Products serving minors… must comply with the additional guidelines outlined in our Support article and all applicable laws" (H; AUP effective Nov 12, 2026) | https://www.anthropic.com/legal/aup, https://support.claude.com/en/articles/9307344 |
| Microsoft Azure (OpenAI, Speech) | **No age clause found** | Code of Conduct (child exploitation bans). Abuse monitoring "will temporarily store Input and Output Content". The Pronunciation Assessment note names children's language apps as a use case | No minors clause in the Product Terms or the Generative AI Services terms I searched (H; absence of a clause, so medium confidence) | https://www.microsoft.com/licensing/terms/productoffering/MicrosoftAzure/MCA |
| ElevenLabs | **No**, without written approval | Account holders 18+. No voice data from under-18s | Apps "directed at individuals under 18 are prohibited unless ElevenLabs has assessed and approved them in writing" (M) | https://elevenlabs.io/use-policy |

## Recommended live-conversation architecture
- **Provider (preferred):** a turn-based, push-to-talk chain of Azure speech-to-text (es-MX/es-ES), then Claude Haiku 5.5, then Azure neural TTS.
  - Every reply exists as text before it is spoken, so it can be moderated first. That is something speech-to-speech cannot do reliably.
  - Both providers' terms allow this audience: Anthropic permits minors with safeguards, and Microsoft has no age bar.
  - It reuses the Azure resource already planned for pronunciation scoring.
- **If full-duplex conversation is wanted:** Azure OpenAI `gpt-realtime-2.1-mini` over WebRTC. It is the same model and price as OpenAI's own, but under Microsoft's terms. Run your own transcript guardrails: the OpenAI Agents SDK checks the transcript every 100 characters and interrupts playback when a check trips. Avoid OpenAI direct (zero-data-retention gate) and Gemini (18+).
- **Auth:** no API keys in the app. A tiny serverless function, protected by a per-device secret plus a parent PIN, mints short-lived tokens. Azure realtime gets ephemeral tokens; Azure Speech's short-lived tokens are from memory and not re-verified. Claude calls go through the function. The function also enforces all caps.
- **Safety:**
  - A fixed lesson-scoped role-play system prompt: Spanish only, ages 6–10, refuse other topics, never ask for names, address or school.
  - No tools, web search or images.
  - Check text against a moderation or keyword list before TTS speaks it.
  - Disclose "I'm a computer helper".
  - Parent-present mode: a session only starts after the parent's PIN.
  - Hard 10-minute timer that closes the connection on the client and in the token minter.
  - Store no transcripts or audio. Don't enable Gemini-style session resumption; Azure keeps data briefly for abuse monitoring.
- **Budget:**
  - Provider side: Anthropic Console spend limit (hard stop). Azure budget alerts plus a low deployment rate quota, since Azure has no hard cap.
  - App side (authoritative): a minutes-per-day and dollars-per-month counter in the token minter that refuses new sessions once reached.
- **Cost estimates for 10 minutes a day:**
  - The chain: about $0–1 per month. Speech-to-text and TTS largely fit the F0 free tier (roughly 1.5 h of child speech and about 100k characters a month, shared with pronunciation scoring). Claude costs about $0.25 per month.
  - `gpt-realtime-2.1-mini`: about $0.16–0.25 per session ($0.016–0.025/min), or $5–8 per month with good caching, assuming 3 min of child speech and 4 min of output. It could reach about $1.50 per session if context isn't cached, so cap it at about $15 per month.
  - GPT-Live-1: at least $0.50 per session plus backend tokens.

## Recommended distribution path
- **(a) Mac + iPad:** prototype with the free Personal Team (rebuild every 7 days). Then pay the $99 per year and install development or Ad Hoc builds through Xcode or Device Hub, with Developer Mode on the iPad. These last about a year and need no TestFlight. Use TestFlight only if the iPad's App Store account belongs to an adult. Xcode Cloud (25 h/month) is optional.
- **(b) No Mac + iPad:** pay the $99 per year. Use Flutter 3.47 with GitHub Actions on `macos-26` (free if the repo is public), `flutter build ipa`, and an App Store Connect API key via fastlane or xcodebuild to upload to TestFlight. Install on the iPad under a **parent's** Apple Account, not the child's. Schedule a monthly rebuild to stay inside the 90-day expiry. Ad Hoc is impractical here because device-ID collection and install tooling are Mac-only.
- **(c) Android tablet:** develop on any OS and install with `adb install` or `flutter install`. ADB is exempt from verification and skips the 24-hour wait, both now and after the 2027 global rollout. Optionally register a free limited-distribution account for cable-free installs.

## Open questions / could not verify
- Whether Firebase AI Logic supports `gemini-3.8-live` yet (moot given Google's terms).
- An official Spanish voice list for OpenAI realtime / GPT-Live in the API.
- Whether Azure content filters apply to gpt-realtime.
- Exact Azure Speech paid rates.
- Gemini's per-turn context re-billing (forum claim only).
- The limited-distribution device cap (20 vs 50).
- Whether an individual can get OpenAI zero data retention.
- Installing Ad Hoc builds over the air without a Mac.
- Whether COPPA applies to a non-commercial family app (legal question).
- Two policy updates arrive this month: re-check Anthropic's AUP (effective Nov 12, 2026) and OpenAI's usage policies (Nov 20, 2026).
- Several facts are rated M only because the network policy blocked direct fetches; see the note at the top.
