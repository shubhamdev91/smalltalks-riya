// the talks, UX v4: relative times (TLK-009), Reddit-style threads (fold TLK-179, "continue this thread" TLK-178) and
// anonymous posting (the hero writing box, inline replies under any comment, reports). Posts go to the talks backend
// through the App Proxy (cfg.endpoint, /apps/talks); nothing is sent anywhere else. Her alias, avatar set and device id
// live in localStorage on her device only. All copy comes from #st-talks-config (locale small_talk.talks.live.v4.*)
// and data attributes, so no shopper-visible text lives here. User text only ever goes in as text nodes.
// Markup built here mirrors snippets/st-talk-row.liquid and st-talk-reply.liquid (keep them in step).

const $ = (sel, root = document) => root.querySelector(sel);
const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];
const reduceMotion = () => matchMedia('(prefers-reduced-motion: reduce)').matches;

/* Relative times: "9 Oct" from Liquid becomes "just now · 5m · 2h · 3d" under 7 days. */
const agoStrings = /** @type {HTMLElement | null} */ ($('[data-st-ago-strings]'))?.dataset ?? {};
const fillN = (pattern, n) => (pattern ? pattern.replace('__n__', String(n)) : null);

/** @param {HTMLElement} el */
function relTime(el) {
  const at = Number(el.dataset.stAgo) * 1000;
  if (!at) return;
  const minutes = Math.floor((Date.now() - at) / 60000);
  let text = null;
  if (minutes < 1) text = agoStrings.agoNow ?? null;
  else if (minutes < 60) text = fillN(agoStrings.agoMinutes, minutes);
  else if (minutes < 1440) text = fillN(agoStrings.agoHours, Math.floor(minutes / 60));
  else if (minutes < 10080) text = fillN(agoStrings.agoDays, Math.floor(minutes / 1440));
  if (text) el.textContent = text;
}

$$('time[data-st-ago]').forEach(relTime);

let cfg = null;
try {
  cfg = JSON.parse($('#st-talks-config')?.textContent || 'null');
} catch {
  cfg = null;
}
if (cfg && !window.__stTalksLive) {
  window.__stTalksLive = true;
  talks(cfg);
}

