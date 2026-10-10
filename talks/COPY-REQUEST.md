# the talks (live): copy request for st-copy (from st-talks, 10 Oct 2026)

**Context:** the talks are now a real anonymous thread board. Anyone can start a talk or reply with no name, email
or login: she picks a topic (or types her own), writes, and taps Post once, and it goes live at once. A filter
blocks contact details, links and slurs, and holds posts that might name a real person for a quick check. Three
reports from different people hide a post. Each device gets a playful alias, which she can change.

**Status:**

- The placeholders below are installed theme-local in `locales/en.default.json → small_talk.talks.live.*`.
- Section settings are in templates/blog.json, metaobject/talk_thread.json and metaobject/talk_topic.json.
- Please give a "final" for each row (or "keep"), plus register IDs. I proposed TLK-101…151.
- Constraints already in the register still apply:
  - no "anonymous" promise (TLK-074 note);
  - no invented counts;
  - "small talk" is lowercase as an author.

## A. Composer (hub first row + Start-a-talk panel)

| Proposed ID | Key | Placeholder now | Notes |
|---|---|---|---|
| TLK-101 | composer_label | Your talk | Visually hidden field label. |
| TLK-102 | composer_placeholder | Spill it. Your first line is the headline. | The first line becomes the bold title. |
| TLK-104 | posting_as | Posting as {{ alias }} | Under the field. |
| TLK-104b | replying_as | Replying as {{ alias }} | Under the reply box. |
| TLK-105 | change | change | Opens the alias editor. |
| TLK-106 | alias_label | Your alias | |
| TLK-107 | alias_hint | Shown instead of your name. Saved on this device only. | True: localStorage. |
| TLK-108 | alias_save | Save | |
| TLK-109 | alias_shuffle | Shuffle | Picks a new generated alias. |
| TLK-110 | topic_label | Pick a topic | Legend over the topic chips. |
| TLK-111 | topic_own | Your own | Chip that opens a short text field. |
| TLK-112 | topic_own_placeholder | Name your topic | Max 30 characters. |
| TLK-113 | post | Post | The ↗ is an icon (board "Post ↗"). |
| TLK-114 | posting | Posting… | On her new row and in the status line. |
| TLK-115 | posted | Posted | |
| TLK-115b | view | See it | Link after posting from the panel under a thread. |
| TLK-116 | held | Held for a quick check. It shows once we’ve had a look. | Status line when the filter holds it. |
| TLK-116b | held_tag | Held for a check | Short tag on her own held row (only she sees it). |
| TLK-117 | failed | Didn’t post. | Network/server failure. |
| TLK-118 | retry | Retry | |
| TLK-119 | edit | Edit | Puts the text back in the composer. |
| TLK-132 | left | {{ count }} left | Character counter, shown under 120 left. |
| TLK-143 | rules_short | Situations, not people. No names, numbers, handles or links. | Under the composer and reply box. |
| TLK-144 | rules_link | House rules | Links to #house-rules. |
| TLK-145 | grievance | Something here about you? Email {{ email }} and we’ll take it down. | Grievance/contact line (store contact email). Owner may want a response time, e.g. "within 24 hours" (fact: owner). |
| TLK-146 | noscript | Posting needs JavaScript switched on. | |
| TLK-147 | moved | This talk has moved. | Old /blogs/the-talks/<handle> URLs forward to the new thread page. |

## B. Errors (status line, `small_talk.talks.live.errors.*`)

| Proposed ID | Key | Placeholder now |
|---|---|---|
| TLK-120 | need_topic | Pick a topic first. |
| TLK-121 | too_short | Say a little more. |
| TLK-122 | too_long | That’s a bit long. Keep it shorter. (talk max 1,200, reply max 800) |
| TLK-123 | blocked_contact | No phone numbers, emails or UPI IDs. Take it out and post again. |
| TLK-124 | blocked_link | No links. Take it out and post again. |
| TLK-125 | blocked_handle | No @handles or social IDs. Take it out and post again. |
| TLK-126 | blocked_words | That word isn’t allowed here. Say it another way? |
| TLK-127 | bad_alias | Pick another alias. No real names, and not “small talk”. |
| TLK-128 | rate_limited | Slow down a little. Try again in a few minutes. |
| TLK-129 | duplicate | You’ve already posted that. |
| TLK-130 | closed | Posting is paused right now. Back soon. |
| TLK-131 | not_found | This talk isn’t open for replies any more. |
| TLK-034 | server | That didn’t post. Check your connection and try again. (existing TLK-034 wording, reused) |

## C. Replies and reports (thread page)

| Proposed ID | Key | Placeholder now | Notes |
|---|---|---|---|
| TLK-133 | reply | Reply | On every reply (one level of nesting). |
| TLK-134b | reply_to_label | Reply to {{ alias }} | Accessible name of that button. |
| TLK-134 | replying_to | Replying to {{ alias }} | Bar above the box, and under a nested reply's meta. |
| TLK-135 | cancel | Cancel | |
| TLK-139a | report_thread_label | Report this talk | Accessible name (visible text = existing TLK-039 "Report"). Not shown on talks posted by small talk. |
| TLK-136 | report_confirm | Report this for breaking the house rules? | Inline confirm after tapping Report. |
| TLK-137 | report_yes | Yes, report | |
| TLK-139 | reported | Reported. Thanks for looking out. | The item then folds away on her device. |
| TLK-140 | hidden_for_you | You reported this, so it’s hidden for you. | Shown on later visits. |
| TLK-141 | show | Show it | Unfolds it again. |

TLK-025 "No replies yet. Go first, any alias works." stays. "any alias" is still true.

## D. Alias generator (TLK-150 / TLK-151)

The alias is adjective + noun with no space, e.g. `lowkeymomo`, `midnightkulfi`, `filmijhumka`. All 400 combinations
pass the alias rules: no real names, no slurs, at most 24 characters. Please replace or approve the two lists. Keep
them as single lowercase words, no names, and nothing that reads as a real person.

- alias_adjectives: lowkey, midnight, filmi, sleepy, rainy, golden, quiet, extra, plot, tiny, soft, late, side,
  main, dramatic, unbothered, overthinking, desi, monsoon, chai
- alias_nouns: momo, samosa, kulfi, jhumka, dupatta, bindi, chutney, pakoda, playlist, era, chapter, bestie,
  gupshup, mango, rickshaw, story, twist, launch, overthinker, diary

## E. Changed section settings (house rules, now true for the live board)

| ID | Old | Placeholder now |
|---|---|---|
| TLK-074 | Your alias is the only name anyone sees. Your email stays private. | Your alias is the only name anyone sees. No email, no account. |
| TLK-075 | Replies go live straight away. We read them, and we take down anything that breaks these rules. | Talks and replies go live straight away. Our filter holds anything that might name someone for a quick check, and we take down what breaks these rules. |
| TLK-076 | Spotted something that breaks the rules? Email us at {email} with the link. | Tap Report on anything that breaks these rules. Three reports and it’s hidden until we’ve checked. Something about you? Email {email} and we’ll take it down. |
| TLK-038 | (rule line under the reply box) | Now the shared TLK-143 line + "House rules" link + grievance line. |
| TLK-052 | Topic select options incl. "Something else" | Topics are now chips from Shopify (talk_topic entries: Plot twists, Tiny wins, Nail talk, Something else) plus "Your own". |
| TLK-060 / TLK-058 | "We’ll read it and may post it as a thread" | Retired: talks now go live at once. |

**Retired:** the contact-form strings TLK-053/055/056/059/060/061 and the reply-box email strings TLK-029/030/036.
They are no longer rendered, and the locale keys stay until you confirm.
