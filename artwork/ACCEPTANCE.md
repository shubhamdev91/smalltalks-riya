# Small Talk artwork: acceptance criteria

Each asset is checked against these criteria before it's marked done. Every check includes a visual inspection of the real output, composited on all seven campaign colours. Rejected candidates go in `rejected/`.

Campaign backgrounds: #ffb900 #073df1 #e10019 #007948 #ff0078 #b7ef00 #6620f2

## Common (all Phase 1 assets)
- C1. Pixels come straight from the locked source atlases. No recolouring, no redraw, no filters on the design. The only per-pixel changes allowed are on the alpha channel and the 1–2 px anti-aliased rim.
- C2. Transparent background. Fully transparent pixels are RGB 0 / alpha 0. Interior alpha is exactly 255, so the campaign colour doesn't tint through.
- C3. No fringe: no stray specks or halo outside the silhouette, and no coloured rim, on any of the seven colours.
- C4. WebP, lossless or quality ≥ 92. Each file is ≤ 120 KB, except the hand base, which is ≤ 200 KB. Sizes are recorded in manifest.json.

## Nail sprites (nails/<set-handle>.webp)
- N1. One file per set, 7 total. 3 columns, one row, all cells the same size: col0 signature, col1 accent, col2 extra accent.
- N2. In every cell the nail is horizontally centred, and its cuticle (lowest opaque point) sits at x = 0.5, y = 0.925 of the cell.
- N3. The nail pattern matches the set description in campaign-metaobjects.json, and the column maps to motion_index.
- N4. One whole nail per cell. No clipping, and nothing from neighbouring atlas cells bleeds in.

## Finger tones (fingers/tone-<n>.webp)
- F1. 4 files on one identical canvas size.
- F2. The nail-bed anchor (cuticle centre of the natural nail) sits at the same normalised point in all four, recorded in the manifest.
- F3. No red/orange specks; edges are clean.

## Preview hand (hand/preview-hand.webp + hand/preview-hand.json)
- H1. Back of a relaxed hand with the wrist, entering from the upper right.
- H2. Exactly four visible fingernails. The thumb is not visible, and the contour where it was removed reads as a natural hand edge: no notch, no straight cut.
- H3. Correct anatomy: four fingers, no extra or merged digits.
- H4. JSON gives four nail slots with centre (normalised), rotation (deg), and scale relative to the sprite cell, in finger order index → little.
- H5. Composites with a nail sprite in every slot on all seven colours: no fringe, and the nails sit on the nail beds.
- H6. Intended display width is ~20–24% of a 390 px hero (78–94 CSS px). Delivered at ≥ 2× that for retina.

## Phase 2 (characters, chapter art): criteria get added when Board 1 is approved

## Phase 1 results (2026-10-09, visually inspected)
- Nails: PASS N1–N4, C1–C4. 7 × 612×354 sheets (cells 204×354), cuticle at (0.5, 0.925). Checked in tests/nails-contact.png on the set colour and on #fffaf0, and at 4× zoom on the edges. Extra accents were downscaled 0.64× to match signature height; no colour change.
- Fingers: PASS F1–F3. 4 × 310×840, nail-bed anchor (0.5, 0.2649). Checked in tests/fingers-contact.png and tests/finger-anchor-test.png.
- Preview hand: PASS H1–H6. 511×639 lossless, 197 KB. Thumb removed with a spline radial edge plus a soft edge falloff. Rejected v1 (thumb sliver left along the index finger) is in rejected/. Minor, accepted: on the ring finger, ≤ 1 px of the natural nail's free edge can show past the press-on tip at 3× zoom; sub-pixel at display size. A very faint thumb-crease tone stays near the radial edge.

## Phase 2: readjustment package (2026-10-09). No generation, no redraw, no recolour.
Allowed operations: crop, mask, alpha feather, composite existing approved assets, WebP derivatives. Every check below includes a visual inspection; I flag problems and don't fix them by painting.

