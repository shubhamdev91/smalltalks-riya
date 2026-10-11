"""v1_header_lab.py: the staged V1 "the talks" wordmark (snippets/st-talks-wordmark + st-header changes + the hub title)
injected into the build preview in the browser (no theme write): header at 320/390/1536/1920 and the hub title at
390/1536. Measures the link (>= 44 px, accessible name), the mark (height = 0.8377em of the old size), the arrow, the
header row height, then saves talks/staged/v4/v1-{header,hub}-<w>.png (2x crops).
Usage: python -I talks/tools/v1_header_lab.py"""
import asyncio, json, re, sys, time
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')
BASE, Q = 'https://0nev20-vn.myshopify.com', '?preview_theme_id=186651934933'
ROOT = 'talks/staged/v4/src/'
snip = open(ROOT + 'snippets/st-talks-wordmark.liquid', encoding='utf-8').read()
DEF = re.search(r"\{%- if as == 'def' -%\}\s*(<svg.*?</svg>)", snip, re.S).group(1)
USE = re.search(r"\{%- else -%\}\s*(<svg.*?</svg>)", snip, re.S).group(1)
css_of = lambda f: '\n'.join(re.findall(r'{% stylesheet %}(.*?){% endstylesheet %}', open(f, encoding='utf-8').read(), re.S))
CSS = css_of(ROOT + 'snippets/st-talks-wordmark.liquid') + css_of(ROOT + 'sections/st-header.liquid') + """
 .tk .tk-wordmark{display:block;margin:0 0 4px;color:#0d0b10;font-size:40px;line-height:1}
 @media (min-width:1024px){.tk .tk-wordmark{font-size:52px}}
 [id^="PBar"], #preview-bar-iframe { display: none !important; } *{transition:none!important;animation:none!important}"""
INJECT = """([def_, use, css]) => {
  document.body.insertAdjacentHTML('afterbegin', def_);
  const st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
  for (const a of document.querySelectorAll('.st-header__talks')) {
    a.innerHTML = '<span class="visually-hidden">the talks</span><span class="st-header__talks-mark">' + use + '<span class="st-header__talks-arrow" aria-hidden="true">↗</span></span>';
  }
  for (const a of document.querySelectorAll('.st-drawer__talks')) a.innerHTML = '<span class="visually-hidden">the talks</span>' + use;
  const h1 = document.querySelector('#MainContent h1');
  if (h1) { h1.className = 'tk-wordmark'; h1.removeAttribute('style'); h1.innerHTML = '<span class="visually-hidden">the talks</span>' + use;
            h1.parentElement.closest('section')?.classList.add('tk'); }
}"""
MEASURE = """() => {
  const a = document.querySelector('.st-header__talks'), svg = a.querySelector('svg'), arr = a.querySelector('.st-header__talks-arrow');
  const r = (e) => { const b = e.getBoundingClientRect(); return [Math.round(b.x*10)/10, Math.round(b.y*10)/10, Math.round(b.width*10)/10, Math.round(b.height*10)/10]; };
  const fs = parseFloat(getComputedStyle(a).fontSize);
  const bar = document.querySelector('.st-header__bar').getBoundingClientRect().height;
  const h1 = document.querySelector('#MainContent h1 svg');
  return {link: r(a), svg: r(svg), arrow: r(arr), font: fs, expectH: Math.round(fs*0.8377*10)/10, bar,
          name: a.querySelector('.visually-hidden').textContent, color: getComputedStyle(a).color,
          h1: h1 ? r(h1) : null, h1font: h1 ? parseFloat(getComputedStyle(h1.parentElement).fontSize) : null,
          caveatUsed: [...document.fonts].filter(f => f.family.includes('Caveat') && f.status === 'loaded').length};
}"""


async def main():
    ok = True
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        for w, h in ((320, 700), (390, 844), (1536, 864), (1920, 1080)):
            pg = await b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=2)
            await pg.goto(f'{BASE}/blogs/the-talks{Q}&_cb={time.time_ns()}', wait_until='networkidle', timeout=60000)
            await pg.evaluate(INJECT, [DEF, USE, CSS])
            await pg.evaluate('document.fonts.ready')
            await pg.wait_for_timeout(400)
            m = await pg.evaluate(MEASURE)
            good = (m['link'][3] >= 44 and abs(m['svg'][3] - m['expectH']) <= 0.6 and m['name'] == 'the talks'
                    and m['arrow'][0] >= m['svg'][0] + m['svg'][2] and m['arrow'][1] + m['arrow'][3] <= m['svg'][1] + m['svg'][3] + 1
                    and m['link'][0] + m['link'][2] <= w)
            ok &= good
            print(('PASS ' if good else 'FAIL ') + f'header @{w}: ' + json.dumps(m))
            await pg.screenshot(path=f'talks/staged/v4/v1-header-{w}.png', clip={'x': 0, 'y': 0, 'width': w, 'height': 80})
            if w in (390, 1536):
                box = await pg.evaluate("(() => { const b = document.querySelector('#MainContent h1').getBoundingClientRect(); return [b.x, b.y, b.width, b.height]; })()")
                await pg.screenshot(path=f'talks/staged/v4/v1-hub-{w}.png', clip={'x': 0, 'y': max(box[1] - 24, 0), 'width': min(w, 900), 'height': 140})
            await pg.close()
        await b.close()
    print('ALL PASS' if ok else 'SOME FAIL')

asyncio.run(main())
