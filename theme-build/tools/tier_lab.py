"""Tier A lab (>= 1680 wide frame; orchestrator 10 Oct, QA LAPTOP-AUDIT-2), nothing written. Store pages on the build
preview as written (CURRENT) and STAGED: the batch's own blocks injected after the compiled styles: every
"/* BEGIN wide frame ... */ ... /* END wide frame */" block of src/ (all inside @media (min-width: 1680px)) and, on the
Journal, owner v12.1 §F (st-journal + st-journal-card desktop blocks and the snippet's campaign images; see
tools/journal_lab.py).
Per page and size: the main content's union box (visible text, images, controls) against the viewport (QA's content %
and empty left / right), the longest text measure (the longest rendered line of any text block, in its own font's ch),
images rendered above their intrinsic width at DPR 1, horizontal overflow, page errors; help: topics vs form heights;
collection: the last row's card positions. At 1536 (and any size < 1680) STAGED with vs without the wide-frame blocks is
pixel-diffed against a no-change baseline (changes above 16 levels; they must match the baseline). Sheets: qa/desktop/tier-a/<page>-<WxH>.png (current | staged).
Usage: python -I tools/tier_lab.py [--pages help,shop,...] [WxH ...]"""
import asyncio, json, pathlib, re, sys, time
from playwright.async_api import async_playwright
from PIL import Image, ImageChops, ImageDraw

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
TB = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TB / 'tools'))
ARGS = sys.argv[1:]
opt = lambda n, d: ARGS[ARGS.index(n) + 1] if n in ARGS else d
SIZES = [tuple(int(v) for v in a.split('x')) for a in ARGS if re.fullmatch(r'\d+x\d+', a)] or [(1536, 703), (1680, 1050), (1920, 1080)]
OUT = TB.parent / 'qa/desktop/tier-a'
OUT.mkdir(parents=True, exist_ok=True)
ORIGIN = 'https://0nev20-vn.myshopify.com'
PAGES = {
    'help': '/pages/help', 'shop': '/collections/all', 'pdp': '/products/bill-idhar', 'journal': '/blogs/journal',
    'our-story': '/pages/our-story', 'story': '/blogs/journal/on-me', 'guide': '/pages/nail-guide',
    'guide-desi': '/pages/nail-guide-desi', '404': '/pages/st-not-a-page',
}
KEYS = opt('--pages', ','.join(PAGES)).split(',')
BASE = '[id^="PBar"], #preview-bar-iframe { display: none !important; } html, body, .page-wrapper { scroll-behavior: auto !important; }'
GROW = 'html, body { height: auto !important; overflow: visible !important; } .page-wrapper { height: auto !important; overflow: visible !important; }'


def blocks(pattern, files):
    out = []
    for f in files:
        s = f.read_text(encoding='utf-8')
        for m in re.finditer(pattern, s, re.S):
            out.append(f'/* {f.name} */\n' + m.group(1))
    return '\n'.join(out)


def wide_css():
    files = sorted([*(TB / 'src/sections').glob('*.liquid'), *(TB / 'src/snippets').glob('*.liquid'), *(TB / 'src/blocks').glob('*.liquid')])
    return blocks(r'/\* BEGIN wide frame.*?\*/(.*?)/\* END wide frame \*/', files)


def journal_css():
    import journal_lab
    return journal_lab.staged_css(), journal_lab.char_map(), journal_lab.INJECT