function talks(cfg) {
  const S = cfg.strings;
  const E = S.errors;
  const DWELL_MS = 2600; // the backend treats faster submits as bots
  const MINE_TTL = 30 * 60 * 1000;
  const desktop = matchMedia('(min-width: 1024px)');

  /* Storage that never throws (private mode, blocked storage): falls back to memory for this page. */
  const memory = new Map();
  const store = {
    get(key, fallback) {
      try {
        const raw = localStorage.getItem(key);
        return raw == null ? (memory.has(key) ? memory.get(key) : fallback) : JSON.parse(raw);
      } catch {
        return memory.has(key) ? memory.get(key) : fallback;
      }
    },
    set(key, value) {
      memory.set(key, value);
      try {
        if (value == null) localStorage.removeItem(key);
        else localStorage.setItem(key, JSON.stringify(value));
      } catch {
        /* memory only */
      }
    },
  };

  const pick = (list) => list[Math.floor(Math.random() * list.length)];
  const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
  const fmt = (text, vars = {}) =>
    String(text ?? '')
      .replace('__alias__', vars.alias ?? '')
      .replace('__n__', vars.n ?? '')
      .replace('__max__', vars.max ?? '');

  function uuid() {
    if (crypto.randomUUID) return crypto.randomUUID();
    const b = crypto.getRandomValues(new Uint8Array(16));
    return [...b].map((x) => x.toString(16).padStart(2, '0')).join('').replace(/^(.{8})(.{4})(.{4})(.{4})/, '$1-$2-$3-$4-');
  }

  function newAlias() {
    const a = pick(cfg.adjectives);
    let n = pick(cfg.nouns);
    for (let i = 0; i < 5 && a === n; i++) n = pick(cfg.nouns);
    return `${a}${n}`.replace(/\s+/g, '').slice(0, cfg.max.alias);
  }

  /** Her identity on this device: { device, alias, avatar }. */
  function me() {
    let m = store.get('st-talks-me', null);
    if (!m || !m.device || !m.alias || !cfg.sets.includes(m.avatar)) {
      m = {
        device: m?.device || uuid(),
        alias: m?.alias || newAlias(),
        avatar: cfg.sets.includes(m?.avatar) ? m.avatar : pick(cfg.sets),
      };
      store.set('st-talks-me', m);
    }
    return m;
  }

  /* Mirror of the backend's contact / link / handle checks, for instant feedback (the server stays the authority). */
  const RX = {
    phone: /\+?\d[\d\s\-().]{6,}\d/g,
    email: /[a-z0-9._%+-]+@[a-z0-9-]+(?:\.[a-z0-9-]+)+/i,
    emailSpelled:
      /\b[a-z0-9._%+-]{2,}\s*(?:\(at\)|\[at\]|\{at\}|\sat\s)\s*(?:gmail|yahoo|outlook|hotmail|icloud|rediffmail|rediff|proton|protonmail|live)\b/i,
    upi: /\b[a-z0-9._-]{2,}@(?:ok)?(?:axis|hdfc|icici|sbi|ybl|paytm|upi|apl|ibl|axl)\b/i,
    url: /(?:https?:\/\/|\bwww\.)\S+/i,
    shortLink: /\bwa\.me\b|\bt\.me\b|\bbit\.ly\b|\blinktr\.ee\b/i,
    domain:
      /\b[a-z0-9][a-z0-9-]{1,62}\.(?:com|in|net|org|co|io|me|ly|app|xyz|link|gg|tv|info|biz|shop|store|site|online|live|club|page|to|fm|cc|ai|dev|lol|social|chat|bio|ink|xxx)(?:\.[a-z]{2,3})?\b/i,
    handle: /(?:^|[^\w@])@[a-z0-9_.]{2,}/i,
    social:
      /\b(?:insta|instagram|ig|snap|snapchat|sc|twitter|tiktok|telegram|tg|discord|threads|bumble|hinge|tinder|bereal)\s*(?:id|handle|username|user\s*name|user)?\s*(?:[:=]|->|→)\s*@?[a-z0-9_.]{3,}/i,
    socialWords: /\b(?:insta|instagram|ig|snap|snapchat|twitter|telegram|discord)\s+(?:id|handle|username)\s+(?:is\s+|hai\s+|:)?@?[a-z0-9_.]{3,}/i,
  };

  function contactCode(text) {
    for (const run of text.match(RX.phone) ?? []) if (run.replace(/\D/g, '').length >= 10) return 'blocked_contact';
    if (RX.email.test(text) || RX.emailSpelled.test(text) || RX.upi.test(text)) return 'blocked_contact';
    if (RX.url.test(text) || RX.shortLink.test(text) || RX.domain.test(text)) return 'blocked_link';
    if (RX.handle.test(text) || RX.social.test(text) || RX.socialWords.test(text)) return 'blocked_handle';
    return null;
  }

  /** The backend's headline rule: first line, or its first sentence (≤ 110 characters). */
  function splitTitle(text) {
    const nl = text.indexOf('\n');
    const first = (nl < 0 ? text : text.slice(0, nl)).trim();
    const rest = nl < 0 ? '' : text.slice(nl + 1).trim();
    if (first.length <= 110) return { title: first, body: rest };
    const m = first.match(/^(.{8,110}?[.?!…])(?:\s|$)/);
    let title;
    let remainder;
    if (m) {
      title = m[1].trim();
      remainder = first.slice(m[0].length).trim();
    } else {
      let cut = first.lastIndexOf(' ', 89);
      cut = cut > 40 ? cut : 90;
      title = `${first.slice(0, cut).replace(/[ ,;:-]+$/, '')}…`;
      remainder = `…${first.slice(cut).trimStart()}`;
    }
    return { title, body: [remainder, rest].filter(Boolean).join('\n') };
  }

  /* DOM helpers: user text only ever goes in as text nodes. */
  function h(tag, attrs = {}, ...kids) {
    const el = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) {
      if (v == null || v === false) continue;
      el.setAttribute(k, v === true ? '' : String(v));
    }
    for (const kid of kids.flat()) {
      if (kid == null || kid === false) continue;
      el.append(kid instanceof Node ? kid : document.createTextNode(String(kid)));
    }
    return el;
  }

  function svg(viewBox, d) {
    const el = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    el.setAttribute('viewBox', viewBox);
    el.setAttribute('aria-hidden', 'true');
    el.setAttribute('focusable', 'false');
    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    path.setAttribute('d', d);
    el.append(path);
    return el;
  }

  /** Replace an element in place; if it had focus, its replacement takes it (screen readers hear the new state). */
  function swap(oldEl, newEl) {
    const hadFocus = oldEl.contains(document.activeElement);
    oldEl.replaceWith(newEl);
    if (hadFocus) {
      newEl.tabIndex = -1;
      newEl.focus({ preventScroll: true });
    }
    return newEl;
  }

  const withBreaks = (text) => String(text).split('\n').flatMap((line, i) => (i ? [h('br'), line] : [line]));

  /** "posting as {alias}" with the alias in bold (TLK-104 / TLK-103). */
  function asLine(pattern, alias) {
    const [before, after = ''] = String(pattern ?? '').split('__alias__');
    return [before, h('b', {}, alias), after];
  }

  function avatar(set) {
    const disc = h('span', { class: 'st-tavatar', 'aria-hidden': 'true' }, h('span', { class: 'st-tavatar__nail' }));
    if (cfg.sprites[set]) disc.style.setProperty('--st-nails', `url("${cfg.sprites[set]}")`);
    return disc;
  }

  function timeEl(iso) {
    const at = Date.parse(iso || '') || Date.now();
    const el = h('time', { class: 'st-ago', datetime: new Date(at).toISOString(), 'data-st-ago': Math.floor(at / 1000) });
    el.textContent = agoStrings.agoNow ?? '';
    relTime(el);
    return el;
  }

  async function api(payload) {
    let res;
    let data = {};
    try {
      res = await fetch(cfg.endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify(payload),
        credentials: 'same-origin',
      });
      data = await res.json().catch(() => ({}));
    } catch {
      throw Object.assign(new Error('server'), { code: 'server', transient: true });
    }
    if (!res.ok || !data.ok) {
      const code = data.code && E[data.code] ? data.code : 'server';
      throw Object.assign(new Error(code), { code, transient: code === 'server' });
    }
    return data;
  }

  function say(statusEl, text, tone) {
    if (!statusEl) return;
    statusEl.textContent = '';
    if (tone) statusEl.dataset.tone = tone;
    else delete statusEl.dataset.tone;
    statusEl.append(...(Array.isArray(text) ? text : [text]).filter(Boolean));
  }

  /* Her alias everywhere: "posting as …" (composer) and "replying as …" (reply box). */
  function paintMe() {
    const m = me();
    for (const slot of $$('[data-st-as]')) {
      const replying = slot.closest('[data-st-reply-form]');
      slot.replaceChildren(...asLine(replying ? S.replying_as : S.posting_as, m.alias));
    }
  }

  /* ---------- Threads list: the hub / topic feed and the hero box ---------- */

  const hub = $('[data-st-feed]');
  const feed = hub?.dataset.stFeed ?? '';
  const list = $('[data-st-list]');
  const firstPage = !list || list.dataset.page === '1';

  function feedTakes(topic) {
    if (!list || !firstPage) return false;
    return feed === 'all' || feed === topic || (topic === '__own' && feed === 'something-else');
  }

  function rowFor(t, state) {
    const linked = Boolean(t.url) && !state;
    const meta = h('span', { class: 'tk-meta' }, h('b', {}, t.alias), ' · ', state ? (state === 'pending' ? S.posting : S.failed) : timeEl(t.posted_at));
    const inner = h(
      linked ? 'a' : 'div',
      { class: 'tk-row', href: linked ? t.url : null },
      h('span', { class: 'tk-row__av' }, avatar(t.avatar)),
      h(
        'span',
        { class: 'tk-row__text' },
        meta,
        h('span', { class: 'tk-row__title' }, t.title),
        t.body ? h('span', { class: 'tk-row__ex' }, t.body.replace(/\s+/g, ' ').slice(0, 160)) : null,
        h('span', { class: 'tk-foot' }, svg('0 0 16 16', 'M2.5 3.5h11v7h-6l-3 2.5v-2.5h-2z'), S.no_replies),
      ),
    );
    return h('li', { class: `tk-r is-mine${state ? ` is-${state}` : ''}`, 'data-st-thread': t.handle || null }, inner);
  }

  function showInList(row) {
    if (!list) return;
    list.prepend(row);
    $('[data-st-empty]', hub ?? document)?.setAttribute('hidden', '');
  }

  function remember(key, item, max = 12) {
    const items = store.get(key, []).filter((x) => x.handle !== item.handle);
    items.unshift({ ...item, saved: Date.now() });
    store.set(key, items.slice(0, max));
  }

  /* Storefront pages can lag a few seconds behind a new entry: keep her own fresh talks on top until Shopify has them. */
  function restoreMine() {
    if (!list) return;
    const now = Date.now();
    const keep = [];
    for (const t of store.get('st-talks-mine', [])) {
      if (!t.handle || now - t.saved > MINE_TTL) continue;
      if (list.querySelector(`[data-st-thread="${CSS.escape(t.handle)}"]:not(.is-mine)`)) continue; // Shopify has it
      keep.push(t);
      if (feedTakes(t.topic) && !list.querySelector(`[data-st-thread="${CSS.escape(t.handle)}"]`)) showInList(rowFor(t, null));
    }
    store.set('st-talks-mine', keep);
  }

  function wireComposer(form) {
    const ta = /** @type {HTMLTextAreaElement} */ ($('textarea[name="text"]', form));
    const topicSel = /** @type {HTMLSelectElement} */ ($('[data-st-topic]', form));
    const ownBox = $('[data-st-own]', form);
    const own = /** @type {HTMLInputElement} */ ($('input[name="topic_own"]', form));
    const status = $('[data-st-status]', form);
    const postBtn = $('.tk-post', form);
    let openedAt = 0;
    let busy = false;
    let lastNudge = '';
    let nudgeIndex = -1;

    const topicChoice = () => topicSel?.value ?? '';
    const open = () => {
      if (!openedAt) openedAt = performance.now();
    };
    const saveDraft = () => store.set('st-talks-draft', { text: ta.value, topic: topicChoice(), own: own?.value ?? '' });
    const clearError = () => {
      if (status?.dataset.tone === 'error') say(status, '');
      for (const el of $$('[aria-invalid]', form)) el.removeAttribute('aria-invalid');
    };
    const showError = (code, field) => {
      say(status, fmt(E[code] ?? E.server, { max: cfg.max.thread.toLocaleString('en-IN') }), 'error');
      if (field) {
        field.setAttribute('aria-invalid', 'true');
        field.focus();
      }
    };
    const syncOwn = () => {
      if (ownBox) ownBox.hidden = topicChoice() !== '__own';
    };
    const setTopic = (value, ownText) => {
      if (topicSel && [...topicSel.options].some((o) => o.value === value)) topicSel.value = value;
      syncOwn();
      if (ownText != null && own) own.value = ownText;
    };

    const draft = store.get('st-talks-draft', null);
    if (draft?.text && !ta.value) {
      ta.value = draft.text;
      if (draft.topic) setTopic(draft.topic, draft.own);
    }

    /* The phone's "spill your tea" bar hides while she types (keyboard up). */
    form.addEventListener('focusin', () => {
      open();
      hub?.classList.add('tk-typing');
    });
    form.addEventListener('focusout', () => {
      setTimeout(() => {
        if (!form.contains(document.activeElement)) hub?.classList.remove('tk-typing');
      }, 0);
    });
    ta.addEventListener('input', () => {
      open();
      saveDraft();
      clearError();
    });
    own?.addEventListener('input', () => {
      saveDraft();
      clearError();
    });
    topicSel?.addEventListener('change', () => {
      syncOwn();
      if (topicChoice() === '__own') own?.focus();
      clearError();
      saveDraft();
    });

    /* "need a nudge?" (TLK-175): a starter for the chosen topic (TLK-158), or the flat list (TLK-176); never over her
       own words. Each tap shows the next one. */
    $('[data-st-nudge]', form)?.addEventListener('click', () => {
      const lines = cfg.starters[topicChoice()] ?? cfg.nudges;
      if (!lines?.length) return;
      if (ta.value.trim() && ta.value !== lastNudge) {
        ta.focus();
        return;
      }
      nudgeIndex = (nudgeIndex + 1) % lines.length;
      lastNudge = `${lines[nudgeIndex]} `;
      ta.value = lastNudge;
      open();
      saveDraft();
      ta.focus();
      ta.setSelectionRange(ta.value.length, ta.value.length);
    });

    $('[data-st-shuffle]', form)?.addEventListener('click', () => {
      store.set('st-talks-me', { ...me(), alias: newAlias() });
      paintMe();
    });

    async function send(payload, row) {
      const waited = performance.now() - openedAt;
      if (waited < DWELL_MS) await sleep(DWELL_MS - waited);
      payload.t = Math.round(performance.now() - openedAt);
      try {
        const { thread } = await api(payload);
        store.set('st-talks-draft', null);
        lastNudge = '';
        const t = { ...thread, topic: payload.topic || '__own' };
        if (thread.handle) remember('st-talks-mine', t);
        if (row) {
          swap(row, rowFor(t, null));
          say(status, S.posted);
        } else if (thread.url) {
          say(status, [`${S.posted} `, h('a', { href: thread.url }, S.view)]);
        } else {
          say(status, S.posted);
        }
      } catch (error) {
        if (row && error.transient) {
          const failedRow = rowFor({ ...payload, ...splitTitle(payload.text) }, 'failed');
          const retry = h('button', { type: 'button', class: 'tk-act tk-act--strong' }, S.retry);
          const edit = h('button', { type: 'button', class: 'tk-act' }, S.edit);
          failedRow.append(h('div', { class: 'tk-r__fail' }, E.server, retry, edit));
          swap(row, failedRow);
          retry.addEventListener('click', () => {
            const again = rowFor({ ...payload, ...splitTitle(payload.text) }, 'pending');
            swap(failedRow, again);
            send(payload, again);
          });
          edit.addEventListener('click', () => {
            failedRow.remove();
            ta.value = payload.text;
            setTopic(payload.topic || '__own', payload.topic_own);
            ta.focus();
          });
          say(status, E.server, 'error');
        } else {
          // Refused (might name someone, blocked, busy, slow down…): nothing was saved, her words stay in the box.
          row?.remove();
          if (!ta.value.trim()) {
            ta.value = payload.text;
            setTopic(payload.topic || '__own', payload.topic_own);
          }
          showError(error.code, ta);
        }
      } finally {
        busy = false;
        postBtn?.removeAttribute('aria-disabled');
      }
    }

    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      if (busy) return;
      clearError();
      const text = ta.value.trim();
      const choice = topicChoice();
      const ownText = choice === '__own' ? (own?.value ?? '').trim() : '';
      if (text.length < 3 || text === lastNudge.trim()) return showError('too_short', ta);
      if (text.length > cfg.max.thread) return showError('too_long', ta);
      if (!choice) return showError('need_topic', topicSel);
      if (choice === '__own' && !ownText) return showError('need_topic', own);
      const blocked = contactCode(`${ownText}\n${text}`);
      if (blocked) return showError(blocked, ownText && contactCode(ownText) ? own : ta);

      busy = true;
      postBtn?.setAttribute('aria-disabled', 'true');
      open();
      const m = me();
      const payload = {
        action: 'post',
        text,
        topic: choice === '__own' ? '' : choice,
        topic_own: ownText,
        alias: m.alias,
        avatar: m.avatar,
        device: m.device,
        hp: /** @type {HTMLInputElement | null} */ (form.elements.namedItem('website'))?.value ?? '',
        t: 0,
      };
      let row = null;
      if (feedTakes(choice)) {
        row = rowFor({ ...payload, ...splitTitle(text), handle: '' }, 'pending');
        showInList(row);
      }
      ta.value = '';
      if (own) own.value = '';
      say(status, S.posting);
      if (row) {
        row.tabIndex = -1;
        row.focus({ preventScroll: true });
        row.scrollIntoView({ block: 'nearest', behavior: reduceMotion() ? 'auto' : 'smooth' });
      }
      await send(payload, row);
    });
  }

  /* ---------- Replies: Reddit-style tree on a flat list ---------- */

  const replies = $('[data-st-replies]');
  const folded = new Set();
  const continued = new Set();
  const depthOf = (li) => Number(li.dataset.depth) || 0;
  const limit = () => (desktop.matches ? 6 : 4); // levels visible before "continue this thread ›"

  /** Ancestors (nearest last) and descendant counts from display order and depth. */
  function tree() {
    const items = $$(':scope > .tk-c', replies);
    const stack = [];
    for (const li of items) {
      const d = depthOf(li);
      while (stack.length && depthOf(stack[stack.length - 1]) >= d) stack.pop();
      li._anc = [...stack];
      stack.push(li);
    }
    items.forEach((li, i) => {
      let n = 0;
      for (let j = i + 1; j < items.length && depthOf(items[j]) > depthOf(li); j++) n++;
      li._desc = n;
    });
    return items;
  }

  /** The ancestor that "continue this thread" opens for a deep comment: its deepest ancestor above the limit. */
  const gateOf = (li, L) => [...li._anc].reverse().find((a) => depthOf(a) < L) ?? null;

  function foldToggle(li) {
    let btn = $(':scope > .tk-c__fold', li);
    if (!btn) {
      btn = h('button', { type: 'button', class: 'tk-c__fold', 'aria-expanded': 'true' }, h('span', { 'aria-hidden': 'true' }, '−'));
      btn.addEventListener('click', () => {
        folded.add(li);
        layout();
        $(':scope > .tk-c__head > .tk-c__more', li)?.focus();
      });
      li.prepend(btn);
    }
    btn.setAttribute('aria-label', fmt(S.collapse_label, { alias: li.dataset.alias ?? '' }));
    return btn;
  }

  function morePill(li) {
    const head = $(':scope > .tk-c__head', li);
    let pill = $(':scope > .tk-c__more', head);
    if (!pill) {
      pill = h('button', { type: 'button', class: 'tk-c__more', 'aria-expanded': 'false' });
      pill.addEventListener('click', () => {
        folded.delete(li);
        layout();
        $(':scope > .tk-c__fold', li)?.focus();
      });
      head?.append(pill);
    }
    const n = li._desc;
    pill.textContent = `+ ${n === 1 ? S.more_one : fmt(S.more_other, { n })}`;
    pill.setAttribute('aria-label', fmt(S.expand_label, { alias: li.dataset.alias ?? '', n }));
    return pill;
  }

  /** Recompute folds, "continue" rows and what is visible. Runs on load, on every change and on resize. */
  function layout() {
    if (!replies) return;
    for (const row of $$(':scope > .tk-continue-row', replies)) row.remove();
    const items = tree();
    const L = limit();
    let lastGate = null;
    for (const li of items) {
      if (!li.isConnected) continue;
      const parent = li._desc > 0;
      li.classList.toggle('tk-c--parent', parent && !folded.has(li));
      li.classList.toggle('tk-c--folded', parent && folded.has(li));
      if (!parent) folded.delete(li);
      if (parent) foldToggle(li).setAttribute('aria-expanded', String(!folded.has(li)));
      else $(':scope > .tk-c__fold', li)?.remove();
      if (parent && folded.has(li)) morePill(li);
      else $(':scope > .tk-c__head > .tk-c__more', li)?.remove();

      const hiddenByFold = li._anc.some((a) => folded.has(a));
      const gate = depthOf(li) >= L ? gateOf(li, L) : null;
      const hiddenByDepth = Boolean(gate) && !continued.has(gate);
      li.hidden = hiddenByFold || hiddenByDepth;
      // One "continue this thread ›" before each run of comments the depth limit hides (TLK-178).
      if (hiddenByDepth && !hiddenByFold && gate !== lastGate) {
        const btn = h('button', { type: 'button', class: 'tk-continue' }, S.continue);
        const row = h('li', { class: 'tk-continue-row', style: `--d: ${Math.min(depthOf(gate) + 1, L)}` }, btn);
        btn.addEventListener('click', () => {
          continued.add(gate);
          layout();
          const first = items.find((x) => x._anc.includes(gate) && !x.hidden);
          if (first) {
            first.tabIndex = -1;
            first.focus({ preventScroll: false });
          }
        });
        li.before(row);
      }
      lastGate = hiddenByDepth ? gate : null;
    }
  }

  /** Make a comment visible: unfold its ancestors and open "continue" above it. */
  function reveal(li) {
    tree();
    for (const a of li._anc ?? []) folded.delete(a);
    const L = limit();
    if (depthOf(li) >= L) {
      const gate = gateOf(li, L);
      if (gate) continued.add(gate);
    }
    layout();
  }

  function replyFor(r, state) {
    const colour = cfg.sets.includes(r.avatar) ? r.avatar : 'on-me';
    const initial = (r.alias || '?').replace(/^@/, '').trim().slice(0, 1).toUpperCase();
    const disc = h('span', { class: `tk-c__av${cfg.lightInk.includes(colour) ? ' tk-c__av--light' : ''}`, 'aria-hidden': 'true' }, initial);
    disc.style.setProperty('--c', `var(--st-tile-${colour})`);
    const when = state ? (state === 'pending' ? S.posting : S.failed) : timeEl(r.posted_at);
    const acts = h('div', { class: 'tk-c__acts' });
    if (!state && r.handle) {
      acts.append(
        h('button', { type: 'button', class: 'tk-act', 'data-st-reply-to': r.handle, 'aria-label': fmt(S.reply_to_label, { alias: r.alias }) }, S.reply),
      );
    }
    const depth = Math.min(Number(r.depth) || 0, cfg.max.depth);
    const li = h(
      'li',
      {
        class: `tk-c is-mine${state ? ` is-${state}` : ''}`,
        id: r.handle ? `reply-${r.handle}` : null,
        'aria-level': depth + 1,
        'data-st-reply': r.handle || null,
        'data-depth': depth,
        'data-alias': r.alias,
        'data-parent': r.parent || null,
      },
      h('p', { class: 'tk-c__head' }, disc, h('b', { class: 'tk-c__alias' }, r.alias), h('span', { class: 'tk-c__when' }, '· ', when)),
      h('div', { class: 'tk-c__body' }, h('p', {}, withBreaks(r.body ?? r.text ?? ''))),
      acts,
    );
    li.style.setProperty('--d', String(depth));
    return li;
  }

  /** Where a new reply goes (mirrors the backend): at the end of its parent's subtree, else at the end. */
  function placeReply(li, parentHandle) {
    if (!replies) return;
    const parent = parentHandle ? $(`:scope > [data-st-reply="${CSS.escape(parentHandle)}"]`, replies) : null;
    if (!parent) {
      replies.append(li);
    } else {
      const pd = depthOf(parent);
      let anchor = parent;
      for (let next = anchor.nextElementSibling; next; next = next.nextElementSibling) {
        if (next.classList.contains('tk-continue-row')) continue;
        if (depthOf(next) <= pd) break;
        anchor = next;
      }
      anchor.after(li);
    }
    $('[data-st-empty]', replies.parentElement ?? document)?.setAttribute('hidden', '');
    reveal(li);
  }

  function bumpCount() {
    const el = $('[data-st-count]');
    if (!el) return;
    const n = (Number(el.dataset.n) || 0) + 1;
    el.dataset.n = String(n);
    el.textContent = n === 1 ? S.reply_one : fmt(S.reply_other, { n });
    el.hidden = false;
  }

  function wireReplyForm(form) {
    const threadHandle = form.dataset.thread;
    const home = $('[data-st-reply-home]');
    const ta = /** @type {HTMLTextAreaElement} */ ($('textarea[name="text"]', form));
    const status = $('[data-st-status]', form);
    const bar = $('[data-st-reply-to-bar]', form);
    const barText = $('[data-st-reply-to-text]', form);
    const cancels = $$('[data-st-reply-cancel]', form);
    const submit = $('.tk-post', form);
    let parent = null;
    let opener = null;
    let openedAt = 0;
    let busy = false;
    const draftKey = `st-talks-reply:${threadHandle}`;

    const draft = store.get(draftKey, null);
    if (draft?.text) ta.value = draft.text;

    form.addEventListener('focusin', () => {
      if (!openedAt) openedAt = performance.now();
    });
    ta.addEventListener('input', () => {
      store.set(draftKey, { text: ta.value });
      if (status?.dataset.tone === 'error') say(status, '');
      ta.removeAttribute('aria-invalid');
    });

    const setParent = (handle, alias) => {
      parent = handle ? { handle, alias } : null;
      if (bar) bar.hidden = !parent;
      if (barText) barText.replaceChildren(...(parent ? asLine(S.replying_to, alias) : []));
      for (const c of cancels) if (c.classList.contains('tk-cancel')) c.hidden = !parent;
    };

    /* "reply" on any comment opens this same box right under it; one box at a time. */
    const openUnder = (li, btn) => {
      setParent(li.dataset.stReply, li.dataset.alias ?? '');
      opener = btn;
      li.append(form);
      say(status, '');
      ta.focus({ preventScroll: true });
      form.scrollIntoView({ block: 'nearest', behavior: reduceMotion() ? 'auto' : 'smooth' });
    };
    /** Back under the talk; focus returns to the "reply" that opened it (unless told where to go). */
    const close = (focusOpener = true) => {
      const back = opener;
      setParent(null);
      opener = null;
      if (home && form.previousElementSibling !== home) home.after(form);
      if (focusOpener && back?.isConnected) back.focus();
    };

    document.addEventListener('click', (event) => {
      const btn = /** @type {HTMLElement} */ (event.target).closest?.('[data-st-reply-to]');
      if (!btn) return;
      const li = btn.closest('.tk-c');
      if (li) openUnder(li, btn);
    });
    for (const c of cancels) c.addEventListener('click', () => close(true));
    form.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && parent) {
        event.preventDefault();
        close(true);
      }
    });

    async function send(payload, li) {
      const waited = performance.now() - openedAt;
      if (waited < DWELL_MS) await sleep(DWELL_MS - waited);
      payload.t = Math.round(performance.now() - openedAt);
      try {
        const { reply } = await api(payload);
        store.set(draftKey, null);
        const done = replyFor({ ...reply, body: payload.text }, null);
        swap(li, done);
        layout();
        if (reply.handle) remember(`st-talks-replies:${threadHandle}`, { ...reply, body: payload.text }, 20);
        bumpCount();
        say(status, S.posted);
      } catch (error) {
        if (error.transient) {
          const failedLi = replyFor({ ...payload }, 'failed');
          const retry = h('button', { type: 'button', class: 'tk-act tk-act--strong' }, S.retry);
          const edit = h('button', { type: 'button', class: 'tk-act' }, S.edit);
          $('.tk-c__acts', failedLi)?.append(E.server, retry, edit);
          swap(li, failedLi);
          layout();
          retry.addEventListener('click', () => {
            const again = replyFor({ ...payload }, 'pending');
            swap(failedLi, again);
            layout();
            send(payload, again);
          });
          edit.addEventListener('click', () => {
            failedLi.remove();
            layout();
            ta.value = payload.text;
            ta.focus();
          });
          say(status, E.server, 'error');
        } else {
          // Refused: nothing was saved; the box goes back to where she was writing, with her words.
          li.remove();
          layout();
          const back = payload.parent ? $(`:scope > [data-st-reply="${CSS.escape(payload.parent)}"]`, replies) : null;
          if (back) openUnder(back, $('[data-st-reply-to]', back));
          if (!ta.value.trim()) ta.value = payload.text;
          say(status, fmt(E[error.code] ?? E.server, { max: cfg.max.reply }), 'error');
          ta.setAttribute('aria-invalid', 'true');
          ta.focus();
        }
      } finally {
        busy = false;
        submit?.removeAttribute('aria-disabled');
      }
    }

    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      if (busy) return;
      const text = ta.value.trim();
      const fail = (code) => {
        say(status, fmt(E[code], { max: cfg.max.reply }), 'error');
        ta.setAttribute('aria-invalid', 'true');
        ta.focus();
      };
      if (!text) return fail('too_short');
      if (text.length > cfg.max.reply) return fail('too_long');
      const blocked = contactCode(text);
      if (blocked) return fail(blocked);
      busy = true;
      submit?.setAttribute('aria-disabled', 'true');
      if (!openedAt) openedAt = performance.now();
      const m = me();
      const parentLi = parent ? $(`:scope > [data-st-reply="${CSS.escape(parent.handle)}"]`, replies) : null;
      const payload = {
        action: 'reply',
        thread: threadHandle,
        parent: parent?.handle ?? null,
        text,
        alias: m.alias,
        avatar: m.avatar,
        device: m.device,
        hp: /** @type {HTMLInputElement | null} */ (form.elements.namedItem('website'))?.value ?? '',
        t: 0,
        depth: parentLi ? Math.min(depthOf(parentLi) + 1, cfg.max.depth) : 0,
      };
      const li = replyFor(payload, 'pending');
      ta.value = '';
      close(false);
      placeReply(li, payload.parent);
      li.tabIndex = -1;
      li.focus({ preventScroll: true });
      li.scrollIntoView({ block: 'nearest', behavior: reduceMotion() ? 'auto' : 'smooth' });
      say(status, S.posting);
      await send(payload, li);
    });
  }

  function restoreReplies() {
    const page = $('[data-st-thread-page]');
    if (!page || !replies) return;
    const key = `st-talks-replies:${page.getAttribute('data-st-thread-page')}`;
    const now = Date.now();
    const keep = [];
    for (const r of store.get(key, [])) {
      if (!r.handle || now - r.saved > MINE_TTL) continue;
      if ($(`:scope > [data-st-reply="${CSS.escape(r.handle)}"]:not(.is-mine)`, replies)) continue; // Shopify has it
      keep.push(r);
      if (!$(`:scope > [data-st-reply="${CSS.escape(r.handle)}"]`, replies)) placeReply(replyFor(r, null), r.parent);
    }
    store.set(key, keep);
  }

  /* ---------- Reports: one tap + confirm, then folded away on her device ---------- */

  const findItem = (target) => {
    const [kind, handle] = target.split(':');
    return kind === 'reply' ? $(`[data-st-reply="${CSS.escape(handle)}"]`) : $(`[data-st-item="${CSS.escape(target)}"]`);
  };

  function foldReported(item, justNow) {
    if (!item || item.classList.contains('is-reported')) return;
    let note = $(':scope > .st-folded', item);
    if (!note) {
      const show = h('button', { type: 'button', class: 'tk-act tk-act--strong' }, S.show);
      note = h('p', { class: 'st-folded', role: justNow ? 'status' : null }, justNow ? S.reported : S.hidden_for_you, ' ', show);
      show.addEventListener('click', () => item.classList.remove('is-reported'));
      item.append(note);
    }
    item.classList.add('is-reported');
  }

  function wireReports() {
    for (const target of store.get('st-talks-reported', [])) foldReported(findItem(target), false);
    document.addEventListener('click', (event) => {
      const btn = /** @type {HTMLElement} */ (event.target).closest?.('[data-st-report]');
      if (!btn || btn.hidden) return;
      const target = btn.getAttribute('data-st-report') ?? '';
      const yes = h('button', { type: 'button', class: 'tk-act tk-act--strong' }, S.report_yes);
      const no = h('button', { type: 'button', class: 'tk-act' }, S.cancel);
      const ask = h('span', { class: 'tk-confirm', role: 'group' }, h('span', {}, S.report_confirm), yes, no);
      btn.hidden = true;
      btn.after(ask);
      yes.focus();
      no.addEventListener('click', () => {
        ask.remove();
        btn.hidden = false;
        btn.focus();
      });
      yes.addEventListener('click', async () => {
        if (yes.getAttribute('aria-disabled')) return;
        yes.setAttribute('aria-disabled', 'true');
        try {
          await api({ action: 'report', target, device: me().device });
          const reported = store.get('st-talks-reported', []);
          if (!reported.includes(target)) store.set('st-talks-reported', [target, ...reported].slice(0, 200));
          ask.remove();
          btn.hidden = false;
          foldReported(findItem(target), true);
        } catch (error) {
          yes.removeAttribute('aria-disabled');
          ask.querySelector('span')?.replaceChildren(E[error.code] ?? E.server);
        }
      });
    });
  }

  /* ---------- Start ---------- */

  if (replies) {
    layout();
    desktop.addEventListener('change', layout);
  }
  if (!cfg.live) return;

  paintMe();
  for (const form of $$('[data-st-compose]')) wireComposer(form);
  for (const form of $$('[data-st-reply-form]')) wireReplyForm(form);
  wireReports();
  restoreMine();
  restoreReplies();

  /* "spill your tea" (dock, empty state, "spill it ›" from a thread): scroll to the writing box and focus it. */
  const focusComposer = (smooth) => {
    const ta = /** @type {HTMLTextAreaElement | null} */ ($('[data-st-compose] textarea'));
    if (!ta) return false;
    ta.closest('.tk-start')?.scrollIntoView({ block: 'start', behavior: smooth && !reduceMotion() ? 'smooth' : 'auto' });
    ta.focus({ preventScroll: true });
    return true;
  };
  for (const link of $$('[data-st-start]')) {
    link.addEventListener('click', (event) => {
      if (focusComposer(true)) event.preventDefault();
    });
  }
  if (location.hash === '#start-a-talk') focusComposer(false);

  /* House rules links open the rules where they are. */
  document.addEventListener('click', (event) => {
    const a = /** @type {HTMLElement} */ (event.target).closest?.('a[href="#house-rules"]');
    if (!a) return;
    const box = $('#house-rules');
    const details = box && [...box.querySelectorAll('details')].find((d) => d.offsetParent !== null);
    if (details) details.open = true;
  });
}
