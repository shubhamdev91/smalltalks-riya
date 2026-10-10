"""Help page functional checks on the preview (no form is ever sent: every POST is aborted).
Usage: python -I tools/help_functional.py [width=390]"""
import asyncio, json, sys, time
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')
W = int(sys.argv[1]) if len(sys.argv) > 1 else 390
BASE = 'https://0nev20-vn.myshopify.com/pages/help?preview_theme_id=186651934933&_cb='


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        pg = await b.new_page(viewport={'width': W, 'height': 844})
        posts = []
        async def guard(route):
            if route.request.method == 'POST' and '/contact' in route.request.url:
                posts.append(route.request.url)
            if route.request.method == 'POST':
                await route.abort()
            else:
                await route.continue_()
        await pg.route('**/*', guard)
        out = {}
        await pg.goto(BASE + str(time.time_ns()) + '#delivery', wait_until='load', timeout=60000)
        await pg.wait_for_timeout(800)
        out['open_on_hash'] = await pg.evaluate("[...document.querySelectorAll('details.st-topic__item')].map(d => d.id + ':' + d.open)")
        out['topics'] = await pg.evaluate("[...document.querySelectorAll('.st-topic__label')].map(e => e.textContent.trim())")
        await pg.locator('#fit summary').click(); await pg.wait_for_timeout(300)
        out['fit_open'] = await pg.evaluate("document.getElementById('fit').open")
        out['fit_link'] = await pg.evaluate("document.querySelector('#fit .st-link')?.getAttribute('href')")
        out['fit_body'] = await pg.evaluate("document.querySelector('#fit .st-topic__body').innerText.slice(0, 80)")
        out['search'] = await pg.evaluate("(() => { const f = document.querySelector('.st-help__search'); const i = f.querySelector('input[type=search]'); return [f.getAttribute('action'), f.method, i.name, document.querySelector('label[for=\"' + i.id + '\"]')?.textContent.trim()]; })()")
        await pg.locator('.st-help-form__submit').click(); await pg.wait_for_timeout(400)
        out['form_errors'] = await pg.evaluate("[...document.querySelectorAll('.st-help-form .st-field__error')].map(e => e.textContent)")
        out['focus'] = await pg.evaluate("document.activeElement?.name")
        out['submit_text'] = await pg.evaluate("document.querySelector('.st-help-form__submit').innerText.trim()")
        out['small_targets'] = await pg.evaluate("""[...document.querySelectorAll('.st-help a, .st-help button, .st-help input:not([type=hidden]), .st-help textarea, .st-help summary')]
              .map(e => { const r = e.getBoundingClientRect(); return [e.className || e.name || e.tagName, Math.round(r.width), Math.round(r.height)]; })
              .filter(([n, w, h]) => h < 44 && w > 0)""")
        out['contact_posts'] = posts
        out['scrollW'] = await pg.evaluate('document.documentElement.scrollWidth')
        print(json.dumps(out, ensure_ascii=False, indent=1))
        await b.close()

asyncio.run(main())
