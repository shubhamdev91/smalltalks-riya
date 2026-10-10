"""PDP narrow-phone check on the preview: at 320 / 375 / 390, document scrollWidth vs viewport, the buy row boxes,
the Add to bag visible text vs accessible name, and full-page shots qa/fidelity/pdp-<w>.png (+ a 3-up sheet)."""
import asyncio, json, pathlib, sys, time
from PIL import Image, ImageDraw
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')
QA = pathlib.Path(__file__).resolve().parents[2] / 'qa/fidelity'
URL = 'https://0nev20-vn.myshopify.com/products/{h}?preview_theme_id=186651934933&_cb={t}'
JS = r'''(() => { const r = s => { const e = document.querySelector(s); if (!e) return null; const b = e.getBoundingClientRect(); return [b.left, b.right].map(Math.round); };
  const btn = document.querySelector('.product-information .add-to-cart-button');
  const more = document.querySelector('.st-atb__more');
  return { scrollW: document.documentElement.scrollWidth, innerW: innerWidth, qty: r('.product-information .quantity-selector'),
           add: r('.product-information .add-to-cart-button'), save: r('.st-save'), visible: btn.innerText.trim().replace(/\s+/g, ' '),
           accName: btn.textContent.trim().replace(/\s+/g, ' '), moreHidden: more ? getComputedStyle(more).clip !== 'auto' : null,
           overflowing: [...document.querySelectorAll('body *')].filter(e => e.getBoundingClientRect().right > innerWidth + 1 && getComputedStyle(e).position !== 'fixed').slice(0, 4).map(e => e.tagName + '.' + String(e.className).split(' ')[0]) }; })()'''


async def main():
    shots = []
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        for w in (320, 375, 390):
            pg = await b.new_page(viewport={'width': w, 'height': 800}, device_scale_factor=1)
            await pg.goto(URL.format(h='bill-idhar', t=time.time_ns()), wait_until='load')
            await pg.add_style_tag(content='[id^="PBar"], #preview-bar-iframe { display: none !important; }')
            await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(1000)
            print(w, json.dumps(await pg.evaluate(JS), ensure_ascii=False))
            out = QA / f'pdp-{w}.png'
            await pg.screenshot(path=str(out), full_page=False)
            shots.append((w, out))
            await pg.close()
        await b.close()
    ims = [(w, Image.open(o).convert('RGB')) for w, o in shots]
    sheet = Image.new('RGB', (sum(i.width for _, i in ims) + 20 * len(ims), max(i.height for _, i in ims) + 24), 'white')
    x = 0; d = ImageDraw.Draw(sheet)
    for w, i in ims:
        sheet.paste(i, (x, 24)); d.text((x + 4, 6), f'{w} px (preview)', fill=0); x += i.width + 20
    sheet.save(QA / 'pdp-narrow-320-375-390.png')

asyncio.run(main())
