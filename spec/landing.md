# Landing: board 3 (read down, then right), plus teasers / FAQ / footer

Source: `3.jpg`. The four columns were cut and scaled to 390 wide:
- `crops/landing-col{1..4}@390.png`
- `…@390-grid.png`: cyan line every 39 px (10%) and every 100 px of height
- `…-traced.png` / `…-beeline.png`: the auto-traces, for checking

Column scale factors are 1.548 / 1.632 / 1.632 / 1.605 (board px → css px).
**y values are css px from the top of that column's crop.** Each section also lists its height. Element y values are absolute within the column; subtract the section's y0 for section-relative positions.
Accuracy is about ±8 px. Hand-traced items are marked (h).

Order (= copy 03-landing): hero → tiles → Diet Cherry → the talks → Brainwave → Green Flag → Journal → Nail Guide → Shaadi Shift → On Me → Wild Card → Pinky Promise → Shop all / FAQ / footer.

## Section table
| Section | Col · y0–y1 · height | Ground (mid) | Glow inner → outer · centre (x%, y% of section) |
|---|---|---|---|
| Hero (On Me) | 1 · 69–722 · 653 | `#fbb804` | `#fcc90a` → `#e8a005` · 49, 22 |
| Tiles | 1 · 722–1062 · 340 | cream `#fdf6e9` | flat |
| Diet Cherry | 1 · 1062–1700 · 638 | `#d40319` | `#ea071e` → `#bb030f` · 49, 40 |
| the talks | 1 · 1700–2264 · 564 | cream `#fef6e9` | flat |
| Brainwave | 2 · 0–850 · 850 | `#033bd6` | `#044ff5` → `#032ebd` · 55, 37 |
| Green Flag | 2 · 850–1715 · 865 | `#046f41` | `#097d4e` → `#035b35` · 53, 27 |
| Journal | 2 · 1715–2387 · 672 | cream `#fef6e9` | flat |
| Nail Guide | 3 · 0–545 · 545 | cream `#fdf5e7` | flat |
| Shaadi Shift | 3 · 545–1320 · 775 | `#f30b5e` | `#f91366` → `#df0747` · 54, 37 |
| On Me | 3 · 1320–2387 · 1067 | `#fbbe10` | `#fbc526` → `#f5ac06` · 48, 26 |
| Wild Card | 4 · 0–850 · 850 | `#aee60d` | `#bff02b` → `#a2de04` · 62, 47 |
| Pinky Promise | 4 · 850–1715 · 865 | `#6919f9` | `#701ffc` → `#5a10e9` · 46, 15 |
| Shop all / FAQ / footer | 4 · 1715–2348 · 633 | cream `#fdfbf4` | flat |

Gradient formula, same as the hero: `radial-gradient(circle at X Y, inner 0, mid 45%, outer 100%)`, sized to the section's longest side. Raw values are in `landing-colours.json`.
- Landing chapter grounds are close to the metaobject colours: Diet Cherry `#d40319` vs `#e10019`, Wild Card `#aee60d` vs `#b7ef00`.
- They're brighter than the board-2 hero glows. The landing chapters follow board 3.

Landing tokens to add (tokens.css):
- `--st-cream: #fdf6e9`
- `--st-landing-red: #bc0a1e`: pills, "Find your fit." `#b00818`, "Shop all sets" `#b80219`, "Open the guide" `#c3021d`, outline-pill text `#ce3e46`, tile labels `#c6292d`
- `--st-navy: #14168f`: FAQ and footer text; "FAQs" `#0d0e87`, "Example talk" `#1b1d91`
- `--st-bubble: #e3e0fe`
- `--st-beeline-red: #c23a2c`

## Section joins (SVG)
Each join has an edge path in its own viewBox (0 0 390 h), with y0 = the column y where the viewBox starts. Fill the lower section's colour below the edge: `path_edge + " L390,h L0,h Z"`, laid over the upper section's bottom. Full paths are in `landing-geometry.json`, keyed by join.

