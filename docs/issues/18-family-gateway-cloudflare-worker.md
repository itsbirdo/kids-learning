---
planned_number: 18
title: "Family gateway (Cloudflare Worker): short-lived tokens, TTS proxy, caps and budgets"
type: Feature
labels: [phase-3-speaking, "area: infra", "area: safety"]
parent: 1
---

**Phase 3 · Size M · Depends on: #3 · Blocks: #17 (production), #20, #21**

## Why
- Keys bundled in an APK can be extracted.
- One tiny server-side component can:
  - hand out short-lived tokens;
  - enforce caps and budgets;
  - moderate conversation (#21).
- A hobby project can run it for free.

## Stack
- Cloudflare Workers (TypeScript, `wrangler`).
- **Counters:** one SQLite-backed Durable Object, so they stay consistent.
- **Secrets:** set with `wrangler secret put`: `AZURE_SPEECH_KEY`, `AZURE_REGION`, `ANTHROPIC_API_KEY` (#21), `ADMIN_SECRET`.
- **Tests:** `vitest` with the Workers test pool; upstream APIs mocked.

## Endpoints
| Method | Path | Phase | Purpose |
|---|---|---|---|
| POST | `/v1/speech/token` | 3 | Calls Azure `POST https://{region}.api.cognitive.microsoft.com/sts/v1.0/issueToken` with `Ocp-Apim-Subscription-Key`. Tokens last **10 min**; cache for 9. Returns `{token, region, expiresIn: 540}` |
| GET | `/v1/usage` | 3 | Today's and this month's counters for the parent dashboard (#14) |
| POST | `/v1/admin/devices` | 3 | Register or revoke device tokens (needs `ADMIN_SECRET`) |
| POST | `/v1/tts` | 4 | Azure TTS in the house voice (SSML template shared with #7). Character cap per request and per day. Returns mp3 (#20) |
| POST | `/v1/chat/turn` | 5 | Conversation turn with moderation and caps (#21) |

## Auth and limits
- **Device tokens:**
  - random 32 bytes, stored *hashed* in the Durable Object, revocable;
  - the app keeps its token in `flutter_secure_storage`;
  - paired by QR code in the parent area (#14).
- **Limits** (all configurable through env vars):

| Limit | Default |
|---|---|
| Requests per device per minute | 30 |
| Speech tokens per day | 200 |
| TTS characters per day | 2,000 |
| Chat turns per day | 60 |
| Chat minutes per day | 15 |

- **Monthly estimated-cost cap,** plus a **kill switch** env var that refuses everything.
- **Why app-side caps matter:** Azure budgets only *alert*; they don't stop usage. Using **F0** makes the free quota the real cap for speech. Anthropic has a Console spend limit that does stop requests (#21).

## Privacy
- Never log bodies, audio or transcripts. Log only status, latency, endpoint and counter changes.
- No CORS: this is not a browser API.

## Ops
- **Azure Speech resource:** F0 tier, in a region that supports pronunciation assessment *(verify the region list)*. Rotate between Key1 and Key2.
- **Deploy:** `wrangler deploy`, manually or from CI on a tag. Use separate `staging` and `prod` environments.
- **Docs:** `docs/gateway.md` covers setup, secrets, pairing a device, rotating keys and reading usage.
- **Cost:** the Workers free plan (about 100k requests a day, *verify*) is far above family use.

## Tasks
- [ ] Worker skeleton, auth middleware, Durable Object counters
- [ ] `/v1/speech/token` with caching, plus tests (mocked Azure)
- [ ] `/v1/usage`, `/v1/admin/devices`
- [ ] App `GatewayClient` plus parent-area pairing (#14)
- [ ] `docs/gateway.md`

## Acceptance criteria
- [ ] The app gets Azure tokens only through the gateway in release builds
- [ ] A revoked device gets 401; going over a cap gets 429 with a friendly app message
- [ ] Tests cover auth, caps, caching, the kill switch and upstream errors
