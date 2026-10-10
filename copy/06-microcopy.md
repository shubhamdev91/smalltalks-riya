# 06 — Microcopy: header, shop, bag, buttons, forms, 404, search, accessibility

Copy register v1.3 · 9 Oct 2026 · nothing here is written to Shopify.

Destination is mostly theme locale overrides (`locales/en.default.json` / `en.default.schema.json` in the new Horizon build) or section settings. These are theme-local, not shared data.
Gate IDs and decisions: see `00-register.md`.

## Header and menu

| id | batch | slot | destination | scope | current text | new text | fact gate | notes |
|---|---|---|---|---|---|---|---|---|
| MC-001 | B3 | Skip link | locale (`accessibility.skip_to_text`) | theme-local (st-foundation) | Skip to content | Skip to content | none |  |
| MC-002 | B3 | Menu button (closed) | locale | theme-local (st-foundation) | — | Open menu | none | Accessible name. Visible icon only. |
| MC-003 | B3 | Menu button (open) | locale | theme-local (st-foundation) | — | Close menu | none |  |
| MC-004 | B3 | Logo link | locale | theme-local (st-foundation) | — | Small Talk home | none | Accessible name for the logo link. v1.4.5: with the image logo this string is the image alt (MC-096/097); the text-logo fallback keeps it as visually hidden text. |
| MC-005 | B3 | the talks header link | section setting | theme-local (st-foundation) | the talks | the talks | none | Locked lowercase, handwritten. v1.3: links to `/blogs/the-talks`. |
| MC-006 | B3 | Bag button | locale | theme-local (st-foundation) | — | Bag · Bag, {count} item / Bag, {count} items | none | Singular/plural. |
| MC-007 | B3 | Search button | locale | theme-local (st-foundation) | — | Search | none |  |
| MC-008 | B3 | Menu item 1 | navigation menu (shared) | shared (owner proposal) | Shop | Shop | none |  |
| MC-009 | B3 | Menu item 2 | navigation menu → `/blogs/the-talks` (shared) | shared (owner proposal) | the talks | the talks | none | v1.3: the destination changes to the blog (owner menu edit). |
| MC-010 | B3 | Menu item 3 | navigation menu | shared (owner proposal) | Journal | Journal | none |  |
| MC-011 | B3 | Menu item 4 | navigation menu | shared (owner proposal) | Our Story | Our Story | none |  |
| MC-012 | B3 | Menu item 5 | navigation menu | shared (owner proposal) | Nail Guide | Nail Guide | none |  |
| MC-013 | B3 | Menu item 6 | navigation menu | shared (owner proposal) | — | Help | none |  |
| MC-014 | B3 | Current page marker | locale | theme-local (st-foundation) | — | (current page) | none | Visually hidden text after the active item, alongside `aria-current="page"`. |
| MC-094 | B3 | Drawer account link — signed out | locale (menu drawer, below the main links) | theme-local (st-foundation) | — | Sign in | none | Owner 9 Oct. Goes to the Shopify customer sign-in. Accessible name: “Sign in to your account” (the drawer gives no other context). |
| MC-095 | B3 | Drawer account link — signed in | locale (menu drawer, below the main links) | theme-local (st-foundation) | — | My orders | none | Owner 9 Oct. Goes to the order history. The visible label is enough; no extra accessible name needed. Shown instead of MC-094 when the customer is signed in. |
| MC-096 | B3 | Header logo image alt (home link: header + menu drawer) | theme: `st-header` logo `image_tag` alt (replaces `alt: shop.name`) | theme-local (st-foundation) | shop.name | Small Talk home | none | v1.4.5. The owner’s official stacked royal-blue wordmark replaces the live-text logo. The image is the link’s only content, so the alt names the link’s purpose; this is the same string as MC-004, so it reads the same as the text logo did. Don’t use `shop.name`: the store name in admin may not be “Small Talk”. Applies to both the header link and the drawer’s small logo link. |
| MC-097 | B3 | Footer logo image alt (home link) | theme: `st-footer` logo alt (replaces the visually hidden `shop.name`) | theme-local (st-foundation) | shop.name (visually hidden) | Small Talk home | none | v1.4.5. Not decorative: the footer logo is a link to the homepage, so it needs a name. Same as MC-096. The tagline next to it is separate text. |
| MC-098 | B3 | Footer Instagram icon link: accessible name | locale `small_talk.footer.social_on` (platform = Instagram) + `small_talk.footer.new_tab` | theme-local (st-foundation) | Small Talk on {{ platform }} | Small Talk on Instagram (opens in a new tab) | none | v1.4.8 (owner, D5). Link: https://www.instagram.com/smalltalks_com/. Icon only, no visible label (board 3 footer shows bare icons; st-fable has the final say on placement). The link keeps `target="_blank" rel="noopener"` so the shopper’s bag and page stay open. Because it opens a new tab, the accessible name must say so (WCAG 3.2.5 / G201). “on Instagram” already tells people where it goes, so no extra “opens Instagram”. Same name in the landing and inner footers. |
| MC-099 | B3 | New-tab suffix (reusable) | locale `small_talk.footer.new_tab` | theme-local (st-foundation) | — | (opens in a new tab) | none | v1.4.8. Appended to the visually hidden text of any link with `target="_blank"` (today only the social icons). Render: `{{ "small_talk.footer.social_on" \| t: platform: "Instagram" }} {{ "small_talk.footer.new_tab" \| t }}`. |

