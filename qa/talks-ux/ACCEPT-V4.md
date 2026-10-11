# Acceptance: the talks v4 + wordmark V1, installed on the build (186651934933). st-fable, 10 Oct 2026

Evidence: st-talks' after-shots `qa/talks/v4-after/` (posting on) and `qa/talks/v4-off/` (posting off); the orchestrator
read back the 20 md5s.

## Verdict: ACCEPTED (inline-reply frame still to come from the E2E)
- **Wordmark V1:**
  - the site header at 390 / 1536 / 1920 and on non-talks pages (home, PDP, Journal at 390 / 1536) shows the outlined
    Caveat 700 mark at the approved size, with the small ↗ on the x-height inside the link;
  - the phone drawer shows the mark without the arrow;
  - the hub title shows V1 at 40 / 52 with no arrow, as V1-FINAL.
  - The header row height is unchanged, and nothing is clipped.
- **Hub:**
  - the hero writing box (≈ 196 px phone, ≈ 216 px desktop) with "need a nudge?", the topic chip and "post it", plus
    the alias + shuffle and rules lines;
  - the phone sticky "spill your tea";
  - the 3-column desktop (topics | feed | house rules), matching the approved v4.
- **Composer (focused):** the box takes focus with the red outline; the starter is in the box. As approved.
- **Thread:** the real state "no replies yet. be the first."; the reply box under the post ("add your two cents…",
  "replying as {alias}", reply); "got your own tea? spill it ›". Thread pages are styled (the CSS move into
  st-talk-config works).
- **Posting off** (`v4-off`, 320 / 390 / 1280):
  - the hero box is replaced by "posting isn't open yet. read along for now.";
  - the thread shows the same line and "no replies yet";
  - there are no reply / report actions.
  - The st-talk-live switch reads correctly both ways (the doc-block fix holds).
- **No fake activity:** every row on the live build reads "no replies yet", the aliases are "small talk", and there are
  no sample replies anywhere.

## Notes (non-blocking; for st-talks / the owner)
1. **Topics:** the rail and chips show 3 topics (plot twists, tiny wins, nail talk). The approved v3/v4 renders showed
   5 (plus second opinions, just venting).
   - If "5 locked topics" means these two should appear, they're missing on the build: a talk_topic entry or the
     chip_order needs checking.
   - If they're hidden because they're empty, that's fine; please confirm.
2. **Desktop topic counts:** the approved renders showed counts next to each topic (9 / 4 / 3 …); the build shows none.
   Optional, owner-neutral.
3. **Inline reply at depth:** accept from the E2E frame once the owner's v0 Publish lands (with real replies, or a
   banded example frame, never fixture data).
