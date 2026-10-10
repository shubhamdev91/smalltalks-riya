"""After-shots of the INSTALLED build (preview of 186651934933), nothing injected: the home whole scroll, the Wild Card and
Shaadi Shift chapters, the Journal index, at 390x844 / 1280x720 / 1536x703 / 1920x1080, and the Tier A pages (help,
collection, PDP) at 1680x1050 / 1920x1080. Every image loaded and decoded first; on laptop the beeline is drawn
(svg.st-beecur) before the shot. Output: qa/desktop/owner-v12/after-<tag>-<page>-<WxH>.png.
Usage: python -I tools/after_shots.py <tag>"""
import asyncio, io, pathlib, sys, time
from playwright.async_api import async_playwright
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
TB = pathlib.Path(__file__).resolve().parents[1]
OUT = TB.parent / 'qa/desktop/owner-v12'
TAG = sys.argv[1] if len(sys.argv) > 1 else 'w4'
ORIGIN = 'https://0nev20-vn.myshopify.com'
Q = 'preview_theme_id=186651934933'
BASE = '[id^="PBar"], #preview-bar-iframe { display: none !important; } html, body, .page-wrapper { scroll-behavior: auto !important; }'
GROW = 'html, body { height: auto !important; overflow: visible !important; } .page-wrapper { height: auto !important; overflow: visible !important; }'
MAIN = [(390, 844), (1280, 720), (1536, 703), (1920, 1080)]
WIDE = [(1680, 1050), (1920, 1080)]


async def load(br, w, h, path):
    ctx = await br.new_context(viewport={'width': w, 'height': h}, device_scale_factor=1)
    pg = await ctx.new_page()
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)[:120]))
    await pg.goto(f'{ORIGIN}{path}{"&" if "?" in path else "?"}{Q}&_cb={time.time_ns()}', wait_until='load', timeout=120000)
    await pg.add_style_tag(content=BASE)
    await pg.evaluate("document.querySelectorAll('.st-land').forEach(s => s.style.contentVisibility = 'visible')")
    await pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager'); document.querySelectorAll('img[data-st-src]').forEach(i => { if (!i.getAttribute('src')) i.src = i.dataset.stSrc; })")
    for y in range(0, 16000, 600):
        await pg.evaluate(f'window.scrollTo(0, {y}); (document.querySelector(".page-wrapper") || {{}}).scrollTop = {y}')
        await pg.wait_for_timeout(25)
    await pg.evaluate("Promise.race([Promise.all([...document.images].map(i => (i.complete ? Promise.resolve() : new Promise(r => { i.onload = i.onerror = r; })).then(() => i.decode ? i.decode().catch(() => 0) : 0))), new Promise(r => setTimeout(r, 10000))])")
    await pg.evaluate('document.fonts.ready')
    if w >= 990:
        await pg.add_style_tag(content=GROW)
    await pg.evaluate('window.scrollTo(0, 0); (document.querySelector(".page-wrapper") || {}).scrollTop = 0')
    if path == '/' and w >= 1024:
        for _ in range(100):
            if await pg.evaluate("!!document.querySelector('svg.st-beecur path[d]')"):
                break
            await pg.wait_for_timeout(100)
    await pg.wait_for_timeout(1200)
    return ctx, pg, errs


def save(im, name, scale):
    if scale != 1:
        im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
    im.save(OUT / name)


async def main():
    async with async_playwright() as p:
        br = await p.chromium.launch(channel='chrome')
        for w, h in MAIN:
            size = f'{w}x{h}'
            ctx, pg, errs = await load(br, w, h, '/')
            save(Image.open(io.BytesIO(await pg.screenshot(full_page=True, animations='disabled'))), f'after-{TAG}-home-{size}.png', 1 if w < 600 else 0.5)
            for key in ('wild-card', 'shaadi-shift'):
                el = await pg.query_selector(f'.st-ch[data-land="{key}"]')
                save(Image.open(io.BytesIO(await el.screenshot(animations='disabled'))), f'after-{TAG}-{key}-{size}.png', 1)
            await ctx.close()
            ctx, pg, e2 = await load(br, w, h, '/blogs/journal')
            save(Image.open(io.BytesIO(await pg.screenshot(full_page=True, animations='disabled'))), f'after-{TAG}-journal-{size}.png', 1 if w < 600 else 0.6)
            await ctx.close()
            print(size, 'home + wild-card + shaadi-shift + journal', 'errors', errs or e2 or 'none')
        for w, h in WIDE:
            size = f'{w}x{h}'
            for name, path in (('help', '/pages/help'), ('collection', '/collections/all'), ('pdp', '/products/bill-idhar')):
                ctx, pg, errs = await load(br, w, h, path)
                save(Image.open(io.BytesIO(await pg.screenshot(full_page=True, animations='disabled'))), f'after-{TAG}-{name}-{size}.png', 0.6)
                await ctx.close()
                print(size, name, 'errors', errs or 'none')
        await br.close()


asyncio.run(main())
