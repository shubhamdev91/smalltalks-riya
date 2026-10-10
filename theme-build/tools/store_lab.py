"""Store desktop lab (STORE-DESKTOP-SPEC v1) on the real preview, before a write: the page renders from the theme as it
is, and with --after the staged CSS is swapped in: assets/st-landing.css is served from src/ (route), and every
section stylesheet's marked desktop block (between "/* BEGIN store desktop" and "/* END store desktop */" in
src/sections/*.liquid) is injected after the compiled styles (they are additive @media (min-width: 1024px) rules, so
this is the cascade they get once written). Scrolls .page-wrapper (Horizon's scroller at >= 990).

Per region (a section, or the footer): its box; the content's union box (visible text, images, links; beelines and the
section's own ground excluded) and its width against the page frame min(1240, 100% - 2 x clamp(32px, 4vw, 64px));
headings and calls to action that end below the fold when the region's top sits at the header; interactive targets
under 44 px; horizontal overflow; page errors. Shots: <out>/<prefix>-<WxH>-<page>-<region>.png.
Usage: python -I tools/store_lab.py <prefix> [--after] [--sizes 1280x720,...] [--pages landing,...] [--out dir]"""
import asyncio, json, pathlib, re, sys, time
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
TB = pathlib.Path(__file__).resolve().parents[1]
ARGS = sys.argv[1:]
PREFIX = ARGS[0] if ARGS and not ARGS[0].startswith('--') else 'store'
AFTER = '--after' in ARGS
opt = lambda n, d: ARGS[ARGS.index(n) + 1] if n in ARGS else d
SIZES = [tuple(int(v) for v in s.split('x')) for s in opt('--sizes', '1280x720,1366x768,1440x800,1536x703').split(',')]
OUT = pathlib.Path(opt('--out', str(TB.parent / 'qa/desktop/lab-w3')))
OUT.mkdir(parents=True, exist_ok=True)
ORIGIN = 'https://0nev20-vn.myshopify.com'
Q = 'preview_theme_id=186651934933'

# page -> (path, [(region name, selector)]); region 'first' = the page's first screen (scroll 0), measured on <main>.
# Store pages also get a full-page shot (<prefix>-<WxH>-<page>-full.png). The bag fills a throwaway context's cart with
# one On Me kit (add.js) and clears it after (clear.js).
MAIN = '#MainContent, main'
PAGES = {
    'landing': ('/', [('tiles', '[data-land="tiles"]'), ('talks', '[data-land="talks-teaser"]'),
                      ('journal', '[data-land="journal-teaser"]'), ('guide', '[data-land="nail-guide-teaser"]'),
                      ('faq', '[data-land="shop-all-faq-footer"]'), ('footer', '.st-footer')]),
    'help': ('/pages/help', [('first', MAIN)]),
    'journal': ('/blogs/journal', [('first', MAIN)]),
    'story': ('/blogs/journal/on-me', [('first', MAIN)]),
    'our-story': ('/pages/our-story', [('first', MAIN)]),
    'guide': ('/pages/nail-guide', [('first', MAIN)]),
    'guide-desi': ('/pages/nail-guide-desi', [('first', MAIN)]),
    'bag': ('/cart', [('first', MAIN)]),
    'pdp': ('/products/bill-idhar', [('first', MAIN)]),
    'search': ('/search?q=nails', [('first', MAIN)]),
    '404': ('/pages/st-not-a-page', [('first', MAIN)]),
}
CART_VARIANT = 67623509622997  # On Me kit (test cart only)
PAGE_KEYS = opt('--pages', 'landing').split(',')


def desktop_css():
    out = []
    for f in sorted([*(TB / 'src/sections').glob('*.liquid'), *(TB / 'src/blocks').glob('*.liquid'), *(TB / 'src/snippets').glob('*.liquid')]):
        s = f.read_text(encoding='utf-8')
        for m in re.finditer(r'/\* BEGIN store desktop.*?\*/(.*?)/\* END store desktop \*/', s, re.S):
            out.append(f'/* {f.name} */\n' + m.group(1))
    return '\n'.join(out)


