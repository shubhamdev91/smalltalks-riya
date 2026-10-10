# Small Talk hero motion: DOM and data contract (v3.8, 10 Oct 2026, board 2 re-fit + HD art + desktop composition)

v3.8: **owner request: desktop/laptop hero composition (≥ 1024 px).** CSS only; JS, DOM and data are unchanged from
v3.7.2/v3.7.3, so st-foundation needs **no Liquid change**. Phones (< 990) are byte-for-byte the v3.7.3 geometry;
990–1023 keeps the v3 rule.
- **Size unit:** `--k` becomes `min(100cqh / 560, 100cqw / 1100)`. Height drives it, and width caps it on narrow
  laptops (1024 × 768). Every k-sized element grows together: finger, nail, loose tips, next-set hand, character art,
  note, controls. At 1280 × 720 (hero 651) the nail is 172 px wide, against 133 px in v3.7.
- **Scene, left of centre:**
  - Finger cuticle at `cx = max(380k, 50cqw − 260k)`, `cy = 100cqh − 175k`.
  - Loose tips sit right of the nail on every set (reading order: character → finger → tips → copy).
  - Characters stay on their bleed edge but larger and lower or closer, so they read with the finger as one scene.
    Brainwave and Pinky faces are 200k wide. On Me sits bottom-left. Diet Cherry's can is at mid height. Shaadi Shift
    and Wild Card are bottom-anchored. **Green Flag is mirrored** (`scale: -1 1`) to bleed left beside the finger; the
    copy owns the right, and the art has no lettering.
- **Copy block, right of the scene** (`x0 = cx + 230k`), vertically centred at 48%:
  - Note, then the headline at 1.1 × k with a flatter arc (`--arc-r: 680`).
  - The pill directly under the headline: gap ≥ 27 px measured on the bent letters, with a per-set sag allowance
    `--dpg`.
  - Note → headline 11–18 px.
- **Glow centred on the subject:** each set's radial gradient sits on the nail (`--gx/--gy`) with radii × 1.6, for the
  root and the cross-fade scene.
- The next-set hand keeps its top-right entry (its art is cut on top and right), now k-sized, so larger.
- **Verified in the lab** at 1280 × 720, 1440 × 800, 1536 × 703 and 1024 × 768, all 7 states:
  - no copy overlapping the hand, controls or character art;
  - copy fully inside the hero;
  - loose tips clear of the art;
  - 7 flights: start ≤ 0.6 px, end ≤ 0.4 px.
  - Phones re-checked at 390 × 844: unchanged (nail 148, note gap 12 on all 7, pill 24/339).
- Sheet: `qa/fidelity/hero-v38-desktop-lab-1280x720.png`.

v3.7.3: **owner override: campaign body at 50%.** CSS only; JS and DOM are unchanged from v3.7.2.
- `--note-scale: 0.5` on `.st-hero` scales the note's font and wrap width, so line breaks stay as on the board. Ticks
  are now em-sized (0.48 × 0.55 em), so they scale with the note. Font floor: 16 px, which keeps 320 × 568 legible.
- Each note is re-placed 12 px above the headline (measured on the arc letters under the note), with the same x and
  tilt. New `--note-y` values: On Me 113, Brainwave 169, Diet Cherry 109, Green Flag 146, Shaadi Shift 152, Wild Card
  109, Pinky Promise 172. Headline size and position are unchanged.
- To retune, change `--note-scale` (and re-derive `--note-y` if the gap matters).

v3.7.2: **held first-paint art.** The set 1 character and the preview hand no longer download while the LCP image (the
finger tone) is still loading. JS + CSS change.
- **Liquid (`st-hero.liquid`):**
  - The first-paint character `<img data-st-hero-character-img>` and `<img class="st-hero__hand">` carry their URL in
    `data-st-src`, not `src`. Keep `width`, `height`, `alt=""` and the classes; add `decoding="async"`
    `fetchpriority="low"`; no `loading` attribute.
  - Without JS they stay empty. That's acceptable, because both are decorative and the hand button needs JS anyway.
- **JS:** once the tone has loaded (the same gate that fills the preview nails), `revealHeld()` copies `data-st-src` to
  `src` and removes `loading`. It clears `data-st-src` when the image has loaded. A set change before that updates the
  held URL, so the reveal always shows the current set; after the reveal, set changes write `src` as before.
- **CSS:** `.st-hero img[data-st-src] { opacity: 0 }`, then a 0.25 s opacity fade on the character image and the hand
  (no transition under reduced motion).