## Shop (collection page)

| id | batch | slot | destination | scope | current text | new text | fact gate | notes |
|---|---|---|---|---|---|---|---|---|
| MC-015 | B3 | Heading | section setting | theme-local (st-foundation) | Pick your plot twist. | Pick your plot twist. | none | Keep. |
| MC-016 | B3 | Handwritten line | section setting | theme-local (st-foundation) | Same nails. Different moods. | Same nails. Different moods. | none | Owner 9 Oct, board wins (board 5). Judged honest under FACTS F1/F2: every set is the same almond press-on in the same 12-size kit, and only the design (the mood) changes. That reverses my v1 objection, which was written before the kit facts existed. Fallback if anyone reads it as “identical designs”: “Same hands. Different moods.” |
| MC-017 | B3 | Filter: all | section setting | theme-local (st-foundation) | All sets | All sets | none |  |
| MC-018 | B3 | Filter: everyday | product tag / filter | shared (owner proposal) | Everyday | Everyday | none (D1 resolved: board) | Owner 9 Oct, board wins (T22). Which sets are Everyday vs Statement is a product-tag decision (shared); the copy is only the chip label. |
| MC-019 | B3 | Filter: statement | product tag / filter | shared (owner proposal) | Statement | Statement | none (D1 resolved: board) | Owner 9 Oct, board wins (T22). |
| MC-020 | B3 | Card link | locale | theme-local (st-foundation) | View set → | View set | none | The arrow is an icon. |
| MC-021 | B3 | Card price | locale | theme-local (st-foundation) | ₹599 (mockup) | {price} | none (G5 met 9 Oct) | Always live. Mockup prices are not facts. |
| MC-022 | B3 | Card badge: coming soon | locale | theme-local (st-foundation) | — | Coming soon | none (G5 met 9 Oct) |  |
| MC-023 | B3 | Card badge: sold out | locale | theme-local (st-foundation) | — | Sold out | none (G5 met 9 Oct) |  |
| MC-024 | B3 | Results count | locale | theme-local (st-foundation) | — | {count} set / {count} sets | none | Announced politely after filtering. |
| MC-025 | B3 | Empty filter state | locale | theme-local (st-foundation) | — | Nothing here yet. Try another filter, or see all sets. | none | “See all sets” is a link that clears the filters. |
| MC-026 | B3 | Bag promo block (board) | section setting | theme-local (st-foundation) | Nails for every plot twist. Collect the whole story. | Nails for every plot twist. ¶ Collect the whole story. | none | Board T17, adopted v1.3 (the sub is back). |

## Bag (cart page + drawer)