HELPERS = """window.__sc = () => { const w = document.querySelector('.page-wrapper');
  return w && /(auto|scroll)/.test(getComputedStyle(w).overflowY) && w.scrollHeight > w.clientHeight + 2 ? w : null; };
window.__sy = () => { const w = window.__sc(); return w ? w.scrollTop - w.getBoundingClientRect().top : scrollY; };
window.__st = (y) => { const w = window.__sc(); if (w) w.scrollTop = y; else window.scrollTo(0, y); };"""

MEASURE = """([sel, hdr, first]) => {
  const el = document.querySelector(sel); if (!el) return null;
  const r = el.getBoundingClientRect(); const W = document.documentElement.clientWidth;
  const vis = (e) => { const cs = getComputedStyle(e); return cs.display !== 'none' && cs.visibility !== 'hidden' && parseFloat(cs.opacity) > 0; };
  const onScreen = (b) => b.right > 0 && b.left < W;
  const leaves = [...el.querySelectorAll('h1,h2,h3,p,li,a,img,summary,button,input,textarea,label,.st-land__card,.st-tiles__nail,.st-talks__avatar,.st-talks__more,svg:not(.st-land__beeline)')]
    .filter(e => !e.closest('.st-land__beeline') && vis(e)).map(e => e.getBoundingClientRect()).filter(b => b.width > 1 && b.height > 1)
    .filter(onScreen).filter(b => !first || (b.top < innerHeight && b.bottom > hdr));
  const U = leaves.length ? { l: Math.min(...leaves.map(b => b.left)), r: Math.max(...leaves.map(b => b.right)), t: Math.min(...leaves.map(b => b.top)), b: Math.max(...leaves.map(b => b.bottom)) } : null;
  const gut = Math.min(Math.max(32, 0.04 * W), 64), frame = Math.min(1240, W - 2 * gut);
  const fold = innerHeight;
  const keys = [...el.querySelectorAll('h1,h2,.st-land__pill,.st-tiles__label,a.button,.st-faq2__shop')].filter(vis).map(e => { const b = e.getBoundingClientRect();
    return { what: (e.textContent || '').trim().slice(0, 24), bottom: Math.round(b.bottom), below: b.bottom > fold + 0.5 }; });
  // inline links inside running text (an FAQ answer, a paragraph) are exempt (WCAG 2.5.8 inline exception)
  const small = [...el.querySelectorAll('a,button,summary,input,select,textarea')].filter(vis).filter(e => !(e.tagName === 'A' && e.closest('p, .st-faq2__a, .rte'))).map(e => ({ e, b: e.getBoundingClientRect() }))
    .filter(({ b }) => b.width > 0 && b.height > 0 && (b.height < 43.5 || b.width < 43.5)).map(({ e, b }) => `${(e.textContent || e.getAttribute('aria-label') || e.tagName).trim().slice(0, 20)} ${Math.round(b.width)}x${Math.round(b.height)}`);
  const R = Math.round;
  return { top: R(r.top + window.__sy()), height: R(r.height), W, frame: R(frame),
           content: U && { l: R(U.l), r: R(U.r), w: R(U.r - U.l), t: R(U.t - r.top), b: R(U.b - r.top), ratio: Math.round((U.r - U.l) / frame * 100) },
           keys, belowFold: keys.filter(k => k.below).map(k => k.what), small };
}"""


