"""QA-window checks: PDP gallery keyboard path, favicon on a fresh profile, /pages/the-talks head, and the PDP
illustration slide of every set at 390 (ground vs image edge). Writes qa/fidelity/w5-*.png."""
import asyncio, json, pathlib, re, sys, time
from playwright.async_api import async_playwright
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
TB = pathlib.Path(__file__).resolve().parents[1]
QA = TB.parent / 'qa/fidelity'
O = 'https://0nev20-vn.myshopify.com'
Q = 'preview_theme_id=186651934933'
PDP = ['bill-idhar', 'haan-mera-idea-tha', 'haan-wohi-wali', 'tum-aa-jao-main-dekh-lungi', 'dulhan-tu-duty-meri',
       'achha-tum-pehle', 'haath-do-main-hoon']


def url(path):
    return f"{O}{path}{'&' if '?' in path else '?'}{Q}&_cb={time.time_ns()}"


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        # 1. keyboard: Tab until the track has focus, then ArrowRight x2, End, Home
        ctx = await b.new_context(viewport={'width': 390, 'height': 844})
        pg = await ctx.new_page()
        await pg.goto(url('/products/bill-idhar'), wait_until='load', timeout=90000)
        await pg.add_style_tag(content='[id^="PBar"], #preview-bar-iframe { display: none !important; }')
        await pg.wait_for_timeout(800)
        tabs = 0
        for tabs in range(1, 60):
            await pg.keyboard.press('Tab')
            if await pg.evaluate("document.activeElement && document.activeElement.classList.contains('st-pdp-media__track')"):
                break
        state = lambda: pg.evaluate("""(() => { const t = document.querySelector('.st-pdp-media__track');
          return { slide: Math.round(t.scrollLeft / t.clientWidth) + 1, thumb: [...document.querySelectorAll('.st-pdp-media__thumb')].findIndex(b => b.getAttribute('aria-current') === 'true') + 1,
                   name: t.getAttribute('aria-label'), focus: document.activeElement === t, ring: getComputedStyle(t).outlineStyle }; })()""")
        log = [('after %d Tab' % tabs, await state())]
        for key in ('ArrowRight', 'ArrowRight', 'End', 'ArrowLeft', 'Home'):
            await pg.keyboard.press(key)
            await pg.wait_for_timeout(700)
            log.append((key, await state()))
        for k, s in log:
            print('keyboard', k, json.dumps(s))
        await pg.keyboard.press('Home')
        await ctx.close()
        # 2. favicon: fresh profile, every icon link, any /favicon.ico or icon 404
        ctx = await b.new_context(viewport={'width': 390, 'height': 844})
        pg = await ctx.new_page()
        bad, icons = [], []
        pg.on('response', lambda r: (bad.append(f'{r.status} {r.url[:120]}') if r.status >= 400 and ('favicon' in r.url or 'icon' in r.url) else None,
                                     icons.append(f'{r.status} {r.url.split("?")[0].split("/")[-1]}') if 'favicon' in r.url or 'apple-touch' in r.url else None))
        await pg.goto(url('/'), wait_until='load', timeout=90000)
        await pg.wait_for_timeout(2000)
        links = await pg.evaluate("[...document.querySelectorAll('link[rel~=icon], link[rel=apple-touch-icon]')].map(l => l.rel + ' ' + (l.sizes.value || '') + ' ' + l.href.split('?')[0].split('/').pop())")
        root = await pg.request.get(f'{O}/favicon.ico')
        print('favicon links', links)
        print('favicon responses', icons, '| errors', bad or 'none', '| GET /favicon.ico', root.status)
        await pg.goto(url('/assets/favicon-192.png') if False else f"{O}/cdn/shop/t/{0}", wait_until='commit') if False else None
        await ctx.close()
        # 3. /pages/the-talks head
        ctx = await b.new_context()
        pg = await ctx.new_page()
        await pg.goto(url('/'), wait_until='commit')
        r = await pg.request.get(url('/pages/the-talks'), headers={'Cache-Control': 'no-cache'})
        head = (await r.text()).split('</head>')[0]
        g = lambda rx: (re.search(rx, head, re.S) or [None, None])[1]
        print('the-talks head', json.dumps({'status': r.status, 'title': re.sub(r'\s+', ' ', g(r'<title>(.*?)</title>') or '').strip(),
              'canonical': g(r'rel="canonical"\s+href="([^"]+)"'), 'robots': g(r'name="robots" content="([^"]+)"'),
              'og_image': g(r'property="og:image"\s+content="([^"]+)"')}, ensure_ascii=False))
        await ctx.close()
        # 4. illustration slide per set
        ctx = await b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2)
        pg = await ctx.new_page()
        shots = []
        for h in PDP:
            await pg.goto(url(f'/products/{h}'), wait_until='load', timeout=90000)
            await pg.add_style_tag(content='[id^="PBar"], #preview-bar-iframe { display: none !important; }')
            await pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager')")
            info = await pg.evaluate("""async () => { const t = document.querySelector('.st-pdp-media__track'); const s = t.querySelector('.st-pdp-media__slide--life');
              t.scrollTo({ left: s.offsetLeft - t.offsetLeft }); const i = s.querySelector('img'); await (i.decode ? i.decode().catch(() => 0) : 0);
              await new Promise(r => setTimeout(r, 700)); const r = s.getBoundingClientRect();
              return { bg: getComputedStyle(s).backgroundColor, box: [r.left, r.top + scrollY, r.width, r.height] }; }""")
            x, y, w, hh = info['box']
            pth = TB / 'tmp' / f'w5-life-{h}.png'
            await pg.screenshot(path=str(pth), clip={'x': x, 'y': y, 'width': w, 'height': hh})
            im = Image.open(pth).convert('RGB')
            # sample the ground at the slide edge vs just inside the image edge (left side, mid-height)
            W, H = im.size
            iw = H * 571 / 679  # contained image width in device px
            x0 = (W - iw) / 2
            edge = im.getpixel((4, H // 2)); inner = im.getpixel((int(x0 + 6), int(H * 0.1)))
            print('life', h, info['bg'], 'slide edge', edge, 'image edge', inner)
            shots.append((pth, h))
        ims = [Image.open(s[0]) for s in shots]
        sw = ims[0].width // 2
        sheet = Image.new('RGB', (sw * 4 + 30, (ims[0].height // 2 + 22) * 2), 'white')
        d = ImageDraw.Draw(sheet)
        for i, (im, (_, h)) in enumerate(zip(ims, shots)):
            X, Y = (i % 4) * (sw + 10), (i // 4) * (ims[0].height // 2 + 22)
            sheet.paste(im.resize((sw, im.height // 2)), (X, Y + 20)); d.text((X, Y + 4), h, fill='black')
        sheet.save(QA / 'w5-pdp-illustration-slides-390.png')
        print('sheet w5-pdp-illustration-slides-390.png')
        await b.close()


asyncio.run(main())
