# 00 — Small Talk copy register: index, gates, decisions

Copy register v1.3 · 9 Oct 2026 · written by the copy session (sole writer of shopper-visible words). The copy session writes nothing to Shopify. The orchestrator installed the owner-approved shared rows marked “installed”. Shared records (products, metaobjects, articles, pages, menus, SEO fields, policies) need separate review before installation. Theme locale and section settings are theme-local.

Files:
- `01-pdp.md`: product pages (shared slots + 7 sets)
- `02-journal.md`: Journal index, article template, 7 stories
- `03-landing.md`: hero, tiles, chapters, teasers, FAQ, footer
- `04-pages.md`: Our Story, Nail Guide, Help, the talks
- `05-seo.md`: titles/metas, image alt register, internal anchors
- `06-microcopy.md`: header, shop, bag, buttons, validation, 404, search, hero a11y
- `07-talks.md`: **the talks as a real blog** (hub, thread page, Start a talk, house rules, 8 seed threads, SEO). New in v1.3, prefix TLK.
- `FACTS.md`: **the single source for every product, policy and community fact** (F1–F15). New in v1.3.
- `terms-of-service-draft.md`: Terms of service for the owner to paste into Settings → Policies (G16). New in v1.3.

## Columns, IDs, batches (v1.1, per orchestrator protocol)
Every row in files 01–07 has these columns: `id | batch | slot | destination | scope | current text | new text | fact gate | notes`.
- **id**: stable string ID. Builders key placeholders to it. Prefixes: PDP (01), JRN (02), LND (03), PG (04), SEO (05), MC (06), TLK (07). Numbers are never reused. A new row gets the next free number in its file.
- **scope**: `theme-local (st-foundation)` = locale / section setting / template, which st-foundation installs. `shared (owner proposal)` = product, page, article, blog, metaobject, menu, policy or SEO field, which goes to the owner as a proposal only. `theme-local render + shared proposal` = a heading the theme can render locally while the shared field stays a proposal. `shared proposal OR theme-local override (D7)` = the PDP stories. `n/a` = remove or reference only.
- **batch**: B1 hero + landing chapters (+ hero a11y labels, art alts) · B2 PDP + purchase states · B3 shop/bag/guide/help/talks/journal/our-story UI · B4 Appendix B metadata · B5 the talks (real feature).

Row status is generated from the rows at the end of this file (“Slot status, v1.3”).

Gated rows install as **hidden** slots keyed to their ID, never with filler text.

Locked and copied verbatim everywhere: product names, the seven headlines (Brainwave = “Haan, mera idea hai.”), the seven notes, the seven design descriptions, “the talks” lowercase, “Diet Cherry”.

## Fact gates

v1.3: the owner said “This is a new brand and a test store. Produce relevant facts and populate wherever required.” So every text gate is now filled from `FACTS.md`. Only G11 (real product photos, which is art) stays open. Before selling to real customers, the owner checks every “copy default” in FACTS.md against the supplier.

