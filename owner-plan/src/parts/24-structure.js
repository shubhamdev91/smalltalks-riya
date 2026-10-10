/* ---------- v5 structure: Riya's plan + Our list (owner restructure, 10 Oct) ---------- */
const OLD = {};
[...SECTIONS_A, ...SECTIONS_B, ...SECTIONS_C, ...SECTIONS_D].forEach(s => s.tasks.forEach(t => { OLD[t.id] = t; }));
const pick = (id, over) => Object.assign({}, OLD[id], over || {});
const IG = 'https://www.instagram.com/smalltalks_com/';
const FACTS_LINE = 'Kit: 24 almond press-ons in 12 sizes, nail glue, a sheet of adhesive tabs, a mini file, a prep pad, a cuticle stick and an instruction card. Wear: with glue up to about 2 weeks, with tabs 1–3 days, depending on prep and how much your hands do that week. Reusable if removed gently. Prices in INR include GST. Ships within India; dispatch within 2 business days, delivery up to 7 days. Returns within 15 days if unused and sealed.';

/* ---------- new SEO & AEO prompts ---------- */
const SEO_RULES = `SMALL TALK SEO RULES (follow exactly):
- Titles: "{Page subject} | Small Talk", max 60 characters, subject first, brand last.
- Meta descriptions: 120–155 characters; say what the page offers plus one distinctive detail.
- Never in titles, meta or alt text: "best", "No. 1", "almond", wear time, "reusable", "non-damaging"/"safe for nails", materials, kit counts, delivery speed or "India", reviews, ratings, customer counts.
- Alt text: max 125 characters; name the set and what is visibly there; illustrations start with "Illustration:"; packaging = "press-on nail box", never "photo of hands"; no keywords stuffing.
- Brand names to copy exactly: On Me, Brainwave, Diet Cherry (never "Cherry Repeat"), Green Flag, Shaadi Shift, Wild Card, Pinky Promise. Brainwave's line is "Haan, mera idea hai."
- AEO = answer-first plain text that a person (or an AI answer) can quote; no special "AI" tricks, no fake FAQ, no promises of ranking.`;

const SEO_FIND_PROMPT = `You are an SEO researcher for an Indian D2C brand. Brand: Small Talk, premium press-on nails for 18–24 urban Indian women; seven designs (On Me burgundy/tortoiseshell/gold; Brainwave cobalt/pearl/silver; Diet Cherry deep red/silver/blush French tip; Green Flag emerald/blush French tip; Shaadi Shift pink/deep red/yellow daisy; Wild Card lime/blush/cobalt-white checks; Pinky Promise lilac with burgundy tips). Store pages: home, Shop all sets, 7 product pages, Nail Guide (sizing, applying, removing), Help (delivery, returns, contact), Journal (stories), the talks (anonymous community board).

Task:
1. List 40 search queries Indian shoppers type about press-on nails (English and Hinglish, e.g. "press on nails price in india", "how to remove press on nails at home", "press on nails for wedding guest").
2. Add 20 real-sounding QUESTIONS people ask Google or ChatGPT ("are press-on nails bad for your nails?", "how long do press on nails last with glue?").
3. Group everything by intent: buy / compare / how-to / occasion / worry.
4. For each group say which existing page should answer it, and mark "NEW JOURNAL POST" where no page fits.
5. Do NOT invent search volumes or rankings. Write "check in Google Trends / Search Console" instead.
Output as a table: query or question | intent | best page | new post? (yes/no).`;

const SEO_ARTICLE_PROMPT = `Write a Journal post for my press-on nail brand Small Talk that answers ONE real question.
QUESTION: [paste one question from your list]

BRAND + VOICE: warm, witty, a friend explaining; light Hinglish in Roman script where natural; Indian context; no hype, no "queen", no empowerment speech.
FACTS YOU MAY USE (and nothing beyond them): ${FACTS_LINE}
HONESTY RULES: no medical or "safe/non-damaging for nails" claims; no wear-time or reuse promises beyond the facts above (always say "depends on prep and how much your hands do"); no fake reviews, quotes, counts or "bestseller"; no competitor bashing; no "best"; no college/campus references.

FORMAT:
1. Answer-first: the first 2 sentences directly answer the question.
2. 600–900 words, short paragraphs, 3–5 H2 subheadings phrased as the questions people ask.
3. One "Quick answer" box of 3 bullet points near the top.
4. Link ideas (I add the links): the Nail Guide for sizing/applying/removing; one or two set pages that fit the topic.
5. End with one soft line pointing to a set, not a hard sell.
Then give me: SEO title (max 60 characters, "{subject} | Small Talk"), meta description (120–155 characters), a 1-sentence excerpt, and alt text (max 125 characters) for one image idea.
${SEO_RULES}`;