| Join | Col · y0 · viewBox h | Shape | Edge path (rounded) |
|---|---|---|---|
| hero → tiles | 1 · 707 · 17 | straight (slight lift at the far left) | `M0,2 C26,12 39,14 78,14 L389,14` |
| tiles → Diet Cherry | 1 · 1055 · 13 | shallow dip, deepest at x 120 | `M0,2.4 C52,6 91,9.3 117,10.5 C143,10.5 182,7.9 234,5 C286,3.7 338,1.6 389,8` |
| Diet Cherry → the talks | 1 · 1721 · 45 | cream rises highest at x 100. The can-hand art overlaps x 230–390, so the real edge there is flat ~y 8. | `M0,12 C52,6.5 91,3.2 117,2.9 C169,5.3 208,10.4 273,20 C330,22 360,10 389,8` (h-smoothed past x 273) |
| (the talks → Brainwave) | not on board (column break) | use the mirror of Brainwave → Green Flag | — |
| Brainwave → Green Flag | 2 · 829 · 27 | wave: high at x 60, low at x 220 | `M0,17 C26,9.5 52,5.8 78,6 C117,12 156,21 195,24.4 C247,24 299,20 312,18 C351,10.5 383,3.6 389,2.2` |
| Green Flag → Journal | 2 · 1692 · 29 | dip at left x 40, then flat | `M0,2.5 C26,24 39,27 52,26 C78,17.6 130,9.6 195,9.9 C260,12.5 338,18.6 389,22.7` |
| (Journal → Nail Guide) | column break; both cream | no edge, cream continues; the beeline carries over | — |
| Nail Guide → Shaadi | 3 · 542 · 20 | one small hump peaking at x 156 | `M0,12 L91,11.6 C117,9.8 143,3.2 156,2.9 C182,6.4 208,9.8 234,13.1 C286,12.2 351,12.3 389,17.9` |
| Shaadi → On Me | 3 · 1289 · 36 | yellow rises left, dips at x 260 (the dupatta pin overlaps the join at x 200–330) | `M0,19.6 C26,5 39,2.5 65,2.5 C117,9.4 169,19.4 234,33 C273,33.9 312,33.1 C338,27.8 364,21.3 389,13.5` |
| (On Me → Wild Card) | column break | use the mirror of Wild Card → Pinky | — |
| Wild Card → Pinky | 4 · 798 · 52 | diagonal sweep: low left, high right | `M0,39.6 C26,47 52,50 78,49.2 C130,42 195,31 234,22 C273,12 299,4.3 312,2.7 C338,0.9 364,3.1 389,9.6` |
| Pinky → Shop all | 4 · 1705 · 11 | straight | `M0,2 C26,7 39,8 78,8 L389,8` |

## Beeline (dashed line)
- **Style:**
  - On colour: `stroke:#fff; stroke-opacity:.9; stroke-width:2.5; stroke-dasharray:9 5.5; fill:none; stroke-linecap:butt`.
  - On cream: `stroke:#c23a2c; stroke-width:2`, same dasharray.
  - Measured: dash 8–12 px (median ~10), pitch 13.6–14.5 px.
- **Continuity:** one path per page section, drawn in a full-width SVG overlay. When it crosses a join it continues with the same dash phase and switches colour (white on chapter colours, red on cream). It always enters and leaves at the side edges or the join, never stopping mid-section, except the dead-end flourishes noted below.
- Auto-traced paths (exact, from `landing-beelines.json`):
  - the talks, left, col 1 y 1730–1880: `M45,1730 C46,1735 56,1755 55,1764 C54,1774 42,1779 36,1786 C31,1793 25,1798 21,1806 C18,1814 14,1823 15,1832 C15,1840 18,1850 22,1858 C27,1866 39,1876 42,1880`
  - Journal, bottom loop, col 2 y 2176–2362: the full path is `col2-red-3` in the json. It swings from the left edge down around the handwritten line and exits right.
  - Nail Guide, top-right, col 3 y 3–66: `M206,3 C223,12 240,19 257,25 C275,29 294,34 313,38 C330,41 346,46 362,52 C370,55 381,64 385,66`
  - Nail Guide, left, col 3 y 290–500: `M7,290 C19,303 32,316 44,331 C56,348 63,366 64,386 C64,396 60,406 57,414 C47,429 36,444 24,459 C13,481 10,485 10,485`