| ID | Fact needed | Blocks | Status (9 Oct) |
|---|---|---|---|
| G1 | Kit contents per SKU: nail count, sizes, adhesive/tabs, tools, printed instructions | PDP “What’s in the kit”; FAQ “What comes in the box?” | **met (owner-directed default, F2)** |
| G2 | Sizing system: sizes included, size chart in mm, measuring method | PDP fit text + “Find your fit” link; Nail Guide step 01 + size chart; FAQ size answer; Guide teaser CTA; Guide/Help SEO | **met (F3)** |
| G3 | Application method, and confirmation that the kit includes instructions | PDP application; Nail Guide step 02 + intro; FAQ apply answer | **met (F4)** |
| G4 | Removal method (and that removal steps are in the kit) | PDP removal; Nail Guide step 03 (incl. “don’t force a nail off”) | **met (owner, F5)** |
| G5 | Live price, availability and active status per product (was DRAFT, ₹0, 0 stock until 9 Oct) | Add to bag / Coming soon / Sold out; every “Shop {set}” CTA; product SEO indexing; quantity-max message. Board prices ₹499/599/699 are mockups. | **met**: 7 products ACTIVE at ₹599/₹499/₹699, stock 10 |
| G6 | Shipping policy: regions, dispatch vs transit time, charges | Help → Delivery; “Delivery & returns” links; footer Shipping; Help SEO | **met**: shipping policy exists (source `policies/Shipping-and-Returns-Policies.md`) |
| G7 | Returns/exchange policy: eligibility, window, process | Help → Returns; “Delivery & returns” links; footer Returns | **met**: refund policy exists (same source) |
| G8 | Working contact channel and whether anyone actually staffs it | Help contact form + success text; “We’re here to help”; bag help block; Contact page + SEO; “Still not sure?” answer | **met**: the owner confirmed store-email messages get answered (email only; phone not confirmed, D10) |
| G9 | Wear time and reuse: substantiated claims | Nail Guide Q “How long do they last?” and “Can I re-use them?” stay **removed** until substantiated | **met (owner, F6, F7)**. Visible copy only; never in metadata |
| G10 | the talks: what happens to submissions (featured or never posted), consent wording, who reads them, privacy wording | Landing CTA “Start a talk” (use “See the talks” until resolved); talks form “Sign it as” / “Send it”; moderation note; the talks SEO meta | **met (owner, F14)**: the talks is a real blog with auto-published replies |
| G11 | Real product photography verified for each set (vs illustrations) | Packaging alts; FAQ “Are the illustrations what I’ll get?”; PDP illustration caption; Our Story packaging alt | open for photos; packaging alts checked against the packaging asset 9 Oct, owner hi-res awaited |
| G12 | All seven sets visible/live (copy says “seven”) | Home/Shop metas; Our Story intro; Journal subheading; Shop handwritten line; FAQ “Which set?”; bag empty-state line; hero “Set n of 7” | **met**: all seven sets live |
| G13 | Whether orders can be changed after placing, and how | Help → Orders | **met (owner, F12)**: the Orders topic is unhidden |
| G14 | Nail shape/material per SKU (packaging prints “ALMOND PRESS-ONS”) | Any shape/material word in copy (currently none used) | **met (owner, F1)**: almond. Metadata change is st-fable’s call |
| G15 | Tax display (GST included in price or not) | Bag subtotal note | **met (owner, F9)**: prices include GST |
| G16 | Legal entity name; Terms/Privacy policy text | Footer copyright; footer Terms/Privacy links | **met once the owner pastes** `terms-of-service-draft.md` (F15) |

## Owner decisions (not facts; a choice someone has to make)

| ID | Decision | Recommendation / status |
|---|---|---|
| D1 | Keep the Everyday/Statement shop filters? (provisional merchandising) | **Resolved 9 Oct: keep (board T22).** The set assignment is a product-tag decision. |
| D2 | the talks filter chips (All · Plot twists · Tiny wins · Nail talk) | **Resolved v1.3:** keep. The talks has real threads, and the chips are real article tags (TLK-005/006). |
| D3 | the talks rule 4: “talk to someone you trust or a local helpline” and whether to link a named helpline | **Resolved 9 Oct:** Tele-MANAS (14416 / 1800-891-4416, free, 24×7), checked against PIB/MoHFW (TLK-077). |
| D4 | Brainwave handle `haan-mera-idea-tha` contains “tha” | Out of copy scope; any handle change/redirect is a separate shared-data decision. The copy never uses “tha”. |
| D5 | Which social accounts exist (Instagram, Pinterest, YouTube, TikTok on board) | **Resolved 10 Oct: Instagram confirmed**: @smalltalks_com, https://www.instagram.com/smalltalks_com/, icon link in both footers (LND-061, MC-098/099). No other accounts are confirmed, so those icons stay hidden. |
| D6 | Duplicate routes (`/pages/contact` vs Help contact; `nail-guide` vs `nail-guide-desi`; `our-story` vs `our-world`; Journal tags) | One destination each. Plan per `seo/STRATEGY.md` §2: guide → `/pages/nail-guide` (meanwhile `nail-guide-desi`), contact → `/pages/help#contact`, `our-world` and `/blogs/news` and the five legacy collections noindexed, then deleted or redirected by the owner (SD5). SEO-029/030 apply only if `/pages/contact` is kept. |
| D7 | PDP story: theme-local PDP override vs edit shared `small_talk_campaign.story` (it feeds other surfaces) | **Resolved 9 Oct: theme-local override (installed).** |
| D8 | Boards 3 and 5 show a real cola trademark (“Diet Coke”) on the Diet Cherry can | Chapter can is now plain and unbranded (pass). **Still open for packaging:** the approved Diet Cherry box front shows a legible “Diet Coke” can (`artwork/tests/contact-packaging.png`). Physical packaging is locked, so this is an owner/legal call; no alt or copy names the brand. The Brainwave box reads “Haan, mera idea hai.” (owner decision 10 Oct: real printed box + HD box; the old “tha” exception is retired). |
| D9 | PDP bookmark/wishlist icon on board 5 | **Resolved 9 Oct: a real Save toggle, stored on the visitor’s device (board T23).** Labels in PDP-055…058. |
| D10 | Show the phone number from the policies on the Help contact block? | **Decided 9 Oct: email only.** No phone number on Help (PG-107). |