### Characters (characters/<set>.webp), from desi-ink-characters-v2.png
- K1. One file per set. Transparent outside the figure. No hard rectangular panel edge visible: either the cut edge is feathered (≥ 24 px soft ramp, smoothstep) or it's declared as `bleed_edge` to sit off-canvas.
- K2. The art's RGB on opaque pixels is unchanged from the source (verified Δ = 0 on the master).
- K3. Placement data: anchor (normalised), bleed edge(s), and suggested CSS height at a 390 px scene.
- K4. Master ≤ 200 KB, or a web derivative (q ≥ 92) that is ≤ 200 KB, with Δ reported.
- K5. Visible nails match the set; props per brief. Report pass/fail with a crop.

### Chapter scenes (chapters/<set>.webp), from desi-ink-characters.png
- S1. A crop matching the Board 3 chapter composition for the set. Opaque.
- S2. The ground colour, sampled in flat background areas, equals the metaobject background. Report ΔRGB per channel. A mismatch gets flagged, not recoloured.
- S3. ≤ 200 KB WebP.
- S4. Story checks: Wild Card card faces point to the woman; Pinky Promise hands connected with correct finger count; Brainwave crescent bag in a notebook with a blue pen, no machinery; Green Flag rotary phone; Diet Cherry can with no legible beverage trademark or trade dress (crop it out, or flag as an owner conflict). Nails match the set.

### Guide (guide/nail-guide.webp): as-is derivative, Δ reported.
### Shop (shop/): finger states cut per set (exact grid). Lifestyle composites = preview hand + sprites per preview_slots. The Diet Cherry can only if desi-diet-can-v1.webp is found and passes the brand check.
### Packaging: never upscale. Keep as-is and mark it "awaiting hi-res from owner".

## HD intake: ChatGPT art v2 (artwork/chatgpt/<set>/ → artwork/hd/), criteria written 2026-10-09 before any file arrived
Pipeline: `scripts/hd_intake.py`. It runs the automatic checks, builds the contact sheets and writes `manifest.json → hd`. A file only ships after I've also inspected it visually. Rejects go to `rejected/hd/` with a reason. The originals in `chatgpt/` are never modified.

**Every file**
- X1. It's the original PNG, not a screenshot or a WhatsApp copy. Long side ≥ 1024 px, no watermark, border or text, unless text was requested (receipt "On me. xx", packaging).
- X2. Not upscaled. Derivatives are only ever downscaled (Lanczos, premultiplied alpha). The reported "max sharp CSS width" is px / 3.

