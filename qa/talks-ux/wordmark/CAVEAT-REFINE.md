# "the talks": refined ORIGINAL (Caveat) + the "goes somewhere" arrow. st-fable, 10 Oct 2026

The owner kept the original handwritten Caveat wordmark ("handwritten works, but make it a bit more chic") and asked for
a small arrow showing the header wordmark goes somewhere. No new fonts: Caveat is OFL and already in the theme.

**Sheets:**
- `caveat-sheet.png`: NOW, V1, V2, V3 and V2 at +10 %. Each row shows the phone header (390), the laptop header
  (1536) and the hub title on phone and desktop.
- `caveat-1536-header-2x.png`: the 1536 header at real size (2× device pixels), with ink height and tap target.
- Lab script: `render_caveat.py`; numbers in `caveat-measure.json`.

| Variant | Recipe | 1536 header: ink / target |
|---|---|---|
| NOW | Caveat 600, 23.8 px, no arrow | 16 px / 68 × 44 |
| V1 confident | Caveat 700, tracking −0.015em, "the" + 0.2 em + "talks", tilt −3°, ink #0d0b10, + arrow | 19 px / 105 × 44 |
| **V2 swash (recommended)** | V1 + a soft red underline swash under "talks" (#c3021d, a hand-drawn curve 0.3 em high, under the word only) | 24 px (swash included) / 105 × 44 |
| V3 two-weight | "the" 500 at 0.78 em, lifted 0.18 em, + "talks" 700 at 1.06 em, tilt −2°, + arrow | 17.5 px / 97 × 44 |
| V2 +10 % | V2 at 26.2 px header size (a size variant only, if the owner wants a touch more presence) | 26.5 px / 115 × 44 |

**Recommendation: V2.** The same handwriting the owner likes, made confident (700, tighter, a slight lift). The single
red swash under "talks" is the chic "spilled tea" accent and echoes the brand red of the pills. It stays readable at
24 px and keeps the −30 % header size.

**The arrow (all variants except NOW):**
- the pills' own "↗" in DM Sans 500, at 0.5 em of the wordmark, 0.22 em after "talks", centred on the x-height
  (translateY −0.12 em), ink colour;
- inside the same `<a class="st-header__talks">`, `aria-hidden="true"`; the link's name stays "the talks";
- the target stays 44 px tall (wider: 105 px at 1536);
- the header only: not in the drawer list or the hub title.

**Build** (talks window, with st-talks; the header is site-wide in st-header):
- The wordmark as an outlined inline SVG from Caveat 700 (OFL), with the swash path in the same SVG and a hidden "the
  talks" (or aria-label on the link).
- The arrow stays live text (DM Sans is already loaded), so it inherits focus and hover colour.
- Sizes: the header mark at today's visual size (23.8 px font equivalent; 19.5 at 320). The hub title at 40 / 52 px with
  a 0.22 em bottom margin, so the swash clears the tagline.
