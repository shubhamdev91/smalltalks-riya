/* ---------- plan data: sections 9-10 ---------- */
const SETS = [
  { key: 'on-me', name: 'On Me', line: 'Bill idhar.', note: 'I\u2019ve got this.', nails: 'burgundy \u00b7 tortoiseshell \u00b7 gold \u00b7 tortoiseshell \u00b7 burgundy', colour: '#FFB900', moment: 'She picks up the bill at dinner. No announcement.', handle: 'bill-idhar' },
  { key: 'brainwave', name: 'Brainwave', line: 'Haan, mera idea hai.', note: 'Called it.', nails: 'pearly white \u00b7 silver chrome \u00b7 cobalt \u00b7 pearly white \u00b7 cobalt (no checkerboard)', colour: '#073DF1', moment: 'A crescent-bag sketch in the margin becomes real. Whose idea? Hers.', handle: 'haan-mera-idea-tha' },
  { key: 'diet-cherry', name: 'Diet Cherry', line: 'Haan, wohi wali.', note: 'My usual.', nails: 'deep red \u00b7 silver chrome \u00b7 blush with pointed red French tip \u00b7 deep red \u00b7 deep red', colour: '#E10019', moment: 'New place, same order. Her friend already knows: the usual.', handle: 'haan-wohi-wali' },
  { key: 'green-flag', name: 'Green Flag', line: 'Tum aa jao. Main dekh lungi.', note: 'Sorted.', nails: 'emerald \u00b7 blush with emerald French tip \u00b7 emerald \u00b7 blush with emerald French tip \u00b7 emerald', colour: '#007948', moment: 'The plan falls apart. Her friend calls. She makes room: come over.', handle: 'tum-aa-jao-main-dekh-lungi' },
  { key: 'shaadi-shift', name: 'Shaadi Shift', line: 'Dulhan tu. Duty meri.', note: 'On duty.', nails: 'pink \u00b7 deep red \u00b7 pink with yellow daisy \u00b7 deep red \u00b7 pink', colour: '#FF0078', moment: 'One missing safety pin at the wedding. She\u2019s on duty for the bride.', handle: 'dulhan-tu-duty-meri' },
  { key: 'wild-card', name: 'Wild Card', line: 'Achha. Tum pehle.', note: 'Your move.', nails: 'lime \u00b7 blush with lime French tip \u00b7 lime \u00b7 cobalt-white checker \u00b7 lime', colour: '#B7EF00', moment: 'Game night. Cards face her, smile gives nothing away. You go first.', handle: 'achha-tum-pehle' },
  { key: 'pinky-promise', name: 'Pinky Promise', line: 'Haath do. Main hoon.', note: 'Right here.', nails: 'lilac with burgundy asymmetric pointed tip on all five', colour: '#6620F2', moment: 'A crowded room. A familiar hand reaches back for hers.', handle: 'haath-do-main-hoon' }
];

const SET_TABLE_TEXT = SETS.map(s => `- ${s.name} (set colour ${s.colour}): headline "${s.line}" · note "${s.note}" · moment: ${s.moment} · five-nail hand, thumb → little finger: ${s.nails}`).join('\n');

const VOICE_RULES = `BRAND: Small Talk, premium press-on nails from India for 18–24 urban desi women. Seven sets; each is tied to a small moment where she naturally shows her hand.
VOICE: warm, witty, a little understated. Hinglish the way friends text (Roman script), short lines, specific everyday Indian moments. The nails are the punctuation of the moment, not the topic of a lecture. Confidence is shown by what she does, never explained.
NEVER: empowerment speeches ("queen", "boss babe", "you deserve"), generic luxury words, forced slang, fake reviews, ratings, customer counts or "bestseller" claims, medical or "safe/non-damaging for nails" claims, any college/campus/university reference, third-party brand names (no soft-drink brands), the name "Cherry Repeat" (it is Diet Cherry), "Haan, mera idea tha" (it is "Haan, mera idea hai."). Copy each headline and note exactly as written.
THE SEVEN SETS:
${SET_TABLE_TEXT}`;

