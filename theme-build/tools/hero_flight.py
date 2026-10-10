"""One live mid-flight hero frame on the preview at 1280x720, in a headed (visible) Chrome window so document.timeline
runs (a hidden pane freezes it at 0). After the intro, pause the autoplay, then click the visible part of the "next set"
preview (the 500 ms next-set flight) and shoot while the flyer (.st-hero__flyer) is in the air; its animation progress
and document.timeline.currentTime are read right before and right after the shot. Retries on the following sets until
both readings fall inside the flight (progress 0.15-0.85). Shot: qa/fidelity/<prefix>-hero-1280x720-midflight.png plus
<prefix>-hero-1280x720-midflight.json. Usage: python -I tools/hero_flight.py <prefix>"""
import asyncio, json, pathlib, sys, time
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
TB = pathlib.Path(__file__).resolve().parents[1]
QA = TB.parent / 'qa/fidelity'
URL = 'https://0nev20-vn.myshopify.com/?preview_theme_id=186651934933'
PREFIX = sys.argv[1] if len(sys.argv) > 1 else 'flight'

PROBE = """() => { const f = document.querySelector('.st-hero__flyer'); const a = f && f.getAnimations()[0];
  const t = a && a.effect.getComputedTiming(); const b = f && f.getBoundingClientRect();
  return { timeline: document.timeline.currentTime, flyer: !!f, progress: t ? t.progress : null,
           box: b ? [Math.round(b.left), Math.round(b.top), Math.round(b.width), Math.round(b.height)] : null,
           label: (document.querySelector('[data-st-hero-preview]') || {}).ariaLabel || '' }; }"""


async def visible_click(pg, sel):
    b = await pg.evaluate(f"""(() => {{ const e = document.querySelector('{sel}'); if (!e) return null; const r = e.getBoundingClientRect();
      const x0 = Math.max(r.left, 0), x1 = Math.min(r.right, innerWidth), y0 = Math.max(r.top, 0), y1 = Math.min(r.bottom, innerHeight);
      return x1 > x0 && y1 > y0 ? [(x0 + x1) / 2, (y0 + y1) / 2] : null; }})()""")
    if b:
        await pg.mouse.click(b[0], b[1])
    return bool(b)


async def main():
    async with async_playwright() as p:
        br = await p.chromium.launch(channel='chrome', headless=False)
        ctx = await br.new_context(viewport={'width': 1280, 'height': 720}, device_scale_factor=1, reduced_motion='no-preference')
        pg = await ctx.new_page()
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)[:120]))
        await pg.goto(f'{URL}&_cb={time.time_ns()}', wait_until='load', timeout=120000)
        await pg.bring_to_front()
        await pg.add_style_tag(content='[id^="PBar"], #preview-bar-iframe { display: none !important; }')
        for _ in range(60):
            if await pg.evaluate("(() => { const h = document.querySelector('[data-st-hero-headline]'); return h && getComputedStyle(h).opacity === '1'; })()"):
                break
            await pg.wait_for_timeout(150)
        t0 = await pg.evaluate('document.timeline.currentTime')
        await pg.wait_for_timeout(500)
        t1 = await pg.evaluate('document.timeline.currentTime')
        print(f'timeline running: {t0:.0f} -> {t1:.0f} ms')
        await visible_click(pg, '[data-st-hero-pause]')
        await pg.wait_for_timeout(1200)
        rec = None
        for attempt in range(8):
            label = await pg.evaluate("(document.querySelector('[data-st-hero-preview]') || {}).ariaLabel || ''")
            await visible_click(pg, '[data-st-hero-preview]')
            for _ in range(40):
                pre = await pg.evaluate(PROBE)
                if pre['flyer'] and pre['progress'] is not None and pre['progress'] >= 0.15:
                    break
                await pg.wait_for_timeout(10)
            out = QA / f'{PREFIX}-hero-1280x720-midflight.png'
            await pg.screenshot(path=str(out))
            post = await pg.evaluate(PROBE)
            ok = pre['flyer'] and pre['progress'] is not None and 0.15 <= pre['progress'] <= 0.85 and post['flyer'] and post['progress'] is not None and post['progress'] <= 0.85
            print(f'attempt {attempt + 1} ({label}): before shot {json.dumps(pre)}  after shot {json.dumps(post)}  {"OK" if ok else "retry"}')
            if ok:
                rec = dict(attempt=attempt + 1, clicked=label, before_shot=pre, after_shot=post, timeline_check=[t0, t1], errors=errs)
                break
            await pg.wait_for_timeout(1500)
        (QA / f'{PREFIX}-hero-1280x720-midflight.json').write_text(json.dumps(rec or {'failed': True, 'errors': errs}, indent=1, ensure_ascii=False), encoding='utf-8')
        print('errors', errs or 'none')
        await ctx.close()
        await br.close()


asyncio.run(main())
