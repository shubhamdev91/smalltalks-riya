// the talks: relative times (TLK-009) and anonymous posting (TLK-1xx): the composer, replies and reports.
// Posts go to the talks backend through the App Proxy (cfg.endpoint, /apps/talks); nothing is sent anywhere else.
// Her alias, avatar set and device id live in localStorage on her device only. All copy comes from
// #st-talks-config (locale small_talk.talks.live.*) and data attributes, so no shopper-visible text lives here.
// Markup built here mirrors snippets/st-talk-row.liquid and st-talk-reply.liquid (keep them in step).

const $ = (sel, root = document) => root.querySelector(sel);
const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];

/* Relative times: "9 Oct" from Liquid becomes "just now · n min ago · nh ago · nd ago" under 7 days. */
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

/* Live talks */
let cfg = null;
try {
  cfg = JSON.parse($('#st-talks-config')?.textContent || 'null');
} catch {
  cfg = null;
}
if (cfg && !window.__stTalksLive) {
  window.__stTalksLive = true;
  live(cfg);
}

function live(cfg) {
  const S = cfg.strings;
  const E = S.errors;
  const DWELL_MS = 2600; // the backend treats faster submits as bots
  const MINE_TTL = 30 * 60 * 1000;
  const HELD_TTL = 24 * 60 * 60 * 1000;

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
    let a = pick(cfg.adjectives);
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

  function aliasProblem(value) {
    const flat = value.toLowerCase().replace(/[\s._-]+/g, ' ').trim();
    if (value.length < 2 || value.length > cfg.max.alias) return true;
    if (!/^[\p{L}\p{N} ._'-]+$/u.test(value)) return true;
    if (/small ?talk/.test(flat) || ['admin', 'mod', 'moderator', 'official', 'team', 'support', 'staff', 'owner'].includes(flat)) return true;
    return Boolean(contactCode(value));
  }

  /** The backend's headline rule: first line, or its first sentence (≤ 110 characters). */
  function splitTitle(text) {
    const nl = text.indexOf('\n');
    const first = (nl < 0 ? text : text.slice(0, nl)).trim();
    const rest = nl < 0 ? '' : text.slice(nl + 1).trim();
    if (first.length <= 110) return [first, rest];
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
    return [title, [remainder, rest].filter(Boolean).join('\n')];
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

  /** Replace a row in place; if it had focus, its replacement takes it (screen readers hear the new state). */
  function swap(oldEl, newEl) {
    const hadFocus = document.activeElement === oldEl;
    oldEl.replaceWith(newEl);
    if (hadFocus) {
      newEl.tabIndex = -1;
      newEl.focus({ preventScroll: true });
    }
    return newEl;
  }

  const withBreaks = (text) => String(text).split('\n').flatMap((line, i) => (i ? [h('br'), line] : [line]));

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

  /* Her alias and avatar everywhere: "Posting as …", "Replying as …" and the discs next to the fields. */
  function paintMe() {
    const m = me();
    for (const slot of $$('[data-st-me-avatar]')) slot.replaceChildren(avatar(m.avatar));
    for (const slot of $$('[data-st-as]')) {
      const replying = slot.closest('[data-st-reply-form]');
      slot.textContent = fmt(replying ? S.replying_as : S.posting_as, { alias: m.alias });
    }
  }

  function wireAlias(form) {
    const toggle = $('[data-st-alias-toggle]', form);
    const panel = $('[data-st-alias-panel]', form);
    const input = /** @type {HTMLInputElement | null} */ ($('[data-st-alias-input]', form));
    const hint = $('[data-st-alias-hint]', form);
    if (!toggle || !panel || !input) return;
    const hintText = hint?.textContent ?? '';
    const close = (focusToggle) => {
      panel.hidden = true;
      toggle.setAttribute('aria-expanded', 'false');
      if (focusToggle) toggle.focus();
    };
    toggle.addEventListener('click', () => {
      if (!panel.hidden) return close(false);
      panel.hidden = false;
      toggle.setAttribute('aria-expanded', 'true');
      input.value = me().alias;
      input.focus();
      input.select();
    });
    $('[data-st-alias-shuffle]', form)?.addEventListener('click', () => {
      input.value = newAlias();
      input.focus();
    });
    const save = () => {
      const value = input.value.trim().replace(/^@+/, '');
      if (aliasProblem(value)) {
        if (hint) {
          hint.textContent = E.bad_alias;
          hint.dataset.tone = 'error';
        }
        input.setAttribute('aria-invalid', 'true');
        input.focus();
        return;
      }
      if (hint) {
        hint.textContent = hintText;
        delete hint.dataset.tone;
      }
      input.removeAttribute('aria-invalid');
      store.set('st-talks-me', { ...me(), alias: value });
      paintMe();
      close(true);
    };
    $('[data-st-alias-save]', form)?.addEventListener('click', save);
    input.addEventListener('keydown', (event) => {
      if (event.key === 'Enter') {
        event.preventDefault();
        save();
      } else if (event.key === 'Escape') {
        close(true);
      }
    });
  }

  /* ---------- Threads: the hub list and the composer ---------- */

  const section = $('[data-st-feed]');
  const feed = section?.dataset.stFeed ?? '';
  const list = $('[data-st-list]');
  const firstPage = !list || list.dataset.page === '1';

  function feedTakes(topic) {
    if (!list || !firstPage) return false;
    return feed === 'all' || feed === topic || (topic === '__own' && feed === 'something-else');
  }

  function rowFor(t, state) {
    const linked = Boolean(t.url) && !state;
    const inner = h(linked ? 'a' : 'div', { class: 'st-trow__link', href: linked ? t.url : null });
    const stateEl =
      state === 'pending'
        ? h('span', { class: 'st-trow__state' }, S.posting)
        : state === 'held'
          ? h('span', { class: 'st-trow__state' }, S.held_tag)
          : state === 'failed'
            ? h('span', { class: 'st-trow__state' }, S.failed)
            : timeEl(t.posted_at);
    inner.append(
      avatar(t.avatar),
      h(
        'span',
        { class: 'st-trow__text' },
        h('span', { class: 'st-trow__meta' }, h('span', { class: 'st-trow__author' }, t.alias), stateEl),
        h('span', { class: 'st-trow__title' }, t.title),
        t.body ? h('span', { class: 'st-trow__excerpt' }, t.body.replace(/\s+/g, ' ').slice(0, 160)) : null,
        linked ? h('span', { class: 'st-trow__count' }, S.first_reply) : null,
      ),
    );
    if (linked) {
      const chevron = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      chevron.setAttribute('viewBox', '0 0 8 14');
      chevron.setAttribute('aria-hidden', 'true');
      chevron.innerHTML = '<path d="M1.5 1.5 L6.5 7 L1.5 12.5"/>';
      $('.st-trow__count', inner)?.append(chevron);
    }
    return h('li', { class: `st-trow is-mine${state ? ` is-${state}` : ''}`, 'data-st-thread': t.handle || null }, inner);
  }

  function showInList(row) {
    if (!list) return;
    list.prepend(row);
    $('[data-st-empty]')?.setAttribute('hidden', '');
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
      const ttl = t.status === 'held' ? HELD_TTL : MINE_TTL;
      if (!t.handle || now - t.saved > ttl) continue;
      if (list.querySelector(`[data-st-thread="${CSS.escape(t.handle)}"]:not(.is-mine)`)) continue; // Shopify has it
      keep.push(t);
      if (feedTakes(t.topic) && !list.querySelector(`[data-st-thread="${CSS.escape(t.handle)}"]`)) {
        showInList(rowFor(t, t.status === 'held' ? 'held' : null));
      }
    }
    store.set('st-talks-mine', keep);
  }

  function wireComposer(form) {
    const ta = /** @type {HTMLTextAreaElement} */ ($('textarea[name="text"]', form));
    const own = /** @type {HTMLInputElement} */ ($('input[name="topic_own"]', form));
    const status = $('[data-st-status]', form);
    const left = $('[data-st-left]', form);
    const postBtn = $('.st-compose__post', form);
    const isRow = form.classList.contains('st-compose--row');
    let openedAt = 0;
    let busy = false;

    const topicChoice = () => /** @type {HTMLInputElement | null} */ ($('input[name="topic"]:checked', form))?.value ?? '';
    const open = () => {
      if (!openedAt) openedAt = performance.now();
      form.dataset.open = '';
    };
    const counter = () => {
      if (!left) return;
      const remaining = cfg.max.thread - ta.value.length;
      left.textContent = remaining < 120 ? fmt(S.left, { n: remaining }) : '';
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
    const setTopic = (value, ownText) => {
      const radio = /** @type {HTMLInputElement | null} */ ($(`input[name="topic"][value="${CSS.escape(value || '')}"]`, form));
      if (radio) radio.checked = true;
      own.hidden = value !== '__own';
      if (ownText != null) own.value = ownText;
    };

    const draft = store.get('st-talks-draft', null);
    if (draft?.text && !ta.value) {
      ta.value = draft.text;
      if (draft.topic) setTopic(draft.topic, draft.own);
      if (isRow) form.dataset.open = '';
      counter();
    }

    form.addEventListener('focusin', open);
    ta.addEventListener('input', () => {
      open();
      counter();
      saveDraft();
      clearError();
    });
    own?.addEventListener('input', () => {
      saveDraft();
      clearError();
    });
    form.addEventListener('change', (event) => {
      const target = /** @type {HTMLInputElement} */ (event.target);
      if (target.name !== 'topic') return;
      own.hidden = target.value !== '__own';
      if (!own.hidden) own.focus();
      clearError();
      saveDraft();
    });
    if (isRow) {
      form.addEventListener('focusout', () => {
        setTimeout(() => {
          if (!form.contains(document.activeElement) && !ta.value.trim() && !busy) delete form.dataset.open;
        }, 0);
      });
    }

    async function send(payload, row) {
      const waited = performance.now() - openedAt;
      if (waited < DWELL_MS) await sleep(DWELL_MS - waited);
      payload.t = Math.round(performance.now() - openedAt);
      try {
        const { thread } = await api(payload);
        store.set('st-talks-draft', null);
        const t = { ...thread, topic: payload.topic || '__own' };
        if (thread.handle) remember('st-talks-mine', t);
        const held = thread.status === 'held';
        if (row) swap(row, rowFor(t, held ? 'held' : null));
        if (held) say(status, S.held);
        else if (row) say(status, S.posted);
        else if (thread.url) say(status, [`${S.posted} · `, h('a', { href: thread.url }, S.view)]);
        else say(status, S.posted);
      } catch (error) {
        const failed = error.transient;
        if (row && failed) {
          const failedRow = rowFor({ ...payload, ...splitParts(payload.text), posted_at: null }, 'failed');
          const retry = h('button', { type: 'button' }, S.retry);
          const edit = h('button', { type: 'button' }, S.edit);
          failedRow.append(h('div', { class: 'st-trow__fail' }, E.server, retry, edit));
          swap(row, failedRow);
          retry.addEventListener('click', () => {
            const again = rowFor({ ...payload, ...splitParts(payload.text) }, 'pending');
            swap(failedRow, again);
            send(payload, again);
          });
          edit.addEventListener('click', () => {
            failedRow.remove();
            ta.value = payload.text;
            setTopic(payload.topic || '__own', payload.topic_own);
            open();
            ta.focus();
          });
          say(status, E.server, 'error');
        } else {
          row?.remove();
          if (!ta.value.trim()) {
            ta.value = payload.text;
            setTopic(payload.topic || '__own', payload.topic_own);
          }
          open();
          showError(error.code, error.code === 'bad_alias' ? $('[data-st-alias-toggle]', form) : ta);
        }
      } finally {
        busy = false;
        postBtn?.removeAttribute('aria-disabled');
      }
    }

    const splitParts = (text) => {
      const [title, body] = splitTitle(text);
      return { title, body };
    };

    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      if (busy) return;
      clearError();
      const text = ta.value.trim();
      const choice = topicChoice();
      const ownText = choice === '__own' ? own.value.trim() : '';
      if (text.length < 3) return showError('too_short', ta);
      if (text.length > cfg.max.thread) return showError('too_long', ta);
      if (!choice) return showError('need_topic', $('input[name="topic"]', form));
      if (choice === '__own' && !ownText) return showError('need_topic', own);
      const blocked = contactCode(`${ownText}\n${text}`);
      if (blocked) return showError(blocked, ownText && contactCode(ownText) ? own : ta);

      busy = true;
      postBtn?.setAttribute('aria-disabled', 'true');
      if (!openedAt) openedAt = performance.now();
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
        row = rowFor({ ...payload, ...splitParts(text), handle: '' }, 'pending');
        showInList(row);
      }
      ta.value = '';
      own.value = '';
      counter();
      say(status, S.posting);
      if (isRow && row) {
        // Fold the composer and bring her new row into view: it carries "Posting…" and then her talk.
        delete form.dataset.open;
        row.tabIndex = -1;
        row.focus({ preventScroll: true });
        row.scrollIntoView({ block: 'nearest', behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
      }
      await send(payload, row);
    });
  }

  /* ---------- Replies ---------- */

  const replies = $('[data-st-replies]');

  function replyFor(r, state) {
    const colour = cfg.sets.includes(r.avatar) ? r.avatar : 'on-me';
    const initial = (r.alias || '?').replace(/^@/, '').trim().slice(0, 1).toUpperCase();
    const disc = h(
      'span',
      { class: `st-reply-item__avatar${cfg.lightInk.includes(colour) ? ' st-reply-item__avatar--light' : ''}`, 'aria-hidden': 'true' },
      initial,
    );
    disc.style.setProperty('--st-reply-bg', `var(--st-tile-${colour})`);
    const stateEl =
      state === 'pending'
        ? h('span', { class: 'st-reply-item__state' }, S.posting)
        : state === 'held'
          ? h('span', { class: 'st-reply-item__state' }, S.held_tag)
          : state === 'failed'
            ? h('span', { class: 'st-reply-item__state' }, S.failed)
            : timeEl(r.posted_at);
    const acts = h('div', { class: 'st-reply-item__acts' });
    if (!state && r.handle) {
      acts.append(
        h('button', { type: 'button', class: 'st-act', 'data-st-reply-to': r.handle, 'aria-label': fmt(S.reply_to_label, { alias: r.alias }) }, S.reply),
      );
    }
    return h(
      'li',
      {
        class: `st-reply-item is-mine${r.depth ? ' st-reply-item--nested' : ''}${state ? ` is-${state}` : ''}`,
        id: r.handle ? `reply-${r.handle}` : null,
        'data-st-reply': r.handle || null,
        'data-depth': r.depth ? 1 : 0,
        'data-alias': r.alias,
      },
      disc,
      h(
        'div',
        { class: 'st-reply-item__text' },
        h(
          'p',
          { class: 'st-reply-item__meta' },
          h('span', { class: 'st-reply-item__alias' }, r.alias),
          ' · ',
          stateEl,
          r.depth && r.reply_to ? h('span', { class: 'st-reply-item__to' }, fmt(S.replying_to, { alias: r.reply_to })) : null,
        ),
        h('div', { class: 'st-reply-item__body' }, h('p', {}, withBreaks(r.body ?? r.text ?? ''))),
        acts,
      ),
    );
  }

  /** Where a reply goes: after its parent's block (the parent and its nested replies), else at the end. */
  function placeReply(li, parentHandle) {
    if (!replies) return;
    const parent = parentHandle ? replies.querySelector(`[data-st-reply="${CSS.escape(parentHandle)}"]`) : null;
    if (!parent) {
      replies.append(li);
    } else {
      let anchor = parent;
      while (anchor.nextElementSibling && anchor.nextElementSibling.getAttribute('data-depth') === '1') anchor = anchor.nextElementSibling;
      anchor.after(li);
    }
    $('[data-st-empty]', replies.parentElement ?? document)?.setAttribute('hidden', '');
  }

  function bumpCount() {
    const el = $('[data-st-count]');
    if (!el) return;
    const n = (Number(el.dataset.n) || Number((el.textContent || '').replace(/\D/g, '')) || 0) + 1;
    el.dataset.n = String(n);
    el.textContent = n === 1 ? S.reply_one : fmt(S.reply_other, { n });
    el.hidden = false;
  }

  function wireReplyForm(form) {
    const threadHandle = form.dataset.thread;
    const ta = /** @type {HTMLTextAreaElement} */ ($('textarea[name="text"]', form));
    const status = $('[data-st-status]', form);
    const bar = $('[data-st-reply-to-bar]', form);
    const barText = $('[data-st-reply-to-text]', form);
    const submit = $('.st-reply__submit', form);
    let parent = null;
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
      if (bar && barText) {
        bar.hidden = !parent;
        barText.textContent = parent ? fmt(S.replying_to, { alias }) : '';
      }
    };
    document.addEventListener('click', (event) => {
      const btn = /** @type {HTMLElement} */ (event.target).closest?.('[data-st-reply-to]');
      if (!btn) return;
      const li = btn.closest('[data-st-reply]');
      setParent(btn.getAttribute('data-st-reply-to'), li?.getAttribute('data-alias') ?? '');
      form.scrollIntoView({ block: 'center', behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
      ta.focus({ preventScroll: true });
    });
    $('[data-st-reply-cancel]', form)?.addEventListener('click', () => {
      setParent(null);
      ta.focus();
    });

    async function send(payload, li) {
      const waited = performance.now() - openedAt;
      if (waited < DWELL_MS) await sleep(DWELL_MS - waited);
      payload.t = Math.round(performance.now() - openedAt);
      try {
        const { reply } = await api(payload);
        store.set(draftKey, null);
        const held = reply.status === 'held';
        const done = replyFor({ ...reply, body: payload.text }, held ? 'held' : null);
        swap(li, done);
        if (reply.handle) remember(`st-talks-replies:${threadHandle}`, { ...reply, body: payload.text }, 20);
        if (held) say(status, S.held);
        else {
          bumpCount();
          say(status, S.posted);
        }
      } catch (error) {
        if (error.transient) {
          const failedLi = replyFor({ ...payload }, 'failed');
          const retry = h('button', { type: 'button', class: 'st-act st-act--strong' }, S.retry);
          const edit = h('button', { type: 'button', class: 'st-act' }, S.edit);
          $('.st-reply-item__acts', failedLi)?.append(E.server, retry, edit);
          swap(li, failedLi);
          retry.addEventListener('click', () => {
            const again = replyFor({ ...payload }, 'pending');
            swap(failedLi, again);
            send(payload, again);
          });
          edit.addEventListener('click', () => {
            failedLi.remove();
            ta.value = payload.text;
            ta.focus();
          });
          say(status, E.server, 'error');
        } else {
          li.remove();
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
      if (!text) return say(status, E.too_short, 'error'), ta.focus();
      if (text.length > cfg.max.reply) return say(status, fmt(E.too_long, { max: cfg.max.reply }), 'error'), ta.focus();
      const blocked = contactCode(text);
      if (blocked) {
        say(status, E[blocked], 'error');
        ta.setAttribute('aria-invalid', 'true');
        return ta.focus();
      }
      busy = true;
      submit?.setAttribute('aria-disabled', 'true');
      if (!openedAt) openedAt = performance.now();
      const m = me();
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
        depth: parent ? 1 : 0,
        reply_to: parent?.alias ?? null,
      };
      const li = replyFor(payload, 'pending');
      placeReply(li, parent?.handle);
      ta.value = '';
      setParent(null);
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
      const ttl = r.status === 'held' ? HELD_TTL : MINE_TTL;
      if (!r.handle || now - r.saved > ttl) continue;
      if (replies.querySelector(`[data-st-reply="${CSS.escape(r.handle)}"]:not(.is-mine)`)) continue;
      keep.push(r);
      if (!replies.querySelector(`[data-st-reply="${CSS.escape(r.handle)}"]`)) {
        placeReply(replyFor(r, r.status === 'held' ? 'held' : null), r.parent);
      }
    }
    store.set(key, keep);
  }

  /* ---------- Reports: one tap + confirm, then folded away on her device ---------- */

  const findItem = (target) => {
    const [kind, handle] = target.split(':');
    return kind === 'reply'
      ? $(`[data-st-reply="${CSS.escape(handle)}"]`)
      : $(`[data-st-item="${CSS.escape(target)}"]`);
  };

  function fold(item, justNow) {
    if (!item || item.classList.contains('is-reported')) return;
    let note = $(':scope > .st-folded', item);
    if (!note) {
      const show = h('button', { type: 'button', class: 'st-act st-act--strong' }, S.show);
      note = h('p', { class: 'st-folded', role: justNow ? 'status' : null }, justNow ? S.reported : S.hidden_for_you, ' ', show);
      show.addEventListener('click', () => item.classList.remove('is-reported'));
      item.append(note);
    }
    item.classList.add('is-reported');
  }

  for (const target of store.get('st-talks-reported', [])) fold(findItem(target), false);

  document.addEventListener('click', (event) => {
    const btn = /** @type {HTMLElement} */ (event.target).closest?.('[data-st-report]');
    if (!btn || btn.hidden) return;
    const target = btn.getAttribute('data-st-report') ?? '';
    const yes = h('button', { type: 'button', class: 'st-act st-act--strong' }, S.report_yes);
    const no = h('button', { type: 'button', class: 'st-act' }, S.cancel);
    const ask = h('span', { class: 'st-confirm', role: 'group' }, h('span', {}, S.report_confirm), yes, no);
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
        fold(findItem(target), true);
      } catch {
        yes.removeAttribute('aria-disabled');
        ask.querySelector('span')?.replaceChildren(E.server);
      }
    });
  });

  /* ---------- Start ---------- */

  paintMe();
  for (const form of $$('[data-st-compose], [data-st-reply-form]')) wireAlias(form);
  for (const form of $$('[data-st-compose]')) wireComposer(form);
  for (const form of $$('[data-st-reply-form]')) wireReplyForm(form);
  restoreMine();
  restoreReplies();

  const focusComposer = () => /** @type {HTMLTextAreaElement | null} */ ($('[data-st-compose] textarea'))?.focus({ preventScroll: true });
  for (const link of $$('[data-st-start]')) {
    link.addEventListener('click', () => setTimeout(focusComposer, 0));
  }
  if (location.hash === '#start-a-talk') focusComposer();
}
