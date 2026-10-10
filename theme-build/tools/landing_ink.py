"""Ink boxes for the chapter stack: renders lab/landing.html at 390 (k = 1, so css px = board px) and, per chapter and
part (note, slogan, nail row, name, pill, caption), screenshots the section with only that part visible on a
transparent ground; the alpha bounding box is the part's real ink. Writes lab/ink.json: per chapter and part
[top, bottom, left, right] in board px relative to the section, plus the set positions they came from (POS), so
tools/build_landing.py can place the stack on visible gaps. Usage: python -I tools/landing_ink.py"""
import asyncio, io, json, pathlib, sys
from playwright.async_api import async_playwright
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
TB = pathlib.Path(__file__).resolve().parents[1]
CHAPTERS = ['diet-cherry', 'brainwave', 'green-flag', 'shaadi-shift', 'on-me', 'wild-card', 'pinky-promise']
PARTS = {'note': '.st-ch__note', 'head': '.st-ch__headline', 'nails': '.st-ch__nails', 'name': '.st-ch__name', 'pill': '.st-ch__pill', 'cap': '.st-ch__caption'}
CSS = """html, body { background: transparent !important; }
.lab-header { display: none !important; }
.st-ch.lab-ink { background: none !important; -webkit-mask: none !important; mask: none !important; }
.st-ch.lab-ink .st-land__beeline, .st-ch.lab-ink .st-land__art, .st-ch.lab-ink .st-land__ticks,
.st-ch.lab-ink :is(.st-ch__note, .st-ch__headline, .st-ch__nails, .st-ch__name, .st-ch__pill, .st-ch__caption) { visibility: hidden !important; }
.st-ch.lab-ink .lab-show, .st-ch.lab-ink .lab-show * { visibility: visible !important; }
.st-ch.lab-ink .st-ch__name::after { display: none !important; }  /* the name's box = the marker stroke, not the soft flash */
body.lab-ink-mode > .shopify-section:not(:has(.lab-ink)) { visibility: hidden !important; }"""


async def main():
    out, hc_by_key = {}, {}
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        pg = await b.new_page(viewport={'width': 390, 'height': 900}, device_scale_factor=1)
        await pg.goto((TB / 'lab/landing.html').as_uri(), wait_until='load')
        await pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager')")
        await pg.add_style_tag(content=CSS)
        await pg.evaluate('document.fonts.ready')
        for key in CHAPTERS:
            sel = f'.st-ch[data-land="{key}"]'
            await pg.evaluate(f"document.body.classList.add('lab-ink-mode'); document.querySelectorAll('.st-ch').forEach(s => s.classList.toggle('lab-ink', s.matches('{sel}')))")
            box = await pg.evaluate(f"""(() => {{ const s = document.querySelector('{sel}'); window.scrollTo(0, s.getBoundingClientRect().top + scrollY); const r = s.getBoundingClientRect();
                const d = document.createElement('div'); d.style.cssText = 'position:absolute;height:var(--hc)'; s.appendChild(d); const h = d.getBoundingClientRect().height; d.remove();
                return {{ x: r.left, y: r.top, w: r.width, h }}; }})()""")
            res = {}
            for part, psel in PARTS.items():
                n = await pg.evaluate(f"""(() => {{ const s = document.querySelector('{sel}'); s.querySelectorAll('.lab-show').forEach(e => e.classList.remove('lab-show'));
                    const e = s.querySelector('{psel}'); if (!e) return 0; e.classList.add('lab-show'); return 1; }})()""")
                if not n:
                    continue
                png = await pg.screenshot(omit_background=True, clip={'x': box['x'], 'y': box['y'], 'width': box['w'], 'height': box['h']})
                a = Image.open(io.BytesIO(png)).getchannel('A').point(lambda v: 255 if v > 60 else 0)
                bb = a.getbbox()
                if bb:
                    W, H = a.size
                    px = a.load()
                    top, bot = [None] * W, [None] * W
                    for x in range(bb[0], bb[2]):
                        ys = [y for y in range(bb[1], bb[3]) if px[x, y]]
                        if ys:
                            top[x], bot[x] = ys[0], ys[-1] + 1
                    res[part] = {'box': [bb[1], bb[3], bb[0], bb[2]], 'top': top, 'bot': bot}
            await pg.evaluate(f"document.querySelector('{sel}').querySelectorAll('.lab-show').forEach(e => e.classList.remove('lab-show'))")
            out[key] = res
            hc_by_key[key] = box['h']
            print(key, {k: v['box'] for k, v in res.items()})
        await b.close()
    pos = json.loads((TB / 'lab/pos.json').read_text(encoding='utf-8')) if (TB / 'lab/pos.json').exists() else {}
    for k, v in hc_by_key.items():
        pos.setdefault(k, {})['hc'] = v
    (TB / 'lab/ink.json').write_text(json.dumps({'ink': out, 'pos': pos}, indent=1), encoding='utf-8')


asyncio.run(main())
