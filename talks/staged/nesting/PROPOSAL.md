# Reddit-style nesting: minimal store-data + backend change (proposal, talks UX v4)

Status: PROPOSAL. Prepared and tested locally only. Nothing changes in the store, the backend or the theme until the
owner approves the v4 design AND this data change.

## Why a data change

Today a reply stores `depth` 0/1 only (a reply to a nested reply is flattened). The owner wants Reddit-style threads:
reply to ANY comment, mid-thread, with a vertical thread line per level.

Depth alone is not enough. The `replies` list is in display order, so a parent could be inferred from the order.
But when moderation hides a reply (Draft), Liquid skips it, and its children would visually attach to the wrong
comment. An explicit parent reference lets the theme show "replying to a removed comment" instead.

## Store data (shared; owner approval)

**One new optional field on the talk_reply definition** (gid://shopify/MetaobjectDefinition/25691979989):

| key | name | type | validation | required |
|---|---|---|---|---|
| `parent` | Replying to (reply) | metaobject_reference | metaobject_definition_id = 25691979989 (talk_reply) | no |

- **`depth`** is already `number_integer` with no validations, so it can hold 0…8 without a definition change. Its
  admin name "Depth (0 = reply to the talk, 1 = nested)" can be renamed to "Depth (0 = reply to the talk)". That rename
  is cosmetic and optional.
- **Existing data:** there are 0 talk_reply entries today, so there is nothing to migrate.
- **Order:** the field must exist BEFORE the new backend is deployed. Otherwise every reply fails, because the create
  would carry an unknown field.

## Backend (v6, on top of v5; `talks/tools/backend_v6.py`)

Local build **b27475e7fe2b** (v5 + v6 + v7: no review queue + security tests), with 53 tests passing (`talks/backend/SECURITY-v5.md`).

**Changes:**

- **Depth:** `depth = parent depth + 1`, capped at `MAX_DEPTH = 8`. The theme shows 4 levels on phones and 6 on desktop,
  then "continue this thread ›".
- **Parent:** the reply stores `parent` = the reply it answers. `reply_to` (the parent's alias) is kept for the
  "↪ @alias" line.
- **Order:** a new reply is placed at the end of its parent's subtree (siblings oldest first), so the flat `replies`
  list stays in display order for Liquid.
- **Refusals:** replying to a hidden (Draft) reply, or to a reply from another thread, returns `not_found`, the same as
  replying to a hidden thread.
- **Unchanged:**
  - moderation per reply: blocked contacts/links/slurs refused at submit, and anything that might name someone also
    refused at submit (TLK-181, `might_name`, nothing saved; there is no held/Draft path). Draft is used only for the
    auto-hide at 3 reports (v7, `test_blocked_and_might_name_refused`);
  - reports and auto-hide at 3 (per reply);
  - recounting active replies;
  - the device key, burst guard, rate limits and duplicate check;
  - anonymity (no login, no IP).

**New tests:**

- `test_reddit_nesting_depth_order_and_parent`: depths 0/1/2/3, subtree order, stored parent.
- `test_nesting_capped_and_hidden_parent_refused`: the cap at 8, and refusal of a hidden parent.

Both FAIL against v5, which proves they catch the old 2-level behaviour.

## Theme (the v4 talks window, after approval)

- **Replies:** rendered from the ordered list, with `--d: depth` (indent 16 px phone / 22 px desktop) and one 1.5 px
  thread line per ancestor level.
- **Fold:** each parent comment's own line is its fold toggle (a 44 px hit area). Folded, it shows "{n} more replies".
- **Deep levels:** depth ≥ 4 (phone) / ≥ 6 (desktop) collapses behind "continue this thread ›", which opens in place.
- **"reply" on any comment** opens the same friendly box, smaller, right under it, posting `parent` = that reply's
  handle.
- **Removed parent:** if `reply.parent.value` is blank while depth > 0, the parent was hidden, so the reply shows
  "replying to a removed comment".

## Deploy order (each step with the owner's OK)

1. The owner approves the v4 design + this data change.
2. Add the `parent` field to talk_reply (`metaobjectDefinitionUpdate`), then read it back.
3. Backend: update the v0 chat `app.py` → the owner clicks Publish → check `/api/talks` shows build **b27475e7fe2b** and
   `GET /apps/talks` shows `{"open": false}`.
4. Theme: one talks window (v4 UX + posting-ON), then the E2E and kill-switch sequence in
   `talks/staged/posting-on/INSTALL.md`.
