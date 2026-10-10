# Talks desktop layout (≥ 1024): install plan

**INSTALLED 10 Oct 15:39–15:40Z.**

- The lock was granted after st-foundation's release.
- Pre-write md5s matched.
- Uploaded in order: list + asset → thread → start + rules.
- All 5 read back equal to the new md5s.

**Verified:**

- **Laptops:** `desktop_probe.py real` gives the same numbers as the prototype. Shots: `qa/talks/desktop/real-*`.
- **Phones:** `phone_diff.py compare` vs the pre-install baseline: 9/9 identical.
- **Errors:** 0 Liquid errors and 0 page errors on fresh loads at 390 and 1366.
- **/blogs/news:** unchanged (flex, no talks chrome).
- **st-talk-ago.js:** served with 200.
- **Lock:** released.

**Request:** orchestrator, 10 Oct. **Spec:** `qa/desktop/STORE-DESKTOP-SPEC.md` §2 (st-fable): talks hub + thread.
Phones and 990–1023 stay unchanged. This is its own window, independent of `talks/staged/posting-on/` (no shared
files).

Staged in `talks\staged\desktop\src\sections\`. Theme 186651934933 only, never the live theme.

## Files (4 sections)

| File | Expected remote md5 (re-read 10 Oct, = my last upload) | New md5 |
|---|---|---|
| sections/st-talks-list.liquid | 27f3e22e4b232c4cc184ba1cbb4809ff | 04fdc439c7b0f16e41df6eb4c3572d38 |
| sections/st-talks-thread.liquid | 169bcc1df9c18a79e55c8333d6061fa7 | 2b96669cec06e3cad752e30fb0b08d44 |
| sections/st-talks-start.liquid | 51169e13fe12aa5ea0a91cd39de8e3ea | 737c910db364af1d67febad5184384c2 |
| sections/st-talks-rules.liquid | bd207701c01fbf1f0203f5e969b3f069 | 565f3fdca4711719b5f96cef215a68d0 |
| assets/st-talk-ago.js (new, optional add-on) | absent (checked 10 Oct) | ec96ff275a459399ad6607017d62f538 |

**Status:** the plan was approved by the orchestrator on 10 Oct. The grant comes after st-foundation's release, and
the remote md5s must be re-checked right before writing.

**Add-on: short relative times for the landing teaser** (orchestrator, spec v1.1 §1a, LND-065).

- `assets/st-talk-ago.js` is a 1.3 KB module. st-talks.js (33 KB, 9.5 KB gzip) is NOT loaded on home.
- **What it does:** every `time[data-st-ago]` (st-talk-time) inside a `[data-st-ago-strings]` host takes the host's
  `data-ago-now / -minutes / -hours / -days` patterns (`__n__` = number).
  - The copy stays in the host's section.
  - It applies under 7 days only; older times keep the server date.
- **Tested in Chrome:** just now / 7m / 3h / 1d / 6d. 8 days, future (which shows "just now") and a bad timestamp
  behave correctly, and times outside a host are untouched.
- **Contract for st-foundation's teaser:**
  - the board element carries the strings (e.g. `__n__m`, LND-065);
  - the section adds
    `<script type="module" src="{{ 'st-talk-ago.js' | asset_url }}" fetchpriority="low"></script>`.
- **Upload it before st-foundation references it.** Until then the teaser shows the plain date.

## st-fable pre-review (10 Oct), restaged

1. **Approved:** the composer card moves right on the hub.
2. **Changed:**
   - The house rules sit DIRECTLY UNDER the card on the hub, topic and thread pages (30 px gap), in normal flow from
     the top. There is no sticky.
   - The aside is ~740–940 px (card + rules), more than the 579–676 px available, and the card and the rules are
     different sections. So a sticky "whole aside when it fits" can't be done in CSS and would never trigger at
     these sizes.
   - **Hub:** the chips row is fixed at 31 + 44 px. A taller card (the open composer once posting is on) only moves
     the rules down and never the feed. Measured: with a 420 px card the feed stays at y = 436 and the rules go from
     474 to 842.
3. **Approved:** the H1, rules and panel headings keep their sizes.

**Re-checked:**

- 4 laptop sizes × 3 pages: 0 horizontal scroll, card→rules gap 30, no overlap, no target under 44.
- Phones 390/990/1023: pixel-identical.
  - Only 1–3 px specks appear inside nail avatars on the hub at 1023. Served vs served shows the same specks, so
    they are image-decode noise.

## What changes

- **Markup (list only):** chips → composer → `<div class="st-talks__feed">` (label, list, empty, more, handwritten
  panel). The wrapper is neutral below 1024.
  - It is a grid, like `.st-talks`.
  - base.css zeroes the top margin of a first-child heading or paragraph, so the label's 52 px and the empty
    state's 48 px are restated.
- **CSS:** everything else sits inside `@media screen and (min-width: 1024px)`.
  - `#MainContent:has(…)` becomes the page grid on talks pages only (hub/topic: `.st-talks[data-st-feed]`; thread:
    `.st-thread[data-st-thread-page]`).
  - News and article pages are untouched.
  - **Page frame:** `padding-inline: max(var(--pg-gutter, clamp(32px, 4vw, 64px)), (100% − var(--pg-max, 1240px)) / 2)`.
  - **Columns:** `minmax(0, 8fr) minmax(0, 4fr)`, with a column gap of `clamp(32px, 4vw, 72px)`.
