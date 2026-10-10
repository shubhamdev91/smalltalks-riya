# Small Talk — SEO/AEO strategy (v1, 9 Oct 2026)

Owner: Fable session (strategy and technical sign-off). Words: st-copy (`copy/05-seo.md`). Theme implementation: st-foundation (lock holder). Shared-data moves (pages, blogs, collections, redirects, SEO fields): owner, via orchestrator proposals.

Scope: theme 186651934933 (unpublished). Everything verified below was read from the preview on 9 Oct 2026 with the preview cookie (`?preview_theme_id=186651934933`, `Shopify.theme.id` confirmed on every fetched page). A correct preview head is not a live migration: the live theme 186547241173 still serves whatever it serves until the owner publishes.

Principles (brief §10, Appendix B):
1. One public URL per shopper intent. Everything else is noindexed now and merged or redirected by the owner later.
2. Metadata states category + distinctive design; the visible page keeps the campaign voice. No "best", wear time, "reusable", "non-damaging", materials, kit counts, delivery geography or speed, reviews or ratings in any metadata or schema (gate list in `copy/00-register.md`).
3. Structured data describes only what the page visibly shows, from live Shopify objects. Never hand-written prices, stock, ratings, reviews, FAQ or fictional authors.
4. AEO = ordinary search fundamentals: answer-first visible text on Guide/Help/PDP, consistent internal links, valid schema. No special "AI" schema or files. No promise of ranking or AI-answer inclusion.
5. Nothing in the theme hardcodes the origin (`request.origin` everywhere), so a later custom domain needs no theme change.

## 1. Page intent map (one route per intent)

| Intent | Public route (canonical) | Template / owner | Index | Status 9 Oct |
|---|---|---|---|---|
| Brand discovery + see the sets | `/` | index.json (st-hero + landing) | index | title/meta come from the SHARED shop SEO field; both currently say "Almond" (G14) → SD4/SEO-001/002 pending |
| Compare and choose a set | `/collections/all` | collection.json (st-shop) | index | 7 products render; title is Shopify's default "Products" (no native SEO field for the automatic `all` collection) → theme-local title/meta override needed (§6) |
| Buy one set (×7) | `/products/<handle>` | product.json | index | all 7 ACTIVE with price + stock; InStock offers render; TWO Product blocks (defect C2) |
| Read the stories | `/blogs/journal` | blog.json (st-journal) | index | published, 7 articles |
| Read one story (×7) | `/blogs/journal/<set>` | article.json (st-article) | index | published; no Article schema yet |
| Understand the brand | `/pages/our-story` | page.our-story | index | published |
| Sizing / application / removal | `/pages/nail-guide-desi` today → proposal: `/pages/nail-guide` | page.nail-guide | index | both routes live with different old bodies (see §2) |
| Delivery, returns, orders, contact | `/pages/help` | page.help / page.desi-help | index | h1 only; body renders EMPTY on preview (gated topics hidden) — see §8 |
| Legal policies | `/policies/shipping-policy`, `/policies/refund-policy`, `/policies/privacy-policy` | Shopify policy template | index (Shopify default) | shipping + refund + privacy exist (200); terms 404 (G16) |
| Community | `/pages/the-talks` | page.the-talks | index | published |
| Utility | `/cart`, `/search`, `/account/*`, `/collections` (list), `/collections/<tag>` filters, `?variant=` | — | noindex / canonicalised | cart + search noindex verified; the rest not yet |

Not an intent, must not compete: `/pages/our-world`, `/pages/nail-guide` (old body), `/blogs/news`, `/pages/contact`, `/collections/frontpage`, `/collections/press-on-nails`, `/collections/soft-chaos`, `/collections/big-energy`, `/collections/after-dark`.

## 2. Duplicate routes — proposals (owner decides; theme applies interim noindex)

Verified on 9 Oct: all of these return 200 on the build theme, carry a self-canonical, no robots meta, and are listed in the live sitemap (`sitemap_pages_1.xml`, `sitemap_collections_1.xml`, `sitemap_blogs_1.xml`).

