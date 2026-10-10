"""Price strings after the store's money format change (₹{{amount_no_decimals}}): shop cards, a PDP, the bag line, the
cart total and the "Prices include GST" line, at 390 on the preview. Flags "Rs.", ".00", a doubled ₹ or "INR" in the
visible text of each surface. One test item is added with add.js in this throwaway context and the cart is cleared.
Shots: qa/fidelity/price-*.png. Usage: python -I tools/price_check.py"""
import asyncio, pathlib, re, sys, time
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
TB = pathlib.Path(__file__).resolve().parents[1]
QA = TB.parent / 'qa/fidelity'
O = 'https://0nev20-vn.myshopify.com'
Q = 'preview_theme_id=186651934933'
BAD = re.compile(r'Rs\.?\s?\d|\d\.00\b|₹\s*₹|INR')


def url(p):
    return f"{O}{p}{'&' if '?' in p else '?'}{Q}&_cb={time.time_ns()}"


async def texts(pg, sel):
    return await pg.evaluate(f"[...document.querySelectorAll({sel!r})].map(e => e.innerText.replace(/\\s+/g, ' ').trim()).filter(Boolean).slice(0, 12)")


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        ctx = await b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2)
        pg = await ctx.new_page()
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)[:120]))
        await pg.add_init_script("document.addEventListener('DOMContentLoaded', () => { const s = document.createElement('style'); s.textContent = '[id^=PBar], #preview-bar-iframe { display: none !important; }'; document.head.appendChild(s); })")
        report = {}
        await pg.goto(url('/collections/all'), wait_until='load', timeout=90000)
        report['shop cards'] = await texts(pg, '.st-card__price, .price, [class*="price"]:not(style)')
        await pg.locator('.st-shop__grid, main').first.screenshot(path=str(QA / 'price-shop-390.png'))
        await pg.goto(url('/products/bill-idhar'), wait_until='load', timeout=90000)
        report['pdp'] = await texts(pg, 'product-price, .price, .st-pdp__price, [class*="price"]:not(style), .add-to-cart-button, button[name="add"]')
        await pg.screenshot(path=str(QA / 'price-pdp-390.png'))
        vid = await pg.evaluate("fetch('/products/bill-idhar.js').then(r => r.json()).then(p => p.variants[0].id)")
        await pg.evaluate(f"fetch('/cart/add.js', {{ method: 'POST', headers: {{ 'Content-Type': 'application/json' }}, body: JSON.stringify({{ items: [{{ id: {vid}, quantity: 1 }}] }}) }})")
        await pg.goto(url('/cart'), wait_until='load', timeout=90000)
        await pg.wait_for_timeout(800)
        report['bag'] = await texts(pg, '.cart-items [class*="price"], .cart-items__price, .cart-summary, [class*="total"], [class*="tax"], .cart__ctas, .cart-note')
        report['gst line'] = await pg.evaluate("[...document.querySelectorAll('main *')].filter(e => e.children.length === 0 && /GST/i.test(e.textContent)).map(e => e.textContent.trim()).slice(0, 4)")
        await pg.screenshot(path=str(QA / 'price-bag-390.png'), full_page=True)
        await pg.evaluate("fetch('/cart/clear.js', { method: 'POST' })")
        await pg.wait_for_timeout(500)
        cleared = await pg.evaluate("fetch('/cart.js').then(r => r.json()).then(c => c.item_count)")
        for k, v in report.items():
            flags = [t for t in v if BAD.search(t)]
            print(f'{k:10}', 'FLAG ' + str(flags) if flags else 'ok', '|', ' || '.join(v)[:260])
        print('cart cleared ->', cleared, '| page errors', errs or 'none')
        await b.close()


asyncio.run(main())
