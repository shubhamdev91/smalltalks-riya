"""HD art swap sheets: shoot the landing at 390 on the preview, crop each changed chapter + the Journal teaser by its DOM box,
and write qa/fidelity/hd1-<key>.png plus hd1-landing.png (all crops side by side). Usage: python -I tools/hd_sheets.py [width]"""
import asyncio, io, json, pathlib, sys, time
from PIL import Image
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')
TB = pathlib.Path(__file__).resolve().parents[1]
QA = TB.parent / 'qa/fidelity'
W = int(sys.argv[1]) if len(sys.argv) > 1 else 390
PREFIX = sys.argv[2] if len(sys.argv) > 2 else 'hd1'
KEYS = ['tiles', 'diet-cherry', 'brainwave', 'green-flag', 'journal', 'shaadi-shift', 'on-me', 'wild-card', 'pinky-promise']


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        pg = await b.new_page(viewport={'width': W, 'height': 844}, device_scale_factor=1)
        await pg.goto(f'https://0nev20-vn.myshopify.com/?preview_theme_id=186651934933&_cb={time.time_ns()}', wait_until='load', timeout=90000)
        await pg.add_style_tag(content='[id^="PBar"], #preview-bar-iframe { display: none !important; } html, body, .page-wrapper { height: auto !important; overflow: visible !important; } *, *::before, *::after { animation-play-state: paused !important; transition: none !important; }')
        await pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager')")
        await pg.evaluate('Promise.race([Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; }))), new Promise(r => setTimeout(r, 8000))])')
        await pg.evaluate('document.fonts.ready')
        # Decode every image and walk the page so Chrome paints the large async-decoded art before the full-page capture.
        await pg.evaluate("Promise.all([...document.images].map(i => (i.decoding = 'sync', i.decode().catch(() => 0))))")
        h = await pg.evaluate('document.documentElement.scrollHeight')
        for y in range(0, h, 700):
            await pg.evaluate(f'window.scrollTo(0, {y})'); await pg.wait_for_timeout(120)
        await pg.evaluate('window.scrollTo(0, 0)'); await pg.wait_for_timeout(1500)
        rects = await pg.evaluate("""keys => Object.fromEntries(keys.map(k => { const e = document.querySelector(`[data-land="${k}"]`) || document.querySelector(`[data-land="${k}-teaser"]`); if (!e) return [k, null]; const r = e.getBoundingClientRect(); return [k, [r.left + scrollX, r.top + scrollY, r.width, r.height]]; }))""", KEYS)
        imgs = await pg.evaluate("""[...document.querySelectorAll('img[src*="st-hd-"]')].map(i => [i.src.split('/').pop().split('?')[0], i.complete, i.naturalWidth, Math.round(i.getBoundingClientRect().width)])""")
        info = await pg.evaluate("({ scrollW: document.documentElement.scrollWidth, liquidErr: document.documentElement.innerHTML.includes('Liquid error') })")
        png = await pg.screenshot(full_page=True)
        await b.close()
    full = Image.open(io.BytesIO(png)).convert('RGB')
    full.save(QA / f'{PREFIX}-landing-full-{W}.png')
    crops = []
    for k in KEYS:
        r = rects.get(k)
        if not r:
            print(k, 'MISSING'); continue
        x, y, w, h = [round(v) for v in r]
        c = full.crop((0, y, W, y + h))
        c.save(QA / f'{PREFIX}-{k}-{W}.png')
        crops.append((k, c))
        print(k, 'y', y, 'h', h)
    sheet = Image.new('RGB', (sum(c.width + 10 for _, c in crops), max(c.height for _, c in crops)), 'white')
    x = 0
    for _, c in crops:
        sheet.paste(c, (x, 0)); x += c.width + 10
    sheet.save(QA / f'{PREFIX}-landing-{W}.png')
    print(json.dumps(info), json.dumps(imgs))

asyncio.run(main())
