# Small Talk — Shopify implementation handoff

Prepared 6 October 2026 · Build, verify, repair, then verify again

## How to give this to her ChatGPT

Upload this file, **Small-Talk-Motion-Sketchboard.png** (or its PDF), the chosen landing/hero design, and the approved shopping and editorial page boards. If possible, also provide the current theme ZIP or repository and approved original product/packaging media. Keep the unchosen designs out of the implementation chat after choosing one.

Send:

> Use the attached Small Talk implementation handoff as your working brief. Our design choice is [Real Women / Desi Ink / Hinglish]. The other attached page boards are approved. Start with Batch 0, inspect the store and your actual access, and then work through the batches. Implement the work you can, test it, fix failures, and keep a short checkpoint. Ask me only for information or access that genuinely blocks the next step. Do not just give me another audit or a plan.

The remainder of this document is the prompt for that ChatGPT. The sketchboard is an engineering diagram, not replacement product artwork. Written requirements below resolve errors in generated design references.

---

## 1. Your role and definition of success

Act as a coordinated senior Shopify theme engineer, mobile performance/QA engineer, technical SEO and answer-content editor, and conversion copywriter. Use the approved UI/UX rather than redesigning it. Apply marketing psychology through clear information, credible product evidence and low-friction shopping; never fabricate reviews, scarcity, results or trust signals.

Build a working, maintainable Shopify store at **https://0nev20-vn.myshopify.com/**. Confirm the current working domain/theme rather than assuming this address is still canonical. The owner is a beginner using ChatGPT and Shopify, with limited time and session allowance. Aim to make the store transaction-ready this week, then improve it over the following two months. Confirm the actual deadline once; older references to dates in our conversation are not a calendar.

Success means real products can be selected, added to a persistent cart and bought through Shopify checkout; the chosen design works on mobile; motion remains smooth without trapping scrolling; the owner can edit ordinary content without source-code changes; content and metadata are saved in the fields the theme actually uses; and an independent final QA pass has repaired and retested material defects. Do not promise a “perfect” site or guaranteed ad return/search visibility.

### Work efficiently

- Inspect available files, tools and access before asking questions. Group essential missing inputs into one short list, offer sensible defaults, and continue independent work.
- Work in a duplicate/draft theme with a backup and change log. Do not overwrite the live theme as a shortcut. Prepare a reviewable preview; publish only with the owner's authorization. Do not change prices, payment settings, domains or paid apps silently.
- Do the work, not just describe it. If a tool cannot write a field or file, supply the exact patch/value and the shortest correct admin steps, then mark it **needs owner action**, not complete.
- Keep one compact Markdown checklist, not an automated dashboard. Columns: task, priority, status, evidence/next action. Statuses: to do / in progress / verified / blocked. Priority: **launch-essential**, **recommended in months 1–2**, **good to have in months 3–6**.
- Batch related changes. At the end of each batch give: changed; tested; blocked; next action. Save a small checkpoint with theme ID/name, file changes, product references, decisions and remaining failures so a new chat can resume without a new full audit.
- For a genuinely necessary manual task, provide a short beginner explanation and a copy-paste continuation prompt. Add one verified official help resource where useful; do not spend sessions assembling a tutorial library.

## 2. Design and product authority

Select exactly one approved hero/landing treatment: **Real Women**, **Desi Ink**, or **Hinglish**. Other page designs are already approved. Do not mix all three or reopen the design process. Fix anatomy, readability, responsive overflow and missing functions within the approved direction.

Authority order: verified actual product/supplier facts and original product media → this written brief for behavior, naming and corrections → chosen final board for composition → older references. If actual product evidence conflicts with a mockup, preserve the actual product and flag the discrepancy. Generated nail images are not proof of the delivered product.

### Locked brand rules

