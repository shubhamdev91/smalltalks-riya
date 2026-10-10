# st-talks: anonymous live talks (10 Oct 2026)

Design: `C:\Users\SSTS\Desktop\Riya\talks\DESIGN.md`. Owner steps: `talks\OWNER-SETUP.md`. Copy request:
`talks\COPY-REQUEST.md`.

## Status (updated 10 Oct, after the TLK-154 window)

- **Data:** live.
- **Theme 186651934933:** posting is OFF. One switch: `snippets/st-talk-live.liquid` (on/off) drives the composer,
  reply box, Report, the TLK-153 notice and house rule 5 (TLK-154 while off, TLK-075 when on).
  - TLK-148 v1.4.4 privacy line is installed.
  - Verified at 390: hub, topic and thread pages; /blogs/news is identical to its pre-install baseline.
- **Backend:** live at https://small-talk-talks-backend.vercel.app (owner's Vercel, v0 chat pEcbsIUvnGe).
  - Live build is b3ce60f7f6e6; local/v0 build c91d3d11afc1 has 37 passing tests.
  - The owner's v0 Publish (OWNER-SETUP step 5.3) brings it live.
  - Not configured yet: OWNER-SETUP 1-5 are pending.
  - Decision A: per-device limits + duplicate check + store-wide flood hold. There is no IP key behind the proxy.
- **Theme write lock:** released.
- **Staged, waiting for a lock:**
  - The posting-ON window: 3 snippets + 2 blocks, talks/staged/posting-on/INSTALL.md. Its grant follows the owner's
    "talks app installed".
- **TLK-156 INSTALLED 10 Oct 15:50Z** (talks/staged/tlk156/INSTALL.md): 0-reply rows say "No replies yet" (no chevron)
  while posting is off, and revert to "First reply's yours ›" when the switch is on. Files: st-talk-row 6e40e666;
  locale 32104278 (insert-only).
