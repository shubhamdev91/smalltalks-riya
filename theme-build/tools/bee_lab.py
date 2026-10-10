"""Laptop beeline lab (owner v12.1c / v12.1d), nothing written: lab/landing.html served over http from 127.0.0.1 (so the
art is same-origin and the canvas alpha read works, as on the store's CDN), the staged st-chapter script draws the line,
then st-fable's independent acceptance probe (qa/desktop/owner-v12/accept_bee.js) measures it per section: min distance
to copy / pills, samples on art ink (alpha > 12), sharpest turn per 24 px, longest near-straight run. Also: the time from
a resize to the redrawn line, page errors, and a whole-page shot. Needs `python -m http.server 8765 --bind 127.0.0.1
--directory <Riya>` running. Output: qa/desktop/owner-v12/bee-staged-<WxH>.png and bee-staged.json.
Usage: python -I tools/bee_lab.py [WxH ...]"""
import asyncio, json, pathlib, re, sys, time
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
TB = pathlib.Path(__file__).resolve().parents[1]
ROOT = TB.parent
OUT = ROOT / 'qa/desktop/owner-v12'
SIZES = [tuple(int(v) for v in a.split('x')) for a in sys.argv[1:] if re.fullmatch(r'\d+x\d+', a)] or [(1280, 720), (1536, 703), (1680, 1050), (1920, 1080)]
GROW = 'html, body { height: auto !important; overflow: visible !important; }'


def http_lab():
    s = (TB / 'lab/landing.html').read_text(encoding='utf-8')
    s = s.replace(ROOT.as_uri() + '/', '/')
    (TB / 'lab/landing-http.html').write_text(s, encoding='utf-8')
    return 'http://127.0.0.1:8765/theme-build/lab/landing-http.html'


async def main():
    url = http_lab()
    probe = (OUT / 'accept_bee.js').read_text(encoding='utf-8')
    rep = {}
    async with async_playwright() as p:
        br = await p.chromium.launch(channel='chrome')
        for w, h in SIZES:
            ctx = await br.new_context(viewport={'width': w, 'height': h}, device_scale_factor=1)
            pg = await ctx.new_page()
            errs = []
            pg.on('pageerror', lambda e: errs.append(str(e)[:160]))
            await pg.goto(f'{url}?_cb={time.time_ns()}', wait_until='load', timeout=120000)
            await pg.evaluate("document.querySelectorAll('.st-land').forEach(s => s.style.contentVisibility = 'visible')")
            # every image loaded and decoded (as accept_bee.py does), then the line redrawn from the complete art
            await pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager')")
            for y in range(0, 16000, 600):
                await pg.evaluate(f'window.scrollTo(0, {y})')
                await pg.wait_for_timeout(25)
            await pg.evaluate("Promise.race([Promise.all([...document.images].map(i => (i.complete ? Promise.resolve() : new Promise(r => { i.onload = i.onerror = r; })).then(() => i.decode ? i.decode().catch(() => 0) : 0))), new Promise(r => setTimeout(r, 10000))])")
            print('   images not loaded:', await pg.evaluate("[...document.images].filter(i => i.getAttribute('src') && (!i.complete || !i.naturalWidth)).map(i => i.src.split('/').pop())"))
            await pg.evaluate('window.scrollTo(0, 0); dispatchEvent(new Event("resize"))')
            await pg.wait_for_timeout(2500)
            for _ in range(150):
                if await pg.evaluate("!!document.querySelector('svg.st-beecur path[d]')"):
                    break
                await pg.wait_for_timeout(100)
            await pg.wait_for_timeout(500)
            # redraw timing: resize -> new path
            ms = await pg.evaluate("""new Promise((res) => { const p = document.querySelector('svg.st-beecur path'); const d0 = p.getAttribute('d');
              const t0 = performance.now(); document.body.style.paddingRight = '1px'; dispatchEvent(new Event('resize'));
              const tick = () => { const q = document.querySelector('svg.st-beecur path'); if (q && q.getAttribute('d') !== d0) res(Math.round(performance.now() - t0 - 150)); else if (performance.now() - t0 > 8000) res(-1); else setTimeout(tick, 20); }; tick(); })""")
            await pg.evaluate("document.body.style.paddingRight = ''; dispatchEvent(new Event('resize'))")
            await pg.wait_for_timeout(1500)
            await pg.add_script_tag(content=probe)
            r = await pg.evaluate('window.__acceptBee()')
            r['errors'] = errs
            r['redraw_ms'] = ms
            rep[f'{w}x{h}'] = r
            S = r.get('sections') or {}
            bad = {k: v for k, v in S.items() if v['minCopy'] < 12 or v['onInk'] or v['maxTurnPer24px'] > 45 or v['straightRun'] > 120}
            print(f'{w}x{h}: alpha {r.get("alphaOk")}  sections {len(S)}  redraw ~{ms} ms  errors {errs or "none"}')
            for k, v in S.items():
                print(f'   {k:20} minCopy {v["minCopy"]:4}  onInk {v["onInk"]:3}  maxTurn/24px {v["maxTurnPer24px"]:5}  straight {v["straightRun"]:4}'
                      f'{"   <-- " + str(v["worst"]) if k in bad else ""}')
            await pg.add_style_tag(content=GROW)
            await pg.wait_for_timeout(300)
            await pg.screenshot(path=str(OUT / f'bee-staged-{w}x{h}.png'), full_page=True, animations='disabled')
            await ctx.close()
        await br.close()
    (OUT / 'bee-staged.json').write_text(json.dumps(rep, indent=1), encoding='utf-8')


asyncio.run(main())
