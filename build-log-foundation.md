# Build log — Small Talk foundation (theme 186651934933)

Writer: foundation session (theme-write lock holder). Reports to st-orchestrator.
Only theme written: 186651934933 "Small Talk — Claude build (Horizon)", UNPUBLISHED, Horizon 4.1.5.

## Tooling
- No Shopify CLI / Node on this machine. Theme files are read and written via Admin GraphQL
  (`theme.files`, `themeFilesUpsert`). Large reads persist to disk and are unpacked into a local mirror:
  `theme-build/src` (working copy), `theme-build/pristine` (stock Horizon as duplicated), `theme-build/ref`
  (read-only copy of the desi layer from 186649313493).
- Every upload is checked by comparing remote `checksumMd5` with the local file.
- Screenshots + overflow checks: `theme-build/tools/qa.py` (Playwright driving the installed Chrome) →
  `qa/foundation/`.
- Theme Check: not available locally (needs Shopify CLI or Node). Shopify's server-side Liquid/JSON validation
  runs on every upsert and rejected two attempts (logged below). See open issues.

## 1. Theme settings — verified 9 Oct
What changed
- `config/settings_data.json`: colour palette = ivory #FFFDF5 (background), body #272332 (foreground),
  ink #1F1A2E (color1), divider #D8CFDA (color2), blue #1013B3 (color3), plum #4A243D (color4),
  secondary #68616E (color5), tint #EEE8F5 (color6). Primary button blue/ivory; secondary button outline blue;
  selected variant blue; inputs white with divider border; drawers/popovers ivory; badges tint/ink.
  page_width normal; cart_type page; quick add off; currency codes off; card hover off.
  Font pickers set to the system font `helvetica_n4` so Horizon downloads no library fonts
  (`sans-serif_n4`, `serif_n4`, `georgia_n4` were rejected by Shopify as invalid handles).
- Fonts copied into the theme (byte-identical; MD5 matches reference theme): st-font-1, st-font-3, st-font-4,
  desi-pen, desi-display-black, desi-condensed (.woff2).
- `snippets/st-brand-styles.liquid` (new): @font-face for ST Display (DM Serif Display), ST Sans (DM Sans),
  ST Pen (Kalam Light), ST Condensed (Barlow Condensed 600/700); `--st-*` tokens read from the palette;
  maps Horizon's `--font-body/subheading/heading/accent--family` and button font onto the brand voices;
  heading colour token (`--st-heading-color`, ink by default, plum under `.st-editorial`); focus ring;
  reduced-motion guard; shared utilities `.st-pen`, `.st-display`, `.st-cta`, `.st-link`.
- `layout/theme.liquid`: renders `st-seo` after `meta-tags`, `st-brand-styles` after `color-palette`;
  preloads only the display font (st-font-4) on the home page.
Verified how
- Preview at 390/1280: body ST Sans, headings ST Display in ink, ground ivory, `--st-blue` = #1013B3,
  no horizontal overflow, no Liquid errors. Shots: qa/foundation/01-settings-390.png, -1280.png.

Licences (fonts): all six are SIL Open Font License per their name tables — Barlow Condensed (Barlow Project),
DM Sans, DM Serif Display, Kalam (Indian Type Foundry), Bodoni Moda (desi-display-black, copied but unused).
No licence doubt.

## 2. Header + footer — verified 9 Oct
What changed
- `sections/st-header.liquid` (new): menu button → drawer (Horizon `dialog-component` + native modal `<dialog>`),
  stacked blue logo (text from shop name in ST Display; uses `settings.logo` image if one is set), desktop nav
  (≥990px) from the `desi-main` menu (Shop / Our Story / Journal / Nail Guide / Help), "the talks" in ST Pen,
  bag link reusing Horizon `cart-icon` + `cart-bubble` (live count on add to cart, blue bubble). Sticky via the
  same group-flattening pattern Horizon's header uses.
- `assets/st-header.js` (new, 40 lines): `st-focus-trap` wraps Tab/Shift+Tab inside the drawer (headless Chrome let
  focus reach "Skip to content" without it).
- `sections/st-footer.liquid` (new): stacked logo, tagline (setting), menu (`desi-main`), social icons only for URLs
  entered in section settings (dashed placeholders in the theme editor only — no fake links), policy links from
  `shop.policies` + Contact → /pages/help, © year shop name.
- `sections/header-group.json` / `footer-group.json`: replaced Horizon's announcement bar + header and footer with
  the two st-* sections.
- `locales/en.default.json`: added a `small_talk` namespace with all new interface strings (header, footer, hero,
  chapter, product, cart, journal, talks, shop). Schema labels in st-* sections are literal English (adding `t:` keys
  would mean re-uploading the 52 KB schema locale; noted for Theme Check).
Verified how
- 320/390/430: menu button visible, drawer opens, Tab cycles Close → 5 links → the talks → Search → Your bag → wraps,
  Escape closes and focus returns to the menu button. 1280: inline nav, no menu button. No overflow at any width.
  Shots: 02-header-{320,390,430,1280}.png, 02-drawer-{320,390,430}.png, 02-footer-{390,1280}.png.
- Only the privacy policy is published in the shop, so it is the only policy link (shipping/returns appear
  automatically once SD3 policies exist).

## 3. Hero `st-hero` — verified 9 Oct
What changed
- `sections/st-hero.liquid` (new): campaign blocks (metaobject picker, optional per-set preview-hand image).
  First campaign rendered statically, CSS only: scene colour, handwritten note, H1 headline, finger (default tone 2),
  signature nail registered on the cuticle, accent + extra nails, next set's preview hand top-right with its four nails,
  pause + tone buttons (aria-disabled until the motion controller attaches), CTA "Shop “Set” ↗", polite live region,
  hidden list of all sets (carries block.shopify_attributes), JSON data block with all seven campaigns.
- `snippets/st-sprite.liquid` (new): atlas cell → real <img> with width/height/srcset/sizes in an overflow box
  (replaces CSS background sprites). `st-nail-crop` (geometry table, single source of truth), `st-nail`
  (campaign + role → sprite), `st-nail-sequence` (5-nail roles per set; preview uses the last four),
  `st-campaign-url` (product URL, else /products/<handle>; no review-mode rewriting), `st-campaign-colors`
  (scene/CTA colours + contrast guard: Wild Card's #baff00 CTA text on #fffaf0 falls back to its ink #09195d).
- Geometry measured from the PNG alpha channels: finger tiles at x 111/512/905/1301 (w 280, y 108–940), natural
  cuticle 25.7% down the crop; nail crops end exactly at the cuticle; preview-hand fingertip anchors + angles.
- Placeholder art read from Shopify Files via `images['…']` (desi-finger-tones, desi-nail-accents-v2,
  desi-preview-hand-base) and from the metaobject (nail_art, character_art). Character crops are feathered with a
  CSS mask (no clip-path). Only the signature nail image has fetchpriority=high; finger/accents eager; the rest lazy.
Verified how
- 320/390/430/1280 screenshots (03-hero-*.png): nail sits on the finger, preview nails on the fingertips, CTA and
  controls clear of art, no overflow, no Liquid errors. JSON parsed in the browser: 7 campaigns with colours, URLs,
  art URLs, crops, sequences.

## 4. Landing template — verified 9 Oct
What changed
- `templates/index.json`: hero → gallery → Diet Cherry → the talks teaser → Brainwave → Green Flag → Journal teaser →
  Nail Guide teaser → Shaadi Shift → On Me → Wild Card → Pinky Promise → Shop all + FAQ (footer from the group).
  Captions, FAQ answers and the labelled talks example are the existing content from the previous build.
- `sections/st-chapter.liquid`: campaign, caption, story-link label, art override, thread side. Layout: body (caption,
  headline, five nails) over a two-column foot (illustration on the thread side | name + Shop set + story link).
  min-height 70svh on phones. The dashed thread SVG is drawn only in the top 3.25rem bridge zone and the side gutter;
  text/nails/buttons keep 2.5rem (4rem desktop) clear of it.
- `sections/st-gallery.liquid`, `st-teaser.liquid` (talks/journal/guide, plum editorial headings, example always
  labelled "Example conversation"), `st-faq.liquid` (native <details>).
Verified how
- Full-page shots 04-landing-{320,390,430,1280}.png. Every chapter measures 70% of the viewport at 320/390/430;
  ~63–68% at 1280 (34rem min). No overflow at any width.
- "Read the story" links are wired to each campaign's `journal` reference but do not render: all 7 Journal articles
  are unpublished (shared data).

## 5. Shop, product, cart, Journal, pages — built; verified where storefront data exists (9 Oct)
What changed
- Collection: `sections/st-shop.liquid` + `snippets/st-product-card.liquid`; `templates/collection.json`.
  Heading + handwritten note, filter pills only from real data (storefront filters with results, else listed tags
  that exist), 2/3/4-column grid, pagination, honest empty state ("No sets to show yet…" + Find your fit). Cards:
  product media or approved packaging, Horizon `price` snippet, sold-out badge, "View set →".
- Product: `templates/product.json` and identical `product.desi.json` (campaign products use suffix `desi`).
  Horizon `product-information` kept: carousel gallery with thumbnail buttons + arrows + zoom, title/price row,
  variant picker, buy-buttons (quantity + add to cart + accelerated checkout; Horizon product form and cart events
  untouched). New `blocks/st-product-notes.liquid` (intro: campaign short description + "Find your fit →";
  details: Delivery & returns / Need a hand? links, disclosures What's in the kit, Fit & application, The story from
  the campaign metaobject with Journal link). `assets/st-product.js` adds ArrowLeft/Right to the gallery.
- Label logic, minimal edits inside Horizon owners: `blocks/add-to-cart.liquid` → "Add to bag · ₹price"; "Coming
  soon" (disabled) when the variant price is 0; sold-out text stays Horizon's "Sold out".
  `blocks/accelerated-checkout.liquid` hidden at price 0. `snippets/price.liquid` prints "Coming soon" instead of ₹0.
- Cart: `templates/cart.json` (Horizon main-cart): title "Your bag" with count, square thumbnails, tint summary panel;
  quantity bounds/remove/totals/empty state are Horizon's. Empty line now "Your bag is empty" (locale).
- Journal: `sections/st-journal.liquid` (`blog.json`, `blog.desi.json`) and `sections/st-article.liquid`
  (`article.json`, `article.desi.json`) + `assets/st-beats.js`. Story beats come from each article's existing
  `di-story-slide` sections (4 per article) → scroll-snap carousel, per-slide "n / N", prev/next + arrow keys, polite
  status; then the rest of the body, Shop CTA, three more stories.
- Pages: `sections/st-page.liquid` + theme blocks `st-packaging`, `st-help-topics`, `st-talk-examples`,
  `st-talk-example`, `st-talk-form`, `st-buttons` (Help/Contact reuse Horizon's `contact-form` block). Templates:
  page.json, page.desi.json (generic), page.our-story.json, page.nail-guide.json, page.help.json = page.desi-help.json,
  page.the-talks.json = page.desi-talks.json, page.contact.json. The talks: three labelled example conversations
  (from the previous build) + "written examples, not real posts" note, private "Start a talk" form (alias, email,
  topic, title, text, consent; native contact form; no counts or replies); community rules come from page content.
Verified how
- 320/390/430/1280 (05-*.png, 07-*.png): shop empty state, bag empty state, Journal empty state, Our Story (desi and
  our-story templates; packaging strip with alt text), contact, search, 404 — no overflow, no Liquid errors, no
  translation-missing strings, no console errors from theme code.
- Help, the talks and nail-guide templates verified on published pages via ?view=help / the-talks / nail-guide,
  because those pages are unpublished.
- NOT verifiable yet: PDP (gallery, Add to bag / Coming soon / Sold out, disclosures), add-to-bag and bag line items,
  Journal cards and story carousel — there is no active product and no published article.

## 6. SEO plumbing — verified 9 Oct
- `snippets/st-seo.liquid`: noindex,follow on cart/search; Organization JSON-LD (home); Product + Offer JSON-LD from
  live variant data (offers only for variants priced > 0, no reviews); BreadcrumbList on product, collection, blog,
  article, page. Titles/descriptions/canonical stay native (`meta-tags`).
- Checked in preview: home (Organization), /collections/all, /pages/our-story, /blogs/journal, /pages/contact
  (BreadcrumbList), /cart and /search (noindex). All JSON-LD parses. Product JSON-LD unverified (no active product).

## 7. Checks — 9 Oct
- Theme Check: not available on this machine (no Shopify CLI, no Node). Substitutes: Shopify's server-side validation
  on every upsert (caught 3 errors during the build, all fixed) and a local lint over all st-* files and the edited
  Horizon files: every `t` key exists, every rendered snippet exists, every `<img>` has width/height/alt, every
  image_tag has alt, schema JSON valid, one stylesheet tag per file, every template section/block type exists — clean.
  Next maintainer step: `shopify theme pull --theme 186651934933` then `shopify theme check`.
- Overflow: none at 320/390/430 (and 1280) on landing, shop, bag, Journal, Our Story, nail guide, help, talks,
  contact, search, 404.
- Keyboard: landing tab order header → hero CTA → gallery → chapter/teaser CTAs → FAQ → footer; every stop shows the
  2px blue focus ring. Drawer: focus contained, Escape closes, focus returns to the menu button.
- Reduced motion (emulated): drawer animation 0.01ms; beats carousel scrolls without smoothing; global guard in
  st-brand-styles.
- Every uploaded file: remote checksumMd5 equals the local mirror (templates are stored compact remotely).
- Hero data contract for the motion session: side-session-notes folder → hero-data-contract.md.

## 8. Motion controller install (motion/CONTRACT.md v2) — verified 9 Oct
- Uploaded byte-identical (remote checksumMd5 = local): assets/st-hero-motion.js (cd0a9328), st-hero.css (ddc8cf99),
  st-nails-{on-me,brainwave,diet-cherry,green-flag,shaadi-shift,wild-card,pinky-promise}.webp, st-tone-1..4.webp,
  st-preview-hand.webp. Masters not uploaded.
- snippets/st-motion-map.liquid (sprite, preview_slots, flight_columns per set key); snippets/st-nail.liquid renders
  `.st-nail` cells with `--st-nails` / `--col`; no transforms on nail ancestors.
- sections/st-hero.liquid rewritten to the contract v2 DOM + JSON v2; JS loaded once (defer), first sprite + default
  tone + hand preloaded, finger image fetchpriority high. Labels MC-080…MC-091 from locale. CTA `hidden` unless the
  set's product is live (G5); JSON exposes `live`.
- Character art is a marked PLACEHOLDER (old atlas crop) until st-artwork's character group is accepted.
- Static paint checked at 390 with st-hero-motion.js blocked (tools/tmp/nojs.py).
- Fix during install: Liquid `'{name}'` inside `{{ }}` breaks parsing; labels are assigned inside `{%- liquid -%}`.

## 9. Copy batch B1 (landing) — 9 Oct
- Every `small_talk.*` locale value now equals a register string (checked by script against the “final” column of
  copy/0*.md; plural forms map to MC-006 / MC-028). Key → ID map: theme-build/copy-map.json (`locale`, `settings`).
- Landing (templates/index.json) installed: LND-010, 011, 014–023, 025–029, 031 (interim wording “See the talks” from
  the row's note), 032, 033, 036–041, 043, 044, 045, 052, 053, 056, 057 (last sentence dropped: G12 not met), 058,
  059; LND-009 via locale; LND-061 via locale template (icons render only when an account URL is entered, D5).
- Hidden / not installed (gated): LND-013 (G11/G12), “Start a talk” (G10), LND-042 guide CTA (G2), FAQ Q1–Q3
  LND-046…051 (G1–G4), Q5 LND-054/055 (G11), LND-060 footer links (shared menu), LND-062 copyright (G16).
- Pending final art (alt text waits for the accepted art): LND-012, LND-034, LND-035, SEO-041.
- Removed previous-build strings with no register row: footer contact link, copyright line, shop tag pills (D1),
  journal empty-state line, talks example note on the landing, talk-form consent line, chapter story-link labels;
  schema defaults (gallery, FAQ, teaser) now use register strings.
- Section/block changes: st-chapter (caption_2, cta_label; CTA only while live), st-teaser (example_label,
  image_alt; example renders only with its label), st-talk-form (hidden slot until “G10 confirmed” + gated labels),
  st-product-notes (gated links removed), st-article (JRN-011 CTA only while live), st-header/footer/shop/journal.
- Talks page: “Start a talk” button (PG-066, G10) removed because it pointed at the hidden form; examples stay for B3.

## 10. Copy batch B2 (PDP + purchase states) — 9 Oct
- D7 story override: snippets/st-story-override.liquid, keyed by product handle, PDP-024/029/034/039/044/049/054 copied
  verbatim from copy/01-pdp.md by script. st-product-notes uses it first and falls back to the metaobject `story`
  (the metaobject is untouched). Heading PDP-001 “The story: {headline}” pulls the headline from the metaobject.
- Kit (PDP-002) and Fit & application (PDP-004) disclosures need an explicit gate checkbox (G1 / G2–G4) AND content;
  both stay hidden today. PDP-007 (G2) and PDP-008 (G6/G7) links stay hidden; PDP-009 “Need a hand?” → /pages/help.
- Add-to-cart: “Add to bag · {selected variant price}” (PDP-011) only for an available, priced variant; “Coming soon”
  (PDP-012) when the price is 0 or the variant can't be bought for a reason other than stock; “Sold out” (PDP-013).
  Horizon's “Unavailable” no longer shows on the PDP button. Sticky add-to-cart bar is off (its Horizon “Add to cart”
  string never renders). PDP-014…017 are the Horizon locale values.
- Uploaded st-story-override, st-product-notes, add-to-cart: remote checksumMd5 = local. Render check blocked: all
  seven campaign products are DRAFT, so no PDP exists on the storefront for this theme.

## 11. Copy batch B3 + board pages (talks, Our Story, Help, Nail Guide, Journal, shop, bag, 404) — 9 Oct
- New theme blocks: st-gate (gated group: children render only once its gate is confirmed; editor shows them in a
  dashed frame), st-note (handwritten / small heading / body), st-features, st-rules (rule 4 held for D3), st-step,
  st-questions + st-question (heading only when a question is visible), st-help-form (whole form held until G8 and a
  success message exist). New section st-bag-extras (help card held until a link is real; MC-026 promo with nail row).
  New asset st-forms.js (register validation messages MC-059…066 and “Sending…”, used by the help and talk forms).
- st-page: theme-local heading + intro settings (PG-001/014/033/062 “theme-local render”); page bodies are off on
  the rebuilt pages (`show_content` false) because the live bodies are shared and duplicate or contradict the board;
  body rows PG-002…005 / PG-016… are owner proposals.
- the talks: PG-062…064, examples PG-069…080 (aliases without @), closing PG-082, rules PG-098…101 shown;
  PG-065/066 in G10 gates, form G10 (PG-083/091/095 prefilled), PG-102 held (D3), PG-103 empty. Filter chips removed (D2).
- Our Story: PG-001, PG-006…012; packaging strip decorative until SEO-053 (G11); invented per-box alt removed; srcset
  no longer claims 700w for ~360 px packaging.
- Help: PG-033; topics PG-036…046 each gated (all held); help form PG-048 + PG-050…058/060 held behind G8.
- Nail Guide: PG-014/015; steps PG-017/021/023/024/026 + alts PG-032 in G2/G3/G4 gates; quick answers PG-027/028/031
  held. Today the page shows only its heading and note.
- Journal: JRN-003; JRN-002 interim “Small stories behind the sets.” (G12); “04 /” eyebrow removed; tag eyebrows
  removed (JRN-008, D6); JRN-012 “Next story: {name}” in metaobject order.
- Shop: MC-015, MC-016 interim “Different sets. Different moods.” (G12). Bag: MC-030 on the empty button, MC-026 promo;
  Horizon tax/shipping line hidden (MC-040, G15); MC-037/039/054/072/073/075/077/078 via Horizon locale keys.
- 404: rebuilt as st-page with MC-068…071.
- Uploads: every file's remote checksumMd5 equals the local mirror (st-gate first failed silently because
  `content_for 'blocks'` appeared twice; rewritten with one call and re-sent as TEXT).

## 12. Live-data verification (products + articles went live 09:24) — 9 Oct
- Shared data changed outside this session: all 7 campaign products ACTIVE (₹499–699, 10 each, Rs. {{amount}}
  money format) and all 7 Journal articles published. G5 now evaluates true from live data, so hero/chapter/Journal
  “Shop …” CTAs and “Add to bag · price” render; PDP, bag and stories were tested for the first time.
- Fixes from that test (all uploaded, remote checksum = local):
  - Add-to-cart showed “Add to bag · {{ price }} · Rs. 599.00” → price passed to MC-048's placeholder.
  - Add confirmation read Horizon's “Added” → `actions.added` = PDP-016 “Added to bag.”.
  - Bag title count bubble → MC-028 “1 item” (blocks/_cart-title); bag quantity buttons → MC-032/033/034 with the
    product name (snippets/quantity-selector, bag context only); empty-bag button → MC-030.
  - PDP gallery to board 5: 1/1.25 frame, contain + padding on the set's colour (no stretching of ~360 px packaging),
    zoom off; story disclosure open; dynamic checkout button switched off via a new buy-buttons setting.
  - Shop: only product-tag filters render (Shopify's “In stock” availability filter label is not a register string);
    cards stack name/price; card image alt is the media's own alt or decorative; srcset capped at the source width.
  - Journal: “Next story” matched metaobjects by `.id` (nil in Liquid) → matched by handle in register order;
    JRN-011 CTA is brand blue (outside the scene). Chapter “Read the story ↗” arrow no longer wraps alone.
- Verified: 7 PDPs (button, story override PDP-024…054 exact, links), add → “Added to bag.”, bag (“Your bag 1 item”,
  “Remove On Me from bag”, Subtotal, Checkout, promo, no tax line), test cart cleared; landing CTAs; Journal index
  (7 cards, Featured) and 3 stories (1/4 beats, Shop {set}, Next story wraps Pinky Promise → On Me). No overflow,
  Liquid or console errors at 320/390/430/1280. Screenshots qa/foundation/b2/.

- Search: results heading MC-074 “Results for “{terms}”” is now the page h1 (was a Horizon h3 “Search results”);
  clear button MC-076; placeholder MC-072; empty state MC-075. Verified with “lilac” and a no-result query.

## 13. C1–C5, hero CONTRACT v2.1, Phase 2 art, packaging panels, policy-body rule — 9 Oct (afternoon)
- C2: Horizon's product `structured_data` removed (one Product+Offer from st-seo). C3: Checkout verified as button
  "Checkout", Tab-reachable. C4: initial/re-rendered bag totals identical. C5: hero CTA fits at 320/390, follows the set.
- Hero v2.1: Fable's st-hero-motion.js (d239f830) + st-hero.css (e24faf77) byte-identical; st-character-<key>.webp ×7;
  static set-1 character DOM; [data-st-hero-main-desc] + aria-describedby (SEO-041); JSON live/altText/character;
  atlas removed. Non-hero nails/art are lazy <img> (fetchpriority low), no CSS background-image outside the hero.
- Phase 2 art (accepted groups only): chapters → st-chapter-<key>.webp (fade, ≤180 css px, rises behind the nail
  row); gallery/Journal tile characters → st-character-*; Journal tile 2 → Brainwave scene (not the “tha” pack);
  guide → st-nail-guide.webp (teaser hidden until G2; guide page illustration, alt LND-043). Lifestyle held (no alt
  rows); finger states not shipped; desi-diet-can-v1 not referenced anywhere.
- Packaging: st-package-<key>.webp + -13x.webp (clean-edge derivatives, content locked) in a campaign-colour panel
  with three loose nails (snippets/st-package-panel): shop cards, PDP (replaces the one-image gallery via a section
  setting), Our Story stack. Box ≤380 css px, srcset of the two files only, CSS shadow.
- Policy links render only when the policy body exists: footer, Help topics (delivery → shipping, returns → refund),
  PDP-008 “Delivery & returns” (both bodies), bag help link. Owner saved Shipping + Refund at 15:01 IST, so they show.
- QA: home, shop, 2 PDPs, Our Story, guide, help, bag, Journal at 320/390/430/1280: no overflow, Liquid or console
  errors (shop.app 403 only). Purchase flow re-verified with the panel PDP. Screenshots qa/foundation/art/, qa/motion/.

## 14. Register v1.2.1 + SEO S1–S4 — 9 Oct (evening)
- v1.2 theme-local rows installed: Help topics rebuilt as anchored disclosures (delivery/returns/orders, bodies
  PG-039/042/047 with “Email us” → #contact, policy links PG-105/106); Help form open (G8: PG-048/049/059 + PG-107 email
  line, matched against the policies, no phone per D10); PG-034; footer LND-060 set + SEO-075…078 (policy links only
  when the body exists; Terms waits on G16); bag help card MC-043/044 + MC-045 links; MC-031 empty-bag line; MC-035;
  MC-016 / JRN-002 / LND-057 final (G12); alts LND-012/013/034/035/043, PG-032, SEO-045…051 (chapters), SEO-033…039
  per SEO-053 (Our Story boxes); lifestyle images released (SEO-079…085): PDP slide 2 with thumbnails, shop-card hover.
- SEO: /collections/all title/meta (SEO-003/004) and 404 title (SEO-073) in meta-tags; st-seo interim noindex list
  (§3); Product @id + spaced description + Home › Shop › Set crumbs; Article JSON-LD (Organization author). One block
  per type verified on PDP and article. S4: the bag DOM has one H1; Horizon's inert empty-cart <template> holds the
  second.
- Uploads verified by checksum; QA 320/390/430/1280 on 11 page types clean (shop.app 403 only).

## 15. Hero v2.2, refund switch, G13 correction — 9 Oct (late)
- Hero v2.2 (st-fable final pass): assets/st-hero-motion.js 3c379254… (27154 B) and assets/st-hero.css 2156b0a6…
  (11980 B), byte-identical to motion/; no Liquid change. Runs clean at 320/390 (sets advance, CTA follows, no errors).
- Theme setting “Refund policy text verified” (config/settings_schema.json, group “Small Talk”, default OFF): while off,
  the Help Returns topic (+ PG-106), PDP-008 and the bag “Delivery & returns” link and the footer Refund policy link are
  hidden (the refund policy body currently repeats the shipping text). Turn it on in the theme editor once fixed.
- G13 not met: Help “Orders” topic (PG-045…047) hidden again. Help shows email only (D10).
- Served copy check: the CDN minifies theme JS/CSS (served JS 17809 B, CSS 8121 B), so its md5 never equals the stored
  file. The served JS contains the v2.2-only code (all four sides set to 'auto' in renderCharacter, srcset removal,
  'playing' state), and the live character renders `inset: 50% auto auto 0px`. Preview rendered: Help topics = delivery
  only; footer = Shipping policy + Privacy policy; PDP = “Need a hand? →” only; bag = MC-044 + Help + Contact us.

## 16. Final-acceptance fixes (J1, H, P) — 9 Oct (evening)
- J1 (blocker): sections/st-article.liquid (15e2f6f7…). Beat nails left absolute positioning: own row under the text on
  phones, reserved right column ≥750px. Beat type ST Display clamp(1.5rem, 0.6rem + 4.5vw, 1.9rem) / 1.14, 24ch (2.25rem
  ≥750). Standfirst (body before the beats) renders above the carousel; empty trailing body div removed. 7 stories × 5 beats ×
  320/390/430/1280: no overlap, no clipping, tallest slide 408px (+44 controls +65 sticky header ≤ 517px). Frames qa/foundation/j1/.
- H: hero v2.3 — assets/st-hero.css 8fe58c14… (12728 B) byte-identical to motion/; JS unchanged 3c379254….
- P: search-dialog result titles h4→h3 under the dialog's h2, h4 look kept (predictive-search-products-list /
  -resource-carousel / -styles). PDP thumbs: aria-current="true" set/removed properly (toggleAttribute wrote an empty value =
  false), blue ring outside the panel colour, thumb image kept inside its button (it overflowed 17px). Noindex for ?page=N past
  the last page: collections by the new theme setting Small Talk › Shop › Products per page (st_shop_per_page, default 24; moved
  from the st-shop section so the head can read it), Journal by 12. Organization/publisher logo = theme logo → shop.brand.logo →
  shop.brand.square_logo; none set today, and the wordmark is live text (no image asset), so the property stays omitted.
- P addendum: /pages/nail-guide-desi gets "noindex, follow" via a new interim handle list in st-seo (465b7b95…), comment
  “remove when G2–G4 guide content is live (only guide route; st-fable)”. Nav link unchanged. Lock released 9 Oct, 12:51.

## 17. Fidelity phase prep — 9 Oct (local only; theme writes blocked by this session's permission classifier)
- Diet can: assets/desi-diet-can-v1.webp read from 186649313493 (read only) → theme-build/ref/ and src/assets/st-diet-can.webp,
  md5 d827ef65…, 1189×1323 RGBA. Not uploaded yet.
- LND-009 → Shop “{name}” (locale small_talk.hero.shop_set; ↗ stays aria-hidden markup). JRN-011 moved to its own key
  small_talk.journal.shop_set (no quotes) in st-article. Not uploaded yet.
- Fonts (board type picks, spec/tokens.css). Licence: SIL Open Font License 1.1 for all six; no Reserved Font Names
  declared. Sources + OFL.txt kept in theme-build/fonts/<family>/. Subsets (Basic Latin, Latin-1, ‘ ’ “ ” … – — · • ₹ ‹ › −,
  ← → ↗ where present) cut with fontTools into src/assets/:
  st-fraunces-900.woff2 16,140 B (static wght 900 SOFT 100 WONK 1 opsz 144) · st-caveat.woff2 66,616 B (wght 600–700) ·
  st-barlow-sc-600.woff2 13,280 B · st-source-serif-700.woff2 20,148 B (static wght 700 opsz 60) · st-kalam-300.woff2 12,892 B ·
  st-dm-sans.woff2 20,716 B (wght 400–600, opsz 14). Total 149,792 B. snippets/st-fonts.liquid: faces with swap, metric-matched
  local fallbacks, stacks with fallback faces. Layout: st-tokens.css (= spec/tokens.css) before st-brand-styles; home preloads
  Fraunces + Caveat only.

## 18. Fidelity prep: hero v3 Liquid, header, landing (local only; theme writes still blocked) — 9 Oct
- Hero v3 (CONTRACT 7f753629…): st-hero.liquid without character inline styles, note/h1 classes and the section's
  font/colour overrides; hero_character + sample_columns map fields (Diet Cherry = st-diet-can.webp 1189×1323; Green Flag
  sampleColumns [1,0]); assets st-hero-motion.js 9224c991… / st-hero.css 30180777… staged byte-identical.
- Header to board 2 at 390 (mocked with real fonts): 69 px paper, burger 14–42, logo 84 px wide at x 92–176 (ST Display
  kept until a logo face is picked), "the talks" Caveat 600 at x 212–309, bag 338–374; :root --st-header-h 69 / 76 px.
- Landing (board 3), built in a lab first (theme-build/lab/landing.html, tools/build_landing.py, landing_fit.py,
  lab_shots.py, ink_bands.py) and ported:
  assets/st-landing.css (scaling unit --k = 100cqw/390 capped 1.4px, top-edge masks, beeline, chapter pattern, cream
  sections; per-chapter positions generated), snippets/st-landing-join (from spec/joins.json: heights, curves, beeline
  paths, dash offsets), snippets/st-landing-map (headline sizes, nail rows, art placements, ticks, collage, avatar crops),
  sections st-chapter (arc headline as SVG textPath, real text in the h2), st-gallery (tiles), st-teaser (talks /
  journal / guide), st-faq (flows with open answers), st-footer (3 board layouts by template), index.json without
  chapter `thread`. Chapter text positions follow the board's ink bands where the spec boxes were off (Diet Cherry
  nails/name/pill sat 25–35 px higher in landing.md than on the board).
