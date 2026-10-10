/* ---------- plan data: sections 1-4 ---------- */
const A = 'https://admin.shopify.com/store/0nev20-vn';
const PREVIEW = 'https://0nev20-vn.myshopify.com/?preview_theme_id=186651934933';
const STORE = 'https://0nev20-vn.myshopify.com';
const BACKEND = 'https://small-talk-talks-backend.vercel.app';
const ORCH = 'the orchestrator session ("Small Talk — Orchestrator" in the Claude app)';

const REFUND_TEXT = `Return and refund policy

Last updated: 9 October 2026

15-day returns
You can return a Small Talk set within 15 days of delivery. Because press-on nails are a personal-care product, we can only accept sets that are unused and unopened, in their original packaging with the seal intact.

Damaged, defective or wrong item
If your set arrives damaged, defective or is not what you ordered, email us within 15 days of delivery with your order number and a photo. We will send a replacement or a full refund, including any shipping you paid, at no cost to you.

How to start a return
1. Email riyaagg24@gmail.com within 15 days of delivery with your order number and the reason for the return.
2. We will confirm the return and tell you where to send the parcel.
3. Pack the set securely in its original packaging and ship it to us. For change-of-mind returns, the return shipping cost is yours; for damaged, defective or wrong items, we cover it.

Refunds
Once we receive and check the return, we will refund the full product price to your original payment method within 7 business days. Your bank or card provider may take a few more days to show it.

Exchanges
We do not offer direct exchanges at the moment. Return the set for a refund and place a new order for the one you want.

Cancellations
You can cancel an order for a full refund any time before it is dispatched. Email us with your order number.

Questions
Email riyaagg24@gmail.com or call +91 981 179 8343.`;

const TERMS_TEXT = `Terms of service

Last updated: 9 October 2026

1. Who we are
This website is run by Small Talk (“we”, “us”). By using the site or placing an order, you agree to these terms. If you don’t agree, please don’t use the site.

2. Our products
We sell press-on nail sets. Product colours on screen can look slightly different from the real thing. Campaign illustrations on the site are artwork, not photos of the product. Please follow the instructions that come with your kit and on our Nail Guide.

3. Prices and payment
Prices are in Indian rupees (INR) and include GST. Any shipping charge is shown at checkout before you pay. We can change prices at any time, but not for an order you have already placed. If a price is clearly wrong because of an error, we may cancel the order and refund you in full.

4. Orders
Placing an order is an offer to buy. Your order is accepted when we dispatch it. We may decline or cancel an order (for example, if an item is out of stock), and if we do, we refund you in full.

5. Delivery, returns and cancellations
Delivery, returns, refunds and cancellations are covered by our Shipping policy and our Return and refund policy, which form part of these terms.

6. the talks
the talks is our community board.
- You can post without a name, email or account. Your alias is the only name shown.
- When you post a talk or a reply, you keep ownership of what you wrote. You give us permission to show it on our site.
- Don’t post real names, phone numbers, emails, links, handles, or anything that could identify someone.
- Don’t post anything hateful, harassing, defamatory, illegal or spam.
- Our filter may stop a post from going up. We may hide or remove any post, at any time, without notice.
- To stop spam, we keep a scrambled device code (never your IP address) for a short time. Our Privacy policy has the details.
- To report a post, tap Report. If something on the board is about you, email us with the link.

7. Our content
The Small Talk name, logo, packaging, illustrations, stories and site content belong to us. Please don’t copy or reuse them without permission.

8. Liability
We provide the site and our products as described. To the extent the law allows, we are not liable for indirect or unexpected losses. If something goes wrong with an order, our responsibility is limited to the amount you paid for that order. Nothing in these terms limits your rights under Indian consumer law.

9. Changes to these terms
We may update these terms from time to time. The version on this page applies to any order you place after it is updated.

10. Law
These terms are governed by the laws of India.

11. Contact
Questions about these terms? Email riyaagg24@gmail.com.`;

