"""Journal index lab (owner v12.1 §F), nothing written: /blogs/journal on the build preview as written (CURRENT) and with
the staged st-journal + st-journal-card applied (STAGED): every marked desktop block of src/ is injected after the
compiled styles (as tools/store_lab.py --after; only st-journal and st-journal-card, the files this batch changes), plus the snippet's base rule for the campaign art, and each card gets
the campaign image the staged snippet renders (parsed from its `case key` map, so the lab uses the snippet's data).
Measures per size: list frame, column tracks, featured card box, per-row card / link heights (spread), empty cells,
campaign art present and clipped by its media, horizontal overflow, page errors; phones: CURRENT vs STAGED pixel diff.
Output: qa/desktop/owner-v12/journal-<tag>-<WxH>.png (current | staged) and the numbers on stdout.
Usage: python -I tools/journal_lab.py <tag> [WxH ...]"""
import asyncio, json, pathlib, re, sys, time
from playwright.async_api import async_playwright
from PIL import Image, ImageChops, ImageDraw

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
TB = pathlib.Path(__file__).resolve().parents[1]
ARGS = sys.argv[1:]
TAG = ARGS[0] if ARGS and not ARGS[0][0].isdigit() else 'staged'
SIZES = [tuple(int(v) for v in a.split('x')) for a in ARGS if 'x' in a and a[0].isdigit()] or \
    [(390, 844), (1024, 768), (1280, 720), (1536, 703), (1680, 1050), (1920, 1080)]
OUT = TB.parent / 'qa/desktop/owner-v12'
URL = 'https://0nev20-vn.myshopify.com/blogs/journal?preview_theme_id=186651934933&_cb='
BASE = '[id^="PBar"], #preview-bar-iframe { display: none !important; } html, body, .page-wrapper { scroll-behavior: auto !important; }'
GROW = 'html, body { height: auto !important; overflow: visible !important; } .page-wrapper { height: auto !important; overflow: visible !important; }'


def staged_css():
    out = []
    for f in (TB / 'src/sections/st-journal.liquid', TB / 'src/snippets/st-journal-card.liquid'):  # the files this batch changes
        s = f.read_text(encoding='utf-8')
        for m in re.finditer(r'/\* BEGIN store desktop.*?\*/(.*?)/\* END store desktop \*/', s, re.S):
            out.append(f'/* {f.name} */\n' + m.group(1))
    card = (TB / 'src/snippets/st-journal-card.liquid').read_text(encoding='utf-8')
    m = re.search(r'(\.st-jcard__char \{\s*display: none;\s*\})', card)
    return m.group(1) + '\n' + '\n'.join(out)


NEW_ASSETS = ['st-hd-shaadi-shift-woman.webp']  # staged, not on the theme yet: served from src/assets


def _serve(f):
    async def handler(route):
        await route.fulfill(path=str(f), content_type='image/webp')
    return handler


async def route_new_assets(pg):
    for name in NEW_ASSETS:
        await pg.route(f'**/assets/{name}*', _serve(TB / 'src/assets' / name))


def char_map():
    s = (TB / 'src/snippets/st-journal-card.liquid').read_text(encoding='utf-8')
    body = s[s.index('  case key'):s.index('  endcase')]
    out = {}
    for blk in re.split(r"\n    when '", body)[1:]:
        key = blk.split("'", 1)[0]
        g = lambda n: (re.search(rf"assign {n} = '?([^'\n]*)'?", blk) or [None, ''])[1]
        out[key] = dict(f=g('char'), w=g('char_w'), h=g('char_h'), pos=g('char_pos'), mod=g('char_mod'))
    return out


INJECT = """([css, map]) => {
  const st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
  const base = (document.querySelector('[style*="st-hd-nails"]').getAttribute('style').match(/url\\('?([^')]+\\/)st-hd-nails/) || [])[1];
  document.querySelectorAll('.st-jcard').forEach((card) => {
    const a = card.querySelector('a'); const key = (a.getAttribute('href') || '').split('/').pop().split('?')[0];
    const m = map[key]; const media = card.querySelector('.st-jcard__media');
    if (!m || !media) return;
    const img = document.createElement('img');
    img.className = 'st-jcard__char' + m.mod; img.src = base + m.f + '?v=lab'; img.width = +m.w; img.height = +m.h; img.alt = '';
    img.loading = 'lazy'; img.decoding = 'async'; img.setAttribute('style', m.pos); media.appendChild(img);
  });
}"""