| id | batch | slot | destination | scope | current text | new text | fact gate | notes |
|---|---|---|---|---|---|---|---|---|
| MC-027 | B3 | Heading | locale | theme-local (st-foundation) | Your bag | Your bag | none |  |
| MC-028 | B3 | Item count | locale | theme-local (st-foundation) | 2 items | {count} item / {count} items | none |  |
| MC-029 | B3 | Empty state heading | locale | theme-local (st-foundation) | — | Your bag’s empty. For now. | none |  |
| MC-030 | B3 | Empty state CTA | locale | theme-local (st-foundation) | — | Shop all sets | none |  |
| MC-031 | B3 | Empty state line (optional) | locale | theme-local (st-foundation) | — | Seven sets, seven little stories. Start anywhere. | none (G12 met 9 Oct) |  |
| MC-032 | B3 | Quantity label | locale | theme-local (st-foundation) | — | Quantity for {product} | none | Visually hidden. |
| MC-033 | B3 | Decrease | locale | theme-local (st-foundation) | − | Decrease quantity for {product} | none | Accessible name. |
| MC-034 | B3 | Increase | locale | theme-local (st-foundation) | + | Increase quantity for {product} | none | Accessible name. |
| MC-035 | B3 | Quantity at max | locale | theme-local (st-foundation) | — | That’s all we have of this one right now. | none (G5 met 9 Oct) | Shown when the inventory limit is reached. Doesn’t mention the stock number. |
| MC-036 | B3 | Quantity error | locale | theme-local (st-foundation) | — | Couldn’t update that. Try again? | none |  |
| MC-037 | B3 | Remove | locale | theme-local (st-foundation) | Remove | Remove | none | Accessible name: “Remove {product} from bag”. |
| MC-038 | B3 | Removed announcement | locale (live region) | theme-local (st-foundation) | — | {product} removed from bag. | none |  |
| MC-039 | B3 | Subtotal label | locale | theme-local (st-foundation) | Subtotal | Subtotal | none |  |
| MC-040 | B3 | Subtotal note | locale | theme-local (st-foundation) | Shipping calculated at checkout. | Prices include GST. Shipping calculated at checkout. | none (G15 met: F9) | FACTS F9 + the shipping policy. Checkout shows “Including ₹… in taxes”. |
| MC-041 | B3 | Checkout button | locale | theme-local (st-foundation) | Checkout | Checkout | none | Blue commerce button. |
| MC-042 | B3 | Continue link | locale | theme-local (st-foundation) | ← Continue shopping | Continue shopping | none |  |
| MC-043 | B3 | Help block heading | section setting | theme-local (st-foundation) | Need a hand? | Need a hand? | none |  |
| MC-044 | B3 | Help block text | section setting | theme-local (st-foundation) | Our team’s here to help with anything from fit to fixes. | Questions about fit, your order or anything else? Ask us. | none (G8 met 9 Oct) | “Our team” and “fixes” were unverifiable claims. |
| MC-045 | B3 | Help block links | section setting | theme-local (st-foundation) | Help centre · Shipping & returns · Contact us | Help centre → · Shipping & returns → · Contact us → | none (G6, G7, G8 met 9 Oct) | Owner 9 Oct, board wins (T18). Destinations unchanged: `/pages/help`, `/pages/help#delivery`, `/pages/help#contact`. → `aria-hidden`. |
| MC-046 | B3 | Cart error (generic) | locale | theme-local (st-foundation) | — | Something went wrong with your bag. Refresh and try again. | none |  |
| MC-047 | B3 | Item no longer available | locale | theme-local (st-foundation) | — | {product} isn’t available right now, so we’ve taken it out of your bag. | none (G5 met 9 Oct) |  |

## Buttons and shared labels

| id | batch | slot | destination | scope | current text | new text | fact gate | notes |
|---|---|---|---|---|---|---|---|---|
| MC-048 | B3 | Add to bag | locale | theme-local (st-foundation) | Add to bag · ₹599 | Add to bag · {price} | none (G5 met 9 Oct) | See 01-pdp. |
| MC-049 | B3 | Coming soon | locale | theme-local (st-foundation) | — | Coming soon | none (G5 met 9 Oct) |  |
| MC-050 | B3 | Sold out | locale | theme-local (st-foundation) | — | Sold out | none (G5 met 9 Oct) |  |
| MC-051 | B3 | Shop the set (chapters) | section setting | theme-local (st-foundation) | Shop set | Shop set ↗ | none (G5 met 9 Oct) | Owner 9 Oct, board match (T7). Accessible name “Shop {name}”. |
| MC-052 | B3 | View set | locale | theme-local (st-foundation) | View set | View set | none |  |
| MC-053 | B3 | Read the story | locale | theme-local (st-foundation) | Read the story | Read the story | none |  |
| MC-054 | B3 | Close (dialogs/drawers) | locale | theme-local (st-foundation) | — | Close | none |  |
| MC-055 | B3 | Back | locale | theme-local (st-foundation) | Back to the talks / All stories | (keep as on pages) | none |  |
| MC-056 | B3 | Loading | locale | theme-local (st-foundation) | — | Loading… | none |  |
| MC-057 | B3 | Show more | locale | theme-local (st-foundation) | — | Show more | none |  |
| MC-058 | B3 | Disclosure expand/collapse | locale | theme-local (st-foundation) | + | (heading text; state via `aria-expanded`) | none | No extra words. The heading is the button. |

## Form validation (all forms)

| id | batch | slot | destination | scope | current text | new text | fact gate | notes |
|---|---|---|---|---|---|---|---|---|
| MC-059 | B3 | Required field | locale | theme-local (st-foundation) | — | Please fill this in. | none |  |
| MC-060 | B3 | Name missing | locale | theme-local (st-foundation) | — | What should we call you? | none |  |
| MC-061 | B3 | Email missing | locale | theme-local (st-foundation) | — | We need an email to reply to. | none | Help form. On the talks form use the generic required message. |
| MC-062 | B3 | Email invalid | locale | theme-local (st-foundation) | — | That email doesn’t look right. Check for typos? | none |  |
| MC-063 | B3 | Message missing | locale | theme-local (st-foundation) | — | Don’t forget the message. | none |  |
| MC-064 | B3 | Topic missing (the talks) | locale | theme-local (st-foundation) | — | Pick a topic. “Something else” works too. | none |  |
| MC-065 | B3 | Too long | locale | theme-local (st-foundation) | — | That’s a bit long. Keep it under {max} characters. | none |  |
| MC-066 | B3 | Error summary | locale | theme-local (st-foundation) | — | A couple of things need fixing before this can send. | none | Placed at the top of the form, with focus moved there. |
| MC-067 | B3 | Spam / rate-limit (Shopify) | locale | theme-local (st-foundation) | — | Too many tries. Wait a minute, then send again. | none |  |

