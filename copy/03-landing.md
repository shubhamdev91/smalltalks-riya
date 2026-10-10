# 03 — Landing page (home)

Copy register v1.3 · 9 Oct 2026 · nothing here is written to Shopify.

Source: board 3.jpg (full landing sequence), brief §8 order: hero → brand/vision + Shop tiles → Diet Cherry → the talks → Brainwave → Green Flag → Journal → Nail Guide → Shaadi Shift → On Me → Wild Card → Pinky Promise → Shop all / FAQ / footer.
Gate IDs and decisions: see `00-register.md`.

## Hero (7 states, driven by the campaign metaobject)

| id | batch | slot | destination | scope | current text | new text | fact gate | notes |
|---|---|---|---|---|---|---|---|---|
| LND-001 | B1 | Note, On Me | metaobject `note` | shared (owner proposal) | I’ve got this. | I’ve got this. | none | Locked. |
| LND-002 | B1 | Note, Brainwave | metaobject `note` | shared (owner proposal) | Called it. | Called it. | none | Locked. |
| LND-003 | B1 | Note, Diet Cherry | metaobject `note` | shared (owner proposal) | My usual. | My usual. | none | Locked. |
| LND-004 | B1 | Note, Green Flag | metaobject `note` | shared (owner proposal) | Sorted. | Sorted. | none | Locked. |
| LND-005 | B1 | Note, Shaadi Shift | metaobject `note` | shared (owner proposal) | On duty. | On duty. | none | Locked. |
| LND-006 | B1 | Note, Wild Card | metaobject `note` | shared (owner proposal) | Your move. | Your move. | none | Locked. |
| LND-007 | B1 | Note, Pinky Promise | metaobject `note` | shared (owner proposal) | Right here. | Right here. | none | Locked. |
| LND-008 | B1 | Headline (×7) | metaobject `headline` | shared (owner proposal) | (locked list) | unchanged | none | See 01-pdp. |
| LND-009 | B1 | Hero CTA | theme section setting (template: “Shop {name}”) | theme-local (st-foundation) | Shop “On Me” ↗ | Shop “{name}” ↗ | none (G5 met 9 Oct) | Owner 9 Oct, board match (board 2): curly quotes around the set name, e.g. Shop “On Me” ↗. This supersedes my v1 no-quotes note. Accessibility: wrap ↗ in `aria-hidden="true"` so screen readers hear “Shop “On Me””, not “north east arrow”. The quotes use typographic “ ” (U+201C/U+201D), never straight quotes. |

## Brand/vision + Shop tiles (two-tile gallery)

| id | batch | slot | destination | scope | current text | new text | fact gate | notes |
|---|---|---|---|---|---|---|---|---|
| LND-010 | B1 | Tile 1 label → `/pages/our-story` | theme section setting | theme-local (st-foundation) | Our Vision ↗ | Our Vision ↗ | none | Owner 9 Oct, board match (T2). Still links to `/pages/our-story`; there is no vision page. ↗ is `aria-hidden`. SEO note: the label no longer matches the destination name (STRATEGY §4), so st-fable is told. |
| LND-011 | B1 | Tile 2 label → Shop | theme section setting | theme-local (st-foundation) | Shop all nails ↗ | Shop all nails ↗ | none | Owner 9 Oct, board match (T3). → `/collections/all`. Elsewhere the same destination says “Shop all sets” (LND-044, footer, Our Story). The board has both, and st-fable is told. |
| LND-012 | B1 | Tile 1 image alt | theme section setting (image alt) | theme-local (st-foundation) | — | Illustration: a woman with a bindi resting her hand on her cheek, nails burgundy and gold. | none | HD batch 2 (10 Oct), checked against artwork/hd (manifest hd.batches["chatgpt-AB-1"]). hd/tiles/our-vision-woman. 90 chars. Replaces the bill-slip alt (the old tile art). |
| LND-013 | B1 | Tile 2 image alt | theme section setting (image alt) | theme-local (st-foundation) | — | Illustration: ten nails from every set, packed tight: burgundy, tortoiseshell, emerald, lime, cobalt, checks, lilac and red. | none | Rewritten 9 Oct to the board-3 collage as the orchestrator described it: 10 nails edge to edge, all seven sets, no silver. 124 chars. Names the main colours once each (blush, under the red tip, is left out for length). The asset file wasn’t in artwork/, so I wrote this from the orchestrator’s description. Checked 9 Oct against the lab render tiles-390.png: matches (10 nails, all seven sets, no silver). |

