"""Nail Guide checks on the preview. Usage: python -I tools/guide_functional.py [width=390]"""
import asyncio, json, sys, time
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')
W = int(sys.argv[1]) if len(sys.argv) > 1 else 390


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        pg = await b.new_page(viewport={'width': W, 'height': 844})
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)[:120]))
        await pg.goto(f'https://0nev20-vn.myshopify.com/pages/nail-guide-desi?preview_theme_id=186651934933&_cb={time.time_ns()}', wait_until='load', timeout=60000)
        await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(700)
        out = {}
        out['h1_vs_peek'] = await pg.evaluate("""(() => { const h = document.querySelector('.st-guide__title'); const r = document.createRange(); r.selectNodeContents(h);
            const ink = r.getBoundingClientRect(); const pk = document.querySelector('.st-guide__peek').getBoundingClientRect();
            return { h1_right: Math.round(ink.right), peek_left: Math.round(pk.left), clear: Math.round(pk.left - ink.right), fs: getComputedStyle(h).fontSize }; })()""")
        out['note_lines'] = await pg.evaluate("document.querySelector('.st-guide__note').innerText")
        out['steps'] = await pg.evaluate("[...document.querySelectorAll('.st-gstep__heading')].map(h => h.innerText.replace(/\s+/g, ' '))")
        out['art'] = await pg.evaluate("(() => { const i = document.querySelector('.st-gstep__art'); return i ? [i.alt, i.complete && i.naturalWidth] : null; })()")
        for sel in ('.st-gcard summary', '.st-gqa summary'):
            loc = pg.locator(sel)
            n = await loc.count()
            opened = []
            for i in range(n):
                await loc.nth(i).click(); await pg.wait_for_timeout(120)
                opened.append(await loc.nth(i).evaluate('s => s.parentElement.open'))
            out[sel] = opened
        out['size_cells'] = await pg.evaluate("[...document.querySelectorAll('.st-gcard__body ul li')].length")
        out['small_targets'] = await pg.evaluate("""[...document.querySelectorAll('.st-guide a, .st-guide summary, .st-guide button')]
            .map(e => { const r = e.getBoundingClientRect(); return [e.className || e.tagName, Math.round(r.width), Math.round(r.height)]; })
            .filter(([n, w, h]) => h < 44 && w > 0)""")
        out['scrollW'] = await pg.evaluate('document.documentElement.scrollWidth')
        out['errors'] = errs
        print(W, json.dumps(out, ensure_ascii=False))
        await b.close()

asyncio.run(main())
