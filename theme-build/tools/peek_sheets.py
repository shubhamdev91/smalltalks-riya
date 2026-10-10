"""Preview (theme 186651934933) check of the HD character peeks: PDP coda (all 7 sets), bag help panel, Our Story eye
crop, guide corner peek, talks-teaser avatar. Per peek: src, loaded natural size, rendered box vs image, density
(natural px / css px), page h-scroll and Liquid errors; crops composed into qa/fidelity/<prefix>-peeks-<W>.png.
The bag uses a throwaway context with a 1-item test cart (only if the empty bag shows no peek), emptied afterwards.
Usage: python -I tools/peek_sheets.py [width] [prefix]"""
import asyncio, json, pathlib, sys, time
from playwright.async_api import async_playwright
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
TB = pathlib.Path(__file__).resolve().parents[1]
QA = TB.parent / 'qa/fidelity'
TMP = TB / 'tmp/peeks'
TMP.mkdir(parents=True, exist_ok=True)
O = 'https://0nev20-vn.myshopify.com'
Q = 'preview_theme_id=186651934933'
W = int(sys.argv[1]) if len(sys.argv) > 1 else 390
PREFIX = sys.argv[2] if len(sys.argv) > 2 else 'hd2'
PDP = ['bill-idhar', 'haan-mera-idea-tha', 'tum-aa-jao-main-dekh-lungi', 'dulhan-tu-duty-meri', 'haan-wohi-wali',
       'achha-tum-pehle', 'haath-do-main-hoon']
PAGES = [('bag', '/cart', '.st-bag-extras__peek', '.st-bag-extras__help'),
         ('our-story', '/pages/our-story', '.st-ours__eye', '.st-ours__moment'),
         ('guide', '/pages/nail-guide-desi', '.st-guide__peek', '.st-guide__header'),
         ('avatar', '/', '.st-talks__avatar', '.st-talks__avatar')]
INFO = r'''([peek, ctx]) => {
  const p = document.querySelector(peek);
  if (!p) return null;
  const c = p.closest(ctx) || document.querySelector(ctx) || p;
  const i = p.querySelector('img');
  const r = e => { const b = e.getBoundingClientRect(); return [b.left, b.top + scrollY, b.width, b.height].map(v => Math.round(v * 10) / 10); };
  return { box: r(p), ctx: r(c), img: i && r(i), src: i && i.currentSrc.split('/').pop().split('?')[0],
           natural: i && [i.naturalWidth, i.naturalHeight], complete: i && i.complete,
           density: i && Math.round(i.naturalWidth / i.getBoundingClientRect().width * 100) / 100,
           hscroll: document.documentElement.scrollWidth > innerWidth };
}'''


async def settle(pg):
    await pg.add_style_tag(content='[id^="PBar"], #preview-bar-iframe { display: none !important; }')
    await pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager')")
    for y in range(0, 20000, 600):
        if not await pg.evaluate(f'(window.scrollTo(0, {y}), {y} < document.documentElement.scrollHeight)'):
            break
        await pg.wait_for_timeout(60)
    await pg.evaluate('window.scrollTo(0, 0)')
    await pg.evaluate('Promise.race([Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; }))), new Promise(r => setTimeout(r, 5000))])')
    await pg.evaluate('document.fonts.ready')
    await pg.wait_for_timeout(500)


async def shot(pg, name, peek, ctx):
    html = await pg.content()
    flags = [x for x in ('Liquid error', 'translation missing') if x in html]
    await pg.evaluate(f"(() => {{ const i = document.querySelector('{peek} img'); return i ? i.decode().catch(() => 0) : 0; }})()")
    info = await pg.evaluate(INFO, [peek, ctx])
    print(name, flags or 'clean', json.dumps(info))
    if not info:
        return None
    x, y, w, h = info['ctx']
    bx, by, bw, bh = info['box']
    top = max(0, min(y, by) - 16)
    bottom = max(y + h, by + bh) + 16
    if bottom - top > 420:  # keep the crop around the peek
        top, bottom = max(0, by - 120), by + bh + 60
    await pg.evaluate(f'window.scrollTo(0, {max(0, top - 100)})')
    await pg.wait_for_timeout(300)
    out = TMP / f'{name}-{W}.png'
    await pg.screenshot(path=str(out), full_page=True, clip={'x': 0, 'y': top, 'width': W, 'height': bottom - top})
    return name, out, info


async def main():
    crops = []
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        ctx = await b.new_context(viewport={'width': W, 'height': 844}, device_scale_factor=2)
        pg = await ctx.new_page()
        errs = []
        pg.on('pageerror', lambda e: errs.append('PAGEERROR ' + str(e)[:160]))
        for h in PDP:
            await pg.goto(f'{O}/products/{h}?{Q}&_cb={time.time_ns()}', wait_until='load', timeout=90000)
            await settle(pg)
            r = await shot(pg, f'pdp-{h}', '.st-notes__peek', '.st-notes__coda')
            if r:
                crops.append(r)
        added = False
        for name, path, peek, c in PAGES:
            await pg.goto(f'{O}{path}?{Q}&_cb={time.time_ns()}', wait_until='load', timeout=90000)
            await settle(pg)
            if name == 'bag' and not await pg.query_selector(peek):
                vid = await pg.evaluate("fetch('/products/bill-idhar.js').then(r => r.json()).then(p => p.variants[0].id)")
                await pg.evaluate(f"fetch('/cart/add.js', {{ method: 'POST', headers: {{ 'Content-Type': 'application/json' }}, body: JSON.stringify({{ items: [{{ id: {vid}, quantity: 1 }}] }}) }})")
                added = True
                await pg.goto(f'{O}{path}?{Q}&_cb={time.time_ns()}', wait_until='load', timeout=90000)
                await settle(pg)
            r = await shot(pg, name, peek, c)
            if r:
                crops.append(r)
            if name == 'bag' and added:
                await pg.evaluate("fetch('/cart/clear.js', { method: 'POST' })")
                await pg.wait_for_timeout(400)
                print('cart cleared ->', await pg.evaluate("fetch('/cart.js').then(r => r.json()).then(c => c.item_count)"))
        print('page errors:', errs or 'none')
        await b.close()
    # sheet: crops at 1x scale (device px / 2), labelled
    ims = [(n, Image.open(o), i) for n, o, i in crops]
    cw = W + 20
    cols = 4
    rows = [ims[i:i + cols] for i in range(0, len(ims), cols)]
    H = sum(max(im.height // 2 for _, im, _ in r) + 40 for r in rows)
    sheet = Image.new('RGB', (cols * cw, H), 'white')
    d = ImageDraw.Draw(sheet)
    Y = 0
    for r in rows:
        for ci, (n, im, info) in enumerate(r):
            X = ci * cw
            sheet.paste(im.resize((im.width // 2, im.height // 2), Image.LANCZOS), (X, Y + 34))
            d.text((X, Y + 2), n, fill='black')
            d.text((X, Y + 16), f"{info['src']}  {info['img'][2]:.0f}css  dens {info['density']}", fill=(90, 90, 90))
        Y += max(im.height // 2 for _, im, _ in r) + 40
    out = QA / f'{PREFIX}-peeks-{W}.png'
    sheet.save(out)
    print('sheet', out)


asyncio.run(main())
