# the talks UX v0: review 1 (st-fable, 10 Oct 2026)

Reviewed: `qa/talks-ux/renders/proposed-*` and `compare-*` (390 × 844, 1536 × 703) against `DIRECTION.md`.
Verdict: **direction approved with the changes below. Not owner-ready until item A is fixed.** Re-render, and I'll re-check.

## Your four questions
1. **Caveat for the hub and sheet titles: yes.** Keep your compact hub header: "the talks" Caveat 40 / 52 inline with the
   tagline, which beats my 52 / 72 because the feed starts higher. The sheet title "spill your tea" in Caveat is good.
   No serif display in the talks.
2. **Cards, not dividers.** Your cards on cream read friendlier and more structured than my divider list. Keep them,
   but tighten (D).
3. **3-column desktop: yes.** It supersedes the 8fr / 4fr from the earlier talks-desktop acceptance: topics left
   (220, sticky), feed ≤ 680, right rail (300, sticky). It matches DIRECTION §6.
4. **Teaser:** keep it as rendered (board slice + bar + "see all talks ›"). The same row styles as the hub are enough;
   the teaser doesn't need full cards.

## Must fix
- **A. No invented activity in anything the owner sees, or anything we build.**
  - The thread renders show replies from "lowkeymomo / sleepyjalebi / goldenchai", and the first hub card says
    "3 replies". The live seeds have 0 replies.
  - Either render the real state ("no replies yet", which is the empty state the owner should see anyway), or add a
    second, clearly labelled frame with a visible band: "example replies: layout preview, not real posts". No fixture
    data in the theme.
- **B. One-tap stays one tap after scrolling (phone).** Keep the bar under the header. When it scrolls out of view,
  show a sticky bottom bar: same component, 56 px, safe-area aware, hidden while the keyboard is open. Hub and topic
  pages only; the thread page keeps its reply bar.
- **C. Body / excerpt at 16 px on phone** (you have 15), so QA's type floor holds. Meta stays at 13.
- **D. Denser cards.**
  - Padding 12 / 14 (phone) and 14 / 18 (desktop); gap between cards 8 / 10.
  - Excerpt 1 line on phone and desktop.
  - Move "💬 n replies" / "no replies yet" to the right end of the meta line, which removes a row.
  - Targets: about ≤ 104 px per card on phone (4 talks in the first screen at 390 × 844) and ≤ 92 px on desktop
    (5 talks at 1536 × 703; today it's 3, at about 160 px each).
  - Show the topic tag only in the "all" view.

## Keep as is
- **Composer:** the single box ("first line = your headline"), 2 starters per topic, "posting as {alias} · shuffle",
  the full-width "post it", the no-login line. It's simple and clear.
- **Pre-launch states:** the bar reads "posting opens soon. read along for now."; no reply / report actions while
  posting is off (they read st-talk-live as built).
- **Replies:** one nested level with the pink connector and "↪ alias"; initial avatars for replies; "show n more"
  after 6.
- **Colours and contrast:** chip #fdf0f0 / #a31a33 (6.9 : 1), CTA white on #c3021d (6.3 : 1), muted #5d5562 (≥ 6.6 : 1 on
  cream and white). Keep every target ≥ 44 px, including the chips' hit area and the "reply" / "report" links.

## For the next renders
CURRENT | PROPOSED at 390 × 844 and 1536 × 703: hub (all + one topic), thread (real 0-reply state, plus the labelled
example frame if you want to show replies), composer open, pre-launch hub, teaser. Add a 1920 × 1080 hub for the
Tier B density check.
