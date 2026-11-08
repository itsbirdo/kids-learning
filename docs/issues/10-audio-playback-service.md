---
planned_number: 10
title: "Audio playback service (clips, slow replay, sequences, interruptions)"
type: Feature
labels: [phase-2-core-app, "area: app"]
parent: 1
---

**Phase 2 · Size S–M · Depends on: #7 (clips), #9 · Blocks: #11**

## Goal
Instant, reliable playback of bundled and runtime-generated clips. Activities can wait for a clip to finish before moving on.

## Spec
**`ClipPlayer` (interface in `platform/`, implemented with `just_audio`)**
- `play(clipId, {variant: normal | slow})` returns a Future that completes when the clip ends.
- `playSequence([...], gapMs)`, e.g. word → pause → word.
- `preload(clipIds)` warms a small cache for the next activity.
- `stop()` is called on navigation, pause or backgrounding.
- `playSfx(id)`: soft chime or sparkle at about −20 LUFS, quieter than speech. **No buzzers or "wrong" sounds.**
- Runtime clips from #20 (mp3 in the app documents folder) use the same API.

**Replay buttons**
- A big replay button on every screen replays the last prompt.
- A second "turtle" button plays the slow variant.

**Interruptions**
- Handle audio focus: pause for calls and other apps; pause when the app is backgrounded.
- Never record while a clip is playing. Recording waits for the clip to end plus 150 ms (#15).

**Fallbacks**
- A missing clip falls back to `SystemTts` (#20) and a warning is logged.
- Release builds should have no missing clips; `kl validate` checks this.

## Targets
- Under 150 ms from tap to sound for preloaded clips on the tablet.
- No overlapping speech: a new prompt stops the previous one.

## Tasks
- [ ] `ClipPlayer` with `just_audio`, plus a fake for tests
- [ ] Preload cache sized to the next 1–2 activities
- [ ] Audio focus and lifecycle handling
- [ ] SFX set (licence-checked; CC0 preferred)

## Acceptance criteria
- [ ] Integration test on the device: play, sequence, stop on navigation, and resume after a simulated interruption
- [ ] Latency target met on the kids' tablet (measured and noted in `docs/hardware.md`)
