/* ---------- app ---------- */
const SECTIONS = RIYA;
const ALL_TASKS = [];
SECTIONS.forEach((s, si) => s.tasks.forEach(t => ALL_TASKS.push({ ...t, sec: s, si })));
const OUR_TASKS = [];
OUR.forEach((s, si) => s.tasks.forEach(t => OUR_TASKS.push({ ...t, sec: s, si })));
const isFlow = t => !t.optional;
const RANKED = PRIORITY.map(([tier, id]) => ALL_TASKS.find(t => t.id === id)).filter(Boolean);
ALL_TASKS.forEach(t => { if (!TIER_OF[t.id]) { console.warn('no tier for', t.id); RANKED.push(t); } });
/* ---------- dependencies ---------- */
const findTask = id => ALL_TASKS.find(t => t.id === id) || OUR_TASKS.find(t => t.id === id);
const isMet = id => { if (done[id]) return true; const t = OUR_TASKS.find(x => x.id === id); return !!(t && /^Done/.test(t.status || '')); };
const fmtDate = ms => new Date(ms).toLocaleDateString('en-IN', { day: 'numeric', month: 'short' });
function blockers(t) {
  const out = [];
  (NEEDS[t.id] || []).forEach(n => {
    if (n.startsWith('ext:')) { const e = EXT[n.slice(4)]; if (e && !isMet(e.our)) out.push({ kind: 'ext', label: e.label, id: e.our }); }
    else if (!isMet(n)) { const d = findTask(n); out.push({ kind: 'task', id: n, label: d ? d.t : n }); }
  });
  const w = WAITS[t.id];
  if (w) {
    const [dep, days] = w;
    const when = Date.parse(done[dep] || '');
    if (!isNaN(when)) { const ready = when + days * 864e5; if (Date.now() < ready) out.push({ kind: 'time', ready }); }
    else if (!out.some(b => b.id === dep)) { const d = findTask(dep); out.push({ kind: 'task', id: dep, label: d ? d.t : dep }); }
  }
  return out;
}
const isReady = t => blockers(t).length === 0;
function waitHtml(t) {
  if (done[t.id]) return '';
  const b = blockers(t);
  if (!b.length) return '';
  const parts = b.map(x => x.kind === 'time' ? `ready from ${fmtDate(x.ready)}`
    : `<a href="#task-${x.id}" data-jump="${x.id}">${esc(x.label)}</a>`);
  const w = WAITS[t.id];
  const extra = w && !b.some(x => x.kind === 'time') ? ` (then ${w[1]} days after it\'s ticked)` : '';
  if (b.every(x => x.kind === 'time')) return `⏳ ${parts.join(', ')} (needs time for data to build up)`;
  return `⏳ waiting on: ${parts.join(', ')}${extra}`;
}
/* priority order, made dependency-safe (prerequisites listed before what needs them) */
const TOPO = [], PLACED = {}, SHOWN_TIER = {}, NEEDED_FOR = {};
function place(t, tier, forT) {
  if (!t || PLACED[t.id]) return;
  PLACED[t.id] = 'visiting';
  (NEEDS[t.id] || []).forEach(n => { const d = ALL_TASKS.find(x => x.id === n); if (d && !PLACED[d.id]) place(d, tier, t); });
  PLACED[t.id] = true;
  SHOWN_TIER[t.id] = tier;
  if (forT) NEEDED_FOR[t.id] = forT.t;
  TOPO.push(t);
}
RANKED.forEach(t => place(t, TIER_OF[t.id] || 'P4', null));
const tierLabel = k => (TIERS.find(x => x.key === k) || {}).label || k;
const LS_KEY = 'st-plan-done-v1';
const LS_OPEN = 'st-plan-open-v1';
let done = {};
let mode = 'local';   // 'local' | 'db' | 'readonly'
let docRef = null;
let writeChain = Promise.resolve();
const copyTexts = [];

function lsGet(k, d) { try { const v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } }
function lsSet(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
function esc(s) { return String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c])); }
function reg(text) { copyTexts.push(text); return copyTexts.length - 1; }
function setVars(s) { return `--set: var(--${s.set}); --set-ink: var(--${s.set}-ink);`; }

done = lsGet(LS_KEY, {});

/* ---------- copy ---------- */
async function doCopy(text, btn) {
  let ok = false;
  try { await navigator.clipboard.writeText(text); ok = true; } catch (e) {
    const ta = document.createElement('textarea');
    ta.value = text; ta.setAttribute('readonly', ''); ta.style.position = 'fixed'; ta.style.opacity = '0';
    document.body.appendChild(ta); ta.select();
    try { ok = document.execCommand('copy'); } catch (e2) { ok = false; }
    ta.remove();
  }
  if (btn) {
    const old = btn.dataset.label || btn.textContent;
    btn.dataset.label = old;
    btn.textContent = ok ? (btn.classList.contains('sos-mini') ? '✓' : 'Copied ✓') : 'Select & copy';
    btn.classList.toggle('done', ok);
    setTimeout(() => { btn.textContent = old; btn.classList.remove('done'); }, 1800);
  }
  if (ok && btn && btn.matches('.sos-mini, .btn-sos')) toast('Copied ✓ Paste it into ChatGPT or Claude.');
  if (!ok) toast('Copy blocked here. Long-press the text to copy.');
}
document.addEventListener('click', e => {
  const b = e.target.closest('[data-copy]');
  if (b) { doCopy(copyTexts[+b.dataset.copy], b); return; }
  const f = e.target.closest('[data-copy-from]');
  if (f) { doCopy(document.getElementById(f.dataset.copyFrom).textContent, f); }
});

