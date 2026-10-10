# the talks: UX pass (v0 draft, 10 Oct). st-talks leads; st-fable sets type/layout and accepts; st-copy writes

**Status:** lab only, no theme writes. These are DRAFT renders for st-fable's direction. Copy is marked DRAFT until
st-copy signs it off (slots U1–U17, `lab/copy.json`).

## The owner's ask (relayed by the orchestrator)

Reddit-like but softer, for college-going young women:

- a clear topic list, and threads with alias + avatar + time + reply count;
- nested replies;
- an obvious one-tap "spill your tea" composer with short guided prompts;
- a friendly empty state;
- minimal chrome, and a tight type scale: a catchy display font for headers only, a readable sans for posts, no
  giant headings;
- a lowercase candid voice, strong contrast, thumb-friendly.

It also absorbs QA Tier B (9 rows as a single stack, about 2.2 folds, 13–15 px text).

## Renders

All are in `renders/`. The **compare** sheets put the current build and the proposal side by side.

| Screen | 390 × 844 | 1536 × 703 |
|---|---|---|
| Hub | `compare-hub-390x844.png` | `compare-hub-1536x703.png` |
| Composer ("spill your tea") | `compare-composer-390x844.png` | `compare-composer-1536x703.png` |
| Thread | `compare-thread-390x844.png` (+ `compare-thread-replies-390x844.png`) | `compare-thread-1536x703.png` |
| Landing teaser | `compare-teaser-390x844.png` | `compare-teaser-1536x703.png` |
| Extra states (proposed only) | `proposed-hub-prelaunch-390x844.png`, `proposed-empty-390x844.png` | |

**How these were made:**

- **CURRENT** (`lab/current_capture.py`): the build preview.
  - The composer, the reply box and replies are injected with the exact markup the Liquid renders once posting is
    ON. Posting is off on the build today, so they can't otherwise be seen.
- **PROPOSED** (`lab/proposed_capture.py` + `lab/proposed.css`): the same preview pages (real header, footer, fonts,
  nail sheets) with the talks area swapped for the proposed markup.
- **Data:** the 9 real threads (`lab/data.json`).
- **Sample content** (review only, never shipped): the thread's 3 replies, and the "3 replies" count on the first card.
  They exist so nesting and counts can be seen.
- Renders show the posting-ON state. The pre-launch variant is shown on the phone hub.

## Proposal

**1. One feed of compact cards (the hub)**

- **Header:** "the talks" in Caveat (40 px phone / 52 desktop), with the one-liner next to it. This replaces the 95 px
  serif H1, the italic tagline, the sub and the big pill.
- **The one-tap bar** sits under the header: the shopper's own nail avatar, "spill your tea…", and a red ↗.
  - One tap opens the composer.
  - While posting is off, the bar turns dashed and quiet, with the pre-launch line.
- **Topic chips:** lowercase, 44 px tall, the teaser's pink/burgundy. They scroll sideways on phones; the selected
  chip is scrolled into view.
- **Feed:** "latest · n talks", then cards. Each card has:
  - avatar 32 + alias (600) · short time + a topic tag;
  - the title (DM Sans 700, 17/19 px);
  - one or two lines of the body (15/16 px muted);
  - "💬 n replies" or "no replies yet".
  - The whole card is one link.
- **House rules:** collapsed into one row ("house rules · 30-second read ›"). The full text stays on the page, inside
  `<details>`.
- **Sign-off:** a small handwritten line ("different thoughts. same energy. ♡").

**2. Composer, "spill your tea"**

- **Phone:** a bottom sheet. **Desktop:** a 560 px dialog.
- **Step 1, "what's it about?":** the topic chips + "your own".
- **The box:** "first line = your headline. then the tea." The first line still becomes the title, exactly as the
  backend splits it today.
