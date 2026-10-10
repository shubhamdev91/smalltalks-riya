"""Screenshot lab/landing.html at a width and cut per-section side-by-sides against the board-3 column crops.
Usage: python -I tools/lab_shots.py [width] [only-key]"""
import asyncio, pathlib, sys, subprocess
from PIL import Image
from playwright.async_api import async_playwright

TB = pathlib.Path(__file__).resolve().parents[1]
RIYA = TB.parent
OUT = TB / 'lab/shots'
OUT.mkdir(parents=True, exist_ok=True)
W = int(sys.argv[1]) if len(sys.argv) > 1 else 390
ONLY = sys.argv[2] if len(sys.argv) > 2 else None
BOARD = {  # key: (column, y0, y1) in board-3 column crops (css px at 390)
    'diet-cherry': (1, 1062, 1700), 'brainwave': (2, 0, 850), 'green-flag': (2, 850, 1715),
    'shaadi-shift': (3, 545, 1320), 'on-me': (3, 1320, 2387), 'wild-card': (4, 0, 850), 'pinky-promise': (4, 850, 1715),
    'tiles': (1, 722, 1062), 'talks-teaser': (1, 1700, 2264), 'journal-teaser': (2, 1715, 2387),
    'nail-guide-teaser': (3, 0, 545), 'shop-all-faq-footer': (4, 1715, 2348),
}


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        pg = await b.new_page(viewport={'width': W, 'height': 900}, device_scale_factor=1)
        await pg.goto((TB / 'lab/landing.html').as_uri())
        await pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager')"); await pg.evaluate('Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; })))'); await pg.evaluate('Promise.all([...document.images].map(i => i.decode().catch(() => 0)))'); await pg.evaluate('document.fonts.ready')
        await pg.wait_for_timeout(500)
        boxes = await pg.evaluate('''(() => [...document.querySelectorAll('section.st-land')].map(s => {
            const r = s.getBoundingClientRect(); const k = parseFloat(getComputedStyle(s).getPropertyValue('--h'));
            return { key: s.dataset.land, top: r.top + scrollY, h: r.height, hk: k }; }))()''')
        await pg.screenshot(path=str(OUT / f'landing-{W}.png'), full_page=True)
        full = Image.open(OUT / f'landing-{W}.png')
        for bx in boxes:
            key = bx['key']
            if ONLY and key != ONLY:
                continue
            kpx = min(W / 390, 1.4)
            top = round(bx['top']); h = round(bx['hk'] * kpx)
            shot = full.crop((0, top, W, top + h))
            sp = OUT / f'{key}-{W}.png'
            shot.save(sp)
            if key in BOARD and W == 390:
                col, y0, y1 = BOARD[key]
                bp = OUT / f'board-{key}.png'
                Image.open(RIYA / f'spec/crops/landing-col{col}@390.png').crop((0, y0, 390, y1)).save(bp)
                subprocess.run([sys.executable, '-I', str(RIYA / 'qa/fidelity/sbs.py'), str(sp), str(bp),
                                str(OUT / f'{key}-390-vs-board.png'), key], cwd=RIYA, capture_output=True)
        print([(bx['key'], round(bx['top']), round(bx['h'])) for bx in boxes])
        await b.close()

asyncio.run(main())