MEASURE = """() => {
  const r = (e) => { const b = e.getBoundingClientRect(); return [Math.round(b.left), Math.round(b.top + scrollY), Math.round(b.width), Math.round(b.height)]; };
  const list = document.querySelector('.st-journal__list'); const cs = getComputedStyle(list);
  const cards = [...list.children].map((li) => {
    const media = li.querySelector('.st-jcard__media'); const ch = li.querySelector('.st-jcard__char');
    let art = null;
    if (ch) { const m = media.getBoundingClientRect(), c = ch.getBoundingClientRect();
      art = { shown: getComputedStyle(ch).display !== 'none', loaded: ch.complete && ch.naturalWidth > 0,
        cut: [c.left < m.left - 0.5 && 'left', c.right > m.right + 0.5 && 'right', c.top < m.top - 0.5 && 'top', c.bottom > m.bottom + 0.5 && 'bottom'].filter(Boolean),
        visW: Math.round(Math.min(c.right, m.right) - Math.max(c.left, m.left)) }; }
    return { key: (li.querySelector('a').getAttribute('href') || '').split('/').pop(), featured: li.classList.contains('st-jcard--featured'),
      box: r(li), link: r(li.querySelector('a')), media: r(media), art };
  });
  const rows = {}; cards.filter((c) => !c.featured).forEach((c) => { (rows[c.box[1]] = rows[c.box[1]] || []).push(c); });
  const cols = cs.gridTemplateColumns.split(' ').length;
  return { vw: innerWidth, list: r(list), cols, tracks: cs.gridTemplateColumns, gap: cs.gap,
    rows: Object.values(rows).map((rw) => ({ n: rw.length, h: rw.map((c) => c.box[3]), linkH: rw.map((c) => c.link[3]), keys: rw.map((c) => c.key) })),
    cards, hscroll: document.documentElement.scrollWidth - innerWidth,
    name: [...document.querySelectorAll('.st-jcard__name')].map((e) => parseFloat(getComputedStyle(e).fontSize)) };
}"""


async def render(br, w, h, staged):
    ctx = await br.new_context(viewport={'width': w, 'height': h}, reduced_motion='reduce', device_scale_factor=1)
    pg = await ctx.new_page()
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)[:120]))
    await route_new_assets(pg)
    await pg.goto(URL + str(time.time_ns()), wait_until='load', timeout=120000)
    await pg.add_style_tag(content=BASE)
    if staged:
        await pg.evaluate(INJECT, [staged_css(), char_map()])
    await pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager')")
    for _ in range(100):
        if not await pg.evaluate("[...document.images].filter(i => i.offsetParent && (!i.complete || !i.naturalWidth)).length"):
            break
        await pg.wait_for_timeout(200)
    await pg.evaluate("Promise.race([Promise.all([...document.images].map(i => i.decode ? i.decode().catch(() => 0) : 0)), new Promise(r => setTimeout(r, 3000))])")
    await pg.evaluate('document.fonts.ready')
    if w >= 990:
        await pg.add_style_tag(content=GROW)
    await pg.wait_for_timeout(600)
    data = await pg.evaluate(MEASURE)
    main = await pg.evaluate("(() => { const b = document.querySelector('.st-journal').getBoundingClientRect(); return [b.top + scrollY, b.bottom + scrollY]; })()")
    f = OUT / f'_j-{w}x{h}-{int(staged)}.png'
    await pg.screenshot(path=str(f), full_page=True, animations='disabled')
    await ctx.close()
    im = Image.open(f).convert('RGB')
    f.unlink(missing_ok=True)
    im = im.crop((0, max(0, int(main[0]) - 20), im.width, min(im.height, int(main[1]) + 10)))
    return im, data, errs


def pair(a, b, la, lb, scale):
    a = a.resize((int(a.width * scale), int(a.height * scale)), Image.LANCZOS)
    b = b.resize((int(b.width * scale), int(b.height * scale)), Image.LANCZOS)
    s = Image.new('RGB', (a.width + b.width + 30, max(a.height, b.height) + 40), 'white')
    d = ImageDraw.Draw(s)
    d.text((10, 10), la, fill='black'); d.text((a.width + 20, 10), lb, fill='black')
    s.paste(a, (10, 30)); s.paste(b, (a.width + 20, 30))
    return s


async def main():
    async with async_playwright() as p:
        br = await p.chromium.launch(channel='chrome')
        for w, h in SIZES:
            ci, cd, ce = await render(br, w, h, False)
            si, sd, se = await render(br, w, h, True)
            pair(ci, si, f'{w}x{h} Journal CURRENT (build as written)', f'{w}x{h} Journal STAGED §F', 1 if w < 600 else 0.5).save(OUT / f'journal-{TAG}-{w}x{h}.png')
            print(f'== {w}x{h}  errors current {ce or "none"} staged {se or "none"}')
            if w < 1024:
                same = ci.size == si.size and not ImageChops.difference(ci, si).getbbox()
                print(f'   phone diff current vs staged: {"none (pixel-identical)" if same else "DIFFERENT " + str(ImageChops.difference(ci, si).getbbox() if ci.size == si.size else (ci.size, si.size))}; art shown: {[c["key"] for c in sd["cards"] if c["art"] and c["art"]["shown"]] or "none"}')
                continue
            for lab, d in (('current', cd), ('staged', sd)):
                fe = next((c for c in d['cards'] if c['featured']), None)
                print(f'   {lab:7} list x{d["list"][0]} w{d["list"][2]} | cols {d["cols"]} ({d["tracks"]}) gap {d["gap"]} | featured {fe["box"][2]}x{fe["box"][3]} media {fe["media"][2]}x{fe["media"][3]} | hscroll {d["hscroll"]}')
                for rw in d['rows']:
                    print(f'           row {rw["n"]}/{d["cols"]}: card h {rw["h"]} (spread {max(rw["h"]) - min(rw["h"])}), link h {rw["linkH"]} {rw["keys"]}')
                if lab == 'staged':
                    for c in d['cards']:
                        a = c['art']
                        print(f'           {c["key"]:14} media {c["media"][2]}x{c["media"][3]} art {"loaded" if a and a["loaded"] else "MISSING"} cut {a and a["cut"]}')
                    print(f'           name sizes {sorted(set(d["name"]))}')
        await br.close()


if __name__ == '__main__':
    asyncio.run(main())
