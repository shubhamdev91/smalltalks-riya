# the talks: anonymous threads (design note, 9 Oct 2026)

Owner goal: a candid, Reddit-style thread board. A shopper picks a topic (or types her own), writes inside the thread
UI and taps once. Her talk shows straight away. Replies work the same way. She needs no name, email or login.

## 1. Data: Shopify metaobjects (shared data, owner-authorised for this feature)

Each definition is merchant-owned. "Publishable" means it has Shopify's own **Active / Draft** status, and that status
is the moderation switch: Liquid never renders a Draft entry.

| Type | Storefront | Capabilities | Fields |
|---|---|---|---|
| `talk_topic` | read | web pages `/pages/talks/<handle>` | `label`, `position`, `pickable`, `threads` (list → talk_thread, newest first, max 1,024) |
| `talk_thread` | read | publishable, web pages `/pages/talk/<handle>` | `title`, `body`, `topic` (→ talk_topic), `topic_label` (her own words), `alias`, `avatar` (set key), `by_brand`, `posted_at`, `replies` (list → talk_reply, in display order), `reply_count`, `last_reply_at`, `report_count`, `mod_note`, `source` |
| `talk_reply` | read | publishable | `thread` (→ talk_thread, filterable), `parent` (→ talk_reply, one level deep), `body`, `alias`, `avatar`, `by_brand`, `posted_at`, `report_count`, `mod_note` |
| `talk_signal` | **none** | — | private rate-limit records: `kind`, `ip_key`, `device_key`, `target`, `body_key`, `at`. Keys are salted HMACs, never raw IPs or device ids. Pruned after 7 days (every write + daily cron). |
| `talk_settings` | **none** | — | one entry `main`: `posting_open` (kill switch), `hold_all` (pre-moderate everything), `extra_blocked`, `extra_held` (one word per line) |

Liquid can't query by field, so the backend keeps index lists. `talk_topic` entry `all` holds every thread, and each
topic holds its own. A thread is added to the lists when it is created, whatever its status. Drafts simply don't
render, so publishing a held post in admin puts it in the right place with no extra step.

Seeds: the 9 `the-talks` articles become `talk_thread` entries with the same handles. They are `by_brand`, alias
"small talk" (TLK-008), the set from their `set:` tag, and `posted_at` = the article date. The old article URLs
forward to the new thread pages. **Proposal for the orchestrator:** unpublish the 9 articles and add URL redirects
once the new threads are live.

## 2. Write path

- **Backend:** one Vercel Python app (`app.py`, a standard-library WSGI `app`, entrypoint set in pyproject.toml), testable on
  this machine. Source is in `talks/backend/` (`app.py`, WSGI entrypoint). It is deployed through the Vercel (v0) connector.
- **Route:** App Proxy `/apps/talks` → `https://<project>.vercel.app/api/talks`. The backend checks Shopify's HMAC
  `signature`. Fallback: direct calls with CORS locked to the store domains, chosen by one theme setting.
  - Open point: Vercel overwrites `X-Forwarded-For` behind a proxy, which would hide the shopper's IP. I'll test it
    after deploying. If the IP is lost through the proxy, the per-IP limit uses direct mode or falls back to the
    device and global limits.
- **Admin access:** a Dev Dashboard app created by the owner, using the client-credentials grant. The 24 h token is
  fetched and cached by the backend.
  - Env vars are pasted by the owner in Vercel: `SHOPIFY_SHOP`, `SHOPIFY_CLIENT_ID`, `SHOPIFY_CLIENT_SECRET`.
  - No token ever goes in the theme or in this folder.
- **API:** `POST /apps/talks` with a JSON body:
  - `{action:"post", topic, topic_own?, text, alias, avatar, device, hp, t}` returns
    `{ok, thread:{handle,url,title,body,status:"live"|"held"}}`
  - `{action:"reply", thread, parent?, text, alias, avatar, device, hp, t}` returns `{ok, reply:{…}}`
  - `{action:"report", target:"thread:<h>"|"reply:<h>", device}` returns `{ok, hidden}`
  - Errors come back as `{ok:false, code}`. The codes are `blocked_contact`, `blocked_link`, `blocked_handle`,
    `blocked_words`, `bad_alias`, `too_short`, `too_long`, `need_topic`, `rate_limited` (+`retry_after`),
    `duplicate`, `closed`, `not_found` and `server`.
- **Title:** the first line (or first sentence, up to 110 characters) becomes the bold headline. The rest becomes
  the body.

## 3. Safety (invisible to honest users)

- **Alias:** a playful alias is made per device and kept in `localStorage`, together with a random set-nail avatar
  and a device ID. She can edit the alias. It must be 2–24 characters, pass the filters, and can't be "small talk",
  "admin", "mod" or "official".
- **Bot checks:** a honeypot field, plus a minimum of 2.5 s between opening the composer and posting. Bots get a fake
  success and nothing is stored.