const SEO_GSC_PROMPT = `I run a small Shopify store (Small Talk press-on nails, India). Below are my Google Search Console exports for the last 28 days: the Queries table and the Pages table (pasted as CSV).
Please:
1. Summarise in 5 short bullets how the store is doing in Google (clicks, impressions, average position, trend if visible).
2. List up to 5 queries with many impressions but few clicks, and for each suggest a better title or meta description for the page that ranks (follow my rules below).
3. List queries where my average position is 8–20 (page 1–2 edge): which page to improve and how, in one line each.
4. Pull out any questions people asked that deserve a Journal post (answer-first).
5. Flag any page that gets no impressions at all and might have an indexing problem.
6. End with ONLY 3 actions for this month, most valuable first.
Don't invent numbers beyond the data. If something can't be told from the data, say so.
${SEO_RULES}

QUERIES CSV:
[paste]

PAGES CSV:
[paste]`;

const SEO_META_PROMPT = `Write the search listing for something new I'm adding to my Shopify store Small Talk (press-on nails, India).
WHAT IT IS: [product / Journal post / page], called [name]
WHAT THE PAGE SHOWS: [2–3 lines, or paste the text]
IMAGES: [describe each image in a few words: what is really in it]
Give me: (1) 3 SEO title options, (2) 3 meta description options, (3) alt text for each image, (4) a URL handle (short, lowercase, hyphens).
${SEO_RULES}`;

const SEO_OUTREACH_PROMPT = `Write a short, friendly outreach message from Riya, founder of Small Talk (premium press-on nails, India), to an Indian beauty or lifestyle creator or blog.
CREATOR: [name / handle], what they post about: [one line], one specific post of theirs I liked: [one line]
WHAT I OFFER: to send one Small Talk set of their choice to try, no obligation to post, and an honest take is welcome even if it's not glowing.
RULES: under 90 words; sounds like a real person, not a template; mention one of our sets that fits their style and its line (e.g. Shaadi Shift "Dulhan tu. Duty meri."); no fake urgency; no paying for positive reviews; say that if they do post about a gifted set, they need to label it as gifted/ad (India's ASCI influencer rules).
Give 2 versions: Instagram DM and email (with subject line).`;

/* ---------- new Instagram prompts ---------- */
const IG_CAL_PROMPT = `You are the social media planner for Small Talk, a premium press-on nail brand from India. Instagram: @smalltalks_com.
${'${VOICE}'}

MONTH: [e.g. November 2026]   STAGE: [1 = 1 post a day · 2 = 2 a day · 3 = 2–3 a day]
CONTENT MIX: about half Reels (AI-video set-moment reels + simple real-hand reels), about 30% carousels, about 20% single posts, plus 3–5 Stories every day.
Make a calendar table for the whole month: date | slot (morning/evening) | format | set | the moment | hook (first line / first second) | CTA | which tool to use (Carousel chat / AI video workflow / phone video). Then a separate list of daily Story ideas (polls, questions, behind-the-scenes, a question from the talks).
Use real Indian occasions in that month only if you are sure of the date; otherwise write "check date". Rotate all seven sets fairly. No fake reviews, giveaways I didn't ask for, or discounts I didn't give you.`;

const IG_BIO_PROMPT = `Write 5 Instagram bio options (max 150 characters each) for Small Talk, premium press-on nails from India, @smalltalks_com. Voice: warm, witty, a little understated, light Hinglish in Roman script. The idea: seven nail sets for the small moments you show your hand ("Bill idhar." · "Haath do. Main hoon."). Line 1 = what it is, line 2 = the feeling, line 3 = a soft call to action pointing to the link. No "queen", no "best", no hashtags, max 2 emoji.`;

const IG_REVIEW_PROMPT = `Here are my Instagram numbers for the last 7 days for Small Talk (@smalltalks_com): [paste: each post/reel with format, reach, likes, comments, saves, shares, profile visits, link taps; plus follower change]. Also my Shopify/GA4 sessions from Instagram this week: [number].
In 6 bullets: what worked best and why (format, set, hook), what flopped, and ONE thing to repeat and ONE thing to drop next week. Don't invent numbers.`;

/* ---------- helper prompt pinned at top ---------- */
function stuckPrompt(cur) {
  const step = cur ? `"${cur.t}" (part of "${cur.sec.title}")` : 'growing the store';
  return `Hi! I'm Riya. I run Small Talk, a premium press-on nail brand from India. I'm a first-year student and new to running a store, so please keep answers short and clear.

MY STORE: Shopify (Basic plan, prices in INR), store address 0nev20-vn.myshopify.com. Instagram: @smalltalks_com. Payment providers in India are third-party (Razorpay/PayU/Cashfree). I don't edit the store's theme code myself.
THE BRAND: seven press-on nail sets, each tied to a small moment where she shows her hand: On Me "Bill idhar.", Brainwave "Haan, mera idea hai.", Diet Cherry "Haan, wohi wali.", Green Flag "Tum aa jao. Main dekh lungi.", Shaadi Shift "Dulhan tu. Duty meri.", Wild Card "Achha. Tum pehle.", Pinky Promise "Haath do. Main hoon." Audience: 18–24 urban Indian women. Voice: warm, witty Hinglish, no hype, no fake reviews.
WHAT I'M DOING: ${step}.
WHERE I'M STUCK: [describe what you see, paste the error message, or attach a screenshot]

Please answer in numbered steps with the exact buttons to click (Shopify/Meta/Google as they look in 2026), tell me if a step could affect my live store or cost money, and never ask me for passwords, API keys or secret codes. Tell me where to paste those myself instead.`;
}

