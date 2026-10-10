# 01 — Product pages (PDP)

Copy register v1.3 · 9 Oct 2026 · owner of words: copy session · nothing here is written to Shopify.

Sources: `backup/theme-186649313493/campaign-metaobjects.json` (current text), brief Appendix A (baseline proposals), board 5.jpg "Product".
Gate IDs (G1–G16) and decisions (D1–D9) are defined in `00-register.md`.

Rules applied: product names, headlines, notes and design descriptions are locked and copied verbatim. Stories stay 30–45 words, one paragraph, fiction, no performance claims. Typography: curly apostrophes (’) to match the existing metaobject records.

## Shared slots (all seven PDPs)

| id | batch | slot | destination | scope | current text | new text | fact gate | notes |
|---|---|---|---|---|---|---|---|---|
| PDP-001 | B2 | Story disclosure heading | theme section setting (PDP disclosure title; headline injected from `campaign.headline`) | theme-local (st-foundation) | The story: Bill idhar. (board) | The story: {headline} | none | Example: “The story: Haan, mera idea hai.” Never hard-code; pull from the campaign record so Brainwave can’t regress to “tha”. |
| PDP-002 | B2 | Kit disclosure heading | theme section setting | theme-local (st-foundation) | What’s in the kit | What’s in the kit | none (G1 met: F2) | Hide the whole disclosure until G1 is confirmed. No placeholder text goes live. |
| PDP-003 | B2 | Kit disclosure body | theme section block (same kit for all 7 sets) | theme-local (st-foundation) | — (absent) | 24 almond press-ons in 12 sizes ¶ Nail glue ¶ A sheet of 24 adhesive tabs ¶ Mini nail file ¶ Prep pad ¶ Cuticle stick ¶ Instruction card | none (G1, G14 met: F1, F2) | FACTS F2, rendered as a list. Theme-local because the kit is identical for every set. |
| PDP-004 | B2 | Fit & application heading | theme section setting | theme-local (st-foundation) | Fit & application | Fit & application | none (G2–G4 met) | Hide until at least one of G2/G3/G4 is confirmed. |
| PDP-005 | B2 | Fit & application body | theme section block (same for all 7 sets) | theme-local (st-foundation) | — (absent) | Fit: every kit has 12 sizes (0–11), so nothing to pick at checkout. Find your fit → ¶ Wear: glue, up to about 2 weeks · tabs, 1–3 days ¶ On: prep, glue or tab, press for 20–30 seconds ¶ Off: soak 10–15 minutes, lift gently from the side. Never force or peel. ¶ Again: yes, if you take them off gently. | none (G2, G3, G4, G9 met: F3–F7) | FACTS F3–F7 as a short list (the owner wants steps, not paragraphs). “Find your fit →” links to the Nail Guide. |
| PDP-006 | B2 | Removal (if a separate disclosure is wanted) | theme section setting | n/a (dropped) | — | Heading: Removal · Body: GATE G4 | G4 | DROPPED v1.3: removal is folded into Fit & application (PDP-005). Optional. Folding it into Fit & application keeps the PDP shorter. |
| PDP-007 | B2 | Link under price: fit | theme section setting (link label) → `/pages/nail-guide` | theme-local (st-foundation) | Find your fit | Find your fit | none (G2 met: F3) | Keep. The label has to match the guide’s real content. |
| PDP-008 | B2 | Link: delivery & returns | theme section setting → `/pages/help#delivery` | theme-local (st-foundation) | Delivery & returns | Delivery & returns | none (G6, G7 met 9 Oct) | Unlocked. Goes to `/pages/help#delivery`; the Delivery and Returns topics there link `/policies/shipping-policy` and `/policies/refund-policy` (R16). |
| PDP-009 | B2 | Link: help | theme section setting → `/pages/help` | theme-local (st-foundation) | Need a hand? | Need a hand? | none | Keep. |
| PDP-010 | B2 | Link: story | theme section setting → Journal article | theme-local (st-foundation) | Read the story | Read the story | none (needs article live) | Goes to the matching Journal article (`campaign.journal`). |
| PDP-011 | B2 | Add to bag button | theme locale / section setting | theme-local (st-foundation) | Add to bag · ₹599 (board) | Add to bag · {selected variant price} | none (G5 met 9 Oct) | Price is always the selected variant’s live price (sets are live at ₹599 / ₹499 / ₹699), never typed into copy. Build note (9 Oct): on screens narrower than ~380 px the button visibly shows only “Add to bag” (the price sits beside the title), but its accessible name stays “Add to bag · {price}”. |
| PDP-012 | B2 | Unavailable: not launched | theme locale | theme-local (st-foundation) | — | Coming soon | none (G5 met 9 Oct) | All seven are live, so this only shows for a future unreleased variant. Disabled button. No date promised. |
| PDP-013 | B2 | Unavailable: no stock | theme locale | theme-local (st-foundation) | — | Sold out | none (G5 met 9 Oct) | Disabled button. |
| PDP-014 | B2 | Quantity label (visually hidden) | theme locale | theme-local (st-foundation) | — | Quantity | none | See 06-microcopy for − / + labels. |
| PDP-015 | B2 | Adding state | theme locale | theme-local (st-foundation) | — | Adding… | none | Button text while the request runs. |
| PDP-016 | B2 | Added confirmation | theme locale (live region) | theme-local (st-foundation) | — | Added to bag. | none | Announced politely; drawer/bag opens per Horizon behaviour. |
| PDP-017 | B2 | Add error | theme locale | theme-local (st-foundation) | — | Couldn’t add that. Try again? | none | Generic. Inventory-limit message lives in 06-microcopy. |
| PDP-018 | B2 | Save / wishlist icon (board shows a bookmark) | — | n/a (superseded) | (icon only on board) | see PDP-055…058 | none (D9 resolved) | Resolved v1.3: D9 → real Save toggle, see PDP-055…058. Horizon has no native wishlist. Recommend dropping the icon rather than labelling a button that does nothing. |
| PDP-019 | B2 | Gallery: illustration notice | theme section setting (caption under campaign art, if campaign art is shown in the PDP gallery) | theme-local (st-foundation) | — | Styled shots of the design. What’s in the kit lists everything you get. | none (owner accepted styled images, 10 Oct) | Recommended visible caption under the PDP gallery (theme-local). The gallery images are photo-style renders (not photos of a delivered kit), and the flatlay shows 5 nails while the kit has 24 (G1). One honest line covers both without spoiling the gallery. Replaces the v1 “Campaign illustration…” caption. |

