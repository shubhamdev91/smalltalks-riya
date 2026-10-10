"""Footer check (D5 Instagram link): the three footer variants (landing /, inner /pages/our-story, compact
/collections/all) at 320, 390 and 1280 on the preview. Per variant: footer height, the inner logo column vs the nav,
the Instagram link (box, colour, target, rel, accessible name), horizontal overflow, page errors. Element shots
qa/fidelity/<prefix>-footer-<variant>-<w>.png (the element is scrolled into view, so Horizon's .page-wrapper scroll at
>= 990 is handled). Usage: python -I tools/footer_check.py <prefix>"""
import asyncio, json, pathlib, sys, time
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
TB = pathlib.Path(__file__).resolve().parents[1]
QA = TB.parent / 'qa/fidelity'
O = 'https://0nev20-vn.myshopify.com'
Q = 'preview_theme_id=186651934933'
PREFIX = sys.argv[1] if len(sys.argv) > 1 else 'footer'
PAGES = [('landing', '/'), ('inner', '/pages/our-story'), ('compact', '/collections/all')]
WIDTHS = [(320, 568), (390, 844), (1280, 800)]

PROBE = """(() => {
  const f = document.querySelector('.st-footer'); if (!f) return null;
  const R = (e) => { if (!e) return null; const b = e.getBoundingClientRect(); return [Math.round(b.left), Math.round(b.top), Math.round(b.width), Math.round(b.height)]; };
  const ig = f.querySelector('a[href*="instagram.com"]');
  const svg = ig && ig.querySelector('svg');
  const logo = f.querySelector('.st-footer__logo'), nav = f.querySelector('.st-footer__nav'), social = f.querySelector('.st-footer__social');
  const fr = f.getBoundingClientRect();
  return { variant: [...f.classList].find(c => c.startsWith('st-footer--')), footerH: Math.round(fr.height),
    logo: R(logo), nav: R(nav), social: R(social), ig: R(ig), glyph: svg && R(svg),
    igColor: ig && getComputedStyle(ig).color, target: ig && ig.target, rel: ig && ig.rel, href: ig && ig.getAttribute('href'),
    name: ig && (ig.getAttribute('aria-label') || ig.innerText.replace(/\\s+/g, ' ').trim() || ig.textContent.replace(/\\s+/g, ' ').trim()),
    overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
    liquid: ['Liquid error', 'translation missing'].filter(x => document.documentElement.innerHTML.includes(x)) };
})()"""


async def main():
    out = {}
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        for w, h in WIDTHS:
            for name, path in PAGES:
                ctx = await b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=2)
                pg = await ctx.new_page()
                errs = []
                pg.on('pageerror', lambda e: errs.append(str(e)[:120]))
                await pg.goto(f'{O}{path}?{Q}&_cb={time.time_ns()}', wait_until='load', timeout=120000)
                await pg.add_style_tag(content='[id^="PBar"], #preview-bar-iframe { display: none !important; }')
                loc = pg.locator('.st-footer').first
                await loc.scroll_into_view_if_needed()
                await pg.wait_for_timeout(600)
                m = await pg.evaluate(PROBE)
                await loc.screenshot(path=str(QA / f'{PREFIX}-footer-{name}-{w}.png'))
                m['errors'] = errs
                out[f'{name}-{w}'] = m
                inner_delta = ''
                if m and m['logo'] and m['nav'] and m['social'] and name == 'inner':
                    col_bottom = max(m['logo'][1] + m['logo'][3], m['social'][1] + m['social'][3])
                    inner_delta = f"  logo column bottom {col_bottom - m['nav'][1]} vs nav {m['nav'][3]} (delta {col_bottom - m['nav'][1] - m['nav'][3]:+d})"
                print(f"{name:8} {w:4}  {m['variant']}  footer {m['footerH']}px  ig {m['ig']} glyph {m['glyph'] and m['glyph'][2:]}  colour {m['igColor']}  "
                      f"target {m['target']} rel '{m['rel']}'  name '{m['name']}'  overflow {m['overflow']}  liquid {m['liquid'] or 'clean'}  errors {errs or 'none'}{inner_delta}")
                await ctx.close()
        await b.close()
    (QA / f'{PREFIX}-footer-measurements.json').write_text(json.dumps(out, indent=1), encoding='utf-8')


asyncio.run(main())
