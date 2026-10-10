/*
 * Small Talk hero motion controller.
 * Upgrades every [data-st-hero] root. Static Liquid first paint is never required to wait for this file.
 *
 * Principles
 * - Every flight is a Web Animations API animation on transform/opacity only (compositor), never per-frame JS.
 * - Flyers live inside the hero and are positioned in hero-local coordinates measured from the offset chain,
 *   so page scroll can never detach a nail. Ancestors of nail elements must not carry CSS transforms.
 * - Pausing (hold, user, hidden tab, offscreen, assets) pauses the running animations in place.
 * - Finite autoplay: at most MAX_SETS sets per pass, then settle. Manual navigation reaches all sets.
 * - Reduced motion: no flights, instant manual changes, autoplay never starts.
 */
(() => {
  'use strict';

  const ROOT = '[data-st-hero]';
  const MAX_SETS = 3;
  const ANCHOR = { x: 0.5, y: 0.925 }; // nail cell cuticle anchor, matches artwork/manifest.json
  const T = { sigHold: 700, accentFlight: 250, accentHold: 450, swapFlight: 250, swapHold: 450, nextFlight: 500, textFade: 180 };
  const REDUCED = window.matchMedia('(prefers-reduced-motion: reduce)');
  const controllers = new WeakMap();
  const decoded = new Map();

  const decode = (src) => {
    if (!src) return Promise.reject(new Error('missing artwork'));
    if (!decoded.has(src)) {
      decoded.set(src, new Promise((resolve, reject) => {
        const img = new Image();
        img.decoding = 'async';
        img.src = src;
        img.decode().then(() => (img.naturalWidth ? resolve(img) : reject(new Error('empty image'))), reject);
      }).catch((e) => { decoded.delete(src); throw e; }));
    }
    return decoded.get(src);
  };

  /** Every artwork URL a campaign's character uses (main image + optional parts). */
  const characterSrcs = (c) => {
    const ch = c && c.character;
    if (!ch || !ch.src) return [];
    return [ch.src, ...(Array.isArray(ch.parts) ? ch.parts.map((p) => p && p.src).filter(Boolean) : [])];
  };

  const parseAngle = (v) => {
    if (!v || v === 'none') return 0;
    const m = /(-?[\d.]+)(deg|rad|turn)?/.exec(v);
    if (!m) return 0;
    const n = parseFloat(m[1]);
    return m[2] === 'rad' ? (n * 180) / Math.PI : m[2] === 'turn' ? n * 360 : n;
  };

  const fill = (tpl, vars) => String(tpl || '').replace(/\{(\w+)\}/g, (_, k) => (vars[k] ?? ''));

  class HeroMotion {
    constructor(root) {
      this.root = root;
      const dataEl = root.querySelector('script[data-st-hero-data]');
      try { this.data = JSON.parse(dataEl.textContent); } catch { this.data = null; }
      if (!this.data || !Array.isArray(this.data.campaigns) || !this.data.campaigns.length) return;

      const q = (s) => root.querySelector(s);
      this.el = {
        scene: q('[data-st-hero-scene]'),
        note: q('[data-st-hero-note]'),
        headline: q('[data-st-hero-headline]'),
        finger: q('[data-st-hero-finger]'),
        toneImg: q('[data-st-hero-tone-sprite]'),
        mainBtn: q('[data-st-hero-main]'),
        main: q('[data-st-hero-main-nail]'),
        accents: [q('[data-st-hero-accent="1"]'), q('[data-st-hero-accent="2"]')],
        preview: q('[data-st-hero-preview]'),
        previewNails: [0, 1, 2, 3].map((i) => q(`[data-st-hero-preview-nail="${i}"]`)),
        character: q('[data-st-hero-character]'),
        characterImg: q('[data-st-hero-character-img]'),
        cta: q('[data-st-hero-cta]'),
        pause: q('[data-st-hero-pause]'),
        tone: q('[data-st-hero-tone]'),
        status: q('[data-st-hero-status]'),
        flyers: q('[data-st-hero-flyers]'),
      };
      if (!this.el.main || !this.el.headline || !this.el.cta || !this.el.preview) return;

      this.campaigns = this.data.campaigns;
      this.labels = this.data.labels || {};
      this.active = Math.max(0, this.campaigns.findIndex((c) => c.key === root.dataset.activeKey));
      const adKey = new URL(location.href).searchParams.get('set');
      const adIndex = this.campaigns.findIndex((c) => c.key === adKey);
      if (adIndex >= 0) this.active = adIndex;
      this.tone = Number(root.dataset.tone || this.data.defaultTone || 1);
      this.toneCount = (this.data.tones || []).length || Number(root.dataset.toneCount || 4);
      this.autoplayAllowed = root.dataset.autoplay === 'true' && this.data.autoplay !== false;
      this.mode = 'idle'; // idle | auto | manual | settled
      this.reasons = new Set();
      this.anims = new Set();
      this.gen = 0;
      this.busy = false;
      this.inFlight = false;
      this.ac = new AbortController();
      this.clock = document.createElement('span');
      this.clock.hidden = true;
      root.append(this.clock);

      this.holdArt = !!root.querySelector('img[data-st-src]'); // v3.7.2: first-paint art held until the LCP image
      this.bind();
      this.renderSet(this.active, false, { deferPreview: true }); // v3.7.1: preview nails are filled after the LCP image
      this.setTone(this.tone, false);
      this.enableControls();
      if (REDUCED.matches) this.reasons.add('reduced');
      if (document.hidden) this.reasons.add('hidden');
      this.syncControls();
      this.boot();
    }

    /* ---------- lifecycle ---------- */
    bind() {
      const { signal } = this.ac;
      const on = (el, ev, fn, opts) => el && el.addEventListener(ev, fn, { signal, ...(opts || {}) });
      on(this.el.preview, 'click', (e) => { e.preventDefault(); this.manualStep(1); });
      on(this.el.pause, 'click', () => this.togglePause());
      on(this.el.tone, 'click', () => this.setTone((this.tone % this.toneCount) + 1, true));

      // Hold to pause on the main nail (pointer + keyboard). Never captures vertical scroll.
      on(this.el.mainBtn, 'pointerdown', (e) => { if (e.button === 0 || e.pointerType !== 'mouse') this.hold(true); });
      on(window, 'pointerup', () => this.hold(false));
      on(window, 'pointercancel', () => this.hold(false));
      on(window, 'blur', () => this.hold(false));
      on(this.el.mainBtn, 'keydown', (e) => { if (e.code === 'Space' || e.code === 'Enter') { e.preventDefault(); this.hold(true); } });
      on(this.el.mainBtn, 'keyup', (e) => { if (e.code === 'Space' || e.code === 'Enter') this.hold(false); });
      on(this.el.mainBtn, 'blur', () => this.hold(false));

      // Horizontal swipe advances; vertical gestures are left to the page (touch-action: pan-y in CSS).
      on(this.root, 'pointerdown', (e) => { if (e.pointerType === 'touch') this.swipe = { x: e.clientX, y: e.clientY, t: performance.now() }; }, { passive: true });
      on(this.root, 'pointerup', (e) => {
        const s = this.swipe; this.swipe = null;
        if (!s || performance.now() - s.t > 700) return;
        const dx = e.clientX - s.x, dy = e.clientY - s.y;
        if (Math.abs(dx) > 48 && Math.abs(dx) > Math.abs(dy) * 1.5) this.manualStep(dx < 0 ? 1 : -1);
      }, { passive: true });
      on(this.root, 'pointercancel', () => { this.swipe = null; }, { passive: true });
      on(this.root, 'keydown', (e) => {
        if (e.target !== this.el.preview && e.target !== this.root) return;
        if (e.key === 'ArrowRight') { e.preventDefault(); this.manualStep(1); }
        if (e.key === 'ArrowLeft') { e.preventDefault(); this.manualStep(-1); }
      });

      on(document, 'visibilitychange', () => this.pause('hidden', document.hidden));
      on(window, 'pagehide', () => this.pause('pagehide', true));
      on(window, 'pageshow', () => this.pause('pagehide', false));
      on(REDUCED, 'change', (e) => { this.pause('reduced', e.matches); if (e.matches) this.abortToStill(); this.syncControls(); });

      this.io = new IntersectionObserver((entries) => this.pause('offscreen', !entries[0].isIntersecting), { threshold: 0.05 });
      this.io.observe(this.root);
      this.ro = new ResizeObserver(() => {
        this.scheduleBend();
        if (!this.inFlight) return;
        clearTimeout(this.resizeT);
        this.resizeT = setTimeout(() => this.onResizeDuringFlight(), 120);
      });
      this.ro.observe(this.root);
      // Headline metrics change when the display font arrives. v3.7.1: only the headline face triggers a re-bend, and
      // re-bends are coalesced (the home page loads ~10 font files; each used to force a synchronous re-layout).
      if (document.fonts) {
        const family = (getComputedStyle(this.el.headline).fontFamily.split(',')[0] || '').replace(/["']/g, '').trim().toLowerCase();
        document.fonts.ready.then(() => { if (!signal.aborted) this.scheduleBend(); }).catch(() => {});
        on(document.fonts, 'loadingdone', (e) => {
          const faces = e && e.fontfaces ? [...e.fontfaces] : null;
          if (!faces || !family || faces.some((f) => String(f.family).replace(/["']/g, '').trim().toLowerCase() === family)) this.scheduleBend();
        });
      }
      // v3.7.1: pause while a dialog (menu drawer, cart, search) is open, so no flight or commit competes with it.
      const overlay = () => this.pause('overlay', !!document.querySelector('dialog[open]'));
      this.mo = new MutationObserver(overlay);
      this.mo.observe(document.body, { subtree: true, attributes: true, attributeFilter: ['open'] });
    }

    /** Coalesced re-bend (resize, font arrival). */
    scheduleBend(delay = 120) {
      clearTimeout(this.bendT);
      this.bendT = setTimeout(() => { if (!this.destroyed) this.bendHeadline(); }, delay);
    }

    /** v3.7.1: resolves once the first-paint finger tone (the LCP image) has loaded, or after 8 s. */
    firstPaintLoaded() {
      const img = this.el.toneImg;
      if (!img || img.tagName !== 'IMG' || (img.complete && img.naturalWidth)) return Promise.resolve();
      return new Promise((resolve) => {
        const done = () => resolve();
        img.addEventListener('load', done, { once: true });
        img.addEventListener('error', done, { once: true });
        setTimeout(done, 8000);
      });
    }

    /** v3.7.2: load the art the Liquid held back (img[data-st-src]: set 1 character, preview hand). The attribute stays until
     *  the image has loaded, so CSS keeps it transparent and then fades it in. */
    revealHeld() {
      this.holdArt = false;
      this.root.querySelectorAll('img[data-st-src]').forEach((img) => {
        const url = img.getAttribute('data-st-src');
        const done = () => img.removeAttribute('data-st-src');
        img.addEventListener('load', done, { once: true });
        img.addEventListener('error', done, { once: true });
        img.removeAttribute('loading'); // the hold replaces lazy loading; a lazy flag would delay it again
        if (url) img.src = url; else done();
      });
    }

    /** v3.7.1: resolves after window load (capped at 4 s from now) and the next idle period. */
    pageSettled() {
      const load = document.readyState === 'complete' ? Promise.resolve()
        : new Promise((resolve) => { window.addEventListener('load', () => resolve(), { once: true }); setTimeout(resolve, 4000); });
      return load.then(() => new Promise((resolve) => ('requestIdleCallback' in window ? requestIdleCallback(() => resolve(), { timeout: 2000 }) : setTimeout(resolve, 200))));
    }

    destroy() {
      this.destroyed = true;
      this.gen++;
      this.anims.forEach((a) => a.cancel());
      this.anims.clear();
      this.ac.abort();
      this.io?.disconnect();
      this.ro?.disconnect();
      this.mo?.disconnect();
      clearTimeout(this.resizeT);
      clearTimeout(this.bendT);
      this.clearFlyers();
      this.clock.remove();
    }

    async boot() {
      const c = this.campaigns[this.active];
      try {
        await decode(c.sprite);
      } catch { /* static first paint already shows the set; nothing to add */ }
      // v3.7.1 load plan: nothing for later sets is requested before the LCP image (the finger tone) has loaded.
      // Then the preview hand gets the next set's nails; autoplay and the next set's art wait for page load + idle.
      await this.firstPaintLoaded();
      if (this.destroyed) return;
      this.revealHeld();
      this.renderPreview((this.active + 1) % this.campaigns.length);
      await this.pageSettled();
      if (this.destroyed) return;
      this.prefetch(this.active + 1);
      // v3.2: the shopper may have taken over while set 1 decoded (hand tap, swipe, arrow, pause/replay).
      // Starting autoplay now would cancel their manual flight, so leave their choice in place.
      if (this.mode !== 'idle' || this.destroyed) return;
      if (this.autoplayAllowed && !REDUCED.matches) this.startPass();
      else { this.mode = REDUCED.matches ? 'manual' : 'settled'; this.syncControls(); }
    }

    prefetch(i) {
      const c = this.campaigns[(i + this.campaigns.length) % this.campaigns.length];
      const go = () => { decode(c.sprite).catch(() => {}); characterSrcs(c).forEach((u) => decode(u).catch(() => {})); };
      'requestIdleCallback' in window ? requestIdleCallback(go, { timeout: 2000 }) : setTimeout(go, 300);
    }

    /* ---------- pause reasons ---------- */
    get running() { return this.mode === 'auto' && this.reasons.size === 0; }

    pause(reason, on) {
      if (on) this.reasons.add(reason); else this.reasons.delete(reason);
      if (this.reasons.size) this.anims.forEach((a) => { if (a.playState === 'running') a.pause(); });
      else if (this.mode === 'auto') this.anims.forEach((a) => { if (a.playState === 'paused') a.play(); });
      this.syncControls();
    }

    hold(on) {
      if (on === this.reasons.has('hold')) return;
      this.pause('hold', on);
    }

    togglePause() {
      if (REDUCED.matches) return;
      if (this.mode === 'auto' && !this.reasons.has('user')) { this.pause('user', true); return; }
      if (this.mode === 'auto') { this.pause('user', false); return; }
      // settled or manual: start a fresh finite pass from the current set
      this.reasons.delete('user');
      this.startPass();
    }

    syncControls() {
      const p = this.el.pause;
      if (p) {
        if (REDUCED.matches) p.hidden = true;
        else {
          p.hidden = false;
          const userPaused = this.mode === 'auto' && this.reasons.has('user');
          const replay = this.mode !== 'auto' && this.mode !== 'idle'; // idle = still decoding set 1 (or a hidden tab): autoplay is coming, not finished
          p.setAttribute('aria-pressed', String(userPaused));
          p.dataset.state = userPaused ? 'paused' : replay ? 'replay' : 'playing';
          p.setAttribute('aria-label', userPaused ? (this.labels.play || 'Play') : replay ? (this.labels.replay || 'Play again') : (this.labels.pause || 'Pause'));
        }
      }
      this.root.dataset.motion = this.mode;
    }

    /* ---------- WAAPI helpers ---------- */
    run(el, keyframes, options) {
      const gen = this.gen;
      const anim = el.animate(keyframes, { fill: 'forwards', ...options });
      this.anims.add(anim);
      if (this.reasons.size) anim.pause();
      return anim.finished.then(() => {
        this.anims.delete(anim);
        if (gen !== this.gen) throw abort();
        try { anim.commitStyles(); } catch { /* element may be detached */ }
        anim.cancel();
      }, () => { this.anims.delete(anim); throw abort(); });
    }

    wait(ms) { return this.run(this.clock, [{ opacity: 1 }, { opacity: 1 }], { duration: ms }); }

    /* ---------- geometry ---------- */
    // Hero-local box and cuticle anchor of a nail element. Walks the offset chain, so ancestors must not be transformed.
    anchorOf(el) {
      let x = 0, y = 0, n = el;
      while (n && n !== this.root) { x += n.offsetLeft; y += n.offsetTop; n = n.offsetParent; }
      const w = el.offsetWidth, h = el.offsetHeight;
      const rot = parseAngle(el.dataset.rot ?? getComputedStyle(el).rotate);
      return { x: x + w * ANCHOR.x, y: y + h * ANCHOR.y, w, h, rot };
    }

    transformAt(a, w, h, rot, scale) {
      return `translate(${(a.x - w * ANCHOR.x).toFixed(2)}px, ${(a.y - h * ANCHOR.y).toFixed(2)}px) rotate(${rot.toFixed(2)}deg) scale(${scale.toFixed(4)})`;
    }

    makeFlyer(sprite, col, w, h) {
      const f = document.createElement('span');
      f.className = 'st-nail st-hero__flyer';
      f.setAttribute('aria-hidden', 'true');
      f.style.setProperty('--st-nails', `url("${sprite}")`);
      f.style.setProperty('--col', String(col));
      f.style.width = `${w}px`;
      f.style.height = `${h}px`;
      (this.el.flyers || this.root).append(f);
      return f;
    }

    clearFlyers() { (this.el.flyers || this.root).querySelectorAll('.st-hero__flyer').forEach((f) => f.remove()); }

    /**
     * Fly one nail from `from` element's anchor to `to` element's anchor.
     * The flyer is sized like `to`; it starts scaled to match `from`.
     */
    fly({ from, to, sprite, col, duration, lift = 0.35, fadeTarget = true, hideFrom = true, arc = true }) {
      const a = this.anchorOf(from), b = this.anchorOf(to);
      const flyer = this.makeFlyer(sprite, col, b.w, b.h);
      const s0 = b.w ? a.w / b.w : 1;
      const liftPx = -Math.min(72, b.h * lift);
      const mid = { x: (a.x + b.x) / 2, y: (a.y + b.y) / 2 + (arc ? liftPx : 0) };
      const frames = [
        { transform: this.transformAt(a, b.w, b.h, a.rot, s0), easing: 'cubic-bezier(.4,0,.6,1)' },
        { transform: this.transformAt(mid, b.w, b.h, (a.rot + b.rot) / 2, (s0 + 1) / 2), easing: 'cubic-bezier(.3,0,.2,1)' },
        { transform: this.transformAt(b, b.w, b.h, b.rot, 1) },
      ];
      if (hideFrom) from.classList.add('is-hidden');
      const jobs = [this.run(flyer, frames, { duration })];
      // v3.3: keep the old nail until the flyer has nearly landed on it, then hand over underneath it, so the finger
      // never shows its bare natural nail mid-flight (visible at the board scale).
      if (fadeTarget) jobs.push(this.run(to, [{ opacity: 1 }, { opacity: 1, offset: 0.8 }, { opacity: 0 }], { duration }));
      return Promise.all(jobs).finally(() => flyer.remove());
    }

    /* ---------- rendering ---------- */
    setNail(el, sprite, col) {
      if (!el) return;
      el.style.setProperty('--st-nails', `url("${sprite}")`);
      el.style.setProperty('--col', String(col));
      el.classList.remove('is-hidden');
      el.style.opacity = '';
    }

    renderPreview(nextIndex) {
      const n = this.campaigns[nextIndex];
      const slots = n.previewSlots || [0, 1, 2, 0];
      this.el.preview.dataset.key = n.key;
      this.el.preview.setAttribute('aria-label', fill(this.labels.next || 'Next set: {name}', { name: n.name }));
      this.el.previewNails.forEach((el, i) => el && this.setNail(el, n.sprite, slots[i] ?? 0));
    }

    /** Swap the campaign character art. Placement and cropping are per set in CSS (keyed on data-active-key). */
    renderCharacter(c) {
      const box = this.el.character, img = this.el.characterImg;
      if (!box) return;
      const ch = c.character;
      if (!ch?.src) { box.hidden = true; return; }
      box.hidden = false;
      const st = box.style;
      st.left = st.right = st.top = st.bottom = st.translate = ''; // v2 wrote inline anchors; v3 never does
      box.dataset.bleed = (ch.bleed || []).join(' ');
      if (img) {
        if (this.holdArt && img.hasAttribute('data-st-src')) img.setAttribute('data-st-src', ch.src); // still held (v3.7.2)
        else if (img.getAttribute('src') !== ch.src) { img.removeAttribute('srcset'); img.removeAttribute('sizes'); img.removeAttribute('data-st-src'); img.src = ch.src; }
        if (ch.width) img.width = ch.width;
        if (ch.height) img.height = ch.height;
        img.alt = '';
      }
      // v3.4: optional extra layers (e.g. Wild Card's cards hand over the woman), painted above the main image in DOM
      // order. Placed per set in CSS via [data-st-hero-character-part="n"]; created on demand, hidden when unused.
      const parts = Array.isArray(ch.parts) ? ch.parts.filter((p) => p?.src) : [];
      const have = [...box.querySelectorAll('[data-st-hero-character-part]')];
      parts.forEach((p, i) => {
        let el = have[i];
        if (!el) {
          el = document.createElement('img');
          el.setAttribute('data-st-hero-character-part', String(i + 1));
          el.decoding = 'async';
          el.alt = '';
          box.appendChild(el);
          have.push(el);
        }
        if (el.getAttribute('src') !== p.src) el.src = p.src;
        if (p.width) el.width = p.width;
        if (p.height) el.height = p.height;
        el.hidden = false;
      });
      have.slice(parts.length).forEach((el) => { el.hidden = true; });
      box.style.opacity = '';
    }

    renderSet(i, announce, opts = {}) {
      const c = this.campaigns[i];
      const next = (i + 1) % this.campaigns.length;
      this.active = i;
      this.root.dataset.activeKey = c.key;
      this.root.dataset.activeIndex = String(i);
      this.root.dataset.nextKey = this.campaigns[next].key;
      const s = this.root.style;
      s.setProperty('--st-scene', c.colors.scene);
      s.setProperty('--st-scene-ink', c.colors.ink);
      s.setProperty('--st-cta-bg', c.colors.ctaBackground);
      s.setProperty('--st-cta-ink', c.colors.ctaForeground);
      if (this.el.scene) { this.el.scene.style.opacity = '0'; this.el.scene.style.background = ''; }
      if (this.el.note) this.el.note.textContent = c.note || '';
      this.setHeadline(c.headline, opts.deferBend);
      this.el.headline.style.opacity = ''; if (this.el.note) this.el.note.style.opacity = '';
      this.el.cta.href = c.url;
      if ('live' in c) this.el.cta.hidden = c.live === false; // fact-gated CTA: draft sets never look purchasable
      const desc = this.root.querySelector('[data-st-hero-main-desc]');
      if (desc && c.altText) desc.textContent = c.altText;
      this.el.cta.textContent = '';
      this.el.cta.append(document.createTextNode(c.ctaLabel || c.name));
      const arrow = document.createElement('span'); arrow.className = 'st-arrow'; arrow.setAttribute('aria-hidden', 'true'); arrow.textContent = '↗';
      this.el.cta.append(arrow);
      this.setNail(this.el.main, c.sprite, 0);
      const cols = this.sampleColumns(c);
      this.el.accents.forEach((el, k) => {
        if (!el) return;
        const col = cols[k];
        if (col == null) { el.classList.add('is-hidden'); el.style.setProperty('--st-nails', `url("${c.sprite}")`); }
        else this.setNail(el, c.sprite, col);
      });
      if (!opts.deferPreview) this.renderPreview(next);
      this.renderCharacter(c);
      if (announce && this.el.status) this.el.status.textContent = fill(this.labels.announce || '{name}. {headline}', c);
    }

    flightColumns(c) { return Array.isArray(c.flightColumns) ? c.flightColumns.filter((n) => n > 0).slice(0, 2) : [1, 2]; }

    /** Columns shown on the two loose samples. Defaults to the flight columns, padded with unused accent columns
     *  (Pinky Promise: [] -> [1, 2]). Green Flag passes sampleColumns [1, 0] in its JSON, as board 2 shows. */
    sampleColumns(c) {
      if (Array.isArray(c.sampleColumns)) return [0, 1].map((k) => (Number.isInteger(c.sampleColumns[k]) ? c.sampleColumns[k] : null));
      const f = this.flightColumns(c);
      const out = [f[0] ?? null, f[1] ?? null];
      [1, 2].filter((n) => !f.includes(n)).forEach((n) => { const i = out.indexOf(null); if (i >= 0) out[i] = n; });
      return out;
    }

    /* ---------- headline: real text, set on an arc ---------- */
    // Two sentences break between them; otherwise the most balanced word split (ties: shorter first line).
    // Short headlines (<= 12 characters) stay on one line.
    splitHeadline(text) {
      const t = String(text || '').trim();
      if (t.length <= 12) return [t];
      const sentences = t.match(/[^.!?]+[.!?]+/g);
      if (sentences && sentences.length === 2 && sentences.join('').length === t.length) return sentences.map((s) => s.trim());
      const words = t.split(/\s+/);
      let best = null;
      for (let i = 1; i < words.length; i++) {
        const a = words.slice(0, i).join(' '), b = words.slice(i).join(' ');
        const d = Math.abs(a.length - b.length);
        if (!best || d < best.d || (d === best.d && a.length < best.a.length)) best = { a, b, d };
      }
      return best ? [best.a, best.b] : [t];
    }

    setHeadline(text, deferBend) {
      const h = this.el.headline;
      if (!h) return;
      h.textContent = '';
      const sr = document.createElement('span');
      sr.className = 'st-hero__sr';
      sr.textContent = text;
      const vis = document.createElement('span');
      vis.className = 'st-hero__arc';
      vis.setAttribute('aria-hidden', 'true');
      this.splitHeadline(text).forEach((line) => {
        const l = document.createElement('span');
        l.className = 'st-hero__line';
        line.split(/\s+/).forEach((word, wi) => {
          if (wi) l.append(document.createTextNode(' '));
          const w = document.createElement('span');
          w.className = 'st-hero__word';
          for (const ch of word) {
            const s = document.createElement('span');
            s.className = 'st-hero__letter';
            s.textContent = ch;
            w.append(s);
          }
          l.append(w);
        });
        vis.append(l);
      });
      h.append(sr, vis);
      // v3.7.1: after a flight the bend runs in the next frame (the headline is fading in from 0), which splits the
      // commit into two shorter main-thread tasks.
      if (deferBend) { clearTimeout(this.bendT); requestAnimationFrame(() => { if (!this.destroyed) this.bendHeadline(); }); }
      else this.bendHeadline();
    }

    /** Bend each line on a convex-up arc (radius = --arc-r board px x k). Letter boxes lose kerning, so each letter
     *  first gets a margin that restores the plain-text (kerned) advance, measured with a Range on a probe. */
    bendHeadline() {
      const h = this.el.headline;
      if (!h || !h.isConnected) return;
      const cs = getComputedStyle(h);
      const k = Math.min(this.root.clientWidth / 390, this.root.clientHeight / 775) || 1;
      const R = (parseFloat(cs.getPropertyValue('--arc-r')) || 380) * k;
      const arc = h.querySelector('.st-hero__arc');
      const rot = h.style.rotate, scl = arc ? arc.style.scale : '';
      h.style.rotate = '0deg'; if (arc) arc.style.scale = '1'; // measure untransformed (CSS rotates the block, condenses the letters)
      h.querySelectorAll('.st-hero__line').forEach((line) => {
        const letters = [...line.querySelectorAll('.st-hero__letter')];
        letters.forEach((s) => { s.style.translate = ''; s.style.rotate = ''; s.style.marginLeft = ''; });
        if (!letters.length || !R) return;
        // Kerned advances from a plain-text probe (same font, same line).
        const text = line.textContent;
        const probe = document.createElement('span');
        probe.textContent = text;
        probe.style.cssText = 'position:absolute;left:0;top:0;white-space:pre;visibility:hidden;';
        line.append(probe);
        const node = probe.firstChild, range = document.createRange(), base = probe.getBoundingClientRect().left;
        const nat = [];
        for (let i = 0; i < text.length; i++) {
          if (/\s/.test(text[i])) continue;
          range.setStart(node, i); range.setEnd(node, i + 1);
          nat.push(range.getBoundingClientRect().left - base);
        }
        probe.remove();
        if (nat.length === letters.length) {
          const cur = letters.map((s) => s.offsetLeft);
          for (let i = 1; i < letters.length; i++) {
            const d = (nat[i] - nat[i - 1]) - (cur[i] - cur[i - 1]);
            if (Math.abs(d) > 0.2) letters[i].style.marginLeft = `${d.toFixed(2)}px`;
          }
        }
        // Letters' offsetParent is the absolutely positioned headline, so offsetLeft is already headline-local.
        const boxes = letters.map((s) => ({ s, x: s.offsetLeft + s.offsetWidth / 2 }));
        const xs = boxes.map((b) => b.x);
        const mid = (Math.min(...xs) + Math.max(...xs)) / 2;
        boxes.forEach(({ s, x }) => {
          const dx = Math.max(-R * 0.95, Math.min(R * 0.95, x - mid));
          s.style.translate = `0 ${(R - Math.sqrt(R * R - dx * dx)).toFixed(2)}px`;
          s.style.rotate = `${Math.asin(dx / R).toFixed(4)}rad`;
        });
      });
      h.style.rotate = rot; if (arc) arc.style.scale = scl;
    }

    async setTone(n, user) {
      const t = (this.data.tones || []).find((x) => Number(x.index) === n);
      this.tone = n;
      this.root.dataset.tone = String(n);
      if (t?.swatch) this.root.style.setProperty('--st-tone-swatch', t.swatch);
      if (this.el.tone) this.el.tone.setAttribute('aria-label', fill(this.labels.tone || 'Skin tone, Skin tone {n} of {count}', { n, count: this.toneCount }));
      if (!t?.src || !this.el.toneImg) return;
      if (user) {
        // Pre-decode to avoid a flash, but never let a slow/deferred decode (background tab, throttled pane) swallow the tap:
        // after 400 ms the src is swapped anyway and the browser keeps the old frame until the new one is ready. A real
        // decode error still leaves the current tone in place.
        const ok = await Promise.race([decode(t.src).then(() => true, () => false), new Promise((res) => setTimeout(() => res(true), 400))]);
        if (!ok) return;
      }
      if (this.tone !== n) return;
      if (this.el.toneImg.tagName === 'IMG') { this.el.toneImg.src = t.src; this.el.toneImg.removeAttribute('srcset'); }
      else this.el.toneImg.style.backgroundImage = `url("${t.src}")`;
    }

    enableControls() {
      [this.el.pause, this.el.tone, this.el.preview, this.el.mainBtn].forEach((b) => b && b.removeAttribute('aria-disabled'));
    }

    /* ---------- sequences ---------- */
    abortToStill() {
      this.gen++;
      this.anims.forEach((a) => a.cancel());
      this.anims.clear();
      this.clearFlyers();
      this.inFlight = false;
      this.renderSet(this.active, false);
    }

    onResizeDuringFlight() {
      const wasAuto = this.mode === 'auto';
      this.abortToStill();
      if (wasAuto) this.startPass(this.visited);
    }

    startPass(visited = 0) {
      if (REDUCED.matches) return;
      this.abortToStill();
      this.mode = 'auto';
      this.visited = visited || 1;
      this.syncControls();
      this.loop(this.gen).catch((e) => { if (e?.name !== 'AbortError') console.error('[st-hero]', e); });
    }

    async loop(gen) {
      while (gen === this.gen) {
        const last = this.visited >= MAX_SETS;
        await this.playSet(gen, !last);
        if (last) break;
        this.visited++;
      }
      if (gen === this.gen) { this.mode = 'settled'; this.syncControls(); }
    }

    async playSet(gen, withNext) {
      const c = this.campaigns[this.active];
      const cols = this.flightColumns(c);
      const [A, B] = cols;
      const sA = this.el.accents[0], sB = this.el.accents[1];
      await this.wait(T.sigHold);

      if (A != null && sA) {
        this.inFlight = true;
        await this.fly({ from: sA, to: this.el.main, sprite: c.sprite, col: A, duration: T.accentFlight });
        this.setNail(this.el.main, c.sprite, A);
        this.inFlight = false;
        await this.wait(T.accentHold);

        // Swap: A returns to its sample while B (or the signature) comes in.
        this.inFlight = true;
        const incoming = B != null && sB ? { from: sB, col: B } : null;
        const back = this.fly({ from: this.el.main, to: sA, sprite: c.sprite, col: A, duration: T.swapFlight, fadeTarget: false, hideFrom: false, lift: 0.25 });
        this.el.main.classList.add('is-hidden');
        const jobs = [back];
        if (incoming) jobs.push(this.fly({ from: incoming.from, to: this.el.main, sprite: c.sprite, col: incoming.col, duration: T.swapFlight, fadeTarget: false }));
        await Promise.all(jobs);
        this.setNail(sA, c.sprite, A);
        this.setNail(this.el.main, c.sprite, incoming ? incoming.col : 0);
        this.inFlight = false;
        await this.wait(T.swapHold);
        if (incoming) {
          // Return B to its sample so the sample row is complete before the next set arrives.
          this.inFlight = true;
          this.el.main.classList.add('is-hidden');
          await this.fly({ from: this.el.main, to: sB, sprite: c.sprite, col: B, duration: T.swapFlight, fadeTarget: false, hideFrom: false, lift: 0.25 });
          this.setNail(sB, c.sprite, B);
          this.setNail(this.el.main, c.sprite, 0);
          this.inFlight = false;
          await this.wait(T.accentHold);
        }
      } else {
        await this.wait(T.accentHold + T.swapHold);
      }

      if (!withNext) return;
      await this.nextFlight(gen, 1);
    }

    /** Fly the next set's signature from the preview hand to the finger, cross-fade the scene, commit. */
    async nextFlight(gen, direction) {
      const next = (this.active + direction + this.campaigns.length) % this.campaigns.length;
      const n = this.campaigns[next];
      try { await decode(n.sprite); } catch { throw abort(); }
      if (n.character?.src) {
        try { await decode(n.character.src); } catch { n.character = null; }
        if (n.character?.parts) n.character.parts = (await Promise.all(n.character.parts.map((p) => decode(p.src).then(() => p, () => null)))).filter(Boolean);
      }
      if (gen !== this.gen) throw abort();
      const current = this.campaigns[this.active];
      const slots = n.previewSlots || [0, 1, 2, 0];
      let slot = slots.indexOf(0); if (slot < 0) slot = 0;
      const source = this.el.previewNails[slot] || this.el.previewNails[0];
      this.inFlight = true;
      const jobs = [];
      if (this.el.scene) {
        this.el.scene.style.background = '';
        this.el.scene.dataset.key = n.key; // per-set glow lives in CSS (.st-hero__scene[data-key])
        jobs.push(this.run(this.el.scene, [{ opacity: 0 }, { opacity: 1 }], { duration: T.nextFlight, easing: 'ease-in-out' }));
      }
      const textOut = (el) => el && this.run(el, [{ opacity: 1 }, { opacity: 0 }], { duration: T.textFade, easing: 'ease-in' });
      if (direction > 0 && source) {
        jobs.push(this.fly({ from: source, to: this.el.main, sprite: n.sprite, col: 0, duration: T.nextFlight, lift: 0.3 }));
      } else {
        jobs.push(this.run(this.el.main, [{ opacity: 1 }, { opacity: 0 }], { duration: T.nextFlight / 2 }));
      }
      jobs.push((async () => {
        await Promise.all([textOut(this.el.headline), textOut(this.el.note)]);
        await this.wait(Math.max(0, T.nextFlight - 2 * T.textFade));
      })());
      if (this.el.character && !this.el.character.hidden) jobs.push(this.run(this.el.character, [{ opacity: 1 }, { opacity: 0 }], { duration: T.nextFlight / 2, easing: 'ease-in' }));
      jobs.push(this.run(this.el.accents[0] || this.clock, [{ opacity: 1 }, { opacity: 0 }], { duration: T.nextFlight / 2 }));
      jobs.push(this.run(this.el.accents[1] || this.clock, [{ opacity: 1 }, { opacity: 0 }], { duration: T.nextFlight / 2 }));
      await Promise.all(jobs);
      this.inFlight = false;
      this.renderSet(next, false, { deferBend: true });
      this.prefetch(next + 1);
      if (this.el.note) this.run(this.el.note, [{ opacity: 0 }, { opacity: 1 }], { duration: T.textFade }).catch(() => {});
      this.run(this.el.headline, [{ opacity: 0 }, { opacity: 1 }], { duration: T.textFade }).catch(() => {});
      if (this.el.character && !this.el.character.hidden) this.run(this.el.character, [{ opacity: 0 }, { opacity: 1 }], { duration: T.nextFlight / 2, easing: 'ease-out' }).catch(() => {});
      void current;
    }

    async manualStep(direction) {
      if (this.busy) return;
      this.busy = true;
      try {
        const was = this.mode;
        this.abortToStill();
        this.mode = 'manual';
        this.reasons.delete('user');
        this.syncControls();
        const gen = this.gen;
        if (REDUCED.matches || direction < 0) {
          const next = (this.active + direction + this.campaigns.length) % this.campaigns.length;
          try { await decode(this.campaigns[next].sprite); } catch { return; }
          if (gen !== this.gen) return;
          this.renderSet(next, true);
        } else {
          await this.nextFlight(gen, 1);
          if (this.el.status) this.el.status.textContent = fill(this.labels.announce || '{name}. {headline}', this.campaigns[this.active]);
        }
        void was;
      } catch (e) {
        if (e?.name !== 'AbortError') console.error('[st-hero]', e);
      } finally {
        this.busy = false;
        this.syncControls();
      }
    }
  }

  const abort = () => Object.assign(new Error('aborted'), { name: 'AbortError' });

  const upgrade = (scope) => {
    (scope.matches?.(ROOT) ? [scope] : [...scope.querySelectorAll(ROOT)]).forEach((root) => {
      if (controllers.has(root)) return;
      const c = new HeroMotion(root);
      if (c.data) controllers.set(root, c);
    });
  };
  const teardown = (scope) => {
    (scope.matches?.(ROOT) ? [scope] : [...scope.querySelectorAll(ROOT)]).forEach((root) => {
      controllers.get(root)?.destroy();
      controllers.delete(root);
    });
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', () => upgrade(document), { once: true });
  else upgrade(document);
  document.addEventListener('shopify:section:load', (e) => upgrade(e.target));
  document.addEventListener('shopify:section:unload', (e) => teardown(e.target));
  window.STHeroMotion = { upgrade, teardown, controllers };
})();