const CAROUSEL_MASTER = `You are the social copywriter and art director for my press-on nail brand. Read all of this, then reply "ready" and wait.

${VOICE_RULES}

FORMAT FOR EVERY CAROUSEL I ASK FOR:
1. Slide-by-slide copy, 6–8 slides, max 12 words per slide on the image. Slide 1 = a hook that makes her stop scrolling. Last slide = a soft call to action ("Shop On Me — link in bio" or "Save this for later"). Hindi words in Roman script.
2. For each slide, an IMAGE PROMPT I can paste into ChatGPT image generation. Style for illustrations: bold comic-ink Indian pop illustration, thick confident black ink outlines, flat saturated colour with soft cel shading, glossy highlights, winged eyeliner, bindi, gold jewellery, dense curly black hair, hands with exactly five fingers and natural joints, long glossy almond press-on nails matching the set's five-nail list EXACTLY (thumb → little finger). Background = the set colour hex. Portrait 1024 × 1536. No text, no logos, no watermark in the image (I add the words myself). For product slides say "realistic beauty product photography" instead.
3. Where the slide text sits (top / middle / bottom) so it doesn't cover the hand.
4. A caption (max 60 words, 1 question to invite comments) and 5–8 hashtags (mix of nail and Indian lifestyle tags, no brand claims).
5. Alt text for each slide (one plain sentence).
Before you answer, check every nail description against the set list above and fix any mismatch.`;

const CAROUSELS = [
  ['Seven moments, one hand', 'Intro: one slide per set. Each slide = the moment in one line + the headline. Cover: "Kuch baatein haath se hoti hain." (or write a better hook).'],
  ['Bill idhar. (On Me)', 'A 6-slide mini story: dinner runs long, one more round, the bill arrives, her hand reaches first. End on "Bill idhar." Nails: On Me.'],
  ['Whose idea was it? (Brainwave)', 'A sketch in the margin becomes a real crescent bag. Slides follow the idea from doodle to done. End: "Haan, mera idea hai."'],
  ['The usual (Diet Cherry)', 'Favourites that travel with you: same order, same seat, same song, same friend. Last slide: "Haan, wohi wali." No soft-drink brand names.'],
  ['Green flags in a friend (Green Flag)', 'Little things a real friend does when plans fall apart. Last slide: "Tum aa jao. Main dekh lungi."'],
  ['Bridesmaid duty list (Shaadi Shift)', 'Shaadi-season checklist of tiny saves: safety pin, lipstick, dupatta fix, chappals, calming the bride. Last slide: "Dulhan tu. Duty meri."'],
  ['Game night tells (Wild Card)', 'Funny tells at Uno / cards night. She just smiles. Last slide: "Achha. Tum pehle."'],
  ['Press-ons in 6 steps (how-to)', 'Saveable how-to from the Nail Guide steps (prep, size, glue or tabs, press 20–30 s, file, removal tip). Use real photos of your hand when you have them; until then, clean illustration of the hand only. Add: wear time depends on prep and how busy your hands are.']
];

