# Hero: board 2, seven states

Source: `2.jpg`. Frames were cut and rescaled to 390 px wide: `spec/crops/hero-<n>-<set>@390.png`, plus `”¦@390-grid.png` with a grid every 39 px (10%).
All coordinates are **CSS px at 390**, measured from the frame top, header included (header 0–69). `%` columns are % of 390 width.
Accuracy is about ±6 px: the boards are AI-rendered at ~271 board px per frame.

## Common structure (all seven)
| Layer (z low → high) | Spec |
|---|---|
| Header | `--st-header-h` 69, paper `#fdfdfc`, no rule visible on the board. Hamburger x 14–42 (3 strokes, 2.5 px, logo blue). Stacked logo "small / talk" centred x 137 (35%), ~84×56, `#1412d5`. "the talks" x 212–305, Caveat 600 34 px, `#0d0b10`. Bag outline x 338–374, 2 px logo blue. |
| Scene | Height = frame H − 69 (751–829 px), which is 100svh − header on a 390×844 phone. Background is the set's radial glow `--hero-<set>` (tokens.css). No section curve at the hero bottom on board 2 (landing joins are in landing.md). |
| Preview hand | Enters top-right; the wrist bleeds off the top and right edges. Visible box ≈ x 240–390, y 69–240 (39% of width). It shows the **next** set's nails (board order confirms `manifest.preview_slots`). Use `artwork/hand/web/preview-hand.webp` at 146 css px wide, positioned so the visible part matches this box. |
| Note | Caveat 700, ~46 px, rotation −8° to −18° (per frame below), set ink colour. Above-left of the headline. |
| Sparkle ticks | 2–3 straight strokes radiating from the note's last letter. Stroke 2.5 px, round caps, set ink. Lengths 20–28 px. Angles about −80°, −35° and −5° from horizontal (pointing up-right / right). 5–8 px gap from the glyphs. |
| Headline | Fraunces 900 SOFT100 WONK1, ~86 px for a one-line set; 2-line sets ~62–66 px per line, leading 0.92. Arc radius ~380 px, convex up, whole block rotated −3°. Tracking −0.06em. |
| Main nail | Signature sprite (col 0) on the finger tone. Nail ≈ 110–130 px wide × 215–235 px tall, centred x ≈ 50–56%. The finger rises from below the pill. Shine is baked into the sprite (two vertical gloss streaks on the right third); add no CSS shine. |
| Loose accents | 2 accent nails (col 1 + col 2), ~70–85 × 100–130 px, long axis tilted 25–40° from vertical. They overlap each other by 10–20 px (the second one in front) and sit left or right of the main nail per frame. |
| Character | Ink character from `artwork/characters/web/<set>.webp`, bleed edges as in the manifest. Half-face crop; eye line given per frame. |
| Controls | Pause and tone circles, `--st-ctrl-d` 52 px, white fill, centre x 345. The tone circle shows the skin swatch with a 4 px white ring. Pause glyph is the pill-ink colour. |
| Pill | Full-width rounded pill, x 22–363 (6%–93%), 62 px tall, bottom 22–30 px above the frame end. Barlow Semi Condensed 600, ~30 px, then a ↗ arrow (2.5 px stroke, 22 px). Fill and ink per set (tokens). |