/* ---------- RIYA'S PLAN ---------- */
const RIYA = [
{
  id: 's1', set: 'on-me', icon: '💳', title: 'Make the store able to sell',
  sub: 'Payments, a test order, and two policy snippets.',
  tasks: [
    pick('pay', { lock: true }),
    pick('g-test'),
    { id: 'p-repaste', t: 'Re-paste 2 updated policy snippets', min: '5 min',
      why: 'The talks have no review queue any more, so two pasted texts that say posts may be "held" need the new wording. Needed only if the old versions are in your policies (they were pasted on 10 Oct).',
      steps: [
        '<b>Settings → Policies → Privacy policy</b>. Find the section "the talks (our community board)". Replace that whole paragraph with the new one (copy below). <b>Save</b>.',
        '<b>Settings → Policies → Terms of service</b>. Replace section "6. the talks" with the new section 6 (copy below), or replace the whole Terms with the full text. <b>Save</b>.',
        'Check: the privacy text now says "may be refused when you submit them, or removed later", and Terms §6 says "Our filter may stop a post from going up".'
      ],
      copy: [['Copy privacy paragraph', PRIVACY_TALKS], ['Copy Terms section 6', TERMS_S6], ['Copy full Terms', TERMS_TEXT]],
      links: [['Settings → Policies', A + '/settings/legal'], ['Check: Privacy policy', STORE + '/policies/privacy-policy'], ['Check: Terms of service', STORE + '/policies/terms-of-service']],
      note: 'Skip this if the policies already show the new wording. Words by the copy session (register v1.7). Not legal advice.' }
  ]
},
{
  id: 's3', set: 'diet-cherry', icon: '💬', title: 'Turn on the talks',
  sub: 'Your two secret-key steps. After that the talks run themselves.',
  foot: '🔜 Coming soon to the talks: "get a ping when someone replies" (WhatsApp or email, only if she agrees).',
  tasks: [
    pick('t-email', { lock: true }),
    pick('t-vercel', { lock: true, steps: [
      'Start once <b>Settings → Apps</b> lists the talks app "Small Talk talks".',
      ...OLD['t-vercel'].steps
    ] }),
    pick('t-moderate', { optional: true, habit: false, t: 'Optional: look at reported talks now and then', min: '2 min, when you like',
      why: 'Nothing waits on you. Posts go live straight away, risky ones (contact details, links, handles, slurs, spam, possible real names) are refused when someone tries to post, and a post that 3 different people report hides itself.',
      steps: [
        '<b>Content → Metaobjects → Talk thread</b>. Look for posts whose <b>Moderation note</b> says "auto-hidden: 3 reports" (Status shows Draft).',
        'Read it. Fine after all? Set Status <b>Active</b> and change <b>Reports</b> to <code>0</code> → Save. Not fine? Leave it hidden, or <b>⋯ → Delete</b>.',
        'Do the same in <b>Talk reply</b>.',
        'If someone emails you about a post that\'s about them, hide or delete it the same way.',
        'Emergency stop for all posting: <b>Talk settings → main → Posting open: off</b>.'
      ] })
  ]
},
{
  id: 's2', set: 'brainwave', icon: '🔍', title: 'Check your kit facts',
  sub: 'Only you know the real box.',
  tasks: [
  {
    id: 'f-confirm', t: 'Confirm 6 facts about your real kit', min: '1 hour + 2 weeks of wearing',
    why: 'The site promises these to every customer. Only you can check them against the real box.',
    steps: [
      '<b>Kit contents</b>: open one real kit. Site says: 24 almond press-ons in 12 sizes, nail glue, a sheet of adhesive tabs, a mini file, a prep pad, a cuticle stick, an instruction card.',
      '<b>Sizes</b>: measure one nail per size with a ruler. Site says size 0 = 18 mm down to size 11 = 7 mm.',
      '<b>Applying and removing</b>: put on a full set following the Nail Guide on the preview, then remove it the way it says. Note anything wrong or confusing.',
      '<b>Wear time</b>: site says glue up to about 2 weeks, tabs 1–3 days, reusable if removed gently. Wear a set and note when nails start lifting.',
      '<b>Delivery</b>: can you really pack within 2 business days and deliver within 7 days (ask your courier, e.g. Shiprocket)?',
      '<b>Returns</b>: are 15-day returns (unused, sealed) OK for you?',
      'Write down only what\'s different and send that list to Shubham.'
    ],
    links: [['Preview: Nail Guide', STORE + '/pages/nail-guide-desi?preview_theme_id=186651934933'], ['Preview: On Me product page', STORE + '/products/bill-idhar?preview_theme_id=186651934933'], ['Shiprocket app', 'https://apps.shopify.com/shiprocket']]
  },
    pick('f-photos', { optional: true, t: 'Real product photos (optional, later)', steps: [
      'Daylight near a window. Plain card in the set colour behind.',
      'Per set: the closed box, the open tray, one hand wearing the set, a close-up of 2 nails.',
      'Phone main camera (1×), no filters.',
      'Put them in a shared folder, one folder per set, and send Shubham the link.'
    ] })
  ]
},
{
  id: 's4', set: 'green-flag', icon: '🚀', title: 'Go live',
  sub: 'The live store runs an older copy of the Claude build. Updating it = duplicate the build, publish the copy.',
  tasks: [
    pick('g-preview', { steps: [
      'Open the preview link on your phone.',
      'Home: the hero animation plays, swipe between sets, scroll all 7 chapters.',
      'Open 2–3 products. Add one to bag. Change quantity. Remove it.',
      'Open Nail Guide, Help, Our Story, Journal, the talks.',
      'Check the footer links work.',
      'Screenshot anything weird and send it to Shubham with one line on what\'s wrong.'
    ] }),
  {
    id: 'g-publish', t: 'Publish the newest store (and know how to undo it)', min: '10 min',
    why: 'Your live store runs an older copy of the build. Publishing a fresh copy makes the newest version live. Undo takes 30 seconds.',
    steps: [
      'Only after: payments on, test order done, and the preview looks right.',
      'Message Shubham 30 minutes before you publish.',
      '<b>Online Store → Themes</b>. Under <b>Draft themes</b> find "<b>Small Talk — Claude build (Horizon)</b>" (ID 186651934933). Don\'t publish this one itself: it\'s the working copy.',
      'On it click <b>⋯</b> → <b>Duplicate</b>. Wait for "Copy of Small Talk — Claude build (Horizon)" to appear.',
      'On that <b>copy</b> click <b>Publish</b> → confirm. The previous live theme moves into Draft themes.',
      'Open your store in a private/incognito tab and click around for 2 minutes.',
      '<b>Never</b> click Customize or Edit code on the live theme. Changes made there are lost at the next publish.',
      '<b>To undo:</b> Draft themes → the previous live theme → <b>Publish</b>. Products, orders and policies don\'t change when you switch themes.'
    ],
    links: [['Online Store → Themes', A + '/themes'], ['Shopify help: duplicate a theme', 'https://help.shopify.com/en/manual/online-store/themes/managing-themes/duplicating-themes'], ['Shopify help: publish / roll back', 'https://help.shopify.com/en/manual/online-store/themes/managing-themes/publishing-themes']]
  }
  ]
},
{
  id: 's5', set: 'pinky-promise', icon: '📊', title: 'Know your visitors',
  sub: 'Meta + Google + Shopify, so you see who comes and what they do.',
  tasks: SECTIONS_B[0].tasks.map(t => t.id === 'g-gsc' ? Object.assign({}, t, {
    prompt: undefined,
    steps: [
      'Do this after the new store is live and has no password.',
      'Open Search Console → <b>Add property</b> → <b>URL prefix</b> → your store address.',
      'Choose <b>HTML tag</b> and copy the tag (it isn\'t a secret). Send the tag to Shubham.',
      'Once the tag is on the live store, click <b>Verify</b>.',
      '<b>Indexing → Sitemaps</b> → type <code>sitemap.xml</code> → <b>Submit</b>.'
    ],
    note: undefined
  }) : t).map(t => t.id === 'g-domain' ? Object.assign({}, t, { optional: true }) : t)
},
{
  id: 's13', set: 'shaadi-shift', icon: '🔎', title: 'SEO & AEO',
  sub: 'Get found on Google, and quoted by AI answers.',
  tasks: [
  {
    id: 'seo-basics', t: 'SEO vs AEO in 2 minutes', min: '2 min',
    why: 'Two names, one habit: answer real questions clearly on your own pages.',
    wwg: ['<b>SEO</b> helps Google list your pages when someone searches. <b>AEO</b> (answer engine optimisation) helps ChatGPT, Gemini and Google\'s AI answers quote you.', 'Both reward the same things: a clear page per topic, the answer in the first lines, honest facts, and other sites mentioning you. There are no secret AI tricks.', 'A simple monthly routine (the next 5 tasks) that slowly brings free visitors.'],
    steps: ['The technical side is already set up: page titles, Google-readable product data, one page per topic, no fake reviews.', 'Your job: questions → answers → check what works → repeat monthly.', 'Results take 2–6 months. Don\'t judge it in week one.']
  },
  {
    id: 'seo-find', t: 'Find what your customers search and ask', min: '30 min',
    why: 'You write for real searches instead of guessing.',
    wwg: ['Builds a list of what Indian shoppers type and ask about press-on nails.', 'Every Journal post and title you write later comes from this list.', 'A table of searches and questions, each matched to a page or marked "new post".'],
    steps: ['Paste the prompt into ChatGPT or Claude.', 'Then check 5–10 of the ideas yourself: type them into Google and note the autocomplete suggestions and the "People also ask" box.', 'Look at Google Trends (India) to see which words people use more.', 'Save the final list in a Google Sheet called "Small Talk questions".'],
    prompt: { label: 'Copy keyword + question finder', text: SEO_FIND_PROMPT },
    links: [['Google Trends (India)', 'https://trends.google.com/trends/?geo=IN']]
  },
  {
    id: 'seo-journal', t: 'Write one Journal post a month that answers a real question', min: '1–2 hours a month',
    why: 'One honest answer page a month adds up to a library that Google and AI answers can quote.',
    wwg: ['Turns one question from your list into a helpful post.', 'Answer-first posts are the kind AI answers and "People also ask" pick up.', 'A ready draft with title, description, excerpt and alt text.'],
    steps: [
      'Pick one question from your list. Paste the prompt with that question.',
      'Read it out loud. Fix anything that doesn\'t sound like you or claims something you can\'t promise.',
      'Shopify: <b>Content → Blog posts</b> (older admins: Online Store → Blog posts; or type "Blog posts" in the admin search) → <b>Add blog post</b>. Blog: <b>Journal</b>. Keep it <b>Hidden</b> first.',
      'Fill the search engine listing with the title and description from the draft. Add the image with its alt text.',
      'The Journal design was built for story posts. Before you make it visible, preview it on your phone; if anything looks off, keep it hidden and send Shubham a screenshot.'
    ],
    prompt: { label: 'Copy Journal article prompt', text: SEO_ARTICLE_PROMPT },
    links: [['Shopify help: writing blog posts', 'https://help.shopify.com/en/manual/online-store/blogs/writing-blogs']]
  },
  {
    id: 'seo-gsc', t: 'Monthly 20-minute Search Console review', min: '20 min a month',
    why: 'Shows which searches already find you, so you improve what\'s close to working.',
    wwg: ['Reads your real Google data and picks 3 actions.', 'Small fixes to titles and posts on almost-ranking pages are the fastest wins.', 'A short summary and 3 clear actions for the month.'],
    steps: [
      'Needs Search Console set up (section "Know your visitors") and about 4 weeks of data.',
      'Search Console → <b>Performance</b> → <b>Search results</b> → date: last 28 days → <b>Export</b> → download.',
      'Open the Queries and Pages tables, copy them, and paste them into the prompt.',
      'Do the 3 actions. Note them in your "Small Talk questions" sheet.'
    ],
    prompt: { label: 'Copy Search Console review prompt', text: SEO_GSC_PROMPT },
    links: [['Google Search Console', 'https://search.google.com/search-console'], ['Help: Performance report', 'https://support.google.com/webmasters/answer/7576553'], ['Help: impressions, clicks, position', 'https://support.google.com/webmasters/answer/7042828']]
  },
  {
    id: 'seo-meta', t: 'SEO title, description and alt text for anything new', min: '10 min each time',
    why: 'Every new product, post or image needs its own clear listing, or Google guesses.',
    wwg: ['Writes the search listing and image descriptions for anything you add.', 'Good titles get clicks; alt text helps Google Images and people using screen readers.', 'Ready-to-paste title, description, alt text and URL handle.'],
    steps: [
      'Paste the prompt and fill in what you\'re adding.',
      'Product or post: scroll to <b>Search engine listing</b> → <b>Edit</b> → paste title and description → Save.',
      'Images: click the image → <b>Add alt text</b> → paste → <b>Save alt text</b>.',
      'Don\'t change the existing seven products\' listings; they\'re already done.'
    ],
    prompt: { label: 'Copy title / description / alt text prompt', text: SEO_META_PROMPT },
    links: [['Shopify help: SEO titles and descriptions', 'https://help.shopify.com/en/manual/promoting-marketing/seo/adding-keywords'], ['Shopify help: alt text', 'https://help.shopify.com/en/manual/products/product-media/add-alt-text']]
  },
  {
    id: 'seo-mentions', t: 'Get mentioned by Indian beauty creators and blogs', min: '30 min a week',
    why: 'Mentions and links from other sites are the strongest signal for Google and AI answers.',
    wwg: ['Writes a short, honest note to creators and blogs offering a set to try.', 'Other people talking about you builds trust and search authority.', 'A DM and an email version you personalise in 2 minutes.'],
    steps: [
      'Make a list of 20 small Indian nail, beauty or lifestyle creators (5k–50k followers) and 5 blogs whose style fits a set.',
      'Each week, send 5 personal messages using the prompt. Never copy-paste the same text to everyone.',
      'If they post about a gifted set, they must label it as gifted or ad (India\'s ASCI rules). Never pay for a positive review.',
      'Track who replied in your sheet.'
    ],
    prompt: { label: 'Copy outreach prompt', text: SEO_OUTREACH_PROMPT },
    links: [['ASCI (advertising standards, India)', 'https://www.ascionline.in/']]
  }
  ]
},
{
  id: 's14', set: 'wild-card', icon: '📱', title: 'Your Instagram plan',
  sub: '@smalltalks_com: a clear mix, a steady rhythm, one batch day a week.',
  tasks: [
  {
    id: 'ig-mix', t: 'Your content mix and posting rhythm', min: '5 min',
    why: 'Knowing what to post and how often stops the daily "what do I post?" panic.',
    html: 'igmix',
    steps: [
      '<b>Mix</b>: about half <b>Reels</b> (AI-video set-moment reels + simple real-hand reels), about 30% <b>carousels</b>, about 20% <b>single posts</b>. Plus <b>3–5 Stories every day</b>.',
      '<b>Ramp up</b>: weeks 1–2 post <b>1 a day</b>. Weeks 3–4 <b>2 a day</b>. After that <b>2–3 a day</b>, but only if your weekly batch keeps the quality. If it slips, go back a step.',
      'Use the weekly numbers in the table below for each stage.',
      'Make carousels with <a href="#sec-s10">Carousels</a> and AI reels with <a href="#sec-s11">AI videos</a>. Simple reels: your hand wearing a set, unboxing, a 10-second "apply one nail" clip.'
    ]
  },
  {
    id: 'ig-batch', t: 'Your weekly batch day', min: '3–4 hours a week',
    why: 'Making a week of posts in one sitting keeps quality up and weekdays free for study.',
    steps: [
      'Pick one day (e.g. Sunday). Open your monthly calendar and take this week\'s slots.',
      'Make the carousels for the week with the <a href="#sec-s10">Carousels</a> prompts.',
      'Make the AI reels with the <a href="#sec-s11">AI videos</a> workflow (1–2 a week is plenty; they take time).',
      'Film the simple reels in one go: same light, 3–4 sets, 10–15 seconds each.',
      'Write all captions in one chat. Add a UTM link only in the bio and Stories (section "UTM links").',
      'Schedule: in Instagram\'s post screen use <b>Advanced settings → Schedule</b>, or Meta Business Suite → <b>Planner</b>.',
      'Stories stay live and daily: polls, "which set for tonight?", behind the scenes, a question from the talks.'
    ],
    links: [['Meta Business Suite', 'https://business.facebook.com/']]
  },
  {
    id: 'ig-cal', t: 'Make your monthly calendar', min: '20 min a month',
    why: 'One prompt gives you the whole month, so batch day is just "make".',
    steps: ['Paste the prompt, fill in the month and your stage (1, 2 or 3).', 'Check every date and occasion it suggests.', 'Copy the table into a Google Sheet. Tick posts off as you schedule them.'],
    prompt: { label: 'Copy monthly calendar prompt', text: '' }
  },
  {
    id: 'ig-profile', t: 'Tune up your profile', min: '15 min',
    why: 'Your profile turns a curious visitor into a store visit.',
    steps: [
      '<b>Bio</b>: use the prompt for 5 options; pick one that sounds like you.',
      '<b>Link in bio</b>: make it with the UTM builder (source instagram, medium social, campaign bio, content link_in_bio) and point it at the shop page.',
      '<b>Highlights</b>: Sets · How to apply · the talks · Help. Simple covers in set colours.',
      '<b>Pin</b> 3 posts: your intro carousel, your best reel, the how-to.',
      'Contact button: your store email.'
    ],
    prompt: { label: 'Copy bio prompt', text: IG_BIO_PROMPT },
    links: [['Open @smalltalks_com', IG]]
  },
  {
    id: 'ig-review', t: 'Your 10-minute weekly review', min: '10 min a week',
    why: 'Doing more of what works is how small accounts grow.',
    steps: [
      'Instagram → <b>Professional dashboard</b> → <b>Insights</b> → last 7 days.',
      'Note per post: reach, saves, shares, profile visits, link taps. Saves and shares matter most.',
      'Check Shopify Analytics or GA4 for visits from Instagram (your UTM links).',
      'Paste the numbers into the prompt. Pick one thing to repeat and one to drop next week.',
      'Reply to every comment and DM within a day, always.'
    ],
    prompt: { label: 'Copy weekly review prompt', text: IG_REVIEW_PROMPT }
  }
  ]
},
{
  id: 's10', set: 'brainwave', icon: '🎨', title: 'Carousels in the brand voice',
  sub: 'Hinglish moments. Nails as punctuation. No speeches.',
  tasks: [
    pick('ig-setup', { t: 'Set up your carousel chat (voice inside)', min: '10 min', html: 'voice',
      why: 'One chat that already knows your voice and nails = consistent posts. How many to make each week is in your Instagram plan.',
      steps: [
        'Each set is a <b>moment</b>, not a product feature. The nails are just there, doing the talking. Never: "queen", "boss babe", fake reviews, "bestseller", college or campus, soft-drink brand names, "Cherry Repeat", "mera idea tha".',
        'ChatGPT → new chat "Small Talk carousels". Attach <code>artwork\\chatgpt-refs\\&lt;set&gt;\\4-exact-nail-designs.png</code> and <code>artwork\\chatgpt-refs\\_shared\\character-sheet.png</code>.',
        'Paste the master prompt below. Wait for "ready".',
        'Weekly numbers: see <a href="#sec-s14">Your Instagram plan</a>.'
      ] }),
    pick('ig-ideas', { t: 'Pick an idea and make the carousel', min: '30–45 min each' })
  ]
},
{
  id: 's11', set: 'green-flag', icon: '🎬', title: 'AI videos with your characters',
  sub: 'Same women, same nails, shot after shot.',
  tasks: [
    { id: 'v-start', t: 'See the workflow and pick your tools', min: '10 min', html: 'tools',
      why: 'Six stages in order is what keeps the women and nails consistent. You need one image tool, one video tool and one editor.',
      steps: [...OLD['v-flow'].steps, 'Start with what you already pay for. Try free credits before paying; prices change, so check before you buy.', 'How many reels a week: see <a href="#sec-s14">Your Instagram plan</a>.'] },
    { id: 'v-sheet-script', t: 'Make the character sheet and the script', min: '30 min',
      why: 'The sheet is your "actor"; the script is one 12–15 second moment.',
      steps: [...OLD['v-sheet'].steps, 'Then paste the script prompt in Claude or ChatGPT with the set name, and pick the version where the hand moment hits hardest.'],
      prompts: [OLD['v-sheet'].prompts[0], OLD['v-script'].prompts[0]] },
    { id: 'v-board-shots', t: 'Storyboard, then make each shot as a still', min: '45 min',
      why: 'Fixing a still is easy; fixing a video isn\'t.',
      steps: ['Paste the storyboard prompt with your character block, style block and script.', ...OLD['v-shots'].steps],
      prompts: [...OLD['v-board'].prompts, OLD['v-shots'].prompts[0]] },
    { id: 'v-motion-post', t: 'Animate, edit and post', min: '1.5 hours',
      why: 'Short, simple moves look real; text and timing make it feel like Small Talk.',
      steps: [...OLD['v-i2v'].steps, ...OLD['v-edit'].steps],
      prompts: [OLD['v-i2v'].prompts[0], OLD['v-edit'].prompts[0]] },
    pick('v-example')
  ]
},
{
  id: 's7', set: 'on-me', icon: '🔗', title: 'UTM links',
  sub: 'Labels on your links so you know which post sold.',
  tasks: [
    pick('u-build', { t: 'Make labelled links and see which ones sell', min: '10 min',
      why: 'A UTM is a label at the end of a link that tells Google Analytics and Shopify where a visitor came from.',
      steps: [
        '<b>source</b> = where (instagram, whatsapp, google) · <b>medium</b> = how (social, paid_social, email) · <b>campaign</b> = why (launch_oct26) · <b>content</b> = which exact post (carousel_bill_idhar). Lowercase, underscores, same words every time.',
        'Use the builder below: paste the page, pick source and medium, type campaign and content, tap <b>Copy link</b>. Use it in your bio, Story link stickers, WhatsApp and emails. Never on links inside your own store.',
        'See results: <b>GA4 → Reports → Acquisition → Traffic acquisition</b> (switch to Session campaign), and <b>Shopify → Analytics → Reports</b> → Marketing → "Sessions attributed to marketing campaigns".'
      ],
      links: OLD['u-see'].links })
  ]
},
{
  id: 's8', set: 'diet-cherry', icon: '💌', title: 'Grow your email and WhatsApp list',
  sub: 'People who said yes to hearing from you.',
  tasks: [
    pick('e-discount'),
    pick('e-email', { note: 'Consent rules: only email people who said yes (no bought or imported lists), never pre-tick boxes, and say what you\'ll send and how often. Shopify adds the unsubscribe link.' }),
    pick('e-wa')
  ]
},
{
  id: 's6', set: 'pinky-promise', icon: '🎯', title: 'Retargeting ads',
  sub: 'Only after real visitors arrive. Start small.',
  tasks: [
    { id: 'a-start', t: 'When to start, and build your 5 audiences', min: '25 min',
      why: 'Ads to "people who visited" need visitors first; audiences are made once and reused forever.',
      steps: [...OLD['a-when'].steps, ...OLD['a-aud'].steps], copy: OLD['a-aud'].copy, links: OLD['a-aud'].links },
    pick('a-camp', { t: 'Run your first small campaign (copy prompt inside)', min: '45 min', prompt: OLD['a-copy'].prompt,
      steps: [...OLD['a-camp'].steps, 'For the ad words, paste the prompt below with the set name. Pick 2 primary texts and 2 headlines per ad; read them out loud.'] }),
    pick('a-weekly')
  ]
},
{
  id: 's12', set: 'shaadi-shift', icon: '📚', title: 'Resources',
  sub: 'Every link in one place.',
  tasks: [ pick('r-links', { optional: true, links: [...OLD['r-links'].links, ['Instagram @smalltalks_com', IG]] }) ]
}
];