function toast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg; t.classList.add('show');
  clearTimeout(toast._t); toast._t = setTimeout(() => t.classList.remove('show'), 2400);
}

/* ---------- special blocks ---------- */
function specialHtml(kind) {
  if (kind === 'voice') {
    return `<div class="mini-tbl"><table><thead><tr><th>Set</th><th>Headline</th><th>Note</th><th>The moment</th></tr></thead><tbody>${
      SETS.map(s => `<tr><td><span class="dot" style="background:${s.colour}"></span>${esc(s.name)}</td><td><b>${esc(s.line)}</b></td><td>${esc(s.note)}</td><td>${esc(s.moment)}</td></tr>`).join('')
    }</tbody></table></div>
    <div class="mini-tbl"><table><thead><tr><th>Set</th><th>Five-nail hand, thumb → little finger (check every image)</th></tr></thead><tbody>${
      SETS.map(s => `<tr><td><span class="dot" style="background:${s.colour}"></span>${esc(s.name)}</td><td>${esc(s.nails)}</td></tr>`).join('')
    }</tbody></table></div>`;
  }
  if (kind === 'carousels') {
    return `<div class="ideas">${CAROUSELS.map(([h, p], i) => `<div class="idea"><h4>${i + 1}. ${esc(h)}</h4><p>${esc(p)}</p><div><button class="btn btn-copy" type="button" data-copy="${reg('Carousel request: "' + h + '". ' + p + ' Follow the FORMAT from my first message exactly, and check the nails against the set list.')}">Copy idea prompt</button></div></div>`).join('')}</div>`;
  }
  if (kind === 'utm') return utmHtml();
  if (kind === 'igmix') return `<div class="mini-tbl"><table><thead><tr><th>Stage</th><th>Posts a week</th><th>Reels</th><th>Carousels</th><th>Single posts</th><th>Stories</th></tr></thead><tbody>
    <tr><td>1 · weeks 1–2 (1 a day)</td><td>7</td><td>3 (1 AI reel)</td><td>2</td><td>2</td><td>3–5 a day</td></tr>
    <tr><td>2 · weeks 3–4 (2 a day)</td><td>14</td><td>7 (1–2 AI reels)</td><td>4</td><td>3</td><td>3–5 a day</td></tr>
    <tr><td>3 · week 5+ (2–3 a day)</td><td>~18</td><td>9 (2 AI reels)</td><td>5</td><td>4</td><td>3–5 a day</td></tr>
  </tbody></table></div>`;
  if (kind === 'video-example') return VIDEO_EXAMPLE_HTML;
  if (kind === 'tools') return TOOLS_HTML;
  return '';
}