const PRIVACY_TALKS = `the talks (our community board)
You can post on the talks without a name, email address or account. What you post is public on our site: your talk or reply, the alias you chose, your avatar and the time you posted. Your alias, avatar, a random device ID and any unsent draft are saved only in your browser’s storage, and clearing your browser data removes them. To prevent spam and abuse, each time you post, reply or report, we keep a short record made from a scrambled, one-way version of that device ID, plus a scrambled version of the text so we can catch repeats. We do not store your IP address with these records, and we delete them automatically within 30 days. Posts are stored in our Shopify store, and our posting service runs on Vercel, a hosting provider; both process each request only to deliver it. Posts that break our house rules may be refused when you submit them, or removed later. If something posted on the talks is about you, email us at riyaagg24@gmail.com with the link and we’ll take it down.`;
const TERMS_S6 = `6. the talks
the talks is our community board.
- You can post without a name, email or account. Your alias is the only name shown.
- When you post a talk or a reply, you keep ownership of what you wrote. You give us permission to show it on our site.
- Don’t post real names, phone numbers, emails, links, handles, or anything that could identify someone.
- Don’t post anything hateful, harassing, defamatory, illegal or spam.
- Our filter may stop a post from going up. We may hide or remove any post, at any time, without notice.
- To stop spam, we keep a scrambled device code (never your IP address) for a short time. Our Privacy policy has the details.
- To report a post, tap Report. If something on the board is about you, email us with the link.`;

