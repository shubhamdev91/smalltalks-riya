# TLK-154 + single posting switch: install plan (next st-talks lock window)

Staged in `talks\staged\src\`. The shared mirror `theme-build\src` is untouched until the lock is granted.

**What changes:**

- The posting switch moves from three section settings (`posting_live` in list, thread and start) into one snippet,
  `snippets/st-talk-live.liquid`. It outputs `on` / `off`.
- The list, thread, start and rules sections all read that one value, so the composer, reply box, Report, the
  TLK-153 notice and house rule 5 can never disagree.
- st-talks-rules gains setting `moderation_prelaunch` (TLK-154). It renders instead of `moderation` (TLK-075) while
  the switch is `off`.

**Upload order.** Each step keeps the storefront consistent, with the switch off throughout:

1. `snippets/st-talk-live.liquid` (new, value `off`).
2. `sections/st-talks-rules.liquid` (reads the snippet; new setting with a TLK-154 default).
3. Templates `blog.json`, `metaobject/talk_topic.json`, `metaobject/talk_thread.json`:
   - drop the `posting_live` keys;
   - add `moderation_prelaunch`.
   The list, thread and start sections still read their old setting until step 4, and the default false matches
   `off`.
4. `sections/st-talks-list.liquid`, `st-talks-thread.liquid`, `st-talks-start.liquid` (read the snippet; the
   `posting_live` setting is removed from the schemas).

**Before writing:**

- Fetch the remote checksums of all 7 changed files plus the new snippet's absence. They must equal the last
  st-talks upload:
  - list 2b427dfb
  - thread 56fd11fb
  - start d4b982af
  - rules 18fa01a1
  - blog/topic b1aedb9a
  - thread template f2da8414
- Copy `talks\staged\src\*` into `theme-build\src\`, then stage → PUT md5 check → upsert in the order above.
- No locale change: TLK-154 is a section setting, like TLK-075.
- **Also in this window:** TLK-148 v1.4.4, "To stop spam, we keep a scrambled code for your device (never your IP
  address) and delete it within 30 days."
  - It is staged in the rules schema default and in the `privacy` setting of all 3 templates.
  - Verify it on hub, topic and thread.

**/blogs/news** (blog.json also serves the default News blog):

- **Baseline, 10 Oct before install** (`talks\staged\news-baseline.json`, `qa\talks\news-before-tlk154-390.png`):
  200, H1 "News", 0 rows, no talks chrome, no Liquid error, scrollWidth 390.
- **After install:** it must be identical. Compare against this baseline and report it.

**Verify** at 390 with the switch off, on hub, topic and thread:

- TLK-153 is visible.
- House rules show TLK-154; TLK-075 is absent.
- There are no Liquid errors and no Report buttons.
- md5 readback.

Then release the lock.

**Later (posting ON):** run `python -I talks/set_live.py on` from theme-build/src, then upload
`snippets/st-talk-live.liquid` only.
