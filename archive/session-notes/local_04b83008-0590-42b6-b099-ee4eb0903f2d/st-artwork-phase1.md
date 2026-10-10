# st-artwork: Phase 1 hand-over (2026-10-09)

Package: `C:\Users\SSTS\Desktop\Riya\artwork\`. The single source of truth is `manifest.json`, which merges nails, fingers, hand, file sizes and test list. Total weight is 927 KB for all 12 WebPs, down from ~9 MB of PNG atlases.

## Nails: nails/<set-handle>.webp (7 files)
- Each file is a 612×354 sheet: 3 cells of 204×354, col0 signature, col1 accent, col2 extra accent. CSS: `background-size: 300% 100%` with positions 0% / 50% / 100%.
- Cuticle anchor sits at (0.5, 0.925) of the cell in every cell. Nail height is 318 px.
- Handles are the campaign metaobject handles (on-me … pinky-promise); set i = motion_index i.
- Extra accents were downscaled to match signature height, so all columns share one scale.
- Sizes are 43–118 KB, WebP q100 or lossless.

## Fingers: fingers/tone-1..4.webp (light → deep)
- Exact common canvas 310×840. Nail-bed anchor at (0.5, 0.2649), the same in all four (fixes M7).
- Main nail on finger: cell scale 0.76, cell anchor on the nail-bed anchor. The tip overflows the canvas top by ~70 px, so the container needs `overflow: visible`.

## Preview hand: hand/preview-hand.webp + preview-hand.json
- 511×639, lossless, 197 KB. Source was desi-preview-hand-base.png with the thumb removed by a smooth radial-edge mask. Nothing was generated, so anatomy and skin are photographic.
- Slots are listed index → little. Placement contract:
  - nail element width = `cell_width_frac_of_hand` × hand width, aspect 204:354
  - transform-origin at 50% 92.5%, placed on `cuticle`
  - `rotate(rotation_deg)`, all about −136° to −139° (this fixes the M2 jump if flights start from these angles)
  - `center` gives the same placement with the origin at the cell centre
- default_columns are [0,1,2,0]. The orchestrator owns the real per-set mapping (M4).
- Display size is ambiguous. Taken literally, "20–24% of 390" for the whole image gives nails ~8 css px. I recommend 146 css px of image, so the four-finger span is ~86 px (22%) and nails are ~13 px. Pick one.

## Tests (tests/)
- `hand-<i>-<set>-bg-with-<next>-nails.png` ×7. Left: hero-like 2× crop on the set colour, showing the next set's nails. Right: 2× detail.
- `nails-contact.png`, `fingers-contact.png`, `finger-anchor-test.png`.
- No fringe found on any of the seven colours. Known, accepted: at 3× zoom, ≤ 1 px of the ring finger's natural free edge can peek past the press-on tip.

## Phase 2
Waiting for Board 1 approval. Generating characters needs an image model. Only a Canva-type generate-image / remove-background connector is visible, and plugin:marketing:canva needs OAuth by the user. There is no local generator.

## Update after orchestrator guards (2026-10-09)
- Colour check (scripts/verify.py): the masters are now lossless, and every opaque pixel is RGB bit-identical to the source atlas (all 7 sets, signature and accent columns, and all 4 tones). The extra-accent column is resampled 0.64×, so it can't be compared pixel for pixel.
- Size trade-off: lossless nails are 118–156 KB and fingers 201–214 KB, over the 120 KB budget. Budget versions are in `nails/web/` and `fingers/web/` (q100, 41–80 KB, alpha identical, RGB mean delta ~1, p99 6–25, figures in derivatives.json). The orchestrator picks which set ships.
- Contact sheets on all seven colours: tests/contact-nails-<set>.png ×7, contact-fingers.png, contact-hand-1x.png, contact-hand-3x-thumb-edge.png.
- Hand judgement: PASS with caveats. At 1× it reads as a natural back of hand. At 3× the edge is smooth with no stump or straight cut. Caveats: a mild change of angle where the new edge meets the index finger's side, and a faint trace of thumb-shadow tone along the upper edge.
- Fallback asset request, if the reviewer rejects the hand: one photo of the same model's left hand, back view, relaxed, wrist entering from top-right at ~40°, four fingers slightly spread with nails facing camera, thumb tucked under the palm and fully hidden, same lighting, ≥2000 px tall, transparent or plain background.
- The Diet Cherry can is noted (D8): an unbranded can, no wordmark or trade dress. It applies to Phase 2 only. No Phase 1 asset contains the can.
- No Canva or external generator gets used without the orchestrator's OK.