- **Guided starters:** 2 dashed chips per topic, which drop a starter into the box.
- **Alias:** "posting as {alias} · shuffle". The alias is generated per device, as now.
- **Button:** a full-width "post it" (#c3021d, 52 px), then "no name, no login. just your alias." and a house rules
  link.
- **After posting:** the card appears at the top of the feed at once (optimistic, as now).

**3. Thread, Reddit-style**

- **Top:** "← the talks", then the original post as a card: avatar 44, alias · time · topic, title 22/28, body 17/18,
  "n replies" and a quiet "report".
- **Replies:** a light list.
  - Each reply has an initial avatar 28 on her set colour, alias · time, the body (16/17 px), and "reply · report".
  - **Nesting:** one indented level with a soft pink connector and "↪ alias".
- **Phone reply bar:** sticky at the bottom ("add your two cents…" + ↗, "replying as {alias} · shuffle").
- **"got your own tea? spill it ›" card:** this replaces the big Start-a-talk panel.

**4. Desktop (≥ 1024), a Reddit-like 3-column layout in the shared frame (min(1240 px, 100% − 2 gutters))**

- **Left, sticky (220 px):** "the talks", the one-liner, and the topic nav with counts.
- **Centre (≤ 680 px):** the bar + the feed (or the thread).
- **Right, sticky (300 px):** "how it works" (3 lines: alias / quick check / 3 reports), then the house rules link and
  the grievance line. On a thread it also has the "spill your tea" bar.

**5. Landing teaser:** same heading. The board rows become the same cards, and the CTA becomes the same one-tap bar +
"see all talks ›". It is one component everywhere.

**Type scale:** only fonts already on the site, so no new downloads.

| Role | Font | Phone | Desktop |
|---|---|---|---|
| Display (headers only) | Caveat 600–700 | 40 / 34 / 30 / 24 | 52 / 34 / 28 |
| Card title | DM Sans 700 | 17 | 19 |
| Original-post title | DM Sans 800 | 22 | 28 |
| Body | DM Sans 400 / lh 1.5 | 16–17 | 17–18 (≤ 64 ch) |
| Meta | DM Sans 400/600 | 13 | 13–14 |
| Chips / buttons | DM Sans 600 | 14 / 15–16 | 14 / 15–16 |

- **Colours:** ink #1a1a2e, muted #5d5562 (6.6 : 1), chip #fdf0f0 / #a31a33 (6.9 : 1), CTA #c3021d (6.3 : 1 white).
- **Targets:** every target is ≥ 44 px, except reply/report (40 px, with 10 px padding on both sides).

**Density, measured with the 9 real threads** (QA Tier B):

| Viewport | Talks in the first screen, current → proposed | Feed length in screens, current → proposed |
|---|---|---|
| 390 × 844 | 1 → 3 | 2.51 → 1.90 |
| 1536 × 703 | 1 → 3 | 2.25 → 2.04 |
| 1680 × 1050 | 3 → 5 | 1.48 → 1.37 |
| 1920 × 1080 | 3 → 5 | 1.47 → 1.33 |

Text goes up from 13–15 px to 16–19 px for titles and bodies.

## Constraints, unchanged by this pass

- **Privacy:** anonymous; no name, email or login; no IP.
- **Spam limits:** the decision-A device key, the burst guard, rate limits, duplicate check and flood hold.
- **Moderation:** blocked contact details / links / slurs; held possible real names; 3 reports auto-hide; owner
  Draft/Active.
- **Backend and data model:** unchanged. This is a theme-only pass: no new fields, and post = text + topic + alias +
  avatar as now.
- **Nesting depth:** 2 levels, i.e. a reply plus one nested level.
  - A reply to a nested reply stays at that level with "↪ alias". This is how the backend already stores
    `depth` 0/1 and orders a reply after its parent's block.
  - Deeper indents would crowd a 390 screen.
- **Topic counts:** from the topic lists the theme already reads.
- **Short times (1d / 3h):** use the st-talk-ago module.

## Implementation sketch (after the owner's approval; pairs with the posting-ON window)

- **Files:** st-talks-list / -thread / -rules / -start, st-talk-row, st-talk-reply, st-talk-composer and st-talks.js.
- **st-talks.js additions:** sheet open/close with focus trap and Esc, starter insertion, and the sticky reply bar.
- **st-foundation:** the teaser rows and CTA in st-teaser.
- **Locale:** the U-slots, insert-only.
- **Checks:** phones are re-baselined, because this pass intentionally changes them.
