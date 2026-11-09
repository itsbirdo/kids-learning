---
planned_number: 14
title: "Parent area: PIN gate, child profiles, settings, progress dashboard, backup"
type: Feature
labels: [phase-2-core-app, "area: app"]
parent: 1
---

**Phase 2 · Size M · Depends on: #9, #12 · Extended by: #17, #18, #19, #20, #21**

## Goal
Parents control everything that isn't learning: profiles, limits, online features, and visibility into progress. Kids can't get in.

## Gate
- Set a 4–6 digit PIN on first launch; entry needs a 3-second hold, then the PIN.
- Lock again after 2 minutes of inactivity.
- Forgotten PIN: reset needs a long-press plus answering an adult maths question, and wipes only the PIN.

## Settings

**Per child**
| Setting | Options (default) |
|---|---|
| Name, avatar, age band | 6–7 / 8–10 |
| Session length | 10 / **12** / 15 min |
| New words per session | auto by age (3–4 / 4–6) or fixed |
| English instructions | full → **fading** → off |
| Captions | **off** (ages 6–7) / on |
| Speaking practice | off / practice only / **scored** (needs #16/#17) |
| Scoring strictness | −10 … +10 (default 0; see #17, #19) |
| Daily limit | none / 15 / 20 / 30 min. Soft stop: finish the current activity, then wrap up |

**Family**
- Online scoring on/off (#17).
- Gateway pairing: device token via QR code or paste (#18).
- Custom word lists (#20) and dialogue settings (#21), when built.
- Backup and restore.
- Acknowledgements and licences (#8).
- A plain-language privacy summary (#24).

## The grown-up turn (R21 in [`docs/learning-methodology.md`](../learning-methodology.md))
Young children learn language far better from live, responsive interaction than from recordings. This includes Kuhl, Tsao & Liu 2003 and Roseberry, Hirsh-Pasek & Golinkoff 2014. Harvard's Center on the Developing Child calls it "serve and return". In Romeo et al. 2018 (Harvard/MIT), back-and-forth conversational turns predicted children's language-related brain function; the number of words heard did not. Brief guidance increases parents' back-and-forth with their children (Leech & Rowe 2021). The evidence is strongest for infants and toddlers, so treat this as cheap insurance for ages 6–10, not a proven requirement.

- **At the end of each session:** a card on the wrap-up screen (#11, #13) suggests **one 5-minute routine**, with today's words and phrases filled in. The parent doesn't need to speak Spanish; each card has model audio.
  - **"Teach me":** the child teaches the parent today's words and gestures. This gives the child output, retrieval and real turn-taking.
  - **TPR swap:** the child gives Spanish commands ("¡Salta!", "Toca tu nariz") to the parent or a sibling.
  - **Chunk of the week:** 2–3 phrases to use in daily routines ("¡Buenos días!", "¿Tienes hambre?"). Ask, then **wait** for the reply.
  - **Story talk:** open today's story, point and ask "¿Qué es?", "¿Dónde está…?". Link it to the child's life ("¿Tienes un perro?").
  - **Prompt, don't lecture:** after a mistake, ask "¿Cómo se dice…?" or replay the model, and praise the attempt.
  - **Dialogue swap:** the parent reads role A from the card, and the child answers as role B, then they swap (#11 core-dialogue stages).
- **Dismissing the card:** the parent can tap "we did it" or "skip". Nothing is scored, and the child is never penalised.
- **Unit parent card:** the parent area shows the current unit's parent card. It has the can-do goal, the chunk of the week, the dialogue script with audio, and offline ideas (#5).
- **Speech-result override:** in parent-present mode, a parent can mark a speaking attempt "that was right". It counts as correct for the SRS, and the override is logged so #19 calibration can use it.

## Progress dashboard (per child)
- Words recognised and words the child can say, per unit (#12 definitions); can-do checklist per unit.
- Sessions and minutes this week, as a simple bar chart.
- Words that need practice, with a play button for each model clip.
- Recent speaking stars.
- The current unit's parent card (above).
- A **"listen again" button** that starts the audio-only replay of this week's dialogues, story and chants (#11).
- **Progress described as "I can…" goals**, never as "fluency". Example: "Can understand 40 animal and food words; can say 15; can do the greeting dialogue." This matches realistic goals for 10–15 min/day (methodology §6).
- Azure and gateway usage this month vs the free quota (#17, #18).

## Recordings (privacy-sensitive, default OFF)
- If a parent turns this on: keep the child's last 3 attempts per word, **on the device only**, so the parent can listen to progress.
- Auto-delete after 7 days. Excluded from backups.

## Backup and restore
- **Export:** progress JSON (profiles, cards, attempts, stickers, settings; **no audio, no tokens**) through the Android share sheet. Restore with import.
- **Auto Backup:** configure Android `fullBackupContent` / `dataExtractionRules` to include the DB and exclude recordings and secure storage.
- **Signing key:** updates must use the same key, or progress is lost (#22). Export before any reinstall.

## Tasks
- [ ] Gate (hold plus PIN), lock and reset flow
- [ ] Profiles CRUD and per-child settings
- [ ] Dashboard queries and screens
- [ ] Export/import with a versioned JSON format, plus a round-trip test
- [ ] Android backup rules
- [ ] Acknowledgements screen fed by #8 data
- [ ] Grown-up turn cards (wrap-up screen) and unit parent cards, filled from content (#5, #6)
- [ ] Parent override for speaking results in parent-present mode, logged for #19

## Acceptance criteria
- [ ] A child tapping randomly for 2 minutes doesn't get past the gate (manual test)
- [ ] Settings persist and take effect at the next session
- [ ] Export → wipe → import restores identical progress (automated test)
