---
planned_number: 13
title: "Kid-facing UX: navigation for pre-readers, unit map and healthy rewards"
type: Feature
labels: [phase-2-core-app, "area: app"]
parent: 1
---

**Phase 2 · Size M · Depends on: #8, #9, #11 · Blocks: #25 playtests**

## Goal
A 6-year-old who can't read yet can start, play and finish a session alone. The app motivates with information and delight, not with pressure.

## Principles
**For pre-readers and beginning readers**
- **Audio everywhere:** every prompt is spoken, and every screen has a big replay button.
- **No reading needed:** navigation is icons only; captions are optional (age 8+).
- **Big targets:** at least 64 dp, with generous spacing.
- **Layout:** landscape tablet layout, one clear action per screen.

**Healthy motivation**
- Positive, informational feedback, e.g. "¡Aprendiste 5 animales!".
- Occasional *surprise* rewards rather than rewards tied to performance.

**Hard "no" list**
- lives or hearts
- timers
- leaderboards
- streaks that can be lost
- push notifications to the child
- autoplay into another session
- ads, purchases, or external links outside the parent gate

## Screens
1. **Who's playing?** Avatars for each child.
2. **Home.** A big "¡Vamos!" play button, the unit map (path with stickers), and the sticker book.
3. **Session.** Activity frame, a progress caterpillar (no countdown), and a pause button.
4. **End.** Recap, sticker reveal, and the mascot waving "¡Hasta mañana!". Then back home.
5. **Parent gate entry.** A small corner button that needs a 3-second hold, then the PIN (#14).

## Rewards
- **Stickers:**
  - one per unit completed;
  - surprise stickers now and then (about 1 in 5 sessions, random, never "earned");
  - a sticker book to browse.
- **Speaking stars:** 1–3 stars per item (#17). **Never 0**: trying always earns a star.
- **Mascot:** reacts warmly; never disappointed.

## Look and feel
- **Theme tokens:** colours, spacing, radii and type scale.
- **Font:** a child-friendly, OFL-licensed font (e.g. Andika or Atkinson Hyperlegible; check licence and ¿¡ñáéíóú support).
- **Sound:** soft chimes only; no buzzers (#10).
- **Accessibility:**
  - "reduce motion" setting
  - high-contrast option
  - haptic feedback on taps
  - colour-unit note for colour-blind kids

## Child-proofing (documented, outside the app)
- Android screen pinning, or Family Link with a kid profile (`docs/install-android.md`, #22).
- The app handles the back button and gestures gracefully (no accidental exits mid-activity).

## Tasks
- [ ] Theme and design tokens, font licence check
- [ ] Home, unit map, sticker book, end-of-session screens
- [ ] Mascot widget with states (#8)
- [ ] Parent gate entry (hold plus PIN), shared with #14
- [ ] Golden tests at the tablet resolution(s)

## Acceptance criteria
- [ ] Playtest (#25): a 6-year-old completes a session without help; an 8–10-year-old finds it "not babyish" (adjust tone per age band if needed)
- [ ] Nothing on the "no" list exists in the app (checklist in the PR)