## Chapter captions (one handwritten line each; headline + name + CTA come from the metaobject)

| id | batch | slot | destination | scope | current text | new text | fact gate | notes |
|---|---|---|---|---|---|---|---|---|
| LND-014 | B1 | Diet Cherry caption | theme section setting (chapter block) | theme-local (st-foundation) | New plans. Same favourite. | New plans. Same favourite. | none | Owner 9 Oct, board match (T4). |
| LND-015 | B1 | Brainwave caption | theme section setting | theme-local (st-foundation) | You had the thought. You did the work. | You had the thought. You did the work. | none | Keep. |
| LND-016 | B1 | Green Flag caption | theme section setting | theme-local (st-foundation) | Plans fell apart? Bring yourself. | Plans fell apart? Bring yourself. | none | Owner 9 Oct, board match (T5). |
| LND-017 | B1 | Shaadi Shift caption | theme section setting | theme-local (st-foundation) | Her big day. Your cue. | Her big day. Your cue. | none | Keep. |
| LND-018 | B1 | On Me caption (top) | theme section setting | theme-local (st-foundation) | Good company. One more round. | Good company. One more round. | none | Keep. |
| LND-019 | B1 | On Me caption (bottom, board shows two) | theme section setting | theme-local (st-foundation) | Before anyone starts splitting… | Before anyone starts splitting… | none | Optional second line near the bill art. Drop it if the layout allows only one. |
| LND-020 | B1 | Wild Card caption | theme section setting | theme-local (st-foundation) | Cards down. Smile on. | Cards down. Smile on. | none | Owner 9 Oct, board match (T6). The owner chose the board over the pose. |
| LND-021 | B1 | Pinky Promise caption (top) | theme section setting | theme-local (st-foundation) | Crowded room. Familiar hand. | Crowded room. Familiar hand. | none | Keep. |
| LND-022 | B1 | Pinky Promise caption (bottom) | theme section setting | theme-local (st-foundation) | Same people. Different days. Still us. | Same people. Different days. Still us. | none | Optional second line. |
| LND-023 | B1 | Chapter CTA (×7) | theme section setting (label) | theme-local (st-foundation) | Shop set ↗ | Shop set ↗ | none (G5 met 9 Oct) | Owner 9 Oct, board match (T7). Accessible name: “Shop {name}”. ↗ `aria-hidden`. |
| LND-024 | B1 | Chapter product name (×7) | product title | shared (owner proposal) | (names) | unchanged | none | Locked. v1.4.7 (10 Oct), owner design change: the name is the chapter’s focal point, shown in curly double quotes, e.g. “Diet Cherry”. The quotes are presentation only: U+201C and U+201D in `aria-hidden="true"` spans around the name inside `p.st-ch__name`, so screen readers hear just “Diet Cherry”. Prefer spans to CSS `::before/::after`, because generated content is read aloud by some screen readers. No locale key and no new string: the name still comes from the campaign record. The Shop pill stays a separate element (visible LND-023 “Shop set ↗”, accessible name “Shop {name}” from `small_talk.chapter.shop_set_name`, MC-051). |

## the talks teaser