MEASURE = """() => {
  const vw = innerWidth;
  const main = document.querySelector('#MainContent') || document.querySelector('main');
  const vis = (e) => { const cs = getComputedStyle(e); if (cs.visibility === 'hidden' || +cs.opacity === 0) return null;
    const b = e.getBoundingClientRect(); return b.width > 1 && b.height > 1 ? b : null; };
  let L = 1e9, R = -1e9;
  const take = (b) => { L = Math.min(L, Math.max(0, b.left)); R = Math.max(R, Math.min(vw, b.right)); };
  main.querySelectorAll('img, svg, video, button, input, textarea, select, a').forEach((e) => { const b = vis(e); if (b && b.width < vw * 0.98) take(b); });
  const tw = document.createTreeWalker(main, NodeFilter.SHOW_TEXT);
  const textEls = new Set();
  while (tw.nextNode()) { const n = tw.currentNode; if (!n.textContent.trim()) continue; const p = n.parentElement; if (!p) continue;
    const rg = document.createRange(); rg.selectNodeContents(n); for (const b of rg.getClientRects()) if (b.width > 1) take(b); textEls.add(p); }
  // measure: per block-level text container, its longest rendered line (line boxes of its text, grouped by line top)
  // in its own font's ch (only blocks with >= 60 characters)
  const blk = (e) => { while (e && e !== main) { const d = getComputedStyle(e).display; if (!/^inline/.test(d)) return e; e = e.parentElement; } return null; };
  const seen = new Set(); let worst = [];
  textEls.forEach((p) => { const b = blk(p); if (!b || seen.has(b)) return; seen.add(b);
    const txt = b.innerText.trim(); if (txt.length < 60) return;
    const cs = getComputedStyle(b);
    const lines = {}; const w2 = document.createTreeWalker(b, NodeFilter.SHOW_TEXT);
    while (w2.nextNode()) { const n = w2.currentNode; if (!n.textContent.trim() || blk(n.parentElement) !== b) continue;
      const rg = document.createRange(); rg.selectNodeContents(n);
      for (const r of rg.getClientRects()) { if (r.width < 1) continue; const k = Math.round(r.top / 4); lines[k] = lines[k] || [1e9, -1e9]; lines[k][0] = Math.min(lines[k][0], r.left); lines[k][1] = Math.max(lines[k][1], r.right); } }
    const lw = Math.max(0, ...Object.values(lines).map(([a, z]) => z - a));
    const s = document.createElement('span'); s.textContent = '0'.repeat(50); s.style.cssText = `position:absolute;visibility:hidden;white-space:nowrap;font:${cs.font};letter-spacing:${cs.letterSpacing}`;
    document.body.appendChild(s); const ch = s.getBoundingClientRect().width / 50; s.remove();
    worst.push({ ch: Math.round(lw / ch), w: Math.round(lw), fs: parseFloat(cs.fontSize), el: (b.className || b.tagName).toString().slice(0, 40), t: txt.slice(0, 40) }); });
  worst.sort((a, b) => b.ch - a.ch);
  const up = [...main.querySelectorAll('img')].filter((i) => vis(i) && i.naturalWidth && !/\\.svg/.test(i.currentSrc || i.src)).map((i) => {
    const b = i.getBoundingClientRect(); const fit = getComputedStyle(i).objectFit;
    let need = b.width;
    if (fit === 'cover') need = Math.max(b.width, b.height * i.naturalWidth / i.naturalHeight);
    return { src: (i.currentSrc || i.src).split('/').pop().split('?')[0].slice(0, 50), shown: Math.round(need), natural: i.naturalWidth, x: +(need / i.naturalWidth).toFixed(2) };
  }).filter((o) => o.x > 1.01);
  const out = { content: [Math.round(L), Math.round(R)], pct: +((R - L) / vw * 100).toFixed(1), emptyL: Math.round(L), emptyR: Math.round(vw - R),
    measure: worst.slice(0, 3), upscaled: up, hscroll: Math.max(document.documentElement.scrollWidth, (document.querySelector('.page-wrapper') || {}).scrollWidth || 0) - vw };
  const hb = document.querySelector('.st-help__blocks');
  if (hb) { const k = [...hb.children].map((e) => e.getBoundingClientRect());
    const last = [...hb.querySelectorAll('.st-topic__item')].pop(); const btn = hb.querySelector('.st-help-form button[type=submit], .st-help-form button');
    out.help = { cells: k.map((b) => Math.round(b.height)), lastDividerBottom: last && Math.round(last.getBoundingClientRect().bottom), buttonBottom: btn && Math.round(btn.getBoundingClientRect().bottom) }; }
  const g = document.querySelector('.st-shop__grid');
  if (g) { const li = [...g.children].map((e) => e.getBoundingClientRect()); const rows = {};
    li.forEach((b) => { (rows[Math.round(b.top)] = rows[Math.round(b.top)] || []).push([Math.round(b.left), Math.round(b.width)]); });
    const gb = g.getBoundingClientRect(); out.shop = { grid: [Math.round(gb.left), Math.round(gb.right)], rows: Object.values(rows) }; }
  return out;
}"""