## Slot status, v1.3 (generated from the rows)

Status meanings: **ready** = install after normal review. **installed** = already in Shopify (owner-approved). **gated** = waits on a fact (only G11, art). **needs owner decision** = waits on a D-choice. “Dropped / superseded” rows stay in the file so their IDs are never reused.

| file | scope | status | rows |
|---|---|---|---|
| 01 | n/a | dropped / superseded / reference | 2 |
| 01 | shared | ready | 28 |
| 01 | theme-local | gated | 1 |
| 01 | theme-local | ready | 27 |
| 02 | shared | installed | 43 |
| 02 | shared | ready | 2 |
| 02 | theme-local | ready | 18 |
| 03 | n/a | dropped / superseded / reference | 8 |
| 03 | shared | ready | 9 |
| 03 | theme-local | ready | 45 |
| 04 | n/a | dropped / superseded / reference | 43 |
| 04 | shared | installed | 4 |
| 04 | theme-local | gated | 1 |
| 04 | theme-local | ready | 60 |
| 05 | n/a | dropped / superseded / reference | 6 |
| 05 | shared | installed | 32 |
| 05 | shared | ready | 3 |
| 05 | shared | ready, not installed (owner step or gate) | 4 |
| 05 | theme-local | ready | 43 |
| 06 | shared | ready | 8 |
| 06 | theme-local | ready | 85 |
| 07 | n/a | dropped / superseded / reference | 1 |
| 07 | shared | ready | 15 |
| 07 | theme-local | ready | 54 |

**gated:** PDP-019 (G11); PG-013 (G11)

**ready, not installed (owner step or gate):** SEO-001 (Status: NOT installed. Online Store pref); SEO-002 (Status: NOT installed. Online Store pref); SEO-029 (Status: not installed (D6). R9. Conditio); SEO-030 (Status: not installed (D6). R9. Conditio)

total 542

## Things I changed from the boards or Appendix A, and why (quick review list)
1. Brainwave PDP: “cobalt-tipped finger” → “cobalt nail” (Brainwave has full cobalt nails, not tips).
2. Wild Card PDP: “lime and blue checks” → “acid lime and blue-white checks” (the checks are cobalt and white).
3. Pinky Promise PDP: “No need to rush her” → “Koi jaldi nahi.”; On Me PDP: removed “That’s all the explanation it needs” → “Bas. No speech needed.”
4. Captions: Diet Cherry “New plans” → “New place”; Green Flag “Bring yourself” → “Just come over”; Wild Card “Cards down” → “Cards close” (cards stay private).
5. Board label fixes: “Our Vision” → “Our story”; “Shop all nails” → “Shop all sets”; “Join the conversation” → “Start a talk”; “Post” → “Send it”; “Same nails. Different moods.” → “Seven sets. Seven moods.”
6. Removed fabricated activity from the talks board (reply counts, timestamps, hearts, reply box) and @handles (aliases now have no @).
7. Removed wear-time and reuse questions from the Nail Guide; removed the “Supplier measurements required” note (internal, not public).
8. Appendix B: the talks meta rewritten (no implied activity); title lowercase “the talks”; Diet Cherry meta aligned; Home meta fixed (“cobalt checks” was inaccurate); Nail Guide meta tightened.

