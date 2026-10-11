# "the talks" wordmark: V1 FINAL (the owner's pick). st-fable, 10 Oct 2026

**V1, confident:** Caveat 700 (OFL), tracking −0.015em, "the" + 0.2 em + "talks", rotated −3°, ink #0d0b10, no swash.
The site header adds the small ↗. The hub title has no arrow.

## Asset
- `st-talks-wordmark-v1.svg`: outlined paths, made by `build_v1_svg.py` from `spec/fonts/caveat/Caveat[wght].ttf`
  instanced at wght 700, with the font's own pair kerning and the rotation baked in.
  - `fill="currentColor"`, `aria-hidden="true"`, 9.3 KB, md5 d31734b678854a8839ee038ef73d80ee.
  - viewBox 92.5 −744 2922.6 837.7; aspect 3.489 : 1.
- Size rule: **height = 0.8377 × the font-size it replaces** (`height: 0.8377em` on the SVG inside the element whose
  font-size is the old wordmark size). Width is auto.
  | Where | font-size | SVG w × h |
  |---|---|---|
  | header ≤ 320 | 19.5 px (`min(var(--fs-talks) * 0.7, 6.1vw)`, unchanged) | 57 × 16.3 |
  | header | 23.8 px (unchanged) | 69.6 × 19.9 |
  | hub title, phone | 40 px | 117 × 33.5 |
  | hub title, desktop | 52 px | 152 × 43.6 |
- Check: `v1-check.png` shows the live text (column 1) against the SVG (column 2) and the header lockup with the arrow
  (column 3) at all four sizes. The shapes match.

## Markup
```html
<!-- site header (st-header): one link, 44 px target -->
<a class="st-header__talks" href="/blogs/the-talks">
  <span class="visually-hidden">the talks</span>
  {% render 'st-talks-wordmark' %}   <!-- inline SVG, aria-hidden -->
  <span class="st-header__talks-arrow" aria-hidden="true">↗</span>
</a>
<!-- hub title -->
<h1 class="st-talks__title"><span class="visually-hidden">the talks</span>{% render 'st-talks-wordmark' %}</h1>
```
```css
.st-header__talks { display: inline-flex; align-items: center; min-height: var(--minimum-touch-target); color: #0d0b10; }
.st-header__talks svg, .st-talks__title svg { height: 0.8377em; width: auto; display: block; }
.st-header__talks-arrow { font-family: var(--font-ui); font-weight: 500; font-size: 0.5em; line-height: 1;
                          margin-left: 0.22em; transform: translateY(-0.12em); }
.st-talks__title { font-size: 40px; margin: 0 0 4px; }          /* 52px at >= 1024 */
```
- The drawer link (`.st-drawer__talks`) uses the same SVG without the arrow.
- Hover and focus: keep today's underline-on-hover on the link (`text-decoration` doesn't reach an SVG, so use a 1 px
  `box-shadow` or `border-bottom` under the lockup) and a visible focus ring.
- OFL: Caveat's `OFL.txt` stays with the theme's font licences (the outlines are derived glyphs).

## Acceptance (mine, talks after-shots)
Header at 390 / 1536 / 1920 and the hub title at 390 / 1536, on the preview:
- the mark is the SVG at the sizes above, ink colour;
- the ↗ sits on the x-height, inside the link;
- the link is 44 px tall, with the accessible name "the talks";
- nothing is clipped, and the header row height is unchanged.
