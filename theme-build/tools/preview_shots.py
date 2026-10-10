"""Preview (theme 186651934933) landing shots at 390 + side-by-sides against board 3 / board 2 crops.
Writes qa/fidelity/landing-390.png and qa/fidelity/landing/<section>-390-vs-board.png."""
import asyncio, pathlib, subprocess, sys, time
from PIL import Image
from playwright.async_api import async_playwright

TB = pathlib.Path(__file__).resolve().parents[1]
RIYA = TB.parent
OUT = RIYA / 'qa/fidelity/landing'
OUT.mkdir(parents=True, exist_ok=True)
URL = f'https://0nev20-vn.myshopify.com/?preview_theme_id=186651934933&_cb={int(time.time())}'
BOARD = {
    'tiles': (1, 722, 1062), 'chapter-diet-cherry': (1, 1062, 1700), 'talks-teaser': (1, 1700, 2264),
    'chapter-brainwave': (2, 0, 850), 'chapter-green-flag': (2, 850, 1715), 'journal-teaser': (2, 1715, 2387),
    'nail-guide-teaser': (3, 0, 545), 'chapter-shaadi-shift': (3, 545, 1320), 'chapter-on-me': (3, 1320, 2387),
    'chapter-wild-card': (4, 0, 850), 'chapter-pinky-promise': (4, 850, 1715),
}
KEY = {'diet-cherry': 'chapter-diet-cherry', 'brainwave': 'chapter-brainwave', 'green-flag': 'chapter-green-flag',
       'shaadi-shift': 'chapter-shaadi-shift', 'on-me': 'chapter-on-me', 'wild-card': 'chapter-wild-card',
       'pinky-promise': 'chapter-pinky-promise'}


def sbs(shot, board, out, label):
    subprocess.run([sys.executable, '-I', str(RIYA / 'qa/fidelity/sbs.py'), str(shot), str(board), str(out), label],
                   cwd=RIYA, capture_output=True)


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        pg = await b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
        await pg.goto(URL, wait_until='load')
        await pg.add_style_tag(content='[id^="PBar"], #preview-bar-iframe { display: none !important; }')
        await pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager')")
        await pg.evaluate('Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; })))')
        await pg.evaluate('Promise.all([...document.images].map(i => i.decode().catch(() => 0)))')
        await pg.evaluate('document.fonts.ready')
        await pg.wait_for_timeout(1200)
        boxes = await pg.evaluate('''(() => {
          const out = [];
          const add = (key, el, h) => { if (!el) return; const r = el.getBoundingClientRect(); out.push({ key, top: r.top + scrollY, h: h || r.height }); };
          add('header', document.querySelector('.st-header'));
          add('hero', document.querySelector('[data-st-hero]'));
          for (const s of document.querySelectorAll('section.st-land')) {
            const k = parseFloat(getComputedStyle(s).getPropertyValue('--h')) * (s.querySelector('.st-land__inner').getBoundingClientRect().width / 390);
            add(s.dataset.land, s, s.classList.contains('st-land--flow') ? null : k);
          }
          const f = document.querySelector('[data-land="shop-all-faq-footer"]'), ft = document.querySelector('.st-footer');
          if (f && ft) out.push({ key: 'end', top: f.getBoundingClientRect().top + scrollY, h: ft.getBoundingClientRect().bottom - f.getBoundingClientRect().top });
          return out; })()''')
        full_path = RIYA / 'qa/fidelity/landing-390.png'
        await pg.screenshot(path=str(full_path), full_page=True)
        await b.close()
    full = Image.open(full_path)
    for bx in boxes:
        key = KEY.get(bx['key'], bx['key'])
        top, h = round(bx['top']), round(bx['h'])
        shot = OUT / f'{key}-390.png'
        full.crop((0, top, 390, top + h)).save(shot)
        if key in BOARD:
            col, y0, y1 = BOARD[key]
            bp = OUT / f'board-{key}.png'
            Image.open(RIYA / f'spec/crops/landing-col{col}@390.png').crop((0, y0, 390, y1)).save(bp)
            sbs(shot, bp, OUT / f'{key}-390-vs-board.png', key)
        elif key == 'end':
            bp = OUT / 'board-end.png'
            Image.open(RIYA / 'spec/crops/landing-col4@390.png').crop((0, 1715, 390, 2348)).save(bp)
            sbs(shot, bp, OUT / 'shop-all-faq-footer-390-vs-board.png', 'shop all + FAQ + footer')
        elif key == 'header':
            bp = OUT / 'board-header.png'
            Image.open(RIYA / 'spec/crops/hero-1-on-me@390.png').crop((0, 0, 390, 69)).save(bp)
            sbs(shot, bp, OUT / 'header-390-vs-board.png', 'header')
        elif key == 'hero':
            bp = OUT / 'board-hero.png'
            Image.open(RIYA / 'spec/crops/hero-1-on-me@390.png').crop((0, 69, 390, 885)).save(bp)
            sbs(shot, bp, OUT / 'hero-390-vs-board.png', 'hero (first frame)')
    print([(bx['key'], round(bx['top']), round(bx['h'])) for bx in boxes])

asyncio.run(main())
