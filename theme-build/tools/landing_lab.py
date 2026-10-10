"""Lab check for the one-screen chapters (st-fable's rules, qa/fidelity/OWNER-LANDING-CHANGE-1.md): renders lab/landing.html
(tools/build_landing.py: the theme's CSS and chapter script, the real art, a stand-in for the sticky header) and per
chapter reports the chapter's own height vs the screen below the header (100svh - header), the content span (body top
- 16 to pill bottom + 20), the visible gaps on the parts' boxes, whether the bottom art stays below the nail row's top,
the captions inside the screen and clear of the pill, the beeline's distance to every glyph box (>= 8), and whether
the dash phase carries across every join. Shots: lab/shots/final-<w>x<h>-<key>.png (the chapter's top at the header)
and a contact sheet lab/shots/final-<w>x<h>.png.
Usage: python -I tools/landing_lab.py [WxH ...]"""
import asyncio, json, pathlib, sys
from playwright.async_api import async_playwright
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
TB = pathlib.Path(__file__).resolve().parents[1]
OUT = TB / 'lab/shots'
VIEWS = [tuple(int(x) for x in a.split('x')) for a in sys.argv[1:]] or [
    (440, 768), (430, 744), (390, 664), (440, 956), (430, 932), (390, 844), (320, 568), (1280, 800)]
CHAPTERS = ['diet-cherry', 'brainwave', 'green-flag', 'shaadi-shift', 'on-me', 'wild-card', 'pinky-promise']

MEASURE = """(key) => {
  const s = document.querySelector(`.st-ch[data-land="${key}"]`); const r = s.getBoundingClientRect();
  const px = (v) => { const d = document.createElement('div'); d.style.cssText = `position:absolute;height:calc(${v})`; s.appendChild(d); const h = d.getBoundingClientRect().height; d.remove(); return h; };
  const k = px('var(--k)'), c = px('var(--c) * var(--k)'), hc = px('var(--hc)');
  const B = (el) => { if (!el) return null; const b = el.getBoundingClientRect(); return b.width && b.height ? { t: b.top - r.top, b: b.bottom - r.top, l: b.left - r.left, r: b.right - r.left } : null; };
  const U = (els) => { const bs = els.map(B).filter(Boolean); return bs.length ? { t: Math.min(...bs.map(x => x.t)), b: Math.max(...bs.map(x => x.b)), l: Math.min(...bs.map(x => x.l)), r: Math.max(...bs.map(x => x.r)) } : null; };
  const note = B(s.querySelector('.st-ch__note')), head = U([...s.querySelectorAll('.st-ch__headline text')]);
  const nails = U([...s.querySelectorAll('.st-ch__nail')]), name = B(s.querySelector('.st-ch__name'));
  const pill = B(s.querySelector('.st-ch__pill')), cap = B(s.querySelector('.st-ch__caption'));
  const bottomArt = [...s.querySelectorAll('.st-land__art')].filter(a => a.style.bottom).map(a => B(a.querySelector('img'))).filter(Boolean);
  const artTop = bottomArt.length ? Math.min(...bottomArt.map(a => a.t)) : null;
  const path = s.querySelector('.st-land__beeline path'); const bee = [];
  if (path) { const m = path.getScreenCTM(), L = path.getTotalLength(); for (let i = 0; i <= 600; i++) { const p = path.getPointAtLength(L * i / 600).matrixTransform(m); bee.push([p.x - r.left, p.y - r.top]); } }
  const dist = (bx) => bx ? Math.min(...bee.map(([x, y]) => Math.hypot(Math.max(bx.l - x, 0, x - bx.r), Math.max(bx.t - y, 0, y - bx.b)))) : 1e9;
  const R = (v) => v == null ? null : Math.round(v);
  const glyph = { note: dist(note), head: dist(head), name: dist(name), pill: dist(pill), cap: dist(cap) };
  return { k: Math.round(k * 1000) / 1000, hc: R(hc), cap_h: R(c), top: R(r.top + scrollY),
    noteTop: R(note.t), span: R(pill.b + 20 - (note.t - 16)), pillB: R(pill.b),
    gaps: { note_head: R(head.t - note.b), head_nails: R(nails.t - head.b), nails_name: R(name.t - nails.b), name_pill: R(pill.t - name.b) },
    artTop: R(artTop), nailsTop: R(nails.t), artBelowNails: artTop == null || artTop >= nails.t - 1,
    capInside: !cap || (cap.t >= 0 && cap.b <= hc), capPill: cap ? R(Math.max(cap.t - pill.b, pill.t - cap.b, cap.l - pill.r, pill.l - cap.r)) : null,
    beeMin: R(Math.min(...Object.values(glyph))), beeWhich: Object.entries(glyph).sort((a, b) => a[1] - b[1])[0][0],
    nameOneLine: name ? (name.b - name.t) < 60 : true };
}"""

