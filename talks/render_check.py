"""Quick render check: status, Liquid errors, page errors, key counts on the talks routes (no POSTs)."""
import asyncio, json, sys, time
from playwright.async_api import async_playwright
sys.stdout.reconfigure(encoding='utf-8')
W = int(sys.argv[1]) if len(sys.argv) > 1 else 390
ROUTES = ['/blogs/the-talks', '/pages/talks/tiny-wins', '/pages/talks/something-else', '/pages/talk/what-s-your-smallest-friendship-green-flag', '/blogs/the-talks/same-outfit-different-confidence']
async def main():
    out = []
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        pg = await b.new_page(viewport={'width': W, 'height': 900})
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
        async def guard(route):
            if route.request.method == 'POST': await route.abort()
            else: await route.continue_()
        await pg.route('**/*', guard)
        for r in ROUTES:
            errs.clear()
            res = await pg.goto(f'https://0nev20-vn.myshopify.com{r}?preview_theme_id=186651934933&_cb={time.time_ns()}', wait_until='load', timeout=60000)
            await pg.wait_for_timeout(800)
            html = await pg.content()
            out.append({'route': r, 'status': res.status, 'final': pg.url.split('?')[0].replace('https://0nev20-vn.myshopify.com', ''),
                        'liquid_error': 'Liquid error' in html or 'Liquid syntax error' in html,
                        'liquid_snips': [html[i-80:i+160] for i in [html.find('Liquid error')] if i >= 0],
                        'rows': await pg.locator('[data-st-list] > li').count(),
                        'replies': await pg.locator('[data-st-replies] > li').count(),
                        'composer': await pg.locator('[data-st-compose]').count(),
                        'soon': await pg.locator('.st-compose--soon, .st-reply__soon').count(),
                        'config': await pg.locator('#st-talks-config').count(),
                        'chips': await pg.eval_on_selector_all('.st-talks__chips a', 'as => as.map(a => a.textContent.trim() + (a.getAttribute("aria-current") ? "*" : ""))'),
                        'title': (await pg.title())[:80],
                        'h1': await pg.evaluate("document.querySelector('h1')?.textContent.trim()"),
                        'scrollW': await pg.evaluate('document.documentElement.scrollWidth'),
                        'pageerrors': list(errs)})
        await b.close()
    print(json.dumps(out, ensure_ascii=False, indent=1))
asyncio.run(main())