**Cutouts** (women, pair, props, nails, finger tones)
- C1. Real transparency. A painted grey/white checkerboard is a REJECT, and the request goes back for real alpha. A flat background is the fallback (prompt rule 4). I key it out automatically with known-foreground/known-background matting and colour unmixing on the rim. Anything other than flat is a REJECT. **Key-colour rule (added after dry-run tests):** a flat background in the set colour collides with the subject (0.4–12% of palette pixels sit within the key tolerance; violet ate 1.2% of Pinky's sweater in a ground-truth test). The fallback key must be pure #00ff00, or #ff00ff for Green Flag and #00ffff for Wild Card. These measured 0% overlap with every set palette. The script flags key collision > 1% for a visual bite check.
- C2. No fringe or halo on the target ground. The rim-halo fraction must be < 2%, plus a visual check on the set colour, white and black at 1× and 3×. No white "sticker" outline.
- C3. One subject. No stray specks: components < 0.1% of the subject area are removed, and anything larger is flagged.

**Nails** (`<set>-nail-<n>`, n → sprite col n−1)
- N1. Design, colour and pattern match `4-exact-nail-designs` and the table in the prompt file. The automatic Lab check against the Phase-1 sprite cell must be ΔE00 < 12 on the dominant colours, and the visual check decides. Any invented pattern is a REJECT.
- N2. Almond shape, tip up, base at the bottom, straight-on. The checks are top-15% width < bottom-30% width, and an aspect ratio of 1.5–2.6. Pinky's asymmetric tip sweeps from the right. Green Flag and Wild Card French tips are pointed.
- N3. Drop-in geometry: each HD sprite is fitted to the same normalised box and cuticle anchor as the Phase-1 cell (0.5, 0.925), so the existing CSS works unchanged. The HD cell is 450×780 (×2.2), so the nail is ~700 px tall, which covers a 233 CSS px hero nail at 3×.

**Fingers** (`finger-tone-1..4`)
- F1. All four share one pose and size. Bare natural nail, clean cuticle, five-digit anatomy not applicable. Each is fitted to the Phase-1 canvas geometry (310×840 → 682×1848, nail-bed anchor 0.5, 0.2649), with the anchor confirmed visually.

**Women, pair, props**
- W1. The same woman as `3-same-woman-reference` and the board. Five fingers per hand with natural joints. Visible nails match the set.
- W2. Story rules:
  - Wild Card: the card faces point toward her; the viewer sees only the backs.
  - Pinky: hands clasped, each wrist joined to its own arm, no extra or fused fingers.
  - Brainwave sketchbook: crescent-bag sketches and a blue pen, no machinery.
  - Green Flag phone: a pink rotary phone with a gold dial centre.
  - On Me receipt: "On me. xx", legible and spelled exactly.
  - Shaadi: bandhani fabric with a gold safety pin.
- W3. Diet Cherry can rule: `diet-cherry-can-hand` copies the board label (owner-accepted trademark); `diet-cherry-pdp-moment` must be unbranded.

**Product photos** (`<set>-pdp-flatlay / -hand / -moment`, `guide-*`, `our-vision-woman`)
- P1. Opaque. The ground is close to the requested colour: ΔE00 < 10 at the border median, otherwise flagged rather than recoloured. Sharp: the Laplacian variance is reported, and focus is judged visually on the nails.
- P2. The `-hand` photo has five fingers, back of the hand to camera, and nails in the exact order given in the prompt (index → little, plus thumb).
- P3. The flat-lay nail count must not contradict the kit (G1 is still open, so flag it, don't block).

**Packaging re-renders** (`<set>-pdp-packaging`, P3)
- K1. Text exactness: every printed string matches the original `*-approved-package.png`, character for character: "small talk", the headline exactly as on the box (Brainwave keeps "tha"), and "ALMOND PRESS-ONS". The check is a visual side-by-side of enlarged text crops. Any difference is a REJECT.
- K2. The illustration matches the original: same figure, props, nail colours and layout. Automatic structural similarity against the original is reported (block NCC); a visual side-by-side and diff heatmap decide. Any added, removed or changed element is a REJECT.
- K3. The cutout is clean (C1/C2) with no baked shadow.

### HD batch 1: board-corrections salvage (2026-10-09), visually inspected
All 8 sources have real alpha (no keying needed); rims clean on the set colour, white and black at 3x; the dark rim metric is the ink outline of the comic style, not fringe.
- ACCEPTED: on-me-woman, on-me-receipt-hand ("On me. xx" legible), green-flag-woman (+hero variant), green-flag-phone, shaadi-shift-sweep, shaadi-shift-pin-hero, brainwave-sketchbook (crescent-bag sketches + blue pen, no machinery), journal-writing, journal-bag-notebook, HD preview hand (4 fingers, thumb concealed, bare nails, slots re-measured; press-ons sit on the nail beds on all 7 colours).
- INTERIM (owner edit A1 pending): wild-card-woman/-hero, wild-card-cards-hand/-hero (card backs to viewer = correct, but blue backs vs red; different woman from the board).
- ACCEPTED on correction: pinky-promise-scene/-face-hero (board 3 = one woman + a second person's lilac-sleeved hand; hands connected, nails correct).
- Below 3x at spec size (sources are 1200x800, never upscaled): on-me-woman 1.47x, on-me-receipt-hand 1.36x, pinky-promise-scene 1.35x; 2.0-2.9x for most others; brainwave-sketchbook and green-flag hero meet 3x.
- Nail checks: On Me receipt hand all burgundy (= board 3; prompt wanted mixed): accepted. Green Flag phone hand blush-tip / emerald alternating = prompt. Journal writer has deep red nails, not cobalt: LND-034/035 alts need st-copy updates.

### HD batch 2: ChatGPT folders A + B (2026-10-10), visually inspected
Files were identified by ChatGPT's "-N" download suffix, cross-checked with file mtimes and by eye; renamed copies are in chatgpt/named/, and the originals → canonical map is in hd/intake-map.json + manifest.
- A (5 files): A1 wild-card-chapter-v2, A2 brainwave-chapter, A3 diet-cherry-chapter, A4 our-vision-woman: all identified. A5 is a retry of our-vision, set aside (softer). The A3/A4 mtimes are swapped vs suffix order; suffix + visual check decided.
- B (22/22): all 18 nails ACCEPTED. They match the locked sprite columns (ΔE00 0.8–7.4), are almond and tip-up, with clean alpha. HD sheets are a drop-in at 2.2× (cells 450×780, same anchor). The 4 finger tones are ACCEPTED at 1.8× (558×1512, the largest without upscaling), with the anchor verified.
- Chapters split and fitted to boards 2/3: brainwave-woman (+hero), diet-cherry-woman, diet-cherry-can-hand (board trademark, owner-accepted; hand enters from the right, so the hero keeps desi-diet-can-v1), wild-card-woman-v2 (+hero) and wild-card-cards-hand-v2 (+hero): red backs to the viewer, curly hair, lime saree. The Wild Card v1 interims are superseded. brainwave-pen-hand is exported with no board slot. our-vision tile crop is 3×.
- Wild Card v2 split: the cards piece has the hair removed by dark-blob subtraction inside a tight polygon. The woman piece's cut hole is grown by 8 px and blurred by 6 px, and the hair top is feathered. Checked alone and composited on plain lime: no notch, no outline remnants.
- C: empty. All 24 P2 files are missing.

### HD batch 3 (2026-10-10): fingers re-measured, nail sheets fixed, folder C, st-fable fixes, hero-v2
- Fingers: the natural nail plate was measured on all 4 tones (206–209 px wide). Every cuticle is now refitted to (0.5, 0.2649). Main nail cell = 0.474 × finger width (P1 0.50), anchor 0.925, no tuck. All 7 signature nails were checked on all 4 tones: no natural nail shows (tests/hd/fingers-hd-main-nail-*.png).
- Nail sheets: the ChatGPT PNGs carried faint specks below each nail, which lifted the solid base 25–30 px off the anchor. Re-cut with the P1 clean; every base now sits at y 721 = 0.925.
- Speck sweep across all HD cutouts (scripts/speck_audit.py).
- C: 24/24 accepted (finger order verified on all 7 hand shots; Diet Cherry moment can unbranded). C-2 rejected (wrong finger order); C-1 and C-12 are alternates. G1 flag: 5-nail fans.
- Fixes: Green Flag is three layers (woman < phone < hand + receiver); Pinky re-cropped with the full clasp and sleeve; dedicated On Me hero cut.
- hero-v2: green-flag (slivers removed, hair top feathered, arm and cord reach the pill at scale 0.41), shaadi pin (tall dupatta strip, pin vertical, via a rotation-only derived source), pinky (full profile, no right feather), wild-card (already cut from A1 v2, top feathered).

### Wild Card hint cards v2: st-fable spec (owner-v12 README §D), criteria written 2026-10-10 before generation
- W-C1: two separate SVGs, st-card-ace-spades.svg and st-card-king-hearts.svg. viewBox 0 0 46 64, card rect rx 4.5, face #fffdf6, 1.2 ink outline #1a1410 drawn fully inside the viewBox. Flat: no shadow, gradient, filter or text element (the outlines are glyph paths, so there is no font dependency).
- W-C2: ace = spade + index in ink #1a1410; king = heart + index in #c3021d. These are the only colours besides the face.
- W-C3: each file is under 3 KB. No ids, no `<use>`, no style blocks, so both files can be inlined on one page without collisions. aria-hidden is set by the theme; the files carry role="img" and an aria-label for standalone use.
- W-C4: the top-left corner index (rank + pip) reads at 42 px card width, rotated by −14° / 9° on lime, judged by eye at 1× and 2×. The rank cap height is ≥ 9 css px at 42 px wide. The bottom-right mirrored index is present.
- W-C5: the centre art is clear of both indices (≥ 1.5 units gap). It stays readable at 70–90 px wide on laptop.
- W-C6: the SVG renders in a real browser the same as the Pillow raster from the same geometry (no holes from fill rules).
- Results (2026-10-10): W-C1–W-C6 pass. ace 1437 B, king 2615 B; cap height 9.6 css px at 42 px wide; centre-to-index clearance ace 5.4, king 3.9 units. Rendered in a real browser with both SVGs inlined on one page: identical to the Pillow raster, no fill holes, no id collisions. Phone (42 px, ~32 px visible) and laptop (80 px) placements composited on lime @1x/@2x: tests/hd/contact-wild-card-hint-cards-v2.png. King primary = crowned heart; plain-heart alternate in hd/wild-card/alt/. The v1 250×350 cards are superseded.

### Shaadi Shift full-face woman (folder E, owner generating in ChatGPT): criteria written 2026-10-10 before the file arrives
- E-S1 (framing): same framing as wild-card-woman-v2. The figure is cut by the LEFT image edge, with no other cut edge (the right/top/bottom silhouette is free or feathered). The face, both eyes and the bindi are fully inside the frame. (The §E "eye at ≥ 35 % height" check is about on-screen placement and belongs to st-fable.) Facing direction is checked against the orchestrator's brief (facing right, into the frame). Laptop uses a CSS mirror, so nothing text-like may be in the art.
- E-S2 (fidelity to the Shaadi character, compared side by side with ChatGPT-upload/E/1-shaadi-shift-reference.png and hd/characters/shaadi-shift-sweep): round red bindi; warm brown skin within ΔE00 ≤ 8 of the reference cheek; dark curly hair; gold jhumkas plus the bead jewellery; hot-pink/red dupatta (ΔE00 ≤ 8 of the reference dupatta mid-tone) with gold floral embroidery and a beaded border; the gold safety pin visible on the dupatta. Each item is listed as present or missing in the report.
- E-S3 (style): the boards' ink style (black ink linework with flat-to-soft colour, as in wild-card-woman-v2 / the shaadi reference). Reject it if it's photoreal, 3D-rendered or painterly without ink lines. No extra hands or fingers, no warped jewellery, no text or watermark.
- E-S4 (mask): background keyed via the known-fg/bg matte. If the background isn't a flat key, use the pure #00FF00 key fallback (never the set colour). Dupatta pinks and gold must survive: ≤ 0.2 % of opaque pixels altered at the key-distance threshold, no green or white fringe (fringe metric as in HD intake F1), alpha snapped per stlib.clean, one component.
- E-S5 (derivatives): master `hd/characters/shaadi-shift-woman.webp` (lossless) plus `.web.webp` q85 at native pixels, cropped to the visible region. No upscale; width × height in the same range as the other chapter women (~730–810 × ~1020). md5s recorded in the manifest batch.
- E-S6 (evidence): contact sheet = the original, the matte on checker, the cutout on the Shaadi chapter ground (unmirrored phone and mirrored laptop), and a 100 % crop of the face, bindi, jhumka and pin.
- Results (2026-10-10), all of E-S1 to E-S6 pass:
  - The source has real alpha. The subject sat at alpha 252–253 and is snapped to 255; 117 px of alpha-1 specks were dropped. No key was needed, so the #00FF00 fallback wasn't used.
  - The cuts are left 90 % and bottom 96 %. The dupatta's right-edge cut (bottom 178 rows) is feathered over 64 px, leaving the right edge 0 % solid. The figure faces right.
  - Fidelity: dupatta ΔE00 1.42, gold 1.38, skin 4.92. The bindi, jhumkas, bead strands, embroidery, beaded border and gold pin are all present, in ink style, with no defects.
  - Fringe: light halo 0. The flagged dark rim is the drawn maroon ink outline (checked at 4× on white, the ground and black).
  - Files: web 780×1022 q92 (269 KB, larger than the other women because of the embroidery detail); master 1088×1426 lossless.
  - Contact sheet: tests/hd/contact-shaadi-shift-woman-E.png, including the laptop mirror mock.
