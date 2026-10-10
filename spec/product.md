# Product (PDP): board 5 frame 2 (On Me shown)

Crop: `crops/product@390.png` (+ `-grid`); scale 1.291.

| Element | Box | Spec |
|---|---|---|
| Header | 0–70 | Landing header. |
| Main media | x 8–383, y 60–375, radius 14 | Square-ish (375 × 315). Set-colour ground (`--st-tile-<set>`). Package box ≈85% of the panel height, left edge at x≈33 (panel-relative ≈25), vertically centred. Scattered sprite nails on the right, ~10% larger than the first build, rotated −40° to +40°, packed up to the box's tray edge (5–10 px overlap with the box is fine). Build: package + 8–9 nail-sprite cells (round 7, st-fable PDP acceptance). |
| Thumbnails | y 385–455, 5 tiles of 70 × 70, gap 6, from x 8 | Radius 6. The selected one gets a 2 px `#e0a020` set-colour border. Thumb 4 shows a white play disc Ø 34. **These are product photos and video the brand doesn't have (G11).** Show only the media that exists. |
| Title | x 15–150, y 475–515 | `--font-pdp-title` Source Serif 4 **Black** (wght 900, opsz 60), 50 px, `--st-burgundy` (round 6, verified serif). |
| Price | right, x 313–375, y 485–510 | `--font-price` IBM Plex Sans Condensed 700, 25 px, `--st-price` (board "599" 41×18 px; round 7). |
| Description | x 15–300, y 520–540 | DM Sans 400, 17 px, `#373f8b` (navy-blue body on this board). |
| "Find your fit →" | y 548–566 | DM Sans 500, 16 px, `--st-hand-blue`, underlined. |
| Qty stepper | x 15–118, y 595–635 (→ 44 tall) | 1 px `#e2e3e3`, radius 6. −, 1, + in DM Sans 500, 18 px. |
| Add to bag | x 128–337, y 593–635 | Fill `#940326`, radius 6 (not a full pill), white DM Sans 600, 17 px: "Add to bag · ₹599". |
| Wishlist | x 347–377, y 593–635 | Outline 1.5 px `#940326`, bookmark glyph. Board extra: no wishlist exists, so **omit it**. |
| Links row | y 650–668 | "Delivery & returns →" | "Need a hand? →". DM Sans 500, 15 px, `#3653c7`, underlined, separated by a 1 px vertical bar. |
| Accordions | y 690–800, 3 rows of 36 px | Titles DM Sans 700, 17 px, `#ae1f36`, "+" right 2 px `#ae1f36`, dividers 1 px `#e8e9eb`. "What's in the kit", "Fit & application", "The story: {headline}". |
| Quote | x 25–235, y 810–905 | Kalam Light, 22 px, `#2e4ac7`, −6°, 4 lines, curly quotes. |
| "Read the story →" | x 125–245, y 915–935 | DM Sans 500, 16 px, blue, underlined. |
| Character peek | x 275–390, y 815–945 | Bleeds right, half face → `characters/<set>` crop (eye line y 880). |
| Footer | y 1170–1215 | Same as the shop. |

Gaps: thumbnails and photos need real product media (G11); the board's wishlist button has no function.
