"""Staged-vs-current sheets (lab only, nothing written): the landing's 7 chapters and their joins, CURRENT = the build
preview as written, STAGED = lab/landing.html (tools/build_landing.py: the staged CSS, map, joins and chapter script),
one tall image per size, plus a Wild Card close-up of each. Sizes 390x844, 1280x720, 1536x703 (and any WxH given).
Output: qa/desktop/owner-v12/<tag>-<WxH>.png and <tag>-<WxH>-wildcard.png.
Usage: python -I tools/staged_sheets.py <tag> [WxH ...]"""
import asyncio, pathlib, sys, time
from playwright.async_api import async_playwright
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
TB = pathlib.Path(__file__).resolve().parents[1]
ARGS = sys.argv[1:]
TAG = ARGS[0] if ARGS and not ARGS[0][0].isdigit() else 'staged'
SIZES = [tuple(int(v) for v in a.split('x')) for a in ARGS if 'x' in a and a[0].isdigit()] or [(390, 844), (1280, 720), (1536, 703)]
OUT = TB.parent / 'qa/desktop/owner-v12'
SRC = {'current': 'https://0nev20-vn.myshopify.com/?preview_theme_id=186651934933&_cb=', 'staged': (TB / 'lab/landing.html').as_uri() + '?_cb='}
BASE = '[id^="PBar"], #preview-bar-iframe { display: none !important; } html, body, .page-wrapper { scroll-behavior: auto !important; }'
GROW = 'html, body { height: auto !important; overflow: visible !important; } .page-wrapper { height: auto !important; overflow: visible !important; }'


async def render(br, w, h, which):
    ctx = await br.new_context(viewport={'width': w, 'height': h}, reduced_motion='reduce', device_scale_factor=1)
    pg = await ctx.new_page()
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)[:120]))
    await pg.goto(SRC[which] + str(time.time_ns()), wait_until='load', timeout=120000)
    await pg.add_style_tag(content=BASE)
    await pg.evaluate("document.querySelectorAll('.st-land').forEach(s => s.style.contentVisibility = 'visible')")
    await pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager')")
    for y in range(0, 16000, 500):
        await pg.evaluate(f'window.scrollTo(0, {y}); (document.querySelector(".page-wrapper") || {{}}).scrollTop = {y}')
        await pg.wait_for_timeout(25)
    for _ in range(120):
        if not await pg.evaluate("[...document.images].filter(i => i.getAttribute('src') && i.offsetParent && (!i.complete || !i.naturalWidth)).length"):
            break
        await pg.wait_for_timeout(200)
    await pg.evaluate("Promise.all([...document.images].map(i => (i.complete ? Promise.resolve() : new Promise(r => { i.onload = i.onerror = r; })).then(() => i.decode ? i.decode().catch(() => 0) : 0)))")
    await pg.evaluate('document.fonts.ready')
    if w >= 990:
        await pg.add_style_tag(content=GROW)
    await pg.evaluate('window.scrollTo(0, 0); (document.querySelector(".page-wrapper") || {}).scrollTop = 0; dispatchEvent(new Event("resize"))')
    await pg.wait_for_timeout(1800)
    box = await pg.evaluate("""(() => { const g = (k) => document.querySelector(`.st-ch[data-land="${k}"]`).getBoundingClientRect();
      const a = g('diet-cherry'), z = g('pinky-promise'), wc = g('wild-card');
      return { from: Math.max(0, a.top + scrollY - 40), to: z.bottom + scrollY + 30, wc: [wc.top + scrollY, wc.height] }; })()""")
    f = OUT / f'_{which}-{w}x{h}.png'
    await pg.screenshot(path=str(f), full_page=True, animations='disabled')
    await ctx.close()
    im = Image.open(f).convert('RGB')
    f.unlink(missing_ok=True)
    run = im.crop((0, int(box['from']), im.width, min(im.height, int(box['to']))))
    wc = im.crop((0, int(box['wc'][0]), im.width, int(box['wc'][0] + min(box['wc'][1], h))))
    return run, wc, errs


def side_by_side(a, b, label_a, label_b, scale):
    a = a.resize((int(a.width * scale), int(a.height * scale)), Image.LANCZOS)
    b = b.resize((int(b.width * scale), int(b.height * scale)), Image.LANCZOS)
    s = Image.new('RGB', (a.width + b.width + 30, max(a.height, b.height) + 40), 'white')
    dr = ImageDraw.Draw(s)
    dr.text((10, 10), label_a, fill='black'); dr.text((a.width + 20, 10), label_b, fill='black')
    s.paste(a, (10, 30)); s.paste(b, (a.width + 20, 30))
    return s


async def main():
    async with async_playwright() as p:
        br = await p.chromium.launch(channel='chrome')
        for w, h in SIZES:
            cr, cw, e1 = await render(br, w, h, 'current')
            sr, sw, e2 = await render(br, w, h, 'staged')
            scale = 1 if w < 600 else 0.5
            side_by_side(cr, sr, f'{w}x{h} CURRENT (build as written)', f'{w}x{h} STAGED v12.1 (lab)', scale).save(OUT / f'{TAG}-{w}x{h}.png')
            side_by_side(cw, sw, f'{w}x{h} Wild Card CURRENT', f'{w}x{h} Wild Card STAGED v12.1', 1 if w < 600 else 0.6).save(OUT / f'{TAG}-{w}x{h}-wildcard.png')
            print(f'{w}x{h}: current {cr.size}, staged {sr.size}, errors current {e1 or "none"} staged {e2 or "none"}')
        await br.close()


asyncio.run(main())