| id | batch | slot | destination | scope | current text | new text | fact gate | notes |
|---|---|---|---|---|---|---|---|---|
| LND-025 | B1 | Heading | theme section setting | theme-local (st-foundation) | the talks | the talks | none | Locked lowercase. v1.4.9: stays “the talks” (already lowercase, locked). |
| LND-026 | B1 | Subheading | theme section setting | theme-local (st-foundation) | A little less filtered. | a little less filtered. | none | Owner 10 Oct: candid, all lowercase, like a real thread. Same words, lowercase. |
| LND-027 | B1 | Example label | theme section setting | n/a (superseded) | Example talk | Example talk | none | SUPERSEDED v1.4.9: the single example bubble is replaced by a slice of the real board (LND-063…067). Keep it visible so no one mistakes the example for a live post. |
| LND-028 | B1 | Example post | theme section setting | n/a (superseded) | Anyone else rehearse a text and still send ‘hey’? | Anyone else rehearse a text and still send ‘hey’? | none | SUPERSEDED v1.4.9 (real threads now; the same question lives on as seed thread TLK-080). Owner 9 Oct, board match (T8). The same question is seed thread TLK-080, so the teaser has a real thread behind it. |
| LND-029 | B1 | Example alias | theme section setting | n/a (superseded) | Velvet Mango | Velvet Mango | none | SUPERSEDED v1.4.9: no example alias. Real threads show their real alias (seed threads: “small talk”). An invented alias, the same one used on the talks page. No @ handle: that could collide with a real account. |
| LND-030 | B1 | “…” overflow button | decorative chip inside the teaser card | n/a (dropped) | ••• | ••• (decorative, `aria-hidden`, no button) | none | DROPPED v1.4.9: the slice has no overflow chip. Owner 9 Oct, board match (T9). Shown as drawn, but it is not a control: no menu exists, so no focus stop and no accessible name. |
| LND-031 | B1 | CTA → `/pages/the-talks` | theme section setting → `/blogs/the-talks` | theme-local (st-foundation) | Join the conversation ↗ | spill your tea ↗ | none (G10 met: the talks is real, F14) | Owner 10 Oct: candid, all lowercase, like a real thread. Exactly the owner’s words. ↗ `aria-hidden`. Accessible name: “spill your tea on the talks” (says where it goes, since the pill sits under a slice of threads). Replaces “Join the conversation ↗” (T10). Optional, owner’s call: while posting is closed, “sip the tea ↗” (= read along) would match the pre-launch board exactly. The default stays “spill your tea”. |
| LND-032 | B1 | Caption | theme section setting | theme-local (st-foundation) | Real conversations on friendship, plans, overthinking and everything in between. | real talk on friendship, plans, overthinking and everything in between. | none (G10 met) | Owner 10 Oct: candid, all lowercase, like a real thread. Lowercase, and “real conversations” becomes “real talk” (the idiom = candid talk). That stays true even while posting is closed and the seed threads have no replies yet; “real conversations” would point to activity that doesn’t exist yet. Fallback if the owner wants the board words: “real conversations on friendship, plans, overthinking and everything in between.” |
| LND-063 | B1 | Talks slice: list label (small, above the threads) | theme section setting | theme-local (st-foundation) | — | latest talks | none | v1.4.9. Same idea as TLK-007, in lowercase. If the board has no visible label, use it as the list’s accessible name. |
| LND-064 | B1 | Talks slice: topic chip | rendered from the `talk_topic` label + CSS `text-transform: lowercase` | theme-local (st-foundation) | Plot twists · Tiny wins · Nail talk (data) | plot twists · tiny wins · nail talk | none | v1.4.9. Lowercase in this section only, via CSS, so the shared topic data stays unchanged. Screen readers read the words the same either way. |
| LND-065 | B1 | Talks slice: thread meta line | locale (reuse TLK-009/TLK-010 keys, lowercase in this section) | theme-local (st-foundation) | — | {alias} · {time} · {n} replies, with the replies part shown only when n > 0  (1 reply · time: just now · {n}m · {n}h · {n}d · then 9 oct) | none | v1.4.9. Real data only: alias as stored (seed threads: “small talk”), real `posted_at`, real `reply_count`. The month is lowercase too (“9 oct”). Accessible: the full row link reads “{title}, {n} replies” (TLK-011). v1.4.10: the “· n replies” part renders only when n > 0. At 0, the row shows LND-066 instead, so “0 replies” never doubles up with “no replies yet”. |
| LND-066 | B1 | Talks slice: zero-replies state | locale | theme-local (st-foundation) | — | posting open: no replies yet · be the first ›  ·  posting closed: no replies yet | none | v1.4.9. No fabricated activity: 0 shows as 0. The invite (“be the first ›”, linking to the thread) appears only while posting is open; with posting closed it would invite something people can’t do yet. |
| LND-067 | B1 | Talks slice: pre-launch line | locale (lowercase variant of TLK-153) | theme-local (st-foundation) | — | posting isn’t open yet. read along for now. | none | v1.4.9. Shown in the slice while `posting_open` is off before launch. Same words as TLK-153, lowercase. No date. |

## Journal teaser