- Hand-traced white paths (h):
  - Diet Cherry, right arc, col 1: `M388,1072 C362,1090 341,1120 342,1150 C344,1170 352,1182 362,1192`
  - the talks, left lower, col 1 (red): `M42,1985 C22,2010 18,2050 30,2080 C40,2100 35,2122 20,2142`
  - Brainwave, top, col 2: `M205,78 C260,60 320,42 390,38`
  - Brainwave, left "(", col 2: `M70,330 C35,380 20,450 30,510 C40,555 70,590 100,612`
  - Brainwave, right, col 2: `M290,640 C320,625 360,622 390,640`
  - Green Flag, left, col 2: `M45,860 C30,890 15,920 5,950` and `M40,1255 C50,1290 30,1330 5,1350`
  - Shaadi, lower right, col 3: `M225,1028 C270,1030 330,1060 390,1105`
  - On Me (whole section, board-matched by st-foundation): in from top-right at x 386, across the top to the left, down the left side under the character art, then out right beside the bill. Section-local path in joins.json (`chapter-on-me`).
  - Wild Card, left, col 4: `M55,110 C30,140 25,180 45,220`
  - Wild Card, right, col 4: `M290,575 C330,560 360,530 390,505`
  - Pinky, around the face, col 4: `M200,1385 C226,1410 222,1460 200,1490`

## Sparkle ticks
Same spec as the hero: 2–3 radiating strokes, 2.5 px, 20–28 px long, set ink.
- Hero (On Me): 3 ticks after "this." (col 1 x 165–200, y 105–145) and 3 ticks right of the headline (x 280–320, y 280–320).
- Green Flag: 3 ticks pointing **left**, before the headline (col 2 x 35–75, y 990–1040).
- On Me: 3 ticks top-left of the note (col 3 x 30–75, y 1360–1420) and 2 right of the note (x 280–310, y 1450–1490).
- Wild Card: 2 ticks right of the note (col 4 x 300–330, y 85–110).

## Chapter pattern (Diet Cherry, Brainwave, Green Flag, Shaadi, On Me, Wild Card, Pinky)
Top to bottom:
1. Note: Caveat 700, ~30–34 px (smaller than the hero), 2 lines, rotated −6° to −10°, centred-left.
2. Headline: **Fraunces 700, SOFT 50, WONK 1, opsz 144**, tracking −0.03em, word-spacing ≈0.18em (orchestrator/st-fable fit; the hero stays 900 SOFT100). ~58–64 px, 2 lines, arc R≈420, −3°.
3. Nail row.
4. Product name: Barlow Semi Condensed 600, 22 px, centred, white on dark grounds, black on yellow and lime.
5. Pill "Shop the set": white fill, set-red ink `#cc2f36`, or blue ink `#0f0bcd` on Brainwave and Green Flag.
   - Size: 175–190 × 46, 20 px text, ↗.
   - Must be ≥44 px tall.
6. Character / prop art bleeding off one or two edges.

**Nail row:**
- 5 nails, each ~62 × 130 px, pitch 72 px, row x 22–368, upright (0°), no overlap (8–10 px gaps).
- Shine is baked into the sprites; no shadow is visible.
- Columns per position (sprite cols):

| Set | Row columns | Board reads |
|---|---|---|
| Diet Cherry | [1,0,2,1,1] | red, silver, blush French, red, red |
| Brainwave | [1,2,0,1,0] | white, silver, cobalt, white, cobalt |
| Green Flag | [1,0,1,0,1] | green, blush, green, blush, green |
| Shaadi Shift | [2,1,0,1,2] | blush, red, flower, red, blush |
| On Me | [0,2,1,2,0] | burgundy, tortoise, gold, tortoise, burgundy |
| Wild Card | [1,2,1,0,1] | lime, blush, lime, checks, lime |
| Pinky Promise | [0,0,0,0,0] | lilac with burgundy tip ×5 |