## Per frame
| # | Set (frame H) | Note box · rot · ticks | Headline box (lines) | Main nail box · cuticle | Loose accents | Character / prop | Controls (pause, tone) | Pill box · style |
|---|---|---|---|---|---|---|---|---|
| 1 | On Me (885) | x 45–230, y 130–250 · −10° · 3 ticks x 180–225, y 130–190 | x 35–382, y 258–356 (1) | x 155–282, y 395–628 · (218, 625) | left: tortoise x 2–92 y 385–495; gold x 65–145 y 420–530 (gold in front) | bottom-left, bleed left+bottom, x 0–135, y 510–885, eye y≈720 | (345,700) (345,757) | x 35–363, y 795–857 · filled `#9c0219`, white text |
| 2 | Brainwave (860) | x 100–245, y 225–300 · −12° · 2 ticks x 245–268, y 215–245 | x 30–380, y 285–405 (2; line 2 indented x 120–365) | x 138–248, y 410–625 · (195, 622) | left: white x 5–75 y 440–540; silver x 40–122 y 478–590 | top-left, bleed left+top, x 0–150, y 69–330, glasses y≈185 | (345,677) (345,733) | x 22–362, y 768–832 · white, ink `#0f0bcd` |
| 3 | Diet Cherry (854) | x 45–210, y 170–235 · −10° · no ticks | x 45–385, y 220–375 (2) | silver x 152–245, y 405–620 · (200, 618) | right: deep red x 262–330 y 410–500; blush red-tip x 300–385 y 465–575 | **hand holding can**, bleed left, x 0–120, y 375–690 (see flag) | (345,672) (345,730) | x 22–365, y 765–827 · white, ink `#d6171a` |
| 4 | Green Flag (898) | x 35–155, y 175–235 · −12° · 3 ticks x 160–195, y 165–215 | x 30–385, y 250–395 (2) | blush green-tip x 130–245, y 435–660 · (190, 655) | left: green x 5–80 y 455–585; blush x 35–105 y 535–650 | right, bleed right, x 210–390, y 390–790, pink phone, eye y≈530 | (343,712) (343,767) | x 18–368, y 805–865 · white, ink `#107247` |
| 5 | Shaadi Shift (851) | x 35–190, y 165–240 · −8° · 3 ticks x 195–232, y 175–220 | x 30–385, y 265–400 (2), ink near-black | flower x 157–270, y 425–665 · (213, 660) | left: blush x 20–100 y 425–530; red x 75–150 y 445–545 | **prop only**: dupatta + safety pin, bleed left, x 0–110, y 425–760 (no face) | (345,652) (345,710) | x 22–375, y 757–822 · filled `#9b021a`, white text |
| 6 | Wild Card (826) | x 35–205, y 115–200 · −18° · 2 ticks x 200–220, y 145–185 | x 80–380, y 215–355 (2), ink navy `#0f0b5c` | checks x 155–262, y 400–620 · (208, 615) | right: lime x 265–345 y 390–520; blush-lime x 320–385 y 440–545 | left, bleed left, x 0–130, y 245–825, cards face her, eye y≈425 | (345,633) (345,690) | x 22–360, y 735–797 · white, ink `#0f0cce` |
| 7 | Pinky Promise (820) | x 100–275, y 205–275 · −8° · 3 ticks x 280–310, y 225–275 | x 45–385, y 280–420 (2) | lilac burgundy-tip x 145–270, y 425–640 · (205, 636) | left: x 10–80 y 455–555; x 45–125 y 485–600 | top-left, bleed left+top, x 0–85, y 69–260 (face edge only) | (345,632) (345,688) | x 15–375, y 728–792 · white, ink `#d6181b` |

Glow per frame (tokens `--hero-<set>`, centre % of the scene / inner / mid / outer):
- on-me: 46/34% · `#fcc01d` / `#f5a908` / `#e18e05`
- brainwave: 52/28% · `#0958f4` / `#0444d9` / `#032cb8`
- diet-cherry: 35/33% · `#d41614` / `#b70a09` / `#780303`
- green-flag: 43/38% · `#0d7b4e` / `#04673c` / `#034727`
- shaadi: 49/40% · `#fa357f` / `#f61d6d` / `#df0a4d`
- wild: 51/34% · `#d2fb23` / `#b4f50a` / `#94e004`
- pinky: 38/32% · `#792ffb` / `#621dec` / `#4812c8`

Raw samples are in `spec/hero-colours.json`.

## Flags
1. **Diet Cherry, frame 3: DECIDED (owner, via the orchestrator): option (c), the board as drawn, trademark included.**
   - Asset: `desi-diet-can-v1.webp`, 1189×1323 transparent; install as theme asset `st-diet-can.webp`.
   - Placement at 390 (fitted visually to the board; check overlay `crops/hero-3-can-placement-check.png`, asset at 60% over the frame): render the whole image at **357 × 397 css px** (scale 0.30), top-left at **x −176, y 366** from the frame top, header included (y 297 inside the scene).
     - The can top sits at y ≈ 372.
     - The can right edge sits at x ≈ 128.
     - The hand and nails overlap the board hand, and the wrist exits the left edge and runs down behind the main finger and pill.
   - As percentages for scaling: `width: 91.5%` of scene width, `left: -45.1%`, `top: 37.0%` of scene height (scene = frame − 69 = 785 px).
   - z-index: above the glow, below the main finger, headline, controls and pill. On the board the main finger overlaps the can hand.

   Original flag, kept for the record: the board's hand-with-can is `desi-diet-can-v1.webp`, which carries a legible "Diet Coke" wordmark. The orchestrator ruled it "not used anywhere", and the brief and D8 forbid beverage trademarks. The owner directive says to match board 2 frame 3. **This needs an owner decision.** Options:
   - (a) The unbranded crop `artwork/rejected/can-crop-proposal-below-wordmark.webp`. It's the lower can plus hand, with the hard top cut off-canvas at y < 375.
   - (b) The unbranded v2 character with the silver can, `characters/web/diet-cherry.webp`, bleed left, x 0–120.
   - (c) The board as drawn, with the trademark.

   The spec boxes above fit (a) or (b) without changes.
2. **Shaadi Shift, frame 5:** the board shows a prop (dupatta + safety pin), not a face. The approved v2 character cell has a face with a pin. Use the character with its face cropped off-canvas left (anchor x 0, shift left ~45%), so only the dupatta and pin show. Or follow the owner's choice.
3. **Pill text:** the board shows `Shop “On Me” ↗` with quotation marks. Register LND-009 says `Shop {name}` without quotes. Listed in TEXT-DIFFS.md; the register wins until the owner decides.
4. The loose accent pairs on board 2 don't always use cols 1+2. For example, Diet Cherry shows deep red + blush-red-tip. The builder should use `distinct_accents`; the colours match the sprites.

