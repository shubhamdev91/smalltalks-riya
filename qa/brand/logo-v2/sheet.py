"""st-fable: logo v2 concept sheet. For CURRENT + A/B/C: hero; one-colour on cream / reversed on brand blue / black on
white; in the real site header (build preview, logo image swapped in the browser only) at 1536 and 390; favicon at 32/16
px for the full stacked mark and for the simplified monogram. Writes LOGO-V2-SHEET.png and the per-variant SVGs."""
import asyncio, base64, pathlib, sys, time
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from playwright.async_api import async_playwright
from PIL import Image, ImageDraw, ImageFont
import make_logo as M

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / 'shots'; OUT.mkdir(exist_ok=True)
BLUE, CREAM, INK = '#001df9', '#fdf6e9', '#0d0b10'
KEYS = ['current', 'A', 'B', 'C']
LABEL = {'current': 'CURRENT (official logo)', 'A': 'A  nail "l": the last "l" of "small" is an almond press-on nail',
         'B': 'B  brush "k": the k\'s leg is one polish-brush stroke, tapering off',
         'C': 'C  bead "k": the k\'s arm ends in a teardrop terminal, a bead of polish'}
# monogram crops (viewBox in logo units): the edited letter; current uses "st"-less full mark only
MONO = {'A': (1162, 0, 174, 452), 'B': (862, 456, 330, 362), 'C': (862, 456, 330, 362)}
PREVIEW = 'https://0nev20-vn.myshopify.com/?preview_theme_id=186651934933'


def vsvg(k, fill):
    return M.svg(M.VARS.get(k), fill) if k != 'current' else M.svg(None, fill)


def mono_svg(k, fill, bg):
    x, y, w, h = MONO[k]
    inner = vsvg(k, fill); inner = inner[inner.index('>') + 1:-6]
    side = max(w, h) * 1.34; cx, cy = x + w / 2, y + h / 2
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{cx - side / 2:.0f} {cy - side / 2:.0f} {side:.0f} {side:.0f}">'
            f'<defs><clipPath id="mc{k}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath></defs>'
            f'<rect x="{cx - side / 2:.0f}" y="{cy - side / 2:.0f}" width="{side:.0f}" height="{side:.0f}" rx="{side * 0.22:.0f}" fill="{bg}"/>'
            f'<g clip-path="url(#mc{k})">{inner}</g></svg>')


def full_icon_svg(k, fill, bg):
    inner = vsvg(k, fill); inner = inner[inner.index('>') + 1:-6]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-82 -341 1500 1500"><rect x="-82" y="-341" width="1500" height="1500" rx="330" fill="{bg}"/>{inner}</svg>')


def uri(svg):
    return 'data:image/svg+xml;base64,' + base64.b64encode(svg.encode()).decode()


