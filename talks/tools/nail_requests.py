"""Which nail sheets does each talks page request? Lists every st-nails-* (P1) and st-hd-nails-* (HD) request on the
hub, a topic and a thread at 390 (preview theme), after scrolling to the bottom so lazy art loads, and which elements
reference P1 sheets. Usage: python -I nail_requests.py [out.json]"""
import asyncio, json, sys, time
from playwright.async_api import async_playwright

ROUTES = ['/blogs/the-talks', '/pages/talks/tiny-wins', '/pages/talk/what-s-your-smallest-friendship-green-flag']
OUT = sys.argv[1] if len(sys.argv) > 1 else None


async def main():
    report = {}
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        for r in ROUTES:
            ctx = await b.new_context(viewport={'width': 390, 'height': 900})
            pg = await ctx.new_page()
            reqs = []
            pg.on('request', lambda q: reqs.append(q.url) if 'nails-' in q.url else None)
            await pg.goto(f'https://0nev20-vn.myshopify.com{r}?preview_theme_id=186651934933&_cb={time.time_ns()}', wait_until='networkidle', timeout=60000)
            for _ in range(12):
                await pg.mouse.wheel(0, 700)
                await pg.wait_for_timeout(150)
            await pg.wait_for_load_state('networkidle')
            refs = await pg.evaluate("""() => {
                const hits = [];
                for (const el of document.querySelectorAll('[style*="nails-"]')) {
                    const m = el.getAttribute('style').match(/(st-(?:hd-)?nails-[a-z-]+)\\.webp/);
                    if (m && !m[1].startsWith('st-hd-')) hits.push((el.className || el.tagName) + ' <- ' + m[1]);
                }
                const cfg = document.getElementById('st-talks-config');
                const sprites = cfg ? Object.values(JSON.parse(cfg.textContent).sprites || {}).map(u => u.split('/').pop().split('?')[0]) : [];
                return { p1_style_refs: hits, config_sprites: sprites };
            }""")
            name = lambda u: u.split('/')[-1].split('?')[0]
            report[r] = {'p1_requests': sorted({name(u) for u in reqs if '/st-nails-' in u}),
                         'hd_requests': sorted({name(u) for u in reqs if '/st-hd-nails-' in u}), **refs}
            await ctx.close()
        await b.close()
    print(json.dumps(report, indent=1))
    if OUT:
        json.dump(report, open(OUT, 'w', encoding='utf-8'), indent=1)

asyncio.run(main())
