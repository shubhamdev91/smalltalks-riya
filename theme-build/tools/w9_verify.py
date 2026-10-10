"""Brainwave + Shaadi Shift HD-box follow-up: at 390 (3x) the shop tiles (all 7 sets, picked source and density), the
Brainwave and Shaadi Shift PDP scenes, Our Story; Liquid / JS errors on each page. Shots → qa/fidelity/hd-pack-*-w9.png."""
import asyncio, json, pathlib, sys, time
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
TB = pathlib.Path(__file__).resolve().parents[1]
QA = TB.parent / 'qa/fidelity'
O = 'https://0nev20-vn.myshopify.com'
Q = 'preview_theme_id=186651934933'
IMG = """(sel) => [...document.querySelectorAll(sel)].slice(0, 10).map(i => { const r = i.getBoundingClientRect();
  return { src: (i.currentSrc || i.src).split('/').pop().split('?')[0], css: Math.round(r.width), natural: i.naturalWidth,
           dens: r.width ? Math.round(i.naturalWidth / r.width * 100) / 100 : null, shown: r.width > 0 && r.height > 0 && i.complete && i.naturalWidth > 0 }; })"""


def url(p):
    return f"{O}{p}{'&' if '?' in p else '?'}{Q}&_cb={time.time_ns()}"


async def settle(pg):
    await pg.add_style_tag(content='[id^="PBar"], #preview-bar-iframe { display: none !important; }')
    await pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager')")
    for y in range(0, 9000, 600):
        if not await pg.evaluate(f'(window.scrollTo(0, {y}), {y} < document.documentElement.scrollHeight)'):
            break
        await pg.wait_for_timeout(40)
    await pg.evaluate('window.scrollTo(0, 0)')
    await pg.evaluate('Promise.race([Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; }))), new Promise(r => setTimeout(r, 4000))])')
    await pg.wait_for_timeout(500)


async def shot(pg, sel, out):
    loc = pg.locator(sel).first
    if not await loc.count():
        print('  (no', sel, ')'); return
    await loc.scroll_into_view_if_needed()
    await pg.wait_for_timeout(400)
    await loc.screenshot(path=str(out))
    print('  shot', out.name)


async def page(pg, path):
    await pg.goto(url(path), wait_until='load', timeout=90000)
    await settle(pg)
    html = await pg.content()
    bad = [x for x in ('Liquid error', 'translation missing') if x in html]
    print(path, '| liquid', bad or 'clean')


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        errs = []
        ctx = await b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=3)
        pg = await ctx.new_page()
        pg.on('pageerror', lambda e: errs.append('PAGEERROR ' + str(e)[:150]))
        pg.on('console', lambda m: errs.append('console ' + m.text[:150]) if m.type == 'error' else None)
        await page(pg, '/collections/all')
        tiles = await pg.evaluate(IMG, '.st-card__pack')
        for t in tiles:
            print('  tile', json.dumps(t))
        print('  tiles on st-hd-pack-*:', sum(t['src'].startswith('st-hd-pack-') for t in tiles), 'of', len(tiles), '| all shown:', all(t['shown'] for t in tiles))
        await shot(pg, '.st-shop__grid', QA / 'hd-pack-shop-390-w9.png')
        for h, k in (('haan-mera-idea-tha', 'brainwave'), ('dulhan-tu-duty-meri', 'shaadi-shift')):
            await page(pg, f'/products/{h}')
            print('  scene box', json.dumps(await pg.evaluate(IMG, '.st-pdp-scene__box')))
            print('  package panel', json.dumps(await pg.evaluate(IMG, '.st-package-panel img, .st-pack--hd img')))
            ss = await pg.evaluate("(document.querySelector('.st-pdp-scene__box') || {}).srcset || ''")
            print('  srcset', [s.strip().split(' ')[0].split('/')[-1].split('?')[0] + ' ' + s.strip().split(' ')[-1] for s in ss.split(',') if s.strip()])
            await shot(pg, '.st-pdp-media__slide', QA / f'hd-pack-pdp-{k}-390-w9.png')
        await page(pg, '/pages/our-story')
        ours = await pg.evaluate(IMG, '.st-ours__box img, .st-pack__box')
        for t in ours:
            print('  box', json.dumps(t))
        await shot(pg, '.st-ours__stack', QA / 'hd-pack-our-story-390-w9.png')
        await ctx.close()
        print('JS errors', [e for e in errs if 'shop.app' not in e and 'Content Security' not in e and 'status of 403' not in e] or 'none')
        await b.close()


asyncio.run(main())