**Measured ink geometry (2026-10-09, `tools/inkgeom.py`, data `landing-inkgeom.json`; supersedes the generic −6…−10° note tilt and R≈420 arc above):**

| Chapter | Note tilt (CSS rotate) | Note lines · baseline pitch | Headline arc radius (per line) | Headline chord tilt |
|---|---|---|---|---|
| Diet Cherry | −5° | 2 · 40 px | ~620 / ~660 | −3° block |
| Brainwave | −5.5° | 2 · 46 px | ~600 / flat (comma skews line 2) | −3° |
| Green Flag | −1° | 2 · 42 px | flat / ~530 (long line "Main dekh lungi.") | −4° |
| Shaadi Shift | −2.5° | 1 | flat / ~450 | −5° |
| On Me | −5.5° | 2 · 39 px | ~670 (1 line) | −6° |
| Wild Card | −4.5° | 1 | **straight** (no arc) | ~0° |
| Pinky Promise | −1° | 1 | ~560 / ~490 | −2° |

Rule for the build:
- Notes: use the per-chapter tilt. The board tilts much less than −8°, which accounts for the 15–40 px extra ink height st-foundation saw. Line pitch is 39–46 px at 390 (lh ≈ 0.95–1.1 at 41 px).
- Headlines: arc R ≈ 560 by default (median of the measured lines; the board is flatter than 420), R ≈ 650 for lines wider than 300 px, Wild Card straight.
- Accuracy is ±15% on radius; the board's handwriting and headlines are hand-set, not a single geometry.
- Residual, accepted (2026-10-09, st-foundation build): Green Flag, Shaadi and On Me headline bottoms sit ~+18 px from the board ink. That's a letterform difference: the board's glyphs are larger and wider than Fraunces 700 / SOFT 50 at the same line width. Type is not distorted to close it; st-fable may set a per-chapter size tweak at acceptance.

**Per chapter boxes** (col y, x range). Re-measured against board 3 on 2026-10-09 at a 10 px grid and cross-checked with st-foundation's fit (`theme-build/lab/fitted-positions.json`, ink-band verified). Pills pixel-verified. Boxes here are **ink** bounds; st-foundation's headline boxes are SVG text cells whose tops sit ~0.25em above the ink, which explains their −23…−39 px headline deltas. Agreed: Diet Cherry ~+30 px; Pinky name/pill corrected up to st-foundation's values.

**Implementation fit (st-foundation, accepted into spec):** visible nails scaled uniformly +8% to 69 px wide with 3 px gaps, row x 12.5–377.5. Render parameters (note/headline font sizes, rotations, art left/top/width/crop/feather) live in `theme-build/tools/build_landing.py` CHAPTERS and `fitted-positions.json` params; they reproduce the ink boxes below.

| Set | Note | Headline | Nails | Name / pill | Art (asset · bleed) |
|---|---|---|---|---|---|
| Diet Cherry (col 1) | x 85–295, y 1117–1197 white | x 65–350, y 1205–1322 white | y 1342–1475 | name y 1495–1518 · pill x 118–278, y 1528–1573 | character left x 0–150, y 1457–1720 (bleed left), eye y 1662; can-hand right x 235–390, y 1457–1720 (bleed right): the trademark can per F1 decision |
| Brainwave (col 2) | x 130–370, y 115–225 white | x 60–365, y 245–350 white | y 375–505 | name y 528–552 · pill x 105–295, y 562–612 | character top-left x 0–150, y 0–350 (bleed left+top); props strip x 0–390, y 615–850 (F2 stand-in) |
| Green Flag (col 2) | x 75–300, y 900–985 white | x 35–385, y 1010–1110 white (sparkles x 35–75, y 990–1040) | y 1135–1255 | name y 1290–1315 · pill x 105–287, y 1322–1372 | rotary phone x 0–215, y 1400–1700 (bleed left+bottom); character right x 180–390, y 1310–1700 (bleed right) |
| Shaadi (col 3) | x 60–330, y 630–685 white | x 60–365, y 720–825 white | y 857–985 | name y 1015–1040 · pill x 140–322, y 1052–1102 | dupatta + face strip left x 0–70, y 545–1320 (bleed left); pin crossing the join x 195–330, y 1195–1295 |
| On Me (col 3) | x 100–335, y 1395–1480 black | x 40–375, y 1515–1585 black, 1 line ~74 px | y 1610–1745 | name y 1765–1795 black · pill x 120–295, y 1803–1853 | character left x 0–190, y 1760–2250 (bleed left); hand with bill right x 160–390, y 1880–2220; handwriting x 50–330, y 2245–2345 (F3 stand-in) |
| Wild Card (col 4) | x 55–330, y 40–100 black | x 85–365, y 105–230 near-black `#000602` | y 255–385 | name y 435–462 black · pill x 145–320, y 470–522 | character left x 0–150, y 260–850 (bleed left); cards-hand x 100–390, y 580–830 → `characters/wild-card` (cards face her) |
| Pinky (col 4) | x 30–385, y 880–945 white | x 70–360, y 930–1060 white | y 1088–1215 | name y 1236–1262 · pill x 120–298, y 1273–1321 (pixel-verified; st-foundation fit) | character + clasped hands x 0–390, y 1350–1715 (bleed left+right+bottom); handwriting x 230–385, y 1365–1500, −12°, white |

