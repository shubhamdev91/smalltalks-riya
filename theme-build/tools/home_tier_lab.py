"""Home for Tier A (>= 1680 wide frame), nothing written. (1) Below 1680: the landing lab before Tier A (a saved copy of
lab/landing.html, given with --before) vs lab/landing.html now, whole page, pixel diff (must be identical). (2) At 1680 /
1920: CURRENT = the build preview's home as written, STAGED = lab/landing.html (tools/build_landing.py: the staged CSS,
map, joins and chapter script), whole page side by side, and per section QA's metrics (LAPTOP-AUDIT-2): the content's
union box (visible text, images, controls; beelines and grounds excluded) as % of the width with the empty left / right
fields, "narrow centre" (<= 62 % with both fields >= 15 %), art >= 60 px cut >= 5 % by the section box or the screen and
on which sides (corner = a horizontal and a vertical side; bottom / left / right are the chapters' intended bleed, top
is not), the longest text measure (ch of its own font), images above their intrinsic width at DPR 1.
Output: qa/desktop/tier-a/home-<WxH>.png. Usage: python -I tools/home_tier_lab.py --before <file> [WxH ...]"""
import asyncio, json, pathlib, re, sys, time
from playwright.async_api import async_playwright
from PIL import Image, ImageChops, ImageDraw

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
TB = pathlib.Path(__file__).resolve().parents[1]
ARGS = sys.argv[1:]
BEFORE = pathlib.Path(ARGS[ARGS.index('--before') + 1]) if '--before' in ARGS else None
SIZES = [tuple(int(v) for v in a.split('x')) for a in ARGS if re.fullmatch(r'\d+x\d+', a)] or [(1024, 768), (1280, 720), (1536, 703), (1680, 1050), (1920, 1080)]
OUT = TB.parent / 'qa/desktop/tier-a'
OUT.mkdir(parents=True, exist_ok=True)
PREVIEW = 'https://0nev20-vn.myshopify.com/?preview_theme_id=186651934933&_cb='
BASE = '[id^="PBar"], #preview-bar-iframe { display: none !important; } html, body, .page-wrapper { scroll-behavior: auto !important; }'
GROW = 'html, body { height: auto !important; overflow: visible !important; } .page-wrapper { height: auto !important; overflow: visible !important; }'

