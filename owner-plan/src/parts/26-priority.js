/* ---------- priority tiers (owner, 10 Oct) ---------- */
const TIERS = [
  { key: 'P1', label: 'P1 · now', blurb: 'Blocks selling or launch. Do these before anything else.' },
  { key: 'P2', label: 'P2 · this week', blurb: 'Switch on measurement before any traffic, plus first-sale basics.' },
  { key: 'P3', label: 'P3 · weeks 2–4', blurb: 'Build your content and search engine.' },
  { key: 'P4', label: 'P4 · later', blurb: 'Month 2+, once there is traffic and data.' }
];
const PRIORITY = [
  ['P1', 'pay', 'Checkout is blocked until a payment provider is active.'],
  ['P1', 'f-confirm', 'Wrong kit facts mean returns and lost trust from the first order.'],
  ['P1', 'g-preview', 'Catch anything broken before real shoppers see it.'],
  ['P1', 'g-test', 'Proves bag → checkout → payment → email works end to end.'],
  ['P1', 'g-publish', 'Makes the newest store live; everything after builds on it.'],
  ['P1', 't-email', 'Talks setup step (done 10 Oct).'],
  ['P1', 't-vercel', 'Talks setup step (done 10 Oct).'],
  ['P2', 'g-privacy', 'Cookie banner first, so every pixel respects consent from day one.'],
  ['P2', 'm-biz', 'Meta ads, Page, Instagram and pixel all live in the portfolio.'],
  ['P2', 'm-ig', 'Needed for Insights, ads and linking Instagram to the portfolio.'],
  ['P2', 'm-app', 'Starts the pixel + Conversions API so audiences build before any ads.'],
  ['P2', 'm-events', 'Confirms Meta actually receives visits, carts and purchases.'],
  ['P2', 'g-app', 'Starts GA4 and free Google listings for your seven sets.'],
  ['P2', 'g-gsc', 'Tells Google your pages exist; data starts collecting now.'],
  ['P2', 'ig-profile', 'Visitors from every post land on your profile first.'],
  ['P2', 'ig-mix', 'Sets your posting rhythm (start at 1 a day).'],
  ['P2', 'u-build', 'Label links before you share any, or you can\'t tell what sold.'],
  ['P2', 'e-discount', 'The welcome offer your signup form and email point to.'],
  ['P2', 'e-email', 'Every new subscriber gets a hello automatically.'],
  ['P2', 't-moderate', 'Optional: posts publish on their own; this is only an occasional look at reports.'],
  ['P2', 'r-links', 'Bookmark your tools once, so you can find them all month.'],
  ['P3', 'ig-batch', 'One making-day a week keeps quality up and weekdays free.'],
  ['P3', 'ig-setup', 'A carousel chat that already knows your voice and nails.'],
  ['P3', 'ig-ideas', 'Eight ready ideas = two months of carousels.'],
  ['P3', 'v-start', 'Pick one image tool, one video tool, one editor.'],
  ['P3', 'v-sheet-script', 'The character sheet keeps her the same in every shot.'],
  ['P3', 'v-board-shots', 'Fix stills before paying for video.'],
  ['P3', 'v-motion-post', 'Turns the stills into a finished Reel.'],
  ['P3', 'v-example', 'A full worked Reel to copy for your first video.'],
  ['P3', 'ig-cal', 'Plans the whole month so batch day is just "make".'],
  ['P3', 'ig-review', 'Do more of what works, every week.'],
  ['P3', 'seo-basics', 'Two minutes to understand SEO and AEO.'],
  ['P3', 'seo-find', 'Builds the list of real searches everything else uses.'],
  ['P3', 'seo-meta', 'Every new product, post or image needs its own listing.'],
  ['P3', 'seo-journal', 'One answer page a month slowly brings free visitors.'],
  ['P3', 'e-wa', 'WhatsApp reaches people in India better than email, with consent.'],
  ['P3', 'g-analytics', 'Five numbers that tell you if the store is working.'],
  ['P3', 'f-photos', 'Real photos build trust once the basics run.'],
  ['P4', 'a-start', 'Audiences need 2–4 weeks of pixel data and some traffic first.'],
  ['P4', 'a-camp', 'Spend only once audiences have people in them.'],
  ['P4', 'a-weekly', 'Starts with your first campaign.'],
  ['P4', 'seo-mentions', 'Outreach works better once you have posts to point to.'],
  ['P4', 'seo-gsc', 'Needs about 4 weeks of Search Console data.'],
  ['P4', 'g-domain', 'Nice to have; best decided before you scale ads.']
];
const HABITS = ['ig-batch', 'ig-cal', 'ig-review', 'seo-meta', 'seo-journal', 'seo-gsc', 'a-weekly'];
const TIER_OF = {}, PWHY = {};
PRIORITY.forEach(([tier, id, why]) => { TIER_OF[id] = tier; PWHY[id] = why; });
/* habits are ticked once she has started them */
RIYA.forEach(s => s.tasks.forEach(t => { if (HABITS.includes(t.id)) t.habit = true; }));
/* talks setup and checkout consent: done 10 Oct (owner/parent verified) */
OUR.forEach(s => s.tasks.forEach(t => {
  if (['t-app', 't-version', 't-install', 't-publish', 't-tell', 'e-checkout'].includes(t.id)) t.status = 'Done ✓ 10 Oct';
}));
