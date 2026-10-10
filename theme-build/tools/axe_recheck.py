"""axe re-run against qa/sonnet/raw/axe baselines (same axe-core 4.10.2 from cdnjs, same exclusions). Prints, per page and
width, the rules that cleared, stayed and appeared. /cart is run with one test item, cleared afterwards.
Usage: python -I tools/axe_recheck.py"""
import asyncio, json, pathlib, sys, time, urllib.request
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
TB = pathlib.Path(__file__).resolve().parents[1]
BASE = TB.parent / 'qa/sonnet/raw/axe'
O = 'https://0nev20-vn.myshopify.com'
Q = 'preview_theme_id=186651934933'
AXE = urllib.request.urlopen('https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.2/axe.min.js', timeout=30).read().decode('utf8')
RUNS = [('home', '/', (390, 1280)), ('products-bill-idhar', '/products/bill-idhar', (390, 1280)),
        ('collections-all', '/collections/all', (390, 1280)), ('cart-with-item', '/cart', (390, 1280)),
        ('search-q-lilac', '/search?q=lilac', (390, 1280)), ('search-q-zzzz', '/search?q=zzzz', (390, 1280)),
        ('pages-the-talks', '/pages/the-talks', (390,))]
RUN = """async () => { const r = await axe.run({exclude: [['#preview-bar-iframe'], ['#PBarNextFrame']]}, {resultTypes: ['violations', 'incomplete']});
  return { v: r.violations.map(x => [x.id, x.impact, x.nodes.length, x.nodes[0] && x.nodes[0].target.join(' ')]), i: r.incomplete.map(x => [x.id, x.nodes.length]) }; }"""


def baseline(slug, w):
    f = BASE / f'{slug}-{w}.json'
    if not f.exists():
        return None, None
    d = json.load(open(f, encoding='utf-8'))
    r = d.get('results', d)
    return ({v['id'] for v in r.get('violations', [])}, {v['id'] for v in r.get('incomplete', [])})


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        for slug, path, widths in RUNS:
            for w in widths:
                ctx = await b.new_context(viewport={'width': w, 'height': 900})
                pg = await ctx.new_page()
                if slug == 'cart-with-item':
                    await pg.goto(f'{O}/?{Q}&_cb={time.time_ns()}', wait_until='load', timeout=90000)
                    vid = await pg.evaluate("fetch('/products/bill-idhar.js').then(r => r.json()).then(p => p.variants[0].id)")
                    await pg.evaluate(f"fetch('/cart/add.js', {{ method: 'POST', headers: {{ 'Content-Type': 'application/json' }}, body: JSON.stringify({{ items: [{{ id: {vid}, quantity: 1 }}] }}) }})")
                sep = '&' if '?' in path else '?'
                await pg.goto(f'{O}{path}{sep}{Q}&_cb={time.time_ns()}', wait_until='load', timeout=90000)
                await pg.wait_for_timeout(1500)
                await pg.add_script_tag(content=AXE)
                r = await pg.evaluate(RUN)
                if slug == 'cart-with-item':
                    await pg.evaluate("fetch('/cart/clear.js', { method: 'POST' })")
                now_v = {x[0] for x in r['v']}
                now_i = {x[0] for x in r['i']}
                bv, bi = baseline(slug, w)
                if bv is None:
                    print(f'{slug} {w}: no baseline; violations {sorted(now_v)}')
                else:
                    print(f'{slug} {w}: cleared {sorted(bv - now_v)} | still {sorted(bv & now_v)} | new {sorted(now_v - bv)} | '
                          f'incomplete cleared {sorted(bi - now_i)} new {sorted(now_i - bi)}')
                for x in r['v']:
                    if x[0] in (now_v - (bv or set())) or x[0] in ((bv or set()) & now_v):
                        print('     ', x)
                await ctx.close()
        await b.close()


asyncio.run(main())
