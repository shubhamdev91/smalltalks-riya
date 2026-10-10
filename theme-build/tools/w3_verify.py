"""Preview (theme 186651934933) checks for the hero v3.7 / board-corrections / PDP gallery / cards / guide photos /
talks SEO window. Writes qa/fidelity/v37-*.png and prints one JSON line per check.
Usage: python -I tools/w3_verify.py [part ...]   parts: hero shaadi pdp shop guide talks story peeks (default all)"""
import asyncio, json, pathlib, re, sys, time
from playwright.async_api import async_playwright
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
TB = pathlib.Path(__file__).resolve().parents[1]
QA = TB.parent / 'qa/fidelity'
TMP = TB / 'tmp/w3'
TMP.mkdir(parents=True, exist_ok=True)
O = 'https://0nev20-vn.myshopify.com'
Q = 'preview_theme_id=186651934933'
PARTS = [a.split(':')[0] for a in sys.argv[1:]] or ['hero', 'shaadi', 'pdp', 'shop', 'guide', 'talks', 'story', 'peeks']
STORY = next((a.split(':')[1] for a in sys.argv[1:] if a.startswith('story:')), 'diet-cherry')
HIDE = '[id^="PBar"], #preview-bar-iframe { display: none !important; }'


def url(path):
    sep = '&' if '?' in path else '?'
    return f'{O}{path}{sep}{Q}&_cb={time.time_ns()}'


async def settle(pg, scroll=True):
    await pg.add_style_tag(content=HIDE)
    await pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager')")
    if scroll:
        for y in range(0, 12000, 700):
            if not await pg.evaluate(f'(window.scrollTo(0, {y}), {y} < document.documentElement.scrollHeight)'):
                break
            await pg.wait_for_timeout(50)
        await pg.evaluate('window.scrollTo(0, 0)')
    await pg.evaluate('Promise.race([Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; }))), new Promise(r => setTimeout(r, 5000))])')
    await pg.evaluate('document.fonts.ready')
    await pg.wait_for_timeout(400)


def liquid_flags(html):
    return [x for x in ('Liquid error', 'translation missing') if x in html] or 'clean'


def sheet(paths, labels, out, cols=4, scale=0.5):
    ims = [Image.open(p) for p in paths]
    ims = [im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS) for im in ims]
    cw = max(im.width for im in ims) + 12
    rows = [ims[i:i + cols] for i in range(0, len(ims), cols)]
    H = sum(max(im.height for im in r) + 22 for r in rows)
    s = Image.new('RGB', (cw * min(cols, len(ims)), H), 'white')
    d = ImageDraw.Draw(s)
    y = 0
    for ri, r in enumerate(rows):
        for ci, im in enumerate(r):
            s.paste(im, (ci * cw, y + 20))
            d.text((ci * cw, y + 4), labels[ri * cols + ci], fill='black')
        y += max(im.height for im in r) + 22
    s.save(out)
    print('sheet', out.name)


HERO_INFO = r'''() => { const h = document.querySelector('[data-st-hero]'); if (!h) return null;
  const ch = h.querySelector('[data-st-hero-character]'); const ci = h.querySelector('[data-st-hero-character-img]');
  const main = h.querySelector('[data-st-hero-main-nail]'); const tone = h.querySelector('[data-st-hero-tone-sprite]');
  const hr = h.getBoundingClientRect(), cr = ch.getBoundingClientRect();
  const f = s => (s || '').split('/').pop().split('?')[0];
  return { key: h.dataset.activeKey, char: f(ci && (ci.currentSrc || ci.src)), charLoaded: !!(ci && ci.complete && ci.naturalWidth),
    parts: [...ch.querySelectorAll('[data-st-hero-character-part]')].map(p => f(p.src)), bleed: ch.dataset.bleed,
    nails: f((getComputedStyle(main).getPropertyValue('--st-nails').match(/url\(["']?([^"')]+)/) || [])[1]),
    tone: f(tone && (tone.currentSrc || tone.src)), heroBottom: Math.round(hr.bottom), charBottom: Math.round(cr.bottom),
    charImgBottom: ci ? Math.round(ci.getBoundingClientRect().bottom) : null, hscroll: document.documentElement.scrollWidth > innerWidth }; }'''


