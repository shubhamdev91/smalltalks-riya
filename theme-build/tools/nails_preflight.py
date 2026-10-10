"""HD nail sheets on every non-hero surface: preview checks at 390 (and 320).
--sim : read-only pre-flight on the CURRENT preview: inject the new CSS (x1.058 about the cuticle on ::before) and swap
        the P1 sprite URLs for the live st-hd-nails files in this browser only, then shoot before | after per surface.
default: shoot the live surfaces (after upload) and list every nail sprite each page requests.
Writes qa/fidelity/hdnails-<surface>-<w>.png (+ -sim when simulated). Usage: python -I tools/nails_preflight.py [--sim] [w]"""
import asyncio, json, pathlib, sys, time
from playwright.async_api import async_playwright
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
TB = pathlib.Path(__file__).resolve().parents[1]
QA = TB.parent / 'qa/fidelity'
TMP = TB / 'tmp/hdnails'
TMP.mkdir(parents=True, exist_ok=True)
O = 'https://0nev20-vn.myshopify.com'
Q = 'preview_theme_id=186651934933'
SIM = '--sim' in sys.argv
W = int(next((a for a in sys.argv[1:] if a.isdigit()), 390))
SURFACES = [  # name, path, selector of the region to shoot
    ('chapters', '/', '.st-ch__nails'),
    ('tiles', '/', '.st-tiles__nail'),
    ('shop-cards', '/collections/all', '.st-card'),
    ('journal-closeup', '/blogs/journal', '.st-closeup'),
    ('pdp-scene', '/products/bill-idhar', '.st-pdp-scene'),
    ('bag', '/cart', '.st-bag-extras__promo'),
    ('our-story-stack', '/pages/our-story', '.st-pack__nails'),
]
CSS = """
.st-ch__nail, .st-bag-extras__nail { position: relative; }
.st-ch__nail, .st-tiles__nail, .st-bag-extras__nail, .st-closeup__nail, .st-card__nail, .st-pdp-scene__nail { background: none !important; }
.st-ch__nail::before, .st-tiles__nail::before, .st-bag-extras__nail::before, .st-closeup__nail::before, .st-card__nail::before,
.st-pdp-scene__nail::before { content: ''; position: absolute; inset: -5.365% -2.9% -0.435%;
  background: var(--st-nails) calc(var(--col, 0) * 50%) 0 / 300% 100% no-repeat; }
.st-nail-img { scale: 1.058; }
"""
SWAP = r"""() => { let n = 0;
  document.querySelectorAll('[style*="st-nails-"]').forEach(e => { e.setAttribute('style', e.getAttribute('style').replace(/st-nails-/g, 'st-hd-nails-')); n++; });
  document.querySelectorAll('img[src*="st-nails-"]').forEach(i => { i.src = i.src.replace('st-nails-', 'st-hd-nails-'); i.removeAttribute('srcset'); n++; });
  return n; }"""


async def settle(pg):
    await pg.add_style_tag(content='[id^="PBar"], #preview-bar-iframe { display: none !important; }')
    await pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager')")
    for y in range(0, 14000, 700):
        if not await pg.evaluate(f'(window.scrollTo(0, {y}), {y} < document.documentElement.scrollHeight)'):
            break
        await pg.wait_for_timeout(40)
    await pg.evaluate('window.scrollTo(0, 0)')
    await pg.evaluate('Promise.race([Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; }))), new Promise(r => setTimeout(r, 4000))])')
    await pg.wait_for_timeout(500)


