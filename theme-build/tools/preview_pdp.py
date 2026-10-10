"""Preview (theme 186651934933) PDP check + shots. /products/<handle> at 390 (and 1280 for errors / layout).
Writes qa/fidelity/pdp-<handle>-390.png, pdp-390-vs-board.png (On Me, px-for-px), pdp-390-vs-board-h.png, pdp-1280.png.
Usage: python -I tools/preview_pdp.py [handle ...]   (default: bill-idhar)"""
import asyncio, json, pathlib, subprocess, sys, time
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')
TB = pathlib.Path(__file__).resolve().parents[1]
RIYA = TB.parent
QA = RIYA / 'qa/fidelity'
O = 'https://0nev20-vn.myshopify.com'
Q = 'preview_theme_id=186651934933'
HANDLES = sys.argv[1:] or ['bill-idhar']
INFO = r'''(() => {
  const r = s => { const e = typeof s === 'string' ? document.querySelector(s) : s; if (!e) return null; const b = e.getBoundingClientRect(); return [b.left, b.top + scrollY, b.right, b.bottom + scrollY].map(Math.round); };
  const cs = (s, p) => { const e = document.querySelector(s); return e ? getComputedStyle(e)[p] : null; };
  const save = document.querySelector('.st-save');
  return {
    title: r('.product-information .group-block h1'), titleFont: cs('.product-information .group-block h1', 'fontFamily') + ' ' + cs('.product-information .group-block h1', 'fontWeight') + ' ' + cs('.product-information .group-block h1', 'fontSize'),
    price: r('.product-information product-price .price'), priceText: (document.querySelector('.product-information product-price .price') || {}).textContent?.trim(),
    media: r('.st-pdp-media__track'), thumbs: [...document.querySelectorAll('.st-pdp-media__thumb')].map(t => r(t)),
    box: r('.st-pdp-scene__box'), nails: document.querySelectorAll('.st-pdp-scene__nail').length,
    short: r('.st-notes__short'), fit: r('.st-notes__fit'),
    qty: r('.product-information .quantity-selector'), add: r('.product-information .add-to-cart-button'),
    addText: (document.querySelector('.product-information .add-to-cart-button') || {}).textContent?.trim().replace(/\s+/g, ' '),
    save: save ? { box: r(save), hidden: save.hidden, pressed: save.getAttribute('aria-pressed'), label: save.getAttribute('aria-label') } : null,
    links: r('.st-notes__links'), linkTexts: [...document.querySelectorAll('.st-notes__links a')].map(a => a.textContent.trim()),
    summaries: [...document.querySelectorAll('.st-notes__summary')].map(s => s.textContent.trim() + ' ' + Math.round(s.getBoundingClientRect().height)),
    quote: r('.st-notes__quote'), quoteText: (document.querySelector('.st-notes__quote') || {}).textContent?.trim(),
    read: r('.st-notes__coda .st-notes__read'), peek: r('.st-notes__peek'),
    footer: r('.st-footer'), page: document.documentElement.scrollHeight, hscroll: document.documentElement.scrollWidth > innerWidth,
    h1s: document.querySelectorAll('h1').length,
  }; })()'''


async def settle(pg):
    await pg.add_style_tag(content='[id^="PBar"], #preview-bar-iframe { display: none !important; }')
    await pg.add_style_tag(content='html, body, .page-wrapper { height: auto !important; overflow: visible !important; }')
    await pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager')")
    await pg.evaluate('Promise.race([Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; }))), new Promise(r => setTimeout(r, 4000))])')
    await pg.evaluate('document.fonts.ready')
    await pg.wait_for_timeout(1000)


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        for w, h in ((390, 844), (1280, 800)):
            pg = await b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=1)
            errs = []
            pg.on('console', lambda m: errs.append(m.text[:140]) if m.type == 'error' and 'shop.app' not in m.text and 'Failed to load resource' not in m.text else None)
            pg.on('pageerror', lambda e: errs.append('PAGEERROR ' + str(e)[:160]))
            for handle in HANDLES:
                resp = await pg.goto(f'{O}/products/{handle}?{Q}&_cb={int(time.time())}', wait_until='load', timeout=60000)
                await settle(pg)
                html = await pg.content()
                flags = [x for x in ('Liquid error', 'translation missing') if x in html]
                print(w, handle, resp.status, flags or 'clean', json.dumps(await pg.evaluate(INFO), ensure_ascii=False))
                if w == 390:
                    await pg.screenshot(path=str(QA / f'pdp-{handle}-390.png'), full_page=True)
                elif handle == HANDLES[0]:
                    await pg.screenshot(path=str(QA / 'pdp-1280.png'), full_page=True)
            if errs:
                print(w, 'console:', sorted(set(errs))[:8])
            await pg.close()
        await b.close()
    if 'bill-idhar' in HANDLES:
        shot, board = QA / 'pdp-bill-idhar-390.png', RIYA / 'spec/crops/product@390.png'
        for mode, out in (('width', 'pdp-390-vs-board.png'), ('height', 'pdp-390-vs-board-h.png')):
            subprocess.run([sys.executable, '-I', str(QA / 'sbs.py'), str(shot), str(board), str(QA / out), 'PDP On Me (preview)', mode],
                           cwd=RIYA, capture_output=True)

asyncio.run(main())
