# Small Talk — final acceptance view (Fable, 9 Oct 2026)

Scope: theme 186651934933 (unpublished) on the preview, built-in browser pane, viewport emulation only (320×568, 390×844,
430×932, 1180, 1280, 1440). No real devices. The pane reports the document as hidden while it is not displayed, so lazy images,
scroll-reveal, carousels and decode-gated work are throttled; anything that depends on that is marked unverified, not failed.
Frames: `qa/motion/` (hero), `qa/store/` (pages).

## Verdict (updated 9 Oct, after re-check)
Theme side accepted. The only remaining blockers are owner actions: payments (SD19) and the refund policy text (SD25).
The Journal defect and the desktop hero defect are fixed and verified on the preview (see "Re-check" below).

## Re-check after fixes (preview, 9 Oct)
- **Journal J1: PASS.** Slide text and nail art no longer overlap: a geometry check of all beat containers on On Me and
  Shaadi Shift (the longest beat) at 390 found 0 overlaps. Nails sit in their own row under the text on phones and in a
  reserved column at 1280. No horizontal scroll at 320. Standfirst sits above the carousel.
  `qa/store/j1-390-on-me-slide1-clean`, `j1-390-shaadi-shift-slide1-clean`, `j1-320-brainwave`, `j1-1280-on-me-reserved-column`.
- **Hero v2.3: PASS.** At 1280 the copy and CTA start at 230 px, clear of the Wild Card character (right edge 167 px);
  Diet Cherry and On Me are clear too, and Brainwave keeps its top-anchored layout. Phones unchanged at 390.
  `qa/motion/v23-preview-1280-*`, `v23-preview-390-wild-card-unchanged`.
- **SEO:** the Help description now promises delivery and contact only, and the talks description promises no submission
  path. Both are live in the rendered head. `/pages/nail-guide-desi` still renders without noindex at the time of the
  re-check (orchestrator: interim noindex in progress). Accepted as interim, because the guide has no sizing facts yet. It
  must become indexable again as the single guide route once G2–G4 content lands.
- Remaining polish (footer heading levels, PDP thumbnail state, empty paginated page, Organization logo) is in progress at
  st-foundation and was not re-checked.

