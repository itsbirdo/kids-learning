---
planned_number: 21
title: "Live conversation practice (optional): supervised role-plays via Azure STT → Claude → Azure TTS"
type: Feature
labels: [phase-5-conversation, "area: speech", "area: safety"]
parent: 1
---

**Phase 5 · Size L · Depends on: #5 (scenarios), #15, #17, #18, #24 · Optional, after the MVP**

## Goal
Short role-plays (10 minutes at most), started by a parent and tied to a lesson, in simple Spanish with a friendly AI character. Examples: meeting a new friend, ordering at a taquería, "Simón dice".

## Provider choice (see #24 for the terms review)
| Option | Verdict |
|---|---|
| Gemini Live / Firebase AI Logic | **Not allowed.** The terms bar apps "likely to be accessed by individuals under the age of 18" |
| OpenAI Realtime / GPT-Live direct | **Impractical.** Needs parental consent, plus zero data retention before processing under-13 data, which needs sales approval |
| **Azure STT → Claude → Azure TTS (chosen)** | Microsoft: no age clause found. Anthropic: allows products serving minors *with safeguards*. Every reply exists as **text before it's spoken**, so it can be checked first — speech-to-speech can't guarantee that |
| Azure OpenAI `gpt-realtime-2.1-mini` (full duplex) | Possible later (about $0.016–0.025/min). Needs our own transcript guardrails. Not planned |

## Flow (push-to-talk, turn-based)
```
child taps mic → Utterance (#15)
  → Azure STT REST (es-MX, token from #18, no assessment header) → child_text
  → gateway POST /v1/chat/turn {scenario_id, history (held by the app), child_text}
      → input checks: length, blocklist, empty → canned nudge
      → Claude Messages API (system prompt = character + scenario + unit vocab + safety rules)
      → output checks: blocklist, Spanish-only, length, no personal-info questions → safe fallback line if any fail
      → counters (turns, minutes, estimated $)
  ← {say, emoji, done}
  → Azure TTS (gateway /v1/tts, house voice) → play; show the emoji cue and mascot animation
```
- The **history lives only in app memory** and is discarded when the session ends. The gateway is stateless apart from counters.
- **Latency target:** under 3 s median from the end of the child's speech to the start of the reply audio. Measure each stage.

## Scenarios (authored in content, #5)
Each scenario has:
- `goal` and the unit vocabulary
- 3–5 target exchanges
- a success condition (e.g. "child ordered two foods"), which earns a sticker
- an opening line
- a fallback hint list

## System prompt rules
- **Persona:** a friendly cartoon helper that **says it's a computer helper**.
- **Language:** Spanish only, A1 level, using the unit vocabulary. At most 12 words per sentence and 2 sentences per turn. **One question at a time.**
- **Errors:** recast them gently; never lecture.
- **Struggling child:** if the child is silent, offer two choices. If the child speaks English, allow a short English hint (parent setting), then go back to Spanish.
- **Never** ask for or repeat personal information: full name, address, school, phone, location, photos.
- **Stay on the scenario.** Redirect off-topic requests back to it. No scary, violent, romantic or commercial content, and no links.
- **Ending:** close warmly when the goal is met or time is up.

## Claude API notes (check current docs at build time)
- **Output:** structured outputs (`output_config.format`) for `{say: string, emoji: string, done: boolean}`.
- **Model:** a gateway env var `CHAT_MODEL`. The owner decides after a latency and quality test.

  | Model | Price per MTok (input / output) | Notes |
  |---|---|---|
  | `claude-haiku-5-5` | $0.10 / $0.50 | Lowest cost and latency |
  | `claude-opus-5-5` | $4 / $20 | Anthropic's default recommendation; higher quality |

- **Effort:** low (`output_config.effort: "low"`); leave adaptive thinking at its default.
- **Don't send** `temperature`, `top_p` or `top_k`; they are rejected from API version 2026-10-21. No assistant prefill.
- **Refusals:** handle `stop_reason: "refusal"` with a friendly fallback line. On the Opus tier, consider server-side fallbacks.
- **Caching:** use prompt caching for the stable system prompt, and check `usage.cache_read_input_tokens`. Short prompts may fall below the minimum cacheable length.
- **Spend:** set a Console **spend limit** (a hard stop) in addition to the gateway caps.
- **Minors policy:** Anthropic's usage policy requires products serving minors to follow its minors guidance (support article 9307344: age-appropriate safeguards, moderation, monitoring, AI disclosure) and applicable law. **Re-read it before enabling;** an updated usage policy takes effect 2026-11-12.

## Safety and parental controls
- A parent PIN starts each session. "Parent present" mode is recommended and shows the live transcript on screen.
- **Hard limits,** enforced in both the app and the gateway: a 10-minute timer, a maximum number of turns, and daily minutes.
- **Nothing stored:** no transcripts or audio. The parent sees only the scenario, the turn count and success.
- A **kill switch** in the gateway (#18).
- The **red-team checklist** in #24 must pass before the feature is turned on.

## Cost (estimates; daily 10-minute session ≈ 20 turns)
| Item | Estimate |
|---|---|
| Haiku tier | About $0.01 per session |
| Opus tier | About $0.10–0.30 per session; less with caching. About $3–9 per month per child |
| Azure STT/TTS | Shares the F0 quota with scoring. Two kids plus conversation may need S0 (about $1 per audio hour, *verify*) |

## Tasks
- [ ] Scenario format in content (#6) and the first scenario (Unit 1, "Meet a new friend")
- [ ] Gateway `/v1/chat/turn`: prompt assembly, Claude call, input/output checks, counters, tests with a mocked API
- [ ] App conversation screen: push-to-talk, transcript in parent-present mode, timer, end-of-session sticker
- [ ] Latency instrumentation and a model-tier comparison (owner picks)
- [ ] Run the #24 red-team checklist and record the results

## Acceptance criteria
- [ ] Scenario 1 works end-to-end on the tablet within the latency target
- [ ] The red-team checklist passes: personal-info probes, off-topic, English-only child, silence, rude words, "ignore your instructions"
- [ ] Caps and the kill switch are verified; no transcript is persisted anywhere