- **Rate limits:** checked per device key and per IP key (when the IP is visible) against `talk_signal`, plus a
  per-instance burst guard.
  - Talks: 3 per 10 min and 10 per day. Replies: 8 per 10 min and 60 per day. Reports: 20 per day.
  - The same text twice in 24 h counts as a duplicate.
  - Global flood guard: more than 40 talks or 200 replies in an hour store-wide sends new posts to review instead of
    blocking them.
- **Blocked:** phone numbers (8+ digits, incl. spaced/dotted, +91), emails (incl. "at gmail dot com"), @handles and
  "insta/snap/ig: name", URLs and domains, and a slur list (English + Hindi/Hinglish, leetspeak-normalised).
  - The owner can add words in `talk_settings`.
  - The same checks run in the browser first, for instant feedback. The server is the authority.
- **Held for review (created as Draft):** posts that look like they name or target a real person:
  - common surnames or distinctive first names
  - "her name is / uska naam"
  - two capitalised words mid-sentence
  - college/office/society identifiers
  - expose/leak/"everyone should know"/address language
  - the owner's `extra_held` words, `hold_all`, or the flood guard
- **Report:** on every thread and reply. One report per device per item. The third distinct reporter switches the
  item to Draft with `mod_note` "auto-hidden: 3 reports", and the reply count is recounted.
- **Owner moderation:** Shopify admin → Content → Metaobjects → Talk thread / Talk reply. Draft hides, Active
  publishes, Delete removes, and `mod_note` says why.
- **Under the composer:** short rules and a grievance/contact line, with wording from st-copy.

## 4. Theme (theme 186651934933 only, talks files only, under the write lock)