## 404 and search

| id | batch | slot | destination | scope | current text | new text | fact gate | notes |
|---|---|---|---|---|---|---|---|---|
| MC-068 | B3 | 404 heading | locale / section setting | theme-local (st-foundation) | — | This page wandered off. | none |  |
| MC-069 | B3 | 404 body | locale | theme-local (st-foundation) | — | It might have moved, or the link’s a little off. Let’s get you back. | none |  |
| MC-070 | B3 | 404 CTA 1 | locale | theme-local (st-foundation) | — | Shop all sets | none |  |
| MC-071 | B3 | 404 CTA 2 | locale | theme-local (st-foundation) | — | Go home | none |  |
| MC-072 | B3 | Search placeholder | locale | theme-local (st-foundation) | — | Search sets, colours, stories | none |  |
| MC-073 | B3 | Search label | locale | theme-local (st-foundation) | — | Search | none | Visually hidden label. |
| MC-074 | B3 | Search results heading | locale | theme-local (st-foundation) | — | Results for “{terms}” | none |  |
| MC-075 | B3 | Search empty state | locale | theme-local (st-foundation) | — | Nothing for “{terms}”. Try a colour, like lilac or emerald, or a set name, like Wild Card. | none |  |
| MC-076 | B3 | Search clear | locale | theme-local (st-foundation) | — | Clear search | none |  |
| MC-077 | B3 | Predictive: products | locale | theme-local (st-foundation) | — | Sets | none |  |
| MC-078 | B3 | Predictive: articles | locale | theme-local (st-foundation) | — | Stories | none |  |
| MC-079 | B3 | Predictive: pages | locale | theme-local (st-foundation) | — | Pages | none |  |

## Hero controls (accessible labels)

| id | batch | slot | destination | scope | current text | new text | fact gate | notes |
|---|---|---|---|---|---|---|---|---|
| MC-080 | B1 | Region label | theme section (`aria-label`) | theme-local (st-foundation) | — | Nail sets | none | `aria-roledescription="carousel"`. |
| MC-081 | B1 | Pause button | locale | theme-local (st-foundation) | — | Pause | none | Toggle. Use `aria-pressed`, or swap the label. |
| MC-082 | B1 | Resume button | locale | theme-local (st-foundation) | — | Play | none |  |
| MC-083 | B1 | Restart (after finite pass settles) | locale | theme-local (st-foundation) | — | Play again | none | Starts a new finite pass. |
| MC-084 | B1 | Hold hint (visible, optional, small) | locale | theme-local (st-foundation) | — | Hold to pause | none | Shown once near the nail. Not announced repeatedly. |
| MC-085 | B1 | Hold — screen reader hint | locale (`aria-description` on main nail) | theme-local (st-foundation) | — | Press and hold to pause. | none | Keyboard: hold Space or Enter. |
| MC-086 | B1 | Skin tone group | locale | theme-local (st-foundation) | — | Skin tone | none | Radio group label. |
| MC-087 | B1 | Skin tone option | locale | theme-local (st-foundation) | — | Skin tone {n} of 4 | none | “Skin tone 1 of 4” … “Skin tone 4 of 4”. Selected state via `aria-checked`. No colour names. |
| MC-088 | B1 | Next set (preview hand) | locale | theme-local (st-foundation) | — | Next set: {name} | none |  |
| MC-089 | B1 | Previous set (keyboard/swipe) | locale | theme-local (st-foundation) | — | Previous set: {name} | none | If a previous control exists. |
| MC-090 | B1 | Slide position | locale | theme-local (st-foundation) | — | Set {n} of 7 | none (G12 met 9 Oct) | Uses the live count, not a hard-coded 7. |
| MC-091 | B1 | Live announcement (manual change only) | locale (polite live region) | theme-local (st-foundation) | — | {name}. {headline} | none | Announce on manual change only, never during autoplay, so it doesn’t keep interrupting. |
| MC-092 | B1 | Journal beat counter | locale | theme-local (st-foundation) | 1 / 4 | {n} / {total} · accessible “Part {n} of {total}” | none |  |
| MC-093 | B1 | Journal prev/next | locale | theme-local (st-foundation) | ‹ › | Previous part · Next part | none | Disabled at the boundaries. |