/* ---------- OUR LIST (Shubham + Claude) ---------- */
const WIP = 'In progress';
const DONE = 'Done ✓ 10 Oct';
const OUR = [
{
  id: 'o1', set: 'on-me', icon: '⚙️', title: 'Store settings',
  sub: 'Done and verified 10 Oct, 18:39 IST, except the items marked otherwise.',
  tasks: [
    pick('refund', { who: 'Claude', status: DONE }),
    pick('refundflag', { who: 'Claude', status: 'Next: theme lock holder', t: 'Switch on "Refund policy text verified" (theme lock holder)', steps: ['Orchestrator reads back /policies/refund-policy.', 'The theme lock holder switches on "Refund policy text verified" on theme 186651934933 and checks Help → Returns and the footer link.'] }),
    pick('terms', { who: 'Claude', status: DONE }),
    pick('addr', { who: 'Claude', status: DONE, t: 'Remove the address-change line from the shipping policy', why: 'Decided: customers can NOT change the address after ordering (G13 = no). The live shipping policy still says they can.',
      steps: ['<b>Settings → Policies → Shipping policy</b> → delete the "Address changes" paragraph → <b>Save</b>.', 'Tell the orchestrator so Help and FACTS.md stay consistent (F12).'],
      prompt: { label: 'Copy message for the orchestrator', text: 'SD26 / G13 done: the "Address changes" paragraph is removed from the shipping policy (customers cannot change the address after ordering). Please make FACTS.md F12 and Help match.' } }),
    pick('money', { who: 'Claude', status: DONE }),
    pick('ship', { who: 'Claude', status: DONE, t: 'Rename the shipping rate to "Standard delivery"', note: 'Renamed to "Standard delivery". The ₹379 price and the international zone stay Shubham\'s/Riya\'s decision.' }),
    pick('seo', { who: 'Claude', status: DONE, t: 'Homepage title and description', note: 'The social sharing image comes from the theme at the next publish, so nothing to upload.' }),
    pick('logo', { who: 'Claude', status: DONE, t: 'Logo: checkout logo + files in Shopify', steps: ['Checkout logo is set (Settings → Checkout → Customize).', 'Logo files are uploaded to <b>Content → Files</b>.', 'Optional: Settings → Brand → pick the same file as Logo / Square logo so Shopify emails use it.'] }),
    pick('e-checkout', { who: 'Claude', status: WIP }),
    pick('g-password', { who: 'Claude', status: WIP })
  ]
},
{
  id: 'o2', set: 'diet-cherry', icon: '💬', title: 'Talks setup',
  sub: 'Starts after Riya verifies her Dev Dashboard email.',
  tasks: [
    pick('t-app', { who: 'Claude', status: 'Waiting on Riya\'s email', t: 'Create the app "Small Talk talks" (Claude in Chrome)' }),
    pick('t-version', { who: 'Claude', status: 'Waiting on Riya\'s email' }),
    pick('t-install', { who: 'Claude', status: 'Waiting on Riya\'s email' }),
    pick('t-publish', { who: 'Shubham', status: 'After Riya pastes keys' }),
    pick('t-tell', { who: 'Shubham', status: 'After v0 Publish' }),
    pick('t-privacy', { who: 'Claude', status: DONE }),
    pick('t-oldtalks', { who: 'Claude', status: 'After talks are live' }),
    { id: 'up-start', who: 'Shubham', status: 'After talks are live', t: 'Start the talks upgrades session (reply pings + private customer link)', min: '10 min',
      why: 'Reply pings with consent and a private link to signed-in customers grow the list without losing "no login".',
      steps: [...OLD['up-what'].steps, ...OLD['up-start'].steps.slice(1), 'Riya approves the consent wording and pastes the new privacy paragraph.'],
      prompt: OLD['up-start'].prompt }
  ]
},
{
  id: 'o3', set: 'green-flag', icon: '🧹', title: 'Facts, tidy-up and apps',
  sub: 'Small jobs that keep the store clean.',
  tasks: [
    pick('f-send', { who: 'Shubham', status: 'When Riya replies', t: 'Pass Riya\'s kit-fact corrections to Claude', steps: ['Collect Riya\'s WhatsApp answers from "Confirm 6 facts about your real kit".', 'Fill in the brackets and paste into the orchestrator session.'] }),
    pick('g-probe', { who: 'Claude', status: 'Any time' }),
    pick('g-oldpages', { who: 'Claude', status: 'With orchestrator' }),
    pick('g-apps', { who: 'Shubham', status: 'Optional' }),
    pick('e-forms', { who: 'Claude', status: 'Later' })
  ]
}
];

/* fill prompts that need the voice block */
(function () {
  const cal = RIYA.find(s => s.id === 's14').tasks.find(t => t.id === 'ig-cal');
  cal.prompt = { label: 'Copy monthly calendar prompt', text: IG_CAL_PROMPT.replace('${VOICE}', VOICE_RULES) };
})();