## Per set

### On Me (`bill-idhar`, metaobject `on-me`)

| id | batch | slot | destination | scope | current text | new text | fact gate | notes |
|---|---|---|---|---|---|---|---|---|
| PDP-020 | B2 | Product name | product title (shared) | shared (owner proposal) | On Me | On Me | none | Locked. |
| PDP-021 | B2 | Design description | metaobject `short_description` | shared (owner proposal) | Burgundy. Tortoiseshell. A little gold. | Burgundy. Tortoiseshell. A little gold. | none | Locked. Keep it beside title and price. |
| PDP-022 | B2 | Headline | metaobject `headline` | shared (owner proposal) | Bill idhar. | Bill idhar. | none | Locked. |
| PDP-023 | B2 | Note | metaobject `note` | shared (owner proposal) | I’ve got this. | I’ve got this. | none | Locked. |
| PDP-024 | B2 | Story | theme-local PDP story override (D7 resolved 9 Oct) | theme-local (st-foundation) | The conversation is still going. Someone orders one more round. You catch the server’s eye and reach for the bill. No announcement. Just a small, certain gesture: this one’s on me. | Everyone’s still talking when the bill arrives. You catch the server’s eye and slide it towards you, burgundy and a little gold catching the light. You wanted to treat them. Bas. No speech needed. Bill idhar. | none | D7 resolved: theme-local override installed; the shared `story` field is untouched. 36 words. Built from Appendix A; I took out the semicolon and the line “That’s all the explanation it needs”, which read as written prose rather than speech. Her choice comes first and the nails just happen to be there. |

