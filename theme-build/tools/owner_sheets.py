"""Owner review sheets (lab only, nothing written to the theme): the landing's 7 chapters and their joins on the BUILD
preview, as one tall scroll image per size, the CURRENT build beside a PROPOSAL rendered from the same page with
injected CSS and/or JS (e.g. st-fable's chapter compositions or a new beeline SVG). Sizes 390x844, 1280x720 and 1536x703.
The capture runs from the first chapter's top (minus the tiles' tail) to the last chapter's end (plus the FAQ cap), with
.page-wrapper grown to its content on desktop so the whole run is one image; reduced motion holds the hero.
Output: qa/desktop/owner-v12/<tag>-<WxH>.png (current | proposal, labelled) and the single renders.
Usage: python -I tools/owner_sheets.py <tag> [--css file.css] [--js file.js] [--sizes 390x844,1280x720,1536x703]"""
import asyncio, pathlib, sys, time
from playwright.async_api import async_playwright
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
TB = pathlib.Path(__file__).resolve().parents[1]
ARGS = sys.argv[1:]
TAG = ARGS[0] if ARGS and not ARGS[0].startswith('--') else 'owner'
opt = lambda n, d=None: ARGS[ARGS.index(n) + 1] if n in ARGS else d
CSS = pathlib.Path(opt('--css')).read_text(encoding='utf-8') if opt('--css') else ''
JS = pathlib.Path(opt('--js')).read_text(encoding='utf-8') if opt('--js') else ''
SIZES = [tuple(int(v) for v in s.split('x')) for s in opt('--sizes', '390x844,1280x720,1536x703').split(',')]
OUT = TB.parent / 'qa/desktop/owner-v12'
OUT.mkdir(parents=True, exist_ok=True)
URL = 'https://0nev20-vn.myshopify.com/?preview_theme_id=186651934933'
BASE = '[id^="PBar"], #preview-bar-iframe { display: none !important; } html, body, .page-wrapper { scroll-behavior: auto !important; }'
GROW = 'html, body { height: auto !important; overflow: visible !important; } .page-wrapper { height: auto !important; overflow: visible !important; }'


async def render(br, w, h, css, js, out):
    ctx = await br.new_context(viewport={'width': w, 'height': h}, reduced_motion='reduce', device_scale_factor=1)
    pg = await ctx.new_page()
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)[:120]))
    await pg.goto(f'{URL}&_cb={time.time_ns()}', wait_until='load', timeout=120000)
    await pg.add_style_tag(content=BASE + css)
    if js:
        await pg.evaluate(js)
    await pg.evaluate("document.querySelectorAll('.st-land').forEach(s => s.style.contentVisibility = 'visible')")
    await pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager')")
    for y in range(0, 16000, 500):
        await pg.evaluate(f'window.scrollTo(0, {y}); (document.querySelector(".page-wrapper") || {{}}).scrollTop = {y}')
        await pg.wait_for_timeout(30)
    for _ in range(120):
        if not await pg.evaluate("[...document.images].filter(i => i.getAttribute('src') && i.offsetParent && (!i.complete || !i.naturalWidth)).length"):
            break
        await pg.wait_for_timeout(200)
    await pg.evaluate('document.fonts.ready')
    if w >= 990:
        await pg.add_style_tag(content=GROW)
    await pg.evaluate('window.scrollTo(0, 0); (document.querySelector(".page-wrapper") || {}).scrollTop = 0')
    await pg.wait_for_timeout(900)
    box = await pg.evaluate("""(() => { const a = document.querySelector('.st-ch[data-land="diet-cherry"]'), z = document.querySelector('.st-ch[data-land="pinky-promise"]');
      const ra = a.getBoundingClientRect(), rz = z.getBoundingClientRect(); return [Math.max(0, ra.top + scrollY - 40), rz.bottom + scrollY + 30]; })()""")
    full = out.with_suffix('.full.png')
    await pg.screenshot(path=str(full), full_page=True, animations='disabled')
    await ctx.close()
    im = Image.open(full).convert('RGB')
    im = im.crop((0, int(box[0]), im.width, min(im.height, int(box[1]))))
    im.save(out)
    full.unlink(missing_ok=True)
    return im, errs


async def main():
    async with async_playwright() as p:
        br = await p.chromium.launch(channel='chrome')
        for w, h in SIZES:
            cur, e1 = await render(br, w, h, '', '', OUT / f'{TAG}-{w}x{h}-current.png')
            pro, e2 = await render(br, w, h, CSS, JS, OUT / f'{TAG}-{w}x{h}-proposal.png')
            scale = 1 if w < 600 else 0.5
            a = cur.resize((int(cur.width * scale), int(cur.height * scale)), Image.LANCZOS)
            b = pro.resize((int(pro.width * scale), int(pro.height * scale)), Image.LANCZOS)
            sheet = Image.new('RGB', (a.width + b.width + 30, max(a.height, b.height) + 40), 'white')
            dr = ImageDraw.Draw(sheet)
            dr.text((10, 10), f'{w}x{h}  CURRENT (build as written)', fill='black')
            dr.text((a.width + 20, 10), f'{w}x{h}  PROPOSAL ({TAG})', fill='black')
            sheet.paste(a, (10, 30)); sheet.paste(b, (a.width + 20, 30))
            sheet.save(OUT / f'{TAG}-{w}x{h}.png')
            print(f'{w}x{h}: current {cur.size}, proposal {pro.size}, errors {e1 + e2 or "none"} -> {TAG}-{w}x{h}.png')
        await br.close()


asyncio.run(main())
