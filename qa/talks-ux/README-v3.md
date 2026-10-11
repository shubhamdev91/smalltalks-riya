# the talks: UX pass, v3 for the owner (10 Oct)

**Roles:** st-talks leads, st-fable directs and accepts, st-copy writes (register v1.5.4).

**Status:** OWNER-READY (st-fable, `REVIEW-3.md`). The compare-* set goes to the owner as is. Lab only: no theme or
data writes.

- The composer frames already carry st-copy's final placeholders (v1.5.4), so the "field hints come with the copy
  pass" caption is not needed.
- **Build gate** (after the owner approves; ONE talks window with posting-ON, `talks/staged/posting-on/INSTALL.md`):
  1. final copy (v1.5.4);
  2. real field labels (`<label>` / `aria-labelledby`, not placeholder-only; the title is `aria-required`);
  3. st-fable's after-shot acceptance on the preview at 390 / 1536 / 1920.

## Owner sheets (`renders/compare-*`: CURRENT | PROPOSED)

| Screen | 390 × 844 | 1536 × 703 | 1920 × 1080 |
|---|---|---|---|
| Hub (all) | ✓ | ✓ | ✓ |
| Topic (tiny wins) | ✓ | ✓ | |
| Thread (real: 0 replies) | ✓ | ✓ | |
| Composer, open | ✓ (bottom sheet) | ✓ (inline at the top of the feed) | |
| Pre-launch hub (posting off) | ✓ | ✓ | |
| Empty topic | ✓ | ✓ | |
| Landing teaser | ✓ | ✓ | |

- **Reply design:** `renders/proposed-thread-example-{390x844,1536x703}.png`, the ONLY frames with replies. A striped
  band across the top reads "example replies: layout preview, not real posts". The aliases are "alias one/two/three".
- **Topics for the owner:** `renders/compare-topics-390.png`, the proposed 5 vs the as-built 4, with a pro/con each.

**How these were made:**

- **CURRENT** = the build preview in the posting-ON state (composer row, reply box, the "no replies yet" line), injected
  with the exact Liquid markup. **Pre-launch** = the build as installed.
- **PROPOSED** = the same preview pages with the talks area swapped for `lab/proposed.css` +
  `lab/proposed_capture.py`.
- **REAL DATA ONLY:** the 9 real threads, all with 0 replies. No invented activity, and no fixture data for the theme.
- **Composer fields:** st-copy v1.5.4. Title: "what's the tea, in one line?" (TLK-170, hidden label TLK-101
  "headline", required). Details: "the rest of the tea (optional)" (TLK-171, label TLK-172). The starters drop into
  the title field. No DRAFT text anywhere.

## The design (approved v1 + REVIEW-2)

**Type and colour:**

- Caveat 600 for the "the talks" wordmark only (52 / 72).
- DM Sans for everything else:
  - labels 14/15 600;
  - list titles 17/19 600;
  - thread title 22/28 700;
  - body 16/17 at lh 1.5 (16 is the floor);
  - meta 13/14 #5d5562.
- The "spill your tea" CTA is Barlow Semi Condensed 600 at 20.
- One accent: #c3021d. No serif.

**Hub:**

- Wordmark + promise, then topic chips (36 px pill / 44 px hit), then "latest · n talks".
- **Rows:** flat with dividers, and each row is one link.
  - Avatar 40/44, "alias · 1d", the title (2 lines on phone; 1 line + a 1-line excerpt on desktop), and
    "💬 no replies yet" / "n replies".
  - Under the title on phone; at the end of the meta line on desktop.
  - "more talks" after 20.
  - House rules collapse to one row on phone; on desktop they live in the rail.
- **Phone:** a sticky "spill your tea ↗" at the bottom (safe-area aware, hidden while typing). Pre-launch: the line
  "posting isn't open yet. read along for now."