/* ---------- render ---------- */
function hasPrompt(t) { return !!(t.prompt && t.prompt.text) || !!(t.prompts && t.prompts.length) || t.html === 'carousels'; }
function chipsHtml(t) {
  const c = [];
  if (!t.who && TIER_OF[t.id]) c.push(`<span class="tchip tier t${TIER_OF[t.id]}">${TIER_OF[t.id]}</span>`);
  if (t.who) c.push(`<span class="tchip who-${t.who.toLowerCase()}">${t.who === 'Claude' ? '🤖' : '🧑'} ${esc(t.who)}</span>`);
  if (t.status) c.push(`<span class="tchip status${t.status === 'In progress' ? ' wip' : ''}${/^Done/.test(t.status) ? ' ok' : ''}">${t.status === 'In progress' ? '⏳ ' : ''}${esc(t.status)}</span>`);
  if (!t.who && hasPrompt(t)) c.push('<span class="tchip prompt">✨ Prompt inside</span>');
  if (t.lock) c.push('<span class="tchip lock">🔒 Only you</span>');
  if (t.habit) c.push('<span class="tchip habit">🔁 Habit</span>');
  if (t.optional) c.push('<span class="tchip opt">Optional</span>');
  c.push(`<span class="tchip">⏱ ${esc(t.min)}</span>`);
  if (NEEDS[t.id] && NEEDS[t.id].length || WAITS[t.id]) c.push(`<span class="tchip waitchip" id="wchip-${t.id}" hidden>⏳ waiting</span>`);
  return `<span class="tchips">${c.join('')}</span>`;
}
function plain(html) { const d = document.createElement('div'); d.innerHTML = String(html || ''); return d.textContent.replace(/\s+/g, ' ').trim(); }
function sosPrompt(t, s) {
  const steps = (t.steps || []).map((x, i) => `${i + 1}. ${plain(x)}`).join('\n');
  const last = (t.steps || []).length ? plain(t.steps[t.steps.length - 1]) : '';
  const prompts = [];
  if (t.prompt && t.prompt.text) prompts.push(`--- ${t.prompt.label} ---\n${t.prompt.text}`);
  (t.prompts || []).forEach(p => prompts.push(`--- ${p.label} ---\n${p.text}`));
  const links = (t.links || []).map(([l, u]) => `- ${l}: ${u}`).join('\n');
  return `Hi! I'm Riya. I run Small Talk, a premium press-on nail brand from India. I'm a first-year student and new to running a store, so please keep it simple.

MY STORE: Small Talk on Shopify (Basic plan, prices in INR), store address https://0nev20-vn.myshopify.com. Instagram: @smalltalks_com.
THE 7 SETS: ${SETS.map(x => `${x.name} "${x.line}"`).join(', ')}. Audience: 18–24 urban Indian women. Voice: warm, witty Hinglish, no hype, no fake reviews.

I'M STUCK ON THIS TASK: "${t.t}" (from the part of my plan called "${s.title}").
WHY IT MATTERS: ${plain(t.why)}
THE STEPS I WAS GIVEN:
${steps || '(no numbered steps; see below)'}
${t.warn ? `IMPORTANT: ${plain(t.warn)}\n` : ''}${t.note ? `NOTE: ${plain(t.note)}\n` : ''}WHAT "DONE" LOOKS LIKE: ${last ? `I've finished every step above, ending with: ${last}` : 'I\'ve finished the task described above.'}
${links ? `LINKS IN MY PLAN:\n${links}\n` : ''}${prompts.length ? `THE TASK ALSO GIVES ME THIS PROMPT TO USE:\n${prompts.join('\n\n')}\n` : ''}
WHERE I'M STUCK: [describe what you see, paste the error, or attach a screenshot]