## v1.2 changes (9 Oct), by destination
Source of each change: st-fable review R1–R17 (`seo/05-seo-review.md`), orchestrator state changes (G5, G6, G7, G8, G12 met; D7 resolved; owner-approved installs), accepted art (`artwork/tests/contact-*.png`, manifest `phase2.checks`), policies (`policies/Shipping-and-Returns-Policies.md`).

**Theme-local (st-foundation)**
- New rows: PG-105, PG-106 (policy links), PG-107 (Help email line), SEO-073 (404 title), SEO-075…078 (footer labels), SEO-079…085 (lifestyle alts).
- New text: LND-043 (guide teaser alt), LND-060 (footer link set), PG-032 (guide alt), PG-038, PG-039, PG-042, PG-046, PG-047 (Help Delivery/Returns/Orders, from the policies; moved from page body to section blocks because the Help body is empty), SEO-045…051 (chapter alts).
- Destination/scope only: PDP-024, 029, 034, 039, 044, 049, 054 (stories → theme-local override, D7); SEO-003, SEO-004 (`/collections/all` override, R1); SEO-057, SEO-069, SEO-070 (anchors → `/pages/help#delivery` and `#contact`).
- Unlocked (gate met, wording unchanged): PDP-008, 011, 012, 013; JRN-002, 011, 019, 025, 031, 037, 043, 049, 055; LND-009, 013 (still G11), 023, 057; PG-031, 034, 037, 040, 041, 045, 049, 059; SEO-060, SEO-072; MC-016, 021, 022, 023, 031, 035, 044, 045, 047, 048, 049, 050, 051, 090.
- Notes only: PG-048 (anchor id), SEO-041 (R14), MC-040.

**Shared (owner proposals)**
- New text: SEO-019 (Journal title, R5), SEO-028 (Help meta), SEO-033…039 (packaging alts, R11), JRN-018, 024, 030, 036, 042, 048, 054 (article image alts → chapter scenes).
- Destination only: SEO-025, SEO-026 (`nail-guide-desi` fields until SD5, R7); SEO-029, SEO-030 (conditional on D6, R9).
- Unlocked / current text recorded: SEO-001, 002 (R2/R4), SEO-005…018 (R3; live fields say “Almond”), SEO-027 (R8), PG-002.
- Marked installed (owner-approved 9 Oct, no wording change): PG-002…005; JRN-014…017, 020…023, 026…029, 032…035, 038…041, 044…047, 050…053.
- Notes only: SEO-020, 021, 022, 032.

**v1.2.1 (9 Oct):** LND-012, LND-013, LND-034, LND-035 and SEO-053 checked against the installed assets the orchestrator named and rewritten (all theme-local). Every alt slot in the register has now been checked against its asset.

**v1.2.2 (9 Oct), owner answers and install status, no new writing:** G13 not met, so PG-045/046/047 are hidden. D10 = email only (PG-107). Installed to shared fields: SEO-005…024 (except 025/026), SEO-027, 028, 031, 033…039; JRN-018, 024, 030, 036, 042, 048, 054 (article image = packaging, so these now carry the packaging alts, superseding the v1.2 chapter wording). Not installed: SEO-001/002 (owner step in Online Store preferences), SEO-025/026 (G2–G4), SEO-029/030 (D6), SEO-032 (G10).

**v1.2.3 (9 Oct), interim metas from st-fable’s final acceptance:** SEO-086 (Help meta while only Delivery and the contact form show; SEO-028 stays as the post-SD25 version), SEO-087 (gate-free talks meta: example talks only, no submission promise; SEO-032 stays G10-gated), SEO-088 (optional gate-free `nail-guide-desi` meta; noindex is recommended instead while the page is thin). All three are shared and B4.

