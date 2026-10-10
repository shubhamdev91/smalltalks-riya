# Fidelity phase prep (st-foundation, 9 Oct 2026)

Theme 186651934933. Read-only inventory; nothing here changes the theme.

## (a) Diet can art
- Source: theme 186649313493 `assets/desi-diet-can-v1.webp` (read only). md5 d827ef654799d627659492c9338c37fe, 215524 B,
  1189×1323 RGBA WebP.
- Local copies: `theme-build/ref/desi-diet-can-v1.webp` and `theme-build/src/assets/st-diet-can.webp`, both byte-identical.
- Upload to 186651934933 as `assets/st-diet-can.webp`: NOT DONE. The staged-upload write was denied by the session's
  permission classifier and is waiting on the user.
- Hero wiring once the spec lands: Diet Cherry's `character` entry in `snippets/st-motion-map.liquid` (w,h,ax,ay,bleed,w390)
  plus the `st-character-diet-cherry.webp` reference in `st-nail` / `st-hero.liquid` → `st-diet-can.webp`. The geometry
  numbers come from st-fable.

## (b) Colour and font tokens: where they live today

### One source for st-* CSS: `snippets/st-brand-styles.liquid` `:root`
These values come from Theme settings › Colors (`settings.color_palette`, stored in settings_data). Hard-coded fallbacks
are in the Liquid header.

| token | palette key | value | uses | role today |
|---|---|---|---|---|
| --st-blue | color3 | #1013B3 | 36 | links, focus ring, default CTA fill, header logo/icons, footer links, FAQ/help/question icons, pagination, thumb ring |
| --st-ink | color1 | #1F1A2E | 36 | default heading colour (--st-heading-color), header text, labels |
| --st-divider | color2 | #D8CFDA | 26 | rules, borders |
| --st-muted | color5 | #68616E | 22 | secondary text |
| --st-tint | color6 | #EEE8F5 | 21 | panels, placeholders, empty chapter |
| --st-plum | color4 | #4A243D | 14 | editorial headings (.st-editorial sets --st-heading-color), features, journal, teasers |
| --st-body | foreground | #272332 | 14 | body text |
| --st-ground | background | #FFFDF5 | 12 | page ground, CTA ink |
| --st-error | (fixed) | #A00027 | 5 | form errors |
| --st-heading-color | → ink / plum | | 1 | h1–h6 colour |

Layout tokens in the same block: --st-gutter (1rem / 2rem ≥750), --st-radius-card (.75rem), --st-section-space.

### Fonts (same snippet, @font-face)
- --st-font-display = ST Display (`st-font-4.woff2`), 14 uses + `.st-display`.
- --st-font-sans = ST Sans (`st-font-3.woff2`, 400–700).
- --st-font-pen = ST Pen (`desi-pen.woff2`, 300), the handwriting; `.st-pen`, 3 uses.
- --st-font-button = ST Condensed (600 `desi-condensed.woff2`, 700 `st-font-1.woff2`), 14 uses.
- Horizon's font roles (--font-body/heading/subheading/accent, button families) are mapped onto these in the same block.

### Per-campaign colours: `snippets/st-campaign-colors.liquid`
- Emits --st-scene / --st-scene-ink / --st-cta-bg / --st-cta-ink from the small_talk_campaign metaobject (shared data, read
  only), with a 4.5:1 contrast guard.
- Hard-coded fallbacks: #EEE8F5, #1F1A2E, #1013B3, #FFFDF5.
- Consumers: st-chapter, st-article (beats), st-hero.css (st-fable), PDP scene (--st-pdp-scene), product card (--st-card-scene),
  package panel and PDP media (--st-pack-bg = campaign background).

### Horizon chrome: `config/settings_data.json` "current" (theme-local)
Role settings point at palette keys. Remap these with the palette so cart drawer, quantity, variant pills, inputs, badges
and the search dialog follow the boards:
- primary button: bg/border color3, text background;
- secondary button: text/border color3;
- selected variant: bg/border color3;
- sale badge: bg color3;
- sold-out badge: color6 / color1;
- inputs: #FFFFFF / foreground / color2;
- drawer and popover: background / foreground / color2.