const SECTIONS_A = [
{
  id: 's1', set: 'on-me', icon: '💳', title: 'Make the store able to sell',
  sub: 'Right now nobody can pay. These fix that.',
  tasks: [
  {
    id: 'pay', t: 'Switch on a payment provider', min: '30 min + 1–3 days KYC',
    why: 'Checkout says "This store can\'t accept payments right now". No payments = no orders.',
    steps: [
      'Open <b>Settings → Payments</b> (link below).',
      'Shopify Payments isn\'t available in India, so under <b>Payment providers</b> click <b>Choose a provider</b> and pick a third-party one: Razorpay, PayU or Cashfree. Only one card provider can be active at a time.',
      'Install that provider\'s Shopify app (links below) and sign up with them. Then come back and click <b>Activate</b> → <b>Save</b>.',
      'Their KYC asks for PAN, bank account and business details. Keep them handy. Approval can take a few days.',
      'Turn on the provider\'s <b>test mode</b> first if it has one. Come back to Settings → Payments and check it says <b>Active</b>.',
      'Then do the test order task in section 4.'
    ],
    links: [['Settings → Payments', A + '/settings/payments'], ['Shopify help: set up a provider', 'https://help.shopify.com/en/manual/payments/third-party-providers/configuring-providers'], ['Shopify Payments countries (no India)', 'https://help.shopify.com/en/manual/payments/shopify-payments/supported-countries'], ['Razorpay Secure app', 'https://apps.shopify.com/razorpay-secure'], ['PayU India app', 'https://apps.shopify.com/payu-india'], ['Cashfree Payments app', 'https://apps.shopify.com/cashfree-payments']],
    warn: 'Your API keys and bank details go only into the provider\'s own screens. Never paste them into Claude or any chat.'
  },
  {
    id: 'refund', t: 'Paste the real refund policy', min: '5 min',
    why: 'Your refund policy page shows the shipping text by mistake. Checkout links to it.',
    steps: [
      'Tap <b>Copy refund policy</b> below.',
      'Open <b>Settings → Policies</b> → <b>Written policies</b> → <b>Return and refund policy</b>. Make sure <b>Use automated policy</b> is off.',
      'Select everything in the box and delete it. Paste.',
      'Click <b>Save</b>.',
      'Open your store\'s <code>/policies/refund-policy</code> page and check it says "15-day returns".'
    ],
    copy: [['Copy refund policy', REFUND_TEXT]],
    links: [['Settings → Policies', A + '/settings/legal'], ['Shopify help: store policies', 'https://help.shopify.com/en/manual/checkout-settings/refund-privacy-tos'], ['Check the live page', STORE + '/policies/refund-policy']],
    note: 'This is the approved text from your policies file. It ends with your email and phone number. Keeping the phone in your policies is your choice: India\'s e-commerce consumer rules expect a reachable contact for complaints. If you want email only, delete " or call +91…" before saving (and do the same in the shipping and privacy policies).'
  },
  {
    id: 'refundflag', t: 'Tell Claude the refund text is in', min: '2 min',
    why: 'The new theme hides Returns links until a setting called "Refund policy text verified" is switched on.',
    steps: [
      'Copy the message below.',
      'Paste it into ' + ORCH + '.',
      'Claude checks your policy page and switches the setting on in the theme. Only one Claude session edits the theme at a time, so let it do this rather than clicking it yourself.'
    ],
    prompt: { label: 'Copy message for the orchestrator', text: 'Refund policy pasted in Settings → Policies (SD25). Please read back /policies/refund-policy, and if it shows the returns text, have the theme lock holder switch on "Refund policy text verified" on theme 186651934933 and confirm Help → Returns and the footer refund link appear on the preview.' }
  },
  {
    id: 'terms', t: 'Paste the Terms of service', min: '5 min',
    why: 'Shoppers and payment providers expect Terms. The footer Terms link appears once it exists.',
    steps: [
      'Tap <b>Copy Terms</b>.',
      '<b>Settings → Policies</b> → <b>Written policies</b> → <b>Terms of service</b>. It\'s empty today. Paste, <b>Save</b>.',
      'If you have a registered business name, swap it in for "Small Talk" in section 1.'
    ],
    copy: [['Copy Terms', TERMS_TEXT]],
    links: [['Settings → Policies', A + '/settings/legal']],
    note: 'Plain-language draft, not legal advice. Have a lawyer look at it when you can.'
  },
  {
    id: 'addr', t: 'Decide: can people change their address after ordering?', min: '3 min',
    why: 'Your live shipping policy says yes (while it\'s being packed). Your answer to Claude was no. They should match.',
    steps: [
      'Pick one: <b>Yes</b>, while it\'s being packed. Or <b>No</b>.',
      'If <b>No</b>: <b>Settings → Policies → Shipping policy</b>, delete the "Address changes" paragraph, <b>Save</b>.',
      'Tell the orchestrator your answer so the Help page matches.'
    ],
    links: [['Settings → Policies', A + '/settings/legal']],
    prompt: { label: 'Copy message for the orchestrator', text: 'SD26 / G13 decision: customers [CAN / CANNOT] change their delivery address while the order is being packed. I have [kept / removed] the "Address changes" paragraph in the shipping policy. Please make Help and FACTS.md match.' }
  },
  {
    id: 'money', t: 'Show prices as ₹599, not Rs. 599.00', min: '3 min',
    why: 'The designs use ₹599. The store format is currently "Rs. {{amount}}", which prints "Rs. 599.00".',
    steps: [
      '<b>Settings → General</b> → <b>Store defaults</b> → the <b>⋯</b> menu → <b>Change currency formatting</b>.',
      'Put the formats below in the matching boxes (HTML with currency, HTML without currency, email with currency, email without currency).',
      'Click <b>Save</b>. Open a product on the preview and check it says ₹599.'
    ],
    copy: [['₹{{amount_no_decimals}}', '₹{{amount_no_decimals}}'], ['₹{{amount_no_decimals}} INR', '₹{{amount_no_decimals}} INR']],
    links: [['Settings → General', A + '/settings/general'], ['Shopify help: currency formatting', 'https://help.shopify.com/en/manual/international/pricing/currency-formatting']],
    note: 'Use the version without "INR" for the two "without currency" boxes, and with "INR" for the two "with currency" boxes. Checkout always shows decimals; that\'s normal.'
  },
  {
    id: 'ship', t: 'Rename the shipping rate (and rethink ₹379)', min: '5 min',
    why: 'Checkout shows the delivery option as "मानक". Many shoppers won\'t read it. ₹379 on a ₹499 set will also stop people.',
    steps: [
      '<b>Settings → Shipping and delivery</b> → <b>Shipping profiles</b> → click your profile (usually <b>General</b>).',
      'Find the Domestic (India) rate "मानक" → <b>⋯</b> → <b>Edit shipping option</b>.',
      'Rename it to something clear, e.g. <b>Standard delivery (up to 7 days)</b>.',
      'Look at the price. Many D2C brands charge ₹49–99 or give free delivery above an amount. Decide what you can afford, change it, <b>Done</b> → <b>Save</b>.'
    ],
    links: [['Settings → Shipping and delivery', A + '/settings/shipping'], ['Shopify help: shipping rates', 'https://help.shopify.com/en/manual/fulfillment/setup/shipping-rates/setting-up-shipping-rates']],
    note: 'International is ₹1,800 to 28 countries. If you only want India for now, remove that zone.'
  },
  {
    id: 'seo', t: 'Homepage title, description and share image', min: '10 min',
    why: 'This is what Google and WhatsApp previews show. Today it says "Small Talk | Almond Press-On Nails. A Lot Said." and we dropped "Almond".',
    steps: [
      '<b>Online Store → Preferences</b> → section <b>Social sharing image and SEO</b>.',
      '<b>Homepage title</b>: paste the title below.',
      '<b>Homepage meta description</b>: paste the description below.',
      'Click <b>Save</b>.'
    ],
    copy: [['Title', 'Small Talk — Press-On Nails with a Story'], ['Description', 'Meet Small Talk: seven press-on nail sets, from burgundy tortoiseshell to lime and cobalt checks. Explore the designs and the little moments behind them.']],
    links: [['Online Store → Preferences', A + '/online_store/preferences'], ['Shopify help: Preferences', 'https://help.shopify.com/en/manual/online-store/setting-up/preferences']]
  },
  {
    id: 'logo', t: 'Upload your logo (it\'s ready)', min: '5 min',
    why: 'Claude made the logo and it\'s already on the new store. Shopify\'s own places (checkout, emails, Google) need it uploaded once.',
    steps: [
      'The files are on the laptop in <code>C:\\Users\\SSTS\\Desktop\\Riya\\artwork\\hd\\logo\\brand\\</code>.',
      '<b>Settings → Brand</b> → <b>Logo</b> → upload <code>small-talk-logo-transparent-1336.png</code>.',
      '<b>Square logo</b> → upload <code>small-talk-logo-square-1200.png</code>. <b>Save</b>.',
      'Checkout: <b>Settings → Checkout</b> → <b>Customize</b> → <b>Logo</b> → pick the same transparent logo → <b>Save</b>.'
    ],
    links: [['Settings (then Brand)', A + '/settings'], ['Settings → Checkout', A + '/settings/checkout']]
  }
  ]
},
{
  id: 's2', set: 'brainwave', icon: '🔍', title: 'Check the facts customers rely on',
  sub: 'Claude filled in sensible guesses. Only you know the real kit.',
  tasks: [
  {
    id: 'f-where', t: 'See where the facts live', min: '3 min',
    why: 'Every fact on the site comes from one file, so a fix in one place fixes all pages.',
    steps: [
      'The file is <code>C:\\Users\\SSTS\\Desktop\\Riya\\copy\\FACTS.md</code> (on the laptop). Facts are numbered F1–F15.',
      'On the site they show on: each product page ("What\'s in the kit", fit, how to apply), the Nail Guide, the FAQ on the homepage, and Help.',
      'You never edit the theme yourself. You tell Claude the correct fact, the copy session updates the words, and the theme session installs them.'
    ],
    links: [['Preview: product page (On Me)', STORE + '/products/bill-idhar?preview_theme_id=186651934933'], ['Preview: Nail Guide', STORE + '/pages/nail-guide-desi?preview_theme_id=186651934933'], ['Preview: Help', STORE + '/pages/help?preview_theme_id=186651934933']]
  },
  {
    id: 'f-kit', t: 'Kit contents (F2)', min: '10 min',
    why: 'If the box is different from the page, you get returns and angry DMs.',
    steps: [
      'Open one real kit from your supplier.',
      'Count: how many nails? how many sizes? Is there glue? tabs (how many)? file? prep pad? cuticle stick? instruction card?',
      'Compare with the site: "24 almond press-ons in 12 sizes, nail glue, a sheet of adhesive tabs, a mini file, a prep pad, a cuticle stick and an instruction card."',
      'Different? Use the correction message below.'
    ]
  },
  {
    id: 'f-size', t: 'Sizes (F3)', min: '15 min',
    why: 'The size chart says size 0 = 18 mm down to size 11 = 7 mm. That was a guess.',
    steps: ['With a ruler, measure the widest point of one nail in each size.', 'Write the 12 widths in mm.', 'Send them with the correction message if they differ.']
  },
  {
    id: 'f-apply', t: 'Applying and removing (F4, F5)', min: '30 min',
    why: 'The 6 apply steps and 4 removal steps should match what really works with your glue and tabs.',
    steps: ['Put on one full set yourself, following the Nail Guide steps on the preview.', 'Then remove it the way the guide says.', 'Note anything that was wrong, missing or confusing.']
  },
  {
    id: 'f-wear', t: 'How long they last (F6, F7)', min: 'over 2 weeks',
    why: 'The site says glue ~2 weeks, tabs 1–3 days, reusable. Only promise what really happens.',
    steps: ['Wear a set with glue and note the day nails start lifting.', 'Try tabs once too.', 'Try reusing a set after removal.', 'Update Claude if your results differ.']
  },
  {
    id: 'f-ship', t: 'Delivery and returns you can really keep (F10, F11)', min: '10 min',
    why: 'The policies promise dispatch in 2 business days, delivery within 7 days, 15-day returns.',
    steps: ['Pick your courier or aggregator (e.g. Shiprocket, Delhivery). Check their real delivery times to small towns.', 'Can you pack within 2 business days, even during exams?', 'If not, tell Claude the numbers you can keep. Policies and Help get updated together.'],
    links: [['Shiprocket on the Shopify App Store', 'https://apps.shopify.com/shiprocket']]
  },
  {
    id: 'f-photos', t: 'Take real product photos (G11)', min: '1 hour',
    why: 'Every picture on the site is illustration or AI art. Real photos build trust before people pay.',
    steps: ['Daylight near a window. Plain card in the set colour behind.', 'Shoot per set: the closed box, the open tray, one hand wearing the set, a close-up of 2 nails.', 'Use your phone\'s main camera (1×). No filters.', 'Put them in a folder <code>artwork\\photos\\&lt;set&gt;\\</code> and tell the orchestrator. Claude adds them to product pages.']
  },
  {
    id: 'f-send', t: 'Send your corrections to Claude', min: '5 min',
    why: 'One message, and every page with that fact gets fixed.',
    steps: ['Fill in the brackets in the message below. Delete lines that are already correct.', 'Paste it into ' + ORCH + '.'],
    prompt: { label: 'Copy facts correction message', text: `FACTS correction from the owner (please route to st-copy, then the theme lock holder; update copy/FACTS.md first):
- F2 kit contents: [e.g. 24 nails in 12 sizes, glue 2 g, 24 tabs, file, prep pad, cuticle stick, card]
- F3 size widths in mm, size 0 → 11: [..]
- F4 / F5 apply or removal step changes: [..]
- F6 wear time: glue [..], tabs [..]; F7 reusable: [yes/no]
- F10 dispatch [..] business days, delivery up to [..] days
- F11 returns window [..] days
Keep all other facts. No medical or "safe for nails" claims. Show me the changed rows before anything is installed.` }
  }
  ]
},
{
  id: 's3', set: 'diet-cherry', icon: '💬', title: 'Turn on the talks',
  sub: 'The anonymous board is built. It needs one small private app from you.',
  tasks: [
  {
    id: 't-email', t: 'Verify your email for the Shopify Dev Dashboard', min: '5 min',
    why: 'You can\'t create the talks app until the Dev Dashboard email is verified. This is where setup got stuck.',
    steps: [
      'Open Gmail for <b>riyaagg24@gmail.com</b>.',
      'Search <b>from:shopify verify</b>. Check <b>Promotions</b> and <b>Spam</b> too.',
      'Open the newest verification email and click the button.',
      'Nothing there? Open dev.shopify.com, sign in with the same account, and look for a "resend verification" banner.',
      'Still nothing after 30 minutes: contact Shopify Support (link) and say "I can\'t verify my email for the Dev Dashboard".'
    ],
    links: [['Gmail search', 'https://mail.google.com/mail/u/0/#search/from%3Ashopify+verify'], ['Shopify Dev Dashboard', 'https://dev.shopify.com/dashboard/'], ['Shopify Support', 'https://help.shopify.com/en/support']]
  },
  {
    id: 't-app', t: 'Create the app "Small Talk talks"', min: '3 min',
    why: 'This tiny app lets the talks save posts into your store. It can only touch talks entries.',
    steps: [
      'Shopify admin → <b>Settings → Apps</b> → <b>Develop apps</b> → <b>Build apps in Dev Dashboard</b>. This opens dev.shopify.com.',
      '<b>Apps</b> → <b>Create app</b> → <b>Start from Dev Dashboard</b>.',
      'Name it <b>Small Talk talks</b> → <b>Create</b>.'
    ],
    copy: [['App name', 'Small Talk talks']],
    links: [['Settings → Apps', A + '/settings/apps'], ['Dev Dashboard', 'https://dev.shopify.com/dashboard/'], ['Shopify dev: create an app', 'https://shopify.dev/docs/apps/build/dev-dashboard/create-apps-using-dev-dashboard']]
  },
  {
    id: 't-version', t: 'Set up the app version', min: '5 min',
    why: 'This tells Shopify where the talks backend is and what it may touch.',
    steps: [
      'In the app, open <b>Versions</b> → <b>Create a version</b>.',
      '<b>App URL</b>: paste the backend address.',
      '<b>Embed app in Shopify admin</b>: <b>off</b>.',
      '<b>Access → Scopes</b>: add exactly these three: <code>read_metaobjects</code>, <code>write_metaobjects</code>, <code>write_app_proxy</code>.',
      '<b>App proxy</b>: Prefix <b>apps</b>, Subpath <b>talks</b>, Proxy URL = the /api/talks address.',
      'Leave everything else. Click <b>Release</b> and confirm.'
    ],
    copy: [['App URL', BACKEND], ['Scopes', 'read_metaobjects,write_metaobjects,write_app_proxy'], ['Prefix', 'apps'], ['Subpath', 'talks'], ['Proxy URL', BACKEND + '/api/talks']]
  },
  {
    id: 't-install', t: 'Install the app on your store', min: '2 min',
    why: 'Creating isn\'t enough; the store has to say yes.',
    steps: ['App overview → <b>Install app</b>.', 'Choose the store <b>0nev20-vn</b> → <b>Install</b> → approve the three permissions.', 'Check: <b>Settings → Apps</b> lists "Small Talk talks" and shows <b>App proxy URL: /apps/talks</b>.'],
    links: [['Settings → Apps', A + '/settings/apps']]
  },
  {
    id: 't-vercel', t: 'Put the keys in Vercel (not in chat!)', min: '5 min',
    why: 'The backend needs the app\'s keys. They live only in Vercel, never in Claude, email or files.',
    steps: [
      'Dev Dashboard → Apps → Small Talk talks → <b>Settings</b>. Copy the <b>Client ID</b>. Click reveal, copy the <b>Client secret</b>.',
      'Open vercel.com → project <b>small-talk-talks-backend</b> → <b>Settings</b> → <b>Environment Variables</b>.',
      'Add 4 variables for <b>Production</b>: <code>SHOPIFY_SHOP</code> = <code>0nev20-vn.myshopify.com</code> · <code>SHOPIFY_CLIENT_ID</code> = the Client ID · <code>SHOPIFY_CLIENT_SECRET</code> = the secret (tick <b>Sensitive</b>) · <code>TALKS_SALT</code> = a long random string you make (40+ letters and numbers, tick <b>Sensitive</b>).',
      'For TALKS_SALT, use your password manager\'s generator. Don\'t reuse a password.'
    ],
    copy: [['SHOPIFY_SHOP', 'SHOPIFY_SHOP'], ['shop value', '0nev20-vn.myshopify.com'], ['SHOPIFY_CLIENT_ID', 'SHOPIFY_CLIENT_ID'], ['SHOPIFY_CLIENT_SECRET', 'SHOPIFY_CLIENT_SECRET'], ['TALKS_SALT', 'TALKS_SALT']],
    links: [['Vercel', 'https://vercel.com/'], ['Vercel help: environment variables', 'https://vercel.com/docs/environment-variables']],
    warn: 'Never paste the Client secret or TALKS_SALT into Claude, WhatsApp, email or a file. Only into Vercel.'
  },
  {
    id: 't-publish', t: 'Publish the backend from v0', min: '3 min',
    why: 'A fresh publish picks up the new code and your 4 variables in one go.',
    steps: [
      'Open the v0 chat <b>small-talk-talks-backend</b> (link) → click <b>Publish</b>.',
      'Don\'t use Vercel\'s "Redeploy" button. It rebuilds the old code.',
      'Wait a minute, then open the check link. It must show <code>"configured": true</code> and <code>"build": "c91d3d11afc1"</code>.'
    ],
    links: [['v0 chat', 'https://v0.app/chat/pEcbsIUvnGe'], ['Check: /api/talks', BACKEND + '/api/talks']]
  },
  {
    id: 't-tell', t: 'Tell Claude "talks app installed"', min: '1 min',
    why: 'Claude then switches posting on, tests posting, replying and reporting, and deletes the test posts.',
    steps: ['Copy the message and paste it into ' + ORCH + '.'],
    prompt: { label: 'Copy message', text: 'talks app installed. /api/talks shows configured: true and build c91d3d11afc1. Please grant st-talks its posting-ON window (HD avatars + posting on + real end-to-end test + delete test posts) and tell me when the talks are live on the preview.' }
  },
  {
    id: 't-privacy', t: 'Add the talks paragraph to your Privacy policy', min: '5 min',
    why: 'People should know what the talks keep (no IP address, scrambled device code, deleted within 30 days).',
    steps: ['Tap <b>Copy paragraph</b>.', '<b>Settings → Policies → Privacy policy</b>. Scroll to the end and paste it as a new section.', '<b>Save</b>.', 'This is a new section at the end; don\'t change the rest of the policy.'],
    copy: [['Copy paragraph', PRIVACY_TALKS]],
    links: [['Settings → Policies', A + '/settings/legal']],
    note: 'Final wording by the copy session (TLK-155, v1.4.4). Not legal advice. Still yours to check: India\'s IT Rules expect sites with user posts to name a grievance contact and respond in time. Ask a lawyer or CA before the board grows.'
  },
  {
    id: 't-moderate', t: 'Learn the 2-minute daily check', min: '2 min a day',
    why: 'The filters catch most bad posts. You decide on held or reported ones.',
    steps: [
      '<b>Content → Metaobjects → Talk thread</b>. Filter <b>Status: Draft</b>.',
      'Read the <b>Moderation note</b>. "held: …" = the filter wasn\'t sure. "auto-hidden: 3 reports" = 3 people reported it.',
      'Fine? Set Status <b>Active</b> → Save. Names or targets someone? Leave as Draft, or <b>⋯ → Delete</b>.',
      'To restore an auto-hidden post: Status <b>Active</b> and Reports <b>0</b>.',
      'Same for <b>Talk reply</b>.',
      'Emergency stop: <b>Talk settings → main → Posting open: off</b>.'
    ],
    links: [['Content → Metaobjects', A + '/content/metaobjects'], ['Shopify help: edit metaobject entries', 'https://help.shopify.com/en/manual/custom-data/metaobjects/creating-entries']]
  },
  {
    id: 't-oldtalks', t: 'After talks are live: retire the old blog talks', min: '10 min',
    why: 'The 9 old "the talks" blog posts and the old page /pages/the-talks are now duplicates.',
    steps: ['Do this only after Claude says the new talks are live.', 'Ask the orchestrator to do it with you (message below). It lists every redirect so no link breaks.'],
    prompt: { label: 'Copy message for the orchestrator', text: 'SD29: the new talks are live. Walk me through (or do, if you have permission) unpublishing the 9 the-talks blog articles with redirects /blogs/the-talks/<handle> → /pages/talk/<handle>, and unpublishing the legacy page /pages/the-talks with a 301 /pages/the-talks → /blogs/the-talks. Give me the exact list first.' }
  }
  ]
},
{
  id: 's4', set: 'green-flag', icon: '🚀', title: 'Go live',
  sub: 'The live store today is the OLD ChatGPT theme. The Claude build is ready but hidden.',
  tasks: [
  {
    id: 'g-which', t: 'Know which theme is which', min: '2 min',
    why: 'So you never publish or edit the wrong one.',
    steps: [
      '<b>Online Store → Themes</b>.',
      'At the top, <b>Current theme</b> = "Copy of Small Talk — Desi Ink / Artwork correction". That is the OLD ChatGPT build. It\'s what shoppers see today.',
      'Below, under <b>Draft themes</b>: "<b>Small Talk — Claude build (Horizon)</b>" = the new store (ID 186651934933).',
      'Don\'t click Edit code or Customize on either while Claude is working. Claude edits only the Claude build, one session at a time.'
    ],
    links: [['Online Store → Themes', A + '/themes']]
  },
  {
    id: 'g-preview', t: 'Walk through the preview on your phone', min: '20 min',
    why: 'You are the first real shopper. Note anything odd before launch.',
    steps: [
      'Open the preview link on your phone.',
      'Home: the hero animation plays, swipe between sets, scroll all 7 chapters.',
      'Open 2–3 products. Add one to bag. Change quantity. Remove it.',
      'Open Nail Guide, Help, Our Story, Journal, the talks.',
      'Check the footer links work.',
      'Screenshot anything weird and send it to the orchestrator with one line on what\'s wrong.'
    ],
    links: [['Open the preview', PREVIEW], ['Shopify help: preview a theme', 'https://help.shopify.com/en/manual/online-store/themes/adding-themes']],
    note: 'The preview link only works while you\'re logged into Shopify in the same browser, or for 14 days from a shared preview link.'
  },
  {
    id: 'g-test', t: 'Place one test order, then cancel it', min: '15 min',
    why: 'Proves the whole path works: bag → checkout → payment → order email.',
    steps: [
      'Do this after payments are on.',
      'In the payment provider, use its test mode, or buy the cheapest set with your own card/UPI.',
      'Check you get the order email and the order shows in <b>Orders</b>.',
      'Cancel and refund it: open the order → <b>More actions → Cancel order</b> → refund.'
    ],
    links: [['Orders', A + '/orders'], ['Shopify help: test orders', 'https://help.shopify.com/en/manual/checkout-settings/test-orders'], ['Shopify help: managing orders', 'https://help.shopify.com/en/manual/fulfillment/managing-orders']]
  },
  {
    id: 'g-probe', t: 'Delete 6 empty test files from the Claude build', min: '5 min',
    why: 'Claude left harmless probe files it isn\'t allowed to delete itself.',
    steps: [
      'Any time is fine: no Claude session touches these files.',
      '<b>Online Store → Themes</b> → Claude build → <b>⋯</b> → <b>Edit code</b>.',
      'Delete <code>snippets/st-zz-test.liquid</code> and <code>sections/st-zz-a.liquid</code> … <code>st-zz-e.liquid</code>. (Click file → ⋯ → Delete.)',
      'Touch nothing else. Close the editor.'
    ],
    links: [['Online Store → Themes', A + '/themes']]
  },
  {
    id: 'g-oldpages', t: 'Tidy the old pages and menus', min: '15 min',
    why: 'An old Nail Guide page with unchecked claims is still linked, and some empty duplicate pages show in Google.',
    steps: [
      '<b>Content → Menus</b> (older admins: Online Store → Navigation). Open <b>small-talk-main</b> and <b>small-talk-footer</b>. Change any link to <code>/pages/nail-guide</code> so it points to <b>Nail Guide (nail-guide-desi)</b>. Save.',
      'Then <b>Online Store → Pages</b> → the old <b>nail-guide</b> page → Visibility <b>Hidden</b> → Save. (Menus first, so nothing breaks.)',
      'For the other old pages and empty collections (our-world, contact, news, 5 empty collections), ask the orchestrator for the exact list and redirects (message below).'
    ],
    links: [['Content → Menus', A + '/content/menus'], ['Pages', A + '/pages']],
    prompt: { label: 'Copy message for the orchestrator', text: 'SD22/SD23: I repointed the menus to /pages/nail-guide-desi and hid the old nail-guide page. Please give me the exact list of legacy pages/collections/blogs to hide or delete (our-world, contact, news, the 5 empty collections) and the 301 redirects to add, per seo/STRATEGY.md §2, in click order.' }
  },
  {
    id: 'g-publish', t: 'Publish the Claude build', min: '5 min',
    why: 'This swaps the live store to the new design. You can undo it in one click.',
    steps: [
      'Only after: payments on, refund policy fixed, test order done, preview looks right.',
      'Tell the orchestrator you\'re publishing, so no Claude session is mid-edit.',
      '<b>Online Store → Themes</b> → <b>Draft themes</b> → "<b>Small Talk — Claude build (Horizon)</b>" → <b>Publish</b> → confirm. The old theme moves into Draft themes.',
      'Open your store in a private/incognito tab and click around for 2 minutes.'
    ],
    links: [['Online Store → Themes', A + '/themes'], ['Shopify help: publish a theme', 'https://help.shopify.com/en/manual/online-store/themes/managing-themes/publishing-themes']],
    prompt: { label: 'Copy message for the orchestrator', text: 'I am about to publish theme 186651934933 (Small Talk — Claude build). Please confirm no session holds the theme write lock, then I publish. After that: remove the preview-only noindex rules that should not apply on the live store, and check the live home, a PDP, cart and checkout.' }
  },
  {
    id: 'g-rollback', t: 'Know how to undo (roll back)', min: '1 min',
    why: 'If something looks broken after launch, you can go back in 30 seconds.',
    steps: ['<b>Online Store → Themes</b> → <b>Draft themes</b>.', 'Find "Copy of Small Talk — Desi Ink / Artwork correction" → <b>Publish</b>.', 'Tell the orchestrator what you saw. Products, orders and policies aren\'t affected by switching themes.'],
    links: [['Online Store → Themes', A + '/themes'], ['Shopify help: publish / roll back', 'https://help.shopify.com/en/manual/online-store/themes/managing-themes/publishing-themes']]
  },
  {
    id: 'g-password', t: 'Check the store isn\'t password-locked', min: '1 min',
    why: 'A password page blocks every visitor, ad and Google.',
    steps: ['<b>Online Store → Preferences</b> → <b>Password protection</b>.', 'If "Restrict access to visitors with the password" is ticked, untick it on launch day → Save.'],
    links: [['Online Store → Preferences', A + '/online_store/preferences']]
  },
  {
    id: 'g-apps', t: 'Optional: remove apps and pixels you don\'t use', min: '10 min',
    why: 'Every app and pixel adds scripts. Removing unused ones is the biggest speed win left on the home page.',
    steps: [
      '<b>Settings → Apps</b>: look at the list. Uninstall anything you don\'t use.',
      '<b>Keep</b>: your payment app (Razorpay/PayU/Cashfree), <b>Small Talk talks</b>, and the apps from this plan (Facebook & Instagram, Google & YouTube, Forms, Messaging).',
      '<b>Settings → Customer events</b>: disconnect custom pixels you don\'t recognise or need.',
      'Not sure about one? Ask the orchestrator before removing it.'
    ],
    links: [['Settings → Apps', A + '/settings/apps'], ['Settings → Customer events', A + '/settings/customer_events'], ['Shopify help: pixels', 'https://help.shopify.com/en/manual/promoting-marketing/pixels/overview']]
  }
  ]
}
];