async def hero_states(b, w, h, want=None, tag=''):
    ctx = await b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=2)
    pg = await ctx.new_page()
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)[:160]))
    pg.on('console', lambda m: errs.append('console ' + m.text[:160]) if m.type == 'error' else None)
    pg.on('response', lambda r: errs.append(f'HTTP {r.status} {r.url[:140]}') if r.status >= 400 else None)
    await pg.goto(url('/'), wait_until='load', timeout=90000)
    await settle(pg, scroll=False)
    print('hero page', w, h, liquid_flags(await pg.content()))
    # stop the autoplay so each shot is one settled state
    pause = await pg.query_selector('.st-hero__controls button')
    shots = []
    seen = []
    for i in range(7):
        info = await pg.evaluate(HERO_INFO)
        if i == 0 and pause and await pg.evaluate("document.querySelector('[data-st-hero]').dataset.autoplay !== undefined"):
            pass
        if want is None or info['key'] == want:
            await pg.wait_for_timeout(1800)
            info = await pg.evaluate(HERO_INFO)
            p = TMP / f'hero-{tag}{w}x{h}-{i}-{info["key"]}.png'
            await pg.screenshot(path=str(p), clip={'x': 0, 'y': 0, 'width': w, 'height': h})
            shots.append((p, f'{i + 1} {info["key"]}'))
            print('state', w, h, json.dumps(info))
            if want:
                break
        seen.append(info['key'])
        # a real tap on the button's visible part (Playwright's click() scrolls the partly off-screen button into view,
        # which scrolls the overflow-hidden hero sideways; a user tap does not)
        bb = await pg.evaluate("(() => { const r = document.querySelector('[data-st-hero-preview]').getBoundingClientRect(); return [r.left + Math.min(r.width, innerWidth - r.left) / 2, Math.max(r.top, 0) + Math.min(r.bottom, innerHeight) / 2 - Math.max(r.top, 0) / 2]; })()")
        await pg.mouse.click(bb[0], bb[1])
        for _ in range(40):
            await pg.wait_for_timeout(100)
            k = await pg.evaluate("document.querySelector('[data-st-hero]').dataset.activeKey")
            if k != info['key']:
                break
        await pg.wait_for_timeout(900)
    print('hero errors', w, h, errs or 'none')
    await ctx.close()
    return shots


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        if 'hero' in PARTS:
            shots = await hero_states(b, 390, 844)
            sheet([s[0] for s in shots], [s[1] for s in shots], QA / 'v37-hero-390.png', cols=4, scale=0.5)
        if 'shaadi' in PARTS:
            shots = []
            for w, h in ((320, 568), (390, 932)):
                shots += await hero_states(b, w, h, want='shaadi-shift', tag='shaadi-')
            sheet([s[0] for s in shots], [f'{s[1]} {Image.open(s[0]).width // 2}x{Image.open(s[0]).height // 2}' for s in shots],
                  QA / 'v37-hero-shaadi-320x568-390x932.png', cols=2, scale=0.5)
        ctx = await b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2)
        pg = await ctx.new_page()
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)[:160]))
        if 'pdp' in PARTS:
            for w in (390, 320):
                await pg.set_viewport_size({'width': w, 'height': 844})
                await pg.goto(url('/products/bill-idhar'), wait_until='load', timeout=90000)
                await settle(pg)
                html = await pg.content()
                info = await pg.evaluate(r'''() => { const m = document.querySelector('.st-pdp-media'); const r = m.getBoundingClientRect();
                  const imgs = [...m.querySelectorAll('.st-pdp-media__photo')].map(i => ({ alt: i.alt, src: (i.currentSrc || '').split('?')[1], loading: i.loading }));
                  const th = m.querySelector('.st-pdp-media__thumbs'); const tr = th.getBoundingClientRect();
                  return { slides: m.querySelectorAll('.st-pdp-media__slide').length, thumbs: th.querySelectorAll('button').length,
                    thumbsRight: Math.round(tr.right), thumbsScroll: th.scrollWidth > th.clientWidth, photos: imgs,
                    caption: (m.querySelector('.st-pdp-media__caption') || {}).textContent, top: Math.round(r.top + scrollY), h: Math.round(r.height),
                    hscroll: document.documentElement.scrollWidth > innerWidth }; }''')
                print('pdp', w, liquid_flags(html), json.dumps(info, ensure_ascii=False))
                # swipe: scroll the track to slide 3 and read the current thumb
                cur = await pg.evaluate(r'''async () => { const t = document.querySelector('.st-pdp-media__track'); t.scrollTo({ left: t.clientWidth * 2 });
                  await new Promise(r => setTimeout(r, 600)); return [...document.querySelectorAll('.st-pdp-media__thumb')].findIndex(b => b.getAttribute('aria-current') === 'true') + 1; }''')
                print('pdp swipe to slide 3 -> current thumb', cur)
                await pg.evaluate("window.scrollTo(0, 0); document.querySelector('.st-pdp-media__track').scrollTo({ left: 0 })")
                await pg.wait_for_timeout(500)
                p0 = TMP / f'pdp-{w}.png'
                await pg.screenshot(path=str(p0), clip={'x': 0, 'y': max(0, info['top'] - 10), 'width': w, 'height': info['h'] + 20})
                # each photo slide too
                shots = [p0]
                for n in range(2, info['slides'] + 1):
                    await pg.evaluate(f"document.querySelector('.st-pdp-media__track').scrollTo({{ left: document.querySelector('.st-pdp-media__track').clientWidth * {n - 1} }})")
                    await pg.wait_for_timeout(700)
                    pn = TMP / f'pdp-{w}-slide{n}.png'
                    # viewport shot: a full-page shot re-lays out the snap track and jumps back a slide
                    await pg.screenshot(path=str(pn), clip={'x': 0, 'y': max(0, info['top'] - 10), 'width': w, 'height': info['h'] + 20})
                    shots.append(pn)
                sheet(shots, [f'{w} slide {i + 1}' for i in range(len(shots))], QA / f'v37-pdp-gallery-{w}.png', cols=5, scale=0.5)
        if 'shop' in PARTS:
            for w in (390, 1280):
                await pg.set_viewport_size({'width': w, 'height': 900})
                await pg.goto(url('/collections/all'), wait_until='load', timeout=90000)
                await settle(pg)
                info = await pg.evaluate(r'''() => ({ cards: document.querySelectorAll('.st-card').length,
                  secondary: document.querySelectorAll('.resource-card__image--secondary').length,
                  searchCards: [...document.querySelectorAll('img.resource-card__image')].slice(0, 2).map(i => i.getAttribute('srcset')),
                  hscroll: document.documentElement.scrollWidth > innerWidth })''')
                print('shop', w, liquid_flags(await pg.content()), json.dumps(info))
                await pg.screenshot(path=str(QA / f'v37-shop-{w}.png'), full_page=True)
        if 'guide' in PARTS:
            await pg.set_viewport_size({'width': 390, 'height': 844})
            await pg.goto(url('/pages/nail-guide-desi'), wait_until='load', timeout=90000)
            await settle(pg)
            info = await pg.evaluate(r'''() => [...document.querySelectorAll('.st-gstep')].map(s => { const i = s.querySelector('.st-gstep__photo');
              return { title: s.querySelector('.st-gstep__title').textContent, img: i && i.currentSrc.split('/').pop().split('?')[0], alt: i && i.alt,
                       loaded: !!(i && i.naturalWidth), w: i && Math.round(i.getBoundingClientRect().width) }; })''')
            print('guide', liquid_flags(await pg.content()), json.dumps(info, ensure_ascii=False))
            box = await pg.evaluate("(() => { const a = document.querySelectorAll('.st-gstep'); const r1 = a[0].getBoundingClientRect(), r3 = a[a.length - 1].getBoundingClientRect(); return [Math.round(r1.top + scrollY) - 10, Math.round(r3.bottom + scrollY) + 10]; })()")
            await pg.screenshot(path=str(QA / 'v37-guide-steps-390.png'), full_page=True, clip={'x': 0, 'y': box[0], 'width': 390, 'height': box[1] - box[0]})
        if 'story' in PARTS:
            await pg.set_viewport_size({'width': 390, 'height': 844})
            await pg.goto(url('/blogs/journal/' + STORY), wait_until='load', timeout=90000)
            await settle(pg)
            info = await pg.evaluate(r'''() => { const h = document.querySelector('.st-story__hero'); const r = h.getBoundingClientRect();
              return { cls: h.className, card: [Math.round(r.width), Math.round(r.height)], layers: [...h.querySelectorAll('img')].map(i => { const b = i.getBoundingClientRect();
                return [i.src.split('/').pop().split('?')[0], Math.round(b.left - r.left), Math.round(b.top - r.top), Math.round(b.width), Math.round(b.bottom - r.top)]; }) }; }''')
            print('story', STORY, liquid_flags(await pg.content()), json.dumps(info))
            box = await pg.evaluate("(() => { const r = document.querySelector('.st-story__hero').getBoundingClientRect(); return [Math.round(r.top + scrollY) - 120, Math.round(r.bottom + scrollY) + 20]; })()")
            await pg.screenshot(path=str(QA / f'v37-story-{STORY}-390.png'), full_page=True, clip={'x': 0, 'y': max(0, box[0]), 'width': 390, 'height': box[1] - max(0, box[0])})
        if 'peeks' in PARTS:
            peek_map = (TB / 'src/snippets/st-peek-map.liquid').read_text(encoding='utf-8')
            def row(part, key):
                sect = peek_map.split(f"{{%- when '{part}' -%}}")[1]
                return re.search(r"when '" + key + r"' -%\}([^\n]+)", sect).group(1).split(',')
            shots = []
            for w in (390, 320):
                await pg.set_viewport_size({'width': w, 'height': 844})
                await pg.goto(url('/products/dulhan-tu-duty-meri'), wait_until='load', timeout=90000)
                await settle(pg)
                info = await pg.evaluate("(() => { const p = document.querySelector('.st-notes__peek'); const i = p.querySelector('img'); const r = p.getBoundingClientRect(); p.scrollIntoView({block: 'center'}); return { src: i.currentSrc.split('/').pop().split('?')[0], w: i.getBoundingClientRect().width, natural: i.naturalWidth, box: [Math.round(r.left), Math.round(r.width)] }; })()")
                print('shaadi pdp peek', w, json.dumps(info))
                await pg.wait_for_timeout(300)
                c = await pg.evaluate("(() => { const r = document.querySelector('.st-notes__coda').getBoundingClientRect(); return [Math.round(r.top + scrollY) - 10, Math.round(r.height) + 20]; })()")
                pth = TMP / f'peek-shaadi-pdp-{w}.png'
                await pg.screenshot(path=str(pth), full_page=True, clip={'x': 0, 'y': c[0], 'width': w, 'height': c[1]})
                shots.append((pth, f'PDP Shaadi {w}'))
                # bag: the cart template's campaign is On Me; apply the Shaadi bag row from st-peek-map in-page (real CSS)
                await pg.goto(url('/cart'), wait_until='load', timeout=90000)
                await settle(pg)
                r = row('bag', 'shaadi-shift')
                asset = await pg.evaluate("document.querySelector('.st-bag-extras__peek img').src")
                new_src = re.sub(r'/[^/?]+\.webp', '/' + r[0], asset, count=1)
                await pg.evaluate(f"""(() => {{ const i = document.querySelector('.st-bag-extras__peek img'); i.src = {json.dumps(new_src)}; i.width = {r[1]}; i.height = {r[2]};
                  i.style.left = '{r[3]}px'; i.style.top = '{r[4]}px'; i.style.width = '{r[5]}px'; }})()""")
                await pg.wait_for_timeout(1200)
                bi = await pg.evaluate("(() => { const i = document.querySelector('.st-bag-extras__peek img'); const h = document.querySelector('.st-bag-extras__help'); h.scrollIntoView({block: 'center'}); return { src: i.currentSrc.split('/').pop().split('?')[0], loaded: i.naturalWidth, w: i.getBoundingClientRect().width }; })()")
                print('shaadi bag peek (simulated)', w, json.dumps(bi))
                await pg.wait_for_timeout(300)
                c = await pg.evaluate("(() => { const r = document.querySelector('.st-bag-extras__help').getBoundingClientRect(); return [Math.round(r.top + scrollY) - 10, Math.round(r.height) + 20]; })()")
                pth = TMP / f'peek-shaadi-bag-{w}.png'
                await pg.screenshot(path=str(pth), full_page=True, clip={'x': 0, 'y': c[0], 'width': w, 'height': c[1]})
                shots.append((pth, f'Bag Shaadi {w} (simulated)'))
            sheet([s[0] for s in shots], [s[1] for s in shots], QA / 'v37-peeks-shaadi.png', cols=2, scale=0.5)
        if 'talks' in PARTS:
            await pg.goto(url('/blogs/the-talks'), wait_until='load', timeout=90000)
            links = await pg.evaluate("[...new Set([...document.querySelectorAll('a[href*=\"/pages/talk/\"], a[href*=\"/pages/talks/\"]')].map(a => new URL(a.href).pathname))]")
            thread = next((l for l in links if l.startswith('/pages/talk/')), '/pages/talk/what-s-your-smallest-friendship-green-flag')
            topic = next((l for l in links if l.startswith('/pages/talks/') and not l.endswith('/all')), None)
            old = '/blogs/the-talks/' + thread.rsplit('/', 1)[1]
            for path in [thread, topic, old, '/blogs/the-talks']:
                if not path:
                    continue
                resp = await pg.request.get(url(path), headers={'Cache-Control': 'no-cache'})
                html = await resp.text()
                head = html.split('</head>')[0]
                g = lambda rx: (re.search(rx, head, re.S) or [None, None])[1]
                info = {'path': path, 'status': resp.status, 'final': resp.url.split('?')[0].replace(O, ''), 'title': re.sub(r'\s+', ' ', g(r'<title>(.*?)</title>') or '').strip(),
                        'canonical': g(r'rel="canonical"\s+href="([^"]+)"'), 'robots': g(r'name="robots" content="([^"]+)"'),
                        'og_type': g(r'property="og:type"\s+content="([^"]+)"'), 'description': (g(r'name="description"\s+content="([^"]+)"') or '')[:90],
                        'ld_types': re.findall(r'"@type":\s*"(BreadcrumbList|DiscussionForumPosting|Article|Organization)"', head),
                        'liquid': liquid_flags(html)}
                print('talks head', json.dumps(info, ensure_ascii=False))
                if path == thread:
                    for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', head, re.S):
                        if 'DiscussionForumPosting' in blk or 'BreadcrumbList' in blk:
                            print('  ld', re.sub(r'\s+', ' ', blk).strip()[:600])
        print('page errors', errs or 'none')
        await b.close()


asyncio.run(main())