const TALKS_PROMPT = `You are a new Claude Code session joining the Small Talk store project. Work at Opus, effort xhigh.

PROJECT: Small Talk, press-on nail brand (Shopify store 0nev20-vn.myshopify.com, Basic plan, INR, India). Owner: Riya (riyaagg24@gmail.com). Project folder: C:\\Users\\SSTS\\Desktop\\Riya.
READ FIRST: Small-Talk-Claude-Implementation-Checklist.md (RESUME HERE block = current truth), talks\\DESIGN.md, talks\\OWNER-SETUP.md, talks\\backend\\ (app.py + tests), copy\\07-talks.md, copy\\FACTS.md (F14), and the shared notes folder C:\\Users\\SSTS\\AppData\\Roaming\\Claude\\side-session-notes\\local_04b83008-0590-42b6-b099-ee4eb0903f2d (st-talks-live.md, 00-orchestrator-protocol.md).

RULES YOU MUST FOLLOW:
- The orchestrator session (local_e4896004-68cd-4d55-9d37-ab925783b63b) owns the checklist and the theme write lock. Report to it with SendMessage; never edit the checklist.
- Only theme 186651934933 ("Small Talk — Claude build (Horizon)") is ever written, and only while you hold a write-lock grant from the orchestrator that arrived after your last release. Never touch 186573160661 (LIVE), 186547241173, 186572636373, 162461974741, 186667663573.
- st-copy (local_ae886ffe-08a8-44d3-abdb-ee70ca852b0d) owns every shopper-visible word. Ask it for copy via the orchestrator; never write UI text yourself.
- st-talks (local_2c74a7fd-f54e-43a8-9df1-0baf05c20c22) built the talks; coordinate with it, don't fork its files.
- Shared data (metaobject definitions, products, policies, customers) = proposal to the orchestrator first; owner approves.
- Secrets (client secret, salt, any email/WhatsApp provider API key) are pasted by the owner into Vercel environment variables. Never ask for them in chat, never put them in files or the theme.
- No IP address collection, ever. Device-only spam keys as today.
- Every new data use needs explicit, unticked-by-default consent, a clear purpose line, and a way to undo it.

WHAT THE OWNER WANTS (two features):
(a) Reply pings. After someone posts a talk or reply, show an OPTIONAL field: "Get a ping when someone replies — add WhatsApp or email", with a consent checkbox (not pre-ticked) saying exactly what we'll send and how to stop. Store the contact privately (no storefront access, e.g. a private metaobject or a field with storefront access NONE), linked to that thread, deleted when the thread is deleted or on request, and with a one-tap unsubscribe. Propose the delivery channel with costs: email via a transactional provider called from the Vercel backend (owner pastes its key into Vercel), and WhatsApp only through an official WhatsApp Business API provider with a pre-approved utility template. Contacts collected here are for reply pings ONLY unless the person separately opts into marketing.
(b) Private customer link. If the shopper is signed in (new customer accounts), the App Proxy request carries Shopify's signed logged_in_customer_id. Store that ID privately with the post (never shown publicly, never in Liquid output, never in the public metaobject fields). Use it for marketing only when that customer's own Shopify marketing consent is "subscribed". This likely needs an extra scope (e.g. read_customers): list exact scope changes so the owner can re-approve the app.
Also: ask st-copy (via the orchestrator) for updated privacy-policy wording (TLK-155 successor) and talks UI copy covering both features; the owner pastes the policy text.

HOW TO WORK:
1. Read everything above. Then write a DESIGN addendum (talks\\DESIGN-pings-and-accounts.md): data model, consent text slots (IDs for st-copy), retention, deletion, scope changes, backend endpoints, abuse limits, costs, owner steps, test plan.
2. Send the orchestrator a one-line summary + the path, and wait for owner approval before any code, deploy, shared-data or theme change.
3. Build in talks\\backend with tests (the current suite must stay green), stage theme files under talks\\staged\\, request the lock from the orchestrator, install, release the lock, and give the orchestrator a readback.
4. Deploys to the owner's Vercel need the owner's OK in this session.`;