| id | batch | slot | destination | scope | current text | new text | fact gate | notes |
|---|---|---|---|---|---|---|---|---|
| LND-033 | B1 | Heading | theme section setting | theme-local (st-foundation) | Small stories. Big feelings. | Small stories. Big feelings. | none | Keep. |
| LND-034 | B1 | Image 1 alt | theme section setting | theme-local (st-foundation) | — | Illustration: a woman in glasses and gold jhumkas writing in a notebook with a blue pen, her nails deep red. | none | HD batch 1 (9 Oct), checked against the files in artwork/hd (manifest hd.batches["board-corrections-1"]). hd/journal/journal-writing.webp. Her nails are deep red now, not cobalt. 108 chars. |
| LND-035 | B1 | Image 2 alt | theme section setting | theme-local (st-foundation) | — | Illustration: a black crescent-shaped handbag beside a blue notebook and a blue pen. | none | HD batch 1 (9 Oct), checked against the files in artwork/hd (manifest hd.batches["board-corrections-1"]). hd/journal/journal-bag-notebook.webp. Black bag, not silver; no sketchbook. 84 chars. |
| LND-036 | B1 | CTA → `/blogs/journal` | theme section setting | theme-local (st-foundation) | From the Journal ↗ | From the Journal ↗ | none | Owner 9 Oct, board match (T12). The button label is “From the Journal”, with no separate eyebrow. |
| LND-037 | B1 | Eyebrow (optional) | theme section setting | n/a (dropped) | — | — | none | Owner 9 Oct, board match (T12). Eyebrow dropped; the board has no eyebrow. |
| LND-038 | B1 | Handwritten line | theme section setting | theme-local (st-foundation) | For the plans still taking shape… | For the plans still taking shape… | none | Keep. v1.4.10 (st-fable desktop spec): hidden on phone, kept on desktop. Optional shorter phone line if the owner wants something there: “Plans still taking shape…”. |

## Nail Guide teaser

| id | batch | slot | destination | scope | current text | new text | fact gate | notes |
|---|---|---|---|---|---|---|---|---|
| LND-039 | B1 | Eyebrow | theme section setting | theme-local (st-foundation) | Nail Guide | Nail Guide | none |  |
| LND-040 | B1 | Heading | theme section setting | theme-local (st-foundation) | Find your fit. | Find your fit. | none | Keep. |
| LND-041 | B1 | Handwritten line | theme section setting | theme-local (st-foundation) | A little help, at your fingertips. | A little help, at your fingertips. | none | Keep. |
| LND-042 | B1 | CTA → `/pages/nail-guide` | theme section setting | theme-local (st-foundation) | Open the guide ↗ | Open the guide | none (G2 met: F3) | Show the teaser only once the guide has real fit content (or at least the apply/remove sections). |
| LND-043 | B1 | Image alt | theme section setting | theme-local (st-foundation) | — | Illustration: a fingertip with a bare natural nail and a measuring tape wrapped across it. | none | Rewritten 9 Oct to the accepted guide art (artwork/tests/contact-guide.png): a bare nail, not pink polish, with a measuring tape. |

## Closing block: Shop all / FAQ / footer

