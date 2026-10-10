"""Talks + Journal teasers (STORE-DESKTOP-SPEC v1.1 §1a/§1b) on lab/landing.html, or on the preview with --preview:
per size, each teaser's own height (box minus the next section's cap), its content's last bottom (in board px and px),
the room left above the next cap, the beeline's nearest distance to any content box (phones; >= 8), font sizes of the
key elements, and whether the CTA / pill sit inside the first screen at >= 1024 (section top at the header).
Shots: lab/shots/teaser-<w>x<h>-<key>.png (qa/fidelity/<prefix>-... with --preview).
Usage: python -I tools/teaser_check.py [--preview <prefix>] [WxH ...]"""
import asyncio, json, pathlib, sys, time
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
TB = pathlib.Path(__file__).resolve().parents[1]
ARGS = sys.argv[1:]
PREVIEW = '--preview' in ARGS
PREFIX = ARGS[ARGS.index('--preview') + 1] if PREVIEW else 'teaser'
SIZES = [tuple(int(v) for v in a.split('x')) for a in ARGS if 'x' in a and a[0].isdigit()] or \
    [(390, 844), (390, 664), (430, 932), (320, 568), (1000, 700), (1280, 720), (1366, 768), (1440, 800), (1536, 703)]
OUT = (TB.parent / 'qa/fidelity') if PREVIEW else (TB / 'lab/shots')
URL = 'https://0nev20-vn.myshopify.com/?preview_theme_id=186651934933' if PREVIEW else (TB / 'lab/landing.html').as_uri()

HELPERS = """window.__sc = () => { const w = document.querySelector('.page-wrapper');
  return w && /(auto|scroll)/.test(getComputedStyle(w).overflowY) && w.scrollHeight > w.clientHeight + 2 ? w : null; };
window.__sy = () => { const w = window.__sc(); return w ? w.scrollTop - w.getBoundingClientRect().top : scrollY; };
window.__st = (y) => { const w = window.__sc(); if (w) w.scrollTop = y; else window.scrollTo(0, y); };"""

MEASURE = """(key) => {
  const s = document.querySelector(`.st-land[data-land="${key}"]`); if (!s) return null;
  const r = s.getBoundingClientRect();
  const px = (v) => { const d = document.createElement('div'); d.style.cssText = `position:absolute;height:calc(${v})`; s.appendChild(d); const h = d.getBoundingClientRect().height; d.remove(); return h; };
  const k = px('var(--k)'), nc = px('var(--nc) * var(--kt, var(--k))');
  const vis = (e) => { const cs = getComputedStyle(e); return cs.display !== 'none' && cs.visibility !== 'hidden'; };
  const els = [...s.querySelectorAll('h2, p, a, li, img, .st-tt__board, .st-jt__card, .st-tavatar')].filter(e => vis(e) && !e.closest('.st-land__beeline'));
  const boxes = els.map(e => e.getBoundingClientRect()).filter(b => b.width > 1 && b.height > 1);
  const bottom = Math.max(...boxes.map(b => b.bottom)) - r.top;
  const own = r.height - nc;
  let bee = null;
  const path = s.querySelector('.st-land__beeline path');
  if (path && vis(path.closest('svg'))) {
    const svg = path.closest('svg'), m = svg.getScreenCTM(); const L = path.getTotalLength(); bee = 1e9;
    for (let i = 0; i <= 300; i++) { const q = path.getPointAtLength(L * i / 300); const x = m.a * q.x + m.c * q.y + m.e, y = m.b * q.x + m.d * q.y + m.f;
      for (const b of boxes) { const dx = Math.max(b.left - x, 0, x - b.right), dy = Math.max(b.top - y, 0, y - b.bottom); bee = Math.min(bee, Math.hypot(dx, dy)); } }
  }
  const fs = (sel) => { const e = s.querySelector(sel); return e && vis(e) ? Math.round(parseFloat(getComputedStyle(e).fontSize) * 10) / 10 : null; };
  const cta = s.querySelector('.st-tt__cta, .st-jt__pill'); const cb = cta && cta.getBoundingClientRect();
  const rows = [...s.querySelectorAll('.st-tt__row')].filter(vis).length;
  return { k: Math.round(k * 1000) / 1000, own: Math.round(own), bottom: Math.round(bottom), room: Math.round(own - bottom), bee: bee === null ? null : Math.round(bee * 10) / 10,
           top: Math.round(r.top + window.__sy()), ctaBottom: cb ? Math.round(cb.bottom - r.top) : null, rows,
           fs: { h: fs('.st-tt__h, .st-jt__h'), hl: fs('.st-tt__hl'), sup: fs('.st-tt__sup'), title: fs('.st-tt__title'), reply: fs('.st-tt__reply'), cta: fs('.st-tt__cta, .st-jt__pill'), note: fs('.st-jt__note') } };
}"""


async def main():
    rep = {}
    async with async_playwright() as p:
        br = await p.chromium.launch(channel='chrome')
        for w, h in SIZES:
            pg = await br.new_page(viewport={'width': w, 'height': h})
            errs = []
            pg.on('pageerror', lambda e: errs.append(str(e)[:120]))
            await pg.goto(URL + (f'&_cb={time.time_ns()}' if PREVIEW else ''), wait_until='load', timeout=120000)
            await pg.add_style_tag(content='[id^="PBar"], #preview-bar-iframe { display: none !important; } html, body, .page-wrapper { scroll-behavior: auto !important; }')
            await pg.evaluate(HELPERS)
            await pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager')")
            await pg.evaluate('document.fonts.ready')
            for y in range(0, 20000, 700):
                await pg.evaluate(f'window.__st({y})'); await pg.wait_for_timeout(25)
            await pg.wait_for_timeout(600)
            hdr = await pg.evaluate("(() => { const e = document.querySelector('.st-header, .lab-header'); return e ? Math.round(e.getBoundingClientRect().height) : 0; })()")
            for key in ('talks-teaser', 'journal-teaser'):
                m = await pg.evaluate(MEASURE, key)
                if not m:
                    print(w, h, key, 'missing'); continue
                await pg.evaluate(f"window.__st({m['top'] - hdr})")
                await pg.wait_for_timeout(250)
                await pg.screenshot(path=str(OUT / f'{PREFIX}-{w}x{h}-{key}.png'))
                fold = (h - hdr) if w >= 1024 else None
                above = (m['ctaBottom'] <= fold) if fold else None
                print(f"{w}x{h} {key:15} k {m['k']}  own {m['own']}  content bottom {m['bottom']}  room {m['room']}  bee {m['bee']}  rows {m['rows']}  "
                      f"cta bottom {m['ctaBottom']}{'' if fold is None else (' (above fold)' if above else ' (BELOW FOLD)')}  fs {m['fs']}")
                rep[f'{w}x{h}/{key}'] = m
            print(f'{w}x{h} errors {errs or "none"}')
            await pg.close()
        await br.close()
    (OUT / f'{PREFIX}-measurements.json').write_text(json.dumps(rep, indent=1), encoding='utf-8')


asyncio.run(main())