- **Not in the hero contract:** the Our Vision tile is st-foundation's gallery. It's at the fold at 390 × 844, so gate it
  like the tiles collage (set its `src` after the tone, 0.25 s fade). No CSS or JS from me is needed.
- **Expected:** at 390 × 844 the only image requests before the tone finishes are the tone and set 1's sheet. That frees
  about 113 KB (character 76 KB + hand 37 KB, plus the tile's 104 KB if gated) on the critical link.

v3.7.1: **load plan, main-thread trims and the a11y fix** (operational QA F1, F2, F4). JS changes; CSS unchanged from v3.7.
- **Load order (JS):**
  1. Init renders set 1 without filling the preview nails.
  2. After set 1's sprite has decoded and the first-paint finger tone (the LCP image) has loaded (8 s cap), the preview
     hand gets the next set's nails.
  3. After window `load` (capped at 4 s) plus the next idle period, the next set's art is prefetched and autoplay starts.
     A tap, swipe, arrow or pause before then still works; it fetches on demand, and autoplay then stays off (v3.2
     rule).
- **Main thread (JS):**
  - Headline re-bends on resize and font arrival are coalesced (120 ms), and only the headline's own face (Fraunces)
    triggers one. The home page loads about 10 font files, and each `loadingdone` used to force a synchronous
    re-layout.
  - After a flight the bend runs in the next animation frame (the headline is fading in from 0), which splits the
    commit into two shorter tasks.
  - New pause reason `overlay`: any `dialog[open]` (menu drawer, cart, search) pauses flights and dwell timers until it
    closes. `details` accordions don't count.
- **Liquid (st-foundation, `st-hero.liquid` and the layout head):**
  1. `<head>`, before the stylesheets: preload the LCP image and set 1's nail sheet, nothing else from the hero:
     `<link rel="preload" as="image" href="{{ 'st-hd-tone-2.webp' | asset_url }}" fetchpriority="high">` and
     `<link rel="preload" as="image" href="{{ set-1 hero_sprite | asset_url }}" fetchpriority="high">`. Only on the home
     template (or wherever the hero renders).
  2. Tone `<img>`: keep `fetchpriority="high"`, no `loading` attribute, no `srcset`.
  3. **Preview nails: no `--st-nails` at first paint** (`style="--col:N"` only). The controller fills them after the LCP
     image. The preview hand `<img>`: `fetchpriority="low"` (keep `loading="lazy"`).
  4. Set 1 character `<img>`: `loading="lazy" fetchpriority="low" decoding="async"` (as before; it is decorative).
  5. **a11y (F4):** remove `aria-hidden="true"` from `div.st-hero__finger`, and add `aria-hidden="true"` to
     `img.st-hero__tone` (it is already `alt=""`). `button.st-hero__main` stays focusable with its label and description:
     it is a real control (Space/Enter hold pauses, the same as pointer hold). The main nail `span` carries no
     semantics. No CSS or JS change is needed for this.
- **Target (lab, Slow-4G):** the tone and set 1's nail sheet are the first two image requests, and no other image starts
  before the tone finishes. The next set's sprite starts only after the tone. Hero autoplay starts after `load`.

v3.7: **hero-v2 cuts** (`artwork/manifest.json` → `hd.batches["hero-v2"]`). CSS only; the JS is byte-identical to
v3.4–v3.6. Install after v3.6 (or instead of v3.6's CSS if v3.6 isn't live yet). The data changes below add to the v3.6 list.
- **Green Flag:** v2. `hd/characters/green-flag-woman-hero-v2.web.webp` (729 x 1020), bleed `["right"]`. Her face is
  at board frame 4's scale (hairline to chin ~180 px vs board ~170; v1 was ~130). The arm and cord run down behind the
  pill. The slivers are gone and the top is feathered in the file, so v3.4's image mask is removed. Placement: 298.9 k
  wide, anchored to the right edge (+8.3 k bleed), centre at 516.6 ky.
- **Shaadi Shift:** v2. `hd/props/shaadi-shift-pin-hero-v2.web.webp` (331 x 1172), bleed `["left"]`. Tall dupatta strip
  with the pin vertical, as on frame 5. Placement: 125.8 k wide, **anchored to the hero bottom** (top =
  100cqh − 446.3 k), so the strip reaches the bottom at 320 x 568, 390 x 844 and 390 x 932.
- **Pinky Promise:** v2. `hd/characters/pinky-promise-face-hero-v2.web.webp` (340 x 516), bleed `["left", "top"]`. Full
  profile with cheek, lips and chin, as on frame 7. Placement: 119.8 k wide at −8.2 / −8.3 k. A 5% right-edge image mask
  softens two hair curls that touch the file's right edge.
- **Wild Card:** unchanged; the hero-v2 entry is an alias of the v3.5 cut.
- **v1 files stay available.** To revert a set, restore its v3.6 CSS block and data.

v3.6: **HD nail sheets** (`hd/nails/<set>.web.webp`, 1350 x 780, cells 450 x 780; st-artwork's 10 Oct re-cut). CSS changes
one line (loose accents 78 -> 82 k). The JS is byte-identical to v3.4/v3.5. Install after v3.5, or together with it.
- **Re-cut sheets:** every cell's plate base sits at 0.924–0.926 of the cell height, centred at 0.5, with no specks
  below. Plates are 0.838–0.853 of the cell width, against 0.887–0.902 on the P1 sheets.
- **Main nail scale unchanged (cell 148 k = 0.526 of the finger canvas).** The HD plate then renders at 123–125 px wide
  at 390, against 122 px on board 2 frame 1 (P1 renders 130). It sits on a 177 px HD finger (board ~170), which keeps
  the board's press-on to finger ratio (0.70 vs 0.72). Do **not** use st-artwork's physical fit (1.08 x natural plate,
  cell 0.474 of the canvas). That renders 113 px, 7% narrower than the board. Sheets: `qa/fidelity/hero-v36-compose.png`
  and `hero-v36-main-nail-vs-board.png`.
- **Accents:** 82 k keeps the accepted loose-nail plate width (82 x 0.846 = 69 px, as 78 x 0.89 before).
- **Preview hand slots unchanged.** HD plates still cover the hand's natural nails (about 1.16x).
- **Data:** each campaign's `sprite` changes to `hd/nails/<set>.web.webp`. So do the first paint's inline `--st-nails`
  URLs (main, accents and preview nails) and the sprite preload. Column order is unchanged in all 7 sets.
- **On Me hero cut (data only, added after the freeze; CSS and JS unchanged):** On Me `character.src` changes to
  `hd/characters/on-me-woman-hero.web.webp` (535 x 721, the same size and placement as v3.4's On Me piece). Same for
  the first-paint character `<img>` (width 535, height 721). The landing keeps `on-me-woman`. The bottom is feathered
  and bleeds below the hero at every checked size (320 x 568 to 1280 x 800).
- **Still to come from st-artwork:** the hero re-cuts for the Shaadi Shift taller crop, the Pinky Promise profile
  feather and the Green Flag slivers. Each arrives as a file swap at the same placement, or as a new version if the
  placement changes.

v3.5.1: documentation only. Adds the rule that `bleed` and `parts` are JSON arrays. JS and CSS are unchanged from v3.5.

v3.5: HD finger tones and the batch `chatgpt-AB-1` hero art (`artwork/manifest.json` → `hd.batches["chatgpt-AB-1"]`).
**CSS only; the JS is byte-identical to v3.4.** Install v3.4 and v3.5 as one step: the v3.5 CSS replaces the v3.4 CSS, and
the data changes below add to the v3.4 list.
- **Fingers:** `hd/fingers/tone-1..4.web.webp`, 558 x 1512. Same aspect and nail-bed anchor (0.5, 0.2649) as 310 x 840, so
  no geometry change. Tone `<img>` attributes become `width="558" height="1512"`. Swatches change to the HD skin medians:
  tone 1 `#e99a6f`, 2 `#d18256`, 3 `#a25838`, 4 `#86472f`. Tone 4 is visibly lighter than v3.4's `#713f2c`.
- **Brainwave:** `hd/characters/brainwave-woman-hero.web.webp` (299 x 542) replaces the atlas character. Half-face, bleeds
  left and top, bottom feathered in the file. The old CSS fade (`--ch-mask`) is removed.
- **Wild Card v2:** `hd/characters/wild-card-woman-v2-hero.web.webp` (366 x 1019) + part `hd/props/wild-card-cards-hand-v2-hero.web.webp`
  (362 x 492): curly hair, lime saree, red card backs. v2 has a clean top, so v3.4's top feather is removed.
- **Diet Cherry** keeps `st-diet-can.webp`. The new can hand enters from the right, and mirroring would reverse the wordmark.
- **Nails (superseded by v3.6): kept `nails/web/<set>.webp`. The HD sheets were not yet a drop-in at the time.** Their
  plates are 0.76–0.84 of the cell width (current 0.89–0.90). In 15 of 21 cells the plate base sits above the 0.925
  anchor: at 0.871–0.912 of the cell height (current 0.921–0.924). On the main nail that leaves a 5–11 px crescent of bare
  natural nail under the press-on for On Me, Diet Cherry, Shaadi Shift, Wild Card and Pinky Promise (sheet
  `qa/fidelity/hero-v35-nail-base-current-vs-hd.png`; also visible on the On Me tile of `artwork/tests/hd/fingers-anchor-hd.png`).
  Swap once each cell is re-normalised: plate base at 0.925, width about 0.89, centred at 0.5. The swap is a data-only
  change; no CSS change is needed.

v3.4: HD preview hand and HD half-face art (st-artwork batch `board-corrections-1`, `artwork/manifest.json` →
`hd.batches["board-corrections-1"]`). JS + CSS changed.
- **Preview hand:** `artwork/hand/hd/preview-hand.web.webp` (510 x 498). New slot numbers; same slot convention. Rendered at
  335 k (not the 170 px st-artwork recommends): that keeps the press-ons at the board size (~28 css px wide, as in v3.3).
  Position: top −139 k, right −170 k (least-squares fit of the new slots to the accepted v3.3 board fit, then 8 px up).
- **Characters:** On Me woman, Green Flag woman-hero, Shaadi Shift pin-hero, Wild Card woman-hero + cards-hand-hero (interim),
  Pinky Promise face-hero, placed per set in CSS at the manifest's 390 placements (vertical anchor = piece centre in `ky`,
  size in `k`; Pinky bleeds off the top). Brainwave and Diet Cherry are unchanged.
- **New optional JSON field `character.parts`:** extra layers painted above the main image (Wild Card's cards hand). The
  controller creates `<img data-st-hero-character-part="n">` inside the character box on demand and hides unused ones.
- **Image-relative masks** (`--ch-img-mask`, on the main image only): Green Flag drops four stray phone-outline slivers left of
  the woman and softens the hair's top cut; Wild Card softens the woman's flat top cut (both edges are the source image's top).
- Layer order unchanged: art (z 1) below the preview hand (2), finger (3), accents (4/5), copy (6), flyers (7), controls and
  pill (8).

v3.3: during a flight onto the main nail, the old nail stays at full opacity until 80% of the flight and then hands over
under the arriving flyer (was: faded out by 45%, which showed the bare natural nail for ~250 ms). JS only; CSS = v3.1.

v3.2: a manual step (hand tap, swipe, arrow) or pause/replay made while set 1 is still decoding is no longer overridden
by the autoplay start (found on the preview: a tap in the idle phase was swallowed). JS only; CSS = v3.1.

v3.1: headline `word-spacing: 0.2em` (the −0.06em tracking ate the word spaces). CSS only; JS and DOM unchanged from v3.

Owner: Fable session. Files: `motion/st-hero-motion.js` (controller), `motion/st-hero.css` (layout + per-set geometry),
`motion/lab/index.html` (reference DOM, generated by `python -I motion/build-lab.py`). Spec: `spec/hero.md`, `spec/tokens.css`.
v2.3 files are archived in `motion/archive/`.

## What changed from v2.3
- Composition follows board 2 at 390 px (the acceptance bar): bigger finger and main nail, large loose accents, big preview
  hand from the top-right, cropped half-face characters, Fraunces arc headline, Caveat note with sparkle ticks, full-width pill,
  per-set radial glow. Side-by-sides: `qa/fidelity/hero-<n>-<set>-390-vs-board.png`.
- Geometry is CSS, keyed on the root's `data-active-key`. The controller no longer writes inline positions for the character.
- Headline is split by the controller into lines, words and letters and set on an arc (radius 380 board px x k). The full text
  stays in the h1 as a visually hidden span; the letters are `aria-hidden`. Kerning is restored per letter (Range measurement).
  The 0.9 horizontal condense applies to `.st-hero__arc` (the aria-hidden letters) only; the h1 and its hidden text are unscaled.
- Cross-fade uses `.st-hero__scene[data-key]` gradients (controller sets `data-key`), not a flat colour.
- Optional JSON per campaign: `sampleColumns: [a, b]` = columns shown on the two loose samples (display only; flights still
  use `flightColumns`). Default: flight columns padded with unused accent columns (Pinky Promise shows 1 and 2).

## Scaling
The root is `container-type: size`. Board px map to `--kx = 100cqw/390` (horizontal positions), `--ky = 100cqh/775`
(vertical positions), `--k = min(kx, ky)` (sizes). Hero height `clamp(30rem, 100svh - var(--st-header-h, 69px), 60rem)`.
Touch targets keep `max(44px, ...)`. Desktop (>= 990 px): same composition spread across the width; copy and pill start right
of the character column (+200 k).

## Non-negotiables the Liquid must respect
1. Static first paint renders set 1 completely with CSS only (sprite URLs as inline `--st-nails`, `--col`), with
   `data-active-key` on the root (all per-set geometry hangs off it).
2. No CSS `transform`/`translate`/`scale`/`rotate` on any ancestor of a nail element. Nails rotate only through
   `rotate: var(--rot)` on `.st-nail`, transform-origin 50% 92.5%. (The headline is rotated and condensed; it holds no nails.)
3. All nail elements are absolutely positioned descendants of `[data-st-hero]`.
4. Sprites: one WebP per set, 3 cells (signature | accent | extra), cell 204x354, anchor (0.5, 0.925).
5. Fonts: `Fraunces` (a static wght 900 / SOFT 100 / WONK 1 / opsz 144 instance is fine; declare it `font-weight: 900` so
   the browser never synthesises bold), `Caveat` with weight 700 available (the note uses 700), `Barlow Semi Condensed` 600,
   declared with these family names (OFL files in `spec/fonts/`). Preload Fraunces (the headline is the largest text).
6. No theme class on the note or headline may set font-family/size (v2 markup used `st-pen` / `st-display`: remove them).
7. `:root { --st-header-h: 69px }` (or the real header height) so the hero fills the first screen.

## DOM (attribute = required hook)
```
<section class="st-hero" data-st-hero data-active-key="on-me" data-active-index data-next-key data-tone data-tone-count data-autoplay>
  <div class="st-hero__scene" data-st-hero-scene aria-hidden="true"></div>
  <div class="st-hero__character" data-st-hero-character aria-hidden="true" data-bleed="...">     <!-- NO inline style -->
    <img data-st-hero-character-img data-st-src=... width=... height=... alt="" decoding="async" fetchpriority="low">   <!-- v3.7.2: URL held in data-st-src -->
    <!-- optional, only if the FIRST set has character.parts (else the controller creates them): -->
    <img data-st-hero-character-part="1" src=... width=... height=... alt="" decoding="async">
  </div>
  <button class="st-hero__preview" data-st-hero-preview aria-label="Next set: {name}" aria-disabled="true">
    <img class="st-hero__hand" data-st-src=preview-hand.web.webp width=510 height=498 alt="" decoding="async" fetchpriority="low">   <!-- v3.4 HD hand; v3.7.2 held -->
    <span class="st-nail" data-st-hero-preview-nail="0..3" style="--col:n"></span> x4   <!-- v3.7.1: no sprite at first paint; the controller fills it -->
  </button>
  <div class="st-hero__copy"><p class="st-hero__note" data-st-hero-note>...</p><h1 class="st-hero__headline" data-st-hero-headline>...</h1></div>
  <div class="st-hero__accent st-hero__accent--2"><span class="st-nail" data-st-hero-accent="2" style="--st-nails;--col"></span></div>
  <div class="st-hero__accent st-hero__accent--1"><span class="st-nail" data-st-hero-accent="1" style="--st-nails;--col"></span></div>
  <div class="st-hero__finger" data-st-hero-finger>   <!-- v3.7.1: NOT aria-hidden (it contains the focusable hold button) -->
    <img class="st-hero__tone" data-st-hero-tone-sprite src=tone-N.web.webp width=558 height=1512 alt="" aria-hidden="true" fetchpriority="high">   <!-- v3.5 HD finger; v3.7.1 aria-hidden here -->
    <button class="st-hero__main" data-st-hero-main aria-label="Hold to pause" aria-describedby="st-hero-main-desc-{{ section.id }}" aria-disabled="true">
      <span class="st-nail" data-st-hero-main-nail style="--st-nails;--col:0"></span></button>
  </div>
  <div class="st-hero__flyers" data-st-hero-flyers aria-hidden="true"></div>
  <div class="st-hero__controls"> pause button (pause + play SVGs) · tone button with .st-hero__swatch </div>
  <a class="st-hero__cta" data-st-hero-cta href="...">Shop “{name}”<span class="st-arrow" aria-hidden="true">↗</span></a>
  <p class="visually-hidden" aria-live="polite" data-st-hero-status></p>
  <p class="visually-hidden" data-st-hero-main-desc id="st-hero-main-desc-{{ section.id }}">{name} nail design: ...</p>
  <script type="application/json" data-st-hero-data>{...}</script>
</section>
```
The arrow glyph is hidden by CSS (font-size 0) and drawn as a mask; keep the span.

## JSON changes in v3.4
`character` is `{ "src", "width", "height", "bleed" }` (intrinsic px of the web file). Placement is CSS; `anchor` and
`widthAt390` are no longer read. **`bleed` must be a JSON array of edge names** (`["left"]`, `["left", "top"]`, `["right"]`):
the controller writes `(ch.bleed || []).join(' ')` to the box's `data-bleed`, so a plain string would throw and stop the set
change. The same goes for `parts`: it must be an array of `{ "src", "width", "height" }` objects.

| Set | `character.src` (from `artwork/`) | width x height | bleed |
|---|---|---|---|
| on-me | v3.6: `hd/characters/on-me-woman-hero.web.webp` (v3.4: `on-me-woman`) | 535 x 721 | left |
| brainwave | v3.5: `hd/characters/brainwave-woman-hero.web.webp` | 299 x 542 | left top |
| diet-cherry | unchanged | | |
| green-flag | v3.7: `hd/characters/green-flag-woman-hero-v2.web.webp` (v3.4: `green-flag-woman-hero` 1201 x 825) | 729 x 1020 | right |
| shaadi-shift | v3.7: `hd/props/shaadi-shift-pin-hero-v2.web.webp` (v3.4: `shaadi-shift-pin-hero` 440 x 457) | 331 x 1172 | left |
| wild-card | v3.5: `hd/characters/wild-card-woman-v2-hero.web.webp` + `"parts": [{ "src": hd/props/wild-card-cards-hand-v2-hero.web.webp, "width": 362, "height": 492 }]` (v3.4's v1 interims are superseded) | 366 x 1019 | left |
| pinky-promise | v3.7: `hd/characters/pinky-promise-face-hero-v2.web.webp` (v3.4: `pinky-promise-face-hero` 254 x 466) | 340 x 516 | left top |

`tones` (v3.5): `[{ "index": 1..4, "swatch": #e99a6f / #d18256 / #a25838 / #86472f, "src": hd/fingers/tone-N.web.webp }]`. The first-paint
`--st-tone-swatch` for the default tone 2 is `#d18256`.

`previewHand` (if the section still emits it) → `{ "src": hand/hd/preview-hand.web.webp, "width": 510, "height": 498 }`;
the controller does not read it (slot geometry is CSS).

## JSON changes from v2.1
- `ctaLabel`: `Shop “{name}”` (owner chose the board's quotes).
- Diet Cherry `character`: `{ "src": st-diet-can.webp, "width": 1189, "height": 1323, ... }` (owner accepted the mark).
- Green Flag: `"sampleColumns": [1, 0]` (board 2 shows emerald + the blush green-tip design as loose samples).
- `colors` stay (used for `--st-scene` fallback); the board glows/inks/pills live in the CSS per set.

## Behaviour (unchanged from v2.3 unless noted)
- Timeline per set about 2.6 s; three sets then settle ("Play again"). Flights are WAAPI transform/opacity, hero-local.
- Pause reasons: user, hold, hidden, pagehide, offscreen, reduced. Hold: pointer, Space/Enter, blur releases.
- Manual: hand tap, ArrowLeft/Right on the hand, horizontal swipe. Announcements only on manual change.
- Reduced motion: no flights, instant manual changes, pause button hidden, autoplay never starts.
- Tone switch swaps after decode or 400 ms; finger geometry never changes with tone.
- Headline re-bends on resize (debounced) and when fonts finish loading.
- Lifecycle: section load/unload upgrade/destroy (listeners via AbortController, observers, animations, timers).

## Verification harness
`python -I motion/build-lab.py`, serve the repo root (`.claude/launch.json`: motion-lab 8765, motion-lab-2 8766), open
`/motion/lab/index.html?set=<key>`. The pane reports the document hidden when not displayed (decodes stall); front the tab,
and capture flights with screenshot bursts. Side-by-side tool: `python -I qa/fidelity/sbs.py <shot> <board crop> <out> <label> width`.