- **Desktop layout (≥ 1024) INSTALLED 10 Oct 15:40Z** (talks/staged/desktop/INSTALL.md):
  - files: list 04fdc439, thread 2b96669c, start 737c910d, rules 565f3fdc, assets/st-talk-ago.js ec96ff27 (the
    landing teaser's short times; st-foundation adds the script tag);
  - layout: 8fr | 4fr, with the rules directly under the card and no sticky;
  - phones are pixel-identical.
- **Live theme:** a published copy of the build; it changes with each owner publish (186695155925 since 10 Oct 14:12Z). Never written by st-talks.
  - Posting reaches shoppers only after the owner re-publishes a fresh copy of the build.
  - The posting-ON window and real end-to-end test run on the build preview only.

## Talks UX pass: st-talks leads, st-fable wordmark/acceptance, st-copy words

- **v4** (owner round 2) is in qa/talks-ux/ (README, renders/compare-{hub,composer,thread,inline-reply}). It has:
  - a hero writing box;
  - Reddit nesting (a line per level, "−/+ n more replies", 4 levels + continue, inline reply under any comment);
  - st-fable's wordmark C in the hub and header;
  - st-copy v1.7.
  It is with st-fable for the re-check; the owner sees it alongside qa/talks-ux/wordmark/options-sheet.png.
- **Owner decisions:**
  - topics LOCKED to 5 (create second-opinions + just-venting in the talks window, then read back; something-else
    hidden);
  - no review queue;
  - ONE duplicate + publish after the talks rework lands.
- **Backend:** next deploy build b27475e7fe2b (v5 + v6 nesting + v7 no-review-queue), 53 tests;
  talks/backend/SECURITY-v5.md. The `parent` field goes on talk_reply first (talks/staged/nesting/PROPOSAL.md).
  Deploy needs the owner's OK.

## Backend state (10 Oct, verified read-only)

- /api/talks: build c91d3d11afc1, configured: true. The proxy GET /apps/talks returns {"open": false}.
- Kill switch: talk_settings/main (gid://shopify/Metaobject/616028176597) posting_open "false", set 19:37:18Z by the
  parent with the owner's OK.
  - Posts and replies are refused with 403 closed before any validation or write (verified with content-free
    POSTs).
  - Reports are not gated (all content is by_brand, so they can't write today).
- **Backend v5 prepared locally** (build 4bc0845998eb, 38 tests): fail-closed settings + ?diag=ip removed; reports
  stay ungated. Deploy only with the owner's OK: update the v0 chat, the owner clicks Publish, then verify.

## Shared data (owner-authorised for this feature; readback verified)

**Metaobject definitions:**

| Type | Definition ID | Storefront | Capabilities |
|---|---|---|---|
| talk_topic | 25691881685 | PUBLIC_READ | web pages /pages/talks/<h> |
| talk_thread | 25691914453 | PUBLIC_READ | publishable, web pages /pages/talk/<h> |
| talk_reply | 25691979989 | PUBLIC_READ | publishable |
| talk_signal | 25692012757 | NONE | private rate-limit / report records, hashed keys only |
| talk_settings | 25692045525 | NONE | — |

**Entries:**

- talk_settings `main`: posting_open true, hold_all false.
- talk_topic:
  - `all` 616028209365
  - `plot-twists` 616028242133
  - `tiny-wins` 616028274901
  - `nail-talk` 616028307669
  - `something-else` 616028340437
- talk_thread: 9 seeds with the same handles as the the-talks articles, alias "small talk", by_brand true, set
  from the `set:` tag, posted_at = article date, ACTIVE:
  - 616028438741 … 616028700885
  - Index lists `all` and per-topic are filled newest-first.
- No products, prices, policies or other shared data touched. No native comments existed. One probe talk_signal was
  created and then deleted.

**Proposal (orchestrator / owner):** unpublish the 9 the-talks articles and add URL redirects
/blogs/the-talks/<h> → /pages/talk/<h>. Until then, article.json forwards to the new page (location.replace) with
a visible link.

## Theme 186651934933: files (round 2, 10 Oct ~07:25 UTC; local md5 = remote checksum, re-read)

| File | md5 (prefix) |
|---|---|
| assets/st-talks.js | f3407219… |
| locales/en.default.json | 722c581c… (round-2 before 4170d1fd → after 722c581c; every line outside small_talk.talks.live byte-identical) |
| sections/st-talks-list.liquid | 2b427dfb… |
| sections/st-talks-thread.liquid | 56fd11fb… |
| sections/st-talks-start.liquid | d4b982af… |
| sections/st-talks-rules.liquid | 18fa01a1… (new `privacy` setting, TLK-148) |
| snippets/st-talk-avatar.liquid | 59dd5e94… |
| snippets/st-talk-config.liquid | 41dec541… |
| snippets/st-talk-row.liquid | 39181ddd… |
| snippets/st-talk-composer.liquid | 4a4c480b… |
| snippets/st-talk-alias.liquid | 9527b8ea… |
| snippets/st-talk-reply.liquid | e6109789… |
| snippets/st-talk-time.liquid | 73129d5c… (unchanged) |
| templates/blog.json, templates/metaobject/talk_topic.json | b1aedb9a… |
| templates/metaobject/talk_thread.json | f2da8414… |
| templates/article.json | 89136fb2… |

- Posting live = OFF in all three templates. The pre-launch line is TLK-153.
- Copy: st-copy v1.4 is installed: TLK-101…153 in locale, house rules TLK-072…076 + TLK-148 in templates, author
  line "{alias} · {date}".
- The retired locale keys are left in place (insert-only rule).

**Locale overlap (round 1):**

- st-foundation's 5ea097b3 (06:50–07:00) = my first live block + their small_talk.header.sign_in / sign_in_label /
  my_orders.
- My 07:01 upload 4170d1fd = 5ea097b3 + one line (`soon`). Nothing of st-foundation's was lost; proven by md5.

**Live theme:** /pages/talk/<h> and /pages/talks/<h> are a clean 404 there, and sitemap_metaobject_pages_1.xml is
empty. The seeds can stay Active.

## Verification (preview, Playwright)

- **Render** (`talks/render_check.py`), at 390 and 1280:
  - /blogs/the-talks: 9 rows, chips All* + 4 topics.
  - /pages/talks/tiny-wins: 3 rows, chip current.
  - /pages/talks/something-else: empty state.
  - /pages/talk/<seed>: thread.
  - /blogs/the-talks/<seed>: forwards to /pages/talk/<seed>.
  - 200 everywhere, no Liquid errors, scrollWidth = viewport.
- **Mock run** (`talks/qa_live.py mock 390|1280`, posting ON at the time, backend stubbed in the browser, nothing
  sent to Shopify): all pass. Results in talks/qa-mock-390.json and -1280.json.
  - Her row appears in 68–119 ms.
  - The payload has no name or email, and waits for the 2.6 s dwell.
  - Held, failed + Retry, rate-limited (text restored), server- and client-side blocked messages, reserved alias,
    reply + nested reply ordering, reply count, report confirm + fold.
- **Screenshots:** C:\Users\SSTS\Desktop\Riya\qa\talks\ (36 PNGs incl. soon-hub/soon-thread at 390/1280).
- **Backend:** `cd talks/backend && python -m unittest discover -s tests`: 28 pass.
  - All 8 GraphQL ops validated against the Admin schema.
  - The search syntax for rate limits was checked on live data.

## Open items

1. **Owner:** reconnect v0, then follow OWNER-SETUP.md (Dev Dashboard app + app proxy /apps/talks + 3 Vercel env
   vars).
2. **st-talks (needs the lock again):**
   - after the owner's setup, check that /api/talks shows `configured: true` and build c91d3d11afc1;
   - install the 3 staged snippets (talks/staged/posting-on/INSTALL.md): HD nail avatars (st-talk-avatar +
     st-talk-config → st-hd-nails-<set>, cell ×1.058 @ 50%/92.5%), then st-talk-live `on`;
   - run `qa_live.py real` at 320/390/1280;
   - delete the test posts.
3. **st-copy:** COPY-REQUEST.md (TLK-101…151 + TLK-148 "Posting opens soon…", rules TLK-074/075/076).
4. **st-fable:** visual acceptance of the composer row and nested replies against board 4 (new elements, not on the
   board).
5. **Known:**
   - Per-IP limits depend on Vercel keeping the shopper IP behind Shopify's proxy (to be tested after deploy). If it
     doesn't, device + store-wide limits still apply.
   - A determined attacker with 3 cleared devices on unknown IPs can auto-hide a post. The owner restores it in
     admin (documented).
