---
planned_number: 9
title: "App architecture, data layer and content loading"
type: Feature
labels: [phase-2-core-app, "area: app"]
parent: 1
---

**Phase 2 · Size M · Depends on: #3, #6 · Blocks: #10–#17**

## Goal
A clean, testable structure that keeps the platform-specific parts small. Recognizer, recorder, player and TTS sit behind interfaces, so the iPad port (#23) and the tests swap implementations without touching features.

## Layers
| Layer | Contents | Rules |
|---|---|---|
| `features/` (presentation) | Screens, widgets, Riverpod providers | No business logic beyond view state |
| `domain/` | Session composer (#11), SRS (#12), word matcher (#16), star decisions (#17) | **Pure Dart**, no Flutter imports, fully unit-tested |
| `data/` | `ContentCatalog`, `ProgressRepository` (drift), `SettingsRepository` | Only layer that touches persistence |
| `platform/` | `ClipPlayer`, `Recorder`, `WordRecognizer`, `SystemTts`, `SecureStore`, `GatewayClient` interfaces + Android impls + fakes | Only layer with platform channels |

- **State and navigation:** Riverpod for state; `go_router` for navigation.
- **Models:** `freezed` + `json_serializable` for immutable models.

## Content loading
- At startup, read `assets/content/content.json`, `audio_manifest.json`, `images_manifest.json`, `grammar.json` and `scoring_config.json`. Build one in-memory `ContentCatalog`.
- Check `content_version`. When it changes, run a reconcile step: new items appear and removed items are hidden. Progress rows are never deleted.
- Tolerate missing optional clips and images: log them and use fallbacks.

## Progress database (drift / SQLite)
| Table | Columns |
|---|---|
| `children` | `id, name, age_band (6-7 \| 8-10), avatar, created_at, settings_json` |
| `cards` | `child_id, item_id, skill (listen \| say), box, due_at, last_seen_at, seen_count, correct_streak, introduced_at`. PK `(child_id, item_id, skill)` |
| `attempts` | `id, child_id, item_id, skill, at, outcome (correct \| retry \| shown \| heard_none), stars, recognizer_json, scorer_json, duration_ms`. **No audio** |
| `sessions` | `id, child_id, started_at, ended_at, new_count, review_count, seconds` |
| `stickers` | `child_id, sticker_id, unit_id, earned_at` |
| `kv_settings` | `key, value` (family settings) |
| `usage` | `day, azure_seconds, tts_chars` (local view of the Azure quotas used by #17 and #20) |

- Schema versions with tested migrations (`drift` schema dumps in `test/`).
- `flutter_secure_storage` (Android Keystore) holds the gateway device token and any dev key.

## Cross-cutting
- **Feature flags** (family settings): speaking checks, online scoring, custom words, dialogues.
- **No analytics, crash-reporting or ads SDKs** (#24). Keep a local rolling debug log that a parent can export from the parent area.
- **Performance:** cold start under 2 s on the tablet; preload the next activity's clips and images.

## Tasks
- [ ] Folder structure, DI with Riverpod providers, router skeleton
- [ ] `ContentCatalog` loader with tests against a fixture bundle
- [ ] drift schema, repositories and migration tests
- [ ] Platform interfaces plus fakes (`FakePlayer`, `FakeRecorder`, `FakeRecognizer`)
- [ ] Settings plus feature flags

## Acceptance criteria
- [ ] The app boots, loads the bundle, creates a child profile, and keeps it across restarts
- [ ] The domain layer has no Flutter imports (enforced by a lint or test)
- [ ] Repository and migration tests pass in CI