- **Desktop:**
  - ≥ 1280: topics 220 with counts (sticky) | feed ≤ 720 | rail 300 (sticky) with the CTA card + house rules.
  - 1024–1279: feed + rail.
  - ≥ 1680: a 1440 frame.

**Composer:** a bottom sheet on phones (focus-trapped dialog, Escape, 150 ms slide, none under reduced motion).

- **On desktop it opens inline at the top of the feed** (REVIEW-2); the rail's CTA scrolls there. The whole form fits
  in one 1536 × 703 screen, and the rail stays sticky.
- **Order:**
  1. "what's it about?" with the topic chips + "your own" (with 5 topics they wrap to 2 rows on desktop; 6 chips need
     ~640 px against ~600).
  2. "need a starting line?" with 2 starters per topic.
  3. Title (required).
  4. Details (optional).
  5. "posting as {alias} · shuffle".
  6. The rules line, then "post it", then "no name, no login. just your alias."
- **Data model unchanged:** title + newline + details is sent as today's single `text`.

**Thread:** "← the talks", then the original post (avatar 48/56, meta + topic, title, body, the reply count,
"report").

- **Replies:** avatar 32, "alias · 2h", text, "reply · report".
- **Depth limit 2:** indent with a 2 px rule. Deeper replies flatten with "↪ @alias", as the backend stores depth 0/1.
  "show n more" after 6.
- **0 replies:** "no replies yet. be the first."
- **Phone reply field:** sticky "add your two cents…" + "replying as {alias}".
- After the replies: "got your own tea? spill it ›".

**Empty topic:** "it's quiet in here…" + "no talks in {topic} yet. start it off?" + the CTA. While closed:
"nothing in {topic} yet." with no button.

**Teaser:** heading and CTA kept; the board rows are the hub row component.

**Density** (9 real threads, measured on v1, accepted in REVIEW-2):

| Viewport | Row height, current → proposed | Screens for 9 rows, current → proposed |
|---|---|---|
| 390 | 174 → 94 px | 2.51 → 1.16 |
| 1536 | 154 → 97 px | 2.25 → 1.24 (5 rows in the first screen) |
| 1920 | | 1.47 → 0.80 |

## Topics (shared data, the owner's decision; nothing is created or edited before approval)

- **Proposed:** plot twists · tiny wins · second opinions · just venting · nail talk. That means 2 new talk_topic
  entries, and "something else" is KEPT as the hidden home of "your own" posts (the backend files them there).
  - It is not shown as a chip or nav item; that is a theme change, because today the hub auto-appends unknown topics.
  - Alternative: relabel it "your own".
  - **Deleting or unpicking it would break every "your own" post.**
  - 0 threads move.
- **Alternative:** keep the 4 as built.

## Unchanged

- Anonymous; no name, email or login; no IP.
- Device key (decision A), burst guard, rate limits, duplicate check, flood hold.
- Moderation: blocked contacts/links/slurs, held real names, 3 reports → hidden, owner Draft/Active.
- The kill switch (`talk_settings/main.posting_open`) and its sequence.
- The backend and data model.
- 0 new font bytes.

## Fixes found in the lab (carried into the implementation)

- Override the theme's global h1–h3 serif inside the talks.
- A grid item with a z-index is stacked even when static, so the composer panel needs `z-index: auto` on desktop, or
  it rides over the sticky header.
- `base.css` zeroes a first-child heading's margin (handled in the installed `.st-talks__feed`).

## Files

- `lab/proposed.css` (v3)
- `lab/proposed_capture.py`, `lab/current_capture.py`, `lab/compose_sheets.py`
- `lab/copy.json` (v1.5.1)
- `lab/data.json` (the real threads)

Superseded variants are kept for the record and must not be shown to the owner: `lab/proposed-v0.css`,
`proposed-v1.css`, `proposed-v2-cards.css`, `proposed_capture_v2_cards.py`, `renders/archive-v2-cards/`.
