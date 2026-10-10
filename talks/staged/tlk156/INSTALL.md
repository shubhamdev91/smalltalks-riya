# TLK-156: zero-reply rows follow the posting switch (small window of its own)

**INSTALLED 10 Oct 15:50Z.**

- **Pre-write:** remote md5s c0eb3cb3 / 39181ddd. `locale_insert.py` was re-run on that base: 1 line inserted, the
  other 658 byte-identical.
- **Readback:** locale 32104278, row 6e40e666.
- **Rows:** hub (9 rows) and tiny-wins (3 rows) at 390 and 1366 all read "No replies yet" with 0 chevrons.
- **Errors:** 0 Liquid errors, 0 "translation missing", 0 page errors.
- **Page heights:** equal to the baseline (390: 3897 / 2420 / 1737).
- **Thread and /blogs/news:** fine.
- **Header:** the baseline diff there is st-foundation's smaller "the talks" wordmark (st-header.liquid and
  st-landing.css, 15:45:35Z), not TLK-156.
- **Lock:** released.

**Ask:** orchestrator, 10 Oct. While posting is OFF, hub and topic rows said "First reply's yours ›", an invite to
something nobody can do yet. It also contradicted the landing teaser's "no replies yet" (LND-066).

**Copy:** st-copy v1.4.11, TLK-156.

- Key: `small_talk.talks.live.no_replies_closed` = "No replies yet".
- No chevron, and sentence case.
- When posting opens, rows go back to TLK-010 "First reply's yours ›" with no further change, because they read the
  same switch.

Staged in `talks\staged\tlk156\src\`. Theme 186651934933 only.

| File | Expected remote md5 (= mirror, checked 10 Oct) | New md5 |
|---|---|---|
| snippets/st-talk-row.liquid | 39181ddd918b6bda922748ab985dae0c | 6e40e66622b9e045a61dd4ee19463e12 |
| locales/en.default.json | c0eb3cb3a3109cde0620c252eb3459e4 | 32104278d43b1fb213c0a4e9dabc71a8 |

**Changes:**

- **Row:** it renders `st-talk-live` once per row (the one switch).
  - Replies > 0: the count + chevron, unchanged.
  - 0 replies and posting on: "First reply's yours ›", unchanged.
  - 0 replies and posting off: "No replies yet", no chevron.
  - Only st-talks-list renders this snippet. st-talks.js builds rows only while posting is open, so it is unchanged.
- **Locale (insert-only):** one line after `"prelaunch"` in `small_talk.talks.live`.
  - `python -I talks/tools/locale_insert.py <current remote file> <out>` proves the other 658 lines are byte-identical
    and that the new key parses.
  - **If the remote md5 differs at write time** (another session inserted keys): fetch the current remote file, re-run
    the tool on it, and upload that output. The new md5 changes, but the proof must still say "1 line inserted".

**Pre-check:** the new text was simulated in the preview DOM on the hub at 390 and 1366. 9 rows switched, and the
row heights did not change (390: 197, 1366: 153). Shot: `qa/talks/tlk156-row-sim-390.png`.

## Order (under a lock)

1. Re-fetch both remote md5s.
2. Locale first. The key exists before anything uses it.
3. Then the row snippet.
4. Verify: hub, a topic and a thread at 390 and 1366.
   - Rows read "No replies yet" with no chevron.
   - No "translation missing", no Liquid error.
   - /blogs/news unchanged.
5. Read back the md5s. Release the lock.