MEASURE = """() => {
  const vw = document.documentElement.clientWidth;
  const vis = (e) => { const cs = getComputedStyle(e); if (cs.visibility === 'hidden' || +cs.opacity === 0 || cs.display === 'none') return null;
    const b = e.getBoundingClientRect(); return b.width > 1 && b.height > 1 ? b : null; };
  return [...document.querySelectorAll('.st-land[data-land]')].map((s) => {
    const sb = s.getBoundingClientRect(); let L = 1e9, R = -1e9;
    const pr = document.createElement('div'); pr.style.cssText = 'position:absolute;height:calc(var(--nc, 0) * var(--kt, var(--k, 1px)))'; s.appendChild(pr);
    const own = sb.bottom - pr.getBoundingClientRect().height; pr.remove();
    const take = (b) => { if (b.right < sb.left || b.left > sb.right || b.bottom < sb.top || b.top >= own - 1) return; L = Math.min(L, Math.max(0, b.left)); R = Math.max(R, Math.min(vw, b.right)); };
    const arts = [];
    s.querySelectorAll('img').forEach((i) => { const b = vis(i); if (!b) return; take(b);
      if (b.top >= own - 1) return;  // the next chapter's cap art (scored with that chapter)
      if (b.width >= 60 && b.height >= 60) { const cut = []; const ca = (a) => a / (b.width * b.height);
        const l = Math.max(0, sb.left - b.left, 0 - b.left), r = Math.max(0, b.right - sb.right, b.right - vw), t = Math.max(0, sb.top - b.top), bt = Math.max(0, b.bottom - sb.bottom);
        const pc = (v) => Math.round(v * 100);
        if (l / b.width >= 0.05) cut.push('left ' + pc(l / b.width)); if (r / b.width >= 0.05) cut.push('right ' + pc(r / b.width));
        if (t / b.height >= 0.05) cut.push('top ' + pc(t / b.height)); if (bt / b.height >= 0.05) cut.push('bottom ' + pc(bt / b.height));
        const name = (i.currentSrc || i.src).split('/').pop().split('?')[0].replace(/\\.webp|\\.svg|\\.png/, '').slice(0, 30);
        const up = i.naturalWidth && !/\\.svg/.test(i.currentSrc || i.src) && !getComputedStyle(i).rotate.match(/deg/) ? b.width / i.naturalWidth : 0;
        arts.push({ name, cut, up: +up.toFixed(2), w: Math.round(b.width), nat: i.naturalWidth }); } });
    s.querySelectorAll('a, button').forEach((e) => { const b = vis(e); if (b && b.width < vw * 0.98) take(b); });
    const tw = document.createTreeWalker(s, NodeFilter.SHOW_TEXT); let worst = null;
    const blocks = new Set();
    while (tw.nextNode()) { const n = tw.currentNode; if (!n.textContent.trim()) continue; const p = n.parentElement; if (!p || p.closest('svg, [aria-hidden=true]')) continue;
      const rg = document.createRange(); rg.selectNodeContents(n); for (const b of rg.getClientRects()) if (b.width > 1) take(b);
      let e = p; while (e && e !== s && /^inline/.test(getComputedStyle(e).display)) e = e.parentElement; if (e) blocks.add(e); }
    blocks.forEach((b) => { const txt = b.innerText.trim(); if (txt.length < 60) return; const cs = getComputedStyle(b);
      const lh = parseFloat(cs.lineHeight) || parseFloat(cs.fontSize) * 1.2; const r = b.getBoundingClientRect(); if (r.height < lh * 1.8) return;
      const sp = document.createElement('span'); sp.textContent = '0'.repeat(50); sp.style.cssText = `position:absolute;visibility:hidden;white-space:nowrap;font:${cs.font}`;
      document.body.appendChild(sp); const ch = sp.getBoundingClientRect().width / 50; sp.remove();
      const m = Math.round((r.width - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight)) / ch);
      if (!worst || m > worst.ch) worst = { ch: m, t: txt.slice(0, 30) }; });
    const pct = (R - L) / vw * 100;
    return { key: s.dataset.land, pct: +pct.toFixed(1), eL: Math.round(L), eR: Math.round(vw - R),
      narrow: pct <= 62 && L >= vw * 0.15 && vw - R >= vw * 0.15, arts, measure: worst };
  });
}"""


async def load(br, w, h, url, grow_wait=True):
    ctx = await br.new_context(viewport={'width': w, 'height': h}, reduced_motion='reduce', device_scale_factor=1)
    pg = await ctx.new_page()
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)[:120]))
    await pg.goto(url + str(time.time_ns()), wait_until='load', timeout=120000)
    await pg.add_style_tag(content=BASE)
    await pg.evaluate("document.querySelectorAll('.st-land').forEach(s => s.style.contentVisibility = 'visible')")
    await pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager'); document.querySelectorAll('img[data-st-src]').forEach(i => { if (!i.getAttribute('src')) i.src = i.dataset.stSrc; })")
    for y in range(0, 16000, 500):
        await pg.evaluate(f'window.scrollTo(0, {y}); (document.querySelector(".page-wrapper") || {{}}).scrollTop = {y}')
        await pg.wait_for_timeout(20)
    for _ in range(100):
        if not await pg.evaluate("[...document.images].filter(i => i.getAttribute('src') && i.offsetParent && (!i.complete || !i.naturalWidth)).length"):
            break
        await pg.wait_for_timeout(200)
    await pg.evaluate("Promise.race([Promise.all([...document.images].map(i => i.decode ? i.decode().catch(() => 0) : 0)), new Promise(r => setTimeout(r, 3000))])")
    await pg.evaluate('document.fonts.ready')
    await pg.add_style_tag(content=GROW)
    await pg.evaluate('window.scrollTo(0, 0); (document.querySelector(".page-wrapper") || {}).scrollTop = 0; dispatchEvent(new Event("resize"))')
    await pg.wait_for_timeout(1500)
    return ctx, pg, errs


