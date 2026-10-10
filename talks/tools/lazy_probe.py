"""Probe: does content-visibility:auto on talk rows defer the off-screen avatar sheets? HTML is rewritten in-flight
(no theme write): the HD swap + an optional row rule are injected into <head>. Counts nail-sheet requests and bytes at
load (no scroll) and after scrolling to the bottom, at 390. Usage: python -I lazy_probe.py"""
import asyncio, time
from playwright.async_api import async_playwright

HUB = '/blogs/the-talks'
HD = '.st-tavatar__nail { transform: translateY(42.5%) scale(1.058) translateY(-42.5%); }'
LAZY = '.st-talks__list > li { content-visibility: auto; contain-intrinsic-size: auto 170px; }'


async def run(b, extra):
    ctx = await b.new_context(viewport={'width': 390, 'height': 844})
    pg = await ctx.new_page()
    seen = {}

    async def on_resp(r):
        if 'nails-' in r.url:
            try:
                seen[r.url.split('/')[-1].split('?')[0]] = len(await r.body())
            except Exception:
                pass
    pg.on('response', lambda r: asyncio.ensure_future(on_resp(r)))

    async def rewrite(route):
        resp = await route.fetch()
        html = (await resp.text()).replace('/st-nails-', '/st-hd-nails-')
        html = html.replace('</head>', f'<style>{HD}{extra}</style></head>', 1)
        await route.fulfill(response=resp, body=html)
    await pg.route(lambda u: u.split('?')[0].endswith(HUB), rewrite)
    await pg.goto(f'https://0nev20-vn.myshopify.com{HUB}?preview_theme_id=186651934933&_cb={time.time_ns()}', wait_until='networkidle', timeout=60000)
    await pg.wait_for_timeout(1000)
    at_load = dict(seen)
    for _ in range(15):
        await pg.mouse.wheel(0, 600)
        await pg.wait_for_timeout(200)
    await pg.wait_for_load_state('networkidle')
    await pg.wait_for_timeout(800)
    shown = await pg.evaluate("""() => [...document.querySelectorAll('.st-tavatar__nail')].every(n => getComputedStyle(n).backgroundImage.includes('st-hd-nails-'))""")
    await ctx.close()
    kb = lambda d: round(sum(d.values()) / 1024, 1)
    return {'at_load': {'sheets': len(at_load), 'KB': kb(at_load)}, 'after_scroll': {'sheets': len(seen), 'KB': kb(seen)},
            'p1_requested': sorted(k for k in seen if k.startswith('st-nails-')), 'all_avatars_hd': shown}


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        print('HD, as staged     ', await run(b, ''))
        print('HD + row c-v:auto ', await run(b, LAZY))
        await b.close()

asyncio.run(main())
