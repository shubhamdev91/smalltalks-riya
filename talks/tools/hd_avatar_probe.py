"""Probe: P1 vs HD avatar on the preview, by in-browser style injection only (no theme write).
For every .st-tavatar on the page: screenshot it as-is (P1), then with the HD sheet + x1.058 about (50%, 92.5%), and
measure where nail pixels touch the disc rim (upper half = tip clipping). Usage: python -I hd_avatar_probe.py <path>"""
import asyncio, sys, time, json, io, math
from PIL import Image
from playwright.async_api import async_playwright

PATH = sys.argv[1] if len(sys.argv) > 1 else '/pages/talk/what-s-your-smallest-friendship-green-flag'
OUT = sys.argv[2] if len(sys.argv) > 2 else 'qa/talks/hd-avatar-probe'
HD_CSS = """.st-tavatar__nail { transform: translateY(42.5%) scale(1.058) translateY(-42.5%); }"""
BLUSH = (0xfb, 0xe3, 0xe6)


def rim_hits(img):
    """Nail pixels on the outermost 2px ring of the disc, split into upper/lower half, plus the nail bbox."""
    w, h = img.size
    cx, cy, r = (w - 1) / 2, (h - 1) / 2, min(w, h) / 2
    px = img.load()
    upper = lower = 0
    margin = r
    xs, ys = [], []
    for y in range(h):
        for x in range(w):
            d = math.hypot(x - cx, y - cy)
            if d > r - 0.5:
                continue
            p = px[x, y][:3]
            nail = sum(abs(a - b) for a, b in zip(p, BLUSH)) > 40
            if nail:
                xs.append(x); ys.append(y)
                if y < cy:
                    margin = min(margin, r - d)
                if d > r - 2.5:
                    if y < cy:
                        upper += 1
                    else:
                        lower += 1
    bbox = (min(xs), min(ys), max(xs), max(ys)) if xs else None
    return {'rim_upper': upper, 'rim_lower': lower, 'tip_margin_px': round(margin, 1), 'bbox': bbox, 'size': [w, h]}


async def main():
    out = []
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        pg = await b.new_page(viewport={'width': 390, 'height': 900}, device_scale_factor=2)
        await pg.goto(f'https://0nev20-vn.myshopify.com{PATH}?preview_theme_id=186651934933&_cb={time.time_ns()}', wait_until='networkidle', timeout=60000)
        await pg.add_style_tag(content='[id^="PBar"], #preview-bar-iframe { display: none !important; }')
        avatars = pg.locator('.st-tavatar:not(.st-tavatar--initial)')
        n = await avatars.count()
        before = []
        for i in range(n):
            png = await avatars.nth(i).screenshot()
            before.append(png)
        urls = await pg.evaluate("""() => [...document.querySelectorAll('.st-tavatar:not(.st-tavatar--initial)')].map(e => e.style.getPropertyValue('--st-nails'))""")
        # swap to the HD sheet (same CDN folder, st-hd-nails-<set>.webp) + the x1.058 cuticle-anchored scale
        await pg.evaluate("""() => document.querySelectorAll('.st-tavatar:not(.st-tavatar--initial)').forEach(e => {
            e.style.setProperty('--st-nails', e.style.getPropertyValue('--st-nails').replace('/st-nails-', '/st-hd-nails-'));
        })""")
        await pg.add_style_tag(content=HD_CSS)
        await pg.wait_for_load_state('networkidle')
        await pg.wait_for_timeout(800)
        for i in range(n):
            png = await avatars.nth(i).screenshot()
            a = Image.open(io.BytesIO(before[i])).convert('RGB')
            c = Image.open(io.BytesIO(png)).convert('RGB')
            pair = Image.new('RGB', (a.width + c.width + 12, max(a.height, c.height)), 'white')
            pair.paste(a, (0, 0)); pair.paste(c, (a.width + 12, 0))
            pair.save(f'{OUT}-{i}.png')
            pa, pc = rim_hits(a), rim_hits(c)
            out.append({'i': i, 'set': urls[i].split('/st-nails-')[-1].split('.webp')[0], 'css_size': pa['size'][0] // 2,
                        'P1': {k: pa[k] for k in ('rim_upper', 'tip_margin_px', 'bbox')},
                        'HD': {k: pc[k] for k in ('rim_upper', 'tip_margin_px', 'bbox')}})
        await b.close()
    for o in out:
        print(json.dumps(o))

asyncio.run(main())