| Pair | Finding | Proposal (owner) | Interim (theme-local, st-foundation) |
|---|---|---|---|
| `/pages/nail-guide` vs `/pages/nail-guide-desi` | Both published. `nail-guide` = old generic guide ("Prep. Press. Express.", wear-time wording → violates G9). `nail-guide-desi` = the new gated body; nav "Nail Guide" links here. Copy register and Appendix B assume `/pages/nail-guide`. | Make `/pages/nail-guide` the single public route: move the gated body + `page.nail-guide` template to the `nail-guide` page, then delete `nail-guide-desi` and add a 301 `/pages/nail-guide-desi → /pages/nail-guide` (URL redirect in admin). Clean slug, already in the sitemap, no "desi" in a public URL. | Until then: `noindex, follow` on `/pages/nail-guide` (the old body), nav keeps pointing at `nail-guide-desi`. Never canonical-point one page at another with different content. |
| `/pages/our-story` vs `/pages/our-world` | `our-world` = old ChatGPT brand page ("Nail art. Desi heart.", "Shop the drop"), different copy, same intent. | Delete `our-world`, 301 → `/pages/our-story`. | `noindex, follow` on `/pages/our-world`; no internal links to it (none found on home). |
| `/blogs/journal` vs `/blogs/news` | `news` is an empty default blog (0 articles, old description "The little moments, and the hands in them"). | Delete the `news` blog (Shopify requires at least one blog; `journal` remains), or leave it empty and unlinked. | `noindex, follow` when `blog.articles_count == 0`. |
| `/pages/help` vs `/pages/contact` | `contact` = default Shopify contact page (name/email/phone/comment form). Register puts the contact form inside Help (D6). | One contact surface: Help. Delete `/pages/contact` and 301 → `/pages/help#contact` (or keep it only if the owner wants a bare form; then SEO-029/030 apply). | `noindex, follow` on `/pages/contact`; footer/bag "Contact us" (SEO-070) points at `/pages/help#contact`. |
| `/collections/all` vs `frontpage`, `press-on-nails`, `soft-chaos`, `big-energy`, `after-dark` | Five legacy collections, all empty of live products (`products.json` = []), yet published, in the sitemap, with keyword titles ("Shop Press-On Nails in India", "Everyday Press-On Nails — Soft Chaos"). `/collections/frontpage` renders the empty state. | Delete the five legacy collections (or unpublish from Online Store). If the owner wants editable Shop metadata and a sitemap entry for the shop, create one automated collection with handle `all` (all products); Shopify then uses it in place of the automatic route. | `noindex, follow` on any collection with `collection.products_count == 0` and on `/collections` (list-collections). |
| `/products/haan-mera-idea-tha` ("tha") | Handle carries the old wording; copy uses "hai". | Keep the handle (D4). A handle change would only add a redirect hop for no shopper benefit. | Self-canonical; nothing to do. |

## 3. Canonical and indexing rules

Canonical:
- Use Shopify's `canonical_url` everywhere (verified clean: no `preview_theme_id`, no `?variant=`, no tag path on the base collection).
- Paginated collection/blog pages: self-canonical with `?page=n` (Shopify default), indexable, titles get " – Page n" (already in meta-tags).
- Tagged/filtered collection URLs (`/collections/all/<tag>`, `?filter.*`): `noindex, follow`; the shop's own filter UI must not generate crawlable duplicate listings. Condition in Liquid: `current_tags != blank or request.path contains '/collections/all/'` or any `filter.` param.
- Never emit a canonical that points at a page with different content (no cross-page canonical for the duplicates above; use noindex + owner redirect).
- Never emit a global/blanket noindex on the theme (it would survive publishing). Every noindex is a per-route condition in `snippets/st-seo.liquid`.

`noindex, follow` list for `st-seo.liquid` (today it covers cart, search, captcha only):
1. `cart`, `search`, `captcha` (done, verified).
2. `list-collections` (`/collections`).
3. `collection` when `collection.products_count == 0` (covers the five legacy collections and any future empty one; the live shop never shows an empty state to Google).
4. `collection` with `current_tags` or filter params.
5. `blog` when `blog.articles_count == 0` (`/blogs/news`).
6. `page` when `page.handle` is one of `our-world`, `nail-guide` (only while its body is the old guide), `contact` (only if folded into Help). Keep this handle list in one Liquid array at the top of the snippet with a comment "remove when owner deletes/redirects (SD5)".
7. `account`, `addresses`, `order` page types (Shopify already disallows `/account` in robots.txt; the meta is belt and braces), `404`, `password`, `gift_card`.