### Hard-coded colours outside the tokens
- Shadows rgb(31 26 46 / .18–.35): st-header (2), st-packaging (1), st-package-panel (2).
- `#fff`: st-talk-form (1).
- #EEE8F5 fallback in st-package-panel.
- Hero skin-tone swatches #efa67d / #d7895d / #9f5a3a / #713f2c in st-hero.liquid (motion contract data, leave as is).

### Plan for the switch (one place)
1. Add `spec/tokens.css` as `assets/st-tokens.css` (byte-identical) and load it in layout/theme.liquid right after
   `st-brand-styles`, or inline it there.
2. In st-brand-styles, repoint the legacy names to role aliases:
   - --st-heading-color → board burgundy;
   - --st-link / --st-hand (handwriting) → board blue;
   - --st-pill-bg → board red;
   - and so on.
   Then sweep the 36 + 36 blue/ink uses by role, not by find-and-replace: blue splits into link, handwriting and focus;
   ink splits into heading and text.
3. Remap the palette and the settings_data role keys above to the same values, so Horizon surfaces match.
4. Shadows and fallbacks become tokens. Campaign metaobject colours stay data-driven unless the spec overrides them per
   screen.

## (c) Structure for curved section edges and a continuous dashed beeline

Live templates are the suffixed ones:
- product.desi
- blog.desi / article.desi
- page.desi (our-story, nail-guide-desi)
- page.desi-help
- page.desi-talks
Keep each pair in sync with its unsuffixed twin.

### Landing order (templates/index.json)
st-hero → st-gallery → st-chapter (diet-cherry) → st-teaser (talks) → st-chapter (brainwave, green-flag) → st-teaser
(journal, guide) → st-chapter (shaadi-shift, on-me, wild-card, pinky-promise) → st-faq, then st-footer (footer group).
That makes 13 sections plus the footer: 13 joins, each crossed by the beeline.

### Constraints
- Every section sits in its own `.shopify-section` wrapper, so one SVG cannot span sections unless it is a page-level
  overlay. An overlay needs JS to measure dynamic heights and breaks with lazy content and reveal, so I'm not recommending it.
- st-chapter already draws a dashed thread, but only in its top "bridge" zone (3.25rem) and one side gutter. It has
  `overflow: hidden` and `isolation: isolate`.
- Other sections have flat edges, ground or tint backgrounds, and no thread.

### Proposed structure, pending the spec's SVG paths
1. Curved edges: each section clips its own top edge with the spec curve (clip-path: path() or an SVG mask) and overlaps
   the section above by the curve height (negative margin-block-start, z-index by `section.index`). No section needs to
   know its neighbour's colour.
2. Beeline: each section draws its own segment as an absolutely positioned SVG with preserveAspectRatio="none" and
   vector-effect: non-scaling-stroke (dashes stay in screen px).
   - Joins line up because the segment enters at (x_in, top) and leaves at (x_out, bottom). Section n's x_out equals
     section n+1's x_in, set per section from the spec.
   - The upper section draws the join crossing inside its overlap zone, above both backgrounds.
   - For an unbroken dash rhythm across joins, a small script sets each segment's stroke-dashoffset to the cumulative
     length so far. Without it the dash phase restarts at each join.
3. Clear zones: the segment avoids text, nails and buttons, as the current chapter thread does. The spec paths should keep
   to gutters and bridge zones, or the copy must reserve space.

### Sections needing structural change
- st-hero: bottom edge and beeline start. Liquid only; st-hero.css belongs to st-fable, so any edge CSS goes in a
  separate wrapper.
- st-gallery: top/bottom edges, segment.
- st-chapter ×7: the thread becomes the beeline segment, and the curved top replaces the straight bridge. Overflow rules
  change: clip the inside only.
- st-teaser ×3 (talks, journal, guide): top edge, segment.
- st-faq: top edge, segment.
- st-footer: top edge, line end.
- Single-section screens (shop, PDP, bag, journal, story, our story, talks, help, guide): edges only at the header/main
  and main/footer joins, and the beeline stays inside one section.
- Header: unchanged, as on the landing and hero boards.
