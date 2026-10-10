"""Asset-window checks (owner-D-1): logo in header / footer, header heights, HD packaging per surface (picked source and
density), og tags on home, favicon on a fresh profile, Liquid / JS errors. Shots → qa/fidelity/hd-pack-*.png, logo-*.png."""
import asyncio, json, pathlib, re, sys, time
from playwright.async_api import async_playwright
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
TB = pathlib.Path(__file__).resolve().parents[1]
QA = TB.parent / 'qa/fidelity'
O = 'https://0nev20-vn.myshopify.com'
Q = 'preview_theme_id=186651934933'
IMG = """(sel) => [...document.querySelectorAll(sel)].slice(0, 8).map(i => { const r = i.getBoundingClientRect();
  return { src: (i.currentSrc || i.src).split('/').pop().split('?')[0], css: Math.round(r.width), natural: i.naturalWidth,
           dens: r.width ? Math.round(i.naturalWidth / r.width * 100) / 100 : null, top: Math.round(r.top + scrollY) }; })"""


def url(p):
    return f"{O}{p}{'&' if '?' in p else '?'}{Q}&_cb={time.time_ns()}"


async def settle(pg):
    await pg.add_style_tag(content='[id^="PBar"], #preview-bar-iframe { display: none !important; }')
    await pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager')")
    for y in range(0, 9000, 600):
        if not await pg.evaluate(f'(window.scrollTo(0, {y}), {y} < document.documentElement.scrollHeight)'):
            break
        await pg.wait_for_timeout(40)
    await pg.evaluate('window.scrollTo(0, 0)')
    await pg.evaluate('Promise.race([Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; }))), new Promise(r => setTimeout(r, 4000))])')
    await pg.wait_for_timeout(500)