## Hero on the landing (col 1, y 69–722)
Same composition as board 2 frame 1 (hero.md), compressed to a 653 px scene (a 390×722 viewport):
- note y 100–200
- headline y 205–285
- loose accents y 290–420
- main nail y 300–540
- controls (345,560) and (345,612)
- pill x 50–355, y 648–708
Use `hero.md` proportions, scaled by scene height.

## Tiles (col 1, y 722–1062)
- Two square image cards on cream: left x 10–190, right x 205–385, both y 740–1000, radius 10, no border.
- Left: on-me character close-up (hand with gold/burgundy nails) → `characters/on-me` cropped to the face and hand.
- Right: scattered nail collage, one per set (LND-013) → built from nail sprites, rotated −40° to +40° and overlapping.
- Labels below: x 30–165 and 225–380, y 1010–1040, Barlow Semi Condensed 600, 21 px, `#c6292d`, plus ↗.

## the talks teaser (col 1, y 1700–2264)
- Heading "the talks": x 105–310, y 1745–1815, Caveat 600, ~66 px, `#0b0603`.
- Sub: x 95–325, y 1825–1860, Caveat 500, ~30 px.
- Label "Example talk": x 40–150, y 1905–1925, DM Sans 700, 17 px, `#1b1d91`.
- Avatar: Ø 80, x 20–100, y 1960–2040, circle crop of a character face.
- Bubble: x 110–350, y 1958–2040, `#e3e0fe`, radius 16; text DM Sans 400, 18 px, `#3b3ba8`.
- Alias: x 125–220, y 2045–2065, DM Sans 600, 15 px, black.
- The "•••" chip at x 300–350 is removed per LND-030.
- Outline pill: x 40–360, y 2100–2152, 2 px `#ce3e46` border, transparent fill, Barlow Semi Condensed 600, 22 px, red text, ↗.
- Handwritten caption: x 40–350, y 2165–2255, Caveat 500, 24 px, black, −3°.
- Red beeline at the left (see above).

## Journal teaser (col 2, y 1715–2387)
- Heading: x 85–310, y 1755–1855, Caveat 500, ~46 px, `#080604`, 2 lines.
- Two image cards: x 15–197 and 205–380, y 1885–2095, radius 10.
  - Left: `characters/brainwave` (woman writing in the notebook).
  - Right: `chapters/brainwave` crop (bag + sketchbook).
- Outline pill: x 65–340, y 2115–2170, same style as the talks pill.
- Handwriting: x 105–330, y 2225–2310, Caveat 500, 32 px.
- Red beeline loop at the bottom.

