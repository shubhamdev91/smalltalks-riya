"""On Me / Pinky row check (st-fable's closing-row conditions) and On Me receipt / Pinky clasp check (st-fable's option D conditions) on lab/landing.html at the test viewports: caption right
ink edge vs W - 18 (k-scaled), pill -> caption gap (>= 16), name stroke -> caption (>= 10), the receipt hand's lowest
nail vs the fold (the chapter's own end) and its slip vs the caption's bottom (>= 8). Ink of the caption is measured on
a transparent-ground screenshot of it alone; the receipt's nails / slip from their rows in the image (43-89 % / 1.5 %).
Usage: python -I tools/onme_check.py"""
import asyncio, io, pathlib, sys
from playwright.async_api import async_playwright
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
TB = pathlib.Path(__file__).resolve().parents[1]
KEY = __import__('os').environ.get('ST_KEY', 'on-me')
VIEWS = [(440, 768), (430, 744), (390, 664), (440, 956), (430, 932), (390, 844), (320, 568), (1280, 800)]
NAIL_BOTTOM, SLIP_TOP = 515 / 581, 9 / 581


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        for w, h in VIEWS:
            pg = await b.new_page(viewport={'width': w, 'height': h})
            await pg.goto((TB / 'lab/landing.html').as_uri(), wait_until='load')
            await pg.evaluate('document.fonts.ready')
            g = await pg.evaluate("""((KEY) => { const s = document.querySelector(`.st-ch[data-land="${KEY}"]`); window.scrollTo(0, s.getBoundingClientRect().top + scrollY); const r = s.getBoundingClientRect();
              const B = (e) => { const b = e.getBoundingClientRect(); return [b.left - r.left, b.top - r.top, b.right - r.left, b.bottom - r.top]; };
              const d = document.createElement('div'); d.style.cssText = 'position:absolute;height:var(--hc);width:var(--k)'; s.appendChild(d); const hc = d.getBoundingClientRect().height, k = d.getBoundingClientRect().width; d.remove();
              const imgs = [...s.querySelectorAll('.st-land__art img')]; const hand = imgs.find(i => i.src.includes(KEY === 'on-me' ? 'receipt' : 'pinky'));
              return { k, hc, inner: B(s.querySelector('.st-land__inner')), pill: B(s.querySelector('.st-ch__pill')), name: B(s.querySelector('.st-ch__name')), cap: B(s.querySelector('.st-ch__caption')), hand: B(hand), secTop: r.top }; })""", KEY)
            # caption ink: screenshot with only the caption visible on a transparent ground
            await pg.add_style_tag(content='.lab-cap-only, .lab-cap-only * { visibility: hidden !important; } .lab-cap-only .st-ch__caption, .lab-cap-only .st-ch__caption * { visibility: visible !important; } html.lab-cap-only, .lab-cap-only body { background: transparent !important; } .lab-cap-only .st-land { background: none !important; -webkit-mask: none !important; mask: none !important; }')
            await pg.evaluate("document.documentElement.classList.add('lab-cap-only')")
            png = await pg.screenshot(omit_background=True, clip={'x': 0, 'y': g['secTop'], 'width': w, 'height': min(g['hc'], h - g['secTop'])})
            await pg.evaluate("document.documentElement.classList.remove('lab-cap-only')")
            a = Image.open(io.BytesIO(png)).getchannel('A').point(lambda v: 255 if v > 60 else 0)
            bb = a.getbbox()
            ink = (bb[0], bb[1], bb[2], bb[3]) if bb else None
            k, hc = g['k'], g['hc']
            x0 = g['inner'][0]
            hand = g['hand']; hh = hand[3] - hand[1]
            nails_b = hand[1] + hh * (NAIL_BOTTOM if KEY == 'on-me' else 677 / 797)
            slip_t = hand[1] + hh * (SLIP_TOP if KEY == 'on-me' else 370 / 797)   # Pinky: the clasp's top
            eyes = hand[1] + hh * (240 / 797) if KEY != 'on-me' else None
            right_margin = (x0 + 390 * k) - ink[2]
            print(f"{w}x{h}  k {k:.3f}  caption ink x {ink[0] - x0:.0f}-{ink[2] - x0:.0f} (right margin {right_margin:.1f} vs {18 * k:.1f})"
                  f"  pill->cap {ink[0] - g['pill'][2]:.0f}  name->cap {ink[1] - g['name'][3]:.0f}"
                  f"  pill centre {(g['pill'][1] + g['pill'][3]) / 2:.0f} / cap box centre {(g['cap'][1] + g['cap'][3]) / 2:.0f}"
                  f"  lowest nail {nails_b:.0f} vs fold {hc:.0f} ({hc - nails_b:+.0f})  {'slip' if KEY == 'on-me' else 'clasp'} top {slip_t:.0f} vs cap ink bottom {ink[3]:.0f} ({slip_t - ink[3]:+.0f})"
                  + (f"  eyes {eyes:.0f} vs pill bottom {g['pill'][3]:.0f} ({eyes - g['pill'][3]:+.0f})" if eyes else ''))
            await pg.close()
        await b.close()


asyncio.run(main())