const SECTIONS_C = [
{
  id: 's9', set: 'shaadi-shift', icon: '🛎️', title: 'Ask Claude for two talks upgrades',
  sub: 'Reply pings, and quietly knowing which posts came from your customers.',
  tasks: [
  {
    id: 'up-what', t: 'Understand the two upgrades', min: '3 min',
    why: 'Both grow your list from people who already care, without losing the "no login" feel.',
    steps: [
      '<b>(a) Reply pings.</b> After posting, a girl can add WhatsApp or email to hear when someone replies. Only if she ticks a box. Pings only, no marketing unless she says yes to that separately.',
      '<b>(b) Private customer link.</b> If she\'s signed in to your store, her post is privately linked to her customer record. Nobody else ever sees it. You may market to her only if she already agreed to marketing in Shopify.',
      'No IP addresses, ever. Your privacy policy gets updated words (you paste them).'
    ]
  },
  {
    id: 'up-start', t: 'Start a new Claude session with the ready brief', min: '5 min',
    why: 'The brief has every path, rule and decision, so the new session doesn\'t break anything.',
    steps: [
      'Do this after the talks are live (section 3).',
      'Claude app → <b>Code</b> → <b>New session</b> → folder <code>C:\\Users\\SSTS\\Desktop\\Riya</code>.',
      'Model <b>Opus</b>, effort <b>xhigh</b>.',
      'Paste the brief below and send.',
      'It will write a plan first and ask the orchestrator. Say yes only after you\'ve read the consent wording.'
    ],
    prompt: { label: 'Copy the full brief', text: TALKS_PROMPT }
  },
  {
    id: 'up-approve', t: 'Approve the plan (and paste the new privacy words)', min: '10 min',
    why: 'You decide what is collected and what it costs. Nothing goes live without your yes.',
    steps: ['Read the plan\'s "consent text" and "costs" parts.', 'If an email or WhatsApp provider needs a key, you paste it into Vercel yourself (like the talks keys).', 'When it\'s built, paste the new privacy paragraph into <b>Settings → Policies → Privacy policy</b>.'],
    links: [['Settings → Policies', A + '/settings/legal']]
  }
  ]
},
{
  id: 's10', set: 'wild-card', icon: '📸', title: 'Instagram carousels in the brand voice',
  sub: 'Hinglish moments. Nails as punctuation. No speeches.',
  tasks: [
  {
    id: 'ig-voice', t: 'Learn the voice in 2 minutes', min: '2 min',
    why: 'If every post sounds like the site, people remember you.',
    html: 'voice',
    steps: [
      'Each set is a <b>moment</b>, not a product feature. She picks up the bill. She hands over a safety pin. The nails are just there, doing the talking.',
      'Write like a friend texts: short, specific, a bit funny. Hindi in Roman script.',
      'Never: "queen", "boss babe", "you deserve this", fake reviews, "bestseller", college or campus, soft-drink brand names, "Cherry Repeat", or "mera idea tha".',
      'Copy each headline exactly (table below).'
    ]
  },
  {
    id: 'ig-setup', t: 'Set up one ChatGPT chat for carousels', min: '5 min',
    why: 'One chat that already knows your voice and nails = consistent posts.',
    steps: [
      'Open ChatGPT → new chat. Name it "Small Talk carousels".',
      'Attach the nail reference images from <code>artwork\\chatgpt-refs\\&lt;set&gt;\\4-exact-nail-designs.png</code> and <code>artwork\\chatgpt-refs\\_shared\\character-sheet.png</code>.',
      'Paste the master prompt below. Wait for "ready".'
    ],
    prompt: { label: 'Copy carousel master prompt', text: CAROUSEL_MASTER },
    links: [['ChatGPT', 'https://chatgpt.com/']]
  },
  {
    id: 'ig-ideas', t: 'Pick an idea and generate it', min: '30 min per post',
    why: 'Eight ready ideas, one per week = two months of posts.',
    html: 'carousels',
    steps: [
      'Tap an idea\'s copy button and paste it into your carousel chat.',
      'Generate each slide image with its image prompt, one slide per message. Check every nail against the table. Wrong? Reply "Fix the nails only: &lt;correct design&gt;. Change nothing else."',
      'Put the text on in Canva or Instagram\'s Edits app (AI often misspells Hinglish). Size 1080 × 1350 (4:5).',
      'Post with the caption. Add a UTM link to your bio or story (section 7).'
    ]
  },
  {
    id: 'ig-rhythm', t: 'Keep a simple posting rhythm', min: '5 min',
    why: 'Steady beats perfect.',
    steps: ['2 carousels a week + stories on the other days.', 'Reply to every comment in the first hour.', 'Every 2 weeks, check Instagram Insights: which post got the most saves and shares? Make more like that.', 'Only real customer photos and words, with their permission. Never invent reviews.']
  }
  ]
}
];