- Blue stacked **small talk** wordmark. Header: menu, left-aligned wordmark next to it, **the talks** in thin black pen-like lowercase lettering, then bag. Desktop adds the approved navigation. Earlier red/bold talks lettering is superseded.
- Premium, expressive, young Indian urban/desi attitude with a kind voice. No public references to campus, college or Masters' Union. Avoid generic cartoon mascots, one recurring ambassador, decorative borders and unrelated clutter.
- Choose the selected board's typography and make it reproducible: real licensed web fonts, a small number of weights, editable live text. If the exact display lettering is custom, use accessible SVG lettering only where necessary, with an equivalent real heading and editable fallback. Confirm Devanagari shaping and mixed-script baselines for Hinglish; do not split a conjunct or matra to force a visual pun. UI and shopping facts stay easy to read.
- Women are distinct, expressive Indian women in the selected photographic/illustrated treatment. Hero appearances are restrained eye/face crops in varied positions, not attached to the main finger. More character is allowed below the hero. No decorative hand may show an incorrect nail set.
- Saturated product-specific colors; modest soft white light behind the nails, not a washed-out background. On Me is rust/mustard yellow, Brainwave cobalt, Green Flag emerald, Shaadi Shift fuchsia, Diet Cherry deep cherry red, Wild Card acid lime, Pinky Promise violet. Shaadi and Diet Cherry must remain clearly different.

### Product–campaign mapping

Find the existing product records before creating anything. Preserve IDs, variants, inventory, approved packaging and existing URLs where practical. These names are distinct from campaign headlines. Prices below are past proposals, **not authority to overwrite actual approved prices**.

| Product | Campaign headline | Nail design to verify against original media | Legacy handle to look up | Earlier price idea |
|---|---|---|---|---:|
| On Me | Bill idhar. | Burgundy; mottled amber tortoiseshell; metallic gold | bill-idhar | ₹599 |
| Brainwave | Haan, mera idea **hai**. | Royal blue, white and silver chrome; no checkerboard | haan-mera-idea-tha | ₹599 |
| Diet Cherry | Haan, wohi wali. | Deep red/burgundy, silver chrome, blush with pointed red French tips | haan-wohi-wali | ₹599 |
| Green Flag | Tum aa jao. Main dekh lungi. | Emerald and blush with pointed green French tips | tum-aa-jao-main-dekh-lungi | ₹499 |
| Shaadi Shift | Dulhan tu. Duty meri. | Pink/red; pink accent with a yellow daisy | dulhan-tu-duty-meri | ₹699 |
| Wild Card | Achha. Tum pehle. | Lime, blush/lime French, blue-and-white checker accent | achha-tum-pehle | ₹699 |
| Pinky Promise | Haath do. Main hoon. | Lilac with deep burgundy asymmetric pointed French tips | haath-do-main-hoon | ₹499 |

Use **Diet Cherry**, not Cherry Repeat. Website Brainwave copy uses **hai**, not tha. Do not alter approved physical package art to match revised website copy. Keep a mapping of product ID, current handle, final display name and campaign reference. If a URL genuinely changes, create and test a redirect.

Specific supporting art: Green Flag keeps the old rotary phone, not an iPhone. Brainwave uses a considered crescent-handbag design sketch, not the robot bee or random machine. Diet Cherry may have a small can held naturally by a hand wearing the verified darker red product nails. Wild Card is a private, hopeful side glance at good cards facing the woman, not a woman showing cards to the viewer. Pinky Promise hands must be anatomically connected and wear the correct tips. These are secondary details; the nail product remains dominant.

### Locked landing sequence

1. Motion hero, normally On Me first; a valid ad-specific entry may open its matching product.
2. A two-image gallery with **Our Vision** → Our Story, and **Shop all nails** → Shop.
3. Diet Cherry product story.
4. **the talks** as its own standout, spacious feature with warm ivory/light contrasting background, thin black handwritten title and “A little less filtered.” No chai cup; no fake live activity.
5. Brainwave product story.
6. Green Flag product story.
7. Journal teaser.
8. Nail Guide as a distinct, clean visual feature.
9. Shaadi Shift product story.
10. On Me product story.
11. Wild Card product story.
12. Pinky Promise product story.
13. Shop all sets, useful FAQs, then complete footer.

The long reference columns are successive crops of **one vertical page**, not horizontal carousels. The seven product chapters appear once each below the hero. At a normal scroll stop, one product world should dominate roughly 70% of the visible area, with only small adjacent hints. Do not shrink three product chapters into one phone screen.

Use 390 × 740 CSS pixels as a comparison canvas for the sketchboard, **not a universal phone size**. Responsive content must fit actual browser space, safe areas, zoom and orientation. Use content-aware minimum heights and small/dynamic viewport units appropriately; never crop critical text/CTA to enforce a 9:16 ratio. Use normal document scrolling. The small curved storyline and beeline lead between chapters, with smoother color joins, readable campaign peaks and visible shop links. Keep the beeline decorative and noninteractive, with an equivalent logical reading order; avoid long sideways/rotated text that cannot be read on a phone.

