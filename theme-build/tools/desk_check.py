"""Desktop chapters check (st-fable's CHAPTERS-DESKTOP-SPEC §3) on lab/landing.html, or on the preview with --preview
(scrolling .page-wrapper, Horizon's scroller at >= 990). Per chapter at 1280x720, 1366x768, 1440x800, 1536x703 and
1000x700 (the 990-1023 fix-2 band): the chapter's own height vs the screen under the header; the copy's top / bottom
margins (>= 24); art vs copy (no overlap; right pieces >= 16 px from the copy's boxes); cut edges only on section edges;
section joins (each section starts where the previous chapter's own height ends) and horizontal overflow; page errors.
Shots: lab/shots/desk-<w>x<h>-<key>.png (or qa/fidelity/<prefix>-... with --preview), the chapter's top at the header.
Usage: python -I tools/desk_check.py [--preview <prefix>] [WxH ...]"""
import asyncio, json, pathlib, sys, time
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
TB = pathlib.Path(__file__).resolve().parents[1]
PREVIEW = '--preview' in sys.argv
PREFIX = sys.argv[sys.argv.index('--preview') + 1] if PREVIEW else 'desk'
OUT = (TB.parent / 'qa/fidelity') if PREVIEW else (TB / 'lab/shots')
URL = 'https://0nev20-vn.myshopify.com/?preview_theme_id=186651934933' if PREVIEW else (TB / 'lab/landing.html').as_uri()
VIEWS = [tuple(int(v) for v in x.split('x')) for x in sys.argv[1:] if 'x' in x and x[0].isdigit()] or     [(1280, 720), (1366, 768), (1440, 800), (1536, 703), (1024, 768), (1000, 700)]
CHAPTERS = ['diet-cherry', 'brainwave', 'green-flag', 'shaadi-shift', 'on-me', 'wild-card', 'pinky-promise']

HELPERS = """window.__sc = () => { const w = document.querySelector('.page-wrapper');
  return w && /(auto|scroll)/.test(getComputedStyle(w).overflowY) && w.scrollHeight > w.clientHeight + 2 ? w : null; };
window.__sy = () => { const w = window.__sc(); return w ? w.scrollTop - w.getBoundingClientRect().top : scrollY; };
window.__st = (y) => { const w = window.__sc(); if (w) w.scrollTop = y; else window.scrollTo(0, y); };"""

MEASURE = """(key) => {
  const s = document.querySelector(`.st-ch[data-land="${key}"]`); const r = s.getBoundingClientRect(); const W = r.width;
  const px = (v) => { const d = document.createElement('div'); d.style.cssText = `position:absolute;height:calc(${v})`; s.appendChild(d); const h = d.getBoundingClientRect().height; d.remove(); return h; };
  const hc = px('var(--hc)'), c = px('var(--c) * var(--kt, var(--k))');
  const kr = px('var(--kr, 0px) * 1000') / 1000, ka = px('var(--ka, 0px) * 1000') / 1000, cxs = px('var(--cxs, 0px)');
  const B = (e) => { if (!e) return null; const b = e.getBoundingClientRect(); return b.width && b.height ? { l: b.left - r.left, t: b.top - r.top, r: b.right - r.left, b: b.bottom - r.top } : null; };
  const U = (els) => { const bs = els.map(B).filter(Boolean); return bs.length ? { l: Math.min(...bs.map(x => x.l)), t: Math.min(...bs.map(x => x.t)), r: Math.max(...bs.map(x => x.r)), b: Math.max(...bs.map(x => x.b)) } : null; };
  const copy = { note: B(s.querySelector('.st-ch__note')), head: U([...s.querySelectorAll('.st-ch__headline text')]), nails: U([...s.querySelectorAll('.st-ch__nail')]),
                 name: B(s.querySelector('.st-ch__name')), pill: B(s.querySelector('.st-ch__pill')), cap: B(s.querySelector('.st-ch__caption')) };
  const cb = Object.values(copy).filter(Boolean);
  const top = Math.min(...cb.map(b => b.t)), bot = Math.max(...cb.map(b => b.b));
  const arts = [...s.querySelectorAll('.st-land__art')].filter(a => getComputedStyle(a).display !== 'none').map(a => {
    const b = B(a.querySelector('img')); const cls = a.className;
    const kind = cls.includes('--r') ? 'r' : cls.includes('--f') ? 'f' : 'l';
    const dtop = cls.includes('--dtop'), dsz = cls.includes('--dsz');
    // owner v1.2: groups may hang from either edge (RIGHT / SPLIT layouts): the side is read from the geometry
    const side = b.l <= 1 ? 'left' : (b.r >= W - 2 ? 'right' : 'mid');
    const fadedBottom = /to top/.test(getComputedStyle(a).maskImage || getComputedStyle(a).webkitMaskImage || '');
    const near = Math.min(...cb.map(x => Math.max(x.l - b.r, b.l - x.r, x.t - b.b, b.t - x.b)));
    return { name: a.querySelector('img').src.split('/').pop().split('?')[0].replace('st-hd-', '').replace('.webp', '').replace('.web', ''), kind, dtop, dsz, side, fadedBottom,
             l: Math.round(b.l), r: Math.round(b.r), t: Math.round(b.t), b: Math.round(b.b), near: Math.round(near * 10) / 10 };
  });
  const R = Math.round;
  return { kr, ka, cxs: R(cxs), hc: R(hc), cap: R(c), W: R(W), top: R(r.top + window.__sy()), height: R(r.height), copyTop: R(top), copyBot: R(bot), arts,
           hiddenBee: [...s.querySelectorAll('.st-land__beeline')].every(e => getComputedStyle(e).display === 'none') };
}"""


