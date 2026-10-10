/* ---------- plan data: sections 5-8 ---------- */
const AD_COPY_PROMPT = `You write Meta (Instagram + Facebook) ad copy for my press-on nail brand. Read the rules, then write what I ask.

${'${VOICE}'}

ADS RULES: no fake urgency ("only 2 left!" unless true), no discounts I haven't given you, no "best/No.1", no reviews or counts, no medical claims, no before/after. Prices only if I give them. Hindi in Roman script.

For the set I name, write:
1. 5 primary texts (max 125 characters each), each built on the set's moment, ending on the headline.
2. 5 headlines (max 40 characters).
3. 3 descriptions (max 30 characters).
4. 2 ideas for a 6–10 second Reel ad: shot by shot, first second must show the hand.
5. One retargeting version for people who visited but didn't buy: friendly, no guilt, mentions what's in the kit (24 almond press-ons in 12 sizes, glue, tabs, file, prep pad, cuticle stick, card).
Set: [NAME THE SET]`;

const SECTIONS_B = [
{
  id: 's5', set: 'pinky-promise', icon: '📊', title: 'Know your visitors',
  sub: 'Meta + Google + Shopify, so you see who comes and what they do.',
  tasks: [
  {
    id: 'm-biz', t: 'Make a Meta business portfolio', min: '10 min',
    why: 'Ads, your Page, Instagram and the pixel all live inside it.',
    steps: [
      'Open business.facebook.com and log in with your personal Facebook.',
      'Create a business portfolio called <b>Small Talk</b>. Use your store email.',
      'If you don\'t have a Facebook Page for Small Talk, create one inside it (Pages → Add → Create a new Page).'
    ],
    links: [['Meta Business Suite', 'https://business.facebook.com/'], ['Meta help: create a business portfolio', 'https://www.facebook.com/business/help/1710077379203657']]
  },
  {
    id: 'm-ig', t: 'Switch Instagram to a professional account', min: '5 min',
    why: 'You need it for Insights, the shop, ads and linking to your Page.',
    steps: [
      'Instagram → your profile → <b>☰</b> → <b>Settings</b> → <b>Account type and tools</b> → <b>Switch to professional account</b>.',
      'Pick <b>Business</b>. Category: e.g. "Beauty, cosmetic & personal care".',
      'Connect it to the Small Talk Facebook Page when asked (or later in Meta Business Suite → Settings → Instagram accounts).'
    ],
    links: [['Instagram help: professional account', 'https://help.instagram.com/502981923235522']]
  },
  {
    id: 'm-app', t: 'Install the Facebook & Instagram app and turn on Conversions API', min: '15 min',
    why: 'This puts the Meta pixel on your store and sends sales to Meta from the server too, so ads learn who buys.',
    steps: [
      '<b>Settings → Sales channels</b> → Shopify App Store → search <b>Facebook & Instagram</b> (by Meta) → <b>Add</b>.',
      '<b>Start set up</b> → <b>Connect account</b>. Connect your business portfolio Small Talk (it must own the Page), the Page, Instagram, the ad account and a pixel/dataset (make a new one called "Small Talk").',
      'Read and accept Meta\'s terms yourself, then <b>Finish setup</b>.',
      'Then <b>Sales channels → Facebook & Instagram → Settings → Data sharing settings</b> → turn on <b>Customer data sharing</b> → choose <b>Maximum</b>. ("Enhanced" adds the Conversions API; "Maximum" is Enhanced plus Meta\'s newest ad tech.)'
    ],
    links: [['Facebook & Instagram app', 'https://apps.shopify.com/facebook'], ['Shopify help: set up Facebook & Instagram', 'https://help.shopify.com/en/manual/online-sales-channels/social-commerce/facebook-instagram-by-meta/setup'], ['Shopify help: data sharing levels', 'https://help.shopify.com/en/manual/promoting-marketing/analyze-marketing/meta-data-sharing'], ['Meta help: Conversions API', 'https://www.facebook.com/business/help/2041148702652965']]
  },
  {
    id: 'm-events', t: 'Check the events arrive in Events Manager', min: '10 min',
    why: 'If events don\'t arrive, ads can\'t find buyers. Check once now, then monthly.',
    steps: [
      'Open Events Manager → your Small Talk dataset → <b>Test events</b>.',
      'Open your store in a new tab and view a product, add to bag, start checkout.',
      'You should see <b>PageView</b>, <b>ViewContent</b>, <b>AddToCart</b>, <b>InitiateCheckout</b>. After a real order, <b>Purchase</b>.',
      'On <b>Overview</b>, each event should say it comes from <b>Browser and Server</b>.'
    ],
    links: [['Events Manager', 'https://business.facebook.com/events_manager'], ['Meta help: test events', 'https://www.facebook.com/business/help/2040882565969969']]
  },
  {
    id: 'g-app', t: 'Install the Google & YouTube app (GA4 + free Google listings)', min: '20 min',
    why: 'Shows your sets free on Google Shopping and connects Google Analytics.',
    steps: [
      'Shopify App Store → <b>Google & YouTube</b> → <b>Add</b>.',
      '<b>Sales channels → Google & YouTube</b> → <b>Connect Google Account</b> (use one you\'ll keep, e.g. a Small Talk Gmail).',
      'Pick a <b>Merchant Center</b> account from the drop-down, or <b>Create new</b>, and finish the phone check. Your 7 products sync automatically.',
      'In the banner "Looking only to set up Google Analytics 4?" click <b>Get started</b> → <b>Create new</b> property (time zone India, currency INR) → <b>Connect</b>.',
      'Fix any product warnings it shows (usually missing GTIN or category; "no GTIN" is fine for your own brand).'
    ],
    links: [['Google & YouTube app', 'https://apps.shopify.com/google'], ['Shopify help: connect Google & YouTube', 'https://help.shopify.com/en/manual/online-sales-channels/marketplaces/google/getting-setup/connect'], ['Google Analytics', 'https://analytics.google.com/'], ['GA4 help: set up', 'https://support.google.com/analytics/answer/9304153']]
  },
  {
    id: 'g-gsc', t: 'Add your store to Google Search Console and send the sitemap', min: '15 min',
    why: 'Tells Google your pages exist and shows what people search to find you.',
    steps: [
      'Do this after the Claude build is live and the store has no password.',
      'Open Search Console → <b>Add property</b> → <b>URL prefix</b> → your store address.',
      'Choose <b>HTML tag</b>. Copy the tag. Send it to the orchestrator (message below); the theme session adds it to the live theme.',
      'Back in Search Console click <b>Verify</b>.',
      '<b>Indexing → Sitemaps</b> → type <code>sitemap.xml</code> → <b>Submit</b>.'
    ],
    links: [['Google Search Console', 'https://search.google.com/search-console'], ['Search Console help: add a property', 'https://support.google.com/webmasters/answer/34592'], ['Search Console help: verify', 'https://support.google.com/webmasters/answer/9008080'], ['Shopify help: sitemap', 'https://help.shopify.com/en/manual/promoting-marketing/seo/find-site-map'], ['Search Console help: sitemaps', 'https://support.google.com/webmasters/answer/7451001'], ['Your sitemap', STORE + '/sitemap.xml']],
    prompt: { label: 'Copy message for the orchestrator', text: 'Search Console verification: please have the theme lock holder add this meta tag to <head> on theme 186651934933 (now live), then tell me so I can click Verify: [PASTE THE <meta name="google-site-verification" ...> TAG HERE]' },
    note: 'A verification tag isn\'t a secret, so it\'s fine to paste it in chat.'
  },
  {
    id: 'g-domain', t: 'Think about a real domain (optional)', min: '15 min',
    why: 'smalltalk-something.in looks more trustworthy than 0nev20-vn.myshopify.com in ads and WhatsApp.',
    steps: ['<b>Settings → Domains</b> → <b>Buy new domain</b> (or connect one you own).', 'Pick something short you can say out loud.', 'Do this before you start ads and Search Console, so links and data don\'t move later.'],
    links: [['Settings → Domains', A + '/settings/domains'], ['Shopify help: domains', 'https://help.shopify.com/en/manual/domains']]
  },
  {
    id: 'g-privacy', t: 'Turn on Shopify\'s cookie banner and privacy settings', min: '10 min',
    why: 'Pixels then follow each visitor\'s choice, and you stay on the right side of privacy rules.',
    steps: [
      '<b>Settings → Customer privacy</b>.',
      'Open <b>Cookie banner</b> → <b>Regions and content</b>. "Automated" shows it where the law needs it; "Manual" lets you pick more regions (e.g. India too). Pick the position → <b>Save</b>. (Needs a published privacy policy; you have one.)',
      'Where the banner shows, Shopify pixels (including the Meta and Google apps) run non-essential tracking only after the visitor agrees. Don\'t paste extra tracking codes into the theme; use apps, so this keeps working.',
      'Check your <b>Privacy policy</b> mentions analytics and ads cookies (Shopify\'s template does).'
    ],
    links: [['Settings → Customer privacy', A + '/settings/privacy'], ['Shopify help: cookie banner', 'https://help.shopify.com/en/manual/privacy-and-security/privacy/customer-privacy-settings/privacy-settings'], ['Shopify help: pixels', 'https://help.shopify.com/en/manual/promoting-marketing/pixels/overview']],
    note: 'Shopify\'s help doesn\'t cover India\'s data protection law (DPDP Act) specifically. Simple rule: ask clearly, collect little, let people say no. Ask a lawyer before collecting more.'
  },
  {
    id: 'g-analytics', t: 'Learn Shopify Analytics in 10 minutes', min: '10 min',
    why: 'Five numbers tell you if the store is working.',
    steps: [
      '<b>Analytics</b> → <b>Overview</b>. Look at: <b>Sessions</b> (visits), <b>Conversion rate</b> (visits that buy), <b>Average order value</b>, <b>Total sales</b>, <b>Top products</b>.',
      '<b>Live View</b> shows people on the store right now. Fun on launch day.',
      '<b>Analytics → Reports</b> → Category <b>Acquisition</b> → "Sessions by referrer"; Category <b>Marketing</b> → "Sessions attributed to marketing campaigns" and "Performance by marketing campaign". These show which posts and ads bring people. (Not sure all are on the Basic plan; use what you see.)',
      'Every Monday, write the 5 numbers in a note. Compare with last week.'
    ],
    links: [['Analytics', A + '/analytics'], ['Shopify help: reports', 'https://help.shopify.com/en/manual/reports-and-analytics/shopify-reports'], ['Shopify help: acquisition reports', 'https://help.shopify.com/en/manual/reports-and-analytics/shopify-reports/report-types/default-reports/acquisition-reports'], ['Shopify help: marketing reports', 'https://help.shopify.com/en/manual/reports-and-analytics/shopify-reports/report-types/default-reports/marketing-reports']]
  }
  ]
},
{
  id: 's6', set: 'on-me', icon: '🎯', title: 'Retargeting ads',
  sub: 'Show ads to people who already looked. Start small.',
  tasks: [
  {
    id: 'a-when', t: 'Know when to start', min: '2 min',
    why: 'Ads to "people who visited" need visitors first.',
    steps: ['Payments on, Claude build live, pixel checked (section 5).', 'Post on Instagram for 1–2 weeks first, so audiences have people in them. Meta needs at least about 100 people for an audience to work well.', 'Set a monthly ad budget you\'re OK losing while you learn. Start small.']
  },
  {
    id: 'a-aud', t: 'Build 5 audiences', min: '20 min',
    why: 'Audiences = who sees which ad. Make them once, reuse forever.',
    steps: [
      'Ads Manager → <b>☰</b> → <b>Audiences</b> → <b>Create audience</b> → <b>Custom audience</b> → <b>Website</b> → your Small Talk dataset.',
      '<b>Visitors 30d</b>: All website visitors, 30 days.',
      '<b>Visitors 90d</b>: All website visitors, 90 days.',
      '<b>Cart, no buy 14d</b>: event AddToCart in 14 days, then <b>Exclude</b> → Purchase in 14 days.',
      '<b>IG engagers 90d</b>: Custom audience → Meta sources: <b>Instagram account</b> → Everyone who engaged with this professional account, 90 days.',
      '<b>Lookalike 1% India</b>: Create audience → <b>Lookalike</b> → source = Visitors 90d (later: buyers) → Location India → 1%.'
    ],
    copy: [['Visitors 30d', 'ST · Visitors 30d'], ['Visitors 90d', 'ST · Visitors 90d'], ['Cart no buy 14d', 'ST · ATC no purchase 14d'], ['IG engagers 90d', 'ST · IG engagers 90d'], ['Lookalike', 'ST · LAL 1% IN · visitors 90d']],
    links: [['Ads Manager: audiences', 'https://adsmanager.facebook.com/adsmanager/audiences'], ['Meta help: custom audiences', 'https://www.facebook.com/business/help/744354708981227'], ['Meta help: website custom audience', 'https://www.facebook.com/business/help/1474662202748341'], ['Meta help: create a lookalike', 'https://www.facebook.com/business/help/465262276878947']]
  },
  {
    id: 'a-camp', t: 'Set up your first small campaign', min: '30 min',
    why: 'One simple structure, so you learn what works without burning money.',
    steps: [
      'Ads Manager → <b>Create</b> → objective <b>Sales</b> → your dataset → conversion event <b>Purchase</b>.',
      '<b>Campaign A, "ST · Retarget"</b>: audience = Visitors 30d + IG engagers 90d + Cart no buy 14d. Exclude buyers (Purchase 30d). Budget about <b>₹200/day</b>.',
      '<b>Campaign B, "ST · New people"</b>: an <b>Advantage+ sales campaign</b> (Meta finds buyers itself), India, or a normal Sales campaign with Lookalike 1% India. Budget about <b>₹300/day</b>.',
      'Placements: Advantage+ placements (Meta picks; Instagram Reels and Stories usually win for you).',
      '3 ads per campaign: 1 carousel, 1 Reel, 1 single image. Use the copy prompt below.',
      'In each ad, under <b>Tracking → URL parameters</b>, paste the UTM line below.',
      'Run 7 days without touching. Then turn off the ad with the highest cost per purchase, and make a new one.'
    ],
    copy: [['URL parameters for Meta ads', 'utm_source=facebook&utm_medium=paid_social&utm_campaign={{campaign.name}}&utm_content={{ad.name}}']],
    links: [['Ads Manager', 'https://adsmanager.facebook.com/'], ['Meta help: Advantage+ sales campaigns', 'https://www.facebook.com/business/help/1362234537597370'], ['Meta help: minimum budgets', 'https://www.facebook.com/business/help/203183363050448']],
    note: '₹500/day ≈ ₹15,000/month. These are starting points to learn with, not a promise of sales. Lower them if that\'s too much. Meta doesn\'t publish one fixed rupee minimum; Ads Manager tells you if a budget is too low when you type it.'
  },
  {
    id: 'a-copy', t: 'Write ad copy in the brand voice', min: '15 min',
    why: 'Ads that sound like your posts feel like a friend, not an ad.',
    steps: ['Copy the prompt, fill in the set at the bottom, paste into ChatGPT or Claude.', 'Pick 2 primary texts and 2 headlines per ad. Read them out loud. Cut anything that sounds like an ad.'],
    prompt: { label: 'Copy ad copy prompt', text: '' }
  },
  {
    id: 'a-weekly', t: 'Do a 15-minute weekly ad check', min: '15 min a week',
    why: 'Small weekly fixes beat big monthly panics.',
    steps: ['Ads Manager → last 7 days. Columns: Amount spent, Purchases, Cost per purchase, CTR.', 'Ads with CTR under ~0.8% after 1,000+ impressions: replace the creative.', 'Compare with Shopify Analytics sales from Facebook/Instagram (UTM report).', 'Never raise a budget more than ~20% at a time.']
  }
  ]
},
{
  id: 's7', set: 'brainwave', icon: '🔗', title: 'UTM links',
  sub: 'Labels on your links so you know which post sold.',
  tasks: [
  {
    id: 'u-what', t: 'Know what a UTM is (one line)', min: '1 min',
    why: 'A UTM is a label added to the end of a link that tells Google Analytics and Shopify where a visitor came from.',
    steps: [
      '<b>source</b> = where (instagram, whatsapp, google).',
      '<b>medium</b> = how (social, paid_social, email, whatsapp, referral).',
      '<b>campaign</b> = why (launch_oct26, diwali_26, shaadi_season).',
      '<b>content</b> = which exact post or ad (carousel_bill_idhar, reel_wild_card_v2).',
      'Always lowercase, underscores, no spaces. Same words every time.'
    ]
  },
  {
    id: 'u-build', t: 'Make a link with the builder', min: '2 min',
    why: 'Paste the result in your bio, story link sticker, WhatsApp or emails.',
    html: 'utm',
    steps: ['Paste the page you want people to land on (a product is best).', 'Pick source and medium, type campaign and content.', 'Tap <b>Copy link</b>. Your last 5 links are saved below the button on this phone.']
  },
  {
    id: 'u-see', t: 'See which links worked', min: '5 min',
    why: 'Then you make more of what works.',
    steps: [
      '<b>GA4</b> → <b>Reports</b> → <b>Acquisition</b> → <b>Traffic acquisition</b>. Change the first column to <b>Session campaign</b> or <b>Session source / medium</b>.',
      '<b>Shopify</b> → <b>Analytics → Reports</b> → Category <b>Marketing</b> → "Sessions attributed to marketing campaigns" / "Performance by marketing campaign". Links with <code>utm_campaign</code> count as marketing. Marketing results also show in the <b>Growth</b> section.',
      'Don\'t add UTMs to links inside your own store (it breaks the data).'
    ],
    links: [['GA4 help: traffic acquisition', 'https://support.google.com/analytics/answer/12923437'], ['Google: Campaign URL Builder', 'https://ga-dev-tools.google/ga4/campaign-url-builder/'], ['Shopify help: marketing performance', 'https://help.shopify.com/en/manual/promoting-marketing/analyze-marketing/marketing-performance'], ['Shopify Analytics reports', A + '/analytics/reports']]
  }
  ]
},
{
  id: 's8', set: 'diet-cherry', icon: '💌', title: 'Grow your email and WhatsApp list',
  sub: 'People who said yes to hearing from you. Your own audience.',
  tasks: [
  {
    id: 'e-discount', t: 'Create a welcome discount', min: '5 min',
    why: 'A small thank-you makes signing up worth it.',
    steps: ['<b>Discounts</b> → <b>Create discount</b> → <b>Amount off order</b>.', 'Code: <b>HELLOTALK</b> (or your own). 10% off. Limit to one use per customer.', 'Save. Keep it simple: one welcome offer, not a new sale every week.'],
    copy: [['Code', 'HELLOTALK']],
    links: [['Discounts', A + '/discounts'], ['Shopify help: discount codes', 'https://help.shopify.com/en/manual/discounts']]
  },
  {
    id: 'e-forms', t: 'Add a signup form with Shopify Forms (free)', min: '20 min',
    why: 'Turns visitors into people you can email for free.',
    steps: [
      'Shopify App Store → <b>Shopify Forms</b> → <b>Install</b>.',
      '<b>Apps → Forms → Create form</b> → <b>Popup</b>: "Get 10% off your first set" + email. Attach the HELLOTALK discount (the app supports adding a discount to a form) → <b>Save</b>.',
      'Keep the marketing consent wording Shopify suggests. Don\'t pre-tick anything.',
      'Forms only show once the <b>Forms app embed</b> is on in the theme (Edit theme → App embeds). Ask the orchestrator to switch it on in the Claude build (message below), then click <b>Turn form on</b>.'
    ],
    links: [['Shopify Forms app', 'https://apps.shopify.com/shopify-forms'], ['Shopify help: Forms', 'https://help.shopify.com/en/manual/promoting-marketing/create-marketing/forms-app'], ['Shopify help: create a form', 'https://help.shopify.com/en/manual/promoting-marketing/create-marketing/forms-app/create']],
    prompt: { label: 'Copy message for the orchestrator', text: 'I installed Shopify Forms and made a popup form. Please have the theme lock holder switch on the Shopify Forms app embed on theme 186651934933 (Customize → App embeds), check it on the preview at 390 px (no overlap with the hero, closes with Escape, accessible), and tell me when it\'s on.' }
  },
  {
    id: 'e-checkout', t: 'Ask for email consent at checkout', min: '3 min',
    why: 'Buyers are your best list. Ask them nicely.',
    steps: ['<b>Settings → Checkout</b> → <b>Marketing opt-in</b>.', 'Turn on the email sign-up option at checkout. Leave it <b>not pre-selected</b>.', 'Save. Everyone who agrees lands in <b>Customers → Email subscribers</b>.'],
    links: [['Settings → Checkout', A + '/settings/checkout'], ['Shopify help: marketing consent', 'https://help.shopify.com/en/manual/promoting-marketing/create-marketing/customer-contact-information']]
  },
  {
    id: 'e-email', t: 'Send a welcome email (Shopify Messaging)', min: '30 min',
    why: 'An automatic hello when someone signs up. Set once, works forever.',
    steps: [
      'Shopify Email is now called <b>Shopify Messaging</b>. Install it (link), then create an automation from the welcome-new-subscriber template.',
      'Write it in your voice: who you are in 2 lines, the seven moments, the HELLOTALK code. Use the prompt below for a draft.',
      'Turn it on. Then send yourself a test.',
      'Every 2 weeks send one email: a new Journal story, a carousel, or a set in a moment. Your plan includes <b>10,000 free emails a month</b>; after that it\'s about US$1 per 1,000.'
    ],
    links: [['Shopify Messaging app', 'https://apps.shopify.com/shopify-messaging'], ['Shopify help: Shopify Messaging', 'https://help.shopify.com/en/manual/promoting-marketing/create-marketing/shopify-messaging'], ['Shopify help: email pricing', 'https://help.shopify.com/en/manual/promoting-marketing/create-marketing/shopify-messaging/email/pricing']],
    prompt: { label: 'Copy welcome-email prompt', text: `Write a short welcome email for my press-on nail brand Small Talk. Subject line (3 options, max 40 characters), preview text, and body under 120 words. Voice: warm, witty Hinglish in Roman script, like a friend; no "queen", no hype, no fake reviews or counts. Mention the seven sets as moments (On Me "Bill idhar.", Brainwave "Haan, mera idea hai.", Diet Cherry "Haan, wohi wali.", Green Flag "Tum aa jao. Main dekh lungi.", Shaadi Shift "Dulhan tu. Duty meri.", Wild Card "Achha. Tum pehle.", Pinky Promise "Haath do. Main hoon."), the code HELLOTALK for 10% off the first order, and one button "Find your set".` }
  },
  {
    id: 'e-wa', t: 'Pick your WhatsApp setup', min: '20 min',
    why: 'In India, WhatsApp gets read far more than email. Start simple, upgrade later.',
    steps: [
      '<b>Now (free):</b> install the <b>WhatsApp Business</b> app on a separate number. Add your catalogue, a greeting message and quick replies. Put the number on Instagram.',
      '<b>Check first:</b> Shopify Messaging added WhatsApp marketing in July 2026 (opted-in subscribers only, checkout WhatsApp checkbox). Whether it works for Indian stores isn\'t confirmed; open its help page and see.',
      '<b>Later (paid):</b> an official WhatsApp Business API provider sends order updates, cart reminders and broadcasts to opted-in people. Indian options with Shopify apps: <b>Interakt</b> (from about US$41/month), <b>Wati</b> (from about US$69/month), <b>AiSensy</b> and <b>Gupshup</b> (free plans). Meta charges per message on top. Every marketing template needs Meta approval.',
      '<b>Consent rule:</b> only message people who clearly said yes to WhatsApp messages from Small Talk. Every broadcast needs a Meta-approved template and an easy way to stop.'
    ],
    links: [['WhatsApp Business app', 'https://business.whatsapp.com/products/business-app'], ['Shopify Messaging: WhatsApp', 'https://help.shopify.com/en/manual/promoting-marketing/create-marketing/shopify-messaging/whatsapp'], ['Interakt', 'https://apps.shopify.com/interakt-sales'], ['Wati', 'https://apps.shopify.com/wati-abandonedcart-recovery'], ['AiSensy', 'https://apps.shopify.com/aisensy-whatsapp-marketing'], ['Gupshup', 'https://apps.shopify.com/gupshup-workflow-automation'], ['WhatsApp Business Messaging Policy', 'https://whatsappbusiness.com/policy/?lang=en'], ['Meta: getting WhatsApp opt-in', 'https://developers.facebook.com/documentation/business-messaging/whatsapp/getting-opt-in']]
  },
  {
    id: 'e-rules', t: 'Keep consent simple and correct', min: '2 min',
    why: 'Trust is the brand. One spammy message can lose a follower forever.',
    steps: ['Only email or WhatsApp people who said yes. Buying or importing lists is a no.', 'Boxes are never pre-ticked.', 'Every email has an unsubscribe link (Shopify adds it). On WhatsApp, reply STOP must work.', 'Say what you\'ll send and how often, and stick to it.']
  }
  ]
}
];