### Brainwave (`haan-mera-idea-tha`, metaobject `brainwave`)

| id | batch | slot | destination | scope | current text | new text | fact gate | notes |
|---|---|---|---|---|---|---|---|---|
| PDP-025 | B2 | Product name | product title | shared (owner proposal) | Brainwave | Brainwave | none | Locked. |
| PDP-026 | B2 | Design description | metaobject `short_description` | shared (owner proposal) | Cobalt blue, pearly white and silver-toned shine. | Cobalt blue, pearly white and silver-toned shine. | none | Locked. |
| PDP-027 | B2 | Headline | metaobject `headline` | shared (owner proposal) | Haan, mera idea hai. | Haan, mera idea hai. | none | Locked. Never “tha”, even though the handle says so. |
| PDP-028 | B2 | Note | metaobject `note` | shared (owner proposal) | Called it. | Called it. | none | Locked. |
| PDP-029 | B2 | Story | theme-local PDP story override (D7 resolved 9 Oct) | theme-local (st-foundation) | It began as a sketch in the margin: a crescent-shaped bag, a better curve, a detail you couldn’t leave alone. You tried it. Changed it. Made it real. When someone asks whose idea it is, you know exactly what to say. | The bag still isn’t right. You turn the sketchbook, redraw the curve, and there it is. Later, someone asks whose idea that detail was. Your cobalt nail taps the page. Haan, mera idea hai. | none | D7 resolved: theme-local override installed; the shared `story` field is untouched. 34 words. Appendix A said “cobalt-tipped finger”, but this set has full cobalt nails, not tips, so I changed it to “cobalt nail”. Sketch world only. Doesn’t suggest Small Talk sells bags. |

### Diet Cherry (`haan-wohi-wali`, metaobject `diet-cherry`)

| id | batch | slot | destination | scope | current text | new text | fact gate | notes |
|---|---|---|---|---|---|---|---|---|
| PDP-030 | B2 | Product name | product title | shared (owner proposal) | Diet Cherry | Diet Cherry | none | Locked. Never “Cherry Repeat” (board 4/5 still shows it; ignore). |
| PDP-031 | B2 | Design description | metaobject `short_description` | shared (owner proposal) | Deep red, blush and silver-toned accents. | Deep red, blush and silver-toned accents. | none | Locked. |
| PDP-032 | B2 | Headline | metaobject `headline` | shared (owner proposal) | Haan, wohi wali. | Haan, wohi wali. | none | Locked. |
| PDP-033 | B2 | Note | metaobject `note` | shared (owner proposal) | My usual. | My usual. | none | Locked. |
| PDP-034 | B2 | Story | theme-local PDP story override (D7 resolved 9 Oct) | theme-local (st-foundation) | A new place. A familiar face across the table. Before the menu reaches you, your friend asks if it’s the usual. You smile. Some favourites travel with you, wherever the evening goes. | New place. Same friend, who knows your order before you’ve even opened the menu. You reach for the cold can, deep red and silver bright against it. “The usual?” You’re already smiling. Haan, wohi wali. | none | D7 resolved: theme-local override installed; the shared `story` field is untouched. 35 words. A plain can with no beverage brand named. Artwork flag: boards 3 and 5 show a real cola trademark on the can (D8). |

### Green Flag (`tum-aa-jao-main-dekh-lungi`, metaobject `green-flag`)

