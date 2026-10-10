# Conversation (thread page): board 4 frame 2

Crop: `crops/conversation@390.png`; scale 1.893.

**Real feature:** this is the `article` template of blog `the-talks`.
- The thread is the article.
- Replies are native Shopify comments: the name field is the alias. The blog is set to auto-publish comments.
- The reply box is the comment form.
- The "Start a talk" panel is a suggestion form: a contact form tagged `start-a-talk`, which sends to the team.

| Element | Box | Spec | Data source |
|---|---|---|---|
| Back "← Back to the talks" | x 28–190, y 100–120 (44 px hit) | DM Sans 500, 15 px, `#1a1a2e`, ← 1.5 px. | `blog.url` |
| Thread avatar | Ø 88, x 22–110, y 158–246 | Set-nail avatar, same rule as talks.md. | article tag `set:<handle>` |
| "•••" overflow | x 340–365 | **Omit.** No menu exists. | — |
| Author line | y 262–282 | DM Sans 400, 16 px, `--st-muted-text`: "{author} · {date}". | `article.author`, `article.published_at` |
| Title | x 25–350, y 297–365 | DM Sans 700, 28 px, `#111`, lh 1.08. | `article.title` |
| Body | x 25–295, y 372–420 | DM Sans 400, 19 px, `#5a5a6e` → `--st-muted-text` for contrast. | `article.content` |
| Reply count | right, y 425–445 | DM Sans 400, 16 px, muted. "{n} replies"; hide at 0. | `article.comments_count` |
| Reply ×N | first at y 490, pitch ~205 | 3 px rule `#d0204a` at x 30 spanning the reply. Avatar Ø 72 at x 55–127. Text column x 145–365: alias line DM Sans 400, 15 px, muted ("{alias} · {date}"); body DM Sans 400, 17 px, `#1a1a2e`, lh 1.45. | `comment.author`, `comment.created_at`, `comment.content`; paginate 20 |
| Reply avatar | Ø 72 | **No photos.** Alias initial: first letter of `comment.author` in Fraunces 900, 32 px, white on a set colour picked by a hash of the alias (one of the 7 campaign colours; white text only on brainwave / diet-cherry / green-flag / pinky, ink on the others). | derived |
| Hearts ♡ and "•••" on replies | | **Omit.** There's no like system, and no fake counts. | — |
| Reply box | x 22–375, y 920–990 | Avatar Ø 66 (initial placeholder "?") + field x 105–375, 60 px, white, 1 px `#ebe6e6`, radius 30. Placeholder "Add a reply…" in `--st-placeholder`. Circular submit Ø 52 `#a80f2a` with white ↗. On focus, it expands to show the required alias (name) and email fields (Shopify's comment form needs both; the email is not shown publicly). | `{% form 'new_comment', article %}`; success / moderation messages from st-copy |
| "Start a talk" panel | x 18–375, y 1010–1595, radius 12, fill `#fdf1f0`, id `start-a-talk` | H2 Source Serif 4 Bold, 40 px, `#b00818`. Sub DM Sans 400, 16 px, `--st-muted-text`. Labels DM Sans 700, 17 px. Fields white, 1 px `#ebe6e6`, radius 6, 44 px (textarea 88). Select with a red chevron `#d0204a` 2 px. Helper 12 px `--st-muted-text`. Submit: full pill `#a80f2a`, Barlow Semi Condensed 600, 24 px, white. | `{% form 'contact' %}` with `contact[topic]`, `contact[title]`, `contact[body]`, `contact[alias]`, `contact[tags]=start-a-talk`; labels from the register (PG-084…095) |
| Footer | y 1610–1750 | Inner-page footer (talks.md). | |

Real-data rules: every count, date and alias is real. A thread with no replies shows the reply box only, plus an empty-state line from st-copy. Comment spam protection is Shopify's built-in reCAPTCHA (it can't be styled away; leave room under the form).
