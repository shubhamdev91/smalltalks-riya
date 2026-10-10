"""Journal story checks on the preview: pager drives the beats (status, disabled ends, ArrowRight on the track), and all
seven stories render (200, clean, eyebrow from the category tag, 5 beats, hero, More stories ×3, scrollWidth)."""
import asyncio, json, sys, time
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')
O = 'https://0nev20-vn.myshopify.com/blogs/journal/'
Q = '?preview_theme_id=186651934933&_cb='
STATE = "(() => ({ status: document.querySelector('[data-st-beats-status]')?.textContent.trim(), prevDisabled: document.querySelector('[data-st-beats-prev]')?.disabled, nextDisabled: document.querySelector('[data-st-beats-next]')?.disabled, scrollLeft: Math.round(document.querySelector('[data-st-beats-track]')?.scrollLeft || 0) }))()"


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        pg = await b.new_page(viewport={'width': 390, 'height': 844})
        errs = []
        pg.on('pageerror', lambda e: errs.append('PAGEERROR ' + str(e)[:160]))
        await pg.goto(O + 'brainwave' + Q + str(time.time_ns()), wait_until='load'); await pg.wait_for_timeout(1000)
        print('start', await pg.evaluate(STATE))
        await pg.click('[data-st-beats-next]'); await pg.wait_for_timeout(900)
        print('after ›', await pg.evaluate(STATE))
        await pg.focus('[data-st-beats-track]'); await pg.keyboard.press('ArrowRight'); await pg.wait_for_timeout(900)
        print('after ArrowRight', await pg.evaluate(STATE))
        for _ in range(4):
            await pg.click('[data-st-beats-next]', force=True); await pg.wait_for_timeout(700)
        print('at end', await pg.evaluate(STATE))
        for h in ('on-me', 'brainwave', 'green-flag', 'shaadi-shift', 'diet-cherry', 'wild-card', 'pinky-promise'):
            resp = await pg.goto(O + h + Q + str(time.time_ns()), wait_until='load'); await pg.wait_for_timeout(400)
            html = await pg.content()
            info = await pg.evaluate("""(() => ({ eyebrow: document.querySelector('.st-story__eyebrow')?.innerText, title: document.querySelector('h1')?.textContent.trim(),
              beats: document.querySelectorAll('.st-story__beat').length, hero: !!document.querySelector('.st-story__hero img'), pull: document.querySelector('.st-story__pull')?.innerText.split('\\n').length,
              cta: document.querySelector('.st-story__cta')?.textContent.trim().replace(/\\s+/g, ' '), more: [...document.querySelectorAll('.st-story__more-name')].map(e => e.textContent.trim()),
              scrollW: document.documentElement.scrollWidth }))()""")
            print(h, resp.status, [x for x in ('Liquid error', 'translation missing') if x in html] or 'clean', json.dumps(info, ensure_ascii=False))
        print('page errors:', errs or 'none')
        await b.close()

asyncio.run(main())
