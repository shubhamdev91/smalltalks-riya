# the talks v4 window: install plan (staged 11 Oct; write only after a fresh lock grant)

**Scope:** ONE window on the build **186651934933** only. Never the live theme: MAIN is 186699514069 ("Store v1.1"), so
re-check `themes { role }` first. The window covers:

- the owner-approved v4 UX (qa/talks-ux/README.md);
- posting ON (the approved posting-on staging: HD avatars, a11y example blocks, st-talk-live `on`);
- the 2 new topic entries.

The header wordmark IS in this window: the owner picked **V1** on 11 Oct (st-fable qa/talks-ux/wordmark/V1-FINAL.md).
st-talks is the single writer of `sections/st-header.liquid` under this grant.

**Backend prerequisite:** `/api/talks` shows build **b27475e7fe2b** (owner OK given 11 Oct; waiting on the owner's v0
Publish), and the talk_reply `parent` field exists (done 11 Oct, read back).

## Files (base = remote md5 re-read 11 Oct ~05:30Z; staged in `talks/staged/v4/src/`)

| File | Base (remote) | New |
|---|---|---|
| locales/en.default.json | 79b4547d3347f921f092e57b2b4551cc | bd4ec6075e42ad03270f1c201a9f8c2b (insert-only: +88 lines, `small_talk.talks.live.v4`; regenerate from the remote with `talks/tools/locale_insert_v4.py` if the base moved) |
| snippets/st-talk-topics.liquid | NEW | 1183a51737cf057debc462f7d45c99ff |
| snippets/st-talk-config.liquid | 41dec54141d5a76086a3f6795b7f28d0 | 8c79137f2474fab7f7009aff7e6f70b2 |
| snippets/st-talk-avatar.liquid | 59dd5e9409145891c6f20efc1d340ebe | 4b5745382dec4fee27d14c0d9cfd132c (HD, approved) |
| snippets/st-talk-row.liquid | 6e40e66622b9e045a61dd4ee19463e12 | f01b4ceedfe8fc8f43da5a1c6a1a0c34 |
| snippets/st-talk-reply.liquid | e6109789bfdf8bb1db2af7db0694c423 | 856cc40d7928533747ba5767ac33a6d4 |
| snippets/st-talk-composer.liquid | 4a4c480bf27427762eadd324dbe70551 | cf2bacc2faa5d05297373fdb09e09842 |
| blocks/st-talk-example.liquid | 73fcea2109bc15d541e170d2ddbfc616 | 44941c76d84707a6e1bd1f12202caa3d (a11y, approved) |
| blocks/st-talk-examples.liquid | fef12c7b70bfd12330683d0d4daa29dc | b5162be3a695216dc3bdf9c3e531bb8e (a11y, approved) |
| assets/st-talks.js | f3407219a7f09a3b2abbd71e7c8c6bb6 | a51e149863fc9591d5377d74836a039b |
| snippets/st-talks-wordmark.liquid | NEW | 6d1e718b0bdcb7452b016ba797f38abb (V1 outlined SVG, st-fable's st-talks-wordmark-v1.svg d31734b6, generated, not retyped) |
| sections/st-header.liquid | 49e3c88be55f94bd69cd1f15333492b5 | 265a403a21d50088de31ad0800ec48b2 (V1 mark + ↗ in the link, drawer mark, sprite defined once) |
| sections/st-talks-list.liquid | 04fdc439c7b0f16e41df6eb4c3572d38 | 7c80c666033a1a0d4c1286638f8295a6 |
| sections/st-talks-thread.liquid | 2b96669cec06e3cad752e30fb0b08d44 | 2952071dac76a0763e599e3afc095b64 |
| sections/st-talks-rules.liquid | 565f3fdca4711719b5f96cef215a68d0 | 442edc6d2cfaaf3dba77f1e3f76814d6 |
| templates/blog.json | e66d1e5dc6320994a5897d58723ffad5 | b700e9b6a0cf0c481b0f6c63ef28c916 |
| templates/metaobject/talk_topic.json | e66d1e5dc6320994a5897d58723ffad5 | b700e9b6a0cf0c481b0f6c63ef28c916 |
| templates/metaobject/talk_thread.json | f5cc2125da8fe4b7bae3d0ebe4ecda4d | 39c32ed13a1e7759d311b01a89a6b6a6 (drops the old "start" panel section) |
| snippets/st-talk-live.liquid | 82c0b8700973b0b34166154b359dbb80 | 6e1a4ff06c7a5c3a17714a3af702c216 (`on`, last) |

**Wordmark V1:**

- The header defines the 9 KB path once, as a zero-size sprite. The header link, the drawer and the hub title draw it
  with `<use>`, each with the visually hidden name "the talks".
- The header's hidden text is set in DM Sans. Caveat (st-caveat.woff2, 59 KB) is then no longer downloaded on any page
  except the homepage, whose hero and landing still use it: a net saving.
- Lab, injected on the preview with no write (`talks/tools/v1_header_lab.py`), ALL PASS:
  - mark 57 × 16.3 at 320 and 69.5 × 19.9 at 390/1536/1920;
  - link 44 px tall, accessible name "the talks";
  - the ↗ sits after the mark, at x-height;
  - bar 69/76 px, unchanged;
  - hub title 117 × 33.5 (phone) and 152 × 43.5 (desktop).
  Crops: `talks/staged/v4/v1-{header,hub}-*.png`.

**Untouched:** st-talks-start, st-talk-alias, st-talk-time, st-talk-ago.js, st-teaser (st-foundation),
page.the-talks.json and settings_data.

**Shared:** st-teaser renders st-talk-avatar (HD) and st-talk-live. With live `on`, its zero-reply stub adds
"· be the first ›" and its pre-launch line goes, both by design (LND-066/067).

## Shared data in this window (owner-approved)

**New talk_topic entries** (labels lowercase per TLK-006):

| Handle | Label | Position | Pickable |
|---|---|---|---|
| `second-opinions` | second opinions | 4 | true |
| `just-venting` | just venting | 5 | true |

Read both back after creating them. talk_topic has no Draft state, so the live theme's old hub also lists them as
chips at once, with empty states, until the owner publishes. Create them just before the E2E.

**Asked, not done:** TLK-006 wants the existing labels lowercase in the data ("Plot twists" → "plot twists", "Tiny
wins", "Nail talk"). That edits shared data, so it needs the orchestrator's OK.

## Order (after the grant)

1. Re-fetch the remote md5 of every file above. Each must equal its Base; otherwise stop and report.
2. Lint all Liquid (`theme-build/tools/liquid_lint.py`).
3. Upload in this order, reading back the md5 after each batch:
   1. the locale;
   2. the snippets, except live (wordmark, topics, config, avatar, row, reply, composer);
   3. the blocks;
   4. st-talks.js;
   5. the 4 sections (header, list, thread, rules);
   6. the 3 templates.
   Posting is still OFF here.
4. Check the build preview (posting OFF) at 320/390/1280: the hub, a topic page, a thread and /blogs/news. Look for
   Liquid errors, horizontal overflow and console errors.
5. Upload st-talk-live `on`, then create and read back the 2 topics.
6. Set `posting_open` "true" (gid://shopify/Metaobject/616028176597) and confirm `{"open": true}`.
7. Run the E2E on the build preview at 320/390/1280: post, reply, nested reply, report, refusals (contact, link,
   might_name, slow-down).
8. Delete every test thread, reply and signal row, and read back that they are gone, along with the topic lists. Set
   `posting_open` "false" and confirm `{"open": false}`. Report, then release the lock.

## Pre-checks done (no theme write)

- `talks/tools/v4_js_lab.py`: **113/113 PASS** at 320/390/1280, on the staged script and CSS with a mocked
  /apps/talks. Covered:
  - fold/expand with focus;
  - "continue this thread" at 4/6 levels;
  - the inline box: one at a time, Esc returns focus;
  - nested placement and depth;
  - refusals keep her words (might_name, busy, contact, too_short);
  - nudge, shuffle and "your own";
  - the optimistic row;
  - report and fold;
  - the payload carries no name or email and respects the 2.6 s dwell.
  Shots: `talks/staged/v4/lab-{hub,thread}-{320,390,1280}.png`.
- **Liquid lint:** OK on all 12 Liquid files. The JSON templates parse. The locale is insert-only (proof in the tool).
- **Escaping audit** (the backend suite's rule): every user field is escaped; the JS has no HTML sinks; the only
  fetch target is cfg.endpoint.
- **Weight:**
  - st-talks.js +4.2 KB raw (≈ +1.3 KB gz), still loaded as a low-priority module;
  - talks CSS +5.4 KB raw (≈ +1.2 KB gz);
  - 0 new fonts (the wordmark is the site's own Caveat);
  - 0 new requests. The HD avatar sheets are as approved in the posting-on window.

## Installed 11 Oct 2026 06:12–06:33Z (final md5 = remote checksum, read back)

| File | Installed md5 |
|---|---|
| assets/st-talks.js | a51e149863fc9591d5377d74836a039b |
| blocks/st-talk-example.liquid | 44941c76d84707a6e1bd1f12202caa3d |
| blocks/st-talk-examples.liquid | b5162be3a695216dc3bdf9c3e531bb8e |
| locales/en.default.json | acc87833ed2cba81ba86ceab36cd1698 |
| sections/st-header.liquid | 265a403a21d50088de31ad0800ec48b2 |
| sections/st-talks-list.liquid | e8caf1b5ca46b1e4680e48c7f476b4b8 |
| sections/st-talks-rules.liquid | 6a202a1914fc7c16496e78698e19567f |
| sections/st-talks-thread.liquid | 9a6b23eeedde573cc8484c374a1e60ab |
| snippets/st-talk-avatar.liquid | 4b5745382dec4fee27d14c0d9cfd132c |
| snippets/st-talk-composer.liquid | 62e5c9ad8abe08af29738674fa1a5f04 |
| snippets/st-talk-config.liquid | ddba95f847b716992971556177fa3064 |
| snippets/st-talk-live.liquid | 50d60ee0c1301e8f0758fa3ef511acad |
| snippets/st-talk-reply.liquid | b4c372e697e8d7ad5bf15e72f49d2f9c |
| snippets/st-talk-row.liquid | 0750e9f8e2710d02421963fa71c13916 |
| snippets/st-talk-topics.liquid | 1f8ef12ec0acbfdbbfe8f83814ca6663 |
| snippets/st-talks-wordmark.liquid | 6d1e718b0bdcb7452b016ba797f38abb |
| templates/blog.json | b700e9b6a0cf0c481b0f6c63ef28c916 |
| templates/metaobject/talk_thread.json | 39c32ed13a1e7759d311b01a89a6b6a6 |
| templates/metaobject/talk_topic.json | b700e9b6a0cf0c481b0f6c63ef28c916 |

Changes after the grant, all inside this window:

- TLK-183 "all house rules ›" with the accessible name "read all the house rules": locale +2 keys, in the rules card.
- Chip, nav and topic case set lowercase with CSS only (orchestrator); the talk_topic labels are unchanged.
- **CSS moved into always-rendered files.** Shopify ships a file's stylesheet only on pages that render it
  (`compiled_assets/styles.css?subset=`).
  - The shared base, the writing/reply box and the buttons moved into st-talk-config, which every talks page renders.
    An inert `<template>` there renders st-talk-avatar, so its CSS ships too.
  - The row CSS moved into st-talks-list.
  - The comment CSS moved into st-talks-thread.
- **st-talk-live.** Its `{% doc %}` block stopped the captured value from ever equalling "on", so posting stayed
  hidden. It's now a `{%- comment -%}`. Verified: `"live": true`, with the form and dock rendered.

Verified on the preview:

- `talks/tools/v4_preview_check.py off`: 18/18 PASS (hub, topic, thread and news at 320/390/1280; home, PDP and journal
  at 390/1536). Results:
  - no Liquid errors and no overflow;
  - the wordmark defined once per page; header link 44 px, mark 57×16.3 (320) and 69.5×19.9;
  - Caveat now loads on the homepage only.
- `talks/tools/v4_aftershots.py`: posting ON with the store switch closed. Shots in `qa/talks/v4-after/`.
  - The composer, dock and reply box render; the dock hides while typing.
  - A real post through /apps/talks got 403 and TLK-130; her text was kept and nothing was saved.
  - The drawer mark renders on home, PDP and journal.