| id | batch | slot | destination | scope | current text | new text | fact gate | notes |
|---|---|---|---|---|---|---|---|---|
| PDP-035 | B2 | Product name | product title | shared (owner proposal) | Green Flag | Green Flag | none | Locked. |
| PDP-036 | B2 | Design description | metaobject `short_description` | shared (owner proposal) | Emerald green and blush, with pointed green tips. | Emerald green and blush, with pointed green tips. | none | Locked. |
| PDP-037 | B2 | Headline | metaobject `headline` | shared (owner proposal) | Tum aa jao. Main dekh lungi. | Tum aa jao. Main dekh lungi. | none | Locked. |
| PDP-038 | B2 | Note | metaobject `note` | shared (owner proposal) | Sorted. | Sorted. | none | Locked. |
| PDP-039 | B2 | Story | theme-local PDP story override (D7 resolved 9 Oct) | theme-local (st-foundation) | The plan falls apart. Your phone rings. There’s no perfect itinerary, no carefully set table. You move a chair, make a little room and say the thing your friend needed to hear: come over. We’ll figure out the rest. | Her plans just fell through. You tuck the receiver against your shoulder and pull out another chair. Green-tipped fingers rest on its back while she asks if you’re sure. You are. Tum aa jao. Main dekh lungi. | none | D7 resolved: theme-local override installed; the shared `story` field is untouched. 37 words. Matches the rotary-phone art (a receiver, not a smartphone). “Just fell through” sounds more like speech than “have fallen through”. |

### Shaadi Shift (`dulhan-tu-duty-meri`, metaobject `shaadi-shift`)

| id | batch | slot | destination | scope | current text | new text | fact gate | notes |
|---|---|---|---|---|---|---|---|---|
| PDP-040 | B2 | Product name | product title | shared (owner proposal) | Shaadi Shift | Shaadi Shift | none | Locked. |
| PDP-041 | B2 | Design description | metaobject `short_description` | shared (owner proposal) | Pink and deep red, with a little yellow flower. | Pink and deep red, with a little yellow flower. | none | Locked. |
| PDP-042 | B2 | Headline | metaobject `headline` | shared (owner proposal) | Dulhan tu. Duty meri. | Dulhan tu. Duty meri. | none | Locked. |
| PDP-043 | B2 | Note | metaobject `note` | shared (owner proposal) | On duty. | On duty. | none | Locked. |
| PDP-044 | B2 | Story | theme-local PDP story override (D7 resolved 9 Oct) | theme-local (st-foundation) | One missing safety pin. One last adjustment. One look that says, stay close. You’re there for the tiny things between the big moments, keeping her laughing while the room gets louder. Her big day. Your very familiar role. | Everyone’s calling for the bride. She’s looking for you. One last fix to her dupatta, one whispered joke, and she’s laughing again. The little yellow flower on your nail flashes as you smooth the edge. Dulhan tu. Duty meri. | none | D7 resolved: theme-local override installed; the shared `story` field is untouched. 39 words. “Fix to her dupatta” replaces “dupatta adjustment”, which read stiff. The nail only smooths fabric and does no work, so there’s no performance claim. |

### Wild Card (`achha-tum-pehle`, metaobject `wild-card`)

| id | batch | slot | destination | scope | current text | new text | fact gate | notes |
|---|---|---|---|---|---|---|---|---|
| PDP-045 | B2 | Product name | product title | shared (owner proposal) | Wild Card | Wild Card | none | Locked. |
| PDP-046 | B2 | Design description | metaobject `short_description` | shared (owner proposal) | Acid lime, blush and cobalt-and-white checks. | Acid lime, blush and cobalt-and-white checks. | none | Locked. |
| PDP-047 | B2 | Headline | metaobject `headline` | shared (owner proposal) | Achha. Tum pehle. | Achha. Tum pehle. | none | Locked. |
| PDP-048 | B2 | Note | metaobject `note` | shared (owner proposal) | Your move. | Your move. | none | Locked. |
| PDP-049 | B2 | Story | theme-local PDP story override (D7 resolved 9 Oct) | theme-local (st-foundation) | Your cards face you. Your smile gives nothing away. Across the table, someone is feeling very confident. You let them take their turn, quietly hoping the next card goes your way. The fun is in what happens next. | You’ve got a good hand. Maybe good enough. You tuck the cards closer, acid lime and blue-white checks bright against the edges. Across the table, someone’s itching to go first. You let them. Achha. Tum pehle. | none | D7 resolved: theme-local override installed; the shared `story` field is untouched. 36 words. Appendix A’s “lime and blue checks” made the checks sound lime, so I corrected it (the checks are cobalt and white). “Itching to go first” sets up “Tum pehle”. The win stays uncertain and the cards face her. |

