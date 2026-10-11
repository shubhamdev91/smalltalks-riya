"""st-fable: refined ORIGINAL "the talks" (Caveat, OFL) variants + the small "goes somewhere" arrow, rendered in context on
the build preview (lab only): site header phone 390 + desktop 1536, hub title phone + desktop, and a 2x real-size crop of
the 1536 header. Writes caveat-sheet.png, caveat-1536-header-2x.png, caveat-measure.json."""
import asyncio, base64, json, pathlib, sys, time
from playwright.async_api import async_playwright
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding='utf-8')
HERE = pathlib.Path(__file__).resolve().parent
F = pathlib.Path(r'C:/Users/SSTS/Desktop/Riya/spec/fonts')
BASE = 'https://0nev20-vn.myshopify.com'
Q = 'preview_theme_id=186651934933'
FACE = "@font-face{font-family:'WM Caveat';src:url(data:font/ttf;base64,%s) format('truetype');font-weight:400 700;font-display:block;}" % base64.b64encode((F / 'caveat' / 'Caveat[wght].ttf').read_bytes()).decode()
INK = '#0d0b10'
SWASH = "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 12' preserveAspectRatio='none'%3E%3Cpath d='M2 8 C 25 3, 55 2, 98 6' fill='none' stroke='%23c3021d' stroke-width='2.4' stroke-linecap='round'/%3E%3C/svg%3E\")"
COMMON = f""".wmc{{display:inline-flex;align-items:baseline;gap:0;color:{INK};font-family:'WM Caveat',cursive;white-space:nowrap;line-height:1;}}
.wmc .t, .wmc .k{{display:inline-block;}}
h1 .wmc{{margin-bottom:0.22em;}}
.wmc-arr{{font-family:var(--font-ui,'DM Sans'),sans-serif;font-weight:500;font-size:0.5em;line-height:1;margin-left:0.22em;align-self:center;transform:translateY(-0.12em);color:{INK};}}"""
VARS = {
    'now': {'label': 'NOW: Caveat 600 (no arrow)', 'css': None},
    'V1': {'label': 'V1  confident: Caveat 700, tracking -0.015em, tilt -3deg, ink + arrow',
           'css': ".wmc{font-weight:700;letter-spacing:-0.015em;transform:rotate(-3deg);} .wmc .t{margin-right:0.2em;}"},
    'V2': {'label': 'V2  swash: V1 + a soft red underline swash under "talks"  (RECOMMENDED)',
           'css': f".wmc{{font-weight:700;letter-spacing:-0.015em;transform:rotate(-3deg);}} .wmc .t{{margin-right:0.2em;}} .wmc .k{{padding-bottom:0.16em;background:{SWASH} left bottom / 100% 0.3em no-repeat;}}"},
    'V3': {'label': 'V3  two-weight: "the" 500 lifted + "talks" 700',
           'css': ".wmc{letter-spacing:-0.02em;transform:rotate(-2deg);} .wmc .t{font-weight:500;font-size:0.78em;margin-right:0.16em;transform:translateY(-0.18em);} .wmc .k{font-weight:700;font-size:1.06em;}"},
    'V2+': {'label': 'V2 at +10 % header size (size variant)', 'css': None, 'base': 'V2', 'scale': 1.1},
}
MARK = """([arrow, scale]) => {
  const out = [];
  const header = [...document.querySelectorAll('.st-header__talks, .st-drawer__talks')];
  const h1 = [...document.querySelectorAll('h1')].find(e => /the talks/i.test(e.textContent || ''));
  const all = header.concat(h1 ? [h1] : []);
  all.forEach(e => {
    const isHeader = e.classList.contains('st-header__talks') || e.classList.contains('st-drawer__talks');
    const fs = parseFloat(getComputedStyle(e).fontSize) * (isHeader ? scale : 1);
    e.innerHTML = '<span class="wmc" style="font-size:' + fs + 'px"><span class="t">the</span><span class="k">talks</span></span>' + (arrow && e.classList.contains('st-header__talks') ? '<span class="wmc-arr" aria-hidden="true">\\u2197</span>' : '');
    e.style.fontFamily = 'inherit';
  });
  const t = document.querySelector('.st-header__talks'); const b = t.getBoundingClientRect();
  const w = t.querySelector('.wmc'), a = t.querySelector('.wmc-arr');
  const r = (x) => x ? (() => { const q = x.getBoundingClientRect(); return [q.left, q.top, q.right, q.bottom]; })() : null;
  return { link: [b.left, b.top, b.right, b.bottom], mark: r(w), arrow: r(a), target: [Math.round(b.width), Math.round(b.height)] };
}"""
MEAS = {}


