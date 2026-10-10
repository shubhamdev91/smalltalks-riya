# Shop (collection): board 5 frame 1

Crop: `crops/shop@390.png` (+ `-grid`); board scale 1.327. y values are css px from the frame top.

| Element | Box (x, y) | Spec |
|---|---|---|
| Header | 0–390, 0–70 | Same as the landing header (owner: landing header everywhere). Board 5 draws "the talks" in red sans; ignore that. |
| H1 "Pick your plot twist." | x 18–280, y 70–170, 2 lines | Source Serif 4 Bold opsz 60, 54 px, lh 0.92, −0.02em, `--st-burgundy` `#820622`. |
| Annotation "Same nails. Different moods." + arrow | x 85–295, y 175–222 | Kalam Light, 19 px, `--st-hand-blue` `#3653c7`, −4°, 2nd line indented 45 px. Hand-drawn arrow ↓: 1.5 px stroke, curls down-right to x 290, y 220. |
| Filter chips | y 234–274 (40 → 44 for touch) | 3 pills: "All sets" x 15–123, selected (fill `#920324`, white DM Sans 600, 16 px); "Everyday" x 133–243 and "Statement" x 253–373, unselected (white, 1 px `#e0e0e6`, text `#1a1a2e`). Radius full. |
| Product grid | x 15–375, starts y 292 | 2 columns: x 15–190 and 203–375 (175 px wide, 13 px gutter). Rows every 236 px: image 0–160, name/price 170–192, link 200–216. Last row (Pinky) single, left. |
| Card image | 176 × 172 tile (2-up), radius 6; last odd card 223 × 155 | Ground `--st-tile-<set>` (board-5 medians, brighter than the hero mid-tones). Composition per tile below. |
| Product name | left, y +170 | **Sans** (round 6): `--font-card-name` IBM Plex Sans Condensed Bold, 21 px, `--st-red` `#a31a33` (runner-up DM Sans 800). |
| Price | right-aligned at the card's right edge | `--font-price` IBM Plex Sans Condensed 700, 17 px, `--st-price` (round 7). |
| "View set →" | left, y +200 | DM Sans 500, 15 px, `#4e6dcd` (hand-blue family), 1 px underline under the text only, → glyph. |
| Footer | y 1205–1250 | 2 centred rows of links separated by " · ": Shop · Our Story · the talks · Journal · Nail Guide / Contact · Shipping · Returns · Privacy · Terms. DM Sans 13 px, `--st-muted`. Hit areas ≥ 44 px. |

Notes:
- Board error: the "Cherry Repeat" product name is ignored, so it's Diet Cherry. The Diet Cherry package shows the Coke can, which is locked packaging and acceptable.
- Board order is On Me, Brainwave, Green Flag, Shaadi Shift, Diet Cherry, Wild Card, Pinky Promise. Prices come from Shopify, never hard-coded.


## Tile composition (round 5, measured on board 5 at 390; % of the tile)
Two patterns appear on the board:

**A. Box + loose nails** (On Me, Shaadi Shift, Diet Cherry, Wild Card)
- Box: `packaging/web/<set>@1.3x.webp`, height 85% of the tile (≈146 px), left 8%, top 8%. Width follows the asset (~62% of the tile). No baked shadow; CSS `drop-shadow(0 4px 8px rgb(0 0 0 / .18))`.
- Loose nails: a vertical stack in the right column, x 76–94%. Nails are sprite cells from `nails/web/<set>.webp`, each ~32 × 48 px visible (cell scaled ×0.15), rotated +15…+20° (tips lean right). Stacked pitch ~24% of the tile height, first at top 8%. The stack sits 4–8 px right of the box edge; the nails don't cover the box. The board shows 4 nails on three tiles and 3 on Wild Card (the orchestrator brief said 3; the board wins):

| Set | Nails top→bottom (sprite cols) | Board reads |
|---|---|---|
| On Me | 0, 2, 1, 0 | burgundy, tortoise, gold, burgundy |
| Shaadi Shift | 1, 2, 0, 2 | red, blush, flower, blush |
| Diet Cherry | 1, 0, 2, 1 | red, silver, blush French, red |
| Wild Card | 1, 0, 2 | lime, checks, blush |

**B. Board shows a wider, near-square box** (Brainwave, Green Flag, Pinky Promise)
- On the board these boxes are drawn ~1:1 (x 8–92%, y 8–92%), with the package's own nail tray as the right-hand column. The approved package assets are portrait (aspect ≈0.73) and can't fill that without distortion. **Build rule:** treat them like pattern A (box 85% tall, left 8%) and fill the right column with the same loose-nail stack, which reproduces the board's tray-of-nails column:

| Set | Nails top→bottom (sprite cols) | Board tray reads |
|---|---|---|
| Brainwave | 0, 1, 0, 1 | cobalt, white, cobalt, white |
| Green Flag | 1, 0, 1, 0 | green, blush, green, blush |
| Pinky Promise | 0, 0, 0, 0 | lilac with burgundy tip ×4 |

**Last card (odd count, phones):** single card, left-aligned, x 14–237 (≈223 px wide, 57% of the viewport), image 155 px tall. Same name/price/link rows below. On the board this is Pinky (pattern B). Its ground reads cobalt `#045af1`, which looks like box art bleeding; st-fable/owner to confirm cobalt vs campaign violet.

Board ordering of tiles is unchanged (see above).
