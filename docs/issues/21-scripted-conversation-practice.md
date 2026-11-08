---
planned_number: 21
title: "Conversation practice (optional): scripted, branching role-play dialogues, fully offline"
type: Feature
labels: [phase-5-conversation, "area: speech", "area: content"]
parent: 1
---

**Phase 5 · Size M–L · Depends on: #5 (dialogues), #7 (audio), #10, #15, #16 · Optional, after the MVP**

## Goal
Short role-plays (3–6 minutes) tied to a lesson, where a friendly character talks with the child in simple Spanish and reacts to what the child says. Examples: meeting a new friend, counting toys, ordering at a taquería, "Simón dice", "What are you wearing?".

## Decision: no LLM, no Claude API
- **Owner decision (2026-11-08): the Claude API is not used.** No other LLM is planned either.
- Conversations are **authored dialogue trees**:
  - every character line is **pre-generated audio** (#7);
  - the child's answer is checked **on the tablet** by Vosk grammar mode (#16).
- Why this fits ages 6–10:
  - **Safe by construction:** the character can only say lines a parent has heard and approved.
  - **Offline, instant and free:** no server, no per-minute cost, no transcripts leaving the device.
  - **Pedagogically sound:** at this level the child's useful answers are a small, known set (A1 phrases from the unit), which is exactly what grammar-constrained recognition is good at.
- **If free-form chat is ever wanted:** that would need its own terms review (#24). The only terms-clean option found was Azure OpenAI under Microsoft's terms. Out of scope for this plan.

## Dialogue format (authored in content, validated by #6)
```yaml
dialogues:
  - id: u01_new_friend
    unit: u01
    character: mascot
    goal: "Greet, say your name, say how you are"
    sticker: friend_badge
    start: n1
    nodes:
      n1:
        say: ["¡Hola! Me llamo Lupe. ¿Cómo te llamas?"]   # 1–3 variants, each pre-generated
        expect:
          - { answers: ["me llamo *", "*"], slot: name, next: n2 }   # wildcard: any speech counts
        hint: { say: "Di: Me llamo…", choices: [] }
      n2:
        say: ["¡Mucho gusto, {name}! ¿Cómo estás?"]       # {name} uses the pre-generated name lines
        expect:
          - { answers: ["bien", "muy bien", "estoy bien"], next: n3_good }
          - { answers: ["mal", "más o menos", "cansado", "cansada"], next: n3_meh }
        hint: { say: "¿Bien o mal?", choices: [fluent/smile, fluent/sad] }
      n3_good: { say: ["¡Qué bien! ¡Adiós!"], end: success }
      n3_meh:  { say: ["¡Oh! Un abrazo. ¡Adiós!"], end: success }
```
**Rules**
- Each node has:
  - 1–3 phrasing variants, so replays don't feel identical;
  - one or more expected answer groups, each leading to a next node;
  - a **hint**: replay plus a simpler question, and optional picture choices the child can tap *or* say.
- **Wildcard answers** (`*`) accept any detected speech. Use them for open slots such as the child's own name, which may be outside the Vosk vocabulary.
- **Slots** fill from content, e.g. foods at the taquería. Prefer whole pre-generated lines per combination. Fall back to clip sequences (`"¿Quieres"` + `"un taco"` + `"?"`) only where the combinations explode.
- **Endings:** every path ends in `success` within about 8 turns. The validator in #6 checks:
  - every node is reachable;
  - every non-end node has a hint;
  - no dead ends;
  - every line has approved audio.

## Runtime
1. The character's line plays (#10); the mascot animates.
2. The mic opens (#15), and the child answers.
3. Vosk runs with a grammar built from **all** answers expected at this node, plus `[unk]` (#16). The matcher (#16) picks the answer group.
4. **Branching:**

   | Result | What happens |
   |---|---|
   | Match | Go to that branch |
   | No match, 1st time | Play the hint (simpler question, picture choices) |
   | No match, 2nd time | The character models a good answer ("Puedes decir: *muy bien*"), then the dialogue continues on the default branch |

   The child is never stuck, and never fails.
5. **Optional stars:** when online scoring is on (#17), the matched answer can also get Azure stars. Off by default in dialogues, to keep the flow fast.
6. **Ending:** the dialogue ends with a sticker (#13). The SRS gets `say` credit for target phrases used correctly on the first try (#12).

## Parent controls (#14)
- On/off per child.
- Whether dialogues appear in the session "Use it" step (#11) or only from the home screen.
- English hints on/off.

## Privacy
- Fully on-device. Audio is kept only in memory (#15).
- Nothing new leaves the tablet. The only exception is optional Azure scoring, which follows #17's rules.

## Authoring effort
- About 1–2 dialogues per unit; each one is roughly 6–12 nodes and 20–40 audio lines.
- Write them alongside the unit content (#5). One review covers the text and the approved audio.

## Tasks
- [ ] Dialogue schema plus validator rules (#6), including the graph checks
- [ ] Dialogue runner (pure Dart, `domain/`): node state, answer matching via the #16 matcher, hint and model-answer fallback, slots
- [ ] Dialogue screen: mascot, speech bubble with an emoji cue, mic button, picture choices
- [ ] First dialogue: Unit 1, "Meet a new friend". Then Units 2, 6, 8 and 9
- [ ] Playtest with both age bands (#25)

## Acceptance criteria
- [ ] Unit 1 dialogue works end to end in **airplane mode** on the tablet
- [ ] Under 1 s from the end of the child's speech to the character's next line
- [ ] Every path reaches `success`; the validator rejects broken graphs (tests)
- [ ] A 6-year-old completes a dialogue without adult help (playtest)