- Caveat subset widened to 500–700 (69,688 B) for the board's lighter handwriting (spec uses Caveat 500 on teasers).

## 19. Upload: hero v3, header, fonts, tokens, landing, footer, guide template — 9 Oct (17:40–17:47 UTC)
- Theme writes allowed by the user. 31 changed files uploaded to 186651934933 (staged PUT, md5 verified, then
  themeFilesUpsert in dependency order: assets → snippets + locale → templates + footer group → sections + layout);
  every remote checksum equals the local file (incl. JSON). Theme stays UNPUBLISHED.
- Assets: st-hero-motion.js 9224c991… / st-hero.css 30180777… (frozen v3), st-tokens.css d05b23f1… (= spec), st-landing.css,
  st-diet-can.webp d827ef65…, fonts st-fraunces-900/-700, st-caveat (500–700), st-barlow-sc-600, st-source-serif-700,
  st-source-serif-logo-900, st-kalam-300, st-dm-sans (all OFL 1.1, subsets).
- Follow-up fix: Pinky note/headline lowered (note was inside the section's top curve at the left); st-landing.css
  166de81c….
- Preview checks (390 + 1280): home 12 landing sections + hero, 7 chapters, 13 arc lines, 10 beeline segments, landing
  footer; no Liquid errors / missing translations / horizontal scroll; console only shop.app 403. Guide template via
  ?view=nail-guide renders 3 steps + quick answers with no robots tag; /pages/nail-guide-desi keeps noindex until its
  suffix changes. Shots + side-by-sides: qa/fidelity/landing-390.png, qa/fidelity/landing/*-390-vs-board.png.

## 20. Shop (board 5 frame 1) — built in the lab, uploaded 9 Oct (18:03–18:05 UTC)
- Lab: tools/build_shop_lab.py (same markup/CSS as the Liquid) → lab/shots/shop-390(-vs-board-w).png; positions fitted to
  board ink (sbs width mode = px-for-px at 390).
- Heading fitted to the board ink, not the spec box: Source Serif 4 **Black** opsz 60, 63 px on a 49 px line (board ink
  x 19–277, baselines 117/166; spec said 700 / 54 px). New face st-source-serif-900.woff2 30ff27b4… (static instance,
  same 206-glyph Latin subset as the 700 file, 18 KB) under its own family "Source Serif 4 Black" (--font-shop-display),
  so the 2.5 KB wordmark subset stays the only 900 file on other pages. Card names also Black, 21 px (board cap height
  14–15 px; 22 px wraps "Shaadi Shift" beside "Rs. 699").
- Note: Kalam 23 px, −4°, second line indented 45 px (board), drawn arrow. Chips: All sets / Everyday / Statement as tag
  URLs (/collections/all/<tag>), aria-current on the active one, 44 px tall, padding 1.1 rem so all three fit one row
  at 390 with the selected chip bold. Visually hidden status "{count} sets" on tag pages (MC-024).
- Cards: 175×160 set-colour tile, package art (st-package-<key>.webp, 1x/1.3x srcset, ≤380 css px), red name, navy price
  through Horizon's price snippet with a new trim_zeros param ("Rs. 599", store currency format unchanged), "View set →".
  Grid 2 cols, 13 px column gap, rows every 236 px (board); 3 cols ≥750, 4 cols ≥990; board order on page 1.
- Footer rows: each row one 44 px hit area (board rows are 22 px apart; accessibility minimum wins), tighter padding.
- Uploaded (md5 = local): assets/st-source-serif-900.woff2 30ff27b4…, snippets/st-fonts.liquid 12f5aa16…,
  snippets/price.liquid c57ae9bd…, snippets/st-product-card.liquid 84ce48cc…, locales/en.default.json e0000049…,
  sections/st-footer.liquid 0a5e9873…, sections/st-shop.liquid c8db0420… (chip padding fix re-upload).
  templates/collection.json unchanged (e4c39d93…).
- Preview (tools/preview_shop.py, 390 + 1280): /collections/all, /all/everyday (4 sets), /all/statement (3 sets) all 200,
  no Liquid errors / missing translations / horizontal scroll; tag pages noindex, follow; chips one row; footer rows
  layout; console only shop.app 403 + Shopify analytics beacons. Horizon ≥990 scrolls inside .page-wrapper (stock drawer
  squeeze), so the desktop shot unwraps it for capture only. Sheets: qa/fidelity/shop-390-vs-board.png (width),
  shop-390-vs-board-h.png (height), shop-tags-390.png, shop-1280.png.
- Known differences: price "Rs. 599" vs board ₹599 (SD20 money format, owner); with ₹ "Pinky Promise" would fit one line.
  Package art is the approved portrait box (362×494), so it doesn't fill the tile like the board's mock-up crop (no new
  art). Board draws the last card wider (220 px); spec keeps the 175 px column. Footer taller (44 px rows); legal row shows
  only policies that exist (Refund hidden until SD25, Terms until G16).

## 21. Preview acceptance 1 fixes: hero v3.2, Brainwave / Green Flag art, FAQ pitch — 9 Oct (18:14 UTC)
- Hero v3.2 FROZEN copied byte-identical from motion/: st-hero-motion.js 44d40cf0… (boot() keeps a tap made while set 1
  decodes), st-hero.css 2da6fc54… (v3.1 word spacing). Remote checksums equal.
- Root cause of both art regressions: Horizon base.css `img { max-width: 100% }` capped art images at their clip-box width
  (Brainwave 209 → 139 px, Green Flag 351 → 230 px, so its 700 px-tall image ended above its box; On Me 400 → 390). The lab
  has no base.css, hence lab ≠ preview. Fix: `.st-land__art img { max-width: none }` in st-landing.css.
- Brainwave character refitted to the board face by normalised cross-correlation (3 patches agree: ≈315 px wide, left −110,
  top −136; set −143 after the visual check): img 315 px (1.04× of the 303 px asset), box 0–170 × 0–330, right feather
  24% (≈41 px) + bottom 15%, intersect. Green Flag chapter art placed by its rotary dial at the board's dial position
  (x≈95, y≈690): 324 px (1.2×), left −127, top −120, same box and masks (the board phone is a different drawing, so
  matching was not usable).
- FAQ rows: Horizon's summary padding (0.7 rem) and 1.4 line-height removed; divider as an inset shadow → 44 px pitch (touch
  minimum; board ≈41, was 50).
- Uploaded (md5 = local): assets/st-landing.css c37b9e9f…, snippets/st-landing-map.liquid a3848f0b… (generated by
  build_landing.py; only the two art lines changed). Preview at 390: Brainwave img 315 px at −110/−143 in 170×330
  (intersect); Green Flag img 324 px spanning section y −120…865 over its 560…865 box; FAQ pitch 44/44; section heights
  unchanged. Route checks 390 + 1280 clean. Sheets refreshed from the preview: qa/fidelity/landing/*-390-vs-board.png.

## 22. Shop acceptance 1 fixes (tile art, tile colours, last card) + MC-016 v1.3.5 — 9 Oct (18:23 UTC)
- Tokens: assets/st-tokens.css = spec/tokens.css 6b6446da… (adds --st-tile-<set>, board-5 medians; Pinky cobalt #045af1
  per the orchestrator).
- Card (snippets/st-product-card.liquid bde30f8a…): tile 176/172, `container-type: size`; box at 8cqw / 8cqh, 85cqh tall
  (CSS drop-shadow); loose-nail column of sprite cells (st-nails-<set>.webp, 204×354 cells, cell = 32% of the column
  height, step 25.3%, rotated 15–20°) starting at max(76% of the tile, box + 4 px), columns per spec (Wild Card 3 nails).
  Plain-% fallbacks for browsers without container units. Product names are now h3 (row is a div).
- Section (st-shop.liquid 0915ad4c…): phones, an odd last card spans to 62% of the grid (223 px) with a 223/155 tile and
  the box + nails centred as a group (the board's wide box isn't available; the approved box is portrait). Shop bottom
  padding 2.5 → 1 rem.
- templates/collection.json adc006bf…: MC-016 v1.3.5 note "Same nails. Different moods." (register row checked).
- Preview (390 + 1280, all 3 routes): tiles 174×170 in token colours, box 14,14 · 144 px tall, nails at 76–91%, last card
  223×155 with "Pinky Promise" on one line (Statement's third card gets the same treatment), 7/4/3 h3s, no Liquid errors /
  missing translations / horizontal scroll. Sheets: qa/fidelity/shop-390-vs-board(-h).png, shop-tags-390.png,
  shop-1280.png.

## 23. Hero v3.3 (JS only) — 9 Oct (18:25 UTC)
- motion/st-hero-motion.js 72defd54… copied byte-identical to assets/st-hero-motion.js (fixes the ~250 ms bare-nail moment
  during flights); remote checksum equal. st-hero.css unchanged (2da6fc54…). Preview smoke test at 390: script loads,
  autoplay advances, no page errors.

## 24. PDP structure (board 5 frame 2, spec/product.md) — 9 Oct (18:35–18:44 UTC)
- Kept Horizon's product-information (variant handling, product form, cart events) and restyled it to the board; the
  board parts live in our blocks/snippets. **The seven products use `templates/product.desi.json`** (template suffix
  "desi"); product.json gets the same settings. JSON templates are normalised by Shopify, so their remote md5
  (1a11202f…) differs from the local file; content checked by reading the remote body.
- Media (snippets/st-pdp-media.liquid): 375×315 panel at x 8, radius 14, set colour (campaign background = hero mid);
  slide 1 is the board scene: approved box at 11% / 13%, 79% tall, plus six sprite-cell nails (genuine designs per set)
  at the board's positions, rotated −25…+25°. Slide 2 the lifestyle composite. Thumbs 70×70, gap 6, radius 6, selected
  ring = deeper set colour. Only existing media (G11).
- Title: Horizon h1 on `--font-pdp-title` (tokens round 6: Source Serif 4 Black; mapped in st-fonts to the full
  'Source Serif 4 Black' face), 50 px burgundy. Price block passes trim_zeros ("Rs. 599"), right-aligned 24 px.
- Buy row: stepper 103×44 radius 6 · Add to bag #940326 radius 6 ("Add to bag · Rs. 599", money_without_trailing_zeros)
  · Save toggle (new snippets/st-save-toggle.liquid, PDP-055…057): icon button, aria-pressed, name "Save {product}" /
  "Saved: {product}", hover/focus hint, polite status "Saved on this device." / "Removed from saved.", localStorage only
  (try/catch; hidden when storage is blocked or before JS), 30 px wide with a 44 px hit area. Dynamic checkout off.
- Notes block (blocks/st-product-notes.liquid): description #373f8b 17 px + "Find your fit →" (PDP-007 → guide);
  links row Delivery & returns (still gated on SD25) | Need a hand?; disclosures in red DM Sans 700 with 2 px "+":
  What's in the kit (PDP-002/003 installed, G1 met), Fit & application (PDP-004/005 installed, G2–G4 met), The story
  (collapsed); coda: the Journal story's excerpt as a Kalam quote (−6°, one sentence per line), "Read the story →"
  (PDP-010) and the set's character peeking from the right edge (eye at 70,65 of a 115×130 crop; scale ≤1.07×).
- Locale: small_talk.product.find_fit / save_label / saved_label / save_hint / saved_hint / saved_note / unsaved_note.
- Checks (tools/pdp_functional.py): Save toggle on/off/persist + announcements OK; Add to bag still adds (cart 0 → 1,
  test cart cleared); all 7 PDPs 200, no Liquid errors / missing translations / horizontal scroll, 6 nails + quote +
  peek each. Sheets: qa/fidelity/pdp-390-vs-board(-h).png, pdp-<handle>-390.png, pdp-1280.png.
- Known differences: board thumbnails 3–5 are product photos/video that don't exist (G11); the board's peek is a flat
  box-style face (no such art; the painterly character is used, per spec); Delivery & returns hidden (SD25); "Rs." (SD20).

## 25. Card-name font (round 6) + shop tile polish — 9 Oct (18:54 UTC)
- New face: IBM Plex Sans Condensed Bold (OFL; source + licence copied to theme-build/fonts/ibmplexsanscondensed/ from
  spec/fonts/) → assets/st-plex-cond-700.woff2, 206-glyph Latin subset (same set as the other faces, incl. ₹, curly
  quotes, →), 15,488 bytes, md5 72040462…. Metric fallback 'IBM Plex Sans Condensed Fallback' = Arial Bold, size-adjust
  89.91% (width-matched), ascent 114.0%, descent 30.59%. st-fonts maps --font-card-name to it.
- Tokens restaged: assets/st-tokens.css = spec/tokens.css d11e148c… (round 6 card-name / PDP-title tokens).
- Shop cards: names on --font-card-name 700 / 21 px / --st-red; prices on the same family 700 / 17 px (acceptance 2:
  board prices are the same bold sans; spec shop.md still says DM Sans 700). Polish: box 90% of the tile height
  (≈64–66% of its width), nails alternate ±12°, Brainwave's lie near horizontal (84° / 96°).
- Uploaded (md5 = local): st-plex-cond-700.woff2, st-tokens.css, snippets/st-fonts.liquid fc0cb2e6…,
  snippets/st-product-card.liquid 7c69b580…. Preview: Plex loads on all shop routes, no errors, box 112×153.
- PDP title already on --font-pdp-title (Source Serif 4 Black). PDP price stays DM Sans 700 24 px per product.md.

## 26. PDP acceptance 1 fixes — 9 Oct (19:01 UTC)
- Scene: box from x 33 (6.7%), 85% of the panel; nails +10% and packed against the box's tray edge (≈7 px overlap).
- PDP price on IBM Plex Sans Condensed 700 / 25 px (one price face across shop / PDP / bag).
- 44 px minimum: stepper 118×44 (−/+ 44 wide; Horizon's 37 px input min-width overridden), Save 44×44, Add to bag 184 px.
- md5: st-pdp-media 95d90194…, st-save-toggle 0f26e292…, st-product-notes 1703fa28…. All 7 PDPs + functional re-run OK.

## 27. Bag (board 5 frame 3, spec/bag.md) — 9 Oct (19:09–19:13 UTC)
- Kept Horizon's main-cart (quantities, remove, checkout) and restyled the page (CSS in sections/st-bag-extras.liquid,
  scoped .cart-page; the cart drawer — not used on this store — keeps Horizon's look via `context != 'drawer'`).
- Shared tile: new snippets/st-pack-art.liquid (box + loose nails, and the tile CSS, which has to live in a snippet that
  renders on the page: snippet {% stylesheet %} only loads where the snippet renders). Used by st-product-card and by
  the bag line items (135×145 tile).
- Line items (snippets/cart-products.liquid): tile, name Plex 19 px red, unit price Plex 17 px, stepper 115×44, visible
  "Remove" (MC-037; accessible name "Remove {product} from bag"), line total visually hidden (board has none), prices
  without trailing zeros. Horizon's "Have an account? Log in…" line hidden (no register row).
- Summary (snippets/cart-summary.liquid): "Subtotal" serif 22 px navy, amount Plex 22 px, MC-040 note installed (G15
  met), burgundy Checkout #8d0223 radius 6; empty-bag CTA restyled burgundy (blue pill retired).
- st-bag-extras: "← Continue shopping" (MC-042), help panel #f8f7f7 (MC-043/044; links "Help centre" SEO-068, "Shipping &
  returns" SEO-069 — still gated SD25 — and "Contact us") with the campaign character peeking bottom-right, promo panel
  #fee2ed (MC-026 heading + Kalam sub "Collect the whole story.", four upright sprite nails).
- md5: st-pack-art 0a315666…, st-product-card 84af6afd…, cart-products bf6bd16e…, cart-summary 66f811a9…,
  st-bag-extras 1f39a6f1…, en.default.json 445aa9da…, templates/cart.json 69747dac….
- Checks (tools/bag_functional.py, tools/preview_bag.py): + / − / Remove work and the subtotal follows; test carts
  emptied; 390 + 1280 clean, no horizontal scroll. Sheets: qa/fidelity/bag-390-vs-board(-h).png, bag-empty-390.png,
  bag-1280.png.

## 28. Narrow-phone buy row (PDP preview 2) + spec round 7 — 9 Oct (19:17 UTC)
- Buy row: Add to bag `flex: 1 1 auto; min-width: 0` (its wrapper too; Horizon gives row children `flex: 1 1 185px`).
  The label is split from the PDP-011 locale string itself (blocks/add-to-cart.liquid: "Add to bag" + " · {price}");
  below 380 px the price part is visually hidden but stays in the accessible name; gap 8 px, padding 6 px there.
  Preview: scrollWidth == viewport at 320 / 375 / 390; Save 16 px from the edge at 320 and 375; full label at 390.
- Round 7: tokens restaged (st-tokens.css 325a6d24…: --font-price, --fw-price, --fs-price-pdp/card/bag,
  --color-price); st-fonts maps --font-price to Plex + its fallback; shop / PDP / bag prices use the tokens. PDP panel +
  thumbs on --st-tile-<set> (campaign background as fallback); scene nails rotated −38…+35°.
- md5: st-tokens 325a6d24…, st-fonts 2d8b8487…, st-pdp-media 806fe5ce…, st-product-card 764b8c9d…, add-to-cart
  cb683877…, st-product-notes 06478dac…, st-bag-extras 828e99fe…. Sheet: qa/fidelity/pdp-narrow-320-375-390.png.

## 29. Bag acceptance 1 fixes + Journal index (board 4 frame 3) — 9 Oct (19:20–19:30 UTC)
- Bag: subtotal label + amount on the price face, 24 px, #14163b; promo heading 30 px. The light "−" at qty 1 is a
  real disabled state (Horizon sets button.disabled at the minimum), kept. st-bag-extras 07e8cc67….
- DM Sans subset rebuilt with weight 400–800 (opsz 14 pinned, as before; same 205 glyphs), 21,204 bytes, a6435076….
- Journal (the Journal blog uses templates/blog.desi.json; blog.json still serves the talks until that step):
  sections/st-journal.liquid rewritten — "04 /" (JRN-056, aria-hidden), H1 blog title Source Serif Black 80 px black,
  sub (JRN-002 "Seven sets. So many stories."), Kalam margin note top right (JRN-003) with drawn slash + squiggle;
  stories in board order (card_order, through each campaign's Journal story), first = Featured (JRN-004) on a tint of
  its set colour. New snippets: st-journal-card (one link per card; DM Sans 800 names, headline 19 px bold on the
  featured card / 16 px regular on rows — board ink, spec said 19, excerpt 12 px, red "Read the story →" JRN-005) and
  st-nail-closeup (four whole sprite nails lying diagonally on --st-tile-<set>; no new art).
- md5: st-journal 79ab9742…, st-journal-card 94ce2c24…, st-nail-closeup 62c8e1d3…, st-fonts 1537d6b4…,
  blog.desi.json b39a7221…. Preview 390: 200, clean, scrollWidth 390. Sheet: qa/fidelity/journal-390-vs-board(-h).png.
- Note: snippet {% stylesheet %} changes reach the preview a few seconds after the upload (compiled styles.css) —
  re-shoot if a sheet looks unchanged.

## 30. Journal story (board 4 frame 4) — 9 Oct (19:32 UTC)
- sections/st-article.liquid rewritten (articles use templates/article.desi.json → st-article): "← All stories"
  (JRN-007), the beat pager "n / N ‹ ›" (JRN-009, 44 px buttons, polite status) top right, category eyebrow from the
  `category:<label>` tag (JRN-008/057–063, uppercased), H1 set name DM Sans 800 58 px, headline 25 px, standfirst
  (JRN-010, required; small muted), hero = the set's chapter art bottom crop (props) on its colour, ≤351 px wide (1.3×
  of 270), excerpt as the pull headline (Source Serif Black 33 px, one sentence per line), beats as body text in a
  scroll-snap track that the top pager drives (<st-beats> now wraps the whole top so st-beats.js is unchanged),
  "Shop {set} →" pill #a80f2a (JRN-011, G5-gated), "More stories from the Journal" (JRN-013; locale updated) = the next
  three other stories in board order with nail close-up thumbs and red chevrons. "Next story" (JRN-012) omitted (T81).
- md5: st-article 8a84fd18…, en.default.json 4f774d70…. Checks (tools/story_functional.py): pager/status/ends/
  ArrowRight OK; 7 stories 200, clean, 5 beats each, eyebrows MY TREAT … SHOWING UP, scrollWidth 390.
  Sheet: qa/fidelity/journal-story-390-vs-board(-h).png.

## 31. Journal acceptance 1 fixes + journal grounds — 9 Oct (19:37 UTC)
- Journal grounds sampled from board 4 (median of each card image's ring 4–10 px inside the edge): on-me #fcc92a,
  brainwave #0452e5, green-flag #105908, shaadi-shift #fa5987, diet-cherry #cb0419, wild-card #d6d306, pinky-promise
  #ca89f4 (lilac). Used as var(--st-journal-<set>, hex) in st-nail-closeup (journal: true) for the index cards and the
  story's "More stories" thumbs; values sent to st-boardspec for journal.md / tokens.css. Shop keeps --st-tile-*.
- New snippet st-sentences: each sentence in a no-wrap span, so two-sentence headlines break only between sentences
  (journal card headlines, story headline, More stories lines).
- Cards: set name is an h2 (inside the one link); the link is aria-labelledby name + headline with a visually hidden
  colon → "Green Flag: Tum aa jao. Main dekh lungi."; the card text wrapper is a div (h2 can't sit in a span).
- md5: st-sentences 9e7d0289…, st-nail-closeup 57502ddb…, st-journal-card eeea3681…, st-article aec30f42….
  Preview: 7 h2s, names as above, grounds = samples, scrollWidth 390; story checks re-run clean.

## 32. Story acceptance 1 fixes + journal tokens restaged — 9 Oct (19:40 UTC)
- tokens.css restaged (77add7a7…): --st-journal-<set> + --st-journal-featured-tint 22% (st-boardspec, round 9); the
  featured card uses the tint token.
- Story body (beats) colour #6e7184 (spec --st-body; the theme's --st-body is the brand setting #272332). Computed
  ground #fffdf5 (paper-like): 4.73:1 (#6a6d85 would be 4.98). H1 62 px (board ink ~7% wider).
- Story headline sentence-safe at 320 ("Tum aa jao. / Main dekh lungi."), scrollWidth 320 / 390.
- md5: st-article 5b7ff6b4…, st-journal-card a12cc38c…. Sheets: journal-390-vs-board.png, journal-story-390-vs-board.png,
  journal-story-green-flag-320.png.

## 33. Our Story (board 4 frame 5) — 9 Oct (19:43–19:46 UTC)
- The page uses templates/page.desi.json → new sections/st-our-story.liquid (replaces st-page there). Centred H1
  PG-001 "Small talk. / A lot said." (Source Serif Black 68 px, board ink; spec said 58), sub = the page body's first
  paragraph (PG-002), stack of three approved boxes (On Me, Brainwave, Pinky; 240 px tall, ~8 px tucked, CSS shadow;
  box alts = product media alts), value columns with drawn sparkle / heart icons (PG-006…009), eye crop at 1.3× (the
  source cap) bleeding in from the left with a slanted top edge, Kalam line PG-010 with slash + inline heart, pills
  PG-011 "Shop all sets →" (#a80f2a) and PG-012 "Read the Journal" (outline #d0204a). PG-003…005 (rest of the body)
  are not on the board: `show_body` (off) renders them.
- md5: st-our-story ddc77433…, page.desi.json 44988683…. Preview 390 / 320: 200, clean, scrollWidth = viewport.
- Known: the board draws the boxes landscape (~265 × 240); the approved boxes are portrait (~176 × 240 at the same
  height); no new art.

## 34. Journal index at 320 (re-check) — 9 Oct (19:47–19:51 UTC)
- st-sentences: sentences are `display: inline-block; max-width: 100%` (whole when they fit, wrap inside when not)
  instead of nowrap — the nowrap version widened the 320 layout to 350.
- Card image column clamp(118px, 49%, 172px) (172 at 390 as on the board; 139 at 320).
- "Journal" H1 clamp(60px, 20.5vw, 80px); below 380 px the H1 is 19vw and the margin note 13 px / 96 px wide, so the note
  stays right of the word.
- md5: st-sentences f508ea95…, st-journal-card ce6df97e…, st-journal 6ee1b584…. Preview (tools/journal_narrow.py):
  scrollWidth 320 / 390 on the index and a story, no clipped card text, story body rgb(110,113,132).

## 35. Our Story at 320 — 9 Oct (19:52 UTC)
- The handwritten note's box is now its content (width: fit-content); below 360 px it is 18 px and starts at x 138
  (eye crop 150 px wide). Preview: note box x 138–296 at 320, 165–371 at 390; scrollWidth = viewport. st-our-story
  b48598c3…. Sheets: qa/fidelity/our-story-320.png, our-story-390.png.

## 36. the talks: hub + thread templates (board 4 frames 1–2) — 9 Oct (20:00–20:22 UTC)
- Option B: the default `templates/blog.json` / `article.json` now render the talks (they serve the-talks and news; the
  Journal keeps blog.desi / article.desi). Sections: `st-talks-list` (hub), `st-talks-thread` (thread + comment form),
  `st-talks-start` (#start-a-talk, contact form tagged start-a-talk), `st-talks-rules` (TLK-070…077, tel:14416 and
  tel:18008914416, mailto to shop.email). Snippets `st-talk-avatar` (set nail, sprite col 0, blush disc, −20°; initial
  fallback), `st-talk-time` ("9 Oct", relative under 7 days via `st-talks.js`). Talks chrome only on blog_handle
  "the-talks". Locale small_talk.talks.{replies,suggested_by,time,hub,thread,start} = TLK-005…061 (en.default 4613e90c…).
  `st-forms.js`: icon-only submit keeps its icon (status region gets "Posting…"), hints stay in aria-describedby,
  folded reply fields open on an invalid submit.
- Links: header talks_link, footer link_3, landing teaser (LND-031) → /blogs/the-talks.
- Board fit (hub, 390): H1 ink 46–344 × 153–223 (board 48–348 × 154–224) = Source Serif 4 Black 95 px −0.06em with a
  sampled burgundy shade (spec said Bold 74); tagline 95–294 × 238–256 (board 97–296 × 238–260), faux italic of a new
  Source Serif 4 500 instance (st-source-serif-500.woff2, 18 KB; no italic master in spec/fonts); sub in the serif at
  20 px as the board shows (spec said DM Sans); pill 72–318 × 319–371. Start panel H2 Black 46 −0.06em (board ink
  186 × 34), sub 18 px.
- Upload incident: `'{n}'` inside `{{ }}` ends the output tag at the first `}` (Liquid tokenizer), so the URL upsert of
  list/thread silently failed; placeholder is now `__n__`. Five probe sections `sections/st-zz-a…e.liquid` were created to
  find it; themeFilesDelete is refused by the MCP policy, so they stay (unused, no presets).
- Preview: /blogs/the-talks 200, Liquid clean, scrollWidth 390 / 320; empty submit of Start a talk shows the MC errors,
  focus to topic, no POST to /contact (POSTs aborted in tools/talks_functional.py); every visible control ≥ 44 px.
  Not verifiable yet: thread rows, avatars, thread page, reply box (all 9 seed threads unpublished).
- md5: st-talks-list 78c213d1…, st-talks-thread f2b9ca16…, st-talks-start ed17f879…, st-talks-rules 6c8f1953…,
  st-talk-avatar 26e148ac…, st-talk-time 73129d5c…, st-talks.js 20a14def…, st-forms.js 56aa3425…, st-fonts 7fcd4712…,
  blog.json 93741e84…, article.json e3530b9f…, index.json eeb80858…, header-group 4da33967…, footer-group 73bc7bb7….

## 37. Our Story H1 at 320 (orchestrator) — 9 Oct (20:23 UTC)
- `.st-ours__title` font-size clamp(52px, 17.4vw, 68px): 55.7 px at 320, 65.3 at 375, 67.9 at 390; "Small talk." and
  "A lot said." one line each (2 lines total) at all three; scrollWidth = viewport. st-our-story 39d8a7f8….

## 38. Help (board 4 frame 6) — 9 Oct (20:25–20:36 UTC)
- New section `st-help` (page.desi-help.json): H1 PG-033, sub PG-034, a real search box (PG-035, GET /search, label =
  placeholder), then the theme blocks. `st-help-topics` ("Browse help topics", PG-036) and `st-help-topic` restyled to the
  board rows (95 px, 36 px line icons — van / clock-arrow / pen / bag, chevron that turns when open, #efeff2 dividers;
  new `icon` setting); inline "Email us" links get 44 px hit areas. `st-help-form` restyled (labels 15/700, fields
  #e6e6ea r8 44 px, textarea 80, Send pill #a80f2a with an aria-hidden arrow), carries its own field CSS now (it was
  unstyled: .st-field lived in the gated talk-form block), order-number field behind `show_order` (off: not on the board).
- Copy v1.3 from the register (template built by script from 04-pages.md): topic subs PG-038/041/044/046, Fit body PG-108
  + "Open the Nail Guide" PG-109 (Fit and Orders now shown: G2–G4, G13 met), intro PG-049, placeholders PG-053/056,
  submit PG-057. Delivery/Returns/Orders bodies unchanged (byte-identical to the register). Returns stays hidden (SD25).
- Board fit (390): H1 Source Serif Black 70 px −0.055em (ink 26–364 × 134–185; board 28–369 × 135–187; spec said Bold
  56); sub 21 px (board ink 189 px; spec 19); "Browse help topics" 22 px; "Still need help?" 21.5; intro 18 px, breaks
  before "to" as drawn. All within 1–4 px of the board; Send sits 7 px lower (44 px fields vs the board's 40).
- Preview: 200, Liquid clean, scrollWidth 390 / 320; #delivery opens on load; Fit opens with body + guide link; empty
  submit → "What should we call you?" / "We need an email to reply to." / "Don’t forget the message.", focus to name, no
  POST to /contact (tools/help_functional.py); no visible control under 44 px. Sheets qa/fidelity/help-390*.png, help-320.
- md5: st-help 44ab574d…, st-help-topic 06d81b21…, st-help-topics 6e5dbcea…, st-help-form bbdaebcb…,
  page.desi-help.json 83eaffab…, en.default 3b2d1ced….

## 39. Nail Guide (board 5 frame 5) — 9 Oct (20:38–20:48 UTC)
- New section `st-guide` (page.nail-guide.json → nail-guide-desi) with its own `step` / `question` blocks, replacing the
  st-page + st-gate + st-step stack. H1 PG-014 (Source Serif Black 54 px with the talks burgundy shade; spec said Bold 50,
  board ink 278 px), Kalam note PG-015 on two lines (−6°), On Me character peek top right (eye crop, 260 px = downscale,
  eye ≈ (370, 123)). Steps PG-017…026: number DM Sans 800 22 px #9e0a2b, title 800 17 px --st-red (board ink widths),
  body 14 px #6e7184; step 01 art = the accepted fingertip illustration turned so the tip points left (CSS rotate, 0.21×,
  no redraw) in the #f4eff0 panel, with three 2.5 px #2547d0 tick strokes; numbered list (PG-019 v1.3 wording) with
  Ø 21 #a60a2f dots; cards that open in place: size chart (PG-020: sub "Sizes 0–11, width in mm", twelve "0 = 18 mm"
  cells + two notes; the board placeholder never shows) and kit instructions (PG-023 / PG-026). Quick answers PG-027…031
  as 44 px rows. Steps 02–03 have no image (PG-032: no approved art).
- Copy built by script from 04-pages.md; kit steps and answers byte-identical to what was installed.
- Preview: 200, Liquid clean, scrollWidth 390 / 320, no page errors; H1 clears the peek (7 px at 390, 2 px at 320);
  all 3 cards and 4 answers open; 12 size cells; no control under 44 px (tools/guide_functional.py).
  Sheets qa/fidelity/guide-390-vs-board.png, guide-320.png. md5 st-guide 9149955f…, page.nail-guide.json b440b649….

## 40. the talks on real data (9 seeds published by the orchestrator) — 9 Oct (20:50–20:58 UTC)
- Hub: 9 rows newest first, each "{title}, 0 replies" link, "First reply’s yours ›" at 0, "11h ago" from published_at,
  set-nail avatars (all 9 resolve a set: tag). Chips Plot twists / Tiny wins / Nail talk; /tagged/tiny-wins 200 with 3
  rows and "Tiny wins" aria-current; an unknown tag is Shopify's 404. Thread: back link, avatar, "small talk · 11h ago",
  title, body, "No replies yet…", reply box (render only; fields fold open on focus, TLK-035/036/037 errors, "Post reply";
  nothing submitted: every POST aborted, no comment/contact POST sent).
- Fixes: "All" chip selected (current_tags is nil on the hub; was `.size == 0`); tag chip current (handleize the tag before
  appending — the filter chain had handleized the whole list); "Latest talks" in DM Sans (was inheriting Horizon's heading
  serif); chips 15 px padding; avatars as close-ups (nail 116 % of the disc, base cropped); thread title 800 / 30 px and
  body 21 px at 276 px (board breaks "…the stories / I never finished."); hub excerpts capped at 226 px (same break);
  the reply box shows the thread's set-nail avatar as the board does (spec said "?").
- Tagline: true italic now — st-source-serif-italic-400.woff2 (SourceSerif4-Italic instanced wght 400 / opsz 20, 206-glyph
  subset, 17 KB, italicAngle −12) + tokens round 10 restaged (st-tokens b3e9719f… = spec/tokens.css): --font/--fs (28 px)
  /--ls/--color-talks-tagline. Ink 89–297 × 235–261 (board 97–296 × 238–260).
- Preview: hub and thread 200, Liquid clean, scrollWidth 390 / 320. Sheets talks-390(-vs-board).png, talks-320.png,
  thread-390(-vs-board).png, thread-320.png, talks-tag-390.png. md5: st-talks-list 9a2aaffa…, st-talks-thread be1fc383…,
  st-talk-avatar 4baeb70e…, st-fonts 3e70db6b….

## 41. Footer dots at 320, guide step 01 copy v1.3.6, shop 320 overflow — 9 Oct (21:00–21:04 UTC)
- Footer rows variant (shop / PDP / bag / guide): the separator was `li + li::before`, which is exactly what puts "·" at the
  start of a wrapped line. Now each item is inline-flex + nowrap and the dot trails it (`li:not(:last-child)::after`), so a
  wrapped row ends with "·" and never starts with one. Checked at 320 on /, /collections/all, a PDP, /cart, the guide,
  Our Story and the talks: no line starts with "·" (landing and inner footers have no dots). st-footer 1366144c….
- Guide (st-copy v1.3.6, register already updated): PG-018 "Use a paper strip or a soft tape measure to find the widest
  part of your natural nail."; PG-019 item 1 "Place a strip of paper or a soft tape measure across your nail." Template
  rebuilt from the register (only those two strings changed). page.nail-guide.json e77715db….
- Found while checking footers: /collections/all overflowed at 320 (scrollWidth 341): the name + price row has no wrap, so
  "Brainwave Rs. 599" (155 px) widened its 138 px column, and the note's arrow ran to x 341. The row now wraps only when
  it must (price drops below the name: 320 all but On Me, 375 Shaadi Shift, 390 none — unchanged), and below 360 px the
  note starts at x 51. scrollWidth 320 / 375 / 390. st-product-card 90a6e372…, st-shop c943ff58….

## 42. 404 in the board system + final batch, lock released — 9 Oct (21:04–21:08 UTC)
- New section `st-404` (templates/404.json): MC-068 heading in Source Serif Black 56 px (≈14.4vw on small phones) with the
  talks/guide burgundy shade, repeated per line (`background-size: 100% 1lh`); MC-069 body 17 px #6e7184 (sentence-safe
  wrap); MC-070 "Shop all sets" filled #920324 pill and MC-071 "Go home" 2 px --st-outline-red pill, Barlow Semi Condensed
  600 22 px, 52 px tall, 300 px wide. No handwritten note (the register has none). Replaces the retired st-page chrome.
  Preview: /pages/no-such-page-xyz 404, Liquid clean, scrollWidth 390 / 320. Sheets qa/fidelity/404-390.png, 404-320.png.
- Footer dots (§41) and guide PG-018/019 v1.3.6 (§41) were already live; re-verified.
- Final file list since §40 (local md5 = remote checksum, all 12 re-read 21:08 UTC):
  assets/st-tokens.css b3e9719f… · assets/st-source-serif-italic-400.woff2 e249cb7d… · snippets/st-fonts.liquid 3e70db6b… ·
  snippets/st-talk-avatar.liquid 4baeb70e… · snippets/st-product-card.liquid 90a6e372… · sections/st-talks-list.liquid
  9a2aaffa… · sections/st-talks-thread.liquid be1fc383… · sections/st-footer.liquid 1366144c… · sections/st-shop.liquid
  c943ff58… · sections/st-404.liquid 954db5c7… · templates/page.nail-guide.json e77715db… · templates/404.json 2ebe5a00….
- Theme write lock on 186651934933 RELEASED by st-foundation (21:08 UTC).

## 43. HD art swap, batch "board-corrections-1" (landing chapters, Journal teaser, two story heroes) — 10 Oct (06:35–06:50 UTC)
- Lock re-granted by the orchestrator for this batch. Source: artwork/manifest.json hd.batches["board-corrections-1"] (web
  files, placements in 390-px section coordinates). Eleven web files copied byte-identical to theme assets st-hd-*.webp
  (md5 = local = remote): on-me-woman 428362d2…, on-me-receipt-hand 9dc89864…, green-flag-woman ff0e37f5…, green-flag-phone
  6dec0acf…, shaadi-shift-sweep 5d83cade…, brainwave-sketchbook 211c5d0c…, pinky-promise-scene d443d21d…, wild-card-woman
  8f6e5361…, wild-card-cards-hand ec63e10f…, journal-writing c7c24a6e…, journal-bag-notebook 591fa74e….
- tools/build_landing.py: the chapter art table now uses the manifest placements verbatim (left / top-in-section / width):
  On Me woman (−6, 450, 364) + receipt hand (111, 555, 287.4); Green Flag phone (−7.4, 590.2, 283.8) BELOW the woman
  (−7, 427.5, 405) (DOM order = stacking inside the art layer); Shaadi sweep (0, 524, 398.2); Brainwave props strip →
  sketchbook (12, 615, 370) (the character at the top stays); Pinky scene (−8.1, 407, 406.3); Wild Card woman (−8.1, 416,
  219.8) + cards-hand (135, 580, 237), marked INTERIM in a Liquid comment. Diet Cherry and the hero untouched. Baseline run
  first reproduced the live files byte-for-byte; after the edit only the art entries of st-landing-map changed (joins /
  st-landing.css identical, beeline and chapter boxes untouched). Art stays z 2 under headline / pills / controls (z 3);
  pieces past the section bottom are cut by the section, as the manifest's edge rule expects.
- Journal teaser (st-teaser): tiles = st-hd-journal-writing / st-hd-journal-bag-notebook, opaque, object-fit cover, the
  card supplies the 10 px radius (image-picker override kept); the unused example-key block removed.
- Story heroes (st-article): where the superseded chapter crops fed them — Brainwave = the sketchbook still life centred
  at the box width (journal-story.md); Green Flag = the landing scene window y 402–865 (the section's own bottom) scaled
  to the 372 × 442 box (--k = 100cqw / 390). Other sets keep their chapter crop. Also: story title min(62px, 17.8vw) —
  "Brainwave" at 62 px widened the column at 320 (pre-existing scrollWidth 331); now 320 on all 7 stories, 62 px at 390.
- Preview: landing 390 / 320 scrollWidth = viewport, Liquid clean, all 11 HD images loaded at the manifest widths; matches
  artwork/tests/hd/verify-landing-from-manifest.png. Sheets: qa/fidelity/hd1-landing-390.png (+ -320), hd1-<key>-390.png,
  hd1-landing-full-390.png, hd1-story-{brainwave,green-flag,on-me}-{390,320}.png. (Shooting note: full-page captures need
  img.decode() + a scroll pass, or Chrome paints the large async-decoded art blank.)
- Files: assets/st-hd-*.webp ×11, snippets/st-landing-map.liquid e02a8dd2…, sections/st-teaser.liquid 75582875…,
  sections/st-article.liquid 6445eb67…; tools/build_landing.py, tools/hd_sheets.py (local).
- Pending: hero v3.4 (wait for st-fable's frozen hashes); alts LND-034/035 + chapter alts from st-copy (the teaser alts
  still describe the old art: cobalt nails, silver bag). Lock held for those.

## 44. HD batch 1 alts (v1.3.7) + drawer account link (MC-094/095) — 10 Oct (06:50–07:00 UTC); lock released
- Alts from the register (05-seo.md, 03-landing.md, read by script): snippets/st-art-alt chapter = SEO-045 On Me, 046
  Brainwave, 048 Green Flag, 049 Shaadi, 050 Wild Card (interim), 051 Pinky (047 Diet Cherry unchanged). The landing map
  now carries them: build_landing.py `art(..., alt=True)` marks the describing layer — the FIRST layer in the DOM for the
  two-layer scenes (Green Flag phone, On Me woman, Wild Card woman), the only HD piece for Brainwave (sketchbook), Shaadi,
  Pinky — emitted as `alt="{{ st_alt | strip | escape }}"` from a capture of st-art-alt; every other layer alt="" (Diet
  Cherry ×2, Brainwave character, Green Flag woman, On Me receipt hand, Wild Card cards-hand). Joins / CSS output still
  byte-identical. Journal teaser tile alts = LND-034 / LND-035 (templates/index.json, two-line edit). Verified on the
  preview: each changed chapter described exactly once, the other layers empty. Hero layers untouched (alt="" when v3.4 lands).
- Drawer account link (owner 9 Oct): below the main links inside the drawer's st-focus-trap, wrapped in
  `shop.customer_accounts_enabled`; signed out "Sign in" (MC-094, accessible name "Sign in to your account") →
  routes.storefront_login_url (else routes.account_login_url); signed in "My orders" (MC-095) → routes.account_url.
  44 px tall. Locale small_talk.header.sign_in / sign_in_label / my_orders. Verified at 390: href
  /customer_authentication/login?return_to=<current page>, Tab cycles inside the dialog (Close → links → Sign in → Search →
  Bag → logo → Close), Escape closes, the link reaches "Sign in - Small Talk" (shopify.com/authentication/83023397077/login),
  back returns to the page; nothing submitted. At 1280 the header shows the desktop nav and no drawer (menu hidden ≥ 990
  px), so desktop has no account link by the owner's "drawer only" rule — flagged.
- Files: snippets/st-art-alt.liquid f1828780…, snippets/st-landing-map.liquid 8531a36e…, templates/index.json 9e6a7592…,
  sections/st-header.liquid 87bd8f60…, locales/en.default.json 5ea097b3… (all local = remote).
- Theme write lock RELEASED (07:00 UTC) for st-talks. Still pending for a later lock window: hero v3.4 (st-fable's frozen
  hashes).

## 45. Hero v3.4 (HD hand + half-faces) + footer account link — 10 Oct (07:05–07:15 UTC); lock released
- Lock re-granted for the v3.4 install. motion/st-hero-motion.js eb43401d… and motion/st-hero.css 333e3ece… copied
  byte-identical (CONTRACT.md 8c7b049d…, "JSON changes in v3.4").
- Assets (web files, byte-identical): st-hd-preview-hand.webp 35c45151… (510×498), st-hd-green-flag-woman-hero 6040ee63…
  (1201×825), st-hd-shaadi-shift-pin-hero db1ff6ee… (440×457), st-hd-wild-card-woman-hero dab555f5… (282×1021),
  st-hd-wild-card-cards-hand-hero 19f1a6a3… (431×554), st-hd-pinky-promise-face-hero cbcd3588… (254×466); On Me reuses
  st-hd-on-me-woman 428362d2… (same bytes as hd/characters/on-me-woman.web.webp, 535×721).
- snippets/st-motion-map hero_character → HD files with bleed left (On Me, Shaadi, Wild Card, Pinky) / right (Green Flag);
  Brainwave + Diet Cherry unchanged; new field hero_parts (Wild Card: cards-hand-hero 431×554). sections/st-hero: JSON
  character = {src, width, height, bleed} (+ parts) — anchor / widthAt390 dropped; bleed stays an array because the v3.4
  controller does (ch.bleed || []).join(' '); previewHand = {src, 510, 498} (stale slots dropped; the controller doesn't
  read it); the preview hand img = HD 510×498 (preload too); first-paint character = HD On Me 535×721; first-paint parts
  rendered in Liquid when the first set has them (data-st-hero-character-part, reused by the controller).
- Preview (390): JSON parses; previewHand HD; first paint On Me HD, bleed left; stepping the hand through all 7 sets:
  on-me / brainwave / diet-cherry / green-flag (right) / shaadi / wild-card (+ cards-hand part visible) / pinky all load
  their character; the only network failure is Shopify's shop.app pay hop (403, not theme).
- Footer account link (owner: footer optional → add it): MC-094 / MC-095 appended to the legal row on every footer variant
  (same targets as the drawer). Verified: landing / rows / inner footers at 390 and 1280 show "Sign in" (44 px,
  accessible name "Sign in to your account"); 1280 click → "Sign in - Small Talk", back → /collections/all; at 320 it wraps
  to its own line with no leading "·"; scrollWidth = viewport.
- Remote = local: st-hero-motion.js eb43401d…, st-hero.css 333e3ece…, st-motion-map bea2049d…, st-hero 4fabdb14…,
  st-footer 44359445…, + the six webp above.
- Theme write lock RELEASED (07:15 UTC) for st-talks. Next for me: hero v3.5 (batch-B finger tones), HD batch 2 (other
  story heroes + Phase-2 character peeks) when the orchestrator re-grants.

## 46. STAGED LOCALLY, NOT UPLOADED (waiting for the next lock window) — 10 Oct (07:25 UTC)
- st-fable HD1 re-check (qa/fidelity/HD1-PREVIEW-1.md): bottom-cut art anchors to the SECTION bottom. build_landing.py
  `art(..., bottom=N)` → `bottom:calc(N*var(--k))`; Shaadi sweep and the interim Wild Card cards-hand at bottom −4.4
  (their flat cuts sat 32 / 55 px above the section edge because the section box includes the next cap).
- Brainwave beeline over the woman's face: the character had z-index 0 under the beeline (z 1); joins.json says "character
  (beeline passes under)", so the character now takes the default art z 2 (still under the text, z 3).
- Local src/snippets/st-landing-map.liquid c540a943… (remote is still 8531a36e…); joins / st-landing.css unchanged.
  Upload with the next window (plus st-artwork's Green Flag phone and Pinky clasp re-cuts when they land).

## 47. Hero v3.5 STAGED LOCALLY, NOT UPLOADED (waiting for a fresh lock grant) — 10 Oct (07:35 UTC)
- motion/st-hero.css 4a0a9a59… copied to src/assets (JS unchanged eb43401d…; CONTRACT ec8550c7…).
- Assets ready in src/assets (byte copies of the files on disk now; re-check before upload): st-hd-tone-1..4.webp
  3f262e49… / b94c0954… / f408772d… / ca1dab88… (558×1512 — on-disk bytes differ from the manifest's web_bytes, so st-artwork
  may have re-encoded them; take whatever is on disk at grant time), st-hd-brainwave-woman-hero.webp bbdc7760… (299×542),
  st-hd-wild-card-woman-v2-hero.webp b10335aa… (366×1019), st-hd-wild-card-cards-hand-v2-hero.webp 2030ab1b… (362×492).
- st-hero.liquid: swatches #e99a6f / #d18256 / #a25838 / #86472f (first paint tone 2 = #d18256), tone src st-hd-tone-N,
  tone img 558×1512 (JSON finger geometry stays 310×840 / anchor 0.2649 per CONTRACT: same aspect, no geometry change).
  st-motion-map: Brainwave → brainwave-woman-hero, bleed left top; Wild Card → v2 hero + part cards-hand-v2 362×492;
  Pinky bleed → left top (CONTRACT v3.5 table). Local md5: st-motion-map 51751f0d…, st-hero 81ff490b….
- Nail sheets NOT swapped (st-artwork re-normalising first).
- Window order when granted: v3.5 → §46 landing fixes → HD batch 2.

## 48. Lock window 10 Oct (07:20 UTC grant, after st-talks released): hero v3.5 + §46 uploaded
- Grant arrived after my 07:15 release; remote checksums re-fetched before every write (st-talks had edited only its
  own files; en.default.json not touched in this window).
- Hero v3.5 (§47) uploaded as staged: st-hero.css 4a0a9a59…, st-hd-tone-1..4 3f262e49… / b94c0954… / f408772d… /
  ca1dab88… (558×1512), st-hd-brainwave-woman-hero bbdc7760…, st-hd-wild-card-woman-v2-hero b10335aa…,
  st-hd-wild-card-cards-hand-v2-hero 2030ab1b…, st-motion-map 51751f0d…, st-hero 81ff490b… (JS unchanged eb43401d…).
  Preview 390/320: 7 states step, tones switch (HD fingers), Wild Card v2 part renders, Pinky bleeds left top.
- §46 landing fixes went up inside the batch-2 st-landing-map (below).

## 49. HD batch 2 ("chatgpt-AB-1"): landing, Our Vision tile, story heroes — 10 Oct (07:25–07:40 UTC)
- Assets (web files, byte copies): st-hd-brainwave-woman e94cb66e… (299×637), st-hd-diet-cherry-woman 8889d856…
  (557×909), st-hd-diet-cherry-can-hand ac4962b5… (363×646), st-hd-wild-card-woman-v2 097f8589… (773×1022),
  st-hd-wild-card-cards-hand-v2 b812252b… (484×556), st-hd-our-vision-woman 818766db… (549×789).
- Landing (tools/build_landing.py → st-landing-map): Diet Cherry = HD woman (−2, 388, 194.9) + can hand (277.3, 460,
  120.9); Brainwave = HD woman (−2, −2, 164.5; the atlas character and its masks dropped); Wild Card = v2 woman (−8.2,
  419.9, 363.3) + v2 cards hand (174.4, bottom −8.8, 217.8); the interim comment removed. The new pieces are alt="" until
  st-copy's batch-2 alts land (SEO-047 / SEO-050 describe the old art).
- Gallery "Our Vision" tile (st-gallery 19d28546…): card 183 × 263 at (10, 16), #f8e6cb, the HD tile cover-fit when no
  image is picked; alt still section.settings.story_alt (old text) until the batch-2 alt.
- Story heroes (st-article b5f5bd73…): every set except Brainwave (sketchbook still life) = its HD landing scene as a
  window "y0,sh" of the chapter (On Me 440/1067, Diet Cherry 212/675, Green Flag 402/865, Shaadi 312/775, Wild Card
  387/850, Pinky 402/865); title clamp min(62px, 17.8vw) for 320. Diet Cherry and Shaadi leave the top ~40% as set colour
  (their art sits low and full-width) — flagged for st-fable.
- Sheets: qa/fidelity/hd2-landing-390/320 (+ -full), hd2-<set>-390/320, hd2-tiles-*, hd2-story-<set>-*, hd2-story-heroes-*.

## 50. HD batch 2: Phase-2 character peeks → HD — 10 Oct (07:40–08:00 UTC)
- New generator tools/build_peeks.py → src/snippets/st-peek-map.liquid ("src,width,height,left,top,css_width" per
  part pdp / bag / story / guide / avatar and set). Same crop logic as Phase-2 (eye at the board point, eye ≈ 43 css on
  PDP/bag, 56 Our Story, 38 guide; avatar = face centre in the circle, eye ≈ 26), but the HD pieces are cut or feathered
  on one side (they bleed off the page on the landing), so the generator searches zoom m ≥ 1 × eye offset, cost
  (offset / quarter box)² + ((m − 1)/0.2)², over crops where ≥ 99.6% of the box is opaque art (avatar circle 99%). Never
  above source density (worst: Pinky Our Story 1.25 src px per css px). Left-cut faces in right-bleed boxes therefore land
  the eye at x ≈ 40 instead of 70 (the box's left edge = the art's cut edge). Shaadi has no HD face: Phase-2 character and
  its exact Phase-2 numbers. Eye centres measured on the art: On Me (90,392) w100, Brainwave (95,228) w105, Diet Cherry
  (130,525) w175, Green Flag (690,393) w150, Wild Card v2 (95,340) w100, Pinky scene (92,300) w70.
- Consumers switched to the map (CSS fixed widths dropped; width/height = intrinsic): blocks/st-product-notes,
  sections/st-bag-extras, st-our-story (unknown handle → On Me), st-guide ('none' → no peek), st-teaser avatar (rendered
  only when the map has the set). build_landing.py's 'face' field removed; st-landing-map edited by hand (the 'face'
  case only) because a regeneration now picks up st-artwork's Green Flag phone (558 wide) and Pinky scene (904×797)
  re-cuts, which are not installed yet (they need a fresh build_peeks run too: the Pinky eye moves).
- Remote = local: st-peek-map 67580131…, st-product-notes c8cf7263…, st-bag-extras 2ae879c3…, st-our-story 84a04dbb…,
  st-guide a3306b09…, st-teaser f4ee0e0f…, st-landing-map c616c37b….
- Preview (tools/peek_sheets.py, 390 + 320): all 11 peeks load their HD source (Shaadi PDP = Phase-2), Liquid clean, no
  h-scroll, no page errors; densities 1.54–6.93 natural px per css px (Shaadi Phase-2 0.94 as before). The empty bag
  shows its peek (no test cart needed). Sheets qa/fidelity/hd2-peeks-390.png, hd2-peeks-320.png.
- Found at 320: the PDP coda peek (fixed 115 px, now fully opaque art) covered the quote's end and "Read the story".
  Fix (st-product-notes a376bb5f…): quote max-width min(195px, 100vw − 150px), link margin-left clamp(0, 100vw − 290px,
  100px) (both unchanged at 390), peek pointer-events none. Measured: peek left 205 / 260 / 275 vs quote right ≤ 193 /
  219 / 219 and link right 184 / 239 / 254 at 320 / 375 / 390; Playwright actionability click on the link passes.

## 51. HD batch 2 alts (register v1.4.1) — 10 Oct (08:00 UTC)
- SEO-046 / SEO-047 / SEO-050 copied verbatim into snippets/st-art-alt (7b415796…); build_landing.py moves the alt to the
  first DOM layer per the register notes (brainwave-woman, diet-cherry-woman, wild-card-woman-v2; alt="" on the
  sketchbook / can hand / cards hand); st-landing-map fde63c66… (regenerated, then the Green Flag phone and Pinky scene
  img sizes put back to the installed 645×479 / 549×711; joins + st-landing.css byte-identical). LND-012 → index.json
  story_alt (c16cd2c4…).
- Preview 390: the three chapter alts and the Our Vision tile alt read exactly as the register; second layers alt="".
- Theme write lock RELEASED (08:05 UTC). Not done (not in this window): Green Flag phone + Pinky clasp re-cuts (on disk
  in artwork/hd since 00:23 PDT; installing them = copy + regenerate st-landing-map + re-measure the Pinky eye and re-run
  build_peeks), hd/nails, PDP gallery photos.

## 52. STAGED LOCALLY, NOT UPLOADED (11 orchestrator items arrived after my 08:04 release) — 10 Oct (08:05–08:40 UTC)
Waiting for a fresh grant. Remote fetched and diffed at 08:35: every file below is still at my last upload (or 9 Oct
version), the hunks are mine only; the templates are rebuilt on the remote text (Shopify re-serialised them).
- Hero v3.7 (CONTRACT 0ab5b156, CSS 8478b089, JS eb43401d unchanged): st-hd-nails-<set> (7 HD sheets, md5s = FROZEN
  list), st-hd-tone-1..4 q85 (46e50cb6 / 95c7d6a7 / 56f3ae68 / c7fa120a), st-hd-on-me-woman-hero (428362d2),
  st-hd-green-flag-woman-hero-v2 (f551dbef), st-hd-shaadi-shift-pin-hero-v2 (3e3d8e56), st-hd-pinky-promise-face-hero-v2
  (1c6bd0d4), Wild Card v2 hero re-cuts (b1196995 / 8c48f2af). st-motion-map ea5083da (new field hero_sprite →
  st-hd-nails-<key>; 'sprite' stays P1 for st-chapter / st-nail), st-hero 550e8861 (3 sprite lookups → hero_sprite).
  Nail geometry: none in Liquid (the JS doesn't read JSON finger/nailCell); the frozen CSS keeps cell 0.526 per CONTRACT.
- Board-corrections: st-hd-green-flag-phone 6e75d1b9 (558×479), st-hd-green-flag-hand d255e9b7 (511×696, new),
  st-hd-pinky-promise-scene 47142d76 (904×797), st-hd-on-me-woman cc02bb10 (223 px colour fix, alpha identical).
  st-landing-map 78068302: Green Flag woman (alt) < phone (−8, 630.8, 200.9) < hand (103.5, 585, 255.5, manifest
  numbers, pixel-aligned with the woman); Pinky (−8.4, 508, 406.8). st-peek-map 090e07f6 (Pinky eye re-measured on the
  re-fit: (175, 302) w73). On Me story hero unchanged (on-me-woman-hero = the old landing bytes, no better fit).
- Talks SEO (STRATEGY §10): meta-tags 940338dd (thread/topic titles "{x} | the talks | Small Talk" with the blog's own
  title, thread description = body, og:type article on threads, old the-talks articles canonical → /pages/talk/<h>),
  st-seo b3fa9124 (noindex,follow on topics + old articles; no Article/Breadcrumb on old articles; BreadcrumbList Home ›
  the talks › title and DiscussionForumPosting (headline, author alias/Organization, datePublished, text, url; no counts)
  on threads).
- Cards: resource-card 8cc740a0 (no media[1] hover image on any card; ≤352 px cards get a 240/352 srcset),
  predictive-search-products-list 50ba1215 (500 → 352). The hover images were in the header's predictive-search results;
  the shop tiles (st-card, theme-asset packaging) never had them.
- PDP gallery: st-pdp-media 0b16360a (packaging scene → product images in media order, cover at the panel aspect with
  focal point, CDN 375/560/750/1000, lazy, media alt → lifestyle illustration; thumbs shrink to fit; caption),
  product-information 36c86aa3 (setting st_gallery_caption), product(.desi).json dc85bc97 (PDP-019 verbatim).
- Nail Guide photos: st-hd-guide-measure f2420c65 / -apply 3f6850c0 / -remove a577c332 (1125×633), st-guide 3360f1d7
  (photo per step, full frame at column width; old illustration kept as "measure-art"), page.nail-guide.json fef68e6f
  (PG-032 / PG-110 / PG-111 verbatim).
- Our Vision: already installed from hd/tiles (manifest-accepted 549×789); hd/photos/our-vision-woman (1125², not in the
  manifest) not used.

## 53. Window 10 Oct (grant after st-talks' ~08:07 release): §52 uploaded + st-fable HD2 fixes — 08:40–09:20 UTC
- Fresh remote checksums before writing: every target at my last upload / 9 Oct version; the new names absent.
- Added before upload: st-fable HD2 fix 1 (st-article 12438ef3: Diet Cherry story hero = woman (−2, 82, 243.6) + can
  hand (227, 174, 151.1) in the 370-wide card), fix 2 (Shaadi PDP / bag / Our Story / guide peeks from the HD sweep,
  eye (115, 495) w170; the avatar keeps Phase-2), fix 3 (Diet Cherry avatar eye 40, anchor (100, 590)); st-peek-map
  7c6a9988. Also re-copied four st-artwork speck re-encodes that were stale on the theme (same size, alpha identical):
  brainwave-sketchbook 1ac6c6f8, green-flag-woman 28a910ff (the hand layer is pixel-aligned to it), on-me-receipt-hand
  a2229e68, shaadi-shift-sweep b16d9d04.
- Uploaded 45 files (28 webp + st-hero.css + 16 Liquid/JSON), all read back remote = local; then two follow-up fixes:
  st-seo ab099c06 (a thread whose alias is the shop name, e.g. the seed's "small talk", is the Small Talk Organization
  in DiscussionForumPosting, not a Person) and st-pdp-media 274ad76f (the lifestyle illustration was cropped: its 100%
  height resolved to its own 445 px in the auto grid row; now pinned to the slide, contain).
- Preview (tools/w3_verify.py): hero 7 states at 390×844 load the v3.7 characters + st-hd-nails sheets + q85 tones,
  Wild Card part on its state only; Shaadi strip bottom 567/568, 843/844, 931/932 (320×568 / 390×844 / 390×932); PDP
  5 slides (scene, flatlay, hand, moment, illustration), 5 thumbs fit at 390 and 320, swipe updates the thumb, photos
  lazy with srcset 375/560/750/1000 (750 picked at 2×), media alts, PDP-019 caption; shop 7 st-card tiles unchanged,
  0 secondary images, search cards srcset 240/352; guide 3 photos with PG-032/110/111; Diet Cherry story layers at
  (−2, 82, 244) / (227, 174, 151), hand bottom 443 vs card 440; Shaadi PDP peek from the sweep (bag simulated in-page
  from the map: the cart template's campaign is On Me); talks heads: thread title "… | the talks | Small Talk",
  canonical self, indexable, og:type article, DiscussionForumPosting + BreadcrumbList; topic "Plot twists | the talks |
  Small Talk" noindex,follow; old article canonical → /pages/talk/<h>, noindex,follow, no JSON-LD; hub unchanged.
  Liquid clean everywhere; the only console errors are Shopify's shop.app pay hop (403 + its CSP framing).
- Capture note: Playwright's click() scrolls the partly off-screen preview button into view and shifts the overflow-
  hidden hero sideways; a real mouse click / touch tap does not (checked), so the script taps.
- Sheets: qa/fidelity/v37-hero-390.png, v37-hero-shaadi-320x568-390x932.png, v37-pdp-gallery-390/320.png,
  v37-shop-390/1280.png, v37-guide-steps-390.png, v37-story-diet-cherry-390.png, v37-peeks-shaadi.png.
- Theme write lock RELEASED.

## 54. STAGED LOCALLY, NOT UPLOADED: HD nail sheets on every surface + thread author rule — 10 Oct (09:25–09:50 UTC)
Two orchestrator grants arrived after my 09:20 release but were written against the window I had already used and
released (they crossed); per the lock protocol I asked and am waiting for a fresh grant.
- One sprite per set site-wide: st-motion-map 'sprite' → st-hd-nails-<set> (0cef938b; the hero's hero_sprite is the same
  file). Every non-hero surface draws the HD cell x1.058 about the cuticle (50%, 92.5%) on ::before (insets −5.365% /
  −2.9% / −0.435%), so rotation pivots and positions are untouched and plates keep the accepted P1 widths (chapter rows
  69 px). Background-in-box scaling was ruled out: HD tips start at 2.7–3.1% of the cell and would clip.
  - st-landing.css 641101bb: .st-ch__nail (chapter rows), .st-tiles__nail (tiles collage); st-landing-map d031bcc1
    (collage URLs, build_landing.py); st-bag-extras ad3b2fc0; st-nail-closeup 9b85e2f7 (Journal); st-pack-art 1e88b832
    (shop cards); st-pdp-media db30223d (PDP scene); st-nail 5649b4b4 (img cells: scale 1.058, already rotating about
    the cuticle; used by the Our Story packaging block and talks' legacy example block).
  - Not mine: the talks avatars (snippets/st-talk-avatar, st-talk-config; st-talk-* = st-talks' files). Until st-talks
    switches them, talks pages still load the P1 sheet.
  - Read-only pre-flight on the preview (tools/nails_preflight.py --sim: CSS injected + URLs swapped in-browser only):
    qa/fidelity/hdnails-<surface>-390-sim.png, P1 vs simulated HD look the same size; the Journal close-up crop is by
    design in both.
- Thread JSON-LD author per the orchestrator's answer c: Person = the alias, "Anonymous" when blank (st-seo c7b99080;
  replaces the §53 Organization rule for brand seeds from STRATEGY §10).

## 55. Window 10 Oct (grant after my 09:20 release + READY): §54 uploaded — 09:55–10:15 UTC
- Fresh remote diff before writing: the 8 nail files at my last upload / 9 Oct versions, hunks mine only; st-seo at
  ab099c06. Author rule corrected per the grant before upload: alias = the shop's name (trimmed, case-insensitive) →
  Organization "Small Talk"; other alias → Person; blank → Person "Anonymous" (st-seo b40a10cd).
- Remote = local: st-landing.css 641101bb, st-motion-map 0cef938b, st-landing-map d031bcc1, st-bag-extras ad3b2fc0,
  st-nail-closeup 9b85e2f7, st-pack-art 1e88b832, st-pdp-media db30223d, st-nail 5649b4b4, st-seo b40a10cd.
- tools/nails_check.py (fresh profile per page, full scroll): 0 P1 st-nails-* requests on /, /products/bill-idhar,
  /collections/all, /blogs/journal, /blogs/journal/on-me, /cart (1 test item, cleared after), /pages/our-story; each
  loads st-hd-nails-<set> only for the sets it shows. /blogs/the-talks still requests the 7 P1 sheets (st-talks'
  st-talk-avatar / st-talk-config; routed to st-talks).
- Shots (tools/nails_preflight.py 390): qa/fidelity/hdnails-chapters-390.png (7 rows, tips clear of the headlines),
  hdnails-shop-cards / -journal-closeup / -pdp-scene / -bag / -tiles -390.png. Seed thread head: DiscussionForumPosting
  author Organization "Small Talk".
- Theme write lock RELEASED.

## 56. STAGED LOCALLY, NOT UPLOADED: QA report items (qa/sonnet/QA-REPORT.md) + favicon — 10 Oct (10:15–10:45 UTC)
- F3 PDP gallery: track tabindex 0 + aria-label from Horizon's accessibility.slideshow ("Slideshow"), focus ring,
  Left / Right / Home / End move a slide (st-pdp-media 5b328ac8).
- F6 cart: native <table> + <caption>, the invalid role="caption" and redundant role="table" dropped (cart-products
  69166537).
- F8 header: the st-header wrapper is now <header> = the one banner (st-header 29f695d4).
- F9 heading order: shop card titles h2 (st-product-card 1d53577e; the shop grid has no group headings); search: Horizon
  product-title aria-level 2 (product-title 2dc97fa6), grid title h2 (product-grid 7f33842b).
- F10 search filters (1280): each horizontal filter is an <li class="facets__overflow-item"> inside overflow-list's
  <ul> (filters 84b0e454).
- Menu button aria-controls: the target id exists (StMenuDialog-<section>); axe reports any aria-controls on an
  aria-haspopup button as "needs review" (controlsWithinPopup), only at 390 where the button is visible. No change.
- F7 /pages/the-talks: noindex, follow (st-seo legacy handles 2c72d602) + canonical to /blogs/the-talks (meta-tags
  f46d80d4, which also emits og:image over https: QA item 11).
- F5 li.st-talk without a list: rendered by blocks/st-talk-example.liquid (st-talks' file) → orchestrator.
- Favicon: favicon.ico 28505d28, favicon-32 9bacd4f9, favicon-192 d9fa21ec, apple-touch-icon-180 6c8fa10a (md5s =
  orchestrator's list) + 4 links in layout/theme.liquid (75caae2f), only when no theme-settings favicon is set.
- Perf: landing chapter art is already loading=lazy decoding=async (all imgs in st-landing-map); the early fetches are
  Chrome's lazy-load distance on slow links. The 0.61 MB checkout-web prefetch comes from Shopify's
  /checkouts/internal/preloads.js (platform, content_for_header; 137 prefetches), plus shop-js' shop.app pay hop; the
  theme's cart drawer (the only every-page checkout-buttons render) is off (cart_type = page). No theme change.
- Extra (QA F4, not on the orchestrator's list): the hero finger wrapper had aria-hidden="true" around the focusable
  hold button; the frozen CONTRACT DOM has none. Removed (st-hero 0cdfb5b6) — upload only if approved.

## 57. STAGED LOCALLY, NOT UPLOADED: st-fable V37 notes 12–14 (added to the §56 window) — 10 Oct (10:45–11:00 UTC)
- 12/13 set grounds: st-tokens.css must stay byte-identical to spec/tokens.css, so the new tokens live in
  st-brand-styles (592835a2, global): --st-chapter-<set> (landing chapter ground = st-landing.css --g2: on-me #fbbe10,
  brainwave #033bd6, diet-cherry #d40319, green-flag #046f41, shaadi-shift #f30b5e, wild-card #aee60d, pinky-promise
  #6919f9) and --st-art-<set> (campaign illustration ground: #ffb900 / #063df1 / #e10019 / #007947 / #fe0078 / #b7f000 /
  #6620f2). st-article (51206e59): story cards use --st-chapter-<set> (Pinky now violet, not the shop cobalt);
  st-pdp-media (cc0d9e19): the illustration slide's background = --st-art-<set>. --st-tile-* stays the shop's.
- 14a: build_peeks TOP_BAND (Shaadi: the box's top 16 px must be fully opaque) → st-peek-map 0199fda2: PDP top −60 →
  −67 (w 307), bag −75 → −85 (w 382), guide −46 → −49; covers 1.000.
- 14b: st-seo (c43e5192): DiscussionForumPosting interactionStatistic (CommentAction) = the published replies counted at
  render time from the thread's replies list (blank / draft entries skipped, as on the thread page); only when the list
  has ≤ 50 references (all visible without pagination), else omitted. The stored reply_count field is not used.

## 58. Window 10 Oct (grant after §57): QA set + favicon + V37 notes 12–14 + F4 uploaded — 11:05–11:40 UTC
- F4 to st-fable's exact spec (CONTRACT v3.7.1): no aria-hidden on div.st-hero__finger, aria-hidden="true" on
  img.st-hero__tone (st-hero ec47c088). Fresh remote diff before writing: hunks mine only; favicon names new.
- Remote = local (18): st-pdp-media cc0d9e19, cart-products 69166537, st-header 29f695d4, st-product-card 1d53577e,
  product-title 2dc97fa6, product-grid 7f33842b, filters 84b0e454, st-seo c43e5192, meta-tags f46d80d4, layout/theme
  75caae2f, st-brand-styles 592835a2, st-article 51206e59, st-peek-map 0199fda2, st-hero ec47c088, favicon.ico 28505d28,
  favicon-32 9bacd4f9, favicon-192 d9fa21ec, apple-touch-icon-180 6c8fa10a.
- axe 4.10.2 re-run vs qa/sonnet baselines (tools/axe_recheck.py), 0 new violations anywhere; cleared: home
  aria-hidden-focus + region; PDP scrollable-region-focusable + region; /collections/all heading-order + region; cart
  with item aria-required-children + aria-allowed-role + region; search lilac heading-order + region (+ list at 1280);
  search zzzz heading-order + region; /pages/the-talks region (listitem stays: st-talks' block). aria-valid-attr-value
  stays "incomplete" (controlsWithinPopup, by design).
- PDP keyboard: 7 Tabs reach the track ("Slideshow", focus ring); ArrowRight ×2 → slide 3, End → 5, ArrowLeft → 4,
  Home → 1, thumbs follow. Favicon: 4 links, the browser fetches favicon-32 (200), no icon request fails on a fresh
  profile (a bare GET /favicon.ico still 404s; browsers no longer request it). /pages/the-talks: noindex, follow,
  canonical /blogs/the-talks. PDP og:image https. Thread head: DFP author Organization (seed); interactionStatistic
  omitted (all 9 threads have 0 published replies).
- Pinky story card #6919f9 (qa/fidelity/v37-story-pinky-promise-390.png); illustration slides: slide edge = image edge
  colour on all 7 sets (w5-pdp-illustration-slides-390.png); Shaadi PDP / bag peeks without the notch
  (v37-peeks-shaadi.png).
- Theme write lock RELEASED.

## 59. STAGED LOCALLY, NOT UPLOADED: hero v3.7.1 perf package — 10 Oct (11:40–12:20 UTC)
- JS: src/assets/st-hero-motion.js ← motion v3.7.1 f0e35c75 (CSS unchanged 8478b089; CONTRACT aa0818c4).
- Head (layout/theme.liquid): on the home page, before every stylesheet, <link rel=preload as=image fetchpriority=high>
  for the LCP tone and set 1's hero_sprite only. Shopify renders the template before the layout, so the URLs come from
  the hero's data-st-preload-tone / -sprite attributes in content_for_layout. The Caveat font preload is removed
  (Fraunces only). st-hero: the in-section preload_tags (sprite, tone, hand) removed; preview nails style="--col:N"
  only (the JS fills them); preview hand, set-1 character and parts: loading=lazy decoding=async fetchpriority=low.
- Below the hero: every landing img loading=lazy decoding=async fetchpriority=low (build_landing art → st-landing-map
  3c7fabd5; st-gallery; st-teaser incl. image-picker branches). st-landing.css (e91bff09): content-visibility:auto +
  contain-intrinsic-size on every .st-land after the tiles except flow sections (they already clip to their box with
  overflow hidden + the edge mask, so paint containment changes nothing visible; heights are explicit).
- Fonts (tools/subset_fonts.py, fonts/out → src/assets): Basic Latin + NBSP + the copy's © ° · × é – — ‘ ’ “ ” • … ‹ › ₹
  ← → ↗ −, all layout features and variation axes kept: 239,280 → 178,764 B (−25%). barlow 13,280→9,432; caveat
  69,688→59,220 (variable 500–700 kept: 500, 600 and 700 are all used); dm-sans 21,204→15,680; fraunces-700
  16,792→12,172; fraunces-900 16,140→11,556; kalam 12,892→8,896; plex-cond 15,488→10,720; source-serif-500
  18,172→12,296; -700 20,148→14,044; -900 18,376→12,812; -italic 17,100→11,936; the logo face untouched.
- Checkout: nothing on home renders accelerated / dynamic checkout buttons (the only matches are Shopify's head script
  checking for them and a CSS selector); the prefetch is platform preloads.js.
- Open for st-fable: the tiles collage draws 10 nails from all 7 HD sheets as CSS backgrounds (~0.5 MB). The tiles
  section is excluded from content-visibility per the spec and sits at the fold at 390, so those sheets still start
  at first render; options: defer the collage's --st-nails until after load (small script), or accept.

## 60. Window 10 Oct (grant after §59): hero v3.7.1 perf package uploaded — 12:25–13:05 UTC
- Added before upload (grant decisions): the tiles collage waits for the hero tone — spans carry --st-nails-src
  (build_landing → st-landing-map b3dc808e), st-landing.css (ac4b64af) resolves --st-nails only under
  .st-tiles__collage.is-ready with a 0.25 s fade on the nail cells (none with reduced motion), st-gallery (a4da8c91) adds
  .is-ready on the tone's load/error (or if already complete), else window load or 4 s; <noscript> resolves at once.
  st-pdp-media (a9697494): illustration slide img object-position 100% 0 (wrist cut on the right edge).
- Fresh remote diff before writing: targets at my last upload; the fonts were the pre-subset files.
- Remote = local (19): st-hero-motion.js f0e35c75 (CSS stays 8478b089), layout/theme d288deb3, st-hero 99a84197,
  st-landing-map b3dc808e, st-landing.css ac4b64af, st-gallery a4da8c91, st-teaser adb80b12, st-pdp-media a9697494; fonts
  (bytes before → after): barlow 8e9391a4 13,280→9,432; caveat 0d1ba627 69,688→59,220; dm-sans 912db6d8 21,204→15,680;
  fraunces-700 1d5c65ff 16,792→12,172; fraunces-900 d8b99445 16,140→11,556; kalam c8211281 12,892→8,896; plex-cond
  05cabbe1 15,488→10,720; source-serif-500 148b7a73 18,172→12,296; -700 4c67b352 20,148→14,044; -900 ae46d375
  18,376→12,812; -italic 67ff0736 17,100→11,936 (total 239,280 → 178,764).
- tools/w6_verify.py, home at 390, Slow 4G (150 ms, 1.6 Mbps) + 4x CPU, fresh profile: the head's first two preloads are
  st-hd-tone-2 and st-hd-nails-on-me (fetchpriority=high), before any stylesheet; Fraunces is the only font preload.
  First image requests: tone 695→5659 ms and set-1 sheet together, then the lazy/low hero character, preview hand and
  Our Vision tile (in or at the first viewport, so lazy doesn't hold them), then the other 6 sheets from 5819 ms —
  collage .is-ready at 5815 ms, right after the tone. LCP = the tone at 5764 ms (QA's lab had ~8.8 s). Liquid clean, no
  JS errors.
- Font render check (home, PDP, Journal story, talks hub at 390): every visible character of every subset face is in
  its cmap (curly quotes, en/em dashes, ↗ →, …, © · × • exercised); no system fallback. The brand ST faces (not
  subset here) unchanged.
- Illustration slides, all 7 at 390: wrist cut on the right edge, slide ground = image ground
  (qa/fidelity/w5-pdp-illustration-slides-390.png).
- Theme write lock RELEASED.

## 61. STAGED LOCALLY, NOT UPLOADED: owner header fix, official-logo prep, HD packaging prep — 10 Oct (13:10–13:45 UTC)
- Header (st-header 18e22253): .st-logo justify-self start → on phones the logo sits right after the menu button
  (column 2's start, x ≈ 56 at 390); desktop was already left, before the nav. Note: spec/hero.md has the board's logo
  "centred x 137 (35%)" (x 95–179), which the old build matched; the owner's instruction wins, st-fable re-checks.
- Logo (st-logo-mark 99aa6268, new; st-header, st-footer 48b077bd): one snippet renders the mark in the header (box h
  56), drawer (45), landing/rows footer (72) and inner footer (50). Switch logo_kind '' (live text, now) → 'svg'
  (st-logo.svg) or 'webp' (st-logo@2x/@3x.webp) + intrinsic size; the link keeps its visually-hidden name, the image is
  alt="". The theme-settings logo (header) still wins when set.
- Share image (meta-tags b30aeae2): og:image fallback 1200 × 630 where page_image is blank; switch st_og_default ''.
- HD packaging (st-motion-map 2bb290c8 'hd_pack' true for On Me / Diet Cherry / Green Flag / Wild Card / Pinky
  Promise, 'pack_hd' = 960-file size, PLACEHOLDER dims at the old aspect; st-pack-src 9c159680, new: "src|srcset|w|h",
  HD = st-hd-pack-<key>-240/360/480/720/960.webp, else the st-package 1x/1.3x pair). Switched every render site:
  st-pack-art 877b8aec (shop cards + cart lines, box aspect from the source), st-pdp-media cfcf5416 (scene box + thumb),
  st-our-story bd62d2ac (stack), st-package-panel 3b24ac6a (Our Story block; .st-pack--hd lifts the 380 px cap). Sizes
  stay per site (~3x picks 480–720; never above 960). DO NOT UPLOAD the hd_pack switch before the ladder files are in
  the theme; replace the placeholder dims with the delivered sizes first.
- Cards: resource-card 70714035 / predictive-search-products-list b58e868d: small cards request ≤ 480 with a
  240/360/480 srcset (Shopify serves the held sets' 362 px media as is).

## 62. STAGED LOCALLY, NOT UPLOADED: logo strings (copy v1.4.5) + hero v3.7.2 held art — 10 Oct (13:50–14:15 UTC)
- Logo names: st-logo-mark (a1f1757b) owns the link's name, "Small Talk home" (locale small_talk.header.home =
  MC-004): the image's alt when the official file is switched on (MC-096 header + drawer, MC-097 footer), else
  visually-hidden text beside the aria-hidden wordmark. st-header (c97b0240): the extra visually-hidden spans removed;
  a theme-settings logo image's alt is now the same string, not shop.name (MC-096). st-footer (e30e1e1b): likewise.
  Visible effect before the files land: the drawer and footer logo links read "Small Talk home" (was "Small Talk").
  meta-tags (fc1eac25): SEO-110 og:image:alt + twitter:image:alt verbatim, only with the logo fallback image.
- Hero v3.7.2 (CONTRACT f35d1801): st-hero-motion.js ← 4a70f913, st-hero.css ← 2d344ccf; st-hero (22aef77b): the
  first-paint character and the preview hand carry data-st-src (no src, no loading), decoding async, fetchpriority low.
- Our Vision tile (st-gallery f242eb5c, st-landing.css 1ad7daea): img.st-tiles__held with data-st-src; one section script
  now reveals the collage and the tile on the tone's load / error (or at once if complete / no hero), else window load or
  4 s; the tile fades in 0.25 s once loaded (none with reduced motion); <noscript> shows a plain copy and hides the held
  one. Width / height kept, so nothing shifts.

## 63. Early window 10 Oct (grant after §62): hero v3.7.2 + header fix + logo prep — 14:25–15:00 UTC
- Local after §62: st-motion-map hd_pack = true for all 7 sets (owner accepted Brainwave "hai" + the new Shaadi box;
  0ddb0ee3, placeholder dims for all 7) — HELD with the rest of the HD packaging set for the asset window.
- Fresh remote diff before writing: targets at my last uploads; hunks mine only; st-logo-mark new. One staged PUT
  (st-logo-mark) failed with curl 000 and passed on retry (md5-ok).
- Remote = local (9): st-hero-motion.js 4a70f913, st-hero.css 2d344ccf, st-landing.css 1ad7daea, st-logo-mark 02697a07,
  meta-tags fc1eac25 (og fallback inactive: no og:image / og:image:alt on home), st-gallery f242eb5c, st-hero 22aef77b,
  st-header c97b0240, st-footer e30e1e1b.
- Home at 390, Slow 4G + 4x CPU: only st-hd-tone-2 (1188→5514 ms) and st-hd-nails-on-me start before the tone ends; then
  the Our Vision tile (5528), the 6 collage sheets (5543–5562, collage ready 5527) and the hero character (5619). LCP =
  the tone at 5556 ms. Liquid clean, no JS errors.
- Header 69 px at 320 / 360 / 390 / 430 (76 at 1280); logo left at 46 / 52 / 56 / 62 right after the menu button (its
  right edge 45 / 48 / 50 / 53); desktop logo at x 32, before the nav. Hero bottom = viewport bottom (844 at 390×844, CTA
  bottom 816). Wordmark text unchanged ("small talk"); the three logo links' accessible name = "Small Talk home"
  (visually hidden). Shots: qa/fidelity/early-header-390.png, early-header-1280.png.
- Theme write lock RELEASED.

## 64. Asset window 10 Oct (grant after §63): owner-D-1 HD packaging (5 sets), official logo, share image, favicons — 15:05–15:45 UTC
- Files (md5s = the grant's): packaging-hd/<set>-240/360/480/720/<box w>.webp → assets/st-hd-pack-<set>-<w>.webp (25,
  RGBA); logo/small-talk-logo.svg b2979261 → st-logo.svg (single path, fill #001df9, no script / links);
  social-share-1200x630.jpg 0a4dd4d1 → st-og-default.jpg; favicon-logo → favicon.ico 2e06bdb1, favicon-32 7a19d08e,
  favicon-192 de5aad85, apple-touch-icon-180 fd10809e (same names and tags).
- st-motion-map 4a40f6ff: hd_pack true for On Me / Diet Cherry / Green Flag / Wild Card / Pinky Promise (Brainwave,
  Shaadi Shift false until delivered); pack_hd = real boxes 863×1153, 866×1151, 865×1153, 865×1153, 867×1131.
  st-pack-src 498d18d6: ladder 240/360/480/720 + the box width (no 960). st-logo-mark 6d01fbf3: 'svg' 1336×818.
  meta-tags 735828b3: st_og_default = st-og-default.jpg. st-brand-styles 4c728592: --st-logo-blue #001df9 (overrides
  spec/tokens.css's board-sampled #1412d5; follows into --st-icon-ink and --logo-color). Uses of --st-logo-blue:
  header hamburger + bag outline (--st-icon-ink), header logo link + text wordmark (--logo-color), cart bubble, desktop
  nav + drawer link hover / current, footer logo link. Contrast on paper ≈ 8.2:1.
- Fresh remote diff before writing: targets at my last uploads; new names absent. Remote = local for all 42 files
  (31 assets + st-motion-map, st-pack-src, st-pack-art, st-pdp-media, st-package-panel, resource-card,
  predictive-search-products-list, st-logo-mark, meta-tags, st-brand-styles, st-our-story).
- Preview (tools/w8_verify.py): header 69 at 320 / 390 / 430 (76 at 1280), SVG logo 78×48 / 91×56 at x 46 / 56 / 62
  (desktop x 32), alt "Small Talk home"; hero bottom = viewport bottom. Footer logo 118×72. Home og:image =
  st-og-default.jpg 1200×630 + SEO-110 og:image:alt / twitter:image:alt; PDP og:image = the (replaced) HD media. At 390 /
  DPR 3: shop tiles pick st-hd-pack-<set>-360 (~114 css), PDP scene 720 (~200 css), Our Story 720 (180 css), bag line
  (96 css) the cached 720; Brainwave / Shaadi keep st-package (13x). Journal cards carry no packaging (nail close-ups).
  Favicon: 4 links, favicon-32 200 on a fresh profile. No page errors; Liquid clean.
- Shots: qa/fidelity/logo-header-390/1280.png, logo-footer-390/1280.png, hd-pack-shop-390.png,
  hd-pack-pdp-bill-idhar-390.png, hd-pack-pdp-haath-do-main-hoon-390.png, hd-pack-pdp-haan-mera-idea-tha-390.png,
  hd-pack-our-story-390.png, hd-pack-bag-390.png.
- Theme write lock RELEASED.

## 65. HD-box follow-up 10 Oct (grant after §64): Brainwave + Shaadi Shift packaging ladders — ~10:50–11:05 UTC (server)
- Scope as granted: the two ladders + st-motion-map only. Nothing else touched.
- Pre-write: remote st-motion-map 4a40f6ff (= my §64 upload), no st-hd-pack-brainwave-* / -shaadi-shift-* on the remote.
- Assets (copied unchanged from artwork/hd/packaging/<set>-<w>.web.webp, RGBA; no resize / redraw), remote = local:
  st-hd-pack-brainwave-240 070f9981, -360 6181d888, -480 ac96c339, -720 a94c02c7, -867 f61813cb;
  st-hd-pack-shaadi-shift-240 5c8fb08f, -360 651915b7, -480 ad7fa9b9, -720 f4f39c30, -859 feaba423.
- snippets/st-motion-map.liquid 4a40f6ff → f2d5c4b3: hd_pack true for brainwave + shaadi-shift (all 7 sets now true);
  pack_hd brainwave 867,1154, shaadi-shift 859,1136. st-pack-src builds 240/360/480/720/<box width> from it, so no other
  file changed.
- Verify (tools/w9_verify.py, 390 / DPR 3): shop tiles 7 of 7 on st-hd-pack-<set>-360 (~114 css = 3.2x source), all
  loaded; Brainwave PDP scene st-hd-pack-brainwave-720 (201 css, srcset 240…867); Shaadi PDP scene
  st-hd-pack-shaadi-shift-720 (202 css, srcset 240…859); Our Story on-me / brainwave / pinky-promise 720 (180 css).
  Liquid clean on all 4 pages; 0 page / console errors.
- Shots: qa/fidelity/hd-pack-shop-390-w9.png (sticky header unstuck in the test page only), hd-pack-pdp-brainwave-390-w9.png,
  hd-pack-pdp-shaadi-shift-390-w9.png, hd-pack-our-story-390-w9.png.
- Theme write lock RELEASED.

## 66. Micro-window 10 Oct (grant after §65): st-logo-mark header fetchpriority — DENIED, nothing written
- Asked (st-fable's optional tweak, taken by the orchestrator): header logo without fetchpriority="high", still eager,
  width / height / alt kept; drawer and footer unchanged (lazy). An add-on had crossed my §65 release, so I asked for a
  fresh grant first and got it.
- Staged locally: src/snippets/st-logo-mark.liquid 6d01fbf3 → af19ebc8 (`{% unless mark_size == 'header' %} loading="lazy"`
  + a comment). Pre-write: remote 6d01fbf3 (= §64 upload), theme UNPUBLISHED.
- stagedUploadsCreate was refused: "Permission for this action was denied by the Claude Code auto mode classifier.
  Reason: [Modify Shared Resources]." Stopped, no workaround; remote still 6d01fbf3.
- Baseline (tools/w9_priority.py, home 390, Slow 4G + 4x CPU): preloads tone + On Me sheet (high); st-logo.svg High at
  278 ms (what the tweak removes); Brainwave sheet boosted Low → High at 5.3 s (after the tone); favicon-32 High at 10.5 s.
  Liquid clean, 0 errors.
- Theme write lock RELEASED (unused). Needs the user's permission and then a fresh grant.

## 67. Landing redesign (owner, via the orchestrator, 10 Oct) — STAGED only, nothing written, no lock held
- BEFORE (read-only): 56 shots qa/fidelity/before-landing-redesign-*.png at 440x956 / 430x932 / 390x844 / 440x830 /
  430x806 / 390x718 / 1280x800 + content spans (tools/landing_shots.py). At 390x718 only Diet Cherry fitted (612/649);
  On Me was 951/649.
- Staged (details, tables, md5s: qa/staging/landing-redesign-staging.md): note at 50 % centred over the slogan; set name
  700/26 in a highlighter box (true Barlow SC Bold subset, new st-barlow-sc-700.woff2; st-artwork's swipe behind
  name_highlight = false until st-fable approves; quotes as aria-hidden spans, chars from st-copy's keys, blank now);
  one screen per chapter (compact layer in tools/build_landing.py from the board params: ink-measured gaps 8/12/7/8,
  nails 0.88, art re-anchored, On Me art 0.62, Brainwave 0.82, caps > 20 px at 70 %, beelines remapped with dash
  offsets recomputed, svh clamp on --k); st-tokens.css re-synced to spec/tokens.css (st-artwork's name tokens).
- Lab AFTER (tools/landing_lab.py): all 49 chapter x viewport cases fit (tightest Wild Card 645/649 at 390x718), beeline
  clear of notes / ticks / names. Remote bases re-fetched: unchanged since my uploads.

## 68. Landing redesign re-staged to st-fable's final rules (10 Oct) — STAGED only, nothing written, no lock held
- Rules: qa/fidelity/OWNER-LANDING-CHANGE-1.md + addendum, the orchestrator's final values (name clamp(22px, 6.7vw,
  29px)/700, marker approved with no glow on Wild Card / On Me and inset -60% -20% on the dark five, gaps 12/12/10/10,
  budgets 595/675/699), st-copy's name markup (aria-hidden quote spans). Owner device shot saved as
  qa/fidelity/before-landing-redesign-owner-iphone16promax-green-flag.webp; extra BEFORE pass at 440x768 / 430x744 /
  390x664 / 320x568 (before-landing-redesign-svh-*).
- Model: chapter height = max(100svh - header, content minimum) (height + contain-intrinsic-size); stack from the top,
  art absolute from the bottom; --cmin / --cmin2 (art below the nail row; beeline and bottom captions >= 10 board px
  from every glyph box, found by search in tools/build_landing.py); desktop fit min(100svh - header, 900px) with the
  stack centred; the svh clamp on --k from §67 removed (desktop layout kept). Beeline per chapter = top part + vertical
  run + bottom part, assembled for the live height and the dash phase carried by a {% javascript %} in st-chapter.
- On Me: option D staged (pill left, caption beside it), st-fable to confirm. Pinky: scene cropped 115, caption top-right.
- Hero v3.7.3: st-hero.css = motion (40804d86); CONTRACT lists no Liquid/data change.
- Lab (tools/landing_lab.py): 56/56 chapter x viewport cases pass (440x768, 430x744, 390x664, full heights, 320x568,
  1280); dash phase continuous. Staging note with BEFORE/AFTER tables: qa/staging/landing-redesign-staging.md.
  Remote bases re-fetched: unchanged since my uploads.

## 69. Landing window (grant after "ready, requesting lock") — STOPPED at a classifier denial, nothing written to the theme
- Re-staged first to st-fable's last conditions: On Me D as one row (pill 18-178 / 160 wide, caption ink 202-373 on
  the pill's centre line, 24 px apart, name 16 px above; receipt hand 0.46 so all four nails and the slip are above
  the fold at 390x664; Wild Card cap 16 so its curve cuts the wrist just below the fold); Pinky crop 115; the 320 pill
  allowance in CSS; caption clearance on the rotated element box. Lab 56/56, dash phase continuous on all 8 viewports.
- Refund flag (config/settings_data.json, remote 68b06f87, reproduced byte-exact): the local edit was refused —
  "Permission for this action was denied by the Claude Code auto mode classifier. Reason: [Modify Shared Resources]."
  Not staged; remote and local untouched.
- Remote bases re-checked (all as listed). stagedUploadsCreate for 9 files succeeded and the PUTs verified (temporary
  staged storage, not theme files). The next step (reading the local upload list) was refused — "Permission for this
  action was denied by the Claude Code auto mode classifier. Reason: [Auto-Mode Bypass]." Stopped: no themeFilesUpsert.
- Staged md5s: st-landing.css 1871d156, st-landing-map ab8305e5, st-landing-join f48dba2a, st-chapter 80d0fb4c, st-fonts
  027e719c, st-barlow-sc-700.woff2 11ecef9f, st-tokens 8236b819, st-hero 40804d86, st-logo-mark af19ebc8.
- Theme write lock RELEASED (unused). Needs the user's permission decision in this session, then a fresh grant.

## 70. Landing window WRITTEN (grant after §69 release; user approved in this session) — 10 Oct
- Before upload, st-fable's two On Me fixes: caption clamp(22px, 6.4vw, 28px), right-aligned (right ink W-18 +/-2 at
  every width), centred on the pill's line; receipt hand 0.47 raised (4 nails 6-10 px above the fold, slip >= 14 px under
  the caption), Wild Card cap 10 so the wrist cut stays under the join. tools/onme_check.py; lab 56/56.
- Written, remote = local: st-landing.css 10a54aef, st-landing-map c5e2f0fe, st-landing-join d8ee43fa, st-chapter
  80d0fb4c, st-fonts 027e719c, st-barlow-sc-700.woff2 11ecef9f (new), st-tokens 8236b819 (= spec), st-hero.css 40804d86
  (hero v3.7.3), st-logo-mark af19ebc8 (header mark without fetchpriority).
- Refund flag NOT written: staging the settings_data.json key was refused twice — "Permission for this action was denied
  by the Claude Code auto mode classifier. Reason: [Modify Shared Resources]." (The API returns settings_data reformatted,
  so no byte-exact copy; a semantic one-key check was prepared.) Owner can tick it in the theme editor.
- Verified on the preview (tools/landing_shots.py after-landing-redesign, 64 shots): every chapter = one screen at
  440x768 / 430x744 / 390x664 / full heights / 320x568; 1280 stack centred, chapters 753-903; 0 page errors, Liquid clean,
  beeline dash phase continuous at all 8 viewports. Prices ₹ everywhere (tools/price_check.py, test cart cleared).
  Header logo starts Medium (was High); first wave = tone + On Me sheet.
- Theme write lock RELEASED. Next: Pinky closing row (st-fable), Instagram footer icon (D5).

## 71. Pinky closing row (st-fable) — STAGED only, nothing written, no lock held
- Same row as On Me: pill 18-178, caption on the pill's centre line to its right (>= 28 px gap at 390, right ink well
  inside W - 17, -12°, board size; shared CSS rule .st-ch:is(on-me, pinky-promise) .st-ch__caption translate), name 11-12
  px above the caption ink; Pinky cap 12; beeline rerouted down the left edge (12 px clear of the pill) into the scene.
- The scene must keep its full width (art on both image edges). Eye line -> lowest nail = 197 board px, which doesn't fit
  between "8 under the left pill" and the fold at 390x664 (28 px short). Staged option C: clasp whole + eyes clear,
  Pinky 623 / 687 / 703 px at 390x664 / 430x744 / 440x768 (+28 / +12 / +4); options A / B / D sent to st-fable.
- Staged md5s: st-landing.css 6b4fbf75, st-landing-map a5606620, st-landing-join 84a05019. Shots:
  qa/fidelity/staged-pinky-row-lab-{390x664,430x744,440x768,390x844}.png.

## 72. Instagram footer link (D5, owner yes; copy v1.4.8; st-fable placement) — STAGED only, nothing written
- sections/st-footer.liquid e30e1e1b -> bbc6d46e: one ig_icon (outline mark, 24 viewBox, 2-unit stroke, aria-hidden,
  focusable false); every social link target _blank rel "noopener noreferrer", name = social_on + new_tab (MC-098 "Small
  Talk on Instagram (opens in a new tab)"); ink var(--st-talks-ink) #0d0b10, hover .75, 44 x 44. Landing: own row between
  nav and legal (4 px each way), glyph 26. Inner: under the logo in its column (8 px below, left-aligned), glyph 20, nav
  spans both rows. Compact rows: inside the "Sign in" item, 12 px after it (no dot, wraps and centres as a pair), glyph 20.
- locales/en.default.json 722c581c -> c0eb3cb3: one line inserted (small_talk.footer.new_tab = "(opens in a new tab)",
  MC-099); the other 656 lines byte-identical to the remote.
- sections/footer-group.json 73bc7bb7 -> 7e65b40b: social_instagram = https://www.instagram.com/smalltalks_com/ (1 line).
  Pinterest / YouTube / TikTok stay empty (hidden). JSON-LD sameAs not added (st-fable's call, open).

## 73. Instagram window WRITTEN (grant after the request) — 10 Oct
- Written, remote = local: locales/en.default.json c0eb3cb3 (re-fetched first; staged minus the new line = remote
  722c581c), sections/footer-group.json 7e65b40b, sections/st-footer.liquid 70002b3b (re-uploaded once in the window: the
  icon colour lost to `.st-footer a { color: inherit }`, fixed with `.st-footer a.st-footer__social-link`; inner gap 8 ->
  2 px so the logo column ends level with the links).
- tools/footer_check.py at 320 / 390 / 1280: 44 x 44, glyph 26 / 20 / 20, #0d0b10, target _blank, rel noopener
  noreferrer, name "Small Talk on Instagram (opens in a new tab)", overflow 0, Liquid clean, 0 errors. Heights before ->
  after: landing +48 (own row); inner -4 (logo column level with links); compact unchanged.
- Refund flag is now ON (set in the theme editor, not by me): Help shows the Returns topic; refund links -> 200.
- Theme write lock RELEASED. Next: Pinky C + tall-screen composed-max cap + desktop k cap (separate window).

## 74. Pinky C + composed-max cap + desktop k cap — STAGED only (st-fable: LANDING-REDESIGN-ACCEPT-1.md)
- Fix 1: --hc = clamp(content min, 100svh - header, --cmax * k); --cmax = pill bottom + 24 + the highest bottom art's reach
  (pill -> art top 24 px); Pinky's keyed to the clasp (its top <= 48 css px under the caption ink: 41 board).
- Fix 2: at >= 990 one k for every landing section = min(width k, 1.4 px, (100svh - header) / --st-comp) with --st-comp
  = the tallest chapter minimum (623, Pinky); fit min(100svh - header, 900px); the stack centring (--dy) dropped.
- Pinky C as accepted: only art passes the fold (+28 / +12 / +4 at 390x664 / 430x744 / 440x768, 0 at full heights and
  1280); eyes 8-16 px under the pill (6 at 320); clasp whole; beeline >= 12 px from the pill, phase continuous.
- Lab 56/56; full heights: chapters 652-887 of 775-887, pill -> art 24-28 (Green 8-21); 1280: every chapter = the screen.
- tools/landing_shots.py scrolls .page-wrapper when Horizon makes it the scroller (>= 990), for the 1280 captures.
- Staged: st-landing.css dba71bb4, st-landing-map a5606620, st-landing-join 60db0c62 (remote 10a54aef / c5e2f0fe /
  d8ee43fa); st-chapter unchanged (80d0fb4c).
- REVISED (orchestrator: hold fix 2; the owner's whole-store laptop request goes to st-fable's spec): the >= 990 block is
  back to the live rules (fit min(100svh - header, 900px), stack centred, --hc = max(fit, content min)); the composed-max
  cap applies below 990 only; the desktop scale reference is removed. Wild Card's art offset -24 so Pinky's shorter cap
  (36 -> 12) leaves it where it is live. Diff vs live: the other 6 chapters differ only by --cmax (read below 990), Wild
  also by --nc with the compensating art offset; Pinky changes everywhere (its composition is width-scaled).
  Lab 56/56, phase continuous. Staged now: st-landing.css 53ee2e17, st-landing-map cc285a47, st-landing-join 14e60af7.

## 75. Window WRITTEN: Pinky C + fix 1 (fix 2 dropped) + hero v3.8 — 10 Oct (final grant after my last "ready")
- Written, remote = local = granted: st-landing.css 53ee2e17, st-landing-map cc285a47, st-landing-join 14e60af7,
  st-hero.css 8efde4ad (= motion v3.8, desktop composition >= 1024; JS 4a70f913 unchanged). A half-done fix-2 re-enable
  (prompted by a crossed grant) was reverted first; regeneration reproduced the granted md5s.
- Preview (tools/landing_shots.py after-pinky-fix1, .page-wrapper scrolled at >= 990): phones one screen per chapter,
  Pinky +28 / +12 / +4 at 390x664 / 430x744 / 440x768 (art only), 320 +18; full heights capped by --cmax; desktop rules as
  live. 0 errors, Liquid clean, dash phase continuous.
- tools/hero_shots.py (all 7 states, pause after the intro; join shot at >= 990): v3.8 laptop composition as specified at
  1280x720 / 1440x800 / 1536x703, hero box and join unchanged; 390x844 states 2-7 pixel-identical (state 1 caught
  mid-intro in the BEFORE pass).
- Theme write lock RELEASED.

## 76. Window 2 STAGED: chapters desktop (CHAPTERS-DESKTOP-SPEC v1) + fix 2 back at 990-1023 — 10 Oct, lock requested
- Files (local; remote still 53ee2e17 / cc285a47): st-landing.css e0b199db, st-landing-map.liquid 1b703ead. Unchanged:
  st-landing-join 14e60af7, st-chapter 80d0fb4c, st-hero 8efde4ad, st-tokens 8236b819; st-hd-green-flag-woman-hero-v2.webp
  already on the theme (f551dbef, from hero v3.8). settings_data untouched.
- >= 990: fix 2's single k (--kt = min(100cqw/390, 1.4px, (100svh - header)/--st-comp 623)) for every landing section; it
  is the whole layout at 990-1023 and the join unit at >= 1024.
- >= 1024: copy frame right (--cx0, kc <= 1.2, centred on the copy span --ctop/--cspan, generated), art left by --ka,
  pieces anchored per spec section 2 (classes --l / --r with --rx / --f, --dfade, --mob / --desk, --mirror from
  build_landing.py); beelines hidden; joins on --kt. Green Flag: hero-v2 woman mirrored, width
  min(400 ka, (fitd - 24) / 0.965 x 729/1020) so her whole figure stays in the screen (at 400 ka her head was cut,
  top -159..-191 px).
- Right-piece clearance (spec 3.2): --kr = ka reduced until the Diet Cherry can / On Me receipt clears every copy box by
  16 px, beside it or under it, floor 1.0; if 1.0 still collides the copy moves left (--cxs). Copy boxes measured by
  tools/desk_boxes.py (kc 1.0 / 1.1 / 1.2, lab/desk_boxes.json), CSS generated by write_desk_clear_css(). kr at
  1280x720: can 1.226, receipt 1.036; 1366: 1.374 / 1.226; 1440: 1.537 / 1.367; 1536x703: 1.458 (= ka) both; 1024x768:
  1.251 / 1.0 with the On Me copy 100 px left.
- tools/desk_check.py (lab): 1280x720, 1366x768, 1440x800, 1536x703, 1024x768 all OK: chapter = screen under the header,
  copy margins >= 59 / 61, no art over copy, right pieces 17 px, left cuts at the section edge, joins 0, h-overflow 0,
  0 errors; 1000x700 (fix 2) heights and joins OK. Sheets: qa/desktop/lab-w2/desk-sheet-*.png.
- Phones: tools/landing_lab.py 49/49 OK at the 7 phone sizes (dash phase continuous); onme_check rows as before;
  full-page lab renders of the pre-desk build (CSS rebuilt = live 53ee2e17) vs staged are pixel-identical at 390x844,
  320x568, 440x956, 430x744.
- st-fable's V38 asks: the two `after-hero-v38-hero-*-1-settled.png` shots renamed `...-diet-cherry-autoplay.png` (they show
  Diet Cherry); one headed live mid-flight frame by tools/hero_flight.py: qa/fidelity/v38-live-hero-1280x720-midflight.png
  (+ .json: timeline 2110 -> 2627 ms while idle; next-set flyer progress 0.17 before / 0.73 after the shot, 0 errors).

## 77. Window 3a STAGED: store desktop part 1 (STORE-DESKTOP-SPEC v1 section 1: landing cream sections + footer) — 10 Oct
- Files (local, on top of window 2): st-landing.css d9035946 (window 2's e0b199db + the cream block), sections/st-footer.liquid
  624cfbef (remote 70002b3b; one marked block "BEGIN/END store desktop" at the end of its stylesheet). All rules inside
  @media (min-width: 1024px); 990-1023 keeps fix 2, phones untouched.
- Cream sections: page frame min(1240, 100% - 2 x clamp(32px, 4vw, 64px)); copy at 1.15 x the phone board (--kl), groups set
  --k on their own elements so the section keeps --kt for cap / mask / join; height = composition (--hd) + next cap.
  Tiles side by side clamp(300px, 30vw, 420px) (narrower on short screens so they fit), the talks 5/7 (example 1.25 x),
  Journal 5/7 (cards clamp(220px, 22vw, 320px), 182 x 210 cover), Nail Guide 6/6 (copy centred, art figure min(70 %, 520 px)
  hung from its bottom-right cut corner), Shop all + FAQ 4/8. Footer (landing / inner / rows): logo + tagline + socials |
  nav | legal + copyright right-aligned; text links >= 44 px wide.
- Lab = the real preview with the staged CSS swapped in (tools/store_lab.py --after: st-landing.css routed from src/, the
  marked section blocks injected; smooth scrolling off for captures). 1280x720, 1366x768, 1440x800, 1536x703, 1024x768:
  content 65-100 % of the frame (was 39-52 %), nothing key below the fold (was the Journal heading/pill, guide pill, FAQ),
  no target under 44 px (inline answer links exempt), h-overflow 0, 0 errors. Sheets qa/desktop/lab-w3/w3a-sheet-*.png.
- Unchanged below 1024 (preview, reduced motion, full page, all images decoded): 320x568 and 430x932 identical to the
  theme as written; 390x844 identical to one of the live theme's two runtime states (the live theme differs from itself by
  25,808 px there: JS headline bend / beeline assembly race); 1000x700 identical to window-2 staging.
- STORE spec talks hub / thread rows: their CSS is in st-talks-* files (not mine): stopped and told the orchestrator.

## 78. Window 3b STAGED: store desktop part 2 (STORE-DESKTOP-SPEC v1 section 2: store pages) — 10 Oct
- Files (local; remote = my pre-edit copies, re-fetched): sections/st-help 44ab574d -> 93f0c28b, st-journal 6ee1b584 ->
  8c839d30, snippets/st-journal-card ce6df97e -> 392d2a1f, sections/st-article 51206e59 -> 85722bfe, st-our-story bd62d2ac ->
  e01f3bdf, st-404 954db5c7 -> a2d8a6cd (+ the desktop art element), st-bag-extras ad3b2fc0 -> d09ef084,
  blocks/st-product-notes a376bb5f -> 08d6fe1b, sections/st-page 6fb63248 -> e2466020, blocks/_search-input d1e17d08 ->
  2de629ac. Each change is one marked block ("BEGIN/END store desktop") at the end of the file's stylesheet, all rules in
  @media (min-width: 1024px) except the 404 art's base display: none.
- Help: header + search centred at 720, topics 7fr | contact form 5fr sticky (blocks sit in .shopify-block wrappers:
  :has()). Journal index: frame, 2-col card grid (3 >= 1360), featured spans 2 as a horizontal card; cards 16:10 media.
  Story: hero card 5fr sticky (min(100svh - header - 48, 640) tall at 372:442) | story 7fr, 68 ch; st-beats display:
  contents (its JS only measures the track). Our Story: hero 6/6 (title, intro, CTAs | stacked boxes, height-driven),
  values across, eye crop on the screen's left edge. 404: 6/6 + st-hd-on-me-woman-hero mirrored at 360 px on the right
  edge, bottom-anchored. Bag: extras as a 2-card row in the cart's page width, promo nails grow; quantity / title targets
  44. PDP: Horizon half grid overridden to gallery min(58 % of 1200, 720) + details (explicit track: Horizon's margin
  track is minmax(margin, 1fr)); notes links and quantity 44. st-page (the Nail Guide page uses it): header 5fr sticky |
  content 7fr, 18 px, 68 ch. Search: already 4 columns + bar 600 left-aligned; clear button raised to 44.
- Lab (tools/store_lab.py --after, staged CSS + the 404 element on the preview) at 1280x720, 1366x768, 1440x800, 1536x703,
  1024x768: every page's first screen spans the frame with heading + real content side by side, no key heading/CTA
  missing from the first screen, no target under 44 px, h-overflow 0, 0 errors. Sheets qa/desktop/lab-w3/w3b-sheet-*.png.
- Unchanged below 1024: all nine pages full-page pixel-identical (390x844 and 1000x700, reduced motion), staged vs as
  written (test cart via add.js in a throwaway context, cleared).
- Flagged: /pages/nail-guide is on the default page template (st-page), not page.nail-guide (st-guide), so the spec's
  guide layout (peek art, photo steps) has nothing to apply to; assigning the template is a page setting (owner).

## 79. Window 2 v1.1 WRITTEN (conditional grant after my release; all checks passed first) — 10 Oct ~15:45 UTC
- Written, readback = local: assets/st-landing.css 53ee2e17 -> cb9766c9, snippets/st-landing-map.liquid cc285a47 -> e2d0d007,
  sections/st-header.liquid c97b0240 -> 49e3c88b (header "the talks" min(calc(var(--fs-talks) * 0.7), 6.1vw): 34 -> 23.8 px,
  44 px target, centred on the bar). Unchanged: st-landing-join 14e60af7, st-chapter 80d0fb4c, settings_data 3674b780.
  No 3a content (st-landing.css rebuilt from the window-2 snapshot, cream block kept aside).
- v1.1 (CHAPTERS-DESKTOP-SPEC top section): art group in reference px of a 600 px screen, --ua = min(fitd / 600, amax / gw),
  amax = copy ink left - 24; build_landing.py art(dsz=...) writes --dw/--dl/--db (--dt + --dtop for Brainwave's woman) and
  --gw per chapter (478/708/750/494/672/700); kc cap 1.3 and <= (50cqw - 48)/390; cx0 68cqw. desk_boxes.py re-fit over kc
  1.0-1.3 (mid 1.1 / 1.2).
- Lab and post-install preview identical (tools/desk_check.py, .page-wrapper scrolled): 1024x768, 1280x720, 1366x768,
  1440x800, 1536x703 all OK (one screen, copy margins >= 39, left/free pieces >= 25 px, can/receipt >= 17, cuts on section
  edges, joins 0, h-overflow 0, 0 errors); 1000x700 = fix 2 unchanged. Phones: landing_lab 49/49, dash continuous; lab
  full-page pixel-identical to live build at 4 phone sizes; post-install 390x844 vs pre-install: only the header wordmark
  (x 214-314, y 23-47) differs, 0 px below the header band. Liquid errors 0 (/, /pages/help, PDP).
- Shots: qa/fidelity/w2v11-post-<size>-<chapter>.png, sheets w2v11-post-sheet-<size>.png, pre/post 390 renders.
- Font fact-check (owner screenshot): cream type at 390x844 identical with the pre-redesign st-landing.css (06:13), the build
  now and the live MAIN (now 186695155925); the old published copy 186687553749 also renders board sizes. Not reproduced.
- Lock RELEASED.

## 80. Window 3a re-STAGED on window 2 v1.1 with STORE spec v1.1 (owner feedback) — 10 Oct, lock requested
- Files (local; remote re-fetched): assets/st-landing.css cb9766c9 -> d4474a45, snippets/st-landing-join 14e60af7 -> 6bf6d049,
  sections/st-teaser adb80b12 -> 89f2ac82, templates/index.json c16cd2c4 -> b4c1e2fc (talks settings only),
  locales/en.default.json 32104278 -> 79b4547d (one 11-line insertion: small_talk.landing.talks.ago.* + be_first; every
  other line byte-identical), sections/st-footer 70002b3b -> e58c975b. Map unchanged (e2d0d007).
- the talks teaser (v1.1 §1a, phone + desktop): a slice of the real board: heading 66/92, headline 30/42, support line
  15/18 (LND-032), white board card (-1.2/-1 deg) with the first 3 topic chips in the hub's chip order (lowercase via CSS),
  "latest talks" (LND-063), the newest real threads from talk_topic 'all' (2 phone / 3 desktop) via st-talk-avatar +
  st-talk-time (rendered, not edited), "alias · time" + " · n replies" only when n > 0, titles as written, desktop excerpt,
  reply stub (lowercase of TLK-156 "no replies yet"; "· be the first ›" only while posting is on), LND-067 (lowercase of
  TLK-153) while posting is off, CTA "spill your tea ↗" #c3021d (aria "spill your tea on the talks") -> /blogs/the-talks;
  st-talk-ago.js (st-talks, uploaded 15:39Z) with the LND-065 short strings on the board. Every type rule scoped to
  [data-land='talks-teaser']. Phone h 670 (k 1), desktop 5/7 over one screen (CTA 450-501 px from the section top).
- Journal (v1.1 §1b): heading 46/64, two landscape cards 168 x 126 rotated / overlapping, pill; closing line from 1024;
  phone h 378, desktop max(320, fitd / 2).
- Beelines: talks and Journal re-routed in the left gutter (x 6-7 board px), entering/leaving at the old x; dash phase
  continuous at all 7 phone sizes; min distance to content 8.8-13.7 px.
- Tiles, Nail Guide (unchanged on phones), Shop all + FAQ, footer (3 layouts; inner nav links 44 px; link text centred in
  its 44 px target) as in §77.
- Checks: lab teasers at 390x844 / 664, 430x932, 320x568, 1000x700, 1024, 1280, 1366, 1440, 1536; landing_lab 49/49, dash
  continuous; desk_check 42/42 (chapters unchanged); preview A/B with the staged CSS (theme markup unchanged): 390x844 and
  430x932 0 px, 320x568 4 px (antialias), 1000x700 identical to a second render of the live theme (its own noise 11,684);
  store lab tiles/guide/FAQ/footer at 5 sizes: content 65-100 % of the frame, nothing below the fold, no target < 44,
  h-overflow 0, 0 errors. Sheets qa/desktop/lab-w3/w3a-sheet-<size>.png.

## 81. Window 3b re-STAGED with STORE spec v1.2 (pre-install fixes) — 10 Oct, lock requested
- Files (local; remote = my pre-edit copies, re-fetched): st-help 44ab574d -> 93f0c28b, st-journal 6ee1b584 -> 8c839d30,
  st-journal-card ce6df97e -> 392d2a1f, st-article 51206e59 -> 55907346, st-our-story bd62d2ac -> 0f67ae8f, st-404 954db5c7 ->
  a2d8a6cd, st-bag-extras ad3b2fc0 -> d09ef084, st-product-notes a376bb5f -> 08d6fe1b, st-page 6fb63248 -> e2466020,
  _search-input d1e17d08 -> 54dad70a, st-guide 3360f1d7 -> e90abfd4 (new). No 3a file in this set.
- v1.2: On Me story scene window '440,1067' -> '604,1067' (Liquid; fixes the phone hero too: hair-only before); story hero
  at >= 1024 372 x 380, scene bottom-anchored, Diet Cherry layers up 62; Our Story boxes as a fan (--ours-box min(clamp(200,
  19vw, 290), (100svh - header) x 0.62), -0.135 overlap, -7 / +7 deg, z 1/2/3 left to right as the spec text says: the
  prototype had 2/3/1, which would hide box 3's title); st-guide desktop on /pages/nail-guide-desi (page.nail-guide):
  H1 row + peek scaled 1.78 from its top-right corner on the screen edge, steps 6/6 (02 mirrored), quick answers in two
  columns. Search results pinned to the shop's 4 columns from 1024 (Horizon's auto-fill gave 5 at 1440 / 1536).
- Lab (store_lab --after, staged CSS + the 404 element + the On Me window on the preview), 10 pages x 1280x720, 1366x768,
  1440x800, 1536x703, 1024x768: no overflow, no errors, no target under 44 px; heading + real content side by side on
  every first screen. Sheets qa/desktop/lab-w3/w3b-sheet-<size>.png.
- Below 1024 (390x844, 1000x700, full page, reduced motion): every page identical to the theme as written except the
  story's hero card (the On Me window fix, by design: bbox = the hero card).

## 82. Windows 3a + 3b WRITTEN (fresh combined grant after my 3b release; GO for 4 corrected files) — 10 Oct 16:36-16:48 UTC
- Readback = local (remote bases re-fetched first, all as granted): 3a st-landing.css d4474a45, st-landing-join 6bf6d049,
  st-teaser e94cbdb5, templates/index.json b4c1e2fc (parsed = local; list_label / topic_order / cta_aria present),
  en.default.json 79b4547d (insert-only vs 32104278), st-footer e58c975b; 3b st-help 93f0c28b, st-journal 8c839d30,
  st-journal-card 392d2a1f, st-article 55907346, st-our-story 0f67ae8f, st-404 a2d8a6cd, st-bag-extras ee4a011d,
  st-product-notes b13fd203, st-page e2466020, _search-input 54dad70a, st-guide e90abfd4. settings_data 3674b780 and the
  map e2d0d007 untouched; no st-talks file touched.
- Incident: the first st-teaser (granted 89f2ac82) was invalid Liquid (patch cut at the wrong `{%- else -%}`, an 8-space
  match inside a 12-space line left an old Journal fragment); the URL upsert dropped it silently (job done, no
  userErrors) and index.json, saved against the old schema, lost the 3 new settings. Rebuilt from the pre-edit copy
  with an exact line anchor (e94cbdb5: tag balance linted, schema parses, non-teaser parts byte-identical), written
  with the orchestrator's GO, then index.json re-written. Bag / PDP quantity fields were 33 / 37 px on the real preview
  (Horizon rules of equal weight later in the bundle win; the lab injects last): selectors +1 class/attribute (ee4a011d,
  b13fd203, GO), 44 x 44 verified with the rules injected first and then on the real preview. Lesson in memory
  (shopify-url-upsert-silent-failure): lint Liquid before upload, read back every md5.
- Verified on the preview: home 0 Liquid errors / missing translations (also cart, PDP, story, guide-desi); talks teaser
  renders real threads (titles as written, "small talk · 1d" via st-talk-ago.js, "No replies yet" -> lowercase), 2 rows
  phone / 3 desktop with excerpts, chips -> /pages/talks/<topic>, pre-launch line, no "be the first", CTA "spill your
  tea ↗" aria "spill your tea on the talks" -> /blogs/the-talks, old bubble/alias/chip gone; Journal note hidden on phone,
  shown on desktop. teaser_check (390x844, 320x568, 430x932, 1024, 1280, 1366, 1440, 1536) = lab exactly; chapters
  desk_check 42/42, joins 0; store_lab landing + bag + PDP at 5 sizes: no target < 44, h-overflow 0, 0 errors; 3b pages
  at 1280 / 1536 render as staged; On Me story phone hero now woman + receipt, other 6 heroes pixel-identical; bag / PDP
  phone and 1000x700 pixel-identical to pre-install; Nail Guide teaser on phones: all 8 elements identical in geometry,
  type and colour to the live (pre-3a) landing (pixel noise = sub-pixel origin + the beeline's carried dash phase).
- Sheets: qa/fidelity/w3-post-sheet-<390x844|320x568|430x932|1024x768|1280x720|1366x768|1440x800|1536x703>.png.
- Lock RELEASED.

## 83. Owner v12.1 STAGED (st-fable's brief, owner GO with changes) — 10 Oct, lock requested
- Files (local; remote bases re-fetched): assets/st-landing.css d4474a45 -> dd5e8745, snippets/st-landing-map e2d0d007 ->
  2f0b28b7, snippets/st-landing-join 6bf6d049 -> bb05517a, sections/st-chapter 80d0fb4c -> 251b3195; new assets
  st-wild-card-ace.svg 261977b7, st-wild-card-king.svg 3600da98 (st-artwork's artwork/hd/wild-card/cards-*.svg, byte-identical).
- Laptop chapters "here and there" (v12.css): RIGHT for Brainwave / Shaadi / Wild Card from 1024, SPLIT >= 1280 for Diet
  Cherry (st-diet-can, rw 470 / rr -6 / rb -40, gwr 470) and On Me (receipt hand rw 330 / rr -10 / rb -8, gwr 330) as map
  entries (only='wide' + --v12r; excluded from every phone metric); 1024-1279 keeps v1.1 for those two. Shaadi fix:
  sweep bottom calc(fitd x 0.17), to-left 74 % fade intersected with a to-top fade (desk_check: faded bottoms exempt
  from "reaches the chapter end").
- Beeline phone: the current route; build_landing.bee_rebuild (port of st-fable's rebuild()) writes the softened path as
  the no-JS fallback plus data-raw (untouched route); st-chapter's script assembles, then rebuild(pull-in x -> 20 +
  x 350/390, straight runs > 70 -> half-waves amp min(11, 0.035 len)), then the dash pass. On Me / Wild Card corner as
  specified (On Me bot "336,-60.1 L330,0", Wild Card top "M330,0 C330,34 386,58 386,118").
- Beeline laptop: one px SVG per section (.st-beecur, prepended at section level, z 1, 3 px 12/7, cream 2.5 red), the
  data-raw route mapped onto the copy frame +-64 (chapters) / the page frame (cream), smoothstep blend from the previous
  frame over the first 18 %, waves at w/390/1.6, phase period 19; redraw on resize (150 ms), load and fonts.ready.
- Wild Card cards: group .st-land__cards (aria-hidden, imgs alt="", z 2): phone 42k x 58k at 358k / 14k, ace -14, king
  42 % / 9 % 9 deg; laptop clamp(70px, 5.6cqw, 90px), margin-left -cxe, left -0.22 w, top 15 % fitd, ace 16, king 52 % /
  26 % 28 deg (v121.css values).
- Lab: desk_check at 1024 / 1280 / 1366 / 1440 / 1536 / 1680 / 1920 + 1000x700: all OK (warnings: RIGHT layouts' nearest
  piece 24.6-24.7 px from copy); joins 0, h-overflow 0, 0 errors. Phone landing_lab: geometry identical to v1.1 (gaps,
  heights, pill->art); the only change is the beeline's glyph distance (now 0 on 5 chapters: the pulled-in line runs
  behind the headline / pill edges, as in st-fable's OWNER121 render). Longest straight run: phone 60.3 px, laptop 64-66.
  Cards visible: phone 38 px; laptop 113 px (1280) / 135 px (1536) with the spec's values (acceptance asks <= 60: flagged).
- Sheets: qa/desktop/owner-v12/v121-staged-<390x844|1280x720|1536x703>.png (+ -wildcard.png), current | staged.

## 84. Fourth-publish window, staging (10 Oct): lock NOT granted for §83; one window for everything
- Orchestrator review of §83: wrong card files (v1 250x350), laptop beeline crosses copy in the cream sections and
  Pinky (st-fable respeccing; the laptop part is on hold), and the same window must carry hero v3.9, Journal §F and
  Tier A. The phone beeline, phone geometry and laptop chapter layouts stay as staged.
- Cards: the v2 pair (st-fable's pick): artwork/hd/wild-card/st-card-ace-spades.svg e5fa7e59 ->
  assets/st-hd-wild-card-ace.svg, st-card-king-hearts.svg (crowned) fe3db249 -> assets/st-hd-wild-card-king.svg
  (viewBox 46x64); the v1 local assets are removed (they never reached the theme). Map regenerated 2f0b28b7 -> 97514552
  (only the two img src / width / height change). Laptop size still v121.css as given; the <= 60 px check can't pass
  with it (king edge = 1.57 x card width): options sent to st-fable.
- Journal §F (README §F, journal.css / journal.js): snippets/st-journal-card 392d2a1f -> 743a0b79 (campaign art map as a
  `case key`, desktop-only lazy img alt="", >= 1024 card system), sections/st-journal 8c839d30 -> c59a5281 (3 columns
  at every width >= 1024, featured 1 / -1, gap clamp(36px, 3.2vw, 56px) clamp(24px, 2.4vw, 40px), --st-journal-max 1440
  from 1680). Lab tools/journal_lab.py (preview + the two files' desktop blocks + the snippet's image map): phone
  390x844 pixel-identical; 1024 / 1280 / 1536 / 1680 / 1920: 3 + 3, row spread 0, featured 1240x421 at 1536 and 1440x486
  at 1920, cards 453 at 1920, all art loaded and clipped by its media, h-overflow 0, 0 errors. Sheets
  qa/desktop/owner-v12/journal-f1-<WxH>.png. Lab lesson: re-injecting every section's desktop block changes the cascade
  order and fakes a phone diff; inject only the files the batch changes.
- Hero bases re-fetched: st-hero-motion.js 4a70f913, st-hero.css 8efde4ad, st-hero.liquid 22aef77b (= local); v3.9 pending.
- Tier A: asked the orchestrator whether st-fable specs it. Frame hook: the talks sections already read
  var(--pg-max, 1240px) / var(--pg-gutter), so a global --pg-max (st-brand-styles, >= 1680) widens them without touching
  talks files; the other 1240 frames: st-page, st-our-story, st-help, st-guide, st-footer, st-article, st-404, st-journal,
  st-landing.css --pgw and st-chapter's cream frame.

## 85. Fourth-publish window, staging continued (10 Oct): hero v3.9, Tier A, v12.2 Shaadi; no grant, no lock held
- Hero v3.9 (st-fable, frozen): assets/st-hero-motion.js 4a70f913 -> 57b4cad4 (byte-identical to motion/st-hero-motion.js,
  CONTRACT v3.9 548798be); st-hero.css 8efde4ad and st-hero.liquid 22aef77b unchanged. Continuous loop through the 7
  sets, pause by button or tap on the art. Preview check after install: 3 sets + one wrap, tap-to-pause, Shop pill
  navigates without pausing.
- Tier A (orchestrator: mine, defaults approved; guardrails a-d). Insert-only: every file gets one block
  "/* BEGIN wide frame ... */ ... /* END wide frame */" at the end of its stylesheet, all inside min-width 1680:
  st-page e2466020 -> e49e8359, st-article 55907346 -> 6c141cb7, st-our-story 0f67ae8f -> f7400a56, st-guide e90abfd4 ->
  e20ecb03, st-404 a2d8a6cd -> 8729b0b5, st-footer e58c975b -> 69699567, st-help 93f0c28b -> bfb5512d, st-shop c943ff58
  -> 96e26541, and st-landing.css (cream sections' --pgw; gallery tiles).
  - Frame min(1440px, 100% - 2 gutters) from 1680 (the Journal §F rule). Talks pages not included (st-talks' files
    read var(--pg-max, 1240px): one global line would add them; proposed, not done).
  - Help: topics block spans the form's rows, both stretch (509 / 509); the topics list spreads its rows
    (align-content: space-between: <details> rows ignore grid / flex stretch), last divider = Send button bottom
    (852 / 852, was 828); an opened topic packs the rows naturally.
  - Collection: 8 tracks, cards span 2 (card width unchanged), short last row centred (3 of 4 starts half a card in).
  - Gallery: tiles grow to the one-screen height, max 520 (Our Vision art 549 x 789: no upscale), each centred in its
    half of the frame: 54 -> 73.8 % (1680), 47.7 -> 64.6 % (1920), no longer "narrow centre".
  - Reading measure: story and page paragraphs keep their 1240-frame width from 1680 (max-width min(68ch, 680px)):
    characters per line identical to 1536 (story 87, guide 84). Pre-existing: 84-87 cpl already at 1024-1679 (> 75):
    Tier B candidate.
  - Guardrail (a): desk_check output byte-identical before / after (1536 / 1680 / 1920); landing lab before vs after:
    0 px > 16 levels at 1280 / 1536, 1024 0-15 px = render noise (after-vs-after baseline 0); store pages at 1536 with vs
    without the wide-frame blocks: 0 px > 16 levels (help, shop, pdp, journal, our-story, story, guide, guide-desi, 404).
  - Pre-existing upscales (not frame-driven): chapter art at 1920 1.14-1.49x (scales with screen height), pack
    images on shop / our-story / PDP 1.1-1.42x, PDP lifestyle 1.23x.
  - Lab tools: tools/tier_lab.py (store pages), tools/home_tier_lab.py (home), tools/liquid_lint.py (pre-upload lint);
    the lab's tiles mirror now follows st-gallery (HD Our Vision tile, HD collage). Sheets: qa/desktop/tier-a/.
- Owner v12.2 Shaadi full face (st-fable spec; st-artwork asset assets/st-hd-shaadi-shift-woman.webp b81ba5f8,
  780 x 1022 = the source with its 14 empty top rows trimmed, scaled; max shown 705 px at 1920): desk-only dsz piece
  (470 / -6 / -60, --gw 470 via GW_OVERRIDES), mirrored by the RIGHT layout, copy-side fade (to right, transparent 0 ->
  #000 14 %); the sweep is phone-only; the v12.1 Shaadi fix and the v12 sweep fade are removed. Journal card: the
  portrait, 44 / -2 / bottom 2, right-edge fade (st-jcard__char--fade-cut). desk_check Shaadi OK 1000-1920; phone
  Shaadi / On Me / Wild Card pixel-identical to before. Laptop portrait alt="" pending st-copy (SEO-049 describes
  the sweep). st-landing.css -> 8bf08350, map -> 6ecd6760, st-journal-card -> 7b57da99.
- Pending before "ready, requesting lock": st-fable's laptop beeline respec (st-chapter 251b3195 + the .st-beecur CSS
  are the rejected version), st-fable's laptop card offset decision, st-copy's Shaadi laptop alt.

- v12.2 FINAL (st-fable, verified on the ship asset): no mask on the laptop portrait, no fade on the Journal card (the
  asset's inner edge is feathered): both removed. st-copy SEO-111 (register v1.4.12) = the laptop portrait's own alt
  via a new st-art-alt kind 'chapter-desk' (st-art-alt 7b415796 -> 9537572a; generator alt='desk' -> ALT_DESK_TOKEN,
  captured as st_alt_desk); SEO-049 stays on the phone sweep. Now: st-landing.css b81a97f3, map df80575c,
  st-journal-card 7c26e5d5. Journal Shaadi card at bottom 2 % (spec) floats 6 px above the media bottom: asked st-fable
  (-2 %?). Labs serve staged new assets (st-hd-shaadi-shift-woman.webp) from src/assets via page.route (journal_lab
  NEW_ASSETS). Final sheets: qa/desktop/tier-a/*-<1680x1050|1920x1080>.png, owner-v12/journal-f2-*, staged-v122-*.
  Status sent to st-fable and the orchestrator; still waiting: laptop beeline respec, card offset, Shaadi card bottom.

## 86. Fourth-publish window: laptop beeline v12.1d ported, card fan, Journal Shaadi -4 %; READY, lock requested (10 Oct)
- Orchestrator: the three values are in qa/desktop/owner-v12/README.md; don't ship the laptop line off; talks --pg-max
  left alone (the talks UX redesign sets it); Tier B logged (story / page 84-87 cpl at 1024-1679, art upscaling).
- st-chapter 251b3195 -> e2fa76a9: laptop() = st-fable's v12.1c / v12.1d one-line algorithm (beecur.js), ported: data-raw
  routes (verified byte-identical to the remote join paths st-fable's lab read) on content frames (chapters inner +-64;
  cream: probed --pgw, = min(1240, W - 2 gutters) below 1680, the Tier A 1440 frame above), Gaussian 160, copy-cluster
  detours, rest re-smooth 36 + meander 12 / 560, elastic band 420 (copy boxes, art ink alpha > 12, 8 px edge band, 18 px
  clearance), spurs, iron x2 (28; meander 7 / 480 on pass 0), settle (meander 6 / 360), free-end trim, Catmull-Rom every
  32 px, every section's SVG = its slice of one path. Theme-side: the art is read from the images, so the lazy ones are
  fetched first (laptop only, 6 s cap, late loads redraw); a run counter drops stale runs; no debug globals.
- Lab tools/bee_lab.py (lab over http://127.0.0.1:8765 so the art is same-origin; st-fable's accept_bee.js measures):
  1280 / 1536 / 1680 / 1920, all 11 sections: copy / pill clearance 12-152 px (>= 12), 0 samples on art ink (Shaadi's
  portrait, Pinky's sleeve included), straight runs <= 102 px, sharpest turn <= 44.5 deg per 24 px except Nail Guide
  teaser at 1536 49.1 deg (st-fable's own figure 52 there); redraw ~190-390 ms after a resize; 0 errors.
  Shots: qa/desktop/owner-v12/bee-staged-<WxH>.png, numbers bee-staged.json.
- Cards v12.1d (st-landing.css a4d86ff1): group left -0.75 x card width, king 30 % / 22 % / 10 deg: visible king 48 / 57 /
  60 px, ace 30 / 36 / 38 px at 1280 / 1536 / 1920 (= the spec); phone ace 38 px.
- Journal Shaadi card bottom -4 % (README; my 2 % flag): cut below the frame (11 px), no strip (st-journal-card 3c39d76a).
- desk_check 56 / 56 OK (7 chapters x 1000-1920), joins 0; phone chapters pixel-identical (one decode race re-run clean).
- Final set (local <- remote base, re-fetched): st-landing.css a4d86ff1 <- d4474a45; st-landing-map df80575c <- e2d0d007;
  st-landing-join bb05517a <- 6bf6d049; st-chapter e2fa76a9 <- 80d0fb4c; st-hero-motion.js 57b4cad4 <- 4a70f913;
  st-journal c59a5281 <- 8c839d30; st-journal-card 3c39d76a <- 392d2a1f; st-art-alt 9537572a <- 7b415796; st-page
  e49e8359 <- e2466020; st-article 6c141cb7 <- 55907346; st-our-story f7400a56 <- 0f67ae8f; st-guide e20ecb03 <- e90abfd4;
  st-404 8729b0b5 <- a2d8a6cd; st-footer 69699567 <- e58c975b; st-help bfb5512d <- 93f0c28b; st-shop 96e26541 <-
  c943ff58; new st-hd-wild-card-ace.svg e5fa7e59, st-hd-wild-card-king.svg fe3db249, st-hd-shaadi-shift-woman.webp
  b81ba5f8. Unchanged: st-hero.css 8efde4ad, st-hero.liquid 22aef77b. 14 / 14 Liquid lint OK. Snapshot scratchpad window4/.

## 87. Fourth-publish window WRITTEN (10 Oct, grant 19:41:07Z), verified, lock released
- Grant 19:41:07Z (after my release); bases re-fetched 19:42Z: all 16 unchanged, the 3 new assets absent, theme
  updatedAt 16:47:39Z, settings_data 3674b780. Staged uploads (19, saved to file), PUT + public md5 all OK.
- themeFilesUpsert by URL, jobs done, no userErrors, every md5 read back = local:
  assets 19:44:02-04Z: st-hd-wild-card-ace.svg e5fa7e59 (new), st-hd-wild-card-king.svg fe3db249 (new),
  st-hd-shaadi-shift-woman.webp b81ba5f8 (new), st-landing.css a4d86ff1, st-hero-motion.js 57b4cad4;
  snippets 19:44:26-27Z: st-art-alt 9537572a, st-journal-card 3c39d76a, st-landing-join bb05517a, st-landing-map df80575c;
  sections 19:45:01-05Z: st-chapter e2fa76a9, st-journal c59a5281, st-page e49e8359, st-article 6c141cb7, st-our-story
  f7400a56, st-guide e20ecb03, st-404 8729b0b5, st-footer 69699567, st-help bfb5512d, st-shop 96e26541.
  Untouched: settings_data 3674b780, st-hero.css 8efde4ad, st-hero.liquid 22aef77b, templates/index.json b4c1e2fc
  (not reformatted), talks files, every other theme.
- Preview verification:
  - desk_check --preview 1000-1920: 56 / 56 chapter rows OK, joins 0, h-overflow 0, 0 errors.
  - st-fable's accept_bee.py on the installed build: PASS at 1280 / 1536 / 1680 / 1920 (alpha read OK from the CDN):
    min copy 12 / 16 / 12 / 12 px, 0 ink samples, max turn 41.9 / 49.1 (Nail Guide teaser, accepted) / 37.6 / 43.3 deg,
    straight <= 72 / 96 / 96 / 102 px (= the lab numbers).
  - Hero v3.9 (tools/hero_v39_preview.py, 1536 x 703 and 390 x 844): the CDN serves Shopify's minified copy of v3.9 (no
    MAX_SETS); loop On Me -> ... -> Pinky -> On Me (wrap at ~25 s); tap on the art pauses / resumes (aria-pressed and
    label Pause / Play in step); tap on the Shop pill doesn't pause, a real click navigates to /products/bill-idhar;
    pause button toggles; 0 errors.
  - Journal (journal_lab): installed = staged at 1536 / 1920 (3 + 3, spread 0, featured 1240 x 421 / 1440 x 486, all 7
    campaign images incl. Shaadi's portrait load); phone pixel-identical.
  - Tier A (tier_lab 1680 / 1920, installed): help 509 / 509 and divider 852 = button 852; shop last row centred, card
    width unchanged; Journal 86 / 75.2 %; story / guide measure 62 ch (unchanged from 1536); h-scroll 0 everywhere.
  - Home (home_tier_lab, installed vs lab): cream sections and chapters equal to the staged numbers (gallery 73.8 /
    64.6 %); the FAQ reads wider on the preview (the real footer).
  - Phone 390 x 844: beeline paths identical to the lab (dash offsets and lengths, every section); chapters differ from
    the lab only in the nail row (the lab mirror's older nail art) and font rasterisation; Wild Card cards top-right.
- Local test server (127.0.0.1:8765) stopped.

## Open issues (shared data / owner decisions — nothing here was changed by this session) — updated 9 Oct, 12:52
- Payments: no payment provider configured (SD19, owner). Nobody can complete checkout.
- Refund policy body repeats the shipping text (SD25, owner). Theme switch “Refund policy text verified” stays OFF until
  fixed; Returns topic, PG-106, PDP-008, bag Delivery & returns link and footer Refund link stay hidden meanwhile.
- No logo image anywhere (theme logo, Brand settings, Files). Organization/publisher JSON-LD omit "logo" until the owner sets
  one (Settings › Brand or the theme logo); the theme already picks it up.
- Home title/meta still say “Almond”, “Indian moments”, “original illustrated packaging” (G14, owner Preferences).
- Money format “Rs. 599.00” vs boards' ₹599 (SD20, store setting). Shop cards now trim to “Rs. 599” (theme-side); the ₹
  symbol needs the owner's money format change.
- G5 evaluates true: 7 products ACTIVE at board prices (SD7) — owner to confirm intent.
- Diet Cherry package shows a legible “Diet Coke” wordmark (D8; owner-accepted deviation SD17/SD18).
- Legacy pages our-world, nail-guide, contact are still published; noindexed in st-seo until the owner deletes/redirects (SD5).
- nail-guide-desi is thin (heading, line, illustration): interim noindex until G2–G4 guide content is live; SEO-026 gated.
- Gates still held in the theme (one checkbox each once confirmed): G1, G2–G4, G9, G10, G11, G13, G14, G15, G16, D3, D6, D10.
- Not verified: menu drawer focus-in/Escape on a real device (acceptance pass caught it mid-slide). Fonts not subset (0.4).
- Theme Check not run (see item 7). Orphan snippets/st-zz-test.liquid and sections/st-zz-a…e.liquid remain (the API blocks deletes; remove in admin › Edit code).
