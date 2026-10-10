"""Shop lab (board 5 frame 1): markup = sections/st-shop.liquid + snippets/st-product-card.liquid output, CSS from those
files plus the header and footer sections, fonts and tokens. Writes lab/shop.html, shoots it at 390 and makes the
side-by-side with spec/crops/shop@390.png. Usage: python -I tools/build_shop_lab.py"""
import asyncio, pathlib, re, subprocess, sys
from PIL import Image
from playwright.async_api import async_playwright

TB = pathlib.Path(__file__).resolve().parents[1]
RIYA = TB.parent
ART = RIYA / 'artwork'
SRC = TB / 'src'
A = lambda p: (ART / p).as_uri()


def css_of(path):
    s = (SRC / path).read_text(encoding='utf-8')
    return s.split('{% stylesheet %}')[1].split('{% endstylesheet %}')[0] if '{% stylesheet %}' in s else ''


ORDER = [('on-me', 'On Me', 'Rs. 599'), ('brainwave', 'Brainwave', 'Rs. 599'), ('green-flag', 'Green Flag', 'Rs. 499'),
         ('shaadi-shift', 'Shaadi Shift', 'Rs. 699'), ('diet-cherry', 'Diet Cherry', 'Rs. 599'),
         ('wild-card', 'Wild Card', 'Rs. 699'), ('pinky-promise', 'Pinky Promise', 'Rs. 499')]


NAILS = {'on-me': '0,2,1,0', 'brainwave': '0,1,0,1', 'green-flag': '1,0,1,0', 'shaadi-shift': '1,2,0,2',
         'diet-cherry': '1,0,2,1', 'wild-card': '1,0,2', 'pinky-promise': '0,0,0,0'}


def card(key, name, price, first):
    im = Image.open(ART / f'packaging/web/{key}.webp'); w, h = im.size
    im13 = Image.open(ART / f'packaging/web/{key}@1.3x.webp'); w13 = im13.size[0]
    nails = ''.join(f'<span class="st-card__nail" style="--col: {c}; --i: {i}"></span>' for i, c in enumerate(NAILS[key].split(',')))
    return f'''<li><article class="st-card" data-set="{key}"><a class="st-card__link" href="#">
<span class="st-card__tile"><span class="st-card__art" style="--box-aspect: {w} / {h}; --box-ar: {round(w / h, 4)}"><img class="st-card__pack" src="{A(f'packaging/web/{key}.webp')}" srcset="{A(f'packaging/web/{key}.webp')} {w}w, {A(f'packaging/web/{key}@1.3x.webp')} {w13}w" sizes="28vw" width="{w}" height="{h}" alt="" loading="eager"><span class="st-card__nails" style="--st-nails: url('{A(f'nails/web/{key}.webp')}')" aria-hidden="true">{nails}</span></span></span>
<div class="st-card__row"><h3 class="st-card__title">{name}</h3><span class="st-card__price"><span class="price">{price}</span></span></div>
<span class="st-card__cta"><span class="st-card__cta-text">View set</span> <span class="st-arrow" aria-hidden="true">→</span></span>
</a></article></li>'''


def page():
    tokens = (SRC / 'assets/st-tokens.css').read_text(encoding='utf-8')
    fonts = (SRC / 'snippets/st-fonts.liquid').read_text(encoding='utf-8').split('{% style %}')[1].split('{% endstyle %}')[0]
    fonts = re.sub(r"\{\{ '([^']+)' \| asset_url \}\}", lambda m: (TB / 'fonts/out' / m.group(1)).as_uri(), fonts)
    css = css_of('sections/st-header.liquid') + css_of('sections/st-shop.liquid') + css_of('snippets/st-product-card.liquid') + css_of('snippets/st-pack-art.liquid') + css_of('sections/st-footer.liquid')
    st_display = (pathlib.Path(r'C:/Users/SSTS/AppData/Local/Temp/claude/C--Users-SSTS-Desktop-Riya/84af96b7-cadf-4ec1-a2eb-81c8910c84b9/scratchpad/dl_font/st-font-4.woff2')).as_uri()
    cards = ''.join(card(k, n, p, i == 0) for i, (k, n, p) in enumerate(ORDER))
    nav = ''.join(f'<li><a href="#">{l}</a></li>' for l in ['Shop', 'Our Story', 'the talks', 'Journal', 'Nail Guide'])
    legal = ''.join(f'<li><a href="#">{l}</a></li>' for l in ['Contact us', 'Shipping policy', 'Privacy policy'])
    return f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Shop lab</title>