async def shot(pg, sel, out, pad=10, maxh=700):
    loc = pg.locator(sel).first
    if not await loc.count():
        print('  (no', sel, ')'); return None
    await loc.scroll_into_view_if_needed()
    await pg.wait_for_timeout(400)
    await loc.screenshot(path=str(out))
    return out


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        errs = []
        # header heights + logo
        for w, h in ((320, 568), (390, 844), (430, 932), (1280, 800)):
            ctx = await b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=2)
            pg = await ctx.new_page()
            pg.on('pageerror', lambda e: errs.append(str(e)[:150]))
            await pg.goto(url('/'), wait_until='load', timeout=90000)
            await settle(pg)
            r = await pg.evaluate("""(() => { const h = document.querySelector('.st-header').getBoundingClientRect(); const i = document.querySelector('.st-header__bar > .st-logo img');
              const ir = i && i.getBoundingClientRect(); const hero = document.querySelector('[data-st-hero]');
              return { header: Math.round(h.height), logo: i && [i.src.split('/').pop().split('?')[0], Math.round(ir.left), Math.round(ir.top), Math.round(ir.width), Math.round(ir.height), i.alt],
                       logoColor: getComputedStyle(document.documentElement).getPropertyValue('--st-logo-blue').trim(), iconInk: getComputedStyle(document.querySelector('.st-header__icon-button')).color,
                       heroBottom: hero && Math.round(hero.getBoundingClientRect().bottom) }; })()""")
            print(f'header {w}x{h}', json.dumps(r))
            if w in (390, 1280):
                await pg.screenshot(path=str(QA / f'logo-header-{w}.png'), clip={'x': 0, 'y': 0, 'width': w, 'height': 90})
                await shot(pg, '.st-footer', QA / f'logo-footer-{w}.png', maxh=500)
                f = await pg.evaluate("(() => { const i = document.querySelector('.st-footer__logo img'); return i && [i.src.split('/').pop().split('?')[0], Math.round(i.getBoundingClientRect().width), Math.round(i.getBoundingClientRect().height), i.alt]; })()")
                print('  footer logo', f)
            if w == 390:
                head = (await pg.content()).split('</head>')[0]
                print('  og', re.findall(r'<meta (?:property|name)="(?:og:image[^"]*|twitter:image:alt)" content="([^"]+)"', head))
            await ctx.close()
        # packaging surfaces at 390 for On Me + Pinky Promise (+ Brainwave = held set)
        ctx = await b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=3)
        pg = await ctx.new_page()
        pg.on('pageerror', lambda e: errs.append(str(e)[:150]))
        shots = []
        await pg.goto(url('/collections/all'), wait_until='load', timeout=90000)
        await settle(pg)
        print('shop tiles', json.dumps(await pg.evaluate(IMG, '.st-card__pack')))
        shots.append(await shot(pg, '.st-shop__grid', QA / 'hd-pack-shop-390.png', maxh=1400))
        for h in ('bill-idhar', 'haath-do-main-hoon', 'haan-mera-idea-tha'):
            await pg.goto(url(f'/products/{h}'), wait_until='load', timeout=90000)
            await settle(pg)
            print('pdp', h, json.dumps(await pg.evaluate(IMG, '.st-pdp-scene__box, .st-pdp-media__thumb img')[:2] if False else await pg.evaluate(IMG, '.st-pdp-scene__box')),
                  'og', await pg.evaluate("(document.querySelector('meta[property=\"og:image\"]') || {}).content"))
            shots.append(await shot(pg, '.st-pdp-media__slide', QA / f'hd-pack-pdp-{h}-390.png'))
        await pg.goto(url('/pages/our-story'), wait_until='load', timeout=90000)
        await settle(pg)
        print('our story', json.dumps(await pg.evaluate(IMG, '.st-ours__box img, .st-pack__box')))
        shots.append(await shot(pg, '.st-ours__stack', QA / 'hd-pack-our-story-390.png'))
        # bag line (one test item, cleared after)
        vid = await pg.evaluate("fetch('/products/bill-idhar.js').then(r => r.json()).then(p => p.variants[0].id)")
        await pg.evaluate(f"fetch('/cart/add.js', {{ method: 'POST', headers: {{ 'Content-Type': 'application/json' }}, body: JSON.stringify({{ items: [{{ id: {vid}, quantity: 1 }}] }}) }})")
        await pg.goto(url('/cart'), wait_until='load', timeout=90000)
        await settle(pg)
        print('bag line', json.dumps(await pg.evaluate(IMG, '.cart-items .st-card__pack, .cart-items img')))
        shots.append(await shot(pg, '.cart-items__table, .cart-items', QA / 'hd-pack-bag-390.png', maxh=500))
        await pg.evaluate("fetch('/cart/clear.js', { method: 'POST' })")
        await pg.wait_for_timeout(400)
        print('cart cleared ->', await pg.evaluate("fetch('/cart.js').then(r => r.json()).then(c => c.item_count)"))
        await pg.goto(url('/blogs/journal'), wait_until='load', timeout=90000)
        await settle(pg)
        print('journal index packaging imgs:', await pg.evaluate("document.querySelectorAll('img[src*=\"st-hd-pack-\"], img[src*=\"st-package-\"]').length"))
        shots.append(await shot(pg, '.st-journal-card, .st-journal__card, article', QA / 'hd-pack-journal-390.png', maxh=600))
        await ctx.close()
        # favicon on a fresh profile
        ctx = await b.new_context(viewport={'width': 390, 'height': 844})
        pg = await ctx.new_page()
        fav = []
        pg.on('response', lambda r: fav.append(f'{r.status} {r.url.split("?")[0].split("/")[-1]}') if ('favicon' in r.url or 'apple-touch' in r.url) else None)
        await pg.goto(url('/'), wait_until='load', timeout=90000)
        await pg.wait_for_timeout(2500)
        print('favicon fresh profile', fav, '| links', await pg.evaluate("[...document.querySelectorAll('link[rel~=icon], link[rel=apple-touch-icon]')].map(l => l.href.split('?')[0].split('/').pop())"))
        await ctx.close()
        print('page errors', errs or 'none')
        await b.close()


asyncio.run(main())