async def main():
    rep = {}
    async with async_playwright() as p:
        br = await p.chromium.launch(channel='chrome')
        for w, h in VIEWS:
            pg = await br.new_page(viewport={'width': w, 'height': h})
            errs = []
            pg.on('pageerror', lambda e: errs.append(str(e)[:120]))
            await pg.goto(URL + (f'&_cb={time.time_ns()}' if PREVIEW else ''), wait_until='load', timeout=120000)
            await pg.add_style_tag(content='[id^="PBar"], #preview-bar-iframe { display: none !important; } html, body, .page-wrapper { scroll-behavior: auto !important; }')
            await pg.evaluate(HELPERS)
            await pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager')")
            for y in range(0, 20000, 600):
                await pg.evaluate(f'window.__st({y})'); await pg.wait_for_timeout(30)
            await pg.evaluate('Promise.race([Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; }))), new Promise(r => setTimeout(r, 5000))])')
            hdr = await pg.evaluate("(() => { const e = document.querySelector('.st-header, .lab-header'); return e ? Math.round(e.getBoundingClientRect().height) : 0; })()")
            screen = h - hdr
            rows = {}
            prev_end = None
            for key in CHAPTERS:
                m = await pg.evaluate(MEASURE, key)
                m['screen'] = screen
                issues = []
                if w >= 1024 and abs(m['hc'] - min(screen, 900)) > 1:
                    issues.append(f"height {m['hc']} vs screen {min(screen, 900)}")
                if w >= 1024 and (m['copyTop'] < 24 or m['hc'] - m['copyBot'] < 24):
                    issues.append(f"copy margins {m['copyTop']}/{m['hc'] - m['copyBot']}")
                for a in m['arts']:
                    if w >= 1024:
                        if a['near'] < (16 if a['kind'] == 'r' else 0):
                            issues.append(f"{a['name']} {a['near']} px from copy")
                        if a['kind'] == 'l' and a['side'] == 'mid':
                            issues.append(f"{a['name']} cut mid-screen ({a['l']}..{a['r']})")
                        if a['kind'] == 'r' and a['r'] < m['W'] - 1:
                            issues.append(f"{a['name']} right cut at {a['r']}")
                        # v1.1: the top-cut piece hangs from the section top; bottom-cut pieces reach the chapter's end
                        if a['dtop'] and a['t'] > 1:
                            issues.append(f"{a['name']} top cut at {a['t']}")
                        if (a['dsz'] or 'v12r' in a.get('cls', '')) and not a['dtop'] and not a['fadedBottom'] and a['kind'] == 'l' and a['b'] < m['hc'] - 1:
                            issues.append(f"{a['name']} ends at {a['b']} above the chapter end {m['hc']}")
                        if a['kind'] != 'r' and 0 <= a['near'] < 25:
                            issues.append(f"(warn) {a['name']} {a['near']} px from copy")
                rows[key] = dict(m, issues=issues)
                await pg.evaluate(f"window.__st({m['top'] - hdr})")
                await pg.wait_for_timeout(250)
                await pg.screenshot(path=str(OUT / f'{PREFIX}-{w}x{h}-{key}.png'))
                art = '  '.join(f"{a['name'][:14]}:{a['kind']} {a['l']}..{a['r']} near {a['near']}" for a in m['arts'])
                kk = f"ka {m['ka']:.3f} kr {m['kr']:.3f} cxs {m['cxs']}" if any(a['kind'] == 'r' for a in m['arts']) and w >= 1024 else ''
                hard = [i for i in issues if not i.startswith('(warn)')]
                print(f"{w}x{h} {key:14} {'OK' if not hard else 'XX'}  h {m['hc']}/{min(screen, 900)}  copy {m['copyTop']}-{m['copyBot']}  bee hidden {m['hiddenBee']}  {art}  {kk}  {issues or ''}")
            joins = await pg.evaluate("""(() => { const ss = [...document.querySelectorAll('.st-land')]; const out = [];
              for (let i = 1; i < ss.length; i++) { const a = ss[i - 1], b = ss[i];
                const d = document.createElement('div'); d.style.cssText = 'position:absolute;height:calc(var(--nc) * var(--kt, var(--k)))'; a.appendChild(d); const nc = d.getBoundingClientRect().height; d.remove();
                out.push(Math.round(b.getBoundingClientRect().top - (a.getBoundingClientRect().bottom - nc))); }
              return out; })()""")
            ovx = await pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
            print(f"{w}x{h} joins (next top - previous own end, px): {joins}  h-overflow {ovx}  errors {errs or 'none'}")
            rep[f'{w}x{h}'] = dict(rows=rows, joins=joins, overflow=ovx, errors=errs)
            await pg.close()
        await br.close()
    (OUT / f'{PREFIX}-measurements.json').write_text(json.dumps(rep, indent=1), encoding='utf-8')


asyncio.run(main())
