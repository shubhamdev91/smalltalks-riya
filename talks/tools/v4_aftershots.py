"""v4_aftershots.py: after-shots of the INSTALLED talks v4 window on the build preview, for st-fable / the orchestrator.
- hub / thread / composer (focused, typed) at 390, 1536, 1920; header crops at 390, 1536, 1920;
- st-header on non-talks pages (home, a PDP, /blogs/journal) at 390 and 1536, plus the phone drawer open;
- one REAL post through /apps/talks while the store switch is closed: it must be refused with the "posting is paused"
  line (TLK-130) and nothing is saved (the backend refuses before any write).
Output: qa/talks/v4-after/*.png + a JSON summary line per check.  Usage: python -I talks/tools/v4_aftershots.py"""
import asyncio, json, os, sys, time
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')
BASE, Q = 'https://0nev20-vn.myshopify.com', '?preview_theme_id=186651934933'
OUT = 'qa/talks/v4-after'
os.makedirs(OUT, exist_ok=True)
HIDE = ('[id^="PBar"], #preview-bar-iframe { display: none !important; } html, body { scroll-behavior: auto !important; } '
        '*, *::before, *::after { transition: none !important; animation: none !important; caret-color: transparent !important; }')
THREAD = '/pages/talk/what-s-your-smallest-friendship-green-flag'


async def open_(b, path, w, h, dpr=1):
    pg = await b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=dpr)
    await pg.goto(f'{BASE}{path}{Q}&_cb={time.time_ns()}', wait_until='networkidle', timeout=60000)
    await pg.add_style_tag(content=HIDE)
    await pg.evaluate('document.fonts.ready')
    await pg.wait_for_timeout(500)
    return pg


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        for w, h in ((390, 844), (1536, 864), (1920, 1080)):
            pg = await open_(b, '/blogs/the-talks', w, h)
            facts = await pg.evaluate("""() => ({composer: !!document.querySelector('[data-st-compose]'), live: JSON.parse(document.querySelector('#st-talks-config').textContent).live,
              dock: getComputedStyle(document.querySelector('.tk-dock') || document.body).display, options: [...document.querySelectorAll('[data-st-topic] option')].map(o => o.textContent.trim()),
              asLine: document.querySelector('[data-st-as]')?.textContent, overflow: document.scrollingElement.scrollWidth - innerWidth})""")
            print(f'hub@{w}', json.dumps(facts, ensure_ascii=False))
            await pg.screenshot(path=f'{OUT}/hub-{w}.png')
            await pg.screenshot(path=f'{OUT}/header-{w}.png', clip={'x': 0, 'y': 0, 'width': w, 'height': 80})
            # composer: focused + typed (her own draft, nothing sent)
            await pg.click('[data-st-compose] textarea')
            await pg.keyboard.type('okay so this just happened…')
            await pg.wait_for_timeout(200)
            await pg.evaluate("document.querySelector('.tk-start').scrollIntoView({block: 'start'})")
            await pg.evaluate("window.scrollBy(0, -90)")
            await pg.wait_for_timeout(200)
            dock = await pg.evaluate("getComputedStyle(document.querySelector('.tk-dock') || document.body).display")
            print(f'composer@{w} dock-while-typing:', dock)
            await pg.screenshot(path=f'{OUT}/composer-{w}.png')
            await pg.evaluate("localStorage.removeItem('st-talks-draft')")
            await pg.close()
            pg = await open_(b, THREAD, w, h)
            facts = await pg.evaluate("""() => ({replyForm: !!document.querySelector('[data-st-reply-form]'), own: !!document.querySelector('.tk-own'),
              none: document.querySelector('[data-st-empty]')?.textContent.trim(), overflow: document.scrollingElement.scrollWidth - innerWidth})""")
            print(f'thread@{w}', json.dumps(facts, ensure_ascii=False))
            await pg.screenshot(path=f'{OUT}/thread-{w}.png')
            await pg.close()

        # one real post while the store switch is closed: refused, nothing saved
        pg = await open_(b, '/pages/talks/tiny-wins', 390, 844)
        calls = []
        pg.on('response', lambda r: calls.append((r.status, r.url.split('?')[0])) if '/apps/talks' in r.url else None)
        await pg.click('[data-st-compose] textarea')
        await pg.keyboard.type('closed-switch check, please ignore')
        await pg.click('[data-st-compose] .tk-post')
        await pg.wait_for_timeout(4500)
        msg = await pg.evaluate("document.querySelector('[data-st-compose] [data-st-status]').textContent")
        kept = await pg.evaluate("document.querySelector('[data-st-compose] textarea').value")
        rows_mine = await pg.evaluate("document.querySelectorAll('.tk-r.is-mine').length")
        print('closed-switch post:', json.dumps({'calls': calls, 'message': msg, 'text_kept': kept, 'my_rows_left': rows_mine}, ensure_ascii=False))
        await pg.evaluate("localStorage.removeItem('st-talks-draft')")
        await pg.close()

        for name, path in (('home', '/'), ('pdp', '/products/bill-idhar'), ('journal', '/blogs/journal')):
            for w, h in ((390, 844), (1536, 864)):
                pg = await open_(b, path, w, h, dpr=2)
                await pg.screenshot(path=f'{OUT}/nontalks-{name}-{w}.png', clip={'x': 0, 'y': 0, 'width': w, 'height': 80})
                if w == 390:
                    await pg.click('.st-header__menu-button')
                    await pg.wait_for_timeout(500)
                    talks = await pg.evaluate("""() => { const a = document.querySelector('.st-drawer__talks'); const s = a?.querySelector('svg')?.getBoundingClientRect();
                      return {name: a?.querySelector('.visually-hidden')?.textContent, mark: s ? [Math.round(s.width), Math.round(s.height)] : null}; }""")
                    print(f'drawer@{name}', json.dumps(talks))
                    await pg.screenshot(path=f'{OUT}/nontalks-{name}-drawer-390.png')
                await pg.close()
        await b.close()

asyncio.run(main())
