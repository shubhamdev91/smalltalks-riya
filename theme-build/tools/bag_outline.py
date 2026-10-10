"""DOM outline of /cart on the preview with a 2-item test cart (cleared afterwards). Usage: python -I tools/bag_outline.py [selector] [depth]"""
import asyncio, sys, time
from playwright.async_api import async_playwright
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, __import__('os').path.dirname(__file__))
from dom_outline import JS  # noqa: E402  (same outline walker)

SEL = sys.argv[1] if len(sys.argv) > 1 else 'main'
DEPTH = int(sys.argv[2]) if len(sys.argv) > 2 else 10
O = 'https://0nev20-vn.myshopify.com'


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        ctx = await b.new_context(viewport={'width': 390, 'height': 844})
        pg = await ctx.new_page()
        await pg.goto(f'{O}/cart?preview_theme_id=186651934933&_cb={time.time_ns()}', wait_until='load')
        for h in ('bill-idhar', 'achha-tum-pehle'):
            vid = await pg.evaluate(f"fetch('/products/{h}.js').then(r => r.json()).then(p => p.variants[0].id)")
            await pg.evaluate(f"fetch('/cart/add.js', {{ method: 'POST', headers: {{ 'Content-Type': 'application/json' }}, body: JSON.stringify({{ items: [{{ id: {vid}, quantity: 1 }}] }}) }})")
        await pg.goto(f'{O}/cart?preview_theme_id=186651934933&_cb={time.time_ns()}', wait_until='load')
        await pg.wait_for_timeout(1000)
        print(await pg.evaluate(JS, [SEL, DEPTH]))
        await pg.evaluate("fetch('/cart/clear.js', { method: 'POST' })")
        await pg.wait_for_timeout(300)
        await ctx.close()
        await b.close()

asyncio.run(main())
