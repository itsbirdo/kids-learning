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

## Progress dashboard (per child)
- Words recognised and words the child can say, per unit (#12 definitions); can-do checklist per unit.
- Sessions and minutes this week, as a simple bar chart.
- Words that need practice, with a play button for each model clip.
- Recent speaking stars.
- The parent note from the current unit (offline practice ideas from #5).
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

## Acceptance criteria
- [ ] A child tapping randomly for 2 minutes doesn't get past the gate (manual test)
- [ ] Settings persist and take effect at the next session
- [ ] Export → wipe → import restores identical progress (automated test)