Please walk me through this step by step in simple language. Before each step, ask me what I see on my screen and wait for my answer. Give exact buttons to click (as they look in 2026), tell me if a step could affect my live store or cost money, and never ask me for passwords, API keys or secret codes. Tell me where to paste those myself instead.`;
}
function taskHtml(t, s, our) {
  const isDone = !!done[t.id];
  let body = `<p class="why">💡 ${t.why}</p>`;
  const sosId = our ? -1 : reg(sosPrompt(t, s));
  if (!our) body += `<div><button class="btn btn-sos" type="button" data-copy="${sosId}" aria-label="SOS: copy a help prompt for ${esc(t.t)}">SOS 🆘 Stuck? Copy this</button></div>`;
  if (NEEDS[t.id] && NEEDS[t.id].length || WAITS[t.id]) body += `<p class="waitline" id="wait-${t.id}" hidden></p>`;
  if (!our && TIER_OF[t.id]) body += `<p class="pwhy"><b>${esc(tierLabel(TIER_OF[t.id]))}</b> · ${esc(PWHY[t.id])}</p>`;
  if (t.wwg) body += `<dl class="wwg"><div><dt>What it does</dt><dd>${t.wwg[0]}</dd></div><div><dt>Why it matters</dt><dd>${t.wwg[1]}</dd></div><div><dt>What you get</dt><dd>${t.wwg[2]}</dd></div></dl>`;
  if (t.steps && t.steps.length) body += `<ol class="steps">${t.steps.map(x => `<li><span>${x}</span></li>`).join('')}</ol>`;
  if (t.html) body += specialHtml(t.html);
  if (t.copy) body += `<div class="chips">${t.copy.map(([label, text]) => {
    const short = text.length > 60 ? label : text;
    return `<span class="chip"><span>${esc(short)}</span><button type="button" data-copy="${reg(text)}">Copy</button></span>`;
  }).join('')}</div>`;
  if (t.prompt && t.prompt.text) body += `<div class="prompt"><pre class="prompt-box">${esc(t.prompt.text)}</pre><div><button class="btn btn-copy" type="button" data-copy="${reg(t.prompt.text)}">📋 ${esc(t.prompt.label)}</button></div></div>`;
  if (t.prompts) t.prompts.forEach(p => { body += `<div class="prompt"><b class="task-meta">${esc(p.label)}</b><pre class="prompt-box">${esc(p.text)}</pre><div><button class="btn btn-copy" type="button" data-copy="${reg(p.text)}">📋 Copy</button></div></div>`; });
  if (t.warn) body += `<div class="callout warn"><b>CAREFUL ·</b> ${t.warn}</div>`;
  if (t.note) body += `<div class="callout note"><b>NOTE ·</b> ${t.note}</div>`;
  if (t.links) body += `<ul class="links">${t.links.map(([l, u]) => `<li><a href="${esc(u)}" target="_blank" rel="noopener">${esc(l)}</a></li>`).join('')}</ul>`;
  return `<div class="task${isDone ? ' is-done' : ''}${our ? '' : ' has-sos'}" id="task-${t.id}" style="${setVars(s)}">
    <input class="chk" type="checkbox" id="chk-${t.id}" data-task="${t.id}" ${isDone ? 'checked' : ''} aria-label="Done: ${esc(t.t)}">
    <details id="det-${t.id}"><summary><span class="task-title">${esc(t.t)}</span>${chipsHtml(t)}</summary><div class="task-body">${body}</div></details>${our ? '' : `
    <button class="sos-mini" type="button" data-copy="${sosId}" aria-label="SOS: copy a help prompt for ${esc(t.t)}" title="Stuck? Copy a help prompt">🆘</button>`}
  </div>`;
}

function renderSections() {
  copyTexts.length = 0;
  renderList('sections', SECTIONS, 'STEP', false);
  renderList('our-sections', OUR, 'LIST', true);
  bindUtm();
  document.getElementById('start-prompt').textContent = START_PROMPT;
}
function renderList(container, list, label, our) {
  const open = lsGet(LS_OPEN, {});
  document.getElementById(container).innerHTML = list.map((s, i) => {
    const n = s.tasks.filter(t => done[t.id]).length;
    const full = n === s.tasks.length;
    return `<details class="sec" id="sec-${s.id}" style="${setVars(s)}" ${open[s.id] ? 'open' : ''}>
      <summary>
        <span class="sec-ico" aria-hidden="true">${s.icon}</span>
        <span><span class="sec-num">${label} ${i + 1}</span><h2 class="sec-title">${esc(s.title)}</h2><div class="sec-sub">${esc(s.sub)}</div></span>
        <span class="sec-count${full ? ' full' : ''}" id="cnt-${s.id}">${full ? '🎉 ' : ''}${n}/${s.tasks.length}</span>
      </summary>
      <div class="sec-mini"><span id="mini-${s.id}" style="width:${(n / s.tasks.length) * 100}%"></span></div>
      <div class="sec-body">${s.tasks.map(t => taskHtml(t, s, our)).join('')}${s.foot ? `<p class="sec-foot">${esc(s.foot)}</p>` : ''}</div>
    </details>`;
  }).join('');
}

function renderProgress() {
  const total = ALL_TASKS.length;
  const n = ALL_TASKS.filter(t => done[t.id]).length;
  const pct = Math.round((n / total) * 100);
  document.getElementById('pct').textContent = pct + '%';
  document.getElementById('count').textContent = `${n} of ${total} tasks done`;
  const bar = document.getElementById('bar');
  bar.setAttribute('aria-valuenow', pct); bar.firstElementChild.style.width = pct + '%';
  const on = OUR_TASKS.filter(t => done[t.id]).length;
  const op = Math.round((on / OUR_TASKS.length) * 100);
  document.getElementById('our-pct').textContent = op + '%';
  document.getElementById('our-count').textContent = `${on} of ${OUR_TASKS.length} done`;
  const ob = document.getElementById('our-bar');
  ob.setAttribute('aria-valuenow', op); ob.firstElementChild.style.width = op + '%';
  [...SECTIONS, ...OUR].forEach(s => {
    const k = s.tasks.filter(t => done[t.id]).length;
    const full = k === s.tasks.length;
    const c = document.getElementById('cnt-' + s.id);
    if (c) { c.textContent = (full ? '🎉 ' : '') + k + '/' + s.tasks.length; c.classList.toggle('full', full); }
    const m = document.getElementById('mini-' + s.id);
    if (m) m.style.width = (k / s.tasks.length) * 100 + '%';
    s.tasks.forEach(t => {
      const el = document.getElementById('task-' + t.id);
      if (el) { el.classList.toggle('is-done', !!done[t.id]); el.querySelector('.chk').checked = !!done[t.id]; }
    });
  });
  [...ALL_TASKS, ...OUR_TASKS].forEach(t => {
    const line = document.getElementById('wait-' + t.id);
    if (!line) return;
    const w = waitHtml(t);
    line.innerHTML = w; line.hidden = !w;
    const chip = document.getElementById('wchip-' + t.id);
    if (chip) chip.hidden = !w;
    const el = document.getElementById('task-' + t.id);
    if (el) el.classList.toggle('is-blocked', !!w);
  });
  renderNext();
  renderOrder();
}

function renderNext() {
  const next = TOPO.find(t => isFlow(t) && !done[t.id] && isReady(t));
  document.getElementById('stuck-text').textContent = stuckPrompt(next);
  const box = document.getElementById('next');
  if (!next) {
    box.innerHTML = `<div class="next all-done" style="--set: var(--wild-card); --set-ink: var(--wild-card-ink)"><span class="kicker">All done</span><h2>Every task ticked. Achha. Tum pehle. 🎉</h2><p>Now keep posting, keep replying, and check your numbers every week.</p></div>`;
    return;
  }
  const s = next.sec;
  box.innerHTML = `<div class="next" style="${setVars(s)}">
    <span class="kicker">👉 Do this next</span>
    <h2>${esc(next.t)}</h2>
    <div class="row">
      <button class="btn btn-solid" type="button" id="next-open">Show me how</button>
      <button class="btn" type="button" id="next-done">Mark done ✓</button>
    </div>
    <div class="meta" style="margin-top:10px">${esc(tierLabel(TIER_OF[next.id]))} · ${esc(s.title)} · ⏱ ${esc(next.min)}${next.lock ? ' · 🔒 only you' : ''}</div>
    <p>${next.why}</p>
  </div>`;
  document.getElementById('next-open').onclick = () => openTask(next);
  document.getElementById('next-done').onclick = () => setDone(next.id, true);
}

function orderRow(t, n, nextId) {
  const isDone = !!done[t.id];
  const chips = [];
  if (hasPrompt(t)) chips.push('<span class="tchip prompt">✨</span>');
  if (t.lock) chips.push('<span class="tchip lock">🔒</span>');
  if (t.habit) chips.push('<span class="tchip habit">🔁</span>');
  if (t.optional) chips.push('<span class="tchip opt">Optional</span>');
  chips.push(`<span class="tchip">⏱ ${esc(t.min)}</span>`);
  const wait = waitHtml(t);
  const state = isDone ? '✓' : (t.id === nextId ? '← next' : (wait ? '⏳' : ''));
  return `<li><a class="orow${isDone ? ' is-done' : ''}${t.id === nextId ? ' is-next' : ''}${wait ? ' is-blocked' : ''}" href="#task-${t.id}" data-jump="${t.id}" style="${setVars(t.sec)}" aria-label="${n}. ${esc(t.t)}${isDone ? ', done' : ''}${t.id === nextId ? ', your next step' : ''}">
    <span class="onum" aria-hidden="true">${n}</span>
    <span class="otext"><span class="otitle">${esc(t.t)}</span><span class="osec">${esc(t.sec.title)} · ${esc(PWHY[t.id] || '')}</span>${NEEDED_FOR[t.id] ? `<span class="osec"><b>Needed first for:</b> ${esc(NEEDED_FOR[t.id])}</span>` : ''}<span class="tchips">${chips.join('')}</span></span>
    <span class="ostate" aria-hidden="true">${state}</span></a>${wait ? `<p class="owait">${wait}</p>` : ''}</li>`;
}
function renderOrder() {
  const list = document.getElementById('order-list');
  if (!list) return;
  const next = TOPO.find(t => isFlow(t) && !done[t.id] && isReady(t));
  const nextId = next ? next.id : '';
  let n = 0, html = '';
  TIERS.forEach(tr => {
    const arr = TOPO.filter(t => (SHOWN_TIER[t.id] || 'P4') === tr.key);
    if (!arr.length) return;
    const k = arr.filter(t => done[t.id]).length;
    html += `<div class="tier-head"><span class="tchip tier t${tr.key}">${esc(tr.label)}</span><span class="task-meta">${k}/${arr.length} done · ${esc(tr.blurb)}</span></div>`;
    html += `<ol class="olist" start="${n + 1}">${arr.map(t => orderRow(t, ++n, nextId)).join('')}</ol>`;
  });
  list.innerHTML = html;
  document.getElementById('order-n').textContent = `(${ALL_TASKS.length})`;
}
function setOrderOpen(open) {
  const b = document.getElementById('order-toggle');
  b.setAttribute('aria-expanded', open);
  document.getElementById('order-list').hidden = !open;
  lsSet('st-order-open', open);
}
function jumpTo(id) {
  const t = ALL_TASKS.find(x => x.id === id);
  const o = t ? null : OUR_TASKS.find(x => x.id === id);
  if (!t && !o) return false;
  if (o) { showTab('our'); openTask(o); try { history.replaceState(null, '', '#task-' + id); } catch (e) {} return true; }
  showTab('plan');
  openTask(t);
  try { history.replaceState(null, '', '#task-' + id); } catch (e) {}
  return true;
}
function openTask(t) {
  const sec = document.getElementById('sec-' + t.sec.id);
  sec.open = true;
  const det = document.getElementById('det-' + t.id);
  det.open = true;
  const el = document.getElementById('task-' + t.id);
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  el.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
  el.classList.remove('flash'); void el.offsetWidth; el.classList.add('flash');
}

/* ---------- state + sync ---------- */
function setDone(id, val) {
  const before = sectionOf(id);
  const wasFull = before && before.tasks.every(t => done[t.id]);
  const next = { ...done };
  if (val) next[id] = new Date().toISOString(); else delete next[id];
  done = next;
  renderProgress();
  persist();
  if (val) {
    const s = sectionOf(id);
    if (s && !wasFull && s.tasks.every(t => done[t.id])) { confetti(s); toast(`🎉 Done: ${s.title}!`); }
    else toast('Nice. Ticked ✓');
  }
}
function sectionOf(id) { return [...SECTIONS, ...OUR].find(s => s.tasks.some(t => t.id === id)); }

function persist() {
  lsSet(LS_KEY, done);
  if (mode !== 'db' || !docRef) return;
  const snapshot = { done: { ...done }, updatedAt: new Date().toISOString() };
  writeChain = writeChain.then(() => docRef.set(snapshot)).catch(err => {
    if (err && (err.code === 'invalid_argument' || err.code === 'not_granted' || err.code === 'revoked')) {
      mode = 'readonly'; setSync();
    } else if (err && err.code === 'unavailable') {
      setTimeout(() => persist(), 1200 + Math.random() * 800);
    }
  });
}

function setSync() {
  const el = document.getElementById('sync');
  if (mode === 'db') el.innerHTML = '<b>●</b> Ticks saved for you and your brother';
  else if (mode === 'readonly') el.textContent = 'Ticks saved on this phone only (ask for edit access to sync)';
  else el.textContent = 'Ticks saved on this device';
}

async function initDb() {
  setSync();
  if (!window.claude || typeof window.claude.use !== 'function') return;
  let db = null;
  try { db = await window.claude.use('db'); } catch (e) { db = null; }
  if (!db) { setSync(); return; }
  try { docRef = db.doc('progress/plan'); } catch (e) { return; }
  let first = true;
  docRef.onSnapshot(snap => {
    const remote = snap.exists ? ((snap.data() || {}).done || {}) : {};
    if (first) {
      first = false;
      mode = 'db';
      // keep ticks made on this device before sync was available
      const localOnly = Object.keys(done).filter(k => !remote[k]);
      done = { ...remote, ...done };
      if (!snap.exists && localOnly.length === 0) { /* nothing yet */ }
      renderProgress(); setSync();
      return;
    }
    done = { ...remote };
    lsSet(LS_KEY, done);
    renderProgress();
  }, () => { mode = 'local'; setSync(); });
}

/* ---------- confetti ---------- */
function confetti(s) {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const c = document.getElementById('confetti');
  c.hidden = false;
  const ctx = c.getContext('2d');
  const dpr = Math.min(window.devicePixelRatio || 1, 2);
  c.width = innerWidth * dpr; c.height = innerHeight * dpr; ctx.scale(dpr, dpr);
  const cols = ['#ffb900', '#073df1', '#e10019', '#007948', '#ff0078', '#b7ef00', '#6620f2'];
  const ps = Array.from({ length: 140 }, () => ({
    x: innerWidth / 2 + (Math.random() - .5) * 80, y: innerHeight * .35,
    vx: (Math.random() - .5) * 14, vy: -Math.random() * 13 - 4,
    w: 6 + Math.random() * 6, h: 10 + Math.random() * 10, r: Math.random() * 6, vr: (Math.random() - .5) * .4,
    c: cols[(Math.random() * cols.length) | 0]
  }));
  const t0 = performance.now();
  (function frame(t) {
    const el = t - t0;
    ctx.clearRect(0, 0, innerWidth, innerHeight);
    ps.forEach(p => {
      p.vy += .38; p.x += p.vx; p.y += p.vy; p.vx *= .99; p.r += p.vr;
      ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.r); ctx.fillStyle = p.c;
      ctx.beginPath(); ctx.ellipse(0, 0, p.w / 2, p.h / 2, 0, 0, Math.PI * 2); ctx.fill(); ctx.restore();
    });
    if (el < 2200) requestAnimationFrame(frame); else { ctx.clearRect(0, 0, innerWidth, innerHeight); ctx.setTransform(1, 0, 0, 1, 0, 0); c.hidden = true; }
  })(t0);
}

/* ---------- stickers ---------- */
function nailSvg(col, rot) {
  return `<svg class="sticker" viewBox="0 0 30 44" style="transform:rotate(${rot}deg)"><path d="M15 2C7 2 3 14 3 24v12c0 3 3 6 6 6h12c3 0 6-3 6-6V24C27 14 23 2 15 2z" fill="${col}" stroke="#0b0b2e" stroke-width="2"/><path d="M9 10c1-3 3-5 5-5" stroke="#fff" stroke-width="2.4" stroke-linecap="round" fill="none" opacity=".8"/></svg>`;
}

/* ---------- UTM builder ---------- */
function utmHtml() {
  return `<form class="utm" id="utm" onsubmit="return false">
    <label for="u-base">Page link<input id="u-base" type="url" inputmode="url" value="${STORE}/products/bill-idhar"></label>
    <div class="grid2">
      <label for="u-src">Source (where)<select id="u-src"><option>instagram</option><option>facebook</option><option>whatsapp</option><option>google</option><option>youtube</option><option>email</option><option>influencer</option><option>other</option></select></label>
      <label for="u-med">Medium (how)<select id="u-med"><option value="social">social (free post / story / bio)</option><option value="paid_social">paid_social (Meta ads)</option><option value="email">email</option><option value="whatsapp">whatsapp (message)</option><option value="referral">referral (creator / friend)</option><option value="cpc">cpc (Google ads)</option></select></label>
      <label for="u-camp">Campaign (why)<input id="u-camp" type="text" value="launch_oct26" autocomplete="off"></label>
      <label for="u-cont">Content (which one)<input id="u-cont" type="text" value="carousel_bill_idhar" autocomplete="off"></label>
    </div>
    <div class="utm-out" id="u-out" aria-live="polite"></div>
    <div><button class="btn btn-pill" type="button" id="u-copy">📋 Copy link</button></div>
    <div class="utm-recent" id="u-recent"></div>
  </form>`;
}
function slug(v) { return String(v || '').trim().toLowerCase().replace(/[^a-z0-9]+/g, '_').replace(/^_+|_+$/g, ''); }
function buildUtm() {
  const base = (document.getElementById('u-base').value || STORE).trim();
  let u;
  try { u = new URL(base.startsWith('http') ? base : 'https://' + base); } catch (e) { return ''; }
  const p = { utm_source: slug(document.getElementById('u-src').value), utm_medium: slug(document.getElementById('u-med').value), utm_campaign: slug(document.getElementById('u-camp').value), utm_content: slug(document.getElementById('u-cont').value) };
  Object.entries(p).forEach(([k, v]) => { if (v) u.searchParams.set(k, v); else u.searchParams.delete(k); });
  return u.toString();
}
function bindUtm() {
  const f = document.getElementById('utm');
  if (!f) return;
  const saved = lsGet('st-utm-form', null);
  if (saved) ['u-base', 'u-src', 'u-med', 'u-camp', 'u-cont'].forEach(k => { if (saved[k] != null) document.getElementById(k).value = saved[k]; });
  const upd = () => {
    document.getElementById('u-out').textContent = buildUtm() || 'Check the page link: it should start with https://';
    const s = {}; ['u-base', 'u-src', 'u-med', 'u-camp', 'u-cont'].forEach(k => s[k] = document.getElementById(k).value); lsSet('st-utm-form', s);
  };
  f.addEventListener('input', upd); f.addEventListener('change', upd); upd();
  const recent = () => {
    const r = lsGet('st-utm-recent', []);
    document.getElementById('u-recent').innerHTML = r.length ? '<span class="task-meta">Recent (tap to copy)</span>' + r.map((x, i) => `<button type="button" data-copy="${reg(x)}">${esc(x)}</button>`).join('') : '';
  };
  recent();
  document.getElementById('u-copy').onclick = e => {
    const link = buildUtm(); if (!link) return;
    doCopy(link, e.currentTarget);
    const r = lsGet('st-utm-recent', []).filter(x => x !== link); r.unshift(link); lsSet('st-utm-recent', r.slice(0, 5)); recent();
  };
}

/* ---------- context tab tables ---------- */
const PRODUCTS = [
  ['On Me', '15404008308949', 'bill-idhar', 'ST-ON-ME', '₹599'],
  ['Brainwave', '15404009291989', 'haan-mera-idea-tha', 'ST-BRAINWAVE', '₹599'],
  ['Diet Cherry', '15404022071509', 'haan-wohi-wali', 'ST-DIET-CHERRY', '₹599'],
  ['Green Flag', '15404016533717', 'tum-aa-jao-main-dekh-lungi', 'ST-GREEN-FLAG', '₹499'],
  ['Shaadi Shift', '15404020236501', 'dulhan-tu-duty-meri', 'ST-SHAADI-SHIFT', '₹699'],
  ['Wild Card', '15404064047317', 'achha-tum-pehle', 'ST-WILD-CARD', '₹699'],
  ['Pinky Promise', '15404065390805', 'haath-do-main-hoon', 'ST-PINKY-PROMISE', '₹499']
];
function renderContext() {
  document.getElementById('ctx-products').innerHTML = PRODUCTS.map((p, i) => {
    const s = SETS[i];
    return `<tr><td><span class="dot" style="background:${s.colour}"></span>${p[0]}</td><td class="num">${p[1]}</td><td class="num">${p[2]}</td><td class="num">${p[3]}</td><td class="num">${p[4]}</td><td class="num">10 (9 Oct)</td><td>${esc(s.line)} · ${esc(s.note)}</td><td class="num">${s.colour}</td></tr>`;
  }).join('');
  document.getElementById('ctx-sets').innerHTML = SETS.map(s => `<tr><td><span class="dot" style="background:${s.colour}"></span>${esc(s.name)}</td><td>${esc(s.line)}</td><td>${esc(s.note)}</td><td>${esc(s.nails)}</td><td>${esc(s.moment)}</td></tr>`).join('');
  document.getElementById('start-prompt').textContent = START_PROMPT;
}

const START_PROMPT = `You are joining the Small Talk store rebuild as a Claude Code session. Work in C:\\Users\\SSTS\\Desktop\\Riya. Use Opus at effort xhigh unless the task is purely operational (then Sonnet).
Working outside that folder? Clone the private repository https://github.com/shubhamdev91/smalltalks-riya and read AGENTS.md first; paths below are relative to its root.