## 3. Build the Shopify architecture for an owner, not just a developer

Inspect the existing theme first. Keep a sound Online Store 2.0 foundation and extend it. Do not replace it with a headless app or an entire custom monolithic page just to reproduce a screenshot. Custom code is expected for motion; ordinary merchandising must remain editable. [S1–S3]

Implement JSON templates, reusable sections/blocks, section schema and presets, and shared header/footer section groups. Give fields human-readable names and useful defaults. Let the owner reorder, hide and configure landing sections in the theme editor. Preserve standard product forms, app-block compatibility and Shopify behavior. Avoid custom features already handled well by the base theme.

### Source-of-truth and field map

Admin navigation labels can change. Verify the current UI and record the exact path you used rather than pretending every mobile app screen has desktop editor parity.

| Content or function | Store it here | Required rendered use / verification |
|---|---|---|
| Sellable sets, prices, variants, stock, availability | **Products**: actual product and variant records | Product template, collection cards, cart and checkout use those records; no hard-coded duplicate prices or IDs |
| Original packaging, product/detail photos and product video | Product **Media**, attached to the correct product | Working gallery, thumbnails, responsive images, meaningful alt text; inspect each published image |
| Logos, character art, finger bases, nail overlays, preview hands, campaign decorations | Shopify **Files** or appropriate theme assets; merchant-facing image pickers/file references | Owner can replace creative assets without rewriting URLs in JS; brand art is not a fake product record |
| Verified kit contents, shape/length, fit, care, application, reuse facts | Typed product metafields, using standard definitions where suitable | Product accordions and guide snippets consume these fields, with a clear empty-state rule |
| Campaign headline, short/long story, product link, colors, chapter art and motion assets | A campaign metaobject or compact equivalent; product reference plus product metafield reference back | One campaign source feeds hero, landing and PDP story link. Avoid circular rendering or duplicating commerce data |
| Landing order and optional feature visibility | Theme editor sections/blocks with product/metaobject pickers | Owner can move or hide a chapter; missing references fail gracefully |
| Journal | Native **Blog** named Journal and real articles; article metafields/sections for carousel slides if needed | Crawlable article URLs, editable title/body/excerpt/image, carousel text available as HTML, links back to the product |
| Our Story, Nail Guide, Help, the talks shell | Native **Pages** with appropriate JSON templates | Functional routes and editable content; not screenshots with invisible fake buttons |
| Navigation and footer | Shopify menus and editor settings | Shop, Our Story, the talks, Journal, Nail Guide, contact and policy links actually resolve |
| Delivery, returns, privacy, terms | Actual business policies in Shopify's policy settings / correct policy resources | Footer, checkout and relevant PDP links agree; do not invent commitments |
| Checkout | Shopify native checkout and available branding settings | Real checkout handoff. Do not recreate credit-card forms; customization depends on the store's plan |
| Search, filters and sorting | Native theme/Shopify collection and search capabilities | Filters reflect real product attributes; no decorative nonworking controls |

Keep campaign data reasonably small: product reference, headline, note, story, background/foreground/CTA color pair, selected main nail, accent nails, next-preview art, character art/focal point, journal article reference. Put normalized animation anchors in one documented technical configuration, not unexplained offsets spread through seven files. Prevent inaccessible color combinations even when the owner changes a color.

Create an asset register: file name, source/permission, product/campaign, dimensions, role, alt treatment and Shopify destination/reference. Preserve originals; make optimized derivatives. Do not leave assets linked to a temporary ChatGPT URL, expiring download or local path. Audit all nail appearances, including previews, women’s hands, package images and gallery thumbnails.

**Owner-edit test:** In the draft, change a product image and price, edit a campaign headline, replace its decorative art, and reorder/hide a chapter through Shopify UI. Confirm every intended storefront location updates without editing code. Restore test data. Give the owner a one-page “where to edit what” guide; identify actions requiring the desktop website instead of claiming all are available in the mobile app.

## 4. Motion implementation contract

