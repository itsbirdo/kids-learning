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

**Healthy motivation** (R20 in [`docs/learning-methodology.md`](../learning-methodology.md))
- **Informational feedback**, specific to what the child did: "¡Aprendiste 5 animales!", "You remembered *perro* from last week!". Informational feedback raises motivation.
- **No completion-contingent rewards.** Expected rewards for doing or finishing a task *lower* children's later motivation (Deci, Koestner & Ryan 1999: d ≈ −0.36 for completion-contingent rewards; tangible rewards are worse for children than adults).
- **Progress is shown as mastery,** not paid for: a "words I can say" collection and the unit map filling in.
- **Rewards are occasional surprises,** never promised in advance.
- **Praise is about the work, not the child** ("You worked that one out!"). Expect small effects (Li & Bates 2019; Sisk et al. 2018).

**Hard "no" list**
- lives or hearts
- timers
- leaderboards
- streaks that can be lost
- rewards promised for finishing a lesson or unit
- push notifications to the child
- autoplay into another session
- ads, purchases, or external links outside the parent gate

## Screens
1. **Who's playing?** Avatars for each child.
2. **Home.** A big "¡Vamos!" play button, the unit map (a path that fills in as words are mastered), the "words I can say" collection, and the sticker book.
3. **Session.** Activity frame, a progress caterpillar (no countdown), and a pause button.
4. **End.** Informational recap of today's words (with play buttons), the **grown-up turn card** (#14), and the mascot waving "¡Hasta mañana!". Sometimes a surprise sticker. Then back home.
5. **Parent gate entry.** A small corner button that needs a 3-second hold, then the PIN (#14).

## Rewards
- **Mastery displays** (the main motivator):
  - a "words I can say" collection: each word appears when its `say` card reaches box 3 (#12), and tapping it plays the child's model clip;
  - the unit map fills in as words are recognised and said;
  - unit completion is shown as the map reaching the next place, not as a prize.
- **Surprise stickers:**
  - now and then, about 1 in 5 sessions, at random;
  - never announced in advance and never "earned" by finishing;
  - a sticker book to browse.
- **Speaking stars:** 1–3 stars per item (#17). **Never 0**: trying always earns a star. Stars are feedback on that attempt, not currency; there is nothing to spend them on.
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
