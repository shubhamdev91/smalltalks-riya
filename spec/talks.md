# the talks (blog index): board 4 frame 1

**Real feature (orchestrator, round 2):** Shopify blog `the-talks`.
- Threads are articles posted by Small Talk.
- Replies are native comments under an alias, auto-published.
- A "Start a talk" suggestion form sits below the list.

This frame is the **blog index**.

Crop: `crops/talks@390.png` (+ `-grid`); scale 1.66. Same header as the landing.

| Element | Box | Spec | Data source |
|---|---|---|---|
| H1 "the talks" | x 45–350, y 150–228 | Source Serif 4 Bold, 74 px, −0.03em, `--st-burgundy`. Lowercase. | blog title |
| Tagline "a little less filtered." | x 95–300, y 233–262 | `--font-talks-tagline`: Source Serif 4 **Italic** (true italic file) wght 400, opsz 20, 28 px, −0.01em, `#c0142f` (round 10, board-verified). | section setting |
| Sub | x 30–362, y 268–292 | DM Sans 400, 18 px, `#1a1a2e`. | section setting |
| Pill "Start a talk ↗" | x 73–318, y 318–370 | Full pill `#920324`, white Barlow Semi Condensed 600, 22 px. Anchors to the Start-a-talk form (#start-a-talk, at the page bottom or on conversation.md). | — |
| Topic chips | y 403–442 (→ 44 tall) | "All" selected (fill `#c0142f`, white DM Sans 600, 13 px) and the topic chips (fill `#fdf0f0`, text `#5a5a6e` → use `--st-muted-text` for contrast). Horizontal scroll if they overflow. | **real:** blog article tags (Plot twists / Tiny wins / Nail talk / Friendship…). Each chip links to `/blogs/the-talks/tagged/<tag>`. |
| Label "Example conversations" | x 20–205, y 497–515 | DM Sans 400, 15 px, `--st-muted-text`. | Change the label to the register's wording for real threads (st-copy). |
| Thread row ×N | starts y 535, pitch ~200 px | Avatar Ø 90 at x 18–108. Text column x 128–370: author line DM Sans 400, 15 px muted (left) + date right; title DM Sans 700, 22 px, `#111`, lh 1.1; excerpt DM Sans 400, 17 px, `#373f8b`; "N replies ›" DM Sans 400, 15 px, muted + chevron 2 px. Whole row is one link (≥44 px). | title = `article.title`; excerpt = `article.excerpt`; author line = "Small Talk" (the posting account) or a thread alias from an article metafield; date = `article.published_at` (relative or "9 Oct"); replies = `article.comments_count` (hide when 0; singular "1 reply"). |
| Avatar | Ø 90 circle | **No photos.** Thread avatar = a set nail: one sprite cell (col 0) of the set tagged on the article, on a blush `#fbe3e6` disc, nail rotated −20°. Fallback: alias initial in Fraunces 900, 40 px, burgundy on blush. | article tag `set:<handle>` → `artwork/nails/web/<handle>.webp` |
| Pagination | under the list | Board doesn't show it. Horizon default "Load more"-style pill, outline `--st-outline-red`. | `paginate blog.articles by 10` |
| Handwritten panel | x 18–375, y 1140–1295, radius 12, fill `#fdecec` | "Different thoughts. / Same energy." Kalam Light, 34 px, `#2b39c4`, −6°, + hand-drawn heart (1.5 px). | section setting |
| Footer (inner pages) | y 1390–1530 | Logo left x 22–98 (stacked, 50 px tall). Link columns at x 142 and 272: Shop/Our Story/the talks and Journal/Help, DM Sans 400, 14 px, `--st-muted-text`. Icons centred y 1478, Ø 18 at x 155 / 197 / 238. Legal y 1517, 12 px. | footer settings |

Real-data rules: no invented reply counts, timestamps or handles. Every number and date comes from Shopify. Aliases are what commenters typed (no @ prefix rendered). An empty state is needed when the blog has no threads (copy from st-copy).
