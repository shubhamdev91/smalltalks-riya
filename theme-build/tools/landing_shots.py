"""Landing redesign BEFORE / AFTER pass (read-only): home at 440x956, 430x932, 390x844, the Safari small-viewport
heights 440x830, 430x806, 390x718, and 1280x800. Per viewport: the hero at scroll 0 and each product chapter scrolled
so its own content top sits under the (sticky) header, as viewport shots qa/fidelity/<prefix>-<w>x<h>-<key>.png; and
per chapter the content span = top of the campaign body (note) to the bottom of the Shop pill / art (art clipped at
the chapter's end), vs the screen left under the header. Writes qa/fidelity/<prefix>-measurements.json and .md.
Usage: python -I tools/landing_shots.py <prefix> [css_override_path]
  css_override_path: serve this file for assets/st-landing.css (local staging preview; markup stays the preview's)."""
import asyncio, json, pathlib, sys, time
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
TB = pathlib.Path(__file__).resolve().parents[1]
QA = TB.parent / 'qa/fidelity'
O = 'https://0nev20-vn.myshopify.com'
Q = 'preview_theme_id=186651934933'
PREFIX = sys.argv[1] if len(sys.argv) > 1 else 'before-landing-redesign'
CSS = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else None
VIEWS = [tuple(int(x) for x in v.split('x')) for v in __import__('os').environ.get('ST_VIEWS', '').split(',') if v] or [(440, 956), (430, 932), (390, 844), (440, 830), (430, 806), (390, 718), (1280, 800)]
CHAPTERS = ['diet-cherry', 'brainwave', 'green-flag', 'shaadi-shift', 'on-me', 'wild-card', 'pinky-promise']

SCROLLER = """window.__stScroller = () => { const w = document.querySelector('.page-wrapper');
  return w && /(auto|scroll)/.test(getComputedStyle(w).overflowY) && w.scrollHeight > w.clientHeight + 2 ? w : null; };
window.__stScrollY = () => { const w = window.__stScroller(); return w ? w.scrollTop - w.getBoundingClientRect().top : scrollY; };
window.__stScrollTo = (y) => { const w = window.__stScroller(); if (w) w.scrollTop = y; else window.scrollTo(0, y); };"""

MEASURE = """(key) => {
  const s = document.querySelector(`.st-ch[data-land="${key}"]`); if (!s) return null;
  const cs = getComputedStyle(s), k = parseFloat(getComputedStyle(s).getPropertyValue('--k')) || null;
  const r = s.getBoundingClientRect(), top = r.top + window.__stScrollY();
  const px = (v) => { const d = document.createElement('div'); d.style.cssText = `position:absolute;height:calc(${v})`; s.appendChild(d); const h = d.getBoundingClientRect().height; d.remove(); return h; };
  const kk = px('var(--k)'), c = px('var(--c) * var(--k)'), h = px('var(--hc, calc(var(--h) * var(--k)))');
  const box = (sel) => [...s.querySelectorAll(sel)].map(e => e.getBoundingClientRect()).filter(b => b.width && b.height);
  const note = box('.st-ch__note')[0], head = box('.st-ch__headline')[0], pill = box('.st-ch__pill')[0], name = box('.st-ch__name')[0],
        nails = box('.st-ch__nails')[0], cap = box('.st-ch__caption')[0];
  const end = r.top + h;  // the chapter's own end (the next section's cap starts here)
  const arts = box('.st-land__art img').map(b => ({ top: Math.max(b.top, r.top + c), bottom: Math.min(b.bottom, end) })).filter(b => b.bottom > b.top);
  const artBottom = arts.length ? Math.max(...arts.map(a => a.bottom)) : null;
  const artTop = arts.length ? Math.min(...arts.map(a => a.top)) : null;
  const bodyTop = note ? note.top : head.top;
  const copyBottom = Math.max(pill ? pill.bottom : 0, name ? name.bottom : 0, cap ? cap.bottom : 0);
  const contentBottom = Math.max(copyBottom, artBottom || 0);
  const R = (v) => v == null ? null : Math.round(v);
  return { k: Math.round(kk * 1000) / 1000, sectionTop: R(top), cap: R(c), chapter: R(h), noteTop: R(bodyTop - r.top), pillBottom: R((pill ? pill.bottom : copyBottom) - r.top),
           artTop: R(artTop == null ? null : artTop - r.top), artBottom: R(artBottom == null ? null : artBottom - r.top),
           copySpan: R(copyBottom - bodyTop), contentSpan: R(contentBottom - bodyTop), fromCapToContentEnd: R(contentBottom - (r.top + c)),
           noteFs: note ? parseFloat(getComputedStyle(s.querySelector('.st-ch__note')).fontSize) : null,
           nameFs: name ? parseFloat(getComputedStyle(s.querySelector('.st-ch__name')).fontSize) : null };
}"""