async def main():
    css = desktop_css() if AFTER else ''
    local_landing = (TB / 'src/assets/st-landing.css').read_text(encoding='utf-8')
    rep = {}
    async with async_playwright() as p:
        br = await p.chromium.launch(channel='chrome')
        for w, h in SIZES:
            for pk in PAGE_KEYS:
                path, regions = PAGES[pk]
                ctx = await br.new_context(viewport={'width': w, 'height': h})
                if AFTER:
                    async def serve(route):
                        await route.fulfill(status=200, content_type='text/css', body=local_landing)
                    await ctx.route(re.compile(r'.*/assets/st-landing\.css.*'), serve)
                pg = await ctx.new_page()
                if pk == 'bag':
                    await pg.goto(f'{ORIGIN}/?{Q}', wait_until='domcontentloaded', timeout=120000)
                    added = await pg.evaluate(f"fetch('/cart/add.js', {{ method: 'POST', headers: {{ 'Content-Type': 'application/json' }}, body: JSON.stringify({{ items: [{{ id: {CART_VARIANT}, quantity: 1 }}] }}) }}).then(r => r.status)")
                    print(f'{w}x{h} bag: test cart add.js -> {added}')
                errs = []
                pg.on('pageerror', lambda e: errs.append(str(e)[:120]))
                sep = '&' if '?' in path else '?'
                await pg.goto(f'{ORIGIN}{path}{sep}{Q}&_cb={time.time_ns()}', wait_until='load', timeout=120000)
                await pg.add_style_tag(content='[id^="PBar"], #preview-bar-iframe { display: none !important; } html, body, .page-wrapper { scroll-behavior: auto !important; }' + css)
                if AFTER:
                    # staged markup (mirrors src/sections/st-404.liquid): the 404's desktop art element
                    await pg.evaluate("""(() => { const s = document.querySelector('.st-404'); if (!s || s.querySelector('.st-404__art')) return;
                      s.insertAdjacentHTML('beforeend', '<div class="st-404__art" aria-hidden="true"><img src="/cdn/shop/t/8/assets/st-hd-on-me-woman-hero.webp" width="535" height="721" alt="" loading="lazy" decoding="async" fetchpriority="low"></div>'); })()""")
                    # staged markup (mirrors src/sections/st-article.liquid): On Me's story scene window 440 -> 604 (v1.2)
                    await pg.evaluate("document.querySelectorAll('.st-story__scene').forEach(s => { if (s.style.getPropertyValue('--y0').trim() === '440') s.style.setProperty('--y0', '604'); })")
                await pg.evaluate(HELPERS)
                await pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager')")
                for y in range(0, 30000, 700):
                    await pg.evaluate(f'window.__st({y})'); await pg.wait_for_timeout(25)
                await pg.evaluate('Promise.race([Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; }))), new Promise(r => setTimeout(r, 6000))])')
                hdr = await pg.evaluate("(() => { const e = document.querySelector('.st-header, header'); return e ? Math.round(e.getBoundingClientRect().height) : 0; })()")
                for name, sel in regions:
                    top = await pg.evaluate(f"(() => {{ const e = document.querySelector('{sel}'); return e ? e.getBoundingClientRect().top + window.__sy() : null; }})()")
                    if top is None:
                        print(f'{w}x{h} {pk}/{name}: missing'); continue
                    first = name == 'first'
                    await pg.evaluate(f'window.__st({0 if first else top - hdr})')
                    await pg.wait_for_timeout(300)
                    m = await pg.evaluate(MEASURE, [sel, hdr, first])
                    await pg.screenshot(path=str(OUT / f'{PREFIX}-{w}x{h}-{pk}-{name}.png'))
                    c = m['content']
                    print(f"{w}x{h} {pk}/{name:8} box h {m['height']}  content {c['l']}..{c['r']} ({c['ratio']}% of frame {m['frame']})  rows {c['t']}..{c['b']}"
                          f"  below fold {m['belowFold'] or '-'}  <44 {m['small'] or '-'}" if c else f'{w}x{h} {pk}/{name} no content')
                    rep[f'{w}x{h}/{pk}/{name}'] = m
                if pk != 'landing':
                    await pg.add_style_tag(content='html, body { height: auto !important; overflow: visible !important; } .page-wrapper { height: auto !important; overflow: visible !important; }')
                    await pg.wait_for_timeout(400)
                    await pg.screenshot(path=str(OUT / f'{PREFIX}-{w}x{h}-{pk}-full.png'), full_page=True)
                if pk == 'bag':
                    await pg.evaluate("fetch('/cart/clear.js', { method: 'POST' }).then(r => r.ok)")
                ovx = await pg.evaluate('document.documentElement.scrollWidth - document.documentElement.clientWidth')
                print(f'{w}x{h} {pk}: h-overflow {ovx}  errors {errs or "none"}')
                rep[f'{w}x{h}/{pk}'] = dict(overflow=ovx, errors=errs)
                await ctx.close()
        await br.close()
    (OUT / f'{PREFIX}-measurements.json').write_text(json.dumps(rep, indent=1, ensure_ascii=False), encoding='utf-8')


asyncio.run(main())
