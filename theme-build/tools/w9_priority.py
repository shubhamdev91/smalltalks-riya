"""Home at 390 (DPR 2, fresh profile, Slow 4G + 4x CPU): the head preloads, then every image request in start order with its
Chrome fetch priority (initial and after any change), and the header logo's attributes. The goal: only the hero tone and
the set 1 (On Me) sheet at High; the header logo eager at default priority. Also Liquid / JS errors."""
import asyncio, pathlib, re, sys, time
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
O = 'https://0nev20-vn.myshopify.com'
Q = 'preview_theme_id=186651934933'


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        ctx = await b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2)
        pg = await ctx.new_page()
        cdp = await ctx.new_cdp_session(pg)
        await cdp.send('Network.enable')
        await cdp.send('Network.emulateNetworkConditions', {'offline': False, 'latency': 150, 'downloadThroughput': 1.6e6 / 8, 'uploadThroughput': 750e3 / 8})
        await cdp.send('Emulation.setCPUThrottlingRate', {'rate': 4})
        reqs, t0 = {}, [None]
        def sent(e):
            u = e['request']['url']
            if not re.search(r'\.(webp|png|jpe?g|avif|gif|svg)(\?|$)', u.split('#')[0]):
                return
            if t0[0] is None:
                t0[0] = e['timestamp']
            reqs.setdefault(e['requestId'], {'name': u.split('?')[0].split('/')[-1], 't': e['timestamp'], 'init': e['request'].get('initialPriority'), 'final': e['request'].get('initialPriority'), 'type': e.get('type')})
        def changed(e):
            if e['requestId'] in reqs:
                reqs[e['requestId']]['final'] = e['newPriority']
        cdp.on('Network.requestWillBeSent', sent)
        cdp.on('Network.resourceChangedPriority', changed)
        errs = []
        pg.on('pageerror', lambda e: errs.append('PAGEERROR ' + str(e)[:150]))
        pg.on('console', lambda m: errs.append('console ' + m.text[:150]) if m.type == 'error' else None)
        await pg.goto(f'{O}/?{Q}&_cb={time.time_ns()}', wait_until='load', timeout=180000)
        await pg.wait_for_timeout(5000)
        html = await pg.content()
        head = html.split('</head>')[0]
        print('head preloads:')
        for l in re.findall(r'<link[^>]*rel="preload"[^>]*>', head):
            print('   ', re.sub(r'(href|imagesrcset)="[^"]*/([^"/?]+)[^"]*"', r'\1=".../\2"', l)[:170])
        print('header logo:', await pg.evaluate("""(() => { const i = document.querySelector('.st-header__bar > .st-logo img'); return i && { src: i.src.split('/').pop().split('?')[0],
            fetchpriority: i.getAttribute('fetchpriority'), loading: i.getAttribute('loading'), width: i.getAttribute('width'), height: i.getAttribute('height') }; })()"""))
        rows = sorted(reqs.values(), key=lambda r: r['t'])
        print('image requests in start order (ms from first, name, initial -> final priority):')
        for r in rows[:14]:
            print(f"   {round((r['t'] - t0[0]) * 1000):6} ms  {r['name'][:44]:44}  {r['init']} -> {r['final']}")
        high = [r['name'] for r in rows if r['final'] in ('High', 'VeryHigh')]
        print('images at High / VeryHigh:', high)
        print('liquid', [x for x in ('Liquid error', 'translation missing') if x in html] or 'clean', '| errors',
              [e for e in errs if 'shop.app' not in e and 'Content Security' not in e and 'status of 403' not in e] or 'none')
        await b.close()


asyncio.run(main())