async def main():
    for k in ['A', 'B', 'C']:
        (HERE / f'logo-v2-{k}.svg').write_text(vsvg(k, BLUE), encoding='utf-8')
    async with async_playwright() as p:
        br = await p.chromium.launch(channel='chrome')
        # 1. static tiles (hero, colourways, favicons)
        pg = await br.new_page(viewport={'width': 1400, 'height': 1000}, device_scale_factor=1)
        for k in KEYS:
            html = f"""<!doctype html><style>body{{margin:0;font-family:Arial}} .t{{display:inline-block;vertical-align:top}} svg{{display:block;width:100%;height:auto;overflow:hidden}}</style>
            <div id=hero class=t style="background:{CREAM};padding:40px 48px;width:760px"><div style="width:760px">{vsvg(k, BLUE)}</div></div>
            <div id=cw class=t style="display:flex">
              <div style="background:{CREAM};padding:28px;width:280px">{vsvg(k, BLUE)}</div>
              <div style="background:{BLUE};padding:28px;width:280px">{vsvg(k, CREAM)}</div>
              <div style="background:#fff;padding:28px;width:280px">{vsvg(k, '#000')}</div></div>"""
            await pg.set_content(html); await pg.wait_for_timeout(200)
            await (await pg.query_selector('#hero')).screenshot(path=str(OUT / f'{k}-hero.png'))
            await (await pg.query_selector('#cw')).screenshot(path=str(OUT / f'{k}-colourways.png'))
            # favicons: full mark (as today) and monogram, at 32 and 16 device px
            icons = [('full', full_icon_svg(k, BLUE, '#ffffff'))] + ([('mono', mono_svg(k, CREAM, BLUE))] if k in MONO else [])
            for name, sv in icons:
                for px in (32, 16):
                    await pg.set_content(f'<body style="margin:0;background:#e9e4dc"><img id=i src="{uri(sv)}" width={px} height={px} style="display:block"></body>')
                    await pg.wait_for_timeout(120)
                    await (await pg.query_selector('#i')).screenshot(path=str(OUT / f'{k}-fav-{name}-{px}.png'))
        await pg.close()
        # 2. real header on the build preview (logo image swapped in this browser only)
        for k in KEYS:
            for w, h in [(1536, 703), (390, 844)]:
                pg = await br.new_page(viewport={'width': w, 'height': h}, device_scale_factor=2)
                await pg.goto(PREVIEW + f'&_cb={time.time_ns()}', wait_until='load', timeout=120000)
                await pg.add_style_tag(content='[id^="PBar"], #preview-bar-iframe { display: none !important; }')
                if k != 'current':
                    await pg.evaluate("(u) => document.querySelectorAll('.st-logo__mark').forEach(i => { i.removeAttribute('srcset'); i.src = u; })", uri(vsvg(k, BLUE)))
                await pg.wait_for_timeout(700)
                await pg.screenshot(path=str(OUT / f'{k}-header-{w}.png'), clip={'x': 0, 'y': 0, 'width': w if w < 900 else 760, 'height': 80})
                await pg.close()
        await br.close()
    # 3. compose
    FT = ImageFont.truetype('arial.ttf', 26); FS = ImageFont.truetype('arial.ttf', 17)
    rows = []
    for k in KEYS:
        hero = Image.open(OUT / f'{k}-hero.png').convert('RGB')
        cw = Image.open(OUT / f'{k}-colourways.png').convert('RGB')
        hd = Image.open(OUT / f'{k}-header-1536.png').convert('RGB'); hd = hd.resize((hd.width // 2 * 2 // 2, hd.height // 2))  # 2x → 1x
        hp = Image.open(OUT / f'{k}-header-390.png').convert('RGB'); hp = hp.resize((hp.width // 2, hp.height // 2))
        W = 2700; H = 46 + max(hero.height, cw.height + 20 + 2 * 90 + 30 + 160)
        row = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(row)
        d.text((14, 10), LABEL[k], fill='#c3021d' if k != 'current' else '#555', font=FT)
        row.paste(hero, (14, 46))
        x0 = hero.width + 40; y = 46
        row.paste(cw, (x0, y)); d.text((x0, y + cw.height + 2), 'blue on cream · reversed on brand blue · black on white', fill='#666', font=FS)
        y += cw.height + 26
        row.paste(hd, (x0, y)); d.text((x0 + hd.width + 10, y + 30), 'site header 1536', fill='#666', font=FS); y += hd.height + 10
        row.paste(hp, (x0, y)); d.text((x0 + hp.width + 10, y + 30), 'site header 390', fill='#666', font=FS); y += hp.height + 18
        # favicons: actual size + 4x nearest
        fx = x0
        for name in ['full', 'mono']:
            if not (OUT / f'{k}-fav-{name}-32.png').exists():
                continue
            f32 = Image.open(OUT / f'{k}-fav-{name}-32.png').convert('RGB'); f16 = Image.open(OUT / f'{k}-fav-{name}-16.png').convert('RGB')
            row.paste(f32, (fx, y + 20)); row.paste(f16, (fx + 40, y + 28))
            row.paste(f32.resize((128, 128), Image.NEAREST), (fx + 70, y + 20)); row.paste(f16.resize((64, 64), Image.NEAREST), (fx + 206, y + 20))
            d.text((fx, y), f'favicon {"full mark" if name == "full" else "monogram"}: 32 / 16 px (real, then 4x)', fill='#666', font=FS)
            fx += 520
        rows.append(row)
    sheet = Image.new('RGB', (2700, sum(r.height for r in rows) + 12 * len(rows)), '#e9e4dc'); y = 0
    for r in rows:
        sheet.paste(r, (0, y)); y += r.height + 12
    sheet.save(HERE / 'LOGO-V2-SHEET.png')
    print('sheet', sheet.size)


asyncio.run(main())