1. Read, in order: Small-Talk-Claude-Implementation-Checklist.md (RESUME HERE is the current truth), C:\\Users\\SSTS\\AppData\\Roaming\\Claude\\side-session-notes\\local_04b83008-0590-42b6-b099-ee4eb0903f2d\\00-orchestrator-protocol.md, C:\\Users\\SSTS\\Downloads\\Small-Talk-Claude-Complete-Brief (1).md (brand rules), spec\\INDEX.md + spec\\tokens.css, copy\\00-register.md + copy\\FACTS.md, qa\\FINAL-ACCEPTANCE.md, and anything in talks\\ or motion\\ your task touches.
2. Store: 0nev20-vn.myshopify.com (Basic, INR, India). BUILD theme = 186651934933 "Small Talk — Claude build (Horizon)", unpublished; it is the ONLY theme anyone writes. LIVE theme = a published duplicate (older copy) of 186651934933; the owner re-publishes by duplicating the build and publishing the copy. Never touch the live copy, nor 186573160661 (former live ChatGPT build), 186547241173, 186572636373, 162461974741, 186667663573.
3. The orchestrator session local_e4896004-68cd-4d55-9d37-ab925783b63b owns the checklist and the single theme write lock. Before any theme write, ask it for the lock; write only after a grant newer than your last release; release explicitly with md5 readbacks. Report to it by SendMessage (one-line summary first); put large evidence in the shared notes folder as <you>-<topic>.md.
4. Shared store data (products, prices, pages, posts, menus, metaobjects, policies, SEO fields) = proposal to the orchestrator; the owner approves. Every shopper-visible word comes from st-copy (local_ae886ffe-08a8-44d3-abdb-ee70ca852b0d) with a register ID. Motion files belong to st-fable (local_46bc18b1-5655-4160-b44f-e32f2f475df6), the only Fable session; never start another.
5. Locked brand rules: "Diet Cherry" (never "Cherry Repeat"); Brainwave = "Haan, mera idea hai."; no campus/college references; no fake reviews, ratings or counts; no medical claims; no new AI artwork by agents (process owner art only, ≤1.3× Lanczos).
6. Never ask for or handle secrets (API keys, client secrets, salts); the owner pastes them into Vercel or provider dashboards.
Then tell the orchestrator who you are, what task you were given, and your plan, and wait for its go-ahead before writing anything.`;

/* ---------- tabs ---------- */
const TABS = ['plan', 'our', 'context'];
function showTab(name) {
  if (!TABS.includes(name)) name = 'plan';
  TABS.forEach(n => {
    document.getElementById('tab-' + n).hidden = n !== name;
    document.getElementById('tabbtn-' + n).setAttribute('aria-selected', n === name);
  });
  lsSet('st-tab', name);
}
TABS.forEach(n => { document.getElementById('tabbtn-' + n).onclick = () => { showTab(n); history.replaceState(null, '', '#' + n); scrollTo(0, 0); }; });
document.addEventListener('click', e => {
  const a = e.target.closest('a[href^="#sec-"]');
  if (!a) return;
  e.preventDefault();
  const sec = document.getElementById(a.getAttribute('href').slice(1));
  if (!sec) return;
  sec.open = true;
  sec.scrollIntoView({ behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'start' });
});

/* ---------- boot ---------- */
document.getElementById('stickers').innerHTML = SETS.map((s, i) => nailSvg(s.colour, [-14, 8, -5, 12, -9, 6, -12][i])).join('');
renderSections();
renderContext();
renderProgress();
const h = (location.hash || '').slice(1);
showTab(TABS.includes(h) ? h : lsGet('st-tab', 'plan'));
window.addEventListener('hashchange', () => { const x = (location.hash || '').slice(1); if (TABS.includes(x)) showTab(x); else if (x.startsWith('task-')) jumpTo(x.slice(5)); });
document.getElementById('order-toggle').addEventListener('click', () => setOrderOpen(document.getElementById('order-toggle').getAttribute('aria-expanded') !== 'true'));
setOrderOpen(!!lsGet('st-order-open', false));
document.addEventListener('click', e => {
  const a = e.target.closest('a[data-jump]');
  if (!a) return;
  e.preventDefault();
  jumpTo(a.dataset.jump);
});
if (h.startsWith('task-')) setTimeout(() => jumpTo(h.slice(5)), 60);
['sections', 'our-sections'].forEach(id => {
  const root = document.getElementById(id);
  root.addEventListener('change', e => {
    const c = e.target.closest('.chk');
    if (c) setDone(c.dataset.task, c.checked);
  });
  root.addEventListener('toggle', e => {
    const d = e.target;
    if (d.classList && d.classList.contains('sec')) { const o = lsGet(LS_OPEN, {}); o[d.id.slice(4)] = d.open; lsSet(LS_OPEN, o); }
  }, true);
});
initDb();