Use **Small-Talk-Motion-Sketchboard.png / .pdf** together with this section. The diagram's coordinates and timings are implementation starting values. Match the chosen final art within this behavior; do not treat sketch silhouettes as production artwork.

### Composition and assets

- One long, natural central finger starts at the hero's bottom edge. Fix its silhouette, scale and cuticle anchor across every product state. Do not make it wider between slides, float it above a control bar or swap differently posed hands.
- Four skin-tone base assets must be registered to the **same pose and canvas**. Tone changes affect the display, not the sellable variant or cart.
- Main nail, base finger, loose accent nails and preview hand are separate layers. Match real product artwork. Normalize nail overlays to a consistent cuticle anchor and scale; retain correct shape and proportions.
- Reserve approximately 24–32 CSS pixels of clear space around the main nail silhouette at the 390-pixel reference width. This is **negative space in the background color**, not a white box. Add a diffused white halo at approximately 8–12% opacity behind the nail/finger. No flashing/strobe effect. Keep small character/prop crops outside this focus zone.
- The next-set preview is a **small relaxed hand entering from the right edge**, in the upper part of the hero. It shows the back of a hand with a natural wrist and fingers reaching inward; not four dangling fingertips from the top. Nails follow each finger's longitudinal direction: cuticle toward wrist, free edge away. Keep the preview's visible width around 20–24% of the hero and its nails much smaller than the main nail. Use the same pose/registration in every state.
- Header, CTA and controls must have stable placements. Place pause and the small circular tone control in the empty lower-right area above the CTA. The tone button has no visible label but an accessible label announcing the selected tone. At least 44 × 44 CSS pixel hit areas, even if the visible circles are smaller.
- Center the main button near the bottom: **Shop “On Me” ↗**, updated with the active product. No hero price. Leave room for safe areas. The arrow is decorative; the whole button is a real product link.

### State order and transitions

Manual cycle: **On Me → Brainwave → Diet Cherry → Green Flag → Shaadi Shift → Wild Card → Pinky Promise → On Me**. The preview always displays the **next** set, not another image of the current set.

Default autoplay visits a maximum of **three products**, normally On Me → Brainwave → Diet Cherry, then stays still. All seven remain manually accessible. A verified ad-matched product may start the sequence at that product; retain the same next-state mapping and three-product limit. Validate any incoming product identifier against the real catalog.

For each product, use the signature nail → one accent from its current loose samples → signature nail again. This gives two quick changes without making the shopper wait through the whole set. For a standard autoplay product, start with this schedule:

| Local time | Motion |
|---|---|
| 0–1,600 ms | Stable signature nail and readable campaign |
| 1,600–1,900 ms | Current-set accent travels from the left sample into the fixed nail anchor; outgoing nail clears the anchor |
| 1,900–2,350 ms | Accent hold |
| 2,350–2,650 ms | Signature nail returns to the same anchor |
| 2,650–3,300 ms | Signature hold; CTA remains usable |
| 3,300–3,900 ms | Next signature nail flies from the right preview into the anchor; background blends smoothly; outgoing nail leaves |
| 3,900–4,000 ms | Settle, then start the next product's clock |

On the third autoplay product, omit the outgoing next-set transition and stop at its signature hold. With this schedule, autoplay settles after about **11.3 seconds** total. These are starting timings to validate for readability and comfort, not a reason to delay first paint. Offer a merchant setting to disable autoplay; reduced-motion preference disables it regardless.

Use real source/target element bounds and normalized cuticle anchors for flights. Translate/rotate/scale the moving overlay into the same receiving point; do not morph the finger itself. Suppress the donor nail layer while it is in flight so two copies are not displayed as one nail. Keep the underlying hand anatomy intact. At transition commit, update the active product, headline, palette, CTA URL and next preview together. During motion, the button must still lead to the product it currently labels. No mismatched purchase destination.

### Interaction and lifecycle rules

