# Posting-ON window: install plan (staged 10 Oct; write only after the owner's setup and a fresh lock grant)

**APPROVED as staged** by the orchestrator (10 Oct), including the byte cost. The grant follows the owner's "talks app
installed". After the install, st-fable compares the avatar tips with the other HD surfaces.

**Live theme:** the live MAIN theme is a published copy of the build and changes with each owner publish (186695155925 since 10 Oct 14:12Z; before that 186687553749). Re-check `themes { role }`. Never write to it.

- This window writes ONLY to the build, 186651934933. The real end-to-end test and test-post deletion run on the build
  preview.
- Shoppers get posting only after the owner re-duplicates the build and publishes the copy (the orchestrator asks the
  owner once this window is accepted).
- The App Proxy is store-level, but live talks pages keep posting OFF (composer hidden) until then.

Staged in `talks\staged\posting-on\src\` (snippets\ and blocks\). The shared mirror `theme-build\src` is untouched until the grant.

## Files: 3 snippets + 2 blocks, theme 186651934933 only

| File | Expected remote md5 (my last upload) | New md5 | Change |
|---|---|---|---|
| snippets/st-talk-avatar.liquid | 59dd5e9409145891c6f20efc1d340ebe | 4b5745382dec4fee27d14c0d9cfd132c | HD nails (below) |
| snippets/st-talk-config.liquid | 41dec54141d5a76086a3f6795b7f28d0 | 3260d12a8e2d6acef2dd5b36031a5159 | `sprites` map → st-hd-nails-<set>.webp (optimistic rows in st-talks.js) |
| snippets/st-talk-live.liquid | 82c0b8700973b0b34166154b359dbb80 | 6e1a4ff06c7a5c3a17714a3af702c216 | `'off'` → `'on'` (posting ON) |
| blocks/st-talk-example.liquid | 73fcea2109bc15d541e170d2ddbfc616 | 44941c76d84707a6e1bd1f12202caa3d | a11y: `<li class="st-talk">` → `<article>` |
| blocks/st-talk-examples.liquid | fef12c7b70bfd12330683d0d4daa29dc | b5162be3a695216dc3bdf9c3e531bb8e | a11y: `<ul class="st-talks__list" role="list">` → `<div>` |

All 5 expected md5s were re-read from the theme on 10 Oct and matched.

**A11y fix (orchestrator, 10 Oct; axe serious "listitem" on /pages/the-talks):**

- `content_for 'blocks'` wraps every theme block in `div.shopify-block`, so an `<li>` card can never sit directly in the
  `<ul>`.
- The cards are now `<article>`s (each has its own h3) in a plain `<div>`. Same classes, and no CSS targets the tags.
- **Pre-check:** I applied the change to the preview DOM (`talks/tools/examples_probe.py`).
  - axe `list` + `listitem`: 3 serious → 0, at 390 and 1280.
  - The examples group is pixel-identical at both widths.
  - The 390 shot is `qa/talks/examples-article-390.png`.
- page.desi-talks.json uses the same blocks, but no page is assigned to it (/pages/desi-talks is 404).

**HD nails (st-fable's rule, via the orchestrator, 10 Oct):**

- The talks avatars use the hero's `assets/st-hd-nails-<set>.webp`, the same file per set site-wide.
- The nail cell is ×1.058 (0.895/0.846) about the cuticle (50% 92.5%), applied first:
  `transform: translateY(42.5%) scale(1.058) translateY(-42.5%)`.
- The existing `rotate: -20deg` and `translate: 4% 16%` are unchanged, and so are the disc sizes (90/88/66/52).
- st-talks.js is unchanged: it reads `cfg.sprites` and the same `.st-tavatar__nail` CSS.

## Store kill switch (server side)

**The switch:** `talk_settings/main`, gid://shopify/Metaobject/616028176597, field `posting_open`.

- The parent set it to "false" at 10 Oct 19:37:18Z, with the owner's approval.
- The backend refuses every post and reply while it is not "true", before any validation or write. Verified live:
  `{"action":"post"}` and `{"action":"reply"}` both return 403 `closed`.
- `GET /apps/talks` shows what the backend reads (`{"open": false}`).
- The value is cached up to 60 s per warm instance.
- **Reports are not gated** (moderation keeps working while posting is paused). Brand posts can't be reported.

**In this window** (owner-approved as part of it; any permission prompt for the mutation is the owner's to answer in
my session):

1. Install the theme files first, posting UI ON, while `posting_open` is still "false". Shoppers can't post yet.
2. Run `metaobjectUpdate` on 616028176597: `posting_open` → "true". Wait ≤ 60 s, then check that `GET /apps/talks`
   returns `{"open": true}`.
3. Run the real E2E: post, reply, report with no login; blocked content; slow-down; 320/390/1280. Then delete the
   test posts.
4. **Pass:** leave it "true".
5. **Any failure:** set it back to "false", confirm `{"open": false}`, and report.

**Backend deploy with this window** (owner's OK + the owner's v0 Publish; the build string changes):

- remove `?diag=ip`;
- make settings fail-closed: open only when `posting_open == "true"`; a missing entry means closed;
- optional: gate reports too, if the owner wants that.

Prepare and test it locally, update the v0 chat files only after the owner's OK, and check the new build string on
`/api/talks` before step 2.

## Order

1. **Before writing:** re-fetch the remote md5 of all 5 files. They must equal the "expected" column. If not, stop and
   tell the orchestrator.
2. **Upload avatar + config + the 2 blocks.** Posting is still OFF.
   - Run axe `list`/`listitem` on /pages/the-talks: `python -I talks/tools/examples_probe.py`. "before" must now show
     0 violations.
   - Verify at 390 on hub, topic and thread: `python -I talks/tools/nail_requests.py` must show 0 `st-nails-*`
     requests and 0 P1 style refs.
   - Take a 390 thread shot with the avatar (tip not clipped).
3. **Upload st-talk-live** (`on`). Run `qa_live.py real` at 320/390/1280, then delete the test posts.
4. **Read back the md5 of all 5 files.** Report to the orchestrator, then release the lock.

## Pre-checks done 10 Oct, by in-browser injection on the preview (no theme write)

**Tip clearance** (`talks/tools/hd_avatar_probe.py`): the tip is clear of the rim on every hub and thread avatar.

| Avatar | P1 nearest-rim gap | HD nearest-rim gap |
|---|---|---|
| Hub, Ø 90 | about 12 CSS px | about 7 CSS px |
| Thread, Ø 88 | about 12 CSS px | about 7 CSS px |

- The HD plate starts higher in its cell, so its tip sits about 5 px higher.
- The base stays cropped by the circle, as on the board.
- Pairs (P1 | HD): `qa/talks/hd-avatar-probe-{hub,thread}-*.png`.

**Requests today** (`talks/staged/nail-requests-before.json`): every P1 `st-nails-*` request on the talks pages comes
from `.st-tavatar`.

| Page | P1 sheets requested |
|---|---|
| Hub | 7 |
| Topic (tiny-wins) | 3 |
| Thread | 1 |

The header, bag and footer request none.

**Weight (cold cache, sheet bytes from the CDN):**

| Page | P1 | HD | Change |
|---|---|---|---|
| Hub | 180 KB | 485 KB | +305 KB (about 408 KB of it is requested at load even without scrolling) |
| Topic | about 70 KB | about 177 KB | +107 KB |
| Thread | 23 KB | 60 KB | +37 KB |

- The sheets are decorative CSS backgrounds that load in parallel. They don't block text or first paint.
- After any visit to the homepage hero (or other HD surfaces) they are already cached: 0 extra bytes.
- `content-visibility: auto` on rows does NOT defer them (measured with `talks/tools/lazy_probe.py`).
- A lazy `<img>` would save little, because Chrome's lazy-load distance covers most of the hub.