<style>{tokens}{fonts}
@font-face {{ font-family: 'ST Display'; src: url('{st_display}') format('woff2'); }}
:root {{ --st-font-display: 'ST Display', Georgia, serif; --minimum-touch-target: 44px; --safe-area-inset-left: 0px; --safe-area-inset-right: 0px; --normal-page-width: 100%; --st-gutter: 1rem; }}
* {{ box-sizing: border-box; }} body {{ margin: 0; background: var(--st-paper); }} ul {{ margin: 0; }}
.visually-hidden {{ position: absolute !important; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); }}
{css}</style>
<div class="st-header"><div class="st-header__bar">
<div class="st-header__menu"><button class="st-header__icon-button"><svg class="st-header__burger" width="28" height="24" viewBox="0 0 28 24" fill="none"><path d="M1 1.75h26M1 12h26M1 22.25h26" stroke="currentColor" stroke-width="2.5"/></svg></button></div>
<a class="st-logo" href="#"><span class="st-logo__words"><span>small</span><span>talk</span></span></a><nav class="st-header__nav"></nav>
<div class="st-header__actions"><a href="#" class="st-header__talks">the talks</a><a href="#" class="st-header__icon-button st-header__bag"><span class="st-header__cart-icon"><svg class="st-header__bag-icon" width="36" height="39" viewBox="0 0 26 28" fill="none"><path d="M4.5 9h17l2 16.5h-21L4.5 9Z" stroke="currentColor" stroke-width="1.45" stroke-linejoin="round"/><path d="M9 11V6.5a4 4 0 0 1 8 0V11" stroke="currentColor" stroke-width="1.45" stroke-linecap="round"/></svg></span></a></div>
</div></div>
<section class="st-shop"><header class="st-shop__header"><h1 class="st-shop__heading">Pick your plot twist.</h1>
<p class="st-shop__note">Same nails.<br><span class="st-shop__note-2">Different moods.</span><svg class="st-shop__arrow" viewBox="0 0 40 48" aria-hidden="true"><path d="M6 3 C 18 6, 26 16, 24 30 C 23 37, 22 41, 21 45 M14 37 L21 45 L29 38"/></svg></p></header>
<nav class="st-shop__chips"><a class="st-shop__chip" href="#" aria-current="page">All sets</a><a class="st-shop__chip" href="#">Everyday</a><a class="st-shop__chip" href="#">Statement</a></nav>
<ul class="st-shop__grid" role="list">{cards}</ul></section>
<div class="st-footer st-footer--rows"><nav class="st-footer__nav"><ul role="list">{nav}</ul></nav><ul class="st-footer__legal" role="list">{legal}</ul></div>
</html>'''


async def shoot():
    out = TB / 'lab/shop.html'
    out.write_text(page(), encoding='utf-8')
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        pg = await b.new_page(viewport={'width': 390, 'height': 844})
        await pg.goto(out.as_uri())
        await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(500)
        m = await pg.evaluate('''(() => { const r = s => { const e = document.querySelector(s); if (!e) return null; const b = e.getBoundingClientRect(); return [b.left, b.top, b.right, b.bottom].map(Math.round); };
          return { h1: r('.st-shop__heading'), note: r('.st-shop__note'), chips: r('.st-shop__chips'), grid: r('.st-shop__grid'), tile: r('.st-card__tile'),
                   title: r('.st-card__title'), cta: r('.st-card__cta'), footer: r('.st-footer'), page: document.documentElement.scrollHeight }; })()''')
        await pg.screenshot(path=str(TB / 'lab/shots/shop-390.png'), full_page=True)
        await b.close()
    print(m)
    board = RIYA / 'spec/crops/shop@390.png'
    subprocess.run([sys.executable, '-I', str(RIYA / 'qa/fidelity/sbs.py'), str(TB / 'lab/shots/shop-390.png'), str(board),
                    str(TB / 'lab/shots/shop-390-vs-board.png'), 'shop'], cwd=RIYA, capture_output=True)

asyncio.run(shoot())