async def shoot(br, key, w, h, path, crop):
    v = VARS[key]; css = v['css'] if v.get('css') is not None else (VARS[v['base']]['css'] if v.get('base') else None)
    pg = await br.new_page(viewport={'width': w, 'height': h}, device_scale_factor=2)
    await pg.goto(f'{BASE}{path}?{Q}&_cb={time.time_ns()}', wait_until='load', timeout=120000)
    await pg.add_style_tag(content='[id^="PBar"], #preview-bar-iframe { display: none !important; }' + ((FACE + COMMON + css) if css else ''))
    if css:
        MEAS[f'{key}-{path}-{w}'] = await pg.evaluate(MARK, [True, v.get('scale', 1)])
    else:
        MEAS[f'{key}-{path}-{w}'] = await pg.evaluate("(() => { const t = document.querySelector('.st-header__talks'); const b = t.getBoundingClientRect(); return { link: [b.left, b.top, b.right, b.bottom], target: [Math.round(b.width), Math.round(b.height)] }; })()")
    await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(700)
    out = HERE / f'cv-{key.replace("+", "p")}-{path.strip("/").replace("/", "_") or "home"}-{w}.png'
    await pg.screenshot(path=str(out), clip=crop)
    await pg.close()
    return out


async def main():
    shots = {}
    async with async_playwright() as p:
        br = await p.chromium.launch(channel='chrome')
        for key in VARS:
            shots[key] = [await shoot(br, key, 390, 844, '/', {'x': 0, 'y': 0, 'width': 390, 'height': 70}),
                          await shoot(br, key, 1536, 703, '/', {'x': 0, 'y': 0, 'width': 1536, 'height': 78}),
                          await shoot(br, key, 390, 844, '/blogs/the-talks', {'x': 0, 'y': 0, 'width': 390, 'height': 260}),
                          await shoot(br, key, 1536, 703, '/blogs/the-talks', {'x': 0, 'y': 0, 'width': 1536, 'height': 300})]
            print(key, 'ok', MEAS.get(f'{key}-/-1536', {}).get('target'))
        await br.close()
    FT = ImageFont.truetype('arial.ttf', 30); FS = ImageFont.truetype('arial.ttf', 20)
    W = 2400; blocks = []
    for key, (ph, dh, phub, dhub) in shots.items():
        a, b, c, d = [Image.open(x).convert('RGB') for x in (ph, dh, phub, dhub)]
        b = b.resize((W - a.width - 40, round(b.height * (W - a.width - 40) / b.width)))
        d = d.resize((W - c.width - 40, round(d.height * (W - c.width - 40) / d.width)))
        blk = Image.new('RGB', (W, 50 + max(a.height, b.height) + 20 + max(c.height, d.height) + 30), 'white'); dr = ImageDraw.Draw(blk)
        dr.text((10, 8), VARS[key]['label'], fill='#c3021d' if key != 'now' else '#666', font=FT)
        y = 50; blk.paste(a, (10, y)); blk.paste(b, (a.width + 30, y)); y += max(a.height, b.height) + 20
        blk.paste(c, (10, y)); blk.paste(d, (c.width + 30, y)); blocks.append(blk)
    sheet = Image.new('RGB', (W, sum(k.height for k in blocks) + 10 * len(blocks)), '#e9e4dc'); y = 0
    for k in blocks:
        sheet.paste(k, (0, y)); y += k.height + 10
    sheet.save(HERE / 'caveat-sheet.png')
    zooms = []
    for key in VARS:
        im = Image.open(HERE / f'cv-{key.replace("+", "p")}-home-1536.png').convert('RGB'); L = MEAS[f'{key}-/-1536']['link']
        c = im.crop((int((L[0] - 24) * 2), 0, int((L[2] + 70) * 2), im.height))
        g = im.crop((int(L[0] * 2), 0, int(L[2] * 2), im.height)).convert('L'); px = g.load()
        rows = [yy for yy in range(g.height) if any(px[xx, yy] < 90 for xx in range(g.width))]
        ink = round((rows[-1] - rows[0] + 1) / 2, 1) if rows else 0
        lab = Image.new('RGB', (max(c.width, 560), c.height + 40), 'white'); dr = ImageDraw.Draw(lab)
        dr.text((6, 6), f'{key}  (1536 header, 2x)  ink {ink} px  target {MEAS[f"{key}-/-1536"]["target"]}', fill='#333', font=FS)
        lab.paste(c, (0, 36)); zooms.append(lab)
        MEAS[f'{key}-/-1536']['ink'] = ink
    Z = Image.new('RGB', (sum(z.width for z in zooms) + 20 * len(zooms), max(z.height for z in zooms)), '#e9e4dc'); x = 0
    for z in zooms:
        Z.paste(z, (x, 0)); x += z.width + 20
    Z.save(HERE / 'caveat-1536-header-2x.png')
    (HERE / 'caveat-measure.json').write_text(json.dumps(MEAS, indent=1), encoding='utf-8')
    print('done', sheet.size, Z.size)


asyncio.run(main())
