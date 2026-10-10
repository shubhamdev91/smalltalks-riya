"""st-fable: hero v3.9 soak + tap-to-pause checks on the motion lab (motion/lab/index.html via file://, the real
st-hero-motion.js + st-hero.css). Two pages in parallel (390x844, 1536x703) for SOAK seconds:
 - set order observed (data-active-key changes) and loop count;
 - live timers (wrapped setTimeout / setInterval), running animations, flyer nodes, controller.anims size;
 - JS heap (CDP Performance.getMetrics) at start / end after a forced GC;
 - long tasks (PerformanceObserver) and frame gaps > 50 ms (rAF);
then a functional pass: tap on art toggles, tap on controls / CTA / preview / tone does not, pause sticks through an
offscreen/hidden cycle, reduced motion starts paused.  Usage: python -I motion/lab/soak_v39.py [seconds]"""
import asyncio, json, pathlib, sys, time
from playwright.async_api import async_playwright
sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
HERE = pathlib.Path(__file__).resolve().parent
URL = 'http://127.0.0.1:8766/motion/lab/index.html'
SOAK = int(sys.argv[1]) if len(sys.argv) > 1 else 600

INIT = """(() => {
  const live = new Set(); window.__timers = live;
  const st = window.setTimeout, ct = window.clearTimeout, si = window.setInterval, ci = window.clearInterval;
  window.setTimeout = function (fn, ms, ...a) { const id = st.call(window, function () { live.delete(id); return typeof fn === 'function' ? fn.apply(this, arguments) : undefined; }, ms, ...a); live.add(id); return id; };
  window.clearTimeout = function (id) { live.delete(id); return ct.call(window, id); };
  window.setInterval = function (fn, ms, ...a) { const id = si.call(window, fn, ms, ...a); live.add('i' + id); return id; };
  window.clearInterval = function (id) { live.delete('i' + id); return ci.call(window, id); };
  window.__long = []; try { new PerformanceObserver((l) => l.getEntries().forEach((e) => window.__long.push(Math.round(e.duration)))).observe({ type: 'longtask', buffered: true }); } catch (e) {}
  window.__gaps = 0; window.__frames = 0; let last = 0;
  const tick = (t) => { if (last && t - last > 50) window.__gaps++; window.__frames++; last = t; requestAnimationFrame(tick); }; requestAnimationFrame(tick);
  window.__order = [];
  const watch = () => { const h = document.querySelector('[data-st-hero]'); if (!h) return setTimeout(watch, 100);
    new MutationObserver(() => { const k = h.dataset.activeKey; if (window.__order[window.__order.length - 1] !== k) window.__order.push(k); }).observe(h, { attributes: true, attributeFilter: ['data-active-key'] });
    window.__order.push(h.dataset.activeKey); };
  document.addEventListener('DOMContentLoaded', watch);
})();"""

STATE = """(() => { const h = document.querySelector('[data-st-hero]'); const c = window.STHeroMotion && window.STHeroMotion.controllers.get(h);
  const p = h.querySelector('[data-st-hero-pause]');
  return { mode: h.dataset.motion, reasons: c ? [...c.reasons] : null, anims: c ? c.anims.size : null, running: document.getAnimations().filter(a => a.playState === 'running').length,
           allAnims: document.getAnimations().length, flyers: h.querySelectorAll('.st-hero__flyer').length, timers: window.__timers.size,
           pressed: p && p.getAttribute('aria-pressed'), label: p && p.getAttribute('aria-label'), state: p && p.dataset.state,
           order: window.__order.length, long: window.__long.length, longMax: Math.max(0, ...window.__long), gaps: window.__gaps, frames: window.__frames, nodes: document.getElementsByTagName('*').length }; })()"""


async def heap(cdp):
    await cdp.send('HeapProfiler.collectGarbage')
    m = await cdp.send('Performance.getMetrics')
    d = {x['name']: x['value'] for x in m['metrics']}
    return round(d['JSHeapUsedSize'] / 1048576, 2), int(d.get('JSEventListeners', 0)), int(d.get('Nodes', 0))


async def soak(br, w, h):
    ctx = await br.new_context(viewport={'width': w, 'height': h})
    await ctx.add_init_script(INIT)
    pg = await ctx.new_page()
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
    pg.on('console', lambda m: errs.append(m.text[:200]) if m.type == 'error' else None)
    pg.on('requestfailed', lambda r: errs.append('FAIL ' + r.url[-80:]))
    pg.on('response', lambda r: errs.append(f'{r.status} ' + r.url[-80:]) if r.status >= 400 else None)
    await pg.goto(URL + f'?v=39&_={time.time_ns()}', wait_until='load')
    cdp = await ctx.new_cdp_session(pg)
    await cdp.send('Performance.enable')
    await pg.wait_for_timeout(8000)        # boot (LCP hold, decode, first set)
    h0 = await heap(cdp)
    s0 = await pg.evaluate(STATE)
    samples = []
    t0 = time.time()
    while time.time() - t0 < SOAK:
        await pg.wait_for_timeout(30000)
        s = await pg.evaluate(STATE); s['t'] = round(time.time() - t0); samples.append(s)
    h1 = await heap(cdp)
    s1 = await pg.evaluate(STATE)
    order = await pg.evaluate('window.__order')
    longs = await pg.evaluate('window.__long')
    await ctx.close()
    return dict(vp=f'{w}x{h}', heap_start=h0, heap_end=h1, start=s0, end=s1, samples=samples, order=order, long=longs, errors=errs)


