"""st-fable: "the talks" wordmark options rendered IN CONTEXT on the build preview (fonts injected as data URIs; lab only):
site header (phone 390 + desktop 1536) and the talks hub title (phone + desktop). Writes options-sheet.png."""
import asyncio, base64, json, pathlib, sys, time
from playwright.async_api import async_playwright
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding='utf-8')
HERE = pathlib.Path(__file__).resolve().parent
F = pathlib.Path(r'C:/Users/SSTS/Desktop/Riya/spec/fonts')
BASE = 'https://0nev20-vn.myshopify.com'
Q = 'preview_theme_id=186651934933'
def face(name, path):
    return f"@font-face{{font-family:'{name}';src:url(data:font/ttf;base64,{base64.b64encode(path.read_bytes()).decode()}) format('truetype');font-weight:100 1000;font-display:block;}}"
FACES = face('WM Fraunces', F / 'fraunces' / 'Fraunces[SOFT,WONK,opsz,wght].ttf') + face('WM Gochi', F / 'gochihand' / 'GochiHand-Regular.ttf') \
    + face('WM CaveatBrush', F / 'caveatbrush' / 'CaveatBrush-Regular.ttf') + face('WM SSItalic', F / 'sourceserif4' / 'SourceSerif4-Italic[opsz,wght].ttf')
INK = '#0d0b10'
# each option: CSS for a ".wm" element at a given size unit (--wm = the old Caveat font-size), plus optional markup split
OPTS = {
    'now': {'label': 'NOW: Caveat 600', 'css': '', 'split': False},
    'A': {'label': 'A  soft serif (Fraunces SOFT 100 / WONK 1, 650)', 'split': False,
          'css': f".wm{{font-family:'WM Fraunces',serif!important;font-weight:650!important;font-variation-settings:'SOFT' 100,'WONK' 1,'opsz' 144!important;font-size:calc(var(--wm) * 0.86)!important;letter-spacing:-0.025em!important;color:{INK}!important;}}"},
    'B': {'label': 'B  marker (Gochi Hand)', 'split': False,
          'css': f".wm{{font-family:'WM Gochi',cursive!important;font-weight:400!important;font-size:calc(var(--wm) * 0.92)!important;letter-spacing:0!important;color:{INK}!important;}}"},
    'C': {'label': 'C  masthead ("the" brush + "talks" serif italic)  RECOMMENDED', 'split': True,
          'css': f".wm{{color:{INK}!important;letter-spacing:0!important;font-size:var(--wm)!important;}} .wm .wm-the{{font-family:'WM CaveatBrush',cursive;font-size:var(--the, 0.74em);margin-right:0.1em;display:inline-block;transform:rotate(-6deg) translateY(-0.05em);}} .st-header__talks.wm, .st-drawer__talks.wm{{--the:1.02em;}} .wm .wm-talks{{font-family:'WM SSItalic',serif;font-weight:800;font-variation-settings:'opsz' 60;font-size:0.9em;letter-spacing:-0.02em;}}"},
}
MARK = """(split) => {
  const els = [...document.querySelectorAll('.st-header__talks, .st-drawer__talks')];
  const h1 = [...document.querySelectorAll('h1, .st-talks__title, .st-talks__heading')].find(e => /the talks/i.test(e.textContent || ''));
  if (h1) els.push(h1);
  els.forEach(e => { const fs = parseFloat(getComputedStyle(e).fontSize); e.style.setProperty('--wm', fs + 'px'); e.classList.add('wm');
    if (split && !e.querySelector('.wm-the')) e.innerHTML = '<span class="wm-the">the</span><span class="wm-talks">talks</span>'; });
  return els.map(e => [e.className, getComputedStyle(e).fontSize]);
}"""


RECTS = {}


async def shoot(br, key, w, h, path, crop):
    pg = await br.new_page(viewport={'width': w, 'height': h}, device_scale_factor=2)
    await pg.goto(f'{BASE}{path}?{Q}&_cb={time.time_ns()}', wait_until='load', timeout=120000)
    await pg.add_style_tag(content='[id^="PBar"], #preview-bar-iframe { display: none !important; }' + (FACES + OPTS[key]['css'] if key != 'now' else ''))
    if key != 'now':
        await pg.evaluate(MARK, OPTS[key]['split'])
    await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(700)
    rects = await pg.evaluate("(() => { const t = document.querySelector('.st-header__talks'); const r = (e) => { if (!e) return null; const b = e.getBoundingClientRect(); return [b.left, b.top, b.right, b.bottom]; }; return { link: r(t), the: r(t && t.querySelector('.wm-the')), talks: r(t && t.querySelector('.wm-talks')) }; })()")
    RECTS[f'{key}-{path}-{w}'] = rects
    out = HERE / f'shot-{key}-{path.strip("/").replace("/", "_") or "home"}-{w}.png'
    await pg.screenshot(path=str(out), clip=crop)
    await pg.close()
    return out


