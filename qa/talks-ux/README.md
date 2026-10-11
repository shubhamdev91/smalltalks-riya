# the talks: UX v4 (owner round 2, 10 Oct)

**Roles:** st-talks leads; st-fable does the wordmark and acceptance; st-copy writes.

**Status:** lab only, no theme, data or deploy changes. v3 (approved by st-fable, not by the owner) is archived in
`renders/v3-owner-set/` and `README-v3.md`.

**The owner's asks (relayed by the orchestrator):**

- Reddit-style threads: a vertical line per level, and reply to any comment mid-thread.
- A simpler, inviting composer with the WRITING BOX AS THE HERO ("we need them to spill").
- Writing inside threads should feel the same as starting one.
- A new "the talks" wordmark.
- Minimal copy.

## Sheets (`renders/compare-*`, CURRENT | PROPOSED, 390 × 844 and 1536 × 703)

| Sheet | What it shows |
|---|---|
| compare-hub | The hero writing box at the top of the hub, then topic filters, then the feed (9 real threads, 0 replies). |
| compare-composer | Starting a thread: the same hero box, focused (the typed starter is her own draft, not activity). |
| compare-thread | Reddit-style nesting, under the visible band "example replies: layout preview, not real posts". |
| compare-inline-reply | "reply" on a mid-thread comment opens the same box, smaller, right under it (banded example). |
| compare-header-wordmark-{390,1536} | NOW vs V2 (refined original Caveat + swash + ↗) in the site header. Every other frame uses V2. |

**CURRENT:**

- Hub and composer: the build in the posting-ON state.
- Thread and inline reply: today's markup with the same banded examples. Today only 2 levels exist, and "Reply" jumps
  to the bottom form.

## What changes

**Hero box, start a thread:**

- A big box at the top of the hub (≈ 5 lines of writing room on phone (196 px) and desktop (216 px, 18 px text)) with a warm two-line placeholder; the first
  line becomes the headline.
- **Inside the box:** one "need a nudge?" chip that drops in a starter.
- **Under the box:** the topic as ONE pre-selected chip ("plot twists ▾") and a big "post it".
- **Small print:** "posting as {alias} · shuffle" and one rules line.
- **Phone:** the sticky "spill your tea" scrolls to the box and focuses it; it hides while typing.

**Threads, Reddit-style:**

- A flat list in display order, with one thin line per ancestor level (16 px phone / 22 px desktop).
- **Fold:** each comment's own line is its fold toggle. Folded, it reads "{n} more replies".
- **Depth:** 4 levels visible on phone, then "continue this thread ›".
- **Each comment:** a 24 px initial avatar, "alias · time", the body, and "reply · report".
- **Reply anywhere:** "reply" opens the same friendly box, smaller, inline under that comment, with
  "replying to {alias} ✕", "cancel" and "reply".
- **Under the original post:** the same small box for replying to the talk itself.

**Copy:** st-copy register v1.7, with no drafts left.

- **Hero placeholder (TLK-173):** "what's the tea? start from the beginning…" / "your first line becomes the
  headline."
- **Nudge (TLK-175):** "need a nudge?"
- **Every inline box:** TLK-026 "add your two cents…", with TLK-134 "replying to {alias} ✕".
- **Threads:**
  - TLK-178 "continue this thread ›";
  - TLK-179 "−" / "+ {n} more replies";
  - TLK-180 "replying to a hidden comment".
- **Rules:** one short line, plus the rail card the owner liked.

**Wordmark:** the owner rejected A/B/C and kept the ORIGINAL Caveat, refined. Every frame uses st-fable's recommended
**V2**:

- **The lockup:** Caveat 700, −0.015em, "the" + 0.2 em + "talks", rotated −3°, ink #0d0b10, with a soft red swash under
  "talks".
- **Site header:** adds a small ↗ (DM Sans 500, 0.5 em, aria-hidden, inside the 44 px link).
- **Hub title:** 40/52, no arrow.
- **Spec:** `wordmark/CAVEAT-REFINE.md`.
- **Fonts:** a lab-only data-URI font. Production is an outlined SVG mark; the arrow stays live text.

**For the owner:**

- `renders/compare-header-wordmark-{390,1536}.png` (NOW vs V2 + arrow);
- st-fable's `wordmark/caveat-sheet.png` and `wordmark/caveat-1536-header-2x.png`, so the owner can also pick V1, V3
  or V2 at +10 %.
- `options-sheet.png` (A/B/C) is NOT in the owner set.

**Topics:** locked by the owner (TLK-006): plot twists · tiny wins · second opinions · just venting · nail talk.
"Something else" stays hidden as the home of "your own" posts. The 2 new topic entries get created in the talks window.

## Data and backend (owner approval needed with the design)

- **Nesting:** `talks/staged/nesting/PROPOSAL.md`. ONE new optional talk_reply field, `parent`
  (metaobject_reference → talk_reply). There are 0 replies today, so nothing to migrate.
- **No review queue + security:** `talks/backend/SECURITY-v5.md`.
  - Might name someone → refused at submit (TLK-181), nothing saved.
  - Flood → refused (TLK-182).
  - Every security item has a test.
- **One backend deploy:** local build **b27475e7fe2b** (v5 + v6 + v7), 53 tests passing.

## Unchanged

- Anonymous; no name, email or login; no IP.
- The device key and burst guard.
- Moderation as built.
- The kill switch.
- No fabricated activity in any unbanded frame.
- 0 new font bytes (unless st-fable's wordmark needs a font).

## Files

- `lab/proposed.css` (v4 is appended to the v3 base)
- `lab/proposed_capture.py` (v4)
- `lab/current_capture.py` (`examples` mode)
- `lab/compose_sheets.py`
- `lab/copy.json` (`v4` keys)
- Superseded: `proposed-v0/v1/v2-cards/v3.css`, `proposed_capture_v3.py`, `proposed_capture_v2_cards.py`,
  `renders/archive-v2-cards/`, `renders/v3-owner-set/`.
