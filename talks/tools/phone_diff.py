"""Phones frozen: full-page 390x844 (and 1023 / 990 widths) pixel diff of hub, topic and thread, as served vs with the
staged desktop change applied (feed wrapper + talks/staged/desktop/desktop.css), or vs a saved baseline.
Usage: python -I phone_diff.py proto            (as served vs injected staged change)
       python -I phone_diff.py save|compare     (baseline before install / compare after install)"""
import asyncio, io, json, os, sys, time
from PIL import Image, ImageChops
from playwright.async_api import async_playwright

MODE = sys.argv[1] if len(sys.argv) > 1 else 'proto'
PAGES = {'hub': '/blogs/the-talks', 'topic': '/pages/talks/tiny-wins',
         'thread': '/pages/talk/what-s-your-smallest-friendship-green-flag'}
SIZES = [(390, 844), (990, 800), (1023, 800)]
CSS = open(os.environ.get('TALKS_CSS', 'talks/staged/desktop/staged-sections.css'), encoding='utf-8').read()
BASE = 'qa/talks/desktop/phone-baseline'
os.makedirs(BASE, exist_ok=True)
WRAP = """() => {
  const s = document.querySelector('.st-talks[data-st-feed]');
  if (!s || s.querySelector(':scope > .st-talks__feed')) return 0;
  const compose = s.querySelector(':scope > .st-talks__compose');
  const feed = document.createElement('div'); feed.className = 'st-talks__feed';
  let n = compose.nextElementSibling; const move = [];
  while (n) { move.push(n); n = n.nextElementSibling; }
  move.forEach(m => feed.appendChild(m)); s.appendChild(feed); return move.length;
}"""
FREEZE = """[id^="PBar"], #preview-bar-iframe { display: none !important; }
*, *::before, *::after { animation: none !important; transition: none !important; caret-color: transparent !important; }"""


async def shot(b, path, w, h, inject):
    pg = await b.new_page(viewport={'width': w, 'height': h})
    await pg.goto(f'https://0nev20-vn.myshopify.com{path}?preview_theme_id=186651934933&_cb={time.time_ns()}', wait_until='networkidle', timeout=60000)
    await pg.add_style_tag(content=FREEZE)
    if inject:
        await pg.evaluate(WRAP)
        await pg.add_style_tag(content=CSS)
    await pg.evaluate("document.fonts.ready")
    await pg.wait_for_timeout(600)
    # the theme scrolls .page-wrapper at >= 990: grow it so a full-page shot covers everything
    await pg.add_style_tag(content='html, body { height: auto !important; overflow: visible !important; } .page-wrapper { height: auto !important; overflow: visible !important; }')
    await pg.wait_for_timeout(300)
    png = await pg.screenshot(full_page=True)
    await pg.close()
    return Image.open(io.BytesIO(png)).convert('RGB')


def diff(a, c):
    if a.size != c.size:
        return {'same': False, 'sizes': [a.size, c.size]}
    box = ImageChops.difference(a, c).getbbox()
    return {'same': box is None, 'bbox': box, 'size': a.size}


async def main():
    out = {}
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        for name, path in PAGES.items():
            for w, h in SIZES:
                key = f'{name}-{w}x{h}'
                if MODE == 'proto':
                    out[key] = diff(await shot(b, path, w, h, False), await shot(b, path, w, h, True))
                elif MODE == 'save':
                    (await shot(b, path, w, h, False)).save(f'{BASE}/{key}.png')
                    out[key] = 'saved'
                else:
                    out[key] = diff(Image.open(f'{BASE}/{key}.png').convert('RGB'), await shot(b, path, w, h, False))
        await b.close()
    for k, v in out.items():
        print(k, json.dumps(v))

asyncio.run(main())
