---
planned_number: 15
title: "Microphone capture: kid-friendly recording, endpointing, 16 kHz PCM utterances"
type: Feature
labels: [phase-3-speaking, "area: speech", android]
parent: 1
---

**Phase 3 · Size M · Depends on: #4 (UX findings), #9, #10 · Blocks: #16, #17, #19, #21**

## Goal
Record one clean utterance per attempt in a form both the on-device check (#16) and Azure scoring (#17) can use. Record once and use it twice.

## Spec
**Capture**
- `record` package with `pcm16bits`, **16 kHz mono**, streaming.
- Prefer the Android `VOICE_RECOGNITION` audio source, which avoids aggressive AGC and noise suppression. Check that `record` exposes the source on Android *(verify)*; otherwise add a small native tweak.

**Interaction (decided in #4)**
- **Default: tap to talk.** The child taps the big mic. A "listening" animation and live level meter show. Recording stops automatically after 1.0–1.5 s of trailing silence, or at the maximum length (words 5 s, phrases 8 s).
- **Option:** hold-to-talk (parent setting).
- **No speech:** after a 4 s initial silence, play "No te escuché…" plus a replay prompt. This is *not* counted as an attempt.

**Endpointing**
- Energy-based voice activity detection with an adaptive noise floor (sample about 300 ms of room noise before the start chime).
- Later option: Silero VAD via sherpa-onnx.

**Echo guard**
- Never record during playback. Start after the clip ends plus 150 ms (#10).

**Output**
```dart
class Utterance {
  final Uint8List pcm16;   // trimmed, 16 kHz mono
  final int durationMs;
  final double peakDb, rmsDb;
  Uint8List toWav();       // for Azure
}
```
- Leading and trailing silence are trimmed, keeping 100 ms padding. This also cuts Azure billing.

**Fan-out**
- The session runner sends the `Utterance` to `WordRecognizer` (#16) and `Scorer` (#17) **in parallel**.

**"Listen to yourself"**
- Play the child's utterance, then the model clip. Kids love this, and it works offline.

**Permissions**
- `RECORD_AUDIO`, asked once on the parent's first setup with an explanation screen, not in front of the child.

**Privacy**
- Audio stays in memory. It is written to disk only if the parent turns on recordings (#14) or calibration mode (#19).

## Tasks
- [ ] `Recorder` interface plus Android implementation plus fake
- [ ] VAD and endpointing with tunable constants (read from `scoring_config.json`)
- [ ] Mic button widget: states, level meter, accessibility
- [ ] Gain check on the kids' tablet (some tablet mics are quiet). Document results in `docs/hardware.md`

## Acceptance criteria
- [ ] On the spike set (#4) or calibration set (#19), at least 95% of kids' utterances in a quiet room are captured with no cut-off start or end
- [ ] Under 300 ms from end of speech to `Utterance` ready
- [ ] Works in airplane mode; no file left on disk with default settings
