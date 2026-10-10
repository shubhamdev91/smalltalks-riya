# Hero motion controller — hand-off to Fable (9 Oct 2026, orchestrator)

## Target
- Theme `186651934933` "Small Talk — Claude build (Horizon)", UNPUBLISHED, Horizon 4.1.5. Preview: https://0nev20-vn.myshopify.com/?preview_theme_id=186651934933
- Write lock: currently **st-foundation**. Build the controller locally first; ask the orchestrator (`local_e4896004-68cd-4d55-9d37-ab925783b63b`) for the lock to install. You'll get it at a clean pause in st-foundation's work.
- Local mirror of theme (read; don't treat as remote truth): `C:\Users\SSTS\Desktop\Riya\theme-build\src` (pristine Horizon in `theme-build/pristine`, old desi layer in `theme-build/ref`). Upload method used so far: Admin GraphQL `themeFilesUpsert` + checksumMd5 readback (no Shopify CLI/Node on this machine). Log: `C:\Users\SSTS\Desktop\Riya\build-log-foundation.md`.

## Hero section files
- `sections/st-hero.liquid`: static Liquid first paint (first campaign complete, CSS only) + `<script type="application/json" data-st-hero-data>` + the section contract comment at the top (data attributes).
- Snippets: `st-sprite.liquid`, `st-nail.liquid`, `st-nail-crop.liquid`, `st-nail-sequence.liquid`, `st-campaign-colors.liquid`, `st-campaign-url.liquid`.
- `templates/index.json`: section `hero` (type st-hero), settings autoplay / default_tone / show_character, one `campaign` block per set in play order: on-me, brainwave, diet-cherry, green-flag, shaadi-shift, wild-card, pinky-promise.
- No motion JS exists yet. Suggested file: `assets/st-hero-motion.js`, a custom element that upgrades `[data-st-hero]`. Controls ship `aria-disabled="true"` until the controller attaches.

### DOM / data contract (from st-hero.liquid header)
- Root `[data-st-hero]`: data-active-key, data-active-index, data-next-key, data-tone, data-tone-count, data-autoplay. CSS vars on root: --st-scene, --st-scene-ink, --st-cta-bg, --st-cta-ink, --st-tone-swatch.
- Parts: [data-st-hero-note], [data-st-hero-headline], [data-st-hero-finger] > [data-st-hero-tone-sprite], [data-st-hero-main] (signature nail, cuticle = bottom edge), [data-st-hero-accent="1"|"2"], [data-st-hero-preview] with [data-st-hero-preview-nail="0..3"], [data-st-hero-character], [data-st-hero-cta], [data-st-hero-pause], [data-st-hero-tone], [data-st-hero-status] (polite live region).
- Data JSON per campaign: key, name, headline, note, index, colors{scene,ink,ctaBackground,ctaForeground}, url, ctaLabel, journalUrl, art{nails,character,previewHand,packaging}, crops, sequence, previewSequence; plus tones[], finger{}, previewHand{anchors}, atlases{}.

### IN PROGRESS at hand-off (st-foundation, defects H1–H4 sent 9 Oct)
- H1 the section still points at the OLD shared-Files atlases (desi-*.png, ≈9 MB, and a preview hand base WITH thumb). It's being switched to the accepted Phase 1 web assets below.
- H2 previewSequence is still the legacy 5-nail mapping; being replaced by `preview_slots` + `distinct_accents` from the manifest.
- H3 CTA label quotes → "Shop {name}" (copy register).
- H4 character atlas = labelled placeholder only, out of first-paint path (character art waits on owner Board 1).
Build against `artwork/manifest.json` as the source of truth, not against the current data block.

## Campaign metaobject
- Type `small_talk_campaign` (definition gid://shopify/MetaobjectDefinition/25563726037). Snapshot: `C:\Users\SSTS\Desktop\Riya\backup\theme-186649313493\campaign-metaobjects.json`.
- Keys used by the hero: handle (on-me, brainwave, diet-cherry, green-flag, shaadi-shift, wild-card, pinky-promise), name, headline, note, background, foreground, cta_background, cta_foreground, motion_index (0–6), product_handle, journal, package_url. Shared data; read-only. Wild Card cta_foreground #baff00 is unreadable → theme-local override (owner proposal SD6).

## Assets (local, accepted by orchestrator; final acceptance yours in the rendered hero)
- Root `C:\Users\SSTS\Desktop\Riya\artwork\`; single source of truth `manifest.json` (every path has a `web` derivative; theme ships web).
- Nails: `nails/web/<handle>.webp`, 612×354 = 3 cells 204×354 (col0 signature | col1 accent | col2 extra). Cuticle anchor (0.5, 0.925) per cell; one shared nail scale.
- Fingers: `fingers/web/tone-1..4.webp` (light→deep), 310×840, nail-bed anchor (0.5, 0.2649) identical in all four. Main nail at cell scale 0.76; tip overflows the canvas top ~70 px (overflow visible).
- Preview hand: `hand/web/preview-hand.webp` 511×639 (92 KB), four nails, thumb concealed (provisional pass: slight angle at the index join, faint thumb-shadow tone; replacement request on file). Slots in `hand/preview-hand.json`: index (0.1009,0.8172) −138.7° s0.2413 · middle (0.1605,0.9019) −137.8° s0.2336 · ring (0.3003,0.9071) −136.2° s0.2346 · little (0.5022,0.8720) −137.0° s0.2145; transform-origin 50% 92.5% on the cuticle.
- Display: hand 146 css px wide at a 390 px scene, scaled with scene width and clamped (tune with rendered evidence).
- `preview_slots` (index→little, keyed by set SHOWN): on-me [0,2,1,0] · brainwave [0,1,2,0] · diet-cherry [1,0,2,1] · green-flag [1,0,1,0] · shaadi-shift [2,1,0,2] · wild-card [1,2,0,1] · pinky-promise [0,0,0,0]. Each set's signature is visible in its preview → the flight source always exists.
- `distinct_accents`: green-flag cols 1≈2 (never fly 1↔2); pinky-promise is one design (no meaningful accent flight); shaadi-shift col0 vs col2 distinct only by the flower; all other pairs distinct.
- First-paint worst case ≈240 KB (set-1 nails + one tone + hand); budget 350 KB.
- Known minor: ≤1 px natural free edge past the ring-finger tip at 3×.

## Spec (locked by owner)
- ~2.6 s per set: 0–0.7 signature hold; 0.7–0.95 accent 1 flies from left sample; 0.95–1.4 hold; 1.4–1.65 accent 2 / signature return; 1.65–2.1 hold; 2.1–2.6 next signature flies from the upper-right hand + background cross-fade + commit. Three sets then settle (~8 s). Web Animations API, transform/opacity only, hero-local coordinates, static Liquid first paint, DesiMotion clock may be retained (ref: theme-build/ref).
- Interaction contract: brief §7 points 1–10 (finite autoplay, hold-to-pause incl. keyboard + blur, preview click / horizontal swipe without capturing vertical scroll, hidden/offscreen pause, reduced motion static, failed-image safety, resize/scroll cancel, editor lifecycle cleanup, no duplicate controllers).
- Strings: hero a11y labels come from copy register `C:\Users\SSTS\Desktop\Riya\copy\06-microcopy.md` MC-081…MC-093 (Pause, Hold to pause, Skin tone, Skin tone {n} of 4 …). Don't write new shopper-visible strings; ask the orchestrator if one is missing.
- Old motion code review findings M1–M10 are in the checklist (`Small-Talk-Claude-Implementation-Checklist.md`).
