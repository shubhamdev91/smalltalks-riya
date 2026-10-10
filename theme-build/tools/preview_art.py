"""Measure landing art boxes on the preview (theme 186651934933) at 390: each .st-land__art box and img (section-relative),
computed mask-composite and max-width, plus FAQ row pitch. Optional --shots: crops Brainwave / Green Flag / FAQ and makes
side-by-sides against the board crops into qa/fidelity/landing/. Usage: python -I tools/preview_art.py [--shots]"""
import asyncio, json, pathlib, subprocess, sys, time
from PIL import Image
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')
TB = pathlib.Path(__file__).resolve().parents[1]
RIYA = TB.parent
OUT = RIYA / 'qa/fidelity/landing'
URL = f'https://0nev20-vn.myshopify.com/?preview_theme_id=186651934933&_cb={int(time.time())}'
BOARD = {'chapter-brainwave': (2, 0, 850), 'chapter-green-flag': (2, 850, 1715), 'end': (4, 1715, 2348)}
JS = '''(() => {
  const r = e => { const b = e.getBoundingClientRect(); return [b.left, b.top + scrollY, b.right, b.bottom + scrollY].map(Math.round); };
  const out = {};
  for (const key of ['brainwave', 'green-flag']) {
    const s = document.querySelector(`section.st-land[data-land="${key}"]`) || document.querySelector(`[data-land="${key}"]`);
    if (!s) { out[key] = 'missing'; continue; }
    const S = r(s);
    out[key] = { section: S, art: [...s.querySelectorAll('.st-land__art')].map(a => {
      const i = a.querySelector('img'), A = r(a), I = r(i), cs = getComputedStyle(a);
      return { box: [A[0] - S[0], A[1] - S[1], A[2] - S[0], A[3] - S[1]], img: [I[0] - S[0], I[1] - S[1], I[2] - S[0], I[3] - S[1]],
               imgW: I[2] - I[0], composite: cs.maskComposite || cs.webkitMaskComposite, maxW: getComputedStyle(i).maxWidth, src: i.currentSrc.split('/').pop().split('?')[0] }; }) };
  }
  const q = [...document.querySelectorAll('.st-faq details, .st-faq .st-question, [data-land="shop-all-faq-footer"] details')];
  out.faq = q.map(e => r(e)[1]);
  out.faqPitch = out.faq.slice(1).map((y, i) => y - out.faq[i]);
  return out; })()'''


async def main(shots):
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
        m = await pg.evaluate(JS)
        print(json.dumps(m, ensure_ascii=False, indent=1))
        if shots:
            full = OUT / '_full-390.png'
            await pg.screenshot(path=str(full), full_page=True)
            boxes = await pg.evaluate('''(() => { const g = s => { const e = document.querySelector(s); if (!e) return null; const b = e.getBoundingClientRect(); return [b.top + scrollY, b.height]; };
              const k = s => { const e = document.querySelector(s); return parseFloat(getComputedStyle(e).getPropertyValue('--h')) * (e.querySelector('.st-land__inner').getBoundingClientRect().width / 390); };
              const f = document.querySelector('[data-land="shop-all-faq-footer"]'), ft = document.querySelector('.st-footer');
              return { 'chapter-brainwave': [g('[data-land="brainwave"]')[0], k('[data-land="brainwave"]')],
                       'chapter-green-flag': [g('[data-land="green-flag"]')[0], k('[data-land="green-flag"]')],
                       end: [f.getBoundingClientRect().top + scrollY, ft.getBoundingClientRect().bottom - f.getBoundingClientRect().top] }; })()''')
            im = Image.open(full)
            for key, (top, h) in boxes.items():
                top, h = round(top), round(h)
                shot = OUT / f'{key}-390.png'
                im.crop((0, top, 390, top + h)).save(shot)
                col, y0, y1 = BOARD[key]
                bp = OUT / f'board-{key}.png'
                Image.open(RIYA / f'spec/crops/landing-col{col}@390.png').crop((0, y0, 390, y1)).save(bp)
                name = 'shop-all-faq-footer' if key == 'end' else key
                subprocess.run([sys.executable, '-I', str(RIYA / 'qa/fidelity/sbs.py'), str(shot), str(bp), str(OUT / f'{name}-390-vs-board.png'),
                                f'{name} (preview)'], cwd=RIYA, capture_output=True)
            full.unlink()
        await b.close()

asyncio.run(main('--shots' in sys.argv))
