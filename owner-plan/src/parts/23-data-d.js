/* ---------- plan data: sections 11-12 ---------- */
const CHAR_ON_ME = `ON ME WOMAN (paste this block into every prompt for her): an Indian woman in her early twenties, natural medium-brown skin, dense curly black hair falling past her shoulders, winged black eyeliner, a small red bindi, gold hoop earrings, a plain red top. Calm, confident, a little amused. Her nails: long glossy almond press-ons; from thumb to little finger: burgundy, amber tortoiseshell, metallic gold, amber tortoiseshell, burgundy (same pattern on both hands). Gold rings on two fingers. Hands always have exactly five fingers with natural joints.`;

const STYLE_BLOCK = `STYLE: bold comic-ink Indian pop illustration, thick confident black ink outlines, flat saturated colour with soft cel shading, glossy highlights; warm evening café palette with mustard #FFB900, burgundy and amber accents. Vertical 9:16 frame. No text, no logos, no watermark, no brand names on any object.`;

const VIDEO_PROMPTS = {
  sheet: `Make a CHARACTER SHEET for an animated short. ${STYLE_BLOCK}
${CHAR_ON_ME}
Layout on one plain off-white sheet: (1) front view head and shoulders, (2) three-quarter view, (3) side profile, (4) full body standing, (5) close-up of her right hand from the back showing all five nails in order, (6) close-up of her hand holding a small restaurant bill folder. Same face, hair, outfit and nails in every panel. Label nothing.`,
  script: `You are a short-video scriptwriter for my press-on nail brand Small Talk.
${'${VOICE}'}
Write a 12–15 second vertical Reel script for the set I name. Structure: 5–6 shots, each 2–3 seconds. First 1 second must hook. The hand moment is the turn. Dialogue optional and at most one line (the headline). On-screen text per shot, max 5 words, Hinglish in Roman script. End card: packaging + "Shop [set] — link in bio". Output a table: shot no., seconds, what we see, camera, on-screen text, sound.
Set: [NAME THE SET]`,
  board: `Turn this script into a storyboard shot list for AI video. For each shot give: (1) a STILL IMAGE prompt that starts with the character block and style block I paste below and describes framing, pose, props, light and where the nails must be clearly visible; (2) an IMAGE-TO-VIDEO prompt of max 40 words: one simple action, one camera move, 4–5 seconds, "keep the face, hair, outfit and nails exactly as in the image, hands keep five fingers". Avoid fast hand movement and finger close-ups in motion (AI warps fingers). Prefer: slow push-in, slight parallax, hair and light moving.
CHARACTER BLOCK: [paste]
STYLE BLOCK: [paste]
SCRIPT: [paste]`,
  shot: `Attach: the character sheet image + 4-exact-nail-designs.png for this set.
Use the attached character sheet as the exact reference for her face, hair, outfit and nails. Do not change them.
${STYLE_BLOCK}
${CHAR_ON_ME}
SHOT: [describe the shot from your storyboard]
Check before you finish: five fingers per hand, nail order thumb → little finger = burgundy, tortoiseshell, gold, tortoiseshell, burgundy.`,
  i2v: `[Upload the shot image as the first frame / start image]
Slow push-in. [ONE action, e.g. "her hand slides the bill folder towards herself across the table"]. Warm café lights twinkle softly in the background. Keep her face, hair, outfit and nails exactly as in the image; hands keep five fingers. 5 seconds, 9:16, no text, no new people.`,
  caption: `Write an Instagram Reel caption (max 50 words, ends with a question) and 6 hashtags for this Small Talk Reel. Voice rules: warm, witty Hinglish in Roman script, no hype, no fake reviews, no "queen". Reel: [paste your shot list]. Also write alt text (one sentence) and a 1-line cover text (max 4 words).`
};

const VIDEO_EXAMPLE_HTML = `<div class="mini-tbl"><table>
<thead><tr><th>#</th><th>Sec</th><th>We see</th><th>On-screen text</th><th>Image-to-video action</th></tr></thead>
<tbody>
<tr><td>1</td><td>0–2</td><td>Wide: café table at night, three friends laughing, fairy lights, empty plates.</td><td>Dinner ran long.</td><td>Slow push-in, lights twinkle, friends laugh.</td></tr>
<tr><td>2</td><td>2–4</td><td>Top-down: a waiter's hand sets a dark bill folder in the middle of the table.</td><td>Then the bill came.</td><td>Folder lands, slight camera settle.</td></tr>
<tr><td>3</td><td>4–6</td><td>Medium: two friends suddenly very busy with their phones, eyebrows up.</td><td>Sab busy. 👀</td><td>Friends glance at each other, small head turns.</td></tr>
<tr><td>4</td><td>6–9</td><td>Close-up: HER hand enters from the right and draws the bill folder towards her. Nails sharp: burgundy · tortoiseshell · gold · tortoiseshell · burgundy.</td><td><b>Bill idhar.</b></td><td>Slow slide of the folder only, hand stays steady, gentle push-in.</td></tr>
<tr><td>5</td><td>9–11</td><td>Half-face: her eyes glance sideways, calm small smile, gold hoop catches light.</td><td>I've got this.</td><td>Tiny smile, hair moves slightly, light flicker.</td></tr>
<tr><td>6</td><td>11–14</td><td>End card: the real On Me box on mustard #FFB900 (use the approved packaging image, don't generate it).</td><td>On Me · press-on nails<br>Shop On Me — link in bio</td><td>No AI: still image with a slow zoom in your editor.</td></tr>
</tbody></table></div>
<p class="small">Music: a light, upbeat track from Instagram's own music library, added inside Instagram so it's licensed. Total ≈14 s.</p>`;

