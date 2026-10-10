# Bag (cart): board 5 frame 3

Crop: `crops/bag@390.png` (+ `-grid`); scale 1.548.

| Element | Box | Spec |
|---|---|---|
| Header | 0–80 | Landing header. |
| H1 "Your bag" | x 18–200, y 100–158 | Source Serif 4 Bold, 46 px, `--st-burgundy`. |
| Count "2 items" | right, x 305–372, y 120–140 | DM Sans 400, 17 px, `#1a1a2e`. |
| Rules | y 173, 360, 550 | 1 px `#e8e9eb`, x 18–375. |
| Line item | rows of ~185 px starting y 190 | Image x 20–155, 135 × 145, radius 6 (package on set colour, like the shop card). Name x 170, y +0, `--font-card-name` (IBM Plex Sans Condensed Bold), 19 px, `--st-red`. Price y +32, `--font-price` IBM Plex Sans Condensed 700, 17 px, `--st-price`. Stepper x 170–285, y +78 (36 → 44 tall), 1 px `#e2e3e3`, radius 6. "Remove" y +125, DM Sans 400, 15 px, underlined, `#1a1a2e`. |
| Subtotal | y 575–600 | Label "Subtotal" and amount both `--font-price` IBM Plex Sans Condensed 700, 24 px, navy `#14163b` (board label has no serifs; Plex matches its 87 px ink width; round 8). |
| Note | y 620–638 | DM Sans 400, 15 px, `--st-muted`. |
| Checkout button | x 22–373, y 665–718 | Fill `#8d0223`, radius 6, white DM Sans 600, 18 px. |
| Continue shopping | centred, y 737–755 | ← + DM Sans 500, 16 px, `#3653c7`, underlined. |
| "Need a hand?" panel | x 15–380, y 805–1095, radius 12 | Fill `#f8f7f7`. Title x 25, y 828–852, DM Sans 700, 20 px, `#111`. Body DM Sans 400, 16 px, `#373f8b`. 3 links at y 930 / 970 / 1008, DM Sans 500, 17 px, `#1b1d91`, underlined, →. Character peek bottom-right x 235–380, y 935–1095, bleed right/bottom. |
| "Nails for every plot twist." panel | x 15–380, y 1110–1370, radius 12 | Fill `#fee2ed`. Heading y 1140–1180, Source Serif 4 Bold, ~30 px (board ink x 44–358), `#b0122a` (round 8). Sub "Collect the whole story." Kalam Light, 22 px, `#2f4ac8`, −3°. 4 sprite nails y 1230–1345, ~60 × 115, pitch 88, upright (On Me: burgundy, tortoise, gold, tortoise-small). |
| Footer | y 1400–1450 | Same as the shop. |