Sitemap: Shopify generates it; noindexed-but-published resources still appear until the owner deletes/unpublishes them, which is why §2 asks for deletion, not just noindex. Products: all 7 ACTIVE and published to Online Store (verified via `/collections/all/products.json`); they will appear in `sitemap_products_1.xml` once the publication catches up (the products sitemap returned only `/` at 14:5x IST; re-check before publishing).

robots.txt: Shopify default (verified). Do not add a `robots.txt.liquid` override; the default already disallows cart, checkout, account, admin, internal endpoints and allows everything shoppable.

Hreflang / markets: single market, single locale (`lang="en"`). No hreflang.

Preview protection: unpublished themes are only reachable with the preview cookie; no extra noindex is needed for the build theme and none may be added.

## 4. Internal link architecture

Depth target: every indexable page within two clicks of `/`; every PDP reachable from Shop, from its Journal story, from its landing chapter and from the hero CTA.

Global (header + footer, every page):
- Header: Shop → `/collections/all` · Our Story · Journal → `/blogs/journal` · Nail Guide → (the one guide route) · Help · the talks · Bag. Verified present.
- Footer: Shop all sets · Our story · Journal · Nail Guide · Help · the talks · Contact us (→ Help#contact) · Shipping policy · Refund policy · Privacy policy · Terms (when G16). Today the footer shows Privacy only; shipping and refund policies now exist and must be linked (also from Help "Delivery"/"Returns" and from the bag help block, SEO-069).

Per page type:
- Home: hero CTA → current set PDP (verified); gallery/chapter "Shop the set" → each PDP (verified, all 7); teasers → Journal, Our Story, Guide, the talks, Help (verified). One anchor per destination (SEO-062…067).
- Shop: card → PDP (title + image in one link, no duplicate adjacent links); shop handwritten line links nothing.
- PDP: "Find your fit" → Guide (G2), "Delivery & returns" → Help#delivery (policies linked from there), "Read the story" → its Journal article, "Need a hand?" → Help, breadcrumb Home › Shop › Set (visible, matches BreadcrumbList).
- Journal index: card → article; article → "Shop {set}" PDP (G5 now satisfied), "Next story" → next article, back → `/blogs/journal`.
- Our Story → Shop all sets, Read the Journal. Guide → Help ("Message us from the Help page"). Help → policies, Guide, Contact anchor. the talks → Help (rules), no outbound social unless D5 confirms accounts.
- Bag: Help, Delivery & returns (→ Help#delivery), Contact us.

Rules: anchor text = destination name (never "click here"/"here"); same destination = same anchor everywhere (register SEO-056…072); no links to noindexed routes from indexable pages (search box excepted); external links `rel="noopener"`, no `nofollow` games.

## 5. Structured data design (JSON-LD only, one block per type per page)

Rendered by `snippets/st-seo.liquid` from live objects. Remove every duplicate emitter: `sections/product-information.liquid` line 3 (`{{ closest.product | structured_data }}`, verified duplicate Product on PDP — defect C2) and the Horizon `sections/header.liquid` Organization block if that section is ever re-enabled (st-header is in use, so it does not render today).

| Page | Types | Source fields | Must not contain |
|---|---|---|---|
| `/` | `Organization` (+ `WebSite` optional, no SearchAction because search is noindex) | `shop.name`, `request.origin`, `settings.logo`, `sameAs` only from configured social settings (D5) | contactPoint with unstaffed channels, founder names, address unless the owner confirms |
| `/collections/all` | `BreadcrumbList` (Home › Shop). `ItemList` optional, skip for now. | | |
| PDP | `Product` + `Offer` (one block), `BreadcrumbList` Home › Shop › {Set} | `product.title`, `product.description` (strip HTML **with spaces** — current output concatenates "gold.Bill idhar.The"), `product.featured_media` + up to 6 images, `variant.sku`, `brand` = "Small Talk", `offers[]` per variant with `price` (number), `priceCurrency` = `cart.currency.iso_code`, `availability` from `variant.available`, `url` with `?variant=`, `itemCondition` New. Only variants with price > 0 (already so). Add `"@id"` = product URL + `#product` so the two emitters can never both claim it. | `aggregateRating`, `review`, `shippingDetails`, `hasMerchantReturnPolicy` (add only after G6/G7 policies are final AND copied from the policy objects), `material`, `color` guesses, `category` strings like "Almond press-on nails" (G14) |
| `/blogs/journal` | `BreadcrumbList` Home › Journal. `Blog` optional, skip. | | |
| Article | `Article` (not BlogPosting with fictional author), `BreadcrumbList` Home › Journal › {title} | `headline` = article.title, `datePublished`/`dateModified` = article.published_at / updated_at, `author` = `{ "@type": "Organization", "name": "Small Talk" }`, `publisher` = Organization with logo, `image` = article.image, `mainEntityOfPage` = canonical, `description` = article.excerpt | `Review`, `Rating`, a person author, `wordCount` claims |
| Pages | `BreadcrumbList` only. | | `FAQPage`, `HowTo` (no rich result value; and the guide steps are gated/kit-dependent), `ContactPage` with phone/hours unless G8 |
| Policies | nothing extra (Shopify template). | | |

Validation gate (Sonnet/operational, after st-foundation reports): every indexable template parses in Google's Rich Results Test / schema.org validator with zero errors; exactly one Product per PDP; Offer price equals the visible price in the buy box; availability equals the visible state; description text has word spaces.

## 6. Metadata rules

- `<title>`: "{Page subject} | Small Talk" (home: "Small Talk — …"). ≤ 60 characters where possible; subject first, brand last; unique per route; never only the brand. Horizon's meta-tags appends " – Small Talk" when the brand is absent and " – Page n" on pagination (keep).
- Meta description: 120–155 characters, states what the page offers and one distinctive detail, no banned words, no count ("seven") unless all seven are visible on that page (G12 is satisfied today: 7 ACTIVE and rendering).
- H1: exactly one per page, real text, matching the intent (verified: shop "Pick your plot twist.", pages/blog titles). Home H1 = the current hero headline (rotates with the set); accepted, because the title tag carries the category and the hero headline is the board. `/search` has no H1 (noindex, low priority, but add one for accessibility). `/cart` renders the empty-state H1 twice (st-foundation defect; one H1).
- Shared vs theme-local: shop/product/page/blog/article SEO fields are shared (owner, SD4). Theme-local overrides are allowed only where Shopify has no field: `/collections/all` title + description (render in `meta-tags.liquid` when `request.path == routes.all_products_collection_url`), 404, list-collections. Do not build a theme-level override table for products/pages: it desynchronises og: tags and the Shopify sitemap/feeds from what Google sees.
- Open Graph / Twitter: Horizon meta-tags covers it. Home has no `og:image` today (no `page_image`): owner sets the social sharing image in Online Store › Preferences (shared), or the theme falls back to a theme setting image when `page_image` is blank (theme-local, acceptable).
- Policy page titles ("Shipping policy – Small Talk") are Shopify defaults; fine.
- Never ship "Almond" (G14), "India"/delivery speed (G6), wear time (G9) or "reusable" in any title/meta/alt until the gate is cleared; the current shared home + product SEO fields and the legacy collections violate G14/G6 and are listed for the owner in the review file.

## 7. Image alt policy

1. Real product photography (packaging box with the nail tray visible, PDP gallery, shop tile, Our Story stack): descriptive alt naming the set, "press-on nail box" and the visible nail colours. The packaging art is an illustration printed on a box; say "box" and never "photo of hands". Shared product media alt (owner, G11). Verified example today: home gallery packaging alts are old wording ("Bill idhar packaging with an illustrated woman paying the bill…") and use the handle-style name, not the set name.
2. Illustrations (chapter scenes, lifestyle hand composites, guide steps): prefix "Illustration:" and describe only what the accepted asset actually shows (manifest `phase2.checks`): On Me chapter has no bill, Pinky Promise has no hands, Brainwave has no blue pen, Shaadi Shift pin is not legible, no scene shows nails. Alt text must not restore the brief's intent that the art does not show.
3. Decorative / duplicated-in-text imagery: `alt=""` — hero character, finger/tone layer, preview hand image (button carries "Next set: {name}"), chapter nail rows, eye illustration, CSS sprite nails (no alt possible; the hidden main-nail description SEO-041 is the one spoken description, verified wired via the controller's `altText`).
4. One description per visual idea: never alt the same nail design twice in one section.
5. Alts are not metadata: no "press-on nails India", no "best". ≤ 125 characters.
6. Every `<img>` carries `width`/`height` (verified on hero/tone/hand) and `loading="lazy"` below the fold; only the hero tone image and set-1 sprite are high priority (verified).

## 8. Findings from the 9 Oct read (for the orchestrator; not SEO copy)

1. `/pages/help` renders only the H1 "Need a hand?" with no body on the build theme (all topics and the contact block are gated and hidden, and Help has no fallback). Shipping and refund policies now exist, so the Delivery/Returns topics can at least link to `/policies/shipping-policy` and `/policies/refund-policy` while G6/G7 wording is confirmed. An empty Help page with an "order support" meta description would be a hard fail for shoppers and for search.
2. PDP emits two `Product` JSON-LD blocks (st-seo + Horizon product-information) — C2, still open on preview.
3. Product JSON-LD description lacks spaces between stripped paragraphs ("gold.Bill idhar.The conversation…").
4. Journal article pages emit no `Article` schema (st-article has none; Horizon's main-blog-post is not used).
5. Legacy routes live and indexable: our-world, nail-guide (old), blogs/news, contact, five empty collections (§2).
6. Footer links Privacy only; shipping/refund policies exist and are unlinked.
7. Home `og:image` missing; shared home title/meta and all 7 product SEO fields carry "Almond" (G14) and "original illustrated packaging"; legacy collections carry "in India".
8. `/cart` has two H1s; `/search` has none.
9. Products sitemap listed only `/` at read time; re-check after publication propagates.

## 9. Verification plan (after st-foundation reports)

Fable (judgement) on preview: rendered head per route in §1 (title, description, canonical, robots), JSON-LD parse + value match against the visible buy box on 2 PDPs, Article schema on 1 article, noindex list, internal link map on home/PDP/article/bag, alt policy spot-check on home/shop/PDP/chapter/journal, Help page body present. Sonnet (operational, if the owner starts one): full-crawl of all routes for status/canonical/robots/schema validity and broken links. Record tool, date, URL, theme id, viewport for each.

## 10. the talks, anonymous v2 routes (added 10 Oct 2026)
The talks moved from blog articles to metaobject pages. Rules:

| Route | Index | Canonical | Title | Structured data |
|---|---|---|---|---|
| `/blogs/the-talks` (hub) | index | self | "the talks \| Small Talk" | BreadcrumbList |
| `/pages/talks/<topic>` | `noindex, follow` | self | "{Topic} \| the talks \| Small Talk" | none |
| `/pages/talk/<handle>` (thread) | index | self | "{title} \| the talks \| Small Talk" | BreadcrumbList (Home › the talks › title). Optional DiscussionForumPosting from real fields only. |
| `/blogs/the-talks/<handle>` (old article) | `noindex, follow` until removed | `/pages/talk/<handle>` | (unchanged) | none (drop Article) |
| `/blogs/the-talks/tagged/<tag>` | `noindex, follow` (unchanged) | self | | none |

- **DiscussionForumPosting, if used:**
  - Author: Organization "Small Talk" for brand seeds, or Person {alias} for shopper posts.
  - `datePublished` = posted_at; `text` = body.
  - `interactionStatistic`: one CommentAction with the real reply count.
  - No Review, Rating or invented engagement.
- **End state:** unpublish the 9 articles and add 301 redirects from `/blogs/the-talks/<handle>` to
  `/pages/talk/<handle>`. Shopify applies a redirect only once the old path returns 404. Each thread then has one
  indexable URL.
- **Meta description:** the thread body excerpt (real text). Held and draft entries never render, so they never index.
- The §1 row "Community `/pages/the-talks`" is superseded by this table.
