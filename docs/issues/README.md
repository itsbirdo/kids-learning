# Issue specs

> **Status:** created on GitHub as issues [#1–#25](https://github.com/itsbirdo/kids-learning/issues) on 2026-11-08 (#26–#27 added 2026-11-09), with matching numbers, labels and issue types. #2–#25 are sub-issues of the epic #1. **The GitHub issues are now the live specs;** these files are the original snapshot.

One file per GitHub issue, numbered in the order they should be created. GitHub assigns numbers in creation order. In an empty repo the planned numbers (#1–#25) therefore match, and the cross-references (`#7`, `#16`…) work as written.

| # | Spec | Phase |
|---|---|---|
| 1 | [Epic: implementation plan](01-epic-implementation-plan.md) | — |
| 2 | [Decision: Flutter, Android first](02-decision-flutter-android-first.md) | 0 |
| 3 | [Scaffolding, repo layout, CI](03-scaffolding-repo-ci.md) | 0 |
| 4 | [Spike: speech and voices on the real tablet](04-spike-speech-voice-validation.md) | 0 |
| 5 | [Curriculum and lesson content](05-curriculum-lesson-content.md) | 1 |
| 6 | [Content schema and `kl` tooling](06-content-schema-tooling.md) | 1 |
| 7 | [Audio generation pipeline](07-audio-generation-pipeline.md) | 1 |
| 8 | [Illustrations and assets](08-illustrations-assets.md) | 1 |
| 9 | [App architecture and data layer](09-app-architecture-data-layer.md) | 2 |
| 10 | [Audio playback service](10-audio-playback-service.md) | 2 |
| 11 | [Lesson engine and activities](11-lesson-engine-activities.md) | 2 |
| 12 | [Spaced repetition and progress](12-spaced-repetition-progress.md) | 2 |
| 13 | [Kid UX and rewards](13-kid-ux-navigation-rewards.md) | 2 |
| 14 | [Parent area](14-parent-area.md) | 2 |
| 15 | [Mic capture](15-mic-capture-recording.md) | 3 |
| 16 | [On-device word check (Vosk)](16-on-device-word-check-vosk.md) | 3 |
| 17 | [Azure scoring and stars](17-azure-pronunciation-scoring-stars.md) | 3 |
| 18 | [Family gateway (Cloudflare Worker)](18-family-gateway-cloudflare-worker.md) | 3 |
| 19 | [Calibration toolkit](19-calibration-toolkit.md) | 3 |
| 20 | [Dynamic speech and custom words](20-dynamic-speech-custom-words.md) | 4 |
| 21 | [Conversation practice: scripted dialogues (optional)](21-scripted-conversation-practice.md) | 5 |
| 22 | [Android release and install](22-android-release-install.md) | 6 |
| 23 | [iPad port](23-ipad-port.md) | 6 |
| 24 | [Privacy, terms and child safety](24-privacy-terms-child-safety.md) | cross-cutting |
| 25 | [Testing, QA and playtests](25-testing-qa-playtests.md) | cross-cutting |
| 26 | [Multi-language: language packs](26-language-packs.md) | 2 |
| 27 | [German course](27-german-course.md) | 7 |

## File format
Each file starts with front matter, followed by the issue body in Markdown:
```yaml
---
planned_number: 7
title: "..."
type: Feature        # GitHub issue type: Feature | Task
labels: [phase-1-content, "area: content"]
parent: 1            # becomes a sub-issue of the epic
---
```

## Creating the issues
`create_issues.py` creates the labels, the issues (with type and labels) and the epic's sub-issue links, using the GitHub CLI:
```bash
gh auth login                      # an account with write access to the repo
python3 docs/issues/create_issues.py --repo itsbirdo/kids-learning --dry-run   # preview
python3 docs/issues/create_issues.py --repo itsbirdo/kids-learning
```
- **Numbering:** if GitHub assigns different numbers (because issues or PRs already exist), the script rewrites the `#N` references to match.
- **Links:** relative links to docs are turned into absolute links on `--ref`, which defaults to `main`.

Once the issues exist, the GitHub issues are the live specs. Update them there and treat these files as the original snapshot.