async def functional(br, w, h):
    out = {}
    ctx = await br.new_context(viewport={'width': w, 'height': h})
    await ctx.add_init_script(INIT)
    pg = await ctx.new_page()
    await pg.goto(URL + f'?v=39f&_={time.time_ns()}', wait_until='load')
    await pg.wait_for_timeout(8000)
    st = lambda: pg.evaluate(STATE)
    out['boot'] = await st()
    box = await pg.evaluate("""(() => { const h = document.querySelector('[data-st-hero]'); const b = h.getBoundingClientRect();
      const r = (sel) => { const e = h.querySelector(sel); if (!e) return null; const x = e.getBoundingClientRect(); return [x.left + x.width / 2, x.top + x.height / 2]; };
      return { scene: [b.left + b.width * 0.5, b.top + b.height * 0.12], copy: r('[data-st-hero-headline]'), cta: r('[data-st-hero-cta]'), preview: r('[data-st-hero-preview]'),
               tone: r('.st-hero__controls button:last-child'), pause: r('[data-st-hero-pause]'), main: r('[data-st-hero-main]') }; })()""")
    out['points'] = box

    async def click_at(pt):
        await pg.mouse.click(pt[0], pt[1]); await pg.wait_for_timeout(350); return await st()
    out['tap_scene'] = await click_at(box['scene'])                 # expect paused (user)
    out['tap_scene_again'] = await click_at(box['scene'])           # expect playing
    out['tap_headline'] = await click_at(box['copy'])               # expect paused
    # offscreen / hidden cycle must not resume a user pause
    await pg.evaluate("window.scrollTo(0, 99999)"); await pg.wait_for_timeout(600)
    await pg.evaluate("window.scrollTo(0, 0)"); await pg.wait_for_timeout(600)
    out['after_offscreen_cycle'] = await st()                       # expect still paused
    out['tap_resume'] = await click_at(box['scene'])                # playing again
    # controls must not be swallowed: tone click changes tone, not pause; CTA is a link (prevent navigation)
    await pg.evaluate("document.querySelector('[data-st-hero-cta]').addEventListener('click', e => { e.preventDefault(); window.__cta = (window.__cta || 0) + 1; })")
    tone0 = await pg.evaluate("document.querySelector('[data-st-hero]').dataset.tone")
    if box['tone']:
        out['tap_tone'] = await click_at(box['tone']); out['tone_changed'] = tone0 != await pg.evaluate("document.querySelector('[data-st-hero]').dataset.tone")
    if box['cta']:
        out['tap_cta'] = await click_at(box['cta']); out['cta_clicks'] = await pg.evaluate('window.__cta || 0')
    out['tap_pause_button'] = await click_at(box['pause'])          # paused via button
    out['tap_pause_button_again'] = await click_at(box['pause'])    # playing
    # keyboard: pause button reachable
    out['pause_focusable'] = await pg.evaluate("(() => { const p = document.querySelector('[data-st-hero-pause]'); p.focus(); return document.activeElement === p && p.tabIndex >= 0; })()")
    await ctx.close()
    # reduced motion
    ctx = await br.new_context(viewport={'width': w, 'height': h}, reduced_motion='reduce')
    pg = await ctx.new_page()
    await pg.add_init_script(INIT)
    await pg.goto(URL + f'?v=39r&_={time.time_ns()}', wait_until='load')
    await pg.wait_for_timeout(6000)
    out['reduced'] = await pg.evaluate(STATE)
    await ctx.close()
    return out


async def main():
    async with async_playwright() as p:
        br = await p.chromium.launch(channel='chrome', args=['--js-flags=--expose-gc'])
        f = await asyncio.gather(functional(br, 390, 844), functional(br, 1536, 703))
        (HERE / 'v39-functional.json').write_text(json.dumps(f, indent=1), encoding='utf-8')
        for r in f:
            print(json.dumps({k: (v if not isinstance(v, dict) else {kk: v.get(kk) for kk in ('mode', 'reasons', 'pressed', 'label', 'state')}) for k, v in r.items() if k != 'points'}, ensure_ascii=False))
        res = await asyncio.gather(soak(br, 390, 844), soak(br, 1536, 703))
        await br.close()
    (HERE / 'v39-soak.json').write_text(json.dumps(res, indent=1), encoding='utf-8')
    for r in res:
        o = r['order']; loops = (len(o) - 1) / 7
        print(r['vp'], 'heap MB start/end', r['heap_start'], r['heap_end'], 'sets', len(o), 'loops %.1f' % loops, 'order head', o[:9])
        print('   start', {k: r['start'][k] for k in ('timers', 'anims', 'running', 'allAnims', 'flyers', 'nodes')}, 'end', {k: r['end'][k] for k in ('timers', 'anims', 'running', 'allAnims', 'flyers', 'nodes', 'long', 'longMax', 'gaps', 'frames')})
        print('   errors', r['errors'] or 'none')


asyncio.run(main())