- **Hub:** `/blogs/the-talks` keeps the board header. Topic chips link to `/pages/talks/<topic>`; with JS, the list
  swaps in place through the Section Rendering API. The composer is the first row of the list ("inside the thread
  interface"), with her avatar, "as {alias} · change", topic chips + "your own", a textarea and one Post pill.
  Under that come the rows (paginated by 10, newest first) and the handwritten panel.
- **Thread page:** `templates/metaobject/talk_thread.json`. Back link, avatar, alias · time, title, body and reply
  count, then replies as a Reddit-style tree: red thread rule, one level of nesting, "Reply" on each reply. The board
  reply box has no fields beyond the text, the Start-a-talk panel uses the same composer, and the house rules follow.
- **Topic page:** `templates/metaobject/talk_topic.json` uses the hub section with the topic selected.
- **Files:** `st-talks-list`, `st-talks-thread`, `st-talks-start` and `st-talks-rules` are rewritten.
  `st-talk-avatar` gains a `set` parameter. There are new snippets for the row, composer and reply. `st-talks.js` is
  rewritten. `blog.json` and `article.json` change, and the 2 metaobject templates are added. Strings are section
  settings keyed to new register IDs (TLK-1xx), with placeholders until st-copy delivers.

## 5. UI states

| State | What she sees |
|---|---|
| **empty** | TLK-013 and the composer. |
| **posting** | Her row appears at the top (or her reply at the end) at once, marked "posting…". The draft is saved locally. |
| **posted** | The marker becomes "just now" and the row links to the thread. A local copy covers storefront cache lag for 10 min. |
| **held** | Her row stays visible to her only, with "held for a quick check". |
| **failed** | Network or server error: "Didn't post" + Retry + Edit. The text is never lost. |
| **blocked / rate-limited / closed** | The row is removed, her text goes back in the composer, and a specific message is shown. |
| **reported** | "Reported. Thanks." The item folds away on her device, with a "show" link. |

## 6. Performance (owner: "don't make the site slower")

- **Server-side rendering:** reads are plain Liquid on Shopify's servers, like the blog today. Pages are paginated
  (10 threads, or 50 replies, per page), and the index lists mean a render never scans the whole table. There are no
  extra requests on page load.
- **Backend:** runs only on Post, Reply or Report. The app adds no script tag, app embed or app block anywhere. Home,
  shop, PDP and bag are untouched.
- **JS:** one small deferred module, loaded only on talks pages. Topic switching and posting use fetch with no page
  reload.
- **Avatars:** reuse the hero's existing `st-nails-<set>.webp` sprites (often already cached). Rows below the fold
  use `content-visibility:auto`.
- **Posting latency** (about 1–3 s, a cold start adds less than 1 s) is hidden by the optimistic UI and never blocks
  the page.

## 7. Decisions the orchestrator asked to see (added 10 Oct, after the build)

**Migration:**

- The 9 seed threads became talk_thread entries with the same handles (alias "small talk", by_brand, set from their
  `set:` tag, original dates).
- **Existing comments: none.** The Admin `comments` query returned 0, so nothing needed migrating and no reply was
  invented.

**Blog and Start-a-talk form:**

- `/blogs/the-talks` stays the hub URL, so header, footer and landing links are unchanged. The blog page now renders
  the metaobject feed.
- Old article URLs forward to `/pages/talk/<handle>`. Proposal: unpublish the 9 articles and add redirects.
- The Start-a-talk **contact form is retired**. The same panel (#start-a-talk, board styling) now holds the live
  composer, and nothing goes to email.
- The native comment form (name + email) is gone.
- The blog's comment setting is untouched (shared data). It no longer matters because the theme renders no
  comment form.

**Moderation default (owner):**

- Talks and replies go **live immediately**.
- The safety net is: filters (block, or hold as Draft) + Report + auto-hide at 3 distinct reporters + admin
  Draft/Active/Delete.
- The owner can switch everything to pre-moderation with Talks settings → "Hold every new post", or pause posting
  with "Posting open".

**Privacy:**

- The talks never ask for or store a name, email, phone number or account.
  - A signed-in customer is not linked: the post only notes "signed-in customer", never the ID.
- Raw IP addresses are never stored or logged.
  - Network and device are kept as salted one-way HMAC keys (24 hex characters) in the private `talk_signal` type
    (storefront NONE).
  - These are used only for rate limits, duplicate checks and one-report-per-person.
  - The salt is the owner's own `TALKS_SALT` Vercel env var (owner step). If it's missing, a salt is derived from
    the client secret, so no key is ever unsalted.
  - Device ids are never stored raw either, only as the salted key.
- **Retention:** `talk_signal` rows older than 7 days (`SIGNAL_DAYS`) are deleted on every post, reply and report,
  in parallel with no added latency, and by a daily Vercel Cron (`/api/talks?task=prune`, 03:17 UTC).
  - So no row outlives about 8 days even when nobody posts.
  - The shopper-facing line TLK-148 promises "within 30 days", which holds.
  - **Decision A (10 Oct, after the deploy test):** Vercel replaces the forwarded shopper address with the proxy's.
    So behind the App Proxy the code never uses or stores a network/IP key (enforced in `handle_request`).
    Limits are the device key + the duplicate check + the store-wide flood hold.
  - TLK-148 → st-copy's device-only wording. Only the optional direct (CORS) mode would key the network.
- Function logs record action, result and timing only: no text, no IP.
- The alias, avatar and device ID live in the shopper's own browser (localStorage).
- A grievance/takedown line (store contact email) sits under every composer and reply box, and the house rules
  explain Report.
- **Owner flag:** the store privacy policy should gain a short talks paragraph (public posts under an alias;
  scrambled device/network code kept for at most 30 days to stop spam; alias stored only in the browser). Text by
  st-copy, pasted by the owner.

**Filters:**

- The contact, link and slur blocks and the real-person/defamation hold are always on in code. There is no switch to
  turn them off.
- The owner can only make them stricter: extra words, "Hold every new post", "Posting open" off.
- Review cadence: daily, plus on any takedown email (click path in OWNER-SETUP.md).

**Deploy:**

- The backend deploys only to the owner's own Vercel account (through the v0/Vercel connector the owner connects).
- It needs the owner's explicit OK in the st-talks session first.
- No secret is ever in the theme, this folder or a chat.

**Seeds and blog:** unpublishing the 9 articles plus the /blogs/the-talks/<h> → /pages/talk/<h> redirects is
owner proposal **SD29** (not done by st-talks).

**Posting live switch:**

- This is a section setting ("Posting live", in 3 templates).
- While the backend isn't configured it stays off, and pages show the pre-launch line (TLK-153 "Posting isn't open
  yet. Read along for now.") instead of a box that can't post (orchestrator condition). Report buttons are hidden
  too.

**Copy:**

- Strings live in the locale (`small_talk.talks.live.*`, the convention the register maps to), not in section
  settings.
- The slots are in COPY-REQUEST.md.

## 8. Owner steps (secrets: owner only; full click path in `talks/OWNER-SETUP.md`)

1. **Admin:** Settings → Apps → Develop apps → Build apps in Dev Dashboard → Create app "Small Talk talks".
2. **New version:**
   - Scopes: `read_metaobjects, write_metaobjects, write_app_proxy`.
   - App URL: the Vercel URL. Embed in admin: off.
   - App proxy: prefix `apps`, subpath `talks`, URL `https://<project>.vercel.app/api/talks`.
   - Release, then install on the store.
3. **Copy credentials:** Dev Dashboard → App settings → Client ID + Client secret.
4. **Vercel:** project → Settings → Environment Variables. Add `SHOPIFY_SHOP=0nev20-vn.myshopify.com`,
   `SHOPIFY_CLIENT_ID`, `SHOPIFY_CLIENT_SECRET` and `TALKS_SALT` (a long random string), then redeploy.
5. **Tell the orchestrator.** I then run the end-to-end check and delete the test posts.
