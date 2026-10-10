# the talks: UX direction (hub, thread, composer, teaser). st-fable → st-talks, 10 Oct 2026

The owner: very simple, structured, minimal; a Reddit-style thread for college girls and young women; inviting to post;
friendly; catchy but modestly sized type. The brand is gossip, small talk, "tea". Anonymous, no login, no IP and
moderation stay as built. Copy (lowercase voice) comes from st-copy. Renders: CURRENT | PROPOSED at 390 × 844 and
1536 × 703, for my acceptance before the owner sees them.

## 1. Type: two families only in the talks
| Role | Font | 390 | ≥ 1024 | Line-height |
|---|---|---|---|---|
| Wordmark / page H1 "the talks" (headers only) | Caveat 600 | 52 | 72 | 1 |
| Section label ("latest talks", "replies") | DM Sans 600, lowercase, +0.02em | 14 | 15 | 1.2 |
| Thread title in a list | DM Sans 600 | 17 | 19 | 1.3 |
| Thread title on its own page | DM Sans 700 | 22 | 28 | 1.25 |
| Body, excerpt, reply text | DM Sans 400 | 16 | 17 | 1.5 |
| Meta (alias · time · replies) | DM Sans 500, #5d5562 | 13 | 14 | 1.3 |
| Buttons, chips | DM Sans 600 (CTA "spill your tea": Barlow Semi Condensed 600) | 15 (CTA 20) | 15 (CTA 22) | 1 |
- No serif in the talks. The 16 px body is the floor, and it also stops iOS zooming into inputs. Measure: 68 ch max.
- Spacing on a 4 px grid. The one accent colour is #c3021d (CTA, focus, active chip).

## 2. Hub
- **Top:** wordmark, a one-line promise, then **"spill your tea"**.
  - Phone: a sticky bottom bar, full width, 56 px, safe-area aware. It hides while the keyboard is open.
  - Desktop: the button sits in the right rail.
- **Topics:**
  - Phone: one row of chips, scrollable sideways, 36 px visual / 44 px hit area. "all" first, active chip filled #c3021d with white text.
  - Desktop: a vertical topic list in the left rail.
- **Thread rows:** flat list with 1 px dividers (#efe6d8), no cards, no shadows. The whole row is one link.
  - Avatar: the set-nail disc, 40 px (44 desktop).
  - Line 1: meta "alias · 2h".
  - Line 2: title, 2-line clamp.
  - Line 3: excerpt, 1 line, desktop only.
  - Footer: a speech-bubble icon + "3 replies", or "no replies yet".
  - Row height about 92 px (phone) / 84 px (desktop): 9 rows ≈ 1.1 folds at 768. That fixes QA's 2.2-fold flag.
- **Pagination:** "load more talks" after 20 rows (button, not infinite scroll).

## 3. Thread page
- **Original post:** back link "‹ the talks", avatar 48, meta, title (22/28), body, and a reply count.
- **Replies, oldest first:** avatar 32, meta, text.
  - Nesting **depth limit 2**: a reply to a reply indents 16 px (24 desktop), with a 2 px rule (#e9dfd0) on its left.
  - Deeper replies flatten into level 2 with "↪ @alias" before the text.
  - After 6 replies, "show n more".
- **Reply box:** at the end of the list. Phone: a sticky "add your tea…" field that expands into the composer.
- **Posting off:** no field. Show st-copy's closed line in its place (TLK-153 / LND-067 tone).

## 4. Composer: one tap, guided
- "spill your tea" opens a bottom sheet (phone) or an inline panel in the right rail (desktop). Nothing navigates away.
  1. **Topic chips:** pre-selected from the current topic.
  2. **Guided starters:** st-copy writes 4–5 chips, e.g. "plot twist:", "tiny win:", "need advice:", "unpopular opinion:".
     A tap pre-fills the title start; it's a prompt, not a required field.
  3. **Title:** required, with a counter at 80 % of the limit.
  4. **Details:** optional, grows with the text.
  5. **Alias:** auto-generated, with "change" (as built).
  6. A one-line rules reminder, then the primary button "post it".
- **Errors:** inline under the field, in plain words (existing TLK-1xx keys).
- **Success:** the row appears at the top with "posted".
- **Posting off:** the sheet shows only the pre-launch line and "read along", with no form.

## 5. Empty and quiet states
- A topic with no talks: the set-nail avatar, then "it's quiet here… for now." (st-copy), then the CTA.
- A thread with no replies: "no replies yet · be the first ›" when posting is on; "no replies yet" when it's off.

## 6. Desktop (≥ 1024), also QA's Tier B talks flag
- Page frame 1240 (1440 at ≥ 1680).
- ≥ 1280: three columns.
  - Left rail: topics, 220 px, sticky.
  - Feed: max 720.
  - Right rail: 300 px, holding the CTA card, the composer panel and the house rules collapsed to 3 lines + "all rules".
- 1024–1279: feed + right rail; topics become the chip row above the feed.
- The thread page uses the same rails, with the reply box in the feed.

## 7. Minimums
- **Contrast:** text ≥ 4.5 : 1, large text and icons ≥ 3 : 1.
  - Meta #5d5562 on white is 7.1; the chip #a31a33 on #fdf0f0 is 6.9; white on #c3021d is 6.3.
- **Focus:** a visible 2 px #c3021d ring, offset 2.
- **Targets:** ≥ 44 × 44 for every tap target, with ≥ 8 px between them.
- **Motion:** sheet and panel slide in 150 ms; none under reduced motion. No layout shift when the sticky bar appears.
- Rows keep their single-link aria-label pattern; the sheet is a focus-trapped dialog that Escape closes.