async def render(br, w, h, key, wide, journal):
    ctx = await br.new_context(viewport={'width': w, 'height': h}, reduced_motion='reduce', device_scale_factor=1)
    pg = await ctx.new_page()
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)[:120]))
    path = PAGES[key]
    import journal_lab
    await journal_lab.route_new_assets(pg)
    await pg.goto(f'{ORIGIN}{path}{"&" if "?" in path else "?"}preview_theme_id=186651934933&_cb={time.time_ns()}', wait_until='load', timeout=120000)
    await pg.add_style_tag(content=BASE)
    if journal and key == 'journal':
        css, cmap, inject = journal_css()
        await pg.evaluate(inject, [css, cmap])
    if wide:
        await pg.add_style_tag(content=wide_css())
    await pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager'); document.querySelectorAll('img[data-st-src]').forEach(i => { if (!i.src) i.src = i.dataset.stSrc; })")
    for _ in range(80):
        if not await pg.evaluate("[...document.images].filter(i => i.offsetParent && i.getAttribute('src') && (!i.complete || !i.naturalWidth)).length"):
            break
        await pg.wait_for_timeout(200)
    await pg.evaluate("Promise.race([Promise.all([...document.images].map(i => i.decode ? i.decode().catch(() => 0) : 0)), new Promise(r => setTimeout(r, 3000))])")
    await pg.evaluate('document.fonts.ready')
    await pg.wait_for_timeout(500)
    data = await pg.evaluate(MEASURE)
    await pg.add_style_tag(content=GROW)
    await pg.wait_for_timeout(300)
    f = OUT / f'_t-{key}-{w}-{int(wide)}.png'
    await pg.screenshot(path=str(f), full_page=True, animations='disabled')
    await ctx.close()
    im = Image.open(f).convert('RGB')
    f.unlink(missing_ok=True)
    return im, data, errs


def strong(a, b):
    """pixels differing by more than 16 levels in any channel (sub-threshold antialiasing varies between captures)"""
    if a.size != b.size:
        return f'SIZE {a.size} vs {b.size}'
    d = ImageChops.difference(a, b).convert('L').point(lambda v: 255 if v > 16 else 0)
    n = d.histogram()[255]
    return f'{n} px > 16 levels' + (f' in {d.getbbox()}' if n else '')


def pair(a, b, la, lb, scale=0.5):
    a = a.resize((int(a.width * scale), int(a.height * scale)), Image.LANCZOS)
    b = b.resize((int(b.width * scale), int(b.height * scale)), Image.LANCZOS)
    s = Image.new('RGB', (a.width + b.width + 30, max(a.height, b.height) + 40), 'white')
    d = ImageDraw.Draw(s)
    d.text((10, 10), la, fill='black'); d.text((a.width + 20, 10), lb, fill='black')
    s.paste(a, (10, 30)); s.paste(b, (a.width + 20, 30))
    return s


def line(tag, d):
    m = d['measure'][0] if d['measure'] else None
    s = f'   {tag:8} content {d["pct"]}% (empty L {d["emptyL"]} / R {d["emptyR"]})  measure max {m["ch"] if m else "-"}ch' \
        f'{f" ({m["el"]}, {m["fs"]}px: {m["t"]!r})" if m else ""}  hscroll {d["hscroll"]}'
    if d.get('upscaled'):
        s += f'\n            UPSCALED: {d["upscaled"]}'
    if d.get('help'):
        s += f'\n            help cells {d["help"]["cells"]}  last divider bottom {d["help"]["lastDividerBottom"]} vs button bottom {d["help"]["buttonBottom"]}'
    if d.get('shop'):
        s += f'\n            shop grid x {d["shop"]["grid"]}  rows {[[c[0] for c in r] for r in d["shop"]["rows"]]}  card w {d["shop"]["rows"][0][0][1]}'
    return s


async def main():
    async with async_playwright() as p:
        br = await p.chromium.launch(channel='chrome')
        for key in KEYS:
            for w, h in SIZES:
                if w < 1680:
                    a, da, ea = await render(br, w, h, key, False, True)
                    b, db, eb = await render(br, w, h, key, True, True)
                    c, dc, ec = await render(br, w, h, key, False, True)
                    print(f'== {key} {w}x{h}: staged with vs without the wide-frame blocks: {strong(a, b)}; without vs without (render noise baseline): {strong(a, c)}  errors {ea or eb or ec or "none"}')
                    continue
                a, da, ea = await render(br, w, h, key, False, False)
                b, db, eb = await render(br, w, h, key, True, True)
                pair(a, b, f'{key} {w}x{h} CURRENT (build as written)', f'{key} {w}x{h} STAGED (Tier A{" + Journal §F" if key == "journal" else ""})').save(OUT / f'{key}-{w}x{h}.png')
                print(f'== {key} {w}x{h}  errors current {ea or "none"} staged {eb or "none"}')
                print(line('current', da))
                print(line('staged', db))
        await br.close()


if __name__ == '__main__':
    asyncio.run(main())