| Event | Required behavior |
|---|---|
| Vertical scroll or swipe | Moves the document immediately; never consumes seven swipes or pins the page to finish products |
| Press and hold the main nail | Temporarily pauses motion; release resumes only if autoplay was eligible before the hold |
| Tap/click next preview | Advances one product and enters manual mode; autoplay does not unexpectedly take over |
| Pause control | Explicit pause/resume; labelled state for assistive technology; a deliberate resume starts a fresh finite three-product pass from the current product |
| Tone circle | Cycles four natural skin tones without resetting the product, clock or scroll position |
| Hero leaves viewport / tab becomes hidden | Pause work and retain state; return resumes only if not explicitly paused/manual/reduced-motion |
| Reduced motion | Static initial product, manual next changes without flight; all links and controls still work |
| JS unavailable or an asset fails | Visible server-rendered first product and working CTA; keep the last good state, never a blank hero |
| Shopify editor section unload/reload | Clean up timers, animation frames, observers and listeners; initialize once on re-render |

Implement an explicit state machine with product, nail phase, tone, playback mode and independent pause reasons. Clear a temporary hold on `pointercancel`; do not disable vertical touch scrolling or keep a stale pointer capture. Disable/queue overlapping next actions so rapid taps cannot corrupt state. Do not announce every autoplay change to a screen reader; announce user-requested changes politely.

Prefer light CSS/JS layer animation over a heavy all-page animation framework or seven videos. Render the first state in Liquid/CSS before JS. Load the visible hero promptly; prepare and decode only necessary next assets. If the next asset is not ready, hold the current frame with its valid CTA. Avoid continuously reading layout during animation. Stop offscreen work and respect theme editor lifecycle events. [S4–S5]

## 5. Content, SEO and AEO: write it, install it, inspect it

Write finished copy in small product groups, then enter it in the actual Shopify fields. A spreadsheet or chat response alone is not installation. Keep PDPs concise: product identity, price, useful one-line description, selection/fit help and buying action first; details and campaign story in clear expandable sections.

### Deliverable inventory

| Deliverable | Required content | Destination |
|---|---|---|
| Seven PDPs | Final name, one-line description, short benefits based on evidence, verified kit/fit/care details, short campaign note and linked Journal story | Product description + rendered metafields/template blocks |
| Seven campaign articles | One original small-talk moment per product; short story, four-slide carousel copy, caption and product CTA. Use the approved phrases; label invented narratives as brand storytelling, not customer testimony | Seven actual Journal articles, article carousel data and readable HTML transcript |
| Core pages | Concise Our Story, Shop introduction, Journal introduction, Help copy, the talks introduction/community rules, form/error/empty/success states | Corresponding pages, templates, sections and form UI |
| Practical guides | Verified sizing/fit, application and removal, and care/reuse guidance; combine topics where duplication would be unhelpful | Nail Guide and a small number of substantive Journal guides, linked from PDPs |
| FAQ/answer bank | Direct, factual answers to the shopper questions below, with fact source and confirmation status | Relevant PDP accordions, Nail Guide, Help and selected homepage FAQs |
| SEO/social fields | Unique search title, description, meaningful image alt text and appropriate share image for each core indexable page | Real native fields plus theme output, not an unused custom field |

Keep stories enjoyable and brief; do not pad pages to a supposed SEO word quota. For every factual unknown use **needs supplier/owner confirmation** in the working draft, never a public placeholder or invented claim. Required facts include contents/count, measurements, adhesive, material, wear/reuse conditions, instructions, dispatch/delivery, return eligibility and contact details. Do not manufacture certifications, waterproof claims, allergy assurances or medical advice.

Questions to answer where relevant: What is included? Which shape and length? How do I measure and choose size? What if I am between sizes? Is glue or adhesive included? How do I apply and remove this exact kit? What affects wear time? Can it be reused and how? Can it get wet? Where do you deliver, what does delivery cost and when is dispatch? What happens with a damaged item or a return? How do I get help? Write answers from verified business/product facts and link to the complete applicable policy.

### Installation map and checks