async def region(pg, sel):
    return await pg.evaluate(f"""(() => {{ const els = [...document.querySelectorAll({json.dumps(sel)})]; if (!els.length) return null;
      let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
      els.slice(0, 12).forEach(e => {{ const r = e.getBoundingClientRect(); x0 = Math.min(x0, r.left); y0 = Math.min(y0, r.top + scrollY); x1 = Math.max(x1, r.right); y1 = Math.max(y1, r.bottom + scrollY); }});
      const pad = 24; return [Math.max(0, x0 - pad), Math.max(0, y0 - pad), Math.min(innerWidth, x1 + pad), y1 + pad]; }})()""")


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        ctx = await b.new_context(viewport={'width': W, 'height': 900}, device_scale_factor=2)
        pg = await ctx.new_page()
        sprites = {}
        pg.on('request', lambda r: sprites.setdefault(pg.url.split('?')[0].replace(O, '') or '/', set()).add(r.url.split('/')[-1].split('?')[0])
              if 'nails-' in r.url and r.url.split('?')[0].endswith('.webp') else None)
        last = None
        for name, path, sel in SURFACES:
            if path != last:
                await pg.goto(f'{O}{path}?{Q}&_cb={time.time_ns()}', wait_until='load', timeout=90000)
                await settle(pg)
                last = path
            if name == 'chapters' and not SIM:
                # every chapter row with the headline above it (tips clear of the headline)
                boxes = await pg.evaluate("""[...document.querySelectorAll('.st-ch__nails')].map(e => { const s = e.closest('.st-ch') || e.parentElement;
                  const h = s.querySelector('.st-ch__head, h2, h3'); const r = e.getBoundingClientRect(); const t = h ? h.getBoundingClientRect().top : r.top - 120;
                  return [s.dataset.land || '', Math.round(Math.min(t, r.top) + scrollY - 10), Math.round(r.bottom + scrollY + 10)]; })""")
                from PIL import Image as _I
                parts = []
                for key, y0, y1 in boxes:
                    pth = TMP / f'chapter-{key}-{W}.png'
                    await pg.screenshot(path=str(pth), full_page=True, clip={'x': 0, 'y': y0, 'width': W, 'height': y1 - y0})
                    parts.append(_I.open(pth))
                sh = _I.new('RGB', (W * 2, sum(im.height + 12 for im in parts)), 'white'); yy = 0
                for im in parts:
                    sh.paste(im, (0, yy)); yy += im.height + 12
                sh.save(QA / f'hdnails-chapters-{W}.png'); print('chapters', len(parts), 'rows shot')
                continue
            box = await region(pg, sel)
            if not box:
                print(name, 'not on page'); continue
            clip = {'x': box[0], 'y': box[1], 'width': box[2] - box[0], 'height': min(box[3] - box[1], 900)}
            if SIM:
                before = TMP / f'{name}-{W}-before.png'
                await pg.screenshot(path=str(before), full_page=True, clip=clip)
                await pg.add_style_tag(content=CSS)
                n = await pg.evaluate(SWAP)
                await pg.wait_for_timeout(1500)
                await pg.evaluate('Promise.race([Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; }))), new Promise(r => setTimeout(r, 3000))])')
                after = TMP / f'{name}-{W}-after.png'
                await pg.screenshot(path=str(after), full_page=True, clip=clip)
                a, c = Image.open(before), Image.open(after)
                s = Image.new('RGB', (a.width + c.width + 20, max(a.height, c.height) + 30), 'white')
                s.paste(a, (0, 30)); s.paste(c, (a.width + 20, 30))
                d = ImageDraw.Draw(s); d.text((4, 6), f'{name} {W}: live P1', fill='black'); d.text((a.width + 24, 6), f'simulated HD x1.058 ({n} swaps)', fill='black')
                s.save(QA / f'hdnails-{name}-{W}-sim.png')
                print(name, 'sim', n, 'swaps')
                last = None  # reload before the next surface on the same page (undo the injection)
            else:
                out = QA / f'hdnails-{name}-{W}.png'
                await pg.screenshot(path=str(out), full_page=True, clip=clip)
                print(name, 'shot')
        for k, v in sprites.items():
            print('sprites', k, sorted(v))
        await b.close()


asyncio.run(main())