**v1.2.4 (9 Oct):** SEO-086 and SEO-087 are installed and verified in the rendered head. SEO-028 and SEO-032 stay as the later versions. SEO-088 is not installed: `nail-guide-desi` is noindex until G2–G4.

**v1.2.5 (9 Oct):** LND-009 hero CTA is now Shop “{name}” ↗ (owner decision, matches board 2).

## v1.3 changes (9 Oct), by destination
Sources: owner decisions A (board wording, T2–T16), B (produce facts → `FACTS.md`), C (the talks becomes a real blog → `07-talks.md`); `spec/TEXT-DIFFS.md`; `spec/talks.md`, `spec/conversation.md`.

**Theme-local (st-foundation)**
- Landing, board wording (A): LND-010, 011, 014, 016, 020, 023, 028, 030, 031, 032, 036, 045, 048, 062; SEO-062, 063, 064, 066 (matching anchors); MC-051.
- Landing FAQ with real answers (A/B): LND-046…051.
- PDP kit and fit disclosures (B, now theme blocks): PDP-003, PDP-005. Unlocked: PDP-002, 004, 007.
- Nail Guide, steps from FACTS (B, plus board wording T19/T20/T21/T28–T32): PG-015, 018, 019, 020, 021, 022, 023, 024, 025, 026, 028, 029, 030, 031. Unlocked: PG-017.
- Help (B + board T33–T35, T37, T38, T40–T42): PG-035, 036, 038, 044, 046, 053, 056, 057. New: PG-108 (Fit body), PG-109 (guide link). Unlocked: PG-043, 045, 047 (Orders is back).
- Bag: MC-026 (board T17, sub restored), MC-040 (GST, G15).
- Unlocked anchors and CTAs: LND-042, LND-060 (Terms once pasted), SEO-056, SEO-065.
- the talks UI: TLK-002…005, 007…016, 020…039, 050…061, 070…077 (all new).
- Notes only: PG-032, PG-041, PG-049, MC-005, MC-045.

**Shared (owner proposals; the orchestrator publishes)**
- the talks blog: TLK-001 (title), TLK-006 (topic tags), TLK-080…087 (8 seed threads), TLK-090…093 (blog SEO and thread patterns).
- Nail Guide SEO unblocked: SEO-025, SEO-026 (st-fable: lift the interim noindex).
- Nav: MC-009 → `/blogs/the-talks` (menu edit).
- Notes only: SEO-031, SEO-087 (old page route).
- Owner paste: `terms-of-service-draft.md` (Settings → Policies).

**Dropped / superseded (IDs kept)**
- PDP-006 (folded into PDP-005), LND-037, LND-052…058, PG-016, SEO-067: dropped.
- PG-062…103 → superseded by 07-talks.md.
- SEO-032 → superseded by TLK-091; SEO-088 → superseded by SEO-026.

**Board diffs I kept on purpose (owner can overrule):**
- T18: bag links keep “Delivery & returns” (one anchor per destination).
- T36: “Returns and exchanges”, because there are no exchanges.
- T39: “get back to you soon”, because no reply time is confirmed.
- T46: “Example conversations” → “Latest talks”, because the threads are real.
- T66: “Post ↗” → “Send it ↗”, because the form sends a suggestion and posts nothing.

**Board diffs still pending owner:** T22 (D1 filters), T23 (wishlist, D9), T24–T27 (Our Story, installed), T67–T91 (Journal, installed).

## v1.3 addendum (9 Oct): board wins for T17–T91, by destination
Rule from the owner, via the orchestrator: board wording wins, with the listed exceptions (T78/T82 board errors; T80 keep the 5 beats; T45/T47/T48/T51–T53/T56 the talks is real; T23 becomes a real Save toggle).

