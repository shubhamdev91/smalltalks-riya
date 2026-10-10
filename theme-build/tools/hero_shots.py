"""Hero shots on the preview (hero v3.8 desktop check): at 1280x720, 1440x800, 1536x703 and 390x844, pause the motion and
shoot all 7 set states (advancing with a real click on the visible part of the "next set" preview; a forced click
scrolls the overflow-hidden hero), plus at >= 990 one shot across the hero -> tiles join (scrolling .page-wrapper,
Horizon's scroller there). Also the hero's box, its join with the tiles, and page errors.
Shots: qa/fidelity/<prefix>-hero-<WxH>-<n>.png, <prefix>-hero-<WxH>-join.png. Usage: python -I tools/hero_shots.py <prefix>"""
import asyncio, json, pathlib, sys, time
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
TB = pathlib.Path(__file__).resolve().parents[1]
QA = TB.parent / 'qa/fidelity'
O = 'https://0nev20-vn.myshopify.com'
Q = 'preview_theme_id=186651934933'
PREFIX = sys.argv[1] if len(sys.argv) > 1 else 'hero'
VIEWS = [(1280, 720), (1440, 800), (1536, 703), (390, 844)]


async def visible_click(pg, sel):
    b = await pg.evaluate(f"""(() => {{ const e = document.querySelector('{sel}'); if (!e) return null; const r = e.getBoundingClientRect();
      const x0 = Math.max(r.left, 0), x1 = Math.min(r.right, innerWidth), y0 = Math.max(r.top, 0), y1 = Math.min(r.bottom, innerHeight);
      return x1 > x0 && y1 > y0 ? [(x0 + x1) / 2, (y0 + y1) / 2] : null; }})()""")
    if b:
        await pg.mouse.click(b[0], b[1])
    return bool(b)


async def main():
    out = {}
    async with async_playwright() as p:
        br = await p.chromium.launch(channel='chrome')
        for w, h in VIEWS:
            ctx = await br.new_context(viewport={'width': w, 'height': h}, device_scale_factor=1 if w > 600 else 2)
            pg = await ctx.new_page()
            errs = []
            pg.on('pageerror', lambda e: errs.append(str(e)[:120]))
            await pg.goto(f'{O}/?{Q}&_cb={time.time_ns()}', wait_until='load', timeout=120000)
            await pg.add_style_tag(content='[id^="PBar"], #preview-bar-iframe { display: none !important; }')
            # pause once the first set's intro has finished (headline fully in), so state 1 isn't caught mid-fade
            for _ in range(40):
                if await pg.evaluate("(() => { const h = document.querySelector('[data-st-hero-headline]'); return h && getComputedStyle(h).opacity === '1'; })()"):
                    break
                await pg.wait_for_timeout(150)
            paused = await visible_click(pg, '[data-st-hero-pause]')
            await pg.wait_for_timeout(800)
            tag = f'{w}x{h}'
            names = []
            for n in range(7):
                label = await pg.evaluate("(document.querySelector('[data-st-hero-preview]') || {}).ariaLabel || ''")
                cur = await pg.evaluate("(document.querySelector('[data-st-hero]') || {}).dataset ? (document.querySelector('[data-st-hero-main]') || {}).ariaLabel || '' : ''")
                await pg.screenshot(path=str(QA / f'{PREFIX}-hero-{tag}-{n + 1}.png'))
                names.append(label)
                if n < 6:
                    await visible_click(pg, '[data-st-hero-preview]')
                    await pg.wait_for_timeout(1600)
            geo = await pg.evaluate("""(() => { const hero = document.querySelector('[data-st-hero]'); const tiles = document.querySelector('.st-land[data-land="tiles"]');
              const hb = hero && hero.getBoundingClientRect(), tb = tiles && tiles.getBoundingClientRect(); const hdr = document.querySelector('.st-header');
              return { hero: hb && [Math.round(hb.top), Math.round(hb.height)], tilesTop: tb && Math.round(tb.top), header: hdr && Math.round(hdr.getBoundingClientRect().height),
                       overflowX: document.documentElement.scrollWidth - document.documentElement.clientWidth }; })()""")
            if w >= 990:
                await pg.evaluate("""(() => { const hero = document.querySelector('[data-st-hero]'); const w = document.querySelector('.page-wrapper');
                  const y = hero.getBoundingClientRect().bottom - innerHeight / 2; if (w && /(auto|scroll)/.test(getComputedStyle(w).overflowY)) w.scrollTop += y; else window.scrollBy(0, y); })()""")
                await pg.wait_for_timeout(900)
                await pg.screenshot(path=str(QA / f'{PREFIX}-hero-{tag}-join.png'))
            out[tag] = dict(geo, paused=paused, next_labels=names, errors=errs)
            print(tag, json.dumps(out[tag], ensure_ascii=False)[:400])
            await ctx.close()
        await br.close()
    (QA / f'{PREFIX}-hero-measurements.json').write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding='utf-8')


asyncio.run(main())
