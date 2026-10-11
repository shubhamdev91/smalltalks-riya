# the talks UX v4 (owner round 2): review 4 (st-fable, 10 Oct 2026)

Reviewed: `renders/compare-{hub,composer,thread,inline-reply}-*` and `proposed-*` (13:39–13:40).
**Verdict: the direction is APPROVED** (hero writing box, Reddit-style thread lines, inline reply at any depth). It goes
to the owner after items 1–4.

## Must fix before the owner set
1. **The band must be visible in every frame that shows sample replies.** The inline-reply frames (390 and 1536) are
   scrolled past the striped band, so their replies read as real. Repeat the band at the top of each such frame (or
   make it sticky in the example frames).
2. **The desktop hero box is too small for "we need them to spill".** At 1536 it's about 3 lines (≈ 100 px). Make it
   at least 5 lines (min-height ≈ 168 px), with the same 18 px text as phone's 17, so the box leads the page on desktop
   too. Phone is good (196 px).
3. **Wordmark:** render the v4 hub at 390 and 1536 with options A, B and C, plus today's version, as a wordmark sheet.
   The CSS for each option is in `qa/talks-ux/wordmark/render_wordmark.py` (`OPTS`, fonts as data URIs from
   `spec/fonts/`). For C, use the header lockup ("the" 1.02 em) in the site header and the hub lockup ("the" 0.74 em)
   for the hub title. Mark C as recommended. The other v4 frames use C.
4. **Copy:** the owner set waits for st-copy's V1–V7 (the drafts are clean, but every shopper-visible word comes from
   the register). If timing forces it, label the frames "copy pending".

## Approved, with notes for build
- **Hero box:** 2-line placeholder (the first line becomes the headline), "need a nudge?" inside the box, one topic
  chip with ▾ plus a big "post it", the alias line and one rules line. The phone sticky "spill your tea" focuses the
  box and hides while typing. Good.
- **Thread lines:**
  - one 1.5 px line per ancestor level (16 px phone / 22 px desktop);
  - 4 visible levels on phone, then "continue this thread ›";
  - folded = "{n} more replies".
  - Build: each line is a `<button aria-expanded>` with a 44 px hit area and a visible focus ring.
- **Inline reply:**
  - the same box, smaller, under any comment;
  - "replying to {alias} ✕" plus cancel / reply.
  - Build: focus moves into the box, Esc cancels and returns focus to the "reply" link; only one inline box open at a time.
- **Hub:** the real 0-reply state is kept everywhere. The phone list starts lower because of the hero box, which is
  accepted: the owner asked for the box to lead.
- **Data proposal** (`talks/staged/nesting/PROPOSAL.md`, an optional `parent` field on talk_reply): store data, so it
  needs the orchestrator and owner's approval. It's not part of this design sign-off.

## Re-check (13:50 renders)
- Item 1, the band in every reply frame: DONE (sticky band).
- Item 2, the desktop hero box: DONE (≈ 186 px, 5 lines).
- Item 4, copy: DONE (st-copy v1.7, no drafts).
- Item 3, the wordmark: **superseded.** The owner rejected A/B/C and kept the original Caveat, refined. The renders still
  use C. Swap to V2 + the header ↗ (`wordmark/CAVEAT-REFINE.md`). The owner gets `caveat-sheet.png` and
  `caveat-1536-header-2x.png`, not `options-sheet.png`.
- Owner-ready after that swap.

## Final look (13:54–13:56 renders): OWNER-READY
- V2 is in everywhere: the site header (V2 + ↗, phone and 1536), the drawer without the arrow, and the hub title at
  40 / 52 with the swash clearing the tagline.
- `compare-header-wordmark-{390,1536}.png` shows NOW vs V2 clearly at 2×.
- Items 1, 2 and 4 are unchanged and fine.
- Owner package from the talks side:
  - `renders/compare-{hub,composer,thread,inline-reply}-{390x844,1536x703}`;
  - `compare-header-wordmark-{390,1536}`;
  - `wordmark/caveat-sheet.png` + `caveat-1536-header-2x.png`.
