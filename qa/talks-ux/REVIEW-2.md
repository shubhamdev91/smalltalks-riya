# the talks UX v1: review 2 (st-fable, 10 Oct 2026)

Reviewed: `renders/proposed-*` and `compare-*` (v1, 12:55–12:58) against DIRECTION.md and REVIEW-1.
**Verdict: the design is APPROVED. It goes to the owner once items 1 and 2 are done** (render-only fixes; no design
change).

## Must fix before the owner sees it
1. **Visible label on sample content.** The thread renders still show invented replies (lowkeymomo / sleepyjalebi /
   goldenchai), and the first hub row says "3 replies". They're marked SAMPLE only in the README, and the owner will
   see the images, not the README. Do one of these:
   - render the real state (0 replies: "no replies yet") for the hub and thread, and keep the reply design in ONE extra
     frame per size that carries a visible band across the top, "example replies: layout preview, not real posts"; or
   - put the band on every frame that shows sample content.
   The hub's first row must show the real "no replies yet" in all hub frames.
2. **No "DRAFT" text in owner renders.** Use st-copy's final placeholders. Until they land, hold the composer frames or
   leave the fields empty.

## Your calls
- **Row height 94 (phone) / 97 (desktop): ACCEPTED.** Keep the 1-line excerpt on desktop; it's worth the extra 13 px.
  At 1536 × 703 five talks show in the first screen, which meets the target. My 84 was a guess.
- **Desktop composer: open it at the top of the feed (720 wide), not in the rail.**
  - The rail's "spill your tea" scrolls to the feed top and opens the panel inline there.
  - Chips fit in one row, the whole form fits in one screen, the rail stays sticky and nothing is cut off.
  - Phone keeps the bottom sheet.
- **Topics 5 vs 4:** the owner's call. Show both crops in the owner set, as you have.
- **Teaser:** approved as is (heading + CTA kept, board rows = the hub row component).

## Checked and approved
- **Type:** Caveat only on "the talks"; DM Sans elsewhere; the "spill your tea" CTA in Barlow. No serif.
- **Hub:**
  - phone sticky "spill your tea" bar; chips with the active "all" filled;
  - meta "small talk · 1d" with "💬 n replies / no replies yet" at its end (desktop) or under the title (phone);
  - 3-column desktop: topics with counts | feed | rail.
- **Thread:** one nested level with "↪ @alias", the sticky "add your two cents…" bar on phone, "got your own tea?
  spill it ›" at the end.
- **Composer:** topic chips, starter chips, alias + shuffle, the rules line, the full-width "post it", "no name, no
  login".
- **Empty state:** "it's quiet in here…" + CTA. **Pre-launch:** the bar is replaced by "posting isn't open yet. read
  along for now."
- Contrast and targets as in DIRECTION §7.
