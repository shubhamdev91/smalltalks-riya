"""Shoot any preview route (theme 186651934933) and side-by-side it with a board crop.
Usage: python -I tools/preview_page.py <path> <spec/crops/xxx@390.png> <name> [width=390]
Writes qa/fidelity/<name>-<w>.png, <name>-<w>-vs-board.png (px-for-px) and -h (equal height); prints basic checks."""
import asyncio, json, pathlib, subprocess, sys, time
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')
TB = pathlib.Path(__file__).resolve().parents[1]
RIYA = TB.parent
QA = RIYA / 'qa/fidelity'
PATH = '/' + sys.argv[1].lstrip('/')
CROP = RIYA / sys.argv[2]
NAME = sys.argv[3]
W = int(sys.argv[4]) if len(sys.argv) > 4 else 390


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        pg = await b.new_page(viewport={'width': W, 'height': 844}, device_scale_factor=1)
        errs = []
        pg.on('pageerror', lambda e: errs.append('PAGEERROR ' + str(e)[:160]))
        sep = '&' if '?' in PATH else '?'
        resp = await pg.goto(f'https://0nev20-vn.myshopify.com{PATH}{sep}preview_theme_id=186651934933&_cb={time.time_ns()}', wait_until='load', timeout=60000)
        await pg.add_style_tag(content='[id^="PBar"], #preview-bar-iframe { display: none !important; }')
        await pg.add_style_tag(content='html, body, .page-wrapper { height: auto !important; overflow: visible !important; }')
        await pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager')")
        await pg.evaluate('Promise.race([Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; }))), new Promise(r => setTimeout(r, 4000))])')
        await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(800)
        html = await pg.content()
        info = await pg.evaluate("({ title: document.title, h1: [...document.querySelectorAll('h1')].map(h => h.textContent.trim().slice(0, 60)), robots: [...document.querySelectorAll('meta[name=robots]')].map(m => m.content).join('|'), scrollW: document.documentElement.scrollWidth, page: document.documentElement.scrollHeight, footer: (document.querySelector('.st-footer') || {}).className })")
        flags = [x for x in ('Liquid error', 'translation missing') if x in html]
        print(PATH, resp.status, flags or 'clean', json.dumps(info, ensure_ascii=False), errs or '')
        shot = QA / f'{NAME}-{W}.png'
        await pg.screenshot(path=str(shot), full_page=True)
        await b.close()
    if CROP.exists():
        for mode, suffix in (('width', ''), ('height', '-h')):
            subprocess.run([sys.executable, '-I', str(QA / 'sbs.py'), str(shot), str(CROP), str(QA / f'{NAME}-{W}-vs-board{suffix}.png'),
                            f'{NAME} (preview)', mode], cwd=RIYA, capture_output=True)

asyncio.run(main())
