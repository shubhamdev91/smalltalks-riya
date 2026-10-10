/* ---------- video tools (checked 10 Oct 2026; prices change, check before paying) ---------- */
const TOOLS = [
  ['ChatGPT Images', 'https://chatgpt.com/', 'Character sheet + still shots', 'Works in India. Go ≈ ₹399/mo, Plus ≈ ₹1,999/mo (third-party figures, check in app)', 'Attach your reference image every time; paid "Thinking" mode can make up to 8 images of the same character'],
  ['Google Flow + Gemini', 'https://flow.google.com/', 'Stills and image-to-video', 'Google AI Plus ₹399/mo (200 Flow credits) · AI Pro ₹1,950/mo (1,000 credits + limited Veo trial) — official India prices', 'Reference images ("Ingredients to video", up to 3). Feature names change often; check in the app'],
  ['Kling AI', 'https://kling.ai/', 'Image-to-video, good with people', 'Web app, works in India. Roughly US$7–37/mo (third-party figures)', 'Multi-image reference and multi-shot (names unconfirmed)'],
  ['Runway', 'https://runway.com/pricing', 'Image-to-video and fixes', 'Free 125 credits once · Standard US$15/mo · Pro US$35/mo (official)', 'Gen-4 References, up to 3 images (third-party description)'],
  ['Hailuo (MiniMax)', 'https://hailuoai.video/', 'Cheaper image-to-video to try', 'About US$10/mo (unconfirmed)', 'Subject reference (unconfirmed)'],
  ['Instagram Edits', 'https://edits.instagram.com/', 'Editing, captions, posting Reels', 'Free (phone app)', 'Use with Instagram\'s music library'],
  ['VN Video Editor', 'https://www.vlognow.me/', 'Editing on phone', 'Free, no watermark', '—'],
  ['Canva', 'https://www.canva.com/video-editor/', 'Text on carousels and video', 'Free tier; Pro price varies, check canva.com', 'Brand fonts and colours in one place']
];
const TOOLS_HTML = `<div class="mini-tbl"><table><thead><tr><th>Tool</th><th>Use it for</th><th>Cost / India</th><th>Keeping her the same</th></tr></thead><tbody>${
  TOOLS.map(([n, u, use, cost, cons]) => `<tr><td><a href="${u}" target="_blank" rel="noopener">${n}</a></td><td>${use}</td><td>${cost}</td><td>${cons}</td></tr>`).join('')
}</tbody></table></div>
<div class="callout note"><b>SKIP ·</b> <b>Sora</b> (OpenAI closed the app in April 2026) and <b>CapCut</b> (still blocked in India since 2020; don't use workarounds).</div>
<div class="callout note"><b>STARTER KIT ·</b> ChatGPT or Gemini for stills + Kling or Google Flow for motion + Edits for editing. Roughly ₹2,000–3,500 a month once you post weekly.</div>`;
