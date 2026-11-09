# kids-learning

A personal, non-commercial Spanish-learning app for kids aged 6–10.
- **Platform:** Android tablet first, iPad later.
- **Voice:** in and out.
- **Cost:** no subscription, near-zero running cost.

> Status: **planning**. No app code yet.

## Start here
- [Implementation plan](docs/implementation-plan.md): architecture, phases, decisions and the issue index.
- [Issue specs](docs/issues/): one detailed spec per part of the build (mirrored as GitHub issues).
- [ADR-001: Flutter, Android first](docs/adr/0001-flutter-android-first.md)
- [Learning method](docs/learning-methodology.md): how the app teaches, and the research behind it.
- [Research](docs/research/): the original research notes, the 2026-11-08 verification reports, and the 2026-11-09 learning-method reviews.

## Planned layout
```
app/        Flutter app (Android first)
content/    Lesson content as YAML (source of truth)
tools/      Python CLI `kl`: validate, build, audio, images, eval
gateway/    Cloudflare Worker: short-lived Azure tokens, TTS proxy, caps
docs/       Plan, ADRs, research, guides
```
