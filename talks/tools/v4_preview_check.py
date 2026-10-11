"""v4_preview_check.py [tag]: the INSTALLED talks v4 window on the build preview (theme 186651934933). For each page x
width (320/390/1280, plus 1536/1920 for the header): HTTP status, no "Liquid error" / "translation missing", no
horizontal overflow, no console errors, and page facts (hub rows, chips, composer state, comments, the wordmark
<use> target, the header link). Prints one JSON line per page/width + PASS/FAIL; screenshots to qa/talks/v4-<tag>/.
Usage: python -I talks/tools/v4_preview_check.py off"""
import asyncio, json, os, sys, time
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')
TAG = sys.argv[1] if len(sys.argv) > 1 else 'check'
BASE, Q = 'https://0nev20-vn.myshopify.com', '?preview_theme_id=186651934933'
OUT = f'qa/talks/v4-{TAG}'
os.makedirs(OUT, exist_ok=True)
PAGES = [('hub', '/blogs/the-talks'), ('topic', '/pages/talks/tiny-wins'), ('thread', '/pages/talk/what-s-your-smallest-friendship-green-flag'),
         ('news', '/blogs/news'), ('home', '/'), ('pdp', '/products/bill-idhar'), ('journal', '/blogs/journal')]
HIDE = '[id^="PBar"], #preview-bar-iframe { display: none !important; } html { scroll-behavior: auto !important; }'
FACTS = """() => {
  const q = (s) => document.querySelector(s), qa = (s) => [...document.querySelectorAll(s)];
  const txt = document.body.innerText;
  const wm = q('#st-talks-wm'), hl = q('.st-header__talks'), hsvg = hl?.querySelector('svg');
  const r = (e) => { if (!e) return null; const b = e.getBoundingClientRect(); return [Math.round(b.width*10)/10, Math.round(b.height*10)/10]; };
  return {
    liquidError: /Liquid error|translation missing/i.test(document.documentElement.innerHTML),
    overflow: document.scrollingElement.scrollWidth - innerWidth,
    wmDef: Boolean(wm), wmDefs: qa('#st-talks-wm').length, headerLink: r(hl), headerMark: r(hsvg), headerName: hl?.querySelector('.visually-hidden')?.textContent ?? null,
    h1: q('#MainContent h1')?.textContent.trim().slice(0, 40) ?? null, h1Mark: r(q('#MainContent h1 svg')),
    rows: qa('.tk-rows > .tk-r').length, chips: qa('.tk-chips .tk-chip').map(c => c.textContent.trim()),
    chipCase: q('.tk-chip > span') ? getComputedStyle(q('.tk-chip > span')).textTransform : null,
    composer: q('[data-st-compose]') ? 'form' : (q('.tk-soon') ? 'soon' : null), topicOptions: qa('[data-st-topic] option').map(o => o.textContent.trim()),
    comments: qa('.tk-comments > .tk-c').length, replyForm: Boolean(q('[data-st-reply-form]')), rules: Boolean(q('#house-rules')),
    config: (() => { try { return JSON.parse(q('#st-talks-config')?.textContent || 'null')?.live; } catch { return 'bad'; } })(),
    dock: q('.tk-dock') ? getComputedStyle(q('.tk-dock')).display : null,
    sideNav: q('.tk-side') ? getComputedStyle(q('.tk-side')).display : null,
    rulesCard: q('.tk-rules--card') ? getComputedStyle(q('.tk-rules--card')).display : null,
    caveatLoaded: [...document.fonts].some(f => f.family.includes('Caveat') && f.status === 'loaded'),
  };
}"""


async def main():
    bad = 0
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        for name, path in PAGES:
            widths = (320, 390, 1280) if name in ('hub', 'topic', 'thread', 'news') else (390, 1536)
            for w in widths:
                pg = await b.new_page(viewport={'width': w, 'height': 900})
                errors = []
                pg.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
                pg.on('pageerror', lambda e: errors.append(str(e)))
                res = await pg.goto(f'{BASE}{path}{Q}&_cb={time.time_ns()}', wait_until='networkidle', timeout=60000)
                await pg.add_style_tag(content=HIDE)
                await pg.evaluate('document.fonts.ready')
                await pg.wait_for_timeout(400)
                f = await pg.evaluate(FACTS)
                errs = [e for e in errors if not any(k in e.lower() for k in ('preview', 'shopify-pay', 'monorail', 'shop.app', 'status of 403'))]  # Shop Pay frame noise
                ok = res.status == 200 and not f['liquidError'] and f['overflow'] <= 0 and f['wmDefs'] == 1 and f['headerName'] == 'the talks'
                ok &= not errs
                if f['sideNav'] is not None:
                    ok &= (f['sideNav'] == 'block') == (w >= 1280)
                bad += not ok
                print(('PASS ' if ok else 'FAIL ') + f'{name}@{w} {res.status} ' + json.dumps(f, ensure_ascii=False) + (f' ERRORS {errs[:3]}' if errs else ''))
                await pg.screenshot(path=f'{OUT}/{name}-{w}.png', full_page=name in ('hub', 'topic', 'thread', 'news'))
                await pg.close()
        await b.close()
    print('ALL PASS' if not bad else f'{bad} FAIL')

asyncio.run(main())
