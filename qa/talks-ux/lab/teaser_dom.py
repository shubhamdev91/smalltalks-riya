"""Dump the landing talks teaser's DOM outline (tags, classes, sizes) at 390 and 1536. Read-only."""
import asyncio, time
from playwright.async_api import async_playwright

JS = """() => {
  const sec = document.querySelector('.st-tt__chips').closest('.shopify-section');
  const out = [];
  const walk = (el, d) => { if (d > 5) return; for (const c of el.children) {
    const r = c.getBoundingClientRect();
    out.push(' '.repeat(d * 2) + c.tagName.toLowerCase() + '.' + String(c.className || '').trim().split(/\\s+/).join('.') + ' ' + Math.round(r.width) + 'x' + Math.round(r.height));
    walk(c, d + 1); } };
  walk(sec, 0);
  return out;
}"""


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        for w, h in ((390, 844), (1536, 703)):
            pg = await b.new_page(viewport={'width': w, 'height': h})
            await pg.goto(f'https://0nev20-vn.myshopify.com/?preview_theme_id=186651934933&_cb={time.time_ns()}', wait_until='load')
            print('==', w)
            print('\n'.join((await pg.evaluate(JS))[:60]))
            await pg.close()
        await b.close()

asyncio.run(main())