const SECTIONS_D = [
{
  id: 's11', set: 'green-flag', icon: '🎬', title: 'AI videos with your characters',
  sub: 'Same women, same nails, shot after shot.',
  tasks: [
  {
    id: 'v-flow', t: 'See the whole workflow', min: '3 min',
    why: 'Six stages. Doing them in order is what keeps the women and nails consistent.',
    steps: [
      '<b>Character sheet</b>: one image of her from all sides + her hands. This is your "actor".',
      '<b>Script</b>: 12–15 seconds, 5–6 shots, one moment.',
      '<b>Storyboard</b>: a still-image prompt and a motion prompt per shot.',
      '<b>Shot images</b>: make each shot as a still, with the sheet attached. Fix nails before moving on.',
      '<b>Image-to-video</b>: animate each still for 4–5 seconds. Simple moves only.',
      '<b>Edit</b>: cut shots together, add your text and Instagram music, export 9:16, post with an AI label.'
    ]
  },
  {
    id: 'v-tools', t: 'Pick your tools', min: '10 min',
    why: 'You don\'t need all of them. One image tool + one video tool + one editor.',
    html: 'tools',
    steps: ['Start with what you already pay for (ChatGPT or Google AI). Add one video tool only when you\'re ready to make Reels every week.', 'Try free credits before paying. Prices change often, so check the page before you buy.']
  },
  {
    id: 'v-sheet', t: 'Make the character sheet', min: '20 min',
    why: 'Every later image copies this, so get it right once.',
    steps: ['New ChatGPT (or Gemini) chat per character. Attach <code>artwork\\chatgpt-refs\\on-me\\3-same-woman-reference.png</code> and <code>4-exact-nail-designs.png</code>.', 'Paste the prompt. Regenerate until the face and nails are right.', 'Download the original PNG. Save as <code>video\\on-me\\character-sheet.png</code>.'],
    prompts: [{ label: 'Character sheet prompt (On Me)', text: VIDEO_PROMPTS.sheet }]
  },
  {
    id: 'v-script', t: 'Write the script', min: '10 min',
    why: 'A 12–15 second story with one hand moment.',
    steps: ['Paste the prompt into Claude or ChatGPT. Fill in the set name.', 'Pick the version where the hand moment hits hardest.'],
    prompts: [{ label: 'Script prompt', text: '' }]
  },
  {
    id: 'v-board', t: 'Turn it into a storyboard', min: '10 min',
    why: 'You get a still prompt and a motion prompt for every shot.',
    steps: ['Paste the prompt, then your character block, style block and script.'],
    prompts: [{ label: 'Storyboard prompt', text: VIDEO_PROMPTS.board }, { label: 'Character block (On Me)', text: CHAR_ON_ME }, { label: 'Style block', text: STYLE_BLOCK }]
  },
  {
    id: 'v-shots', t: 'Make each shot as a still image', min: '40 min',
    why: 'Fixing a still is easy. Fixing a video isn\'t.',
    steps: ['One message per shot, sheet attached every time.', 'Check: same face, five fingers, nails in the right order. Wrong? "Fix the nails only: …. Change nothing else."', 'Download originals (not screenshots).'],
    prompts: [{ label: 'Shot image prompt (template)', text: VIDEO_PROMPTS.shot }]
  },
  {
    id: 'v-i2v', t: 'Animate each shot (image-to-video)', min: '1 hour',
    why: 'Short, simple moves look real. Long, busy ones warp hands.',
    steps: ['Upload the still as the start frame, paste the motion prompt, 5 s, 9:16.', 'Make 2–3 takes per shot and keep the best.', 'For the end card, don\'t generate the box: use the approved packaging image with a slow zoom in your editor.'],
    prompts: [{ label: 'Image-to-video prompt (template)', text: VIDEO_PROMPTS.i2v }]
  },
  {
    id: 'v-edit', t: 'Edit, caption, add music, post', min: '40 min',
    why: 'Text and timing make it feel like Small Talk.',
    steps: [
      'Put the clips in order in Instagram Edits or VN (CapCut is blocked in India). Trim each to 2–3 s.',
      'Add the on-screen text in Barlow-style bold caps or a handwritten font. Keep it in the middle 80% of the screen.',
      'Export 1080 × 1920. Post as a Reel and add music from Instagram\'s library.',
      'Turn on Instagram\'s <b>AI label</b> for AI-made video. Never call it real footage of the product.',
      'Write the caption with the prompt. Add a UTM link in your bio (section 7).'
    ],
    prompts: [{ label: 'Caption prompt', text: VIDEO_PROMPTS.caption }]
  },
  {
    id: 'v-example', t: 'Worked example: "Bill idhar." (On Me)', min: 'read 5 min',
    why: 'A full Reel from script to prompts, ready to make.',
    html: 'video-example',
    steps: ['Make the On Me character sheet first.', 'Use the shot table below with the Shot image template (paste the "We see" column as SHOT).', 'Animate shots 1–5 with the "Image-to-video action" column. Shot 6 is the real packaging, no AI.'],
    prompts: [
      { label: 'Shot 4 image prompt (the hero shot)', text: VIDEO_PROMPTS.shot.replace('[describe the shot from your storyboard]', 'Close-up, eye level with the café table at night. Her right hand enters from the right edge and rests two fingers on a dark leather restaurant bill folder in the middle of the table, about to draw it towards herself. The back of her hand faces the camera so all five nails are sharp and fully visible. Warm fairy-light bokeh behind, a half-empty glass and plates softly blurred. Her face is out of frame.') },
      { label: 'Shot 4 image-to-video prompt', text: 'Start frame = the shot 4 image. Her hand slowly draws the bill folder towards herself across the table, steady and unhurried. Gentle push-in toward the hand. Fairy lights twinkle in the background. Keep her hand, rings and nails exactly as in the image; five fingers; no new hands enter. 5 seconds, 9:16, no text.' }
    ]
  }
  ]
},
{
  id: 's12', set: 'pinky-promise', icon: '📚', title: 'Resources',
  sub: 'Every link in one place.',
  tasks: [
  {
    id: 'r-links', t: 'Bookmark these', min: '2 min',
    why: 'When you\'re stuck, start here.',
    steps: ['Tap any link. Shopify admin links open after you log in.'],
    links: [
      ['Store preview (Claude build)', PREVIEW],
      ['Shopify admin', A],
      ['Online Store → Themes', A + '/themes'],
      ['Shopify Help Center', 'https://help.shopify.com/en'], ['Shopify dev: app proxies', 'https://shopify.dev/docs/apps/build/online-store/app-proxies'],
      ['Shopify Support', 'https://help.shopify.com/en/support'],
      ['Shopify App Store', 'https://apps.shopify.com/'],
      ['Talks backend status', BACKEND + '/api/talks'],
      ['v0 chat (talks backend)', 'https://v0.app/chat/pEcbsIUvnGe'],
      ['Vercel', 'https://vercel.com/'],
      ['GitHub repository','https://github.com/shubhamdev91/smalltalks-riya'],
      ['Meta Business Suite', 'https://business.facebook.com/'],
      ['Meta Events Manager', 'https://business.facebook.com/events_manager'],
      ['Meta Ads Manager', 'https://adsmanager.facebook.com/'],
      ['Meta Blueprint (free ad courses)', 'https://www.facebook.com/business/learn'], ['Blueprint course catalog', 'https://www.facebookblueprint.com/student/catalog'],
      ['Google Analytics', 'https://analytics.google.com/'],
      ['Google Search Console', 'https://search.google.com/search-console'],
      ['Google Merchant Center', 'https://merchants.google.com/'],
      ['Google Skillshop (free courses)', 'https://skillshop.withgoogle.com/'],
      ['GA4 help', 'https://support.google.com/analytics/'],
      ['Search Console help', 'https://support.google.com/webmasters/'],
      ['Campaign URL Builder', 'https://ga-dev-tools.google/ga4/campaign-url-builder/'],
      ['ChatGPT', 'https://chatgpt.com/']
    ],
    note: 'Project folder on the laptop: <code>C:\\Users\\SSTS\\Desktop\\Riya</code>.'
  }
  ]
}
];

/* fill prompts that need the voice block */
(function () {
  const adTask = SECTIONS_B.find(s => s.id === 's6').tasks.find(t => t.id === 'a-copy');
  adTask.prompt.text = AD_COPY_PROMPT.replace('${VOICE}', VOICE_RULES);
  const scr = SECTIONS_D[0].tasks.find(t => t.id === 'v-script');
  scr.prompts[0].text = VIDEO_PROMPTS.script.replace('${VOICE}', VOICE_RULES);
})();
