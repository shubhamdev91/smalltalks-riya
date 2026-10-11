# the talks backend: security and no-review-queue, as of the next deploy (10 Oct)

**Next deploy** = v5 (fail-closed, no diag) + v6 (Reddit nesting) + v7 (no review queue).

- **Next build:** `b00440d7cd4a` (= b27475e7fe2b + row 19), **54 tests pass**. b27475e7fe2b is LIVE since 11 Oct ~06:35Z (copy: talks/staged/app-b27475e7fe2b.py).
- **Earlier local build:** `b27475e7fe2b`, **53 tests pass** (`cd talks/backend && python -m unittest discover -s tests`).
- **Live today:** `c91d3d11afc1`, with the store kill switch OFF (`talk_settings/main.posting_open = "false"`, verified
  live: `{"open": false}`, and posts/replies return 403 `closed`).
- **Proof:** every NEW test below was run against the previous build and FAILS there.

**Deploy:** the owner's OK in st-talks' session, then the store-data step, then v0 Publish, then the checks.

1. Add the optional `parent` field to talk_reply (`talks/staged/nesting/PROPOSAL.md`).
2. Update the v0 chat `app.py`; the owner clicks Publish.
3. Check that `/api/talks` shows build `b27475e7fe2b` and `GET /apps/talks` shows `{"open": false}`.

| # | Measure | Already there (live build) | New in this deploy | Test(s) |
|---|---|---|---|---|
| 1 | App-proxy HMAC on every write + timestamp freshness + this shop only | Yes: HMAC-SHA256 over sorted params with `compare_digest`; 900 s window; `shop` must equal `SHOPIFY_SHOP`; writes need a valid signature (CORS mode is off) | One end-to-end test (fresh, stale, other shop, tampered, unsigned) | `test_signature_message_matches_docs`, `test_unsigned_rejected_and_get_health`, `test_bad_requests`, **`test_hmac_required_fresh_and_this_shop_only`** |
| 2 | Posting switch fails closed | No: a missing entry meant open | **Yes**: open only when `posting_open == "true"` | **`test_settings_fail_closed`**, `test_closed_and_hold_all` |
| 3 | `?diag=ip` removed | No: it echoed forwarding headers (stored and logged nothing) | **Yes**: removed | **`test_no_diag_and_404`** |
| 4a | Strict lengths | Yes: talk 3–1200, reply 1–800, alias 2–24 (letters/numbers/space/.-'), own topic ≤ 30, title ≤ 110, request ≤ 16 KB | Explicit test | `test_need_topic_and_lengths`, `test_alias`, **`test_strict_lengths`** |
| 4b | Topic allow-list | Yes: only `pickable` talk_topic entries | **Yes**: the hidden "something-else" (home of "your own") can't be picked directly | **`test_hidden_topic_only_via_your_own`**, `test_own_topic` |
| 4c | Unicode normalisation + control characters | Yes: NFKC (stricter than NFC); control and zero-width characters stripped | Explicit test | **`test_unicode_normalised_and_controls_stripped`** |
| 5 | Output is always escaped text (no HTML, markdown or links) | Yes: Liquid `\| escape` on every user field; st-talks.js writes user text with textContent (its only `innerHTML` is a constant SVG path); the API returns plain JSON strings | Static audit as a test | **`test_theme_escapes_user_text`** (scans every talks template and st-talks.js), **`test_json_never_carries_markup`** |
| 6 | Per-device rate limits for post/reply/report + duplicate fingerprint | Yes: salted device hash; 3/10 min and 10/day posts, 8/10 min replies, 10/10 min reports; burst 4/min; duplicate text per device | Reply/report test | `test_rate_limit_and_duplicate`, `test_proxy_buckets_are_per_device`, **`test_rate_limits_reply_and_report_per_device`** |
| 7 | Bot friction without CAPTCHA or tracking | Yes: honeypot field + minimum 2 s to submit, answered with a silent fake success; nothing saved | Explicit test | `test_bot_gets_fake_success`, **`test_honeypot_and_min_time`** |
| 8 | Request body size cap | Yes: 16 KB → 413 | Explicit test | **`test_body_size_cap`** |
| 9 | No IP or PII stored or logged | Yes: no IP is used behind the proxy (decision A); the device id is stored only as a salted HMAC; logs show action/status/code/ms only | Explicit store + log test | `test_proxy_has_no_store_wide_bucket`, `test_salt_env`, **`test_no_ip_or_text_in_store_or_logs`** |
| 10 | Admin token scoped to metaobjects | Yes: app scopes `read_metaobjects`, `write_metaobjects`, `write_app_proxy` (Dev Dashboard version v1); a 24 h client-credentials token held in memory only | The code calls metaobject operations only | **`test_admin_api_surface_is_metaobjects_only`** |
| 11 | Secrets only in Vercel | Yes: `SHOPIFY_CLIENT_ID`, `SHOPIFY_CLIENT_SECRET` and `TALKS_SALT` are read from the environment (Vercel, marked Secret) | No secret in the code | **`test_no_secrets_in_code`** |
| 12 | **No review queue:** might name someone | No: these were held as Draft for the owner | **Yes**: refused at submit with `might_name` (TLK-181); nothing is saved (no talk, reply or signal) | **`test_blocked_and_might_name_refused`** |
| 13 | Blocked content refused at submit | Yes: contact details, links, handles/social ids, slurs (incl. spaced/leet), the owner's extra words | n/a | `test_contact_blocked`, `test_links_blocked`, `test_handles_blocked`, `test_slurs_blocked`, `test_extra_words` |
| 14 | Store-wide flood | No: held as Draft | **Yes**: refused with `busy` (429, TLK-182) | **`test_flood_refuses_not_holds`** |
| 15 | The only automatic removal is 3 distinct reports | Yes: auto-hide at 3 distinct devices, per talk and per reply; brand posts excepted | n/a | `test_reports_hide_after_three_distinct`, `test_reply_report_recounts`, `test_brand_posts_not_auto_hidden` |
| 16 | `hold_all` stays "false" | Data: "false" in talk_settings/main (verified) | The owner's emergency lever only | `test_closed_and_hold_all` |
| 17 | Missing or short device id rejected (no shared bucket) | Yes | n/a | `test_missing_device_is_rejected_not_bucketed` |
| 18 | Reddit nesting: parent per reply; moderation, reports and auto-hide per reply | No: depth 0/1 only | **Yes**: depth = parent + 1 (cap 8); placed after the parent's subtree; a hidden or foreign parent is refused | **`test_reddit_nesting_depth_order_and_parent`**, **`test_nesting_capped_and_hidden_parent_refused`**, `test_reply_to_hidden_thread_refused` |
| 19 | Duplicate check and per-device limits see brand-new rows | No: they read Shopify's search index, which lags new talk_signal rows by seconds; the live E2E (11 Oct) saved the same talk twice 3 s apart | **Yes** (build b00440d7cd4a): each check also merges the newest 50 signal rows read straight from the store and this instance's own fresh signals; the report count does too | **`test_search_lag_cannot_bypass_duplicate_or_limits`** (fails on b27475e7fe2b) |

**Theme follow-ups (in the talks window):**

- Map the new error codes `might_name` (TLK-181) and `busy` (TLK-182) to st-copy's lines. Her text stays in the box.
- Retire the held UI (TLK-116 / TLK-149).
- Hide "something else" from the chips and nav.
- Render nesting with the `parent` reference: show TLK-180 "replying to a hidden comment" when the parent is hidden.