## Nail Guide teaser (col 3, y 0–545)
- Eyebrow: x 40–150, y 45–68, DM Sans 700, 19 px, `#b0121f`.
- Heading "Find your fit.": x 40–370, y 85–145, Source Serif 4 Bold, ~50 px, `#b00818`, −0.02em.
- Handwriting: x 35–235, y 165–250, Caveat 500, 30 px, black, −12°.
- Finger + tape art: right x 180–390, y 175–450, bleeds right → `guide/web/nail-guide.webp` crop (the board shows pink polish; the approved art is a bare nail, which is fine).
- Filled pill: x 45–350, y 460–518, `#c3021d`, white Barlow Semi Condensed 600, 22 px.
- Red beelines at the top-right and left.

## Shop all / FAQ / footer (col 4, y 1715–2348)
- Filled pill "Shop all sets": x 38–358, y 1745–1805, `#b80219`, white, 26 px.
- Heading: x 30–105, y 1835–1880, Source Serif 4 Bold, 30 px, `#0d0e87`.
- Rows: x 30–360, 3 rows of 40 px at y 1890 / 1930 / 1970.
  - DM Sans 400, 18 px, navy `#14168f`; "+" at x 345, 2 px.
  - 1 px dividers `#e4e2ec` between rows.
- Rule: y 2030, 1 px, `#c9c9d6`, x 30–360.
- Logo: stacked, centred, ~100 × 72, y 2050–2120, `#1412d5`.
- Tagline: y 2125–2155, DM Sans 400, 20 px, `#3335a3`.
- Nav row: y 2175–2195, DM Sans 400, 14 px, `#3335a3`, centred, 14 px gaps: Shop · Our Story · the talks · Journal · Nail Guide.
- Social icons: Ø 32 glyphs, y 2210–2245, x 80 / 160 / 230 / 300, navy (D5 decides which stay).
- Legal row: y 2265–2285, 14 px. Copyright: y 2300–2320, 14 px.
- Touch targets: give links and icons 44 px hit areas, even though the board is tighter.

## Flags: decisions (orchestrator, owner directive)
- **F1 DECIDED:** the Diet Cherry chapter uses the can hand with the trademark (`desi-diet-can-v1`, theme asset `st-diet-can.webp`). Box: right x 240–390, y 1500–1700, bleed right. Same scale family as the hero (≈0.30): ~357 css px wide image, positioned so the can sits at x 270–390, y 1505–1640.
- **F2 DECIDED:** the Brainwave props strip uses the v2 atlas cells as a stand-in, at most 1.3× upscale. It's replaced by the ChatGPT "Brainwave sketchbook still life" when that arrives. The old 180 px chapter cap is lifted: art is sized to the board, limited only by the ≤1.3× source rule.
  - Source widths: `characters/brainwave` is 303 px, so ≤394 css px at 1×, which is enough for 390. `chapters/brainwave` is ~270 px, so ≤351 css px.
- **F3 DECIDED:** `characters/on-me` stands in for the hand-with-receipt until the ChatGPT art arrives.
- **F4 ACCEPTED:** mirrored joins; st-fable judges them in acceptance.
- Copy: the owner chose board wording for T2–T16. The FAQ shows the board's 3 rows, with answers from st-copy.

Original flags:
- **F1:** the Diet Cherry chapter again uses the hand holding a "Diet Coke" can. Same owner decision as hero flag 1. Unbranded alternatives:
  - `characters/diet-cherry` (silver can)
  - `chapters/diet-cherry-fade` (plain can on a table)
- **F2:** there's no approved asset for the Brainwave props illustration (bag sketch, notebook, pen as a drawn strip). Closest approved art:
  - `chapters/brainwave-fade` (photo-style bag + sketchbook, no pen)
  - `characters/brainwave` (notebook + blue pen)

  Recommendation: the chapter fade at full width, capped at 180 css px wide per the earlier decision. That cap conflicts with board-3 full-bleed, so the owner decides, or ChatGPT art fills it.
- **F3:** the On Me hand-with-bill ("On me. xx" receipt) has no separate asset. `characters/on-me` shows the woman holding a bill near her face, which is the closest.
- **F4:** two column breaks hide joins (talks → Brainwave, On Me → Wild Card). The spec reuses mirrored joins.
