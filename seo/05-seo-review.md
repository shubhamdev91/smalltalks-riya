# Review of `copy/05-seo.md` against `seo/STRATEGY.md` (Fable, 9 Oct 2026)

Verdict: the register is sound. Wording stays with st-copy (Opus); the items below are rule changes, route decisions and factual corrections it must absorb. Current-state facts were read from the build-theme preview on 9 Oct (see STRATEGY §1/§8).

## Required changes (st-copy)

| # | Rows | Change | Why |
|---|---|---|---|
| R1 | SEO-003, SEO-004 | Shop route is confirmed: `/collections/all`. Change destination to "theme-local (st-foundation) title/meta override in meta-tags for `/collections/all`" (the automatic `all` collection has no native SEO field). Keep the wording. | STRATEGY §1, §6 |
| R2 | SEO-001, 002, 004 and every "seven" | G12 is satisfied: all 7 products are ACTIVE, priced, stocked and render on `/collections/all`. Mark these rows ready (still shared → owner install). | Verified 9 Oct |
| R3 | SEO-005…018 | Add to the current-text column: live shared product SEO titles are "{Set} Almond Press-On Nails \| Small Talk" and metas say "almond press-on nail design… Explore the set and story." for all 7. Note the G14 breach ("Almond") so the owner sees why the replacement matters. Proposed wording unchanged. | §6 |
| R4 | SEO-001, 002 | Same: current shared home title "Small Talk \| Almond Press-On Nails. A Lot Said." / meta "Seven almond press-on nail designs inspired by everyday Indian moments. Explore bold colour stories, original illustrated packaging and little power moves." Record as current text (G14). | §6 |
| R5 | SEO-019 | Drop "The": title becomes "Journal — Stories Behind the Sets \| Small Talk". The nav, H1 and breadcrumb all say "Journal"; one name per destination. Record current shared blog title "Journal \| Small Stories, Big Feelings \| Small Talk". | §4 anchor rule |
| R6 | SEO-021, 022 | Current article titles already follow "{Set}: {Headline} \| Small Talk Journal" and current metas are the first story paragraph. Mark title rows as "matches current"; meta rows stay proposals. Add: article `description` in schema = the same excerpt. | Verified |
| R7 | SEO-025, 026 | Route proposal: final public guide URL `/pages/nail-guide`; `nail-guide-desi` redirects to it (owner, SD5). Until then the row's destination is the `nail-guide-desi` page SEO fields; the old `/pages/nail-guide` is noindexed. Record current `nail-guide-desi` title "Find your fit. \| Small Talk". | §2 |
| R8 | SEO-027, 028 | Help meta may not be installed while Help renders no body. Add a gate note: "install only when the Delivery and Returns topics render (they can link `/policies/shipping-policy` and `/policies/refund-policy`, which exist now) and the contact block is live (G8)". Record current title "Need a hand? \| Small Talk" and current meta (the contact intro). | §8 finding 1 |
| R9 | SEO-029, 030 | Make conditional: "only if the owner keeps `/pages/contact`". Default plan folds contact into Help and noindexes/redirects `/pages/contact` (D6). Record current title "Contact – Small Talk". | §2 |
| R10 | SEO-032 | Current shared meta is the talks form intro ("A little less filtered… Submissions go privately to our team for review…"). Record it. Proposal stands (G10). | — |
| R11 | SEO-033…039 | Packaging alts are accurate to the asset (box with the nail tray visible along the side; the illustration is printed on the box). Add the word "illustrated" so the box art is never read as a photo of hands, e.g. "On Me press-on nail box by Small Talk, illustrated front, with burgundy, tortoiseshell and gold nails in the tray." Keep ≤ 125 chars. Current shared alts exist and must go in the current-text column (e.g. "Bill idhar packaging with an illustrated woman paying the bill and bur…", "Haan, wohi wali packaging with a familiar-drink illustration…"). | §7.1 |
| R12 | SEO-045, 046, 049, 051 | Rewrite to what the accepted chapter art shows (manifest `phase2.checks`): On Me = no bill (brass cups/plate on a table), Brainwave = crescent bag + sketchbook, no blue pen, Pinky Promise = no hands, Shaadi Shift = dupatta, pin not legible. No scene shows nails. Keep the "Illustration:" prefix. The alt must not describe the brief's intent. | §7.2 |
| R13 | SEO-047, 048, 050 | Confirm against the art (can is plain silver, unbranded: pass; rotary phone pink: pass; cards face her, backs to viewer: pass) and remove "nails" claims (no nails visible in any chapter scene). | §7.2 |
| R14 | SEO-041 | Matches the installed contract (`altText` → hidden `[data-st-hero-main-desc]`, hold button `aria-describedby`). Mark as implemented-pending-verification; no wording change. | CONTRACT v2.1 |
| R15 | New rows | Add: (a) `/collections/all` title+meta destination (see R1); (b) 404 page title "Page not found \| Small Talk" (theme-local, locale); (c) `/collections` list page and empty collections → no copy, noindex (reference row); (d) footer link labels "Shipping policy" / "Refund policy" / "Privacy policy" (SEO-0xx, theme-local, G6/G7 satisfied by the existence of the policies; wording of the policies themselves stays owner data); (e) "Contact us" anchor destination `/pages/help#contact`. | §3, §4 |
| R16 | SEO-057, SEO-069 | Destination becomes `/pages/help#delivery` with the Help topics linking the two policy pages. Anchor "Delivery & returns" unchanged. | §4 |
| R17 | Banned list (header of file) | Add "Almond"/any shape word (G14), "India"/"in India" (G6, geography), and "original illustrated packaging" only if the owner confirms the art is original (otherwise drop the adjective). | §6 |

## No change needed

- Title pattern "{Subject} | Small Talk", lowercase "the talks" at title start (SEO-031), Brainwave handle kept (D4), "colours" spelling, Diet Cherry meta alignment, internal anchor set SEO-056…072 (one anchor per destination).
- Decorative alt="" rows SEO-042, 043, 044, 052, 054 match the policy and the installed hero DOM.

## For the orchestrator (not copy)

See STRATEGY §8: empty Help body, duplicate Product schema (C2), schema description spacing, missing Article schema, legacy routes to noindex now and for the owner to delete/redirect (SD5 extended with the five empty collections and `/pages/contact`), footer policy links, missing home og:image, products sitemap recheck, cart double H1 / search no H1.
