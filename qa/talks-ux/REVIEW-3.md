# the talks UX v3: review 3 (st-fable, 10 Oct 2026)

Reviewed: `renders/compare-*` and `proposed-*` (13:19–13:21), against REVIEW-2.
**Verdict: OWNER-READY.** The owner set can go out as is.

- **Real state only:** every hub frame's first row reads "no replies yet", and the thread shows "no replies yet. be the
  first.".
  - The reply design appears ONLY in `proposed-thread-example-*`, under the striped "example replies: layout preview,
    not real posts" band, with neutral aliases (alias one / two / three). This meets the standing rule.
- **No DRAFT text:** the composer fields are empty.
  - Before build they need st-copy's placeholders, and each field needs a programmatic label
    (`<label>` / `aria-labelledby`), not only a placeholder.
  - For the owner set, add one caption line: "field hints come with the copy pass".
- **Desktop composer:** opens inline at the top of the feed, fits in one 1536 × 703 screen, and the rail stays sticky.
  **Two rows of chips: ACCEPTED.** Keep the 15 px chips and the 44 px hit area; don't shrink them to fit one row.
- **Topics 5 vs 4:** both crops, with pros and cons, go to the owner. That's their call.
- Everything else is as approved in REVIEW-2 (type, rows 94 / 97, thread nesting, sticky bars, pre-launch, empty
  state, teaser).

**Build gate (later, st-talks' window):**
- the final copy from st-copy (placeholders, starters);
- labels on the fields;
- my after-shot acceptance on the preview at 390 / 1536 / 1920 with the real data.

## Final look (st-copy v1.5.4 composer lines in place): OWNER-READY, unchanged verdict
- The composer reads well: "what's the tea, in one line?" (hidden label "headline", required) and "the rest of the tea
  (optional)". The starters drop into the title. There is no DRAFT text and no empty field.
- The desktop chips wrap to 2 rows: ACCEPTED (as above). Don't shrink them.
- At build time, give the details field a hidden label too, alongside the title's.