### Pinky Promise (`haath-do-main-hoon`, metaobject `pinky-promise`)

| id | batch | slot | destination | scope | current text | new text | fact gate | notes |
|---|---|---|---|---|---|---|---|---|
| PDP-050 | B2 | Product name | product title | shared (owner proposal) | Pinky Promise | Pinky Promise | none | Locked. |
| PDP-051 | B2 | Design description | metaobject `short_description` | shared (owner proposal) | Lilac with deep burgundy, asymmetric pointed tips. | Lilac with deep burgundy, asymmetric pointed tips. | none | Locked. |
| PDP-052 | B2 | Headline | metaobject `headline` | shared (owner proposal) | Haath do. Main hoon. | Haath do. Main hoon. | none | Locked. |
| PDP-053 | B2 | Note | metaobject `note` | shared (owner proposal) | Right here. | Right here. | none | Locked. |
| PDP-054 | B2 | Story | theme-local PDP story override (D7 resolved 9 Oct) | theme-local (st-foundation) | The room is crowded. Everyone seems to know where to go. Then a familiar hand reaches back for yours. No big speech. Just a small reminder that you don’t have to find your way through alone. | At the doorway, she slows down. You reach back and her fingers find yours. Lilac, burgundy tips, one small squeeze. Koi jaldi nahi. You’ll walk in together. Haath do. Main hoon. | none | D7 resolved: theme-local override installed; the shared `story` field is untouched. 31 words. Changed from Appendix A: the semicolon is gone, and “No need to rush her” is now “Koi jaldi nahi”, which is how you’d actually say it to a friend. Both hands are connected and the reassurance is gentle, with no promise of a confidence change. |
| PDP-055 | B2 | Save toggle (board bookmark) — accessible name | locale | theme-local (st-foundation) | bookmark icon (board) | Off: Save {product} · On: Saved: {product} | none | Owner 9 Oct (T23): a real Save toggle, stored on the visitor’s device. Icon-only button with `aria-pressed`. The accessible name changes with state. |
| PDP-056 | B2 | Save toggle — tooltip / visible hint | locale | theme-local (st-foundation) | — | Off: Save · On: Saved | none | Shown on hover and focus. |
| PDP-057 | B2 | Save toggle — announcement | locale (polite live region) | theme-local (st-foundation) | — | Saved on this device. · Removed from saved. | none | “On this device” is the truth: there are no accounts, so it is not synced (FACTS: stored in the browser). |
| PDP-058 | B2 | Saved list (only if st-foundation builds one) | locale | theme-local (st-foundation) | — | Heading: Saved sets · Empty: Nothing saved yet. Tap the bookmark on any set to keep it here. · Note: Saved on this device only. | none | Optional. Use it only if a saved-sets view exists; otherwise ignore the row. |

## Implementation notes for the build session
- The `story` field is shared with landing and Journal surfaces. Decision D7: either a theme-local PDP override or a reviewed shared-record change. These stories are written for the PDP slot only.
- Order inside the PDP, as Appendix A asks: title → design description → price/purchase → practical disclosures → story disclosure. The story always sits below the practical information.
