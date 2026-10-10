# the talks: owner setup (about 15 minutes, one time)

The talks need one small private app. Its secret lives only in Vercel. Claude never sees it, and it is not in the
theme or in any file. Do the steps in order. Stop and tell the orchestrator if a screen looks different.

**What you will have at the end:**

- An app called **Small Talk talks**, installed on your store, that can only read and write the talks entries
  (metaobjects).
- The Vercel project **small-talk-talks-backend** holding the app's Client ID and Client secret.
- Shopify sends every post from `/apps/talks` on your store to that Vercel project (the "App proxy").

## 0. Before you start (one time)

- **Reconnect v0/Vercel:** in claude.ai → Settings → Connectors → **v0** → Reconnect.
- **Say OK to the deploy:** tell the talks session (st-talks) "OK to deploy the talks backend to my Vercel
  account". It is an outward-facing deploy, so Claude waits for your OK.
- **Done 10 Oct:** the backend is live in your own Vercel account (project **small-talk-talks-backend**) at
  `https://small-talk-talks-backend.vercel.app`.
- Check it: the address shows a one-line info page, and `/api/talks` says `"configured": false` until step 5.

## 1. Create the app (Shopify Dev Dashboard)

1. Shopify admin → **Settings** → **Apps** → **Develop apps** → **Build apps in Dev Dashboard**. This opens
   dev.shopify.com.
2. **Apps** → **Create app** → **Start from Dev Dashboard**. Name it `Small Talk talks` and click **Create**.

## 2. Configure a version

You land on the app's **Versions** tab, or go to **Versions → Create a version**.

1. **App URL:** `https://small-talk-talks-backend.vercel.app` (a one-line info page)
2. **Embed app in Shopify admin:** **off**
3. **Access → Scopes:** add exactly these three:
   - `read_metaobjects`
   - `write_metaobjects`
   - `write_app_proxy`
4. **App proxy:**
   - Prefix: **apps**
   - Subpath: **talks**
   - Proxy URL: `https://small-talk-talks-backend.vercel.app/api/talks`
5. Leave everything else as it is. Click **Release** and confirm.

## 3. Install it on the store

1. In the app's overview (Dev Dashboard → Apps → Small Talk talks), click **Install app**.
2. Choose the store `0nev20-vn` and **Install**, then approve the three permissions.
3. Check it worked: Shopify admin → Settings → Apps should now list **Small Talk talks**, and its page shows
   **App proxy URL: /apps/talks**.

## 4. Copy the two credentials

1. Dev Dashboard → Apps → Small Talk talks → **Settings**.
2. Copy the **Client ID**.
3. Click **reveal** and copy the **Client secret**.
4. Paste them straight into Vercel (next step). Never send them in chat, email or a file.

## 5. Put them in Vercel

1. vercel.com → your team → project **small-talk-talks-backend** → **Settings** → **Environment Variables**.
2. Add these four, for Environment **Production** (Preview is fine too):

   | Name | Value |
   |---|---|
   | `SHOPIFY_SHOP` | `0nev20-vn.myshopify.com` |
   | `SHOPIFY_CLIENT_ID` | the Client ID from step 4 |
   | `SHOPIFY_CLIENT_SECRET` | the Client secret from step 4 (mark it **Sensitive**) |
   | `TALKS_SALT` | a long random string you make yourself (mark it **Sensitive**) |

   - **About `TALKS_SALT`:** it is the "scrambling" ingredient for the device codes the talks keep to stop spam.
   - **How to make one:** use your password manager's generator (40+ characters, letters and numbers), or type any long
     random mix of keys. Don't reuse a password.
   - **Keep it secret.** Don't send it to anyone, including Claude.
   - **Changing it later** just starts new codes; nothing breaks.

3. Open **v0.app** → the chat **small-talk-talks-backend** → **Publish**. This makes a fresh deployment that picks up
   both the newest code and the four variables.
   - Don't use Vercel's own "Redeploy" button: it rebuilds the previous code.
   - Check it worked: https://small-talk-talks-backend.vercel.app/api/talks should show `"configured": true` and
     `"build": "c91d3d11afc1"`.
4. Nothing else to set up. The project includes a daily clean-up job (Vercel Cron, free plan) that deletes old spam
   codes. You can see it under **Settings → Cron Jobs**.

## 6. Tell the orchestrator

Say "talks app installed". Claude then:

- opens the talks on the preview and posts, replies and reports with no login;
- checks the blocked-content and slow-down messages;
- deletes every test post.

You don't need to do anything else.

---

## Day to day: moderating the talks (Shopify admin, no app needed)

**How often:**

- Once a day, about 2 minutes. Check held posts, and anything three people reported.
- Straight away when someone emails the store about a talk.
- The filters (blocked contact details, links, slurs; held possible real names) are always on. You don't switch them
  on.

**The 2-minute daily check:**

1. Shopify admin → **Content** → **Metaobjects** → **Talk thread**.
2. Sort or filter by **Status** to see the **Draft** entries.
3. Read the **Moderation note** of each new one:
   - `held: …` → read the talk. If it's fine, set Status **Active** → **Save**, and it appears in its place. If it
     names or targets someone, leave it as Draft or **Delete** it.
   - `auto-hidden: 3 reports` → read it. Keep it hidden (Draft) or Delete it. To restore it, set **Active** and
     change **Reports** to `0`.
4. Do the same in **Talk reply**.

**Privacy policy (owner, one-time):** the store's privacy policy should mention the talks. Suggested points, to be
worded by st-copy and pasted in Settings → Policies:

- Talks and replies are public and shown under an alias.
- To stop spam, the talks keep a scrambled code for the device (never the device itself, and no IP address) and
  delete it within 30 days.
- The alias is stored only in the visitor's own browser.

**Reference:** Go to **Content → Metaobjects**.

- **Talk thread** / **Talk reply**: every post.
  - The **Status** column shows **Active** (visible) or **Draft** (hidden).
  - The **Moderation note** column says why something is a Draft:
    - `held: …` means the filter thought it might name a real person, or you switched "Hold every new post" on.
    - `auto-hidden: 3 reports` means three different people reported it.
- **To publish a held post:** open it → Status **Active** → Save. It appears in its place in the list
  automatically.
- **To hide a post:** open it → Status **Draft** → Save.
- **To delete:** open it → **⋯** → **Delete**.
- **To restore an auto-hidden post:** set the Status to **Active** and change **Reports** to `0`. If you leave it at
  3, the next report hides it again.
- **Talks settings → main:**
  - **Posting open:** off pauses all posting and replies straight away (the kill switch).
  - **Hold every new post for review:** on means nothing shows until you publish it.
  - **Extra blocked words** / **Extra words that send a post to review:** one word or phrase per line. They take
    effect within a minute.
- **Talk signal (private):** rate-limit and report records. Each holds the kind of action, a scrambled device code, a
  scrambled fingerprint of the text (to catch repeats), which talk or reply it was about, and the time. There are no
  names, emails or IP addresses, and they are deleted automatically after about 7 days. Leave them alone.
- **Grievances:** the talks tell people to email the store contact address to get something about them taken down.
  Reply from that inbox, and hide or delete the post as above.

## If something breaks

| What you see | What it means |
|---|---|
| "That didn't post. Check your connection and try again." on every post | Usually the app proxy or the Vercel variables. Check steps 2.4 and 5, then redeploy. |
| Need to stop everything now | Talks settings → main → **Posting open** off. |
| Need to rotate the secret | Dev Dashboard → App settings → rotate the Client secret, update `SHOPIFY_CLIENT_SECRET` in Vercel, redeploy. |
