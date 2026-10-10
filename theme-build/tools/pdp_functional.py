"""Functional checks on the preview PDP (theme 186651934933), 390 px, in a throwaway browser context:
1. Save toggle: click -> aria-pressed true, label "Saved: …", status text; reload -> still pressed; click -> off.
2. Add to bag still works (Horizon product form): click, then /cart.js item_count goes up by one. The test cart is
   emptied afterwards (/cart/clear.js) so nothing lingers in this context.
3. All seven set PDPs render: status 200, no Liquid errors / missing translations, scene + 6 nails + quote present."""
import asyncio, json, sys, time
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')
O = 'https://0nev20-vn.myshopify.com'
Q = 'preview_theme_id=186651934933'
HANDLES = ['bill-idhar', 'haan-mera-idea-tha', 'tum-aa-jao-main-dekh-lungi', 'dulhan-tu-duty-meri', 'haan-wohi-wali',
           'achha-tum-pehle', 'haath-do-main-hoon']


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        ctx = await b.new_context(viewport={'width': 390, 'height': 844})
        pg = await ctx.new_page()
        errs = []
        pg.on('pageerror', lambda e: errs.append('PAGEERROR ' + str(e)[:160]))
        url = f'{O}/products/bill-idhar?{Q}&_cb={time.time_ns()}'
        await pg.goto(url, wait_until='load')
        await pg.wait_for_timeout(800)
        save = pg.locator('.st-save')
        state = lambda: pg.evaluate("(() => { const s = document.querySelector('.st-save'); const st = document.querySelector('[data-st-save-status]'); return [s.getAttribute('aria-pressed'), s.getAttribute('aria-label'), st ? st.textContent : null, localStorage.getItem('st-saved-sets')]; })()")
        print('save initial', await state())
        await save.click(); await pg.wait_for_timeout(300)
        print('save after click', await state())
        await pg.reload(wait_until='load'); await pg.wait_for_timeout(800)
        print('save after reload', await state())
        await pg.locator('.st-save').click(); await pg.wait_for_timeout(300)
        print('save after 2nd click', await state())

        before = await pg.evaluate("fetch('/cart.js').then(r => r.json()).then(c => c.item_count)")
        await pg.locator('.product-information .add-to-cart-button').click()
        await pg.wait_for_timeout(2500)
        after = await pg.evaluate("fetch('/cart.js').then(r => r.json()).then(c => c.item_count)")
        label = await pg.evaluate("document.querySelector('.product-information .add-to-cart-button').textContent.trim().replace(/\\s+/g, ' ')")
        print('add to bag: cart', before, '->', after, '| button now:', label)
        await pg.evaluate("fetch('/cart/clear.js', { method: 'POST' })")
        await pg.wait_for_timeout(500)
        print('cart cleared ->', await pg.evaluate("fetch('/cart.js').then(r => r.json()).then(c => c.item_count)"))

        for h in HANDLES:
            resp = await pg.goto(f'{O}/products/{h}?{Q}&_cb={time.time_ns()}', wait_until='load')
            await pg.wait_for_timeout(500)
            html = await pg.content()
            info = await pg.evaluate("""(() => ({ nails: document.querySelectorAll('.st-pdp-scene__nail').length, box: !!document.querySelector('.st-pdp-scene__box'),
              quote: (document.querySelector('.st-notes__quote') || {}).textContent?.trim().slice(0, 40), peek: !!document.querySelector('.st-notes__peek img'),
              title: document.querySelector('.product-information h1')?.textContent.trim(), add: document.querySelector('.add-to-cart-button')?.textContent.trim().replace(/\\s+/g, ' '),
              hscroll: document.documentElement.scrollWidth > innerWidth }))()""")
            flags = [x for x in ('Liquid error', 'translation missing') if x in html]
            print(h, resp.status, flags or 'clean', json.dumps(info, ensure_ascii=False))
        print('page errors:', errs or 'none')
        await ctx.close()
        await b.close()

asyncio.run(main())