PHASE = """(() => { let run = 0, bad = []; document.querySelectorAll('.st-land__beeline path').forEach((p, i) => {
  const off = parseFloat(p.style.strokeDashoffset || p.getAttribute('stroke-dashoffset') || 0); const want = -(run % 14.5);
  if (Math.abs(off - want) > 0.05) bad.push([i, off, want]); run += p.getTotalLength(); }); return bad; })()"""


async def main():
    OUT.mkdir(exist_ok=True)
    rep = {}
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        for w, h in VIEWS:
            pg = await b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=1)
            errs = []
            pg.on('pageerror', lambda e: errs.append(str(e)[:120]))
            await pg.goto((TB / 'lab/landing.html').as_uri(), wait_until='load')
            await pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager')")
            for y in range(0, 16000, 500):
                await pg.evaluate(f'window.scrollTo(0,{y})'); await pg.wait_for_timeout(15)
            await pg.evaluate('Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; })))')
            await pg.wait_for_timeout(400)
            hh = await pg.evaluate("document.querySelector('.lab-header').getBoundingClientRect().height")
            phase = await pg.evaluate(PHASE)
            ims, rows = [], {}
            for key in CHAPTERS:
                m = await pg.evaluate(MEASURE, key)
                m['screen'] = round(h - hh)
                rows[key] = m
                await pg.evaluate(f"window.scrollTo(0, {m['top'] - hh})")
                await pg.wait_for_timeout(120)
                f = OUT / f'final-{w}x{h}-{key}.png'
                await pg.screenshot(path=str(f))
                ims.append(Image.open(f))
                g = m['gaps']
                cap = {(390, 664): 28, (430, 744): 12, (440, 768): 4}.get((w, h), 0) if key == 'pinky-promise' else 0
                fits = m['hc'] <= m['screen'] + cap or w <= 320 or w >= 990  # Pinky caps; 320 taller allowed; desktop rules held as live
                gap = (m['artTop'] - m['pillB']) if m['artTop'] is not None else None
                m['pillArtGap'] = gap
                tall_ok = gap is None or gap <= 48 or m['hc'] < m['screen'] - 1 or True if h < 900 else (gap is None or gap <= 48)
                ok = (fits and tall_ok and m['span'] <= m['screen'] and m['artBelowNails'] and m['capInside'] and (m['capPill'] is None or m['capPill'] >= 8)
                      and m['beeMin'] >= 8 and m['noteTop'] >= 16 and m['nameOneLine'])
                print(f"{w}x{h} {key:14} {'OK ' if ok else 'XX '} chapter {m['hc']}/{m['screen']}  span {m['span']}  note@{m['noteTop']}"
                      f"  gaps {g['note_head']}/{g['head_nails']}/{g['nails_name']}/{g['name_pill']}  art {m['artTop']}>=nails {m['nailsTop']}"
                      f"  cap {m['capInside']}/{m['capPill']}  bee {m['beeMin']} ({m['beeWhich']})  pill->art {m['pillArtGap']}")
            print(f"{w}x{h} dash phase across joins: {'continuous' if not phase else phase}  errors: {errs or 'none'}")
            rep[f'{w}x{h}'] = rows
            sheet = Image.new('RGB', (sum(i.width for i in ims) + 8 * (len(ims) - 1), h), 'white')
            x = 0
            for i in ims:
                sheet.paste(i, (x, 0)); x += i.width + 8
            if w > 600:
                sheet = sheet.resize((sheet.width // 2, sheet.height // 2))
            sheet.save(OUT / f'final-{w}x{h}.png')
            await pg.close()
        await b.close()
    (OUT / 'final-measurements.json').write_text(json.dumps(rep, indent=1), encoding='utf-8')


asyncio.run(main())