- **Homepage:** Online Store → Preferences → homepage/social sharing SEO fields, confirming current labels. Verify the rendered `<title>`, meta description and social image.
- **Products, collections, pages and blog posts:** their native **Search engine listing / Edit website SEO** fields. Keep SEO titles descriptive while preserving short product names in the shopping UI. Check actual rendered output; avoid duplicate theme/app tags. Around 50–60 title characters and 140–160 description characters are editorial guides, not guaranteed snippet lengths. [S6]
- **Images:** product media's alt-text field for product images; correct image/resource field or section setting for other content images. Check that the Liquid image output uses it. Describe visible product details, not keyword lists. Decorative duplicates use empty alt text and do not repeat the campaign to a screen reader.
- **Article body and carousel:** store real text, headings, image captions and product links. Do not publish a carousel image as the only readable version of a story.
- **Structured data:** inspect existing JSON-LD first. Keep one consistent product representation based on actual variant price/currency/availability and real product URLs/media; add appropriate breadcrumbs, organization and article data as applicable. Do not invent ratings, reviews, GTINs or shipping/return values. Validate rendered markup and fix conflicts with apps. [S7]
- **Technical indexability:** canonical domain/URLs, status codes, redirects, sitemap, robots directives, accidental noindex/password walls, duplicate routes, internal links, real headings and mobile content parity. Keep private account/cart/search-result behavior appropriate; don't indiscriminately index every URL.
- **AEO:** prioritize useful visible answers, original evidence, clear product facts and crawlable internal links. Do not promise AI citations or add hidden answer stuffing. Google does not require special AI markup or `llms.txt`; check current official guidance for any other engine actually targeted. Search Console/Merchant Center steps need the owner's access and verified business details. [S8]
- **Current FAQ caveat:** Google's official update log says FAQ rich results stopped appearing on 7 May 2026. Do not sell FAQ markup as a launch requirement or a route to that feature. Useful visible FAQs still belong on the site. Recheck current documentation at implementation time. [S9]

For every installed content group, record its Shopify resource/field, storefront URL and proof that the value appears in rendered HTML or the relevant image tag. Mark draft-only work separately from saved-and-visible work.

## 6. Make the talks and supporting pages real

The talks is part of the website, not a downloadable app. Keep generous white space and focus on the user's words. Use cute pseudonyms and simple topic/thread/reply flows from the approved boards. Example messages/counts in visual boards are mock content, not existing community activity.

First determine whether an appropriate forum/community backend or approved Shopify app already exists. Liquid plus browser local storage does **not** create shared persistent threads. Implement real persistence, submission feedback and loading/empty/error states through the actual supported service. Never expose an Admin API token in the storefront.

Include report/moderation controls, rate limiting, escaped/sanitized input and practical rules against naming/identifying people, harassment and private information. An alias is not a promise of total anonymity. Do not require or collect unnecessary personal details. Verify access controls and the owner's ability to remove content. If backend access is missing, prepare the exact integration and a clearly labelled moderated-submission MVP; do not call a decorative mock thread “live.” Community must not block checkout readiness.

Our Story, Journal, Nail Guide, Help/contact, search, cart and policies must all work. Preserve native Shopify checkout. Do not leave mock wishlist, filters, heart counts, social icons or contact buttons that imply functions they do not have. Implement the agreed function, link correctly, or flag and remove an unapproved nonworking control from the launch build.

## 7. Technical audit and acceptance matrix

Audit baseline before substantial changes, then independently audit the finished preview. Label every result **observed**, **measured**, **inferred**, or **not tested**. Record URL, theme/version, viewport/device and reproduction steps. Never infer a performance pass from a screenshot.

