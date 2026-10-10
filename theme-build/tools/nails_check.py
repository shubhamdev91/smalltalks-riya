"""Which nail sprite files each page requests (fresh browser profile per page, full scroll so every lazy surface renders).
P1 = st-nails-<set>.webp, HD = st-hd-nails-<set>.webp. /cart is checked with one test item, cleared afterwards.
Usage: python -I tools/nails_check.py [width]"""
import asyncio, json, sys, time
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
O = 'https://0nev20-vn.myshopify.com'
Q = 'preview_theme_id=186651934933'
W = int(sys.argv[1]) if len(sys.argv) > 1 else 390
PAGES = ['/', '/products/bill-idhar', '/collections/all', '/blogs/journal', '/blogs/journal/on-me', '/cart', '/pages/our-story',
         '/blogs/the-talks']


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        for path in PAGES:
            ctx = await b.new_context(viewport={'width': W, 'height': 900})
            pg = await ctx.new_page()
            seen = []
            pg.on('request', lambda r: seen.append(r.url.split('?')[0].split('/')[-1]) if 'nails-' in r.url and '.webp' in r.url else None)
            if path == '/cart':
                await pg.goto(f'{O}/?{Q}&_cb={time.time_ns()}', wait_until='load', timeout=90000)
                vid = await pg.evaluate("fetch('/products/bill-idhar.js').then(r => r.json()).then(p => p.variants[0].id)")
                await pg.evaluate(f"fetch('/cart/add.js', {{ method: 'POST', headers: {{ 'Content-Type': 'application/json' }}, body: JSON.stringify({{ items: [{{ id: {vid}, quantity: 1 }}] }}) }})")
                seen.clear()
            await pg.goto(f'{O}{path}?{Q}&_cb={time.time_ns()}', wait_until='load', timeout=90000)
            await pg.add_style_tag(content='[id^="PBar"], #preview-bar-iframe { display: none !important; }')
            for y in range(0, 16000, 500):
                if not await pg.evaluate(f'(window.scrollTo(0, {y}), {y} < document.documentElement.scrollHeight)'):
                    break
                await pg.wait_for_timeout(60)
            await pg.wait_for_timeout(1200)
            html = await pg.content()
            p1 = sorted({s for s in seen if s.startswith('st-nails-')})
            hd = sorted({s for s in seen if s.startswith('st-hd-nails-')})
            extra = ''
            if path == '/cart':
                extra = f" items={await pg.evaluate('fetch(\"/cart.js\").then(r => r.json()).then(c => c.item_count)')}"
                await pg.evaluate("fetch('/cart/clear.js', { method: 'POST' })")
                await pg.wait_for_timeout(400)
                extra += f" -> cleared {await pg.evaluate('fetch(\"/cart.js\").then(r => r.json()).then(c => c.item_count)')}"
            print(json.dumps({'page': path, 'P1_requests': len([s for s in seen if s.startswith('st-nails-')]), 'P1': p1, 'HD': hd,
                              'liquid': [x for x in ('Liquid error', 'translation missing') if x in html] or 'clean'}) + extra)
            await ctx.close()
        await b.close()


asyncio.run(main())
