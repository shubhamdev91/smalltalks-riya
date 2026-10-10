"""Measure the talks hub / thread on the preview: element boxes + ink boxes inside them (390 by default).
Usage: python -I tools/talks_measure.py <path> <selector,...> [width]"""
import asyncio, io, json, sys, time
import numpy as np
from PIL import Image
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')
PATH = '/' + sys.argv[1].lstrip('/')
SELS = sys.argv[2].split(',')
W = int(sys.argv[3]) if len(sys.argv) > 3 else 390


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        pg = await b.new_page(viewport={'width': W, 'height': 844}, device_scale_factor=1)
        sep = '&' if '?' in PATH else '?'
        await pg.goto(f'https://0nev20-vn.myshopify.com{PATH}{sep}preview_theme_id=186651934933&_cb={time.time_ns()}', wait_until='load', timeout=60000)
        await pg.add_style_tag(content='[id^="PBar"], #preview-bar-iframe { display: none !important; } html, body, .page-wrapper { height: auto !important; overflow: visible !important; }')
        await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(900)
        png = await pg.screenshot(full_page=True)
        im = np.asarray(Image.open(io.BytesIO(png)).convert('RGB')).astype(int)
        for sel in SELS:
            r = await pg.evaluate("s => { const e = document.querySelector(s); if (!e) return null; const b = e.getBoundingClientRect(); const cs = getComputedStyle(e); return [b.left + scrollX, b.top + scrollY, b.right + scrollX, b.bottom + scrollY, cs.fontSize, cs.fontFamily.slice(0, 30), cs.fontWeight, cs.color, cs.backgroundColor]; }", sel)
            if not r:
                print(sel, 'MISSING'); continue
            x0, y0, x1, y1 = [int(round(v)) for v in r[:4]]
            a = im[max(y0, 0):y1, max(x0, 0):x1]
            bg = np.median(a.reshape(-1, 3), axis=0) if a.size else np.array([255, 255, 255])
            m = np.abs(a - bg).sum(-1) > 90
            ys, xs = np.nonzero(m)
            inkb = (x0 + xs.min(), y0 + ys.min(), x0 + xs.max(), y0 + ys.max()) if len(xs) else None
            print(f'{sel:28s} box {x0},{y0}-{x1},{y1}  ink {inkb}  {r[4]} {r[5]} {r[6]} {r[7]} bg {r[8]}')
        await b.close()

asyncio.run(main())