async def shot(pg, name):
    f = OUT / f'_{name}.png'
    await pg.screenshot(path=str(f), full_page=True, animations='disabled')
    im = Image.open(f).convert('RGB')
    f.unlink(missing_ok=True)
    return im


def strong(a, b):
    """pixels differing by more than 16 levels in any channel (Chrome's full-page captures of the lab differ by
    sub-threshold antialiasing from run to run)"""
    if a.size != b.size:
        return f'SIZE {a.size} vs {b.size}'
    d = ImageChops.difference(a, b).convert('L').point(lambda v: 255 if v > 16 else 0)
    n = d.histogram()[255]
    return f'{n} px > 16 levels' + (f' in {d.getbbox()}' if n else '')


def pair(a, b, la, lb, scale=0.35):
    a = a.resize((int(a.width * scale), int(a.height * scale)), Image.LANCZOS)
    b = b.resize((int(b.width * scale), int(b.height * scale)), Image.LANCZOS)
    s = Image.new('RGB', (a.width + b.width + 30, max(a.height, b.height) + 40), 'white')
    d = ImageDraw.Draw(s)
    d.text((10, 10), la, fill='black'); d.text((a.width + 20, 10), lb, fill='black')
    s.paste(a, (10, 30)); s.paste(b, (a.width + 20, 30))
    return s


async def main():
    lab = (TB / 'lab/landing.html').as_uri() + '?_cb='
    async with async_playwright() as p:
        br = await p.chromium.launch(channel='chrome')
        for w, h in SIZES:
            if w < 1680:
                if not BEFORE:
                    continue
                c1, p1, e1 = await load(br, w, h, BEFORE.as_uri() + '?_cb=')
                a = await shot(p1, f'hb-{w}'); await c1.close()
                c2, p2, e2 = await load(br, w, h, lab)
                b = await shot(p2, f'ha-{w}'); await c2.close()
                c3, p3, e3 = await load(br, w, h, lab)
                b2 = await shot(p3, f'ha2-{w}'); await c3.close()
                print(f'== home lab {w}x{h}: before vs after Tier A: {strong(a, b)}; after vs after (render noise baseline): {strong(b, b2)}  errors {e1 or e2 or e3 or "none"}')
                continue
            res = {}
            for tag, url in (('current', PREVIEW), ('staged', lab)):
                ctx, pg, errs = await load(br, w, h, url)
                if tag == 'staged':  # the laptop beeline is on hold for st-fable's respec: not part of these sheets
                    await pg.add_style_tag(content='.st-beecur { display: none !important; }')
                    await pg.wait_for_timeout(200)
                res[tag] = (await shot(pg, f'h{tag}-{w}'), await pg.evaluate(MEASURE), errs)
                await ctx.close()
            pair(res['current'][0], res['staged'][0], f'home {w}x{h} CURRENT (build preview as written)', f'home {w}x{h} STAGED (v12.1 + Tier A, lab; laptop beeline on hold, hidden)').save(OUT / f'home-{w}x{h}.png')
            print(f'== home {w}x{h}  errors current {res["current"][2] or "none"} staged {res["staged"][2] or "none"}')
            cur = {s['key']: s for s in res['current'][1]}
            for s in res['staged'][1]:
                c = cur.get(s['key'])
                cuts = '; '.join(f'{a["name"]} {"+".join(a["cut"])}' for a in s['arts'] if a['cut'])
                top = [a['name'] for a in s['arts'] if any(c.startswith('top') for c in a['cut'])]
                up = [f'{a["name"]} {a["w"]}/{a["nat"]}' for a in s['arts'] if a['up'] > 1.01]
                print(f'   {s["key"]:20} content {c["pct"] if c else "-":>5}% -> {s["pct"]:5}%  empty L/R {s["eL"]}/{s["eR"]}{"  NARROW" if s["narrow"] else ""}'
                      f'  measure {s["measure"]["ch"] if s["measure"] else "-"}ch  cuts [{cuts}]{"  TOP CUT " + str(top) if top else ""}{"  UPSCALED " + str(up) if up else ""}')
        await br.close()


if __name__ == '__main__':
    asyncio.run(main())