## Blockers as first reported (items 3 and the hero defect are now fixed)
1. **Payments (owner, SD19).** Checkout opens and shows contact and delivery for ₹1,198 (2 × On Me), but no payment
   provider is configured (orchestrator's earlier walk-through; payment step not re-entered here). Nobody can buy.
2. **Refund policy shows the shipping policy (owner, SD25).** `/policies/refund-policy` has the title "Refund policy" and the
   shipping policy body. It is linked from Shopify checkout and indexable. Help correctly hides Returns meanwhile.
3. **Journal story slide 1 is unreadable at 390 (st-foundation).** On `/blogs/journal/on-me` the large story text runs under the
   burgundy nail art ("Every good dinner has t… moment at … end. The pl…"). Same layout on every article. Text must never sit
   under the art (stack art below text on phones, or reserve the art column). `qa/store/390-journal-on-me-slide1-text-under-nail`.

## Hero (my files)
- **v2.2 on the preview: PASS** on everything I re-checked. Green Flag character right-hand at 320/390/430 and bottom-right at
  1280. Diet Cherry and Wild Card samples sit right of the finger. Brainwave and Pinky Promise headlines sit below the hand and
  end above the main nail (320 and 390). Tones 2→3→4→1→2 swap the finger image with identical nail geometry. Pause label at
  load reads Pause. One script, new `?v=`.
- **New desktop defect found and fixed as v2.3:** at 1280 the Wild Card and Diet Cherry characters covered the first letters of
  the headline, and left-anchored characters sat under the CTA (`qa/motion/v22-preview-1280-wild-card-headline-under-character`).
  CSS-only fix, verified in the lab at 1180/1280/1440, phones unchanged (`qa/motion/v23-lab-*`).
  - `motion/st-hero.css` MD5 8fe58c142699e355b1e2c7ea9aeb8054 (byte-identical copy needed)
  - `motion/st-hero-motion.js` unchanged, 3c379254a4e445cb2fca65565493ddff
  - `motion/CONTRACT.md` v2.3 MD5 622a66aae0504bac7e6f1c37b7c50907
- Contract points 8 (offscreen, reduced motion) and 10 (theme-editor lifecycle) remain verified by code only.

## SEO implementation (preview, rendered HTML)
PASS:
- `/collections/all` title "Shop Press-On Nail Sets | Small Talk" + register meta; pagination appends "– Page 2".
- 404: "Page not found | Small Talk", `noindex, follow`.
- `noindex, follow` on cart, search, `/collections`, empty collections (frontpage, press-on-nails), `/blogs/news`,
  `/pages/our-world`, old `/pages/nail-guide`, `/pages/contact`, filtered collection URLs. Tagged URLs 301.
- PDP: exactly one Product with `@id`, spaced description, offer price/currency/InStock matching the buy box (₹599 On Me,
  ₹699 Wild Card), no rating/review; BreadcrumbList Small Talk › Shop › {Set}.
- Article: Article with Organization author and publisher, published/modified dates, image, mainEntityOfPage, excerpt
  description; BreadcrumbList Small Talk › Journal › {title}.
- Shared fields as written: product titles/metas match the register (e.g. "On Me Burgundy Press-On Nails"), Journal
  "Journal — Stories Behind the Sets", article metas, Our Story, packaging alts with "illustrated front … in the tray".
- S4 cart H1: agree to accept. The live DOM has one H1; the second sits in an inert `<template>`.

Required changes:
1. **Help meta promises returns information** that the page hides ("Find delivery and returns information…"). Change the
   shared Help description to delivery + contact only until SD25 is fixed (st-copy words, orchestrator writes).
2. **the talks meta promises a submission path that does not exist** ("Send a little of your world… Submissions go privately
   to our team for review"). The page has no form (G10). Use a gate-free description with no submit promise.
3. **Home title/meta still say "Almond", "Indian moments", "original illustrated packaging"** (owner step in Preferences,
   G14). The same text falls through to `/collections` and `/search` (both noindex, so low).
Low: `nail-guide-desi` has no SEO description (auto-excerpt "Start with your own nails Look…", missing break; gated SEO-026);
Organization has no logo (theme logo setting empty); `/collections/all?page=2` is an empty but indexable page.

## Functional and accessibility (observed)
- Shop: 7 cards, prices, links to PDPs. PDP: Add to bag works ("Added to bag." announced, bag 2→3). Cart: quantity
  decrease 3→2 updates line and subtotal (₹1,797 → ₹1,198), Help and Contact links (Contact → `/pages/help#contact`),
  Checkout reaches Shopify checkout. Search: results for "green" (4), no-results state with suggestions, H1 present.
- Help: Delivery topic with shipping facts + policy link; contact form fields all labelled, required marked. Not submitted
  (would email the owner).
- the talks: examples labelled "Example conversation", aliases without handles, no fabricated activity, no form (gated).
- 404 page with Shop/Home actions. Our Story text only, no images.
- Static sweep of 29 routes: every `<img>` has an alt attribute, no unnamed buttons in the live DOM, inputs labelled.
  Site-wide heading jump h2→h4 in the footer (low).
- PDP thumbnails have names via image alt but no selected state (`aria-current`/`aria-pressed`) (low).
- Menu drawer: real labelled button, focusable. Focus did not move into the drawer and a synthetic Escape did not close it,
  but the frame was caught mid-slide in the hidden pane. Unverified; needs a visible-tab or device check.

## Visual (against boards, phone first)
- Hero matches board 2 composition per set (character placement, four-nail preview hand, campaign CTA colours).
- Landing order matches board 3. Chapters, talks teaser, Journal teaser, FAQ and footer render at 390 and 1280.
- Known owner-accepted deviations stay as recorded (SD17/SD18): same woman in all characters, Diet Coke mark on the Diet
  Cherry box, chapter scene gaps. Money shows "Rs. 599.00" instead of "₹599" (SD20, owner setting; checkout shows ₹).
- Not verified: home sections below the fold at 1280 rendered blank in one pass and correctly in another (pane throttling
  of reveal/lazy content); Journal index images lazy-loaded only when the pane was visible.

## Performance (honest)
Preview, theme 186651934933, 9 Oct, pane at 1280 (hidden), first view of `/`: encoded transfer about 421 KB images, 384 KB
JS, 96 KB CSS, 215 KB fonts; navigation TTFB 310 ms, DOMContentLoaded 1.03 s, load 1.08 s at 390. These are single in-pane
readings, not Lighthouse and not field data. No Core Web Vitals claim. Fonts are the largest avoidable cost (subsetting not
done, checklist 0.4).

## Not tested
Real devices and orientation change, reduced-motion emulation, offscreen pause, theme-editor lifecycle, failed-image path,
payment and order emails, contact form submission, keyboard-only walk through the whole site.

---

# Phase 2: board fidelity (390 px is the bar) — acceptance view, 9 Oct 2026 (Fable)

Every screen was compared side by side with its board frame at 390 and checked at 320 (plus 375/430/1280 where layout
changed), on the live preview of theme 186651934933 using browser-pane emulation (not real devices). Reports are in
`qa/fidelity/`.

## Screens accepted
| Screen | Board | Report | Status |
|---|---|---|---|
| Header | 2/3 | LANDING-PREVIEW-1 | accepted |
| Hero (motion v3.3) | 2 | HERO-V3, LANDING-PREVIEW-2 | accepted. All 7 states, tones, flights, first-tap fix and bare-nail hand-over verified on the preview. |
| Landing (13 sections) | 3 | LANDING-PREVIEW-1/2 | accepted; Green Flag and On Me chapters pass on stand-in art |
| Shop | 5 f1 | SHOP-PREVIEW-1/2 | accepted |
| Product page | 5 f2 | PDP-PREVIEW-1/2 | accepted (including 320/375 buy row) |
| Bag | 5 f3 | BAG-PREVIEW-1 | accepted |
| Journal index | 4 f3 | JOURNAL-PREVIEW-1 | accepted (including 320) |
| Journal story | 4 f4 | STORY-PREVIEW-1 | accepted |
| Our Story | 4 f5 | OURSTORY-PREVIEW-1 | accepted |
| Help | 4 f6 | HELP-PREVIEW-1 | accepted (Returns row hidden until SD25) |
| Nail Guide | 5 f5 | GUIDE-PREVIEW-1 | accepted with 2 small items below |
| the talks (hub + thread) | 4 f1–2 | TALKS-PREVIEW-1 | accepted (reply list to re-check once a real reply exists) |
| Checkout | 5 f4 | — | Shopify-hosted; reference only, not themeable |

## Open items (theme / copy; none block launch on their own)
1. **404 page uses the retired blue/plum chrome** (new). Restyle to burgundy H1 and pills. (st-foundation)
2. **Footer at 320 (shop / PDP / bag / guide variant):** the wrapped link row starts with an orphan "·". Fix with `li + li::before`
   and no-wrap items. (st-foundation)
3. **Nail Guide step 01 copy:** "Use a paper strip … like this", but the approved art shows a tape measure. Change the wording.
   (st-copy)
4. **Stand-in art to re-check when the ChatGPT originals arrive:** hero characters (soft at 2× density), Green Flag and On Me
   chapter scenes, Journal story heroes, PDP and bag character peeks, Nail Guide steps 02/03 (no art at all).
5. **Help Returns row** returns in board position 2 once SD25 is fixed; re-check then.
6. **the talks reply list** layout to re-check when the first real reply exists.

## Owner blockers (re-checked live on the preview at the time of writing)
1. **Payments (SD19):** checkout cannot take payment (last verified at the payment step earlier today; not re-entered).
2. **Refund policy text (SD25):** `/policies/refund-policy` still shows the shipping policy body under the "Refund policy"
   title. The Returns topic and footer link stay hidden until it's fixed.
3. **Home title and meta (SD4):** still "Small Talk | Almond Press-On Nails. A Lot Said." / "Seven almond press-on nail
   designs … original illustrated packaging". G14 wording is in the shared Online Store preferences; owner step.
4. **Money format (SD20):** prices still show "Rs. 599" instead of the boards' "₹599" (Settings → General, owner).
5. **Terms of service (G16/F15):** `/policies/terms-of-service` is 404; the draft is in `copy/terms-of-service-draft.md`
   for the owner to paste. The footer Terms link stays hidden until then.

## Verdict
Phase 2 fidelity: **all screens accepted against the boards at 390**, with six small open items listed above. The store is
not ready to take real orders until the owner clears payments (SD19) and the refund text (SD25). SD4, SD20 and Terms
should be done before launch for honesty and polish.

## Phase 2 last re-check (Fable, 9 Oct 2026)
Checked live on the preview of theme 186651934933 with browser-pane emulation at 320, 375 and 390. Open items 1–3 above
are now closed, and one new shop fix is verified.

| Item | Result | Evidence |
|---|---|---|
| 1. 404 restyle | PASS | "This page wandered off." is Source Serif 4 900 burgundy (gradient text from #8a0619), 56 px at 390 and 46 px at 320, 2 lines. Body #6e7184 DM Sans. "Shop all sets" is a filled #920324 pill with white text; "Go home" is an outline pill. Both are Barlow Semi Condensed 600 22 px, 300 × 52 px, linking to /collections/all and /. No blue, ink or plum left. `noindex, follow`. scrollWidth 320 and 390. Matches sheets `qa/fidelity/404-390.png` and `404-320.png`. |
| 2. Footer separators at 320 | PASS | Shop, PDP, bag and Nail Guide all render "Shop · Our Story · the talks · Journal ·" then "Nail Guide" on line 2. Each item is `nowrap` with the dot in `::after` (none on the last item, no `::before`). No line starts with "·". The legal row "Contact us · Shipping policy · Privacy policy" fits one line. |
| 3. Shop 320 overflow | PASS | scrollWidth equals the viewport at 320, 375 and 390, with no element past the right edge. At 320 "On Me Rs. 599" stays on one row and "Brainwave" wraps its price below. At 375 and 390 every name and price share one row. The note sits at x 53–286 at 320 and at x 84–317 at 375/390 (board position unchanged). |
| 4. Nail Guide step 01 copy | PASS | It now reads "Use a paper strip or a soft tape measure to find the widest part of your natural nail." List step 1 says "a strip of paper or a soft tape measure". "like this" is gone. Copy and tape-measure art agree, matching FACTS F3. |

Open items 1, 2 and 3 are closed. Items 4–6 (stand-in art, Help Returns row, talks reply list) stay as re-checks for
later. The owner blockers are unchanged.

**Phase 2 (board fidelity) is closed.** Every screen is accepted at 390, and 320, 375 and 1280 remain usable.

## Owner overrides of the boards (logged 10 Oct 2026)
- **Header logo left-aligned** (owner instruction, relayed by the orchestrator).
  - Phones: directly after the menu button, at x ≈ 56 at 390 (scaled at 320). Desktop: left, before the nav.
  - Boards and spec/hero.md had it centred at x 95–179.
  - Acceptance judges only spacing, vertical alignment and the 44 px targets, not the board position.
  - The official logo image replaces the live-text wordmark (header, drawer, footers), with the link name kept as
    "Small Talk home".
  - Dependency: the hero height uses `--st-header-h` (69 px). The header must stay 69 px tall, or the variable must
    change with it.
- **Landing redesign, owner (10 Oct):**
  - Campaign body at 50% on all chapters and the hero (hero v3.7.3).
  - Product name in curly quotes as the focal point, with a soft set-hue highlight.
  - One screen per chapter at 100svh.
  - Board positions and sizes for these elements no longer apply. Decisions and constraints:
    `qa/fidelity/OWNER-LANDING-CHANGE-1.md`.
