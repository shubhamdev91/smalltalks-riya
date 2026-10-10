# st-artwork: Phase 2 readjustment package (2026-10-09)

Nothing was generated, redrawn or recoloured. The only operations were crops, alpha masks, feathering, composites of existing approved assets, and WebP encoding.

Sources were downloaded read-only to `artwork/_source/`:
- From Shopify Files: the two ink sheets, the nail guide, the finger states and the 7 packages.
- `desi-diet-can-v1.webp` is a theme asset in theme 186649313493, not a Files upload. It was read via the Admin API (read-only).

Every asset has a lossless master at `<group>/<name>.webp` and a shippable q100 version at `<group>/web/<name>.webp`. Full data, including sizes, deltas, anchors and the pass/fail checks, is in `artwork/manifest.json` → `phase2`. The same data is split across `artwork/phase2.json` and `artwork/phase2-checks.json`.

## Characters (characters/, from desi-ink-characters-v2.png)
- 7 cells cut on their own alpha. The top is a natural hair silhouette and is left untouched.
- Straight panel cuts get a 36 px smoothstep alpha feather, except on bleed edges.
- RGB on opaque pixels is unchanged (Δ 0).
- Bleed edges and anchors follow the Board 2 hero placement:

  | Set | Bleed edges | Anchor |
  |---|---|---|
  | on-me | left + bottom | (0, 1) |
  | brainwave | left + top | (0, 0) |
  | diet-cherry | left | (0, 0.5) |
  | green-flag | right | (1, 0.5) |
  | shaadi-shift | left + bottom | (0, 1) |
  | wild-card | left | (0, 0.5) |
  | pinky-promise | left + top | (0, 0) |

- Suggested 150 css px wide at 390 (native ~280–311 px ≈ 2×).
- Web versions are 94–128 KB.
- Caveat: where black hair crosses a cut, the dissolve reads as a soft dark smudge on yellow and lime.
- Contact sheets: tests/contact-character-<set>.png and tests/contact-characters-hero-placement.png.

## Chapters (chapters/, from desi-ink-characters.png)
- Each panel is ~270×821 (1–2 px seam trimmed). Web versions are 103–120 KB.
- `-fade` variant: the top 38% dissolves to transparent, so the page's real campaign colour shows above the scene.
- Ground colour Δ (scene minus target), all FAIL: on-me [−11,−18,2], brainwave [−7,−1,−61], diet-cherry [−70,2,−10], green-flag [2,−40,−22], shaadi-shift [−18,19,−16], wild-card [1,−20,2], pinky-promise [−43,−5,−98]. Not recoloured.
- Resolution: 270 px wide only reaches 2× at ≤135 css px, so full-width chapter use would upscale.
- Contact sheet: tests/contact-chapters.png (raw | fade on the true colour).

## Guide (guide/)
- nail-guide.webp: 1086×1448, alpha despeckle only, RGB Δ 0. Web version 184 KB.
- nail-guide-asis.webp: untouched copy.

## Shop (shop/)
- finger-state-<set>.webp: 7 crops on a common 248×658 canvas, tip anchor (0.5, 0.0091). Web versions ~61–66 KB.
- lifestyle-<set>.webp: 571×679 on the set colour. The preview hand carries the set's own nails, per preview_slots. Web versions 79–85 KB.
- Contact sheets: tests/contact-finger-states.png, tests/contact-lifestyle.png.

## Packaging (packaging/)
- As-is, no upscaling. Status: "awaiting hi-res from owner".

## Flags for orchestrator/owner (not fixed)
1. desi-diet-can-v1.webp shows a legible "Diet Coke" wordmark. That's an owner conflict. The only crop that removes it keeps the lower can body plus 3 nails, and its hard top cut would have to sit off-canvas (rejected/can-crop-proposal-below-wordmark.webp). Not shipped. The v2 character can and the chapter can are both plain and unbranded: PASS.
2. Character sheet v2: all seven cells read as the same woman, so the "distinct women" requirement FAILs.
3. Character checks:
   - Pinky Promise: the hands are clasped, not a pinky hook. They read as plausible, but the finger structure needs a human look. One nail is solid burgundy and one is lilac without a tip.
   - Brainwave: no crescent-bag sketch is visible.
4. Chapter checks:
   - Pinky Promise: no hands at all (FAIL).
   - On Me: no bill (FAIL).
   - Brainwave: bag and sketchbook PASS, no blue pen.
   - Shaadi Shift: the safety pin is unclear.
   - Wild Card cards face her: PASS. Green Flag rotary phone: PASS.
   - No nails are visible in any scene.
5. Finger states:
   - Shaadi Shift has two white-centred flowers, but the set has one red-centred flower.
   - Pinky Promise has a crimson tip, not burgundy.
   - The source order isn't motion_index, so the crops are re-keyed by handle.
6. Chapter ground colours don't match the metaobjects (see the Δ list above).

Crops for each check are in tests/checks/.