**Theme-local (st-foundation)**
- Bag: MC-045 (Help centre → · Shipping & returns → · Contact us →), SEO-068, SEO-069 (matching anchors).
- Shop chips: MC-018, MC-019 (D1 resolved: Everyday / Statement).
- PDP Save toggle: PDP-055, 056, 057, 058 (new). PDP-018 → superseded.
- Our Story blocks: PG-007, PG-009, PG-011.
- Help: PG-041 (Returns and exchanges), PG-049 (get back to you soon).
- Journal UI: JRN-056 (new “04 /” eyebrow), JRN-002, 004, 005, 009 (1 / 5), 011, 012, 013; closing CTAs JRN-019, 025, 031, 037, 043, 049, 055 (Shop {set} →, “Next story” only if there is space).
- the talks: TLK-008, 021 (author “small talk”), TLK-016 (♡ aria-hidden), TLK-024, TLK-051 (board sub), TLK-058 (Post ↗).
- Already board-matched earlier in v1.3: T17, T19, T20/T21 (with FACTS values), T28–T35, T37, T38, T40–T45, T59–T65.

**Shared (the orchestrator publishes)**
- Our Story intro: PG-002 (board T24; re-install).
- Journal excerpts, board T77…T91: JRN-015, 021, 027, 033, 039, 045, 051. JRN-045 fixes the board’s point of view (see its notes).
- Journal categories: JRN-008 + JRN-057…063 (article tags `category:<label>`).
- Seed threads: TLK-083 and TLK-084 now carry the board titles and bodies; TLK-088 is new (board thread “Same outfit, different confidence.”). Publish order is in TLK-088. Author = “small talk”.

**Still not board, on purpose:** TLK-007 “Latest talks” (spec and orchestrator slot list: the threads are real). JRN-045 point of view. T69 handwritten note (the board is illegible; I kept mine). T76 article titles (installed, not in the board list).

**v1.3.1 (9 Oct), owner decisions and installs:** installed: PG-002, JRN-015/021/027/033/039/045/051 (+ description_tags), JRN-008 and JRN-057…063 (categories). Created but unpublished: TLK-080…088, author “small talk”. Decided: TLK-007 “Latest talks” (T46 overruled), the JRN-045 POV fix, 9 threads, D3 → TLK-077 Tele-MANAS line, D5 → icons hidden. No open owner decisions left in the register.


**v1.3.2 (9 Oct):** LND-013 rewritten to the new board-3 collage (theme-local).

**v1.3.3 (9 Oct):** LND-013 checked against the lab render (no change). LND-012 rewritten to the cropped tile as rendered.

**v1.3.4 (9 Oct):** LND-060 footer nav switched to the board’s 5 labels (Shop · Our Story · the talks · Journal · Nail Guide). No SEO anchor rows change: footer legal labels SEO-075…078 stay, and the header labels MC-008…013 already match.

**v1.3.5 (9 Oct):** MC-016 shop handwritten line → board “Same nails. Different moods.” (honest under F1/F2; fallback in the row notes).

**v1.3.6 (9 Oct):** PG-018 and PG-019 name both a paper strip and a soft tape measure, to match the guide art; “like this” dropped. FACTS F3 step 1 updated to match.

**v1.3.7 (9 Oct), HD art batch 1:** alts rewritten to the new art: SEO-045, 046, 048, 049, 050 (Wild Card interim), 051; LND-034, LND-035. SEO-044 note: the HD hero layers are decorative. SEO-047 unchanged.

**v1.3.8 (9 Oct):** MC-094 “Sign in” and MC-095 “My orders” added (menu drawer account link, theme-local).

**v1.4 (10 Oct), the talks as a live anonymous board (talks/COPY-REQUEST.md, talks/DESIGN.md):**
- New theme-local rows TLK-101…152 (composer, errors, replies/reports, privacy line TLK-148, alias lists TLK-150/151).
- st-talks’ suffixed IDs got clean numbers: 104b → TLK-103, 115b → TLK-142, 116b → TLK-149, 134b → TLK-138, 139a → TLK-152.
- Rewritten: TLK-008, 013, 039 (notes), 072, 073, 074, 075, 076, 094.
- Retired: TLK-027…030, 035…038, 052, 053, 055, 056, 058…061.
- FACTS F14 and Terms §6 rewritten to match the new design.

**v1.4.1 (10 Oct):** HD batch 2 alts: SEO-046, SEO-047 (neutral can, no brand name), SEO-050 (Wild Card v2), LND-012 (Our Vision tile). New TLK-153 pre-launch line. TLK-130 confirmed as the closed-state line.