- **Hub/topic:**
  - The list section joins the grid through subgrid (columns and rows).
  - The H1 block is centred across both columns.
  - Left: chips + feed (rows wider, title 24 px, excerpt 18 px / 62ch).
  - Right: the composer card, with the house rules directly under it.
- **Thread:**
  - Left: back link, thread (title 32 px, body 18 px / 68ch, avatar 96 px), replies (18 px) and the reply box.
  - Right: the Start-a-talk panel, with the house rules directly under it.

## Deviations from the spec (for st-fable)

1. **Hub "Start a talk" panel = the hub's own composer card**, moved to the right column. I did not add a second
   Start-a-talk section.
   - A second section would mean two composers when posting is on, and a duplicate `#start-a-talk`.
   - While posting is off, the card carries the TLK-153 note. The spec had the note on the left.
2. **No sticky aside.** First staged as a sticky card with the rules last. Replaced after st-fable's pre-review: the
   rules now sit directly under the card, in normal flow.
3. **Unchanged type:** the hub H1 (95 px, the board's display size), the rules heading (28) and the panel heading (46)
   keep their sizes. The spec's explicit numbers are applied: row title 24, thread title 32, body 18, avatar 96.

## Pre-checks (preview, staged CSS injected + the wrapper simulated in the DOM; no theme write)

**Laptops** (`talks/tools/desktop_probe.py proto`, shots in `qa/talks/desktop/proto-*`):

- Measured at 1280×720, 1366×768, 1440×800 and 1536×703, on hub, topic and thread.
- 0 horizontal scroll.
- **Content width:** 751–790 px (was 600 px hub / 386 px thread).
- **First screen:** heading + first row + aside side by side.
- **Right column:** the rules sit 30 px under the card at every size, with no overlap.
- **Targets:** no target under 44 px in the aside or the rules.

**Phones frozen** (`talks/tools/phone_diff.py proto`): full-page pixel-identical on hub, topic and thread at 390×844,
990×800 and 1023×800.

- One run showed a 1-pixel difference on the hub at 1023.
- On re-run, served vs served and served vs staged were all identical, so that pixel was render noise.

**Liquid:** if/for/paginate/unless/capture and `<div>` are balanced in all 4 files.

## Order

1. **Before writing:**
   - Re-fetch the remote md5 of all 4 files. They must equal "expected"; stop if not.
   - Save the phone baseline: `python -I talks/tools/phone_diff.py save`.
2. **Copy to `theme-build\src` and upload**, in this order: list → thread → start → rules.
   - The grid comes first.
   - Between steps, the aside cards keep their old max-width and auto margins inside the new columns, so no
     intermediate state is broken.
3. **Verify:**
   - `python -I talks/tools/desktop_probe.py real` at the 4 sizes.
   - `python -I talks/tools/phone_diff.py compare`: identical at 390/990/1023.
   - The /blogs/news render check (`talks/staged/news-baseline.json`).
   - `render_check.py`: 0 Liquid errors.
4. **Read back the md5s**, report with shots, release the lock.

**After posting is ON** (posting-ON window), check the open composer in the right column at 1280: alias, topics and
Post all fit, the rules move down under it, and the feed doesn't move.