async def settle(pg):
    await pg.add_style_tag(content='[id^="PBar"], #preview-bar-iframe { display: none !important; }')
    await pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager')")
    await pg.evaluate(SCROLLER)
    for y in range(0, 16000, 500):
        if not await pg.evaluate(f'(window.__stScrollTo({y}), {y} < (window.__stScroller() || document.documentElement).scrollHeight)'):
            break
        await pg.wait_for_timeout(60)
    await pg.evaluate('window.__stScrollTo(0)')
    await pg.evaluate('Promise.race([Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; }))), new Promise(r => setTimeout(r, 5000))])')
    await pg.wait_for_timeout(1200)


async def header_bottom(pg):
    return await pg.evaluate("(() => { const h = document.querySelector('.st-header'); if (!h) return 0; const b = h.getBoundingClientRect(); return b.bottom > 0 && getComputedStyle(h).visibility !== 'hidden' ? Math.round(b.bottom) : 0; })()")


LIQ, PHASES = [], []


async def main():
    out = {}
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        errs = []
        for w, h in VIEWS:
            ctx = await b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=2)
            pg = await ctx.new_page()
            pg.on('pageerror', lambda e: errs.append(f'{w}x{h} PAGEERROR ' + str(e)[:150]))
            if CSS:
                body = CSS.read_bytes()
                await pg.route('**/st-landing.css*', lambda r: r.fulfill(status=200, content_type='text/css', body=body))
            await pg.goto(f'{O}/?{Q}&_cb={time.time_ns()}', wait_until='load', timeout=120000)
            await settle(pg)
            html = await pg.content()
            LIQ.extend(f'{w}x{h} {x}' for x in ('Liquid error', 'translation missing') if x in html)
            bad = await pg.evaluate("""(() => { let run = 0, bad = []; document.querySelectorAll('.st-land__beeline path').forEach((p, i) => {
              const off = parseFloat(p.style.strokeDashoffset || p.getAttribute('stroke-dashoffset') || 0); const want = -(run % 14.5);
              if (Math.abs(off - want) > 0.05) bad.push([i, off, want]); run += p.getTotalLength(); }); return bad; })()""")
            if bad:
                PHASES.append((f'{w}x{h}', bad))
            tag = f'{w}x{h}'
            await pg.screenshot(path=str(QA / f'{PREFIX}-{tag}-hero.png'))
            rows = {}
            for key in CHAPTERS:
                m = await pg.evaluate(MEASURE, key)
                if not m:
                    print(tag, key, 'missing'); continue
                hb0 = await header_bottom(pg)
                top_in = min(m['cap'], m['noteTop'] - 6)  # the cap or the note's top, whichever is higher
                target = m['sectionTop'] + top_in - (hb0 or 69)
                await pg.evaluate(f'window.__stScrollTo({target})')
                await pg.wait_for_timeout(700)
                hb = await header_bottom(pg)
                if hb == 0:  # header hides on scroll-down: align the chapter's content top with the viewport top instead
                    await pg.evaluate(f'window.__stScrollTo({m["sectionTop"] + top_in})')
                    await pg.wait_for_timeout(500)
                    hb = await header_bottom(pg)
                await pg.wait_for_timeout(300)
                await pg.screenshot(path=str(QA / f'{PREFIX}-{tag}-{key}.png'))
                m['header'] = hb
                m['screenBelowHeader'] = h - hb
                m['fits'] = m['contentSpan'] <= h - hb
                m['over'] = m['contentSpan'] - (h - hb)
                rows[key] = m
                print(tag, key, json.dumps({x: m[x] for x in ('k', 'chapter', 'noteTop', 'copySpan', 'contentSpan', 'header', 'screenBelowHeader', 'over', 'noteFs', 'nameFs')}))
            out[tag] = rows
            await ctx.close()
        await b.close()
    (QA / f'{PREFIX}-measurements.json').write_text(json.dumps(out, indent=1), encoding='utf-8')
    md = [f'# {PREFIX}: chapter content spans (css px)', '',
          'contentSpan = top of the campaign body (note) to the bottom of the Shop pill / art (art clipped at the chapter end);',
          'screen = viewport height minus the visible sticky header; over = contentSpan - screen (> 0: does not fit).', '']
    for tag, rows in out.items():
        md += [f'## {tag}', '', '| chapter | k | chapter h | copy span | content span | screen | over |', '|---|---|---|---|---|---|---|']
        for key, m in rows.items():
            md.append(f"| {key} | {m['k']} | {m['chapter']} | {m['copySpan']} | {m['contentSpan']} | {m['screenBelowHeader']} | {m['over']} |")
        md.append('')
    (QA / f'{PREFIX}-measurements.md').write_text('\n'.join(md), encoding='utf-8')
    print('errors', errs or 'none')
    print('liquid', LIQ or 'clean', '| beeline dash phase', PHASES or 'continuous')


asyncio.run(main())
