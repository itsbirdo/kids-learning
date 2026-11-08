---
planned_number: 24
title: "Privacy, provider terms for minors, licences and child-safety checklist"
type: Task
labels: [cross-cutting, "area: safety"]
parent: 1
---

**Cross-cutting · Size S–M (then re-checked at each phase) · Gates: #7 provider choice, #17 online scoring, #21 dialogue content**

**Owner decision (2026-11-08):** no Claude API, and no LLM APIs at all. The only cloud provider in the plan is **Microsoft Azure Speech** (scoring, TTS), plus ElevenLabs for lesson audio only if this review clears it.

## Why
The research notes said privacy is "not a concern" for personal family use. That holds for COPPA's *publishing* duties. **API providers' terms still apply to how we use their services**, whether or not the app is published.

## Provider terms for minors (checked 2026-11-08; re-check before each phase)
| Provider | Use by a 6–10-year-old under parental supervision? | Key wording / conditions | Our use |
|---|---|---|---|
| Google Gemini API / Firebase AI Logic | **No.** Users must be 18+, and the services can't be used in an app "directed towards or… likely to be accessed by individuals under the age of 18" | Supervision doesn't change this. Whether pre-generated offline clips are covered is unanswered by Google | **None** (no Gemini TTS, no Gemini Live, no Gemini images) |
| Google Cloud / Vertex generative AI | **No.** §20(d): the same under-18 rule | | None |
| OpenAI API | **Conditionally.** Parental consent required; for under-13 personal data, zero data retention must be in place first (needs sales approval) | Impractical for a hobbyist | None |
| Anthropic API | Yes, with safeguards ("Products serving minors… must comply with the additional guidelines…") | Age-appropriate safeguards, moderation, monitoring, AI disclosure | **None** (owner decision: no Claude API) |
| **Microsoft Azure Speech** | **No age clause found** in the Product Terms (absence of a clause, so medium confidence). The pronunciation assessment transparency note names children's language apps as a use case | Code of Conduct | Scoring (#17), lesson TTS (#7), custom-word TTS (#20) |
| ElevenLabs | **No, without written approval.** Apps "directed at individuals under 18 are prohibited unless ElevenLabs has assessed and approved them in writing"; account holder 18+; no under-18 voice data | Is a parent pre-generating static clips for home use an "app directed at minors"? Unclear | Only if this review concludes it's fine, or approval is obtained (#7) |

**Decision to record here:** the provider set, plus the date and links of each terms check.

## Data-flow inventory (→ `docs/privacy.md`)
| Data | Where it goes | Retention | Notes |
|---|---|---|---|
| Progress, attempts (no audio), settings | Device SQLite | Until deleted; parent export | Auto Backup to the parent's Google account, if enabled |
| Child audio for scoring | Azure Speech over HTTPS | Not logged by default. **Never** set `storeAudio` or enable audio logging | Kept only in memory on the device by default |
| Parent-enabled recordings | Device only | Auto-deleted after 7 days; excluded from backup | Default off (#14) |
| Calibration recordings | Family computer only | Parent's choice | **Never** in the repo or CI (#19) |
| Dialogue answers (#21) | **Device only** (Vosk on the tablet) | Not stored | Optional Azure stars follow the scoring row above |
| Custom words typed by a parent (#20) | Gateway → Azure TTS | Not logged by the gateway | Text only; no child data |
| Kids' first names | `content/local/family.yaml` (gitignored); sent to the TTS provider once at generation | | Consider nicknames |
| Analytics, ads, crash SDKs | **None** | | |

## Repo hygiene
- Decide whether the GitHub repo stays **private**. Recommended if it ever contains the family's generated name clips or exports.
- `.gitignore` and a CI check: fail if `*.wav` or `content/local/**` is committed outside test fixtures.

## Licences to track (→ Acknowledgements screen, #8/#14)
| Component | Licence | Obligation |
|---|---|---|
| Fluent Emoji | MIT | Notice + licence text |
| Vosk model `small-es-0.42` | Apache-2.0 | Notice |
| espeak-ng, `piper_phonemize` | **GPL-3.0** | Only if #20 tier 4 is built. Fine at home; must be replaced before any publishing |
| Piper voices | Per voice (some datasets are restrictive) | Check each voice's model card |
| ElevenLabs (if used) | Free plan: attribution, non-commercial | Paid plan for commercial use |
| Fonts, SFX | OFL / CC0 preferred | Notice |

## If we ever publish (not planned)
- **COPPA** (amended rule, compliance date 2026-04-22): audio of a child's voice is personal information. There is a narrow exception for audio used only to answer the request and then deleted.
- Google Play Families policy / Apple Kids category: parental gates, no third-party analytics.
- Replace GPL components; get commercial licences; redo every terms review.
- *This is not legal advice.*

## Dialogue content checklist (each dialogue in #21, before release)
There is no AI in the conversation feature, so the character can only say approved lines. The review covers the script itself.
- [ ] No line asks for personal info beyond a first name (no school, address, location, photos)
- [ ] Tone is warm. No scary, mocking or commercial content. Cultural references were checked by the Spanish-speaking reviewer
- [ ] A child who is silent, speaks English or babbles always reaches a hint, then a modelled answer, then `success`. No loops (validator, #6)
- [ ] Every line's audio was approved by a parent (#7)
- [ ] Nothing persisted, checked in app storage after a dialogue

## Acceptance criteria
- [ ] `docs/privacy.md` written; provider decisions recorded with dates
- [ ] Repo visibility decided; the CI hygiene check is in place
- [ ] Re-check dates noted for each phase gate (#7, #17, #21)
