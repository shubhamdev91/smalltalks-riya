"""Preview (theme 186651934933) shop checks + shots. Routes /collections/all and its two tag pages at 390 (and 1280 for
errors / layout). Writes qa/fidelity/shop-390.png, shop-390-vs-board.png (px-for-px, width mode), shop-390-vs-board-h.png
(equal height), shop-everyday-390.png, shop-statement-390.png, shop-1280.png. Usage: python -I tools/preview_shop.py"""
import asyncio, json, pathlib, subprocess, sys, time
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')
TB = pathlib.Path(__file__).resolve().parents[1]
RIYA = TB.parent
QA = RIYA / 'qa/fidelity'
O = 'https://0nev20-vn.myshopify.com'
Q = 'preview_theme_id=186651934933'
ROUTES = [('all', '/collections/all'), ('everyday', '/collections/all/everyday'), ('statement', '/collections/all/statement')]
INFO = '''(() => {
  const r = s => { const e = document.querySelector(s); if (!e) return null; const b = e.getBoundingClientRect(); return [b.left, b.top + scrollY, b.right, b.bottom + scrollY].map(Math.round); };
  const cards = [...document.querySelectorAll('.st-card')];
  return {
    robots: [...document.querySelectorAll('meta[name=robots]')].map(m => m.content).join('|'),
    title: document.title,
    h1: r('.st-shop__heading'), note: r('.st-shop__note'), chips: r('.st-shop__chips'), grid: r('.st-shop__grid'),
    tile: r('.st-card__tile'), cardTitle: r('.st-card__title'), cta: r('.st-card__cta'), footer: r('.st-footer'),
    chipList: [...document.querySelectorAll('.st-shop__chip')].map(a => a.textContent.trim() + (a.getAttribute('aria-current') ? '*' : '') + ' ' + new URL(a.href).pathname),
    status: (document.querySelector('.st-shop [role=status]') || {}).textContent || '',
    cards: cards.map(c => c.dataset.set + ':' + (c.querySelector('.st-card__price') || {}).textContent.trim().replace(/\\s+/g, ' ')),
    imgs: cards.map(c => { const i = c.querySelector('img'); return i ? (i.currentSrc.split('/').pop().split('?')[0] + ' ' + i.naturalWidth + ' alt=' + JSON.stringify(i.alt)) : 'none'; }),
    footerClass: (document.querySelector('.st-footer') || {}).className || '',
    footerLinks: [...document.querySelectorAll('.st-footer a')].map(a => a.textContent.trim() + ' ' + Math.round(a.getBoundingClientRect().height)),
    h1Font: getComputedStyle(document.querySelector('.st-shop__heading') || document.body).fontFamily + ' ' + getComputedStyle(document.querySelector('.st-shop__heading') || document.body).fontWeight,
    fontsLoaded: [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family + ' ' + f.weight).join(', '),
    note: (document.querySelector('.st-shop__note') || {}).textContent.trim().replace(/\\s+/g, ' '),
    tiles: cards.map(c => { const t = c.querySelector('.st-card__tile'), a = c.querySelector('.st-card__pack'), n = c.querySelectorAll('.st-card__nail'), nb = c.querySelector('.st-card__nails');
      const T = t.getBoundingClientRect(), A = a.getBoundingClientRect(), N = nb ? nb.getBoundingClientRect() : null;
      return c.dataset.set + ' ' + getComputedStyle(t).backgroundColor + ' tile ' + Math.round(T.width) + 'x' + Math.round(T.height) +
        ' box ' + Math.round(A.left - T.left) + ',' + Math.round(A.top - T.top) + ' ' + Math.round(A.width) + 'x' + Math.round(A.height) +
        ' nails ' + n.length + (N ? ' @' + Math.round(100 * (N.left - T.left) / T.width) + '-' + Math.round(100 * (N.right - T.left) / T.width) + '%' : '') +
        ' title ' + Math.round(c.querySelector('.st-card__title').getBoundingClientRect().height); }),
    h3: document.querySelectorAll('.st-shop h3').length,
    hscroll: document.documentElement.scrollWidth > innerWidth,
    page: document.documentElement.scrollHeight,
  }; })()'''


def sbs(shot, board, out, label, mode='height'):
    subprocess.run([sys.executable, '-I', str(QA / 'sbs.py'), str(shot), str(board), str(out), label, mode], cwd=RIYA, capture_output=True)


async def settle(pg):
    await pg.add_style_tag(content='[id^="PBar"], #preview-bar-iframe { display: none !important; }')
    # Horizon >=990: .page-wrapper is the scroll container (drawer squeeze); unwrap it so full-page shots see the page.
    await pg.add_style_tag(content='html, body, .page-wrapper { height: auto !important; overflow: visible !important; }')
    await pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager')")
    await pg.evaluate('Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; })))')
    await pg.evaluate('Promise.all([...document.images].map(i => i.decode().catch(() => 0)))')
    await pg.evaluate('document.fonts.ready')
    await pg.wait_for_timeout(1000)


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        for w, h in ((390, 844), (1280, 800)):
            pg = await b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=1)
            errs = []
            pg.on('console', lambda m: errs.append(m.text[:140]) if m.type == 'error' and 'shop.app' not in m.text and 'Framing' not in m.text else None)
            pg.on('pageerror', lambda e: errs.append('PAGEERROR ' + str(e)[:160]))
            for key, r in ROUTES:
                resp = await pg.goto(f'{O}{r}?{Q}&_cb={int(time.time())}', wait_until='load')
                await settle(pg)
                html = await pg.content()
                info = await pg.evaluate(INFO)
                flags = [x for x in ('Liquid error', 'translation missing') if x in html]
                print(w, r, resp.status, flags or '', json.dumps(info, ensure_ascii=False))
                if w == 390:
                    name = 'shop-390.png' if key == 'all' else f'shop-{key}-390.png'
                    await pg.screenshot(path=str(QA / name), full_page=True)
                elif key == 'all':
                    await pg.screenshot(path=str(QA / 'shop-1280.png'), full_page=True)
            if errs:
                print(w, 'console:', sorted(set(errs))[:8])
            await pg.close()
        await b.close()
    board = RIYA / 'spec/crops/shop@390.png'
    sbs(QA / 'shop-390.png', board, QA / 'shop-390-vs-board.png', 'shop /collections/all (preview)', 'width')
    sbs(QA / 'shop-390.png', board, QA / 'shop-390-vs-board-h.png', 'shop /collections/all (preview)', 'height')

asyncio.run(main())
