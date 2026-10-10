"""Probe whether the PDP renders the current product.json settings (fresh browser context per page).
Prints one line per handle: story open?, Find-your-fit link count, kit disclosure count, accelerated checkout count."""
import asyncio, sys, time
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')
HANDLES = sys.argv[1:] or ['bill-idhar']


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        for handle in HANDLES:
            ctx = await b.new_context(viewport={'width': 390, 'height': 844})
            pg = await ctx.new_page()
            await pg.goto(f'https://0nev20-vn.myshopify.com/products/{handle}?preview_theme_id=186651934933&_cb={time.time_ns()}', wait_until='load')
            h = await pg.content()
            print(handle, 'story-open', 'st-notes__item--story" open' in h, '| fit-link', h.count('st-notes__fit'),
                  '| kit', h.count('in the kit'), '| accel', h.count('accelerated-checkout'))
            await ctx.close()
        await b.close()

asyncio.run(main())
