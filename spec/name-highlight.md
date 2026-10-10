# Landing chapter product name: highlighter swipe

Owner request: on each landing chapter, the product name between the nail row and the Shop pill becomes the focal point. It's set in curly quotes, slightly larger and bolder, with a subtle highlight in the set's own light hue. The highlight is not a box.

Mock contact sheet: `artwork/tests/name-highlight-mock.png`. Each row shows the board on the left and the proposal on the right, at 390, for all 7 sets.
- Tool: `spec/tools/name_highlight.py`.
- Measured data: `spec/name-highlight-check.json`.

## 1. Shape (same for all 7): a marker swipe plus a soft flash
- **Choice:** a highlighter stroke with slightly angled, uneven ends, sitting on a faint elliptical glow of the same hue.
  - A plain radial glow alone disappears on light grounds (On Me, Wild Card).
  - A plain skewed band reads as a box.
  - The stroke with angled ends reads as a highlighter.
- No new artwork: everything is CSS (clip-path plus gradients).

```css
.chapter__name {                      /* the <p>/<span> holding “Diet Cherry” */
  position: relative; display: inline-block; isolation: isolate;
  font: 700 26px/1.1 "Barlow Semi Condensed", sans-serif;   /* was 22px / 600 */
  letter-spacing: 0;
  padding: .20em .38em;              /* stroke = ink box + this padding */
  color: var(--name-ink);
}
.chapter__name::before {              /* marker stroke */
  content: ""; position: absolute; inset: 0; z-index: -1;
  background: var(--name-hl);
  clip-path: polygon(3% 10%, 99% 0%, 97% 92%, 0% 100%);   /* uneven, angled marker ends */
  transform: rotate(-1.5deg);
  filter: blur(.4px);                 /* soft marker edge (0.8 px at 2x) */
}
.chapter__name::after {               /* soft flash behind the stroke */
  content: ""; position: absolute; inset: -95% -28%; z-index: -2;
  background: radial-gradient(closest-side,
              color-mix(in srgb, var(--name-hl) 55%, transparent) 0%,
              color-mix(in srgb, var(--name-hl) 28%, transparent) 40%,
              transparent 100%);
  pointer-events: none;
}
```

- **Geometry relative to the text:**
  - stroke = ink box + 0.38 em left/right and 0.20 em top/bottom (≈ 100–188 × 29–34 px at 390)
  - rotation −1.5°, edge blur 0.4 px
  - glow ellipse radii = 0.78 × stroke width and 1.45 × stroke height, peak 55% opacity
- **Position:** unchanged. The name stays centred between the nail row and the pill (landing.md boxes).
  - The stroke is ~6–10 px taller than the old text line. Take it from the gap above the pill, not from the nail row.
  - Keep ≥ 8 px clear between the stroke and the pill top.
- **Quotes:** typographic “ ” (U+201C/U+201D), part of the visible text (copy decision; st-copy owns the string).
- **Static:** no animation, so nothing is needed for reduced-motion.

## 2–3. Colours per set (verified)
`--name-hl` is the set's light hue, from the nail sheet's light tones and the chapter's light accents, lifted to a highlighter tint. `--name-ink` is the set's deep tone.

The minimum contrast was **measured over every glyph pixel** of the rendered mock: the text colour against whatever lies under it, whether stroke core, blurred edge or glow. Thanks to the 0.20 em vertical padding, 97.9–100% of glyph pixels sit on the solid stroke core.

| Set | ground | `--name-hl` | `--name-ink` | min on glyphs | ink vs stroke | ink vs bare ground |
|---|---|---|---|---|---|---|
| on-me | #fbbe10 | #ffe59a | #470100 | **13.30** | 13.30 | 9.81 |
| brainwave | #033bd6 | #dfe7ff | #0a2a9e | **8.92** | 9.26 | 1.41 |
| diet-cherry | #d40319 | #ffd6d0 | #7a0010 | **8.23** | 8.60 | 2.09 |
| green-flag | #046f41 | #cdeedb | #013a1d | **8.02** | 10.37 | 2.07 |
| shaadi-shift | #f30b5e | #ffd3e3 | #8e0016 | **6.96** | 7.25 | 2.32 |
| wild-card | #aee60d | #f2ffbf | #0f0b5c | **16.03** | 16.22 | 11.55 |
| pinky-promise | #6919f9 | #e4d6ff | #5e0412 | **9.22** | 10.23 | 2.07 |

- **Guard:** the dark ink on its own fails against the dark chapter grounds (1.4–2.3:1, last column). The text is only legible because it always sits on the stroke.
  - Never render the name without the `::before` (e.g. a missing pseudo-element, forced-colors, or a wrapped line).
  - Fallback: `@media (forced-colors: active) { .chapter__name { color: CanvasText; } }`.
  - Keep the name on one line: `white-space: nowrap`. "Pinky Promise" at 26 px is a 188 px stroke, well within 390.
- **On Me and Wild Card:** these have light grounds. Their stroke is a pale tint of the ground (1.4:1 against it), so it reads as a gentle marker, as the owner asked; the dark ink stays 9.8–11.6:1 even where the glow fades.

Tokens to add to `tokens.css` (one pair per set):
```css
--name-hl-on-me:#ffe59a;      --name-ink-on-me:#470100;
--name-hl-brainwave:#dfe7ff;  --name-ink-brainwave:#0a2a9e;
--name-hl-diet-cherry:#ffd6d0;--name-ink-diet-cherry:#7a0010;
--name-hl-green-flag:#cdeedb; --name-ink-green-flag:#013a1d;
--name-hl-shaadi-shift:#ffd3e3;--name-ink-shaadi-shift:#8e0016;
--name-hl-wild-card:#f2ffbf;  --name-ink-wild-card:#0f0b5c;
--name-hl-pinky-promise:#e4d6ff;--name-ink-pinky-promise:#5e0412;
```

## Mock caveats
- The mock removes the board's baked name by inpainting. The faint smudge left of "Wild Card" is that inpaint touching the hair; it's not part of the design.
- The real build renders live text over the real chapter art, so the art layer (hair, can) may overlap the glow edge. That's fine: the glow is behind the text but above the ground.
- z-order: ground < glow < stroke < text. Character art follows the existing chapter layering.
