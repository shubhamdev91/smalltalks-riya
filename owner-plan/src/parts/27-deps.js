/* ---------- dependencies (owner, 10 Oct) ---------- */
/* needs: task ids (Riya's or Our list) or 'ext:<key>' for events outside Riya's plan */
const NEEDS = {
  'pay': [], 'f-confirm': [], 'g-preview': [], 't-email': [], 'g-privacy': [], 'm-biz': [], 'ig-profile': [],
  'e-discount': [], 'r-links': [], 'ig-setup': [], 'v-start': [], 'v-example': [], 'seo-basics': [], 'e-wa': [],
  'f-photos': [], 'g-domain': [], 'u-build': [],
  'g-test': ['pay'],
  'g-publish': ['g-preview', 'g-test', 'f-confirm'],
  't-vercel': ['t-email'],
  'm-ig': ['m-biz'],
  'm-app': ['m-biz', 'm-ig'],
  'm-events': ['m-app', 'g-publish'],
  'g-app': ['g-publish'],
  'g-gsc': ['g-publish'],
  'ig-mix': ['ig-profile'],
  'e-email': ['e-discount', 'ext:forms'],
  't-moderate': ['ext:talks-open'],
  'ig-batch': ['ig-mix'],
  'ig-ideas': ['ig-setup'],
  'v-sheet-script': ['v-start'],
  'v-board-shots': ['v-sheet-script'],
  'v-motion-post': ['v-board-shots'],
  'ig-cal': ['ig-mix'],
  'ig-review': ['ig-batch'],
  'seo-find': ['seo-basics'],
  'seo-meta': ['seo-basics'],
  'seo-journal': ['seo-find'],
  'g-analytics': ['g-publish'],
  'a-start': ['m-events'],
  'a-camp': ['a-start', 'ig-setup', 'pay'],
  'a-weekly': ['a-camp'],
  'seo-mentions': ['g-publish', 'ig-profile'],
  'seo-gsc': ['g-gsc'],
  /* Our list */
  'up-start': ['ext:talks-open']
};
/* time-based waits: [prerequisite, days after it was ticked] */
const WAITS = { 'a-start': ['m-events', 14], 'seo-gsc': ['g-gsc', 28] };
/* outside events: cleared when the matching Our-list task is ticked or marked Done */
const EXT = {
  'talks-open': { label: 'talks posting is open', our: 'x-talks-open' },
  'forms': { label: 'the signup form is live (Our list)', our: 'e-forms' }
};
/* Our-list item that represents "talks posting is open" */
(function () {
  const o2 = OUR.find(s => s.id === 'o2');
  if (o2 && !o2.tasks.some(t => t.id === 'x-talks-open')) {
    o2.tasks.splice(o2.tasks.findIndex(t => t.id === 't-privacy'), 0, {
      id: 'x-talks-open', who: 'Claude', status: 'Waiting', t: 'Talks posting is open on the live store', min: '—',
      why: 'Riya\'s daily talks check and the talks upgrades start the day posting opens.',
      steps: ['st-talks runs its posting-ON window (HD avatars, posting on, real end-to-end test, test posts deleted).', 'Tick this when shoppers can post on the live store.']
    });
  }
})();
