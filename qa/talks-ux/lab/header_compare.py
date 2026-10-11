"""NOW vs V2 header frames (st-fable's refined original Caveat + the small arrow), at 390 and 1536, 2x crops of the real
site header on the build preview (lab only). Output: qa/talks-ux/renders/compare-header-wordmark-{390,1536}.png"""
import asyncio, io, time
from PIL import Image, ImageDraw, ImageFont
from playwright.async_api import async_playwright

src = open('qa/talks-ux/lab/proposed_capture.py', encoding='utf-8').read().replace('asyncio.run(main())', '')
exec(compile(src, 'pc', 'exec'))
try:
    FT = ImageFont.truetype('arialbd.ttf', 26)
except OSError:
    FT = ImageFont.load_default()


async def shot(b, w, h, v2):
    pg = await b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=2)
    await pg.goto(f'{BASE}/blogs/the-talks{Q}&_cb={time.time_ns()}', wait_until='networkidle', timeout=60000)
    await pg.add_style_tag(content=HIDE + (WORDMARK_CSS if v2 else ''))
    if v2:
        await pg.evaluate(MARK)
    await pg.evaluate('document.fonts.ready')
    await pg.wait_for_timeout(500)
    png = await pg.screenshot(clip={'x': 0, 'y': 0, 'width': w, 'height': 76})
    await pg.close()
    return Image.open(io.BytesIO(png)).convert('RGB')


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        for w, h in ((390, 844), (1536, 703)):
            now, v2 = await shot(b, w, h, False), await shot(b, w, h, True)
            gap, head = 16, 40
            sheet = Image.new('RGB', (now.width, now.height * 2 + head * 2 + gap), '#f3efe9')
            d = ImageDraw.Draw(sheet)
            d.text((10, 8), 'NOW: Caveat 600, no arrow', fill='#5d5562', font=FT)
            sheet.paste(now, (0, head))
            d.text((10, head + now.height + gap + 8), 'V2 (recommended): refined Caveat + swash + arrow', fill='#a31a33', font=FT)
            sheet.paste(v2, (0, head * 2 + now.height + gap))
            sheet.save(f'{OUT}/compare-header-wordmark-{w}.png')
            print('header compare', w, sheet.size)
        await b.close()

asyncio.run(main())