**v1.4.2 (10 Oct), owner PDP and guide images (hd.batches["chatgpt-C-1"]):** 21 product-media alts SEO-089…109 (shared); guide alts PG-032 (rewritten), PG-110, PG-111 (new); PDP-019 gallery caption “Styled shots of the design. What’s in the kit lists everything you get.” Wording rule in SEO-089: describe what is shown, name the set, never say “photo”, never state a nail count.

**v1.4.3 (10 Oct):** TLK-154, pre-launch variant of house rule TLK-075 (“Once posting opens, …”).

**v1.4.4 (10 Oct), talks privacy is device-only (no IP behind the App Proxy):** TLK-148 rewritten; new TLK-155 privacy-policy paragraph (owner paste, SD33); FACTS F14 and Terms §6 aligned. No other copy mentioned network or IP codes.

**v1.4.5 (10 Oct), official logo:** MC-096 header logo alt and MC-097 footer logo alt (“Small Talk home”); SEO-110 og:image:alt. Packaging alts SEO-033…039 kept (notes on the Brainwave and Shaadi Shift holds). No copy says “no logo” or describes the wordmark as text.

**v1.4.6 (10 Oct), owner box decisions:** Brainwave: the real and HD boxes read “Haan, mera idea hai.”, and the “packaging says tha” exception is retired everywhere (D8 note, SEO-034 note). “tha” survives only in the product handle `haan-mera-idea-tha` (D4, no URL change) and in rows that record the board’s mistake. Shaadi Shift: the new box is accepted, and SEO-037 is still accurate (the yellow daisy with a red centre is a “yellow-flower” nail). No alt or copy describes the box-front hands. **No string changes; notes only.**


**v1.4.7 (10 Oct):** landing chapter name shown in curly quotes (owner design). Presentation only (aria-hidden U+201C/U+201D spans), noted on LND-024. No new strings or keys.

**v1.4.8 (10 Oct), Instagram (D5):** LND-061 updated; new MC-098 (accessible name “Small Talk on Instagram (opens in a new tab)”) and MC-099 (new-tab suffix). Icon only. FACTS F13 lists the channel.


**v1.4.9 (10 Oct), landing talks teaser goes candid and lowercase (owner):** LND-026, LND-031 (“spill your tea ↗”), LND-032, SEO-066 changed; LND-063…067 new (list label, topic chip, meta line, zero-replies state, pre-launch line); LND-027…029 superseded, LND-030 dropped. Post text stays as typed (no forced lowercase on real posts).

**v1.4.10 (10 Oct):** LND-065 shows the reply count only when n > 0; LND-038 hidden on phone (optional short line in its notes).

**v1.4.11 (10 Oct):** TLK-156 “No replies yet” for 0-reply hub and topic rows while posting is closed; TLK-010’s invite applies only while posting is open.

**v1.4.12 (10 Oct):** SEO-111, alt for the laptop Shaadi Shift portrait (separate from SEO-049, the phone sweep), with a one-<picture> fallback in its notes.

**v1.5 (10 Oct), talks UX rework (owner brief via the orchestrator): lowercase, candid, warm.**
- 82 TLK rows rewritten. Each row’s old text is kept in its “current text” column; backup of v1.4.12 in the scratchpad.
- New rows: TLK-157 (replies toggle), TLK-158 (guided prompts), TLK-159 (collapsed composer trigger), TLK-160 (alias/avatar picker heading), TLK-161 (empty topic, posting closed), TLK-162 (prompts label).
- Topics (shared `talk_topic` data): plot twists · tiny wins · second opinions · just venting · nail talk; “something else” retired.
- Not touched: SEO rows (TLK-090…093), seed threads (TLK-080…088), the privacy-policy paragraph (TLK-155), alias word lists (TLK-150/151).

**v1.5.1 (10 Oct), st-talks UX slots U1–U17:** updated TLK-003, 007, 020, 026, 050, 102, 104, 110, 113, 134, 153, 158, 159; new TLK-163…169 (empty-topic headline, line and button; house-rules toggle; reassurance line; “got your own tea?” card and link).