| Area | Required checks and evidence |
|---|---|
| Theme/source | Inspect actual Liquid, JSON schemas, JS/CSS and dependencies. Run Shopify Theme Check and appropriate syntax/lint checks. Review duplicate IDs, invalid forms/links, CSS collisions, fragile hard-coded data, unused scripts and errors. Preserve required Shopify layout objects/app integrations. |
| Commerce | Every set and valid variant → add → cart → quantity update → remove → refresh/back persistence → checkout. Test out-of-stock, missing selection, invalid quantity, double click and network failure. Confirm image/name/price/variant and totals remain correct. Test discounts, shipping and taxes only against actual settings. |
| Checkout/order | Use native checkout. Test payment/order creation only in an authorized test setup; do not charge a real card. Verify order, inventory and notifications when that access is available. Distinguish reaching checkout from completing an order. |
| Motion | Fixed anchor/pose across all seven products and four tones; correct next-set art; no inverted nails. Test rapid next taps, hold/release/cancel, explicit pause, offscreen/tab pause, reduced motion, slow/missing assets, all three autoplay states and restart behavior. |
| Loading/unloading | Cold/warm load, navigation away/back, browser back-forward cache, resize/orientation, repeated theme-editor section reload/removal and long sessions. Check duplicated listeners, lingering timers/animation frames, memory growth, stale product links and blank frames. |
| Mobile/responsive | Representative widths 320/360/390/430, tablet around 768 and desktop around 1440; vary height too. Real iOS Safari, Android Chrome and Instagram in-app browser where accessible. Emulation is useful but must be labelled as emulation. Test keyboard opening, safe areas, menu/cart drawers, sticky CTA and long text. |
| Accessibility | Keyboard/focus, meaningful link names, form labels/errors, contrast, zoom/reflow, 44-pixel control targets, dialog focus/escape, screen-reader order, reduced motion, pause control, alternative text and correct language support. |
| Performance | Baseline/post-change home, collection and representative PDP. Save comparable mobile Lighthouse/PageSpeed reports; use several comparable runs when judging changes. Record configuration and asset/network evidence, not just a score. Check LCP image loading, layout shifts, long JS tasks and animation work. |
| SEO/content | Check the installed values and rendered HTML for each core page, canonical/robots/sitemap status, valid product/article data, image alt usage and crawlable text/links. Review for leftover “tha,” “Cherry Repeat,” placeholder claims and broken story/product links. |
| Owner editing | Perform the UI edit test in section 3 and repeat the most affected page checks. Changes must persist after preview reload and not require source edits. |
| Analytics for validation | If access exists, verify consent-aware product views, add-to-cart, checkout and purchase events, actual value/currency/product IDs, and Pixel/CAPI deduplication where both are configured. Do not double-install pixels. No ad spend is authorized by this brief. |

Performance targets: good field Core Web Vitals are LCP ≤2.5 seconds, INP ≤200 ms and CLS ≤0.1 at the 75th percentile. Treat these as goals to measure, not promises; field data may be unavailable for a new store. Lab TBT is not a measured field INP. Separate lab results from real-user data. [S10]

Optimize actual bottlenecks: responsive image sizes/dimensions, no lazy-loading of the initial LCP hero, restrained preload use, deferred noncritical scripts, small font payloads/fallback metrics, lazy below-fold media, limited app scripts, no unnecessary full-resolution assets for all seven motion states. Avoid claiming a universal byte budget or a guaranteed Lighthouse score. [S4]

### Checks this handoff has not performed

The design boards were reviewed to prepare this brief. This file is **not a current live-store technical audit or a certificate that the site works**. Reproduce the previously reported missing cart and intermittent/scroll-locked hero rather than assuming their causes or that they remain unchanged.

| Missing evidence/access | What you need to finish the check |
|---|---|
| Full theme source and private configuration | Current theme ZIP/repository, or authenticated theme access with appropriate permissions. Public storefront HTML is not all Liquid/source code. |
| Saved products, metafields, files and theme editor behavior | Authorized Shopify admin/plugin capabilities; a preview URL alone cannot verify every saved field. |
| Real payments, shipping rules, order emails and fulfillment | Authorized test gateway/order workflow and settings access; otherwise explicitly record the untested steps. |
| Real-device Safari/Android/Instagram behavior | Actual device/browser tests; if unavailable, request a short guided owner recording and report emulated tests separately. |
| Field performance and indexing | Sufficient real-user traffic and access to Shopify performance/Search Console as applicable; lab results cannot substitute. |
| Community persistence, moderation and privacy | Actual backend/app access and multi-user tests, not just a theme preview. |
| Supplier claims and exact media accuracy | Original approved product assets and supplier/owner confirmation of specifications and business policies. |
| Pixel/CAPI/consent and purchase deduplication | Relevant Shopify/customer-events/Meta access plus authorized test events. |

If a tool is unavailable, say what it prevents and the smallest way the owner can enable that check. Never ask for passwords in chat; use supported sign-in/connection flows or a theme export.

## 8. Execution batches — continue until launch-ready work is concrete

Use one main implementation chat. Only split a specialist review into another chat when necessary; carry over the checkpoint and changed files. Do not have two chats edit the same theme files concurrently.

