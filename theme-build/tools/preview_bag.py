"""Preview (theme 186651934933) bag check + shots, in a throwaway browser context with a 2-item test cart (On Me,
Brainwave), emptied afterwards. Writes qa/fidelity/bag-390.png, bag-390-vs-board.png (px-for-px), bag-390-vs-board-h.png,
bag-empty-390.png, bag-1280.png. Usage: python -I tools/preview_bag.py"""
import asyncio, json, pathlib, subprocess, sys, time
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')
TB = pathlib.Path(__file__).resolve().parents[1]
RIYA = TB.parent
QA = RIYA / 'qa/fidelity'
O = 'https://0nev20-vn.myshopify.com'
Q = 'preview_theme_id=186651934933'
ITEMS = ['bill-idhar', 'achha-tum-pehle']
INFO = r'''(() => {
  const r = e => { if (!e) return null; const b = e.getBoundingClientRect(); return [b.left, b.top + scrollY, b.right, b.bottom + scrollY].map(Math.round); };
  const q = s => document.querySelector(s);
  return {
    h1: r(q('main h1, .cart-title h1, h1')), h1Text: (q('h1') || {}).textContent?.trim().replace(/\s+/g, ' '),
    items: [...document.querySelectorAll('.cart-items__table-row, .cart-item, [data-key]')].slice(0, 4).map(e => r(e)),
    subtotal: (q('.cart-totals__total-value, .cart__subtotal, [class*=subtotal]') || {}).textContent?.trim().replace(/\s+/g, ' ').slice(0, 60),
    checkout: r(q('[name=checkout], .cart__checkout-button, button[type=submit][name=checkout]')),
    help: r(q('.st-bag-extras__help')), promo: r(q('.st-bag-extras__promo')),
    footer: r(q('.st-footer')), page: document.documentElement.scrollHeight, hscroll: document.documentElement.scrollWidth > innerWidth,
  }; })()'''


async def settle(pg):
    await pg.add_style_tag(content='[id^="PBar"], #preview-bar-iframe { display: none !important; }')
    await pg.add_style_tag(content='html, body, .page-wrapper { height: auto !important; overflow: visible !important; }')
    await pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager')")
    await pg.evaluate('Promise.race([Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; }))), new Promise(r => setTimeout(r, 4000))])')
    await pg.evaluate('document.fonts.ready')
    await pg.wait_for_timeout(800)


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        for w, h in ((390, 844), (1280, 800)):
            ctx = await b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=1)
            pg = await ctx.new_page()
            errs = []
            pg.on('pageerror', lambda e: errs.append('PAGEERROR ' + str(e)[:160]))
            await pg.goto(f'{O}/cart?{Q}&_cb={time.time_ns()}', wait_until='load', timeout=60000)
            await settle(pg)
            if w == 390:
                await pg.screenshot(path=str(QA / 'bag-empty-390.png'), full_page=True)
                print('empty', json.dumps(await pg.evaluate(INFO), ensure_ascii=False))
            for handle in ITEMS:
                vid = await pg.evaluate(f"fetch('/products/{handle}.js').then(r => r.json()).then(p => p.variants[0].id)")
                await pg.evaluate(f"fetch('/cart/add.js', {{ method: 'POST', headers: {{ 'Content-Type': 'application/json' }}, body: JSON.stringify({{ items: [{{ id: {vid}, quantity: 1 }}] }}) }})")
            await pg.goto(f'{O}/cart?{Q}&_cb={time.time_ns()}', wait_until='load', timeout=60000)
            await settle(pg)
            html = await pg.content()
            flags = [x for x in ('Liquid error', 'translation missing') if x in html]
            print(w, 'bag', flags or 'clean', json.dumps(await pg.evaluate(INFO), ensure_ascii=False))
            await pg.screenshot(path=str(QA / ('bag-390.png' if w == 390 else 'bag-1280.png')), full_page=True)
            await pg.evaluate("fetch('/cart/clear.js', { method: 'POST' })")
            await pg.wait_for_timeout(400)
            print(w, 'cart cleared ->', await pg.evaluate("fetch('/cart.js').then(r => r.json()).then(c => c.item_count)"), errs or '')
            await ctx.close()
        await b.close()
    shot, board = QA / 'bag-390.png', RIYA / 'spec/crops/bag@390.png'
    for mode, out in (('width', 'bag-390-vs-board.png'), ('height', 'bag-390-vs-board-h.png')):
        subprocess.run([sys.executable, '-I', str(QA / 'sbs.py'), str(shot), str(board), str(QA / out), 'bag (preview)', mode],
                       cwd=RIYA, capture_output=True)

asyncio.run(main())