async def main():
    shots = {}
    async with async_playwright() as p:
        br = await p.chromium.launch(channel='chrome')
        for key in OPTS:
            shots[key] = [
                await shoot(br, key, 390, 844, '/', {'x': 0, 'y': 0, 'width': 390, 'height': 70}),
                await shoot(br, key, 1536, 703, '/', {'x': 0, 'y': 0, 'width': 1536, 'height': 78}),
                await shoot(br, key, 390, 844, '/blogs/the-talks', {'x': 0, 'y': 0, 'width': 390, 'height': 260}),
                await shoot(br, key, 1536, 703, '/blogs/the-talks', {'x': 0, 'y': 0, 'width': 1536, 'height': 300}),
            ]
            print(key, 'ok')
        await br.close()
    try:
        FT = ImageFont.truetype('arial.ttf', 30); FS = ImageFont.truetype('arial.ttf', 20)
    except OSError:
        FT = FS = ImageFont.load_default()
    W = 2400; blocks = []
    for key, (ph, dh, phub, dhub) in shots.items():
        a, b, c, d = [Image.open(x).convert('RGB') for x in (ph, dh, phub, dhub)]
        b = b.resize((W - a.width - 40, round(b.height * (W - a.width - 40) / b.width)))
        d = d.resize((W - c.width - 40, round(d.height * (W - c.width - 40) / d.width)))
        hgt = 50 + max(a.height, b.height) + 20 + max(c.height, d.height) + 30
        blk = Image.new('RGB', (W, hgt), 'white'); dr = ImageDraw.Draw(blk)
        dr.text((10, 8), OPTS[key]['label'], fill='#c3021d' if key != 'now' else '#666', font=FT)
        y = 50; blk.paste(a, (10, y)); blk.paste(b, (a.width + 30, y)); y += max(a.height, b.height) + 20
        blk.paste(c, (10, y)); blk.paste(d, (c.width + 30, y))
        blocks.append(blk)
    sheet = Image.new('RGB', (W, sum(bk.height for bk in blocks) + 10 * len(blocks)), '#e9e4dc'); y = 0
    for bk in blocks:
        sheet.paste(bk, (0, y)); y += bk.height + 10
    sheet.save(HERE / 'options-sheet.png')
    # real-size check: the 1536 header wordmark at native 2x (device pixels), all options side by side
    zooms = []
    for key in OPTS:
        im = Image.open(HERE / f'shot-{key}-home-1536.png').convert('RGB')
        L = RECTS[f'{key}-/-1536']['link']
        box = (int((L[0] - 24) * 2), 0, int((L[2] + 70) * 2), im.height)
        c = im.crop(box)
        # ink height of "the" (C) or the whole mark, in CSS px: dark rows inside the link box
        def ink_h(x0, x1):
            g = im.crop((int(x0 * 2), 0, int(x1 * 2), im.height)).convert('L'); px = g.load(); rows = [y for y in range(g.height) if any(px[x, y] < 90 for x in range(g.width))]
            return round((rows[-1] - rows[0] + 1) / 2, 1) if rows else 0
        info = f'mark ink height {ink_h(L[0], L[2])} px'
        T = RECTS[f'{key}-/-1536'].get('the')
        if T: info += f'  |  "the" ink height {ink_h(T[0], T[2])} px'
        lab = Image.new('RGB', (max(c.width, 520), c.height + 40), 'white'); d = ImageDraw.Draw(lab)
        d.text((6, 6), f'{OPTS[key]["label"].split("  ")[0]}  (1536 header, 2x)  {info}', fill='#333', font=FS)
        lab.paste(c, (0, 36)); zooms.append(lab)
        print(key, info)
    Z = Image.new('RGB', (sum(z.width for z in zooms) + 20 * len(zooms), max(z.height for z in zooms)), '#e9e4dc'); x = 0
    for z in zooms:
        Z.paste(z, (x, 0)); x += z.width + 20
    Z.save(HERE / 'options-1536-header-2x.png')
    (HERE / 'rects.json').write_text(json.dumps(RECTS, indent=1), encoding='utf-8')
    print('sheet', sheet.size)


asyncio.run(main())
