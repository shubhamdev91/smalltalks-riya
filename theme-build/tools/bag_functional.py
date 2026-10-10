"""Functional checks on the preview bag (theme 186651934933), 390 px, throwaway context; the test cart is emptied after.
+ raises the quantity, − lowers it, Remove empties the line (the visible "Remove" text button keeps Horizon's handler),
the subtotal follows, and the cart drawer (if the theme opens one from the PDP) still renders its own remove icon."""
import asyncio, sys, time
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')
O = 'https://0nev20-vn.myshopify.com'
Q = 'preview_theme_id=186651934933'
count = "fetch('/cart.js').then(r => r.json()).then(c => [c.item_count, c.total_price])"


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        ctx = await b.new_context(viewport={'width': 390, 'height': 844})
        pg = await ctx.new_page()
        errs = []
        pg.on('pageerror', lambda e: errs.append('PAGEERROR ' + str(e)[:160]))
        await pg.goto(f'{O}/cart?{Q}&_cb={time.time_ns()}', wait_until='load')
        vid = await pg.evaluate("fetch('/products/bill-idhar.js').then(r => r.json()).then(p => p.variants[0].id)")
        await pg.evaluate(f"fetch('/cart/add.js', {{ method: 'POST', headers: {{ 'Content-Type': 'application/json' }}, body: JSON.stringify({{ items: [{{ id: {vid}, quantity: 1 }}] }}) }})")
        await pg.goto(f'{O}/cart?{Q}&_cb={time.time_ns()}', wait_until='load')
        await pg.wait_for_timeout(1000)
        print('start', await pg.evaluate(count), '| remove label:', await pg.get_attribute('.st-bag-remove', 'aria-label'),
              '| text:', (await pg.inner_text('.st-bag-remove')).strip())
        await pg.click('.cart-page .quantity-plus'); await pg.wait_for_timeout(2500)
        print('after +', await pg.evaluate(count), '| subtotal shown:', (await pg.inner_text('.cart-totals__total-value')).strip())
        await pg.click('.cart-page .quantity-minus'); await pg.wait_for_timeout(2500)
        print('after -', await pg.evaluate(count))
        await pg.click('.st-bag-remove'); await pg.wait_for_timeout(2500)
        print('after Remove', await pg.evaluate(count), '| empty heading:', (await pg.inner_text('h1')).strip()[:40])
        # drawer: add from the PDP and look for Horizon's drawer markup
        await pg.goto(f'{O}/products/bill-idhar?{Q}&_cb={time.time_ns()}', wait_until='load'); await pg.wait_for_timeout(800)
        await pg.click('.product-information .add-to-cart-button'); await pg.wait_for_timeout(2500)
        drawer = await pg.evaluate("(() => { const d = document.querySelector('cart-drawer-component, .cart-drawer'); if (!d) return 'no drawer'; return { open: d.hasAttribute('open') || !!d.querySelector('dialog[open]'), tiles: d.querySelectorAll('.st-bag-tile').length, icons: d.querySelectorAll('.cart-items__remove svg').length }; })()")
        print('drawer after add:', drawer, '| cart', await pg.evaluate(count))
        await pg.evaluate("fetch('/cart/clear.js', { method: 'POST' })"); await pg.wait_for_timeout(400)
        print('cleared ->', await pg.evaluate(count), '| page errors:', errs or 'none')
        await ctx.close(); await b.close()

asyncio.run(main())