| Batch | Work and exit condition | Priority |
|---|---|---|
| 0 — Inspect | Read attachments; identify selected style, current theme, catalog, capabilities and missing facts. Take a short baseline. Prepare draft/backup and a concrete file/data plan. Continue independent fixes while awaiting true blockers. | Launch-essential |
| 1 — Data and purchase path | Real products/media, templates, fit/variant data, cart and native checkout work. Establish source-of-truth field map and factual gaps. | Launch-essential |
| 2 — Editable approved pages | Build selected landing, Shop/PDP/cart, Story, Journal, Guide, Help and navigation using editable sections and references. Match the locked sequence. | Launch-essential |
| 3 — Motion | Implement section 4 and sketchboard. Verify static first paint, stable geometry, finite autoplay, all manual states, natural scroll and graceful failure. Keep a static fallback if motion fails launch gates. | Launch-essential |
| 4 — Copy and discovery | Install seven concise PDPs, core page copy, metadata, alt text, essential factual answers and correct product data. Draft seven campaign articles; publish only finished, fact-checked articles with real assets. Essential fit/care/policy information cannot wait for a blog. | Essentials now; article expansion months 1–2 |
| 5 — the talks | Implement supported real community or clearly scoped moderated MVP. Verify its backend and moderation; do not delay a working shop for speculative community features. | Agreed MVP now; advanced features months 1–2 |
| 6 — Independent QA | Run the matrix. Rank findings by user impact and reproducibility; attach evidence. Fix blockers and material failures, then rerun those tests and affected commerce/motion regressions. Do not stop after producing the defect list. | Launch-essential |
| 7 — Owner handover/launch | Demonstrate editing, list any genuine untested gates, prepare rollback and release notes. Request final publish approval for the actual preview when needed. After authorized publish, smoke-test public URLs, assets, cart and metadata again. | Launch-essential |
| 8 — Validation | In months 1–2, use actual funnel/creative data to improve drop-offs, answer recurring questions and finish useful articles. Months 3–6: optional richer community, additional motion and advanced personalization only if evidence justifies effort. | Recommended / good to have |

For Batch 6, review as if you did not write the code: compare the implementation against this brief line by line. Every failed requirement gets a repair or an explicit reason it is blocked. After repairs, run a second pass for new regressions. Stop optional testing once the agreed gates are sufficiently verified; do not enter an endless redesign/test loop.

The minimal launch gate is reliable buying, accurate products/policies, usable mobile pages, no critical accessibility/navigation defects, correct editable data and essential discovery fields. A graceful static hero is preferable to a broken buying experience while motion is being repaired, but do not silently mark motion complete. Advanced community features and extra campaign volume must not consume the launch week.

### Required final delivery from you

1. Working draft/published URL and theme identity, with what is actually implemented.
2. A short evidence-based pass/fail/blocked checklist, including repair-and-retest outcomes.
3. File/change log, asset/product/campaign mapping, installed SEO/content field register and backup/rollback instructions.
4. One-page owner editing guide and the next prioritized tasks. Separate required owner inputs from optional improvements.
5. A portable checkpoint prompt: “Resume Small Talk from this theme/version and these open items; do not redesign or repeat completed checks.”

Begin Batch 0 now. Keep the first response concise, inspect what is already available, and take the first useful implementation step.

---

## Official implementation references

Checked while preparing this handoff on 6 October 2026. Recheck current documentation during implementation, especially feature availability, APIs and admin labels. Sources support platform guidance; motion timings, composition and work batches are project decisions.

- **S1 — Shopify theme architecture:** https://shopify.dev/docs/storefronts/themes/architecture
- **S2 — Sections and schema:** https://shopify.dev/docs/storefronts/themes/architecture/sections and https://shopify.dev/docs/storefronts/themes/architecture/sections/section-schema
- **S3 — Dynamic sources:** https://shopify.dev/docs/storefronts/themes/architecture/settings/dynamic-sources
- **S4 — Shopify performance:** https://shopify.dev/docs/storefronts/themes/best-practices/performance and https://shopify.dev/docs/storefronts/themes/best-practices/performance/use-section-index
- **S5 — Theme editor lifecycle:** https://shopify.dev/docs/storefronts/themes/best-practices/editor/integrate-sections-and-blocks
- **S6 — Native SEO fields and alt text:** https://help.shopify.com/en/manual/promoting-marketing/seo/adding-keywords
- **S7 — Product structured data:** https://developers.google.com/search/docs/appearance/structured-data/product
- **S8 — Google AI search guidance:** https://developers.google.com/search/docs/fundamentals/ai-optimization-guide
- **S9 — FAQ feature update, May/June 2026:** https://developers.google.com/search/updates
- **S10 — Core Web Vitals:** https://web.dev/articles/vitals
