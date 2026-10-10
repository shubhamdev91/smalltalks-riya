"""Journal index + a story at 320 / 390 on the preview: waits until the compiled CSS has the new sentence rule, then
checks scrollWidth, H1 size vs the margin note (no overlap), card image width, clipped card text, story body colour,
and writes qa/fidelity/journal-<w>.png / journal-story-<w>.png."""
import asyncio, json, pathlib, sys, time
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')
QA = pathlib.Path(__file__).resolve().parents[2] / 'qa/fidelity'
O = 'https://0nev20-vn.myshopify.com'
Q = 'preview_theme_id=186651934933'
INDEX = r'''(() => { const r = e => e.getBoundingClientRect();
  const h1 = document.querySelector('.st-journal__title'), note = document.querySelector('.st-journal__note');
  const range = document.createRange(); range.selectNodeContents(h1); const a = range.getBoundingClientRect(), b = r(note);
  const overlap = !(a.right <= b.left || b.right <= a.left || a.bottom <= b.top || b.bottom <= a.top);
  const clipped = [...document.querySelectorAll('.st-jcard__text')].filter(t => t.scrollWidth > t.clientWidth + 1).length;
  return { scrollW: document.documentElement.scrollWidth, h1: getComputedStyle(h1).fontSize, h1InkRight: Math.round(a.right), h1InkBottom: Math.round(a.bottom), noteLeft: Math.round(b.left), noteTop: Math.round(b.top), noteBottom: Math.round(b.bottom), overlap,
           media: Math.round(r(document.querySelector('.st-jcard__media')).width), clippedCards: clipped,
           sent: getComputedStyle(document.querySelector('.st-sent')).display }; })()'''
STORY = r'''(() => ({ scrollW: document.documentElement.scrollWidth, body: getComputedStyle(document.querySelector('.st-story__beat p')).color,
  sent: getComputedStyle(document.querySelector('.st-sent')).display }))()'''


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        for attempt in range(8):
            pg = await b.new_page(viewport={'width': 320, 'height': 700})
            await pg.goto(f'{O}/blogs/journal?{Q}&_cb={time.time_ns()}', wait_until='load')
            ok = await pg.evaluate("getComputedStyle(document.querySelector('.st-sent')).display") == 'inline-block'
            await pg.close()
            if ok:
                break
            await asyncio.sleep(5)
        for w in (320, 390):
            pg = await b.new_page(viewport={'width': w, 'height': 800}, device_scale_factor=1)
            await pg.goto(f'{O}/blogs/journal?{Q}&_cb={time.time_ns()}', wait_until='load'); await pg.wait_for_timeout(1200)
            print(w, 'index', json.dumps(await pg.evaluate(INDEX)))
            await pg.screenshot(path=str(QA / f'journal-{w}.png'), full_page=True)
            await pg.goto(f'{O}/blogs/journal/green-flag?{Q}&_cb={time.time_ns()}', wait_until='load'); await pg.wait_for_timeout(1200)
            print(w, 'story', json.dumps(await pg.evaluate(STORY)))
            await pg.screenshot(path=str(QA / f'journal-story-{w}.png'), full_page=True)
            await pg.close()
        await b.close()

asyncio.run(main())