| id | batch | slot | destination | scope | current text | new text | fact gate | notes |
|---|---|---|---|---|---|---|---|---|
| LND-044 | B1 | Shop all CTA | theme section setting | theme-local (st-foundation) | Shop all sets ↗ | Shop all sets | none |  |
| LND-045 | B1 | FAQ heading | theme section setting | theme-local (st-foundation) | FAQs | FAQs | none | Owner 9 Oct, board match (T13). |
| LND-046 | B1 | Q1 | theme section setting (collapsible row) | theme-local (st-foundation) | How do I find my size? | How do I find my size? | none (G2 met: F3) | Owner 9 Oct, board match (T15). Board row 1. |
| LND-047 | B1 | A1 | theme section setting | theme-local (st-foundation) | — | Every kit has all 12 sizes, so there’s nothing to pick at checkout. At home, match each nail to a press-on, or measure with our Nail Guide. | none (G2 met: F3) | From FACTS F3. “Nail Guide” links to the guide. |
| LND-048 | B1 | Q2 | theme section setting | theme-local (st-foundation) | How do I apply and remove? | How do I apply and remove? | none (G3, G4 met: F4, F5) | Owner 9 Oct, board match (T14). |
| LND-049 | B1 | A2 | theme section setting | theme-local (st-foundation) | — | Prep your nails, then press on with glue (lasts up to about 2 weeks) or tabs (1–3 days). To remove, soak for 10–15 minutes and lift gently from the side. Never force them. Step by step in our Nail Guide. | none (G3, G4, G9 met: F4–F6) | From FACTS F4, F5, F6. Wear time appears here (visible copy) but never in metadata (STRATEGY). |
| LND-050 | B1 | Q3 | theme section setting | theme-local (st-foundation) | What comes in the box? | What comes in the box? | none (G1 met: F2) | Owner 9 Oct, board match (T15). Board row 3. |
| LND-051 | B1 | A3 | theme section setting | theme-local (st-foundation) | — | 24 almond press-ons in 12 sizes, nail glue, a sheet of adhesive tabs, a mini file, a prep pad, a cuticle stick and an instruction card. | none (G1, G14 met: F1, F2) | FACTS F2 short form. |
| LND-052 | B1 | Q4 (no gate) | theme section setting | n/a (dropped) | — | Are the stories real? | none | DROPPED (owner 9 Oct, T15: the board shows 3 FAQ rows). |
| LND-053 | B1 | A4 | theme section setting | n/a (dropped) | — | They’re short stories we wrote around each set. Fiction, not reviews. The moments are made up; the feelings are probably familiar. | none | DROPPED (owner 9 Oct, T15: the board shows 3 FAQ rows). Ready. |
| LND-054 | B1 | Q5 (no gate) | theme section setting | n/a (dropped) | — | Are the illustrations what I’ll get? | none | DROPPED (owner 9 Oct, T15: the board shows 3 FAQ rows). |
| LND-055 | B1 | A5 | theme section setting | n/a (dropped) | — | The illustrations are campaign art. To see the actual set, check the product photos on each set’s page. | G11 | DROPPED (owner 9 Oct, T15: the board shows 3 FAQ rows). Ready once each PDP has real product photos (G11). |
| LND-056 | B1 | Q6 (no gate) | theme section setting | n/a (dropped) | — | Which set should I pick? | none | DROPPED (owner 9 Oct, T15: the board shows 3 FAQ rows). |
| LND-057 | B1 | A6 | theme section setting | n/a (dropped) | — | Go by mood. On Me is burgundy and tortoiseshell, Brainwave is cobalt and white, Wild Card is lime with checks. All seven are in the shop, side by side. | none (G12 met 9 Oct) | DROPPED (owner 9 Oct, T15: the board shows 3 FAQ rows). Ready: all seven sets are live and in the shop. |
| LND-058 | B1 | FAQ link | theme section setting | n/a (dropped) | — | More answers in Help | none | DROPPED (owner 9 Oct: keep only if the board has room; it doesn’t). → `/pages/help`. |
| LND-059 | B1 | Footer tagline | theme section setting (footer) | theme-local (st-foundation) | Nails for real conversations. | Nails for real conversations. | none | Keep. |
| LND-060 | B1 | Footer links | footer section links (theme section setting); if the footer reads a Shopify menu, an owner menu edit | theme-local (st-foundation) | Shop · Our Story · the talks · Journal · Nail Guide · Contact · Shipping · Returns · Privacy | Nav row: Shop · Our Story · the talks · Journal · Nail Guide ¶ Legal row: Contact us · Shipping policy · Refund policy · Privacy policy · Terms | none (G6, G7, G8 met; G16 met once the owner pastes the Terms draft: F15) | Owner 9 Oct, board wins (board 3): 5 short nav labels on one row, in board order. Destinations: Shop → `/collections/all`, Our Story → `/pages/our-story`, the talks → `/blogs/the-talks`, Journal → `/blogs/journal`, Nail Guide → the guide route. Help is reached through “Contact us” (→ `/pages/help#contact`) in the legal row and through the header menu. Legal-row labels are unchanged (SEO-075…078). Terms shows once `/policies/terms-of-service` exists. |
| LND-061 | B1 | Social icon labels | theme settings (accessible names) | theme-local (st-foundation) | (icons) | Instagram icon only, accessible name “Small Talk on Instagram (opens in a new tab)” (MC-098). Pinterest, YouTube and TikTok stay hidden (no URL set). | none (D5 resolved 10 Oct: Instagram confirmed) | v1.4.8: D5 resolved 10 Oct. The owner confirmed Instagram, @smalltalks_com → https://www.instagram.com/smalltalks_com/ (footer setting, both footers). No other accounts are confirmed. For st-fable: Organization `sameAs` can now include this URL (STRATEGY §5, from the configured social setting). |
| LND-062 | B1 | Copyright | theme section setting | theme-local (st-foundation) | © 2026 Small Talk. All rights reserved. | © 2026 Small Talk. All rights reserved. | none | Owner 9 Oct, board match (T16). Render the year from the current date so it never goes stale; the text is identical in 2026. Swap in the registered business name if the owner gives one (F15). |
