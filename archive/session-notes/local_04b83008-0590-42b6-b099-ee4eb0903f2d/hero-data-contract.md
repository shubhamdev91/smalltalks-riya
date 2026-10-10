# st-hero — data contract for the motion controller

Theme 186651934933. Written by the foundation session, 9 Oct 2026. Local mirror of every file:
`C:\Users\SSTS\Desktop\Riya\theme-build\src\` (same paths as in the theme).

## Files
- `sections/st-hero.liquid` — markup, CSS geometry, JSON data block, schema (campaign blocks).
- `snippets/st-sprite.liquid` — atlas cell → `<img>` in an overflow box (`.st-sprite` + `.st-sprite__img`).
- `snippets/st-nail.liquid` — campaign + role → sprite.
- `snippets/st-nail-crop.liquid` — crop table (single source of truth for atlas geometry).
- `snippets/st-nail-sequence.liquid` — 5-nail role sequence per set (preview hand uses items 1–4).
- `snippets/st-campaign-colors.liquid` — scene/CTA colours + contrast guard. `st-campaign-url.liquid` — set URL.
- No JavaScript ships for the hero. Load the controller as a module from the section (or an asset) when ready.

## Root element
`<section class="st-hero" data-st-hero …>`
- `data-active-key` (campaign handle, first block), `data-active-index="0"`, `data-next-key` (second block)
- `data-tone` (1–4, from section setting, default 2), `data-tone-count="4"`
- `data-autoplay` ("true"/"false", section setting)
- Inline custom properties: `--st-scene`, `--st-scene-ink`, `--st-cta-bg`, `--st-cta-ink`, `--st-tone-swatch`
- Geometry custom properties on `.st-hero` (CSS): `--hero-h`, `--finger-h`, `--finger-w`, `--finger-cx`,
  `--accent-w`, `--preview-w`, `--preview-right`, `--preview-lift` (redefined ≥990px).

## Parts (all inside the root)
| Selector | What | Notes |
|---|---|---|
| `[data-st-hero-note]` | handwritten note `<p>` | text = campaign.note |
| `[data-st-hero-headline]` | `<h1>` | text = campaign.headline |
| `[data-st-hero-finger]` | finger box, bottom-anchored | contains `[data-st-hero-tone-sprite]` (`.st-sprite`, finger atlas) |
| `[data-st-hero-main]` | signature nail wrapper inside the finger | bottom edge = cuticle; `bottom: 74.3%`, `width: 52%` of finger |
| `[data-st-hero-accent="1"]` | accent nail sprite (nails row 1) | wrapper `.st-hero__accent--1` |
| `[data-st-hero-accent="2"]` | extra nail sprite (accent atlas) | wrapper `.st-hero__accent--2` |
| `[data-st-hero-preview]` | next set's preview hand | `data-key` = next handle; contains `.st-hero__hand` img |
| `[data-st-hero-preview-nail="0..3"]` | four nails on the fingertips | anchored at cuticle (bottom-centre), `rotate` per finger; slot 0 = index finger … 3 = little finger |
| `[data-st-hero-character]` | campaign character (feathered mask) | only when "Show campaign character" is on |
| `[data-st-hero-cta]` | `<a class="st-cta">` | text `Shop “Name” ↗`, href = set URL |
| `[data-st-hero-pause]` | pause button | `aria-pressed="false"`, `aria-disabled="true"` until the controller attaches |
| `[data-st-hero-tone]` | tone button (swatch = `--st-tone-swatch`) | `aria-disabled="true"` until attached; label includes "Skin tone n of 4" |
| `[data-st-hero-status]` | `aria-live="polite"` `<p>` (visually hidden) | empty at first paint |

## JSON: `<script type="application/json" data-st-hero-data>`
```json
{
  "version": 1,
  "autoplay": true,
  "defaultTone": 2,
  "tones": [{ "index": 1, "swatch": "#efa67d", "crop": { "x": 111, "y": 108, "w": 280, "h": 832 } }, "… 4 tones (x 111/512/905/1301)"],
  "finger": { "atlas": "//…/desi-finger-tones.png?…&width=1672", "atlasWidth": 1672, "atlasHeight": 941,
              "cuticle": { "x": 0.5, "y": 0.257 }, "nailWidth": 0.52 },
  "previewHand": { "image": "//…/desi-preview-hand-base.png?…", "nailWidth": 0.1,
                   "anchors": [{ "x": 0.138, "y": 0.805, "rotate": 225 }, { "x": 0.204, "y": 0.876, "rotate": 218 },
                               { "x": 0.33, "y": 0.878, "rotate": 222 }, { "x": 0.52, "y": 0.847, "rotate": 226 }] },
  "atlases": { "accents": "//…/desi-nail-accents-v2.png?…&width=2172" },
  "campaigns": [{
    "key": "on-me", "name": "On Me", "headline": "Bill idhar.", "note": "I’ve got this.", "index": 0,
    "colors": { "scene": "#ffb900", "ink": "#180e0b", "ctaBackground": "#a00027", "ctaForeground": "#fffaf0" },
    "url": "/products/bill-idhar", "ctaLabel": "Shop “On Me”", "journalUrl": null,
    "art": { "nails": "//…/desi-nail-overlays.png?…&width=2400", "character": "//…/desi-ink-characters-v2.png?…",
             "previewHand": null, "packaging": "https://cdn.shopify.com/…/bill-idhar-approved-package.png?…" },
    "crops": { "signature": "80,28,184,319,0,7,2", "accent": "80,13,184,319,1,7,2",
               "extra": "23,126,280,496,0,7,1", "character": "8,56,294,631,0,7,1" },
    "sequence": [0, 2, 1, 2, 0], "previewSequence": [2, 1, 2, 0]
  }, "… 7 campaigns in block order"],
  "cropFormat": "x,y,w,h,row,cols,rows (px inside the atlas cell; column = campaign index; nail cuticle = bottom edge)",
  "roles": ["signature", "accent", "extra"]
}
```
- `colors.ctaForeground` is already contrast-guarded (Wild Card → `#09195d`).
- `journalUrl` is null while the Journal articles are unpublished.
- `art.previewHand` is a per-set override image (block setting); when null, build the hand from `previewHand.image`
  plus the next set's `previewSequence` roles at `previewHand.anchors`.
- Role numbers: 0 signature (nails row 0), 1 accent (nails row 1), 2 extra (accent atlas).

## Sprite maths (same as Liquid)
For atlas width `W`, height `H`, grid `cols × rows`, cell column = campaign `index`, row from the crop:
`cellW = W/cols`, `cellH = H/rows`, `left = cellW*col + x`, `top = cellH*row + y`;
wrapper `aspect-ratio: w / h`; img `width: (W/w)*100%`, `left: -(left/w)*100%`, `top: -(top/h)*100%`.
Changing a set = swap `--sprite-left/--sprite-top` (and `src` only if the atlas changes).

## Constraints already honoured by the static paint
- Only the signature-nail atlas image has `fetchpriority="high"`; finger and accents eager; preview, character lazy.
- Reduced motion: global guard in `snippets/st-brand-styles.liquid` sets animation/transition durations to 0.01ms.
- Nothing in the hero is fixed-positioned; all parts are absolutely positioned inside `.st-hero` (overflow hidden).
