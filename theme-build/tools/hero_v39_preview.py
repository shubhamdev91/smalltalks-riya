"""Hero v3.9 on the build preview (after install; st-fable's checks, selectors from motion/lab/soak_v39.py): the served
st-hero-motion.js md5; continuous loop (data-active-key order: at least 3 changes and a wrap back to the first set);
tap on the art pauses / resumes (aria-pressed in step); a tap on the Shop pill does not pause (default prevented, then a
real click navigates); the pause button toggles. 1536 x 703 and 390 x 844 in parallel.
Usage: python -I tools/hero_v39_preview.py"""
import asyncio, hashlib, json, sys, time, urllib.request
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
URL = 'https://0nev20-vn.myshopify.com/?preview_theme_id=186651934933'
INIT = """(() => { window.__order = []; window.__t0 = Date.now();
  const watch = () => { const h = document.querySelector('[data-st-hero]'); if (!h) return setTimeout(watch, 100);
    new MutationObserver(() => { const k = h.dataset.activeKey; if (window.__order[window.__order.length - 1]?.[0] !== k) window.__order.push([k, Math.round((Date.now() - window.__t0) / 100) / 10]); })
      .observe(h, { attributes: true, attributeFilter: ['data-active-key'] });
    window.__order.push([h.dataset.activeKey, 0]); };
  document.addEventListener('DOMContentLoaded', watch); })();"""
STATE = "(() => { const h = document.querySelector('[data-st-hero]'); const p = h.querySelector('[data-st-hero-pause]'); return { pressed: p && p.getAttribute('aria-pressed'), label: p && p.getAttribute('aria-label'), key: h.dataset.activeKey, motion: h.dataset.motion }; })()"


async def run(br, w, h):
    out = {}
    ctx = await br.new_context(viewport={'width': w, 'height': h})
    await ctx.add_init_script(INIT)
    pg = await ctx.new_page()
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)[:160]))
    await pg.goto(URL + f'&_cb={time.time_ns()}', wait_until='load', timeout=120000)
    await pg.add_style_tag(content='[id^="PBar"], #preview-bar-iframe { display: none !important; }')
    src = await pg.evaluate("[...document.scripts].map(s => s.src).find(s => s.includes('st-hero-motion')) || ''")
    out['script_md5'] = hashlib.md5(urllib.request.urlopen('https:' + src if src.startswith('//') else src).read()).hexdigest()[:8] if src else None
    # loop: wait for a wrap (the first key again after the others), up to 150 s
    for _ in range(300):
        o = await pg.evaluate('window.__order')
        keys = [k for k, _ in o]
        if len(keys) > 7 and keys[-1] == keys[0]:
            break
        await pg.wait_for_timeout(500)
    o = await pg.evaluate('window.__order')
    out['order'] = o
    keys = [k for k, _ in o]
    out['loop_ok'] = len(keys) >= 4 and len(set(keys[:7])) == min(7, len(keys)) and len(keys) > 7 and keys[7] == keys[0]
    st = lambda: pg.evaluate(STATE)
    box = await pg.evaluate("""(() => { const h = document.querySelector('[data-st-hero]'); const b = h.getBoundingClientRect();
      const r = (sel) => { const e = h.querySelector(sel); if (!e) return null; const x = e.getBoundingClientRect(); return [x.left + x.width / 2, x.top + x.height / 2]; };
      return { scene: [b.left + b.width * 0.5, b.top + b.height * 0.12], cta: r('[data-st-hero-cta]'), pause: r('[data-st-hero-pause]') }; })()""")

    async def click_at(pt):
        await pg.mouse.click(pt[0], pt[1])
        await pg.wait_for_timeout(400)
        return await st()
    out['boot'] = await st()
    out['tap_art'] = await click_at(box['scene'])
    out['tap_art_again'] = await click_at(box['scene'])
    await pg.evaluate("document.querySelector('[data-st-hero-cta]').addEventListener('click', e => { e.preventDefault(); window.__cta = (window.__cta || 0) + 1; }, { once: true })")
    out['tap_shop_pill'] = await click_at(box['cta'])
    out['shop_clicks'] = await pg.evaluate('window.__cta || 0')
    out['pause_button'] = await click_at(box['pause'])
    out['pause_button_again'] = await click_at(box['pause'])
    href = await pg.evaluate("document.querySelector('[data-st-hero-cta]').href")
    async with pg.expect_navigation(timeout=30000):
        await pg.mouse.click(box['cta'][0], box['cta'][1])
    out['shop_navigates'] = pg.url.split('?')[0] == href.split('?')[0]
    out['shop_href'] = href.split('?')[0]
    out['errors'] = errs
    await ctx.close()
    return f'{w}x{h}', out


async def main():
    async with async_playwright() as p:
        br = await p.chromium.launch(channel='chrome')
        res = await asyncio.gather(run(br, 1536, 703), run(br, 390, 844))
        await br.close()
    for size, o in res:
        print(f'== {size}: script {o["script_md5"]}  loop {"OK" if o["loop_ok"] else "FAIL"}  order {o["order"]}')
        print(f'   boot {o["boot"]}')
        print(f'   tap art -> {o["tap_art"]["pressed"]} ({o["tap_art"]["label"]}); again -> {o["tap_art_again"]["pressed"]}')
        print(f'   tap Shop pill (default prevented) -> pressed {o["tap_shop_pill"]["pressed"]}, clicks {o["shop_clicks"]}; real click navigates: {o["shop_navigates"]} ({o["shop_href"]})')
        print(f'   pause button -> {o["pause_button"]["pressed"]} ({o["pause_button"]["label"]}); again -> {o["pause_button_again"]["pressed"]}; errors {o["errors"] or "none"}')


asyncio.run(main())
