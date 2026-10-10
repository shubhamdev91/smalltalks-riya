"""Desktop layout probe for the talks (qa/desktop/STORE-DESKTOP-SPEC.md §2).
mode 'proto': injects talks/staged/desktop/desktop.css (+ wraps the hub feed like the staged markup) into the preview.
mode 'real' : measures the preview as it is (after install).
At 1280x720, 1366x768, 1440x800, 1536x703 (scroller .page-wrapper): column rects, horizontal overflow, first screen,
sticky aside after scrolling, aside vs rules overlap, targets < 44 px in the aside. Shots: qa/talks/desktop/.
Usage: python -I desktop_probe.py proto|real"""
import asyncio, json, os, sys, time
from playwright.async_api import async_playwright

MODE = sys.argv[1] if len(sys.argv) > 1 else 'proto'
SIZES = [(1280, 720), (1366, 768), (1440, 800), (1536, 703)]
PAGES = {'hub': '/blogs/the-talks', 'topic': '/pages/talks/tiny-wins',
         'thread': '/pages/talk/what-s-your-smallest-friendship-green-flag'}
CSS = open(os.environ.get('TALKS_CSS', 'talks/staged/desktop/staged-sections.css'), encoding='utf-8').read()
OUT = 'qa/talks/desktop'
os.makedirs(OUT, exist_ok=True)

WRAP = """() => {
  const s = document.querySelector('.st-talks[data-st-feed]');
  if (!s || s.querySelector(':scope > .st-talks__feed')) return false;
  const compose = s.querySelector(':scope > .st-talks__compose');
  const feed = document.createElement('div'); feed.className = 'st-talks__feed';
  let n = compose.nextElementSibling;
  const move = []; while (n) { move.push(n); n = n.nextElementSibling; }
  move.forEach(m => feed.appendChild(m)); s.appendChild(feed); return move.length;
}"""

MEASURE = """() => {
  const r = e => { if (!e) return null; const b = e.getBoundingClientRect(); return [Math.round(b.left), Math.round(b.top), Math.round(b.width), Math.round(b.height)]; };
  const pw = document.querySelector('.page-wrapper');
  const q = s => document.querySelector(s);
  const main = q('.st-talks[data-st-feed] > .st-talks__feed') || q('.st-thread[data-st-thread-page]');
  const aside = q('.st-talks[data-st-feed] > .st-talks__compose > .st-compose') || q('.st-tform-section > .st-tform');
  const rules = q('.st-trules');
  const small = [...(aside ? aside.querySelectorAll('a, button, input, textarea, [role=button]') : []), ...(rules ? rules.querySelectorAll('a') : [])]
    .filter(e => e.offsetParent).map(e => [e.textContent.trim().slice(0, 20), Math.round(e.getBoundingClientRect().height)]).filter(x => x[1] < 44);
  return {
    hscroll: pw ? pw.scrollWidth - pw.clientWidth : null, docScroll: document.documentElement.scrollWidth - innerWidth,
    title: r(q('.st-talks__title') || q('.st-thread__title')), main: r(main), aside: r(aside), rules: r(rules),
    firstRow: r(q('.st-trow') || q('.st-thread__header')), scrollH: pw ? pw.scrollHeight : null, small,
  };
}"""


async def main():
    report = {}
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        for w, h in SIZES:
            for name, path in PAGES.items():
                pg = await b.new_page(viewport={'width': w, 'height': h})
                await pg.goto(f'https://0nev20-vn.myshopify.com{path}?preview_theme_id=186651934933&_cb={time.time_ns()}', wait_until='load', timeout=60000)
                await pg.wait_for_timeout(800)
                await pg.add_style_tag(content='[id^="PBar"], #preview-bar-iframe { display: none !important; }')
                if MODE == 'proto':
                    await pg.evaluate(WRAP)
                    await pg.add_style_tag(content=CSS)
                await pg.wait_for_timeout(400)
                top = await pg.evaluate(MEASURE)
                await pg.screenshot(path=f'{OUT}/{MODE}-{name}-{w}x{h}.png')
                # scroll the page scroller well down: the aside must stay at header + 24 (or stop above the rules)
                await pg.evaluate("() => { const pw = document.querySelector('.page-wrapper'); pw.scrollTop = Math.min(900, pw.scrollHeight); }")
                await pg.wait_for_timeout(300)
                mid = await pg.evaluate(MEASURE)
                await pg.screenshot(path=f'{OUT}/{MODE}-{name}-{w}x{h}-scrolled.png')
                await pg.evaluate("() => { const pw = document.querySelector('.page-wrapper'); pw.scrollTop = pw.scrollHeight; }")
                await pg.wait_for_timeout(300)
                end = await pg.evaluate(MEASURE)
                a, r_ = end['aside'], end['rules']
                overlap = bool(a and r_ and a[1] + a[3] > r_[1] + 1 and a[1] < r_[1] + r_[3] and a[0] < r_[0] + r_[2] and r_[0] < a[0] + a[2])
                report[f'{name} {w}x{h}'] = {'top': top, 'aside_after_900': mid['aside'], 'end_aside': a, 'end_rules': r_,
                                             'aside_rules_overlap_at_end': overlap}
                await pg.close()
        await b.close()
    for k, v in report.items():
        print(k, json.dumps(v))
    json.dump(report, open(f'{OUT}/{MODE}-report.json', 'w'), indent=1)

asyncio.run(main())
