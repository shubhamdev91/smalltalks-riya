"""Hero v3.7.1 load plan on the preview: home at 390 under Slow 4G (150 ms RTT, 1.6 Mbps) + 4x CPU, fresh profile.
Prints the head preloads, the first image requests in order (with start / end ms), the tone vs collage timing, LCP,
and console / page errors. Part 2 (fonts): on home, a PDP, a Journal story and the talks hub at 390, every visible
text character is checked against the cmap of the subset woff2 its computed font-family resolves to (or the DM Sans
fallback the stacks carry); anything left would fall to a system font.
Usage: python -I tools/w6_verify.py [load] [fonts]"""
import asyncio, json, pathlib, re, sys, time
from fontTools.ttLib import TTFont
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
TB = pathlib.Path(__file__).resolve().parents[1]
O = 'https://0nev20-vn.myshopify.com'
Q = 'preview_theme_id=186651934933'
PARTS = sys.argv[1:] or ['load', 'fonts']


def url(path):
    return f"{O}{path}{'&' if '?' in path else '?'}{Q}&_cb={time.time_ns()}"


async def load(b):
    ctx = await b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2)
    pg = await ctx.new_page()
    cdp = await ctx.new_cdp_session(pg)
    await cdp.send('Network.enable')
    await cdp.send('Network.emulateNetworkConditions', {'offline': False, 'latency': 150, 'downloadThroughput': 1.6e6 / 8, 'uploadThroughput': 750e3 / 8})
    await cdp.send('Emulation.setCPUThrottlingRate', {'rate': 4})
    errs = []
    pg.on('pageerror', lambda e: errs.append('PAGEERROR ' + str(e)[:200]))
    pg.on('console', lambda m: errs.append('console ' + m.text[:200]) if m.type == 'error' else None)
    await pg.add_init_script("""window.__lcp = []; new PerformanceObserver(l => l.getEntries().forEach(e => window.__lcp.push([Math.round(e.startTime), e.url ? e.url.split('/').pop().split('?')[0] : (e.element && e.element.tagName)]))).observe({ type: 'largest-contentful-paint', buffered: true });
      window.__ready = null; document.addEventListener('DOMContentLoaded', () => { const mark = () => { const c = document.querySelector('.st-tiles__collage.is-ready'); if (c && window.__ready === null) window.__ready = Math.round(performance.now()); }; mark();
        new MutationObserver(mark).observe(document.documentElement, { subtree: true, attributes: true, attributeFilter: ['class'] }); });""")
    await pg.goto(url('/'), wait_until='load', timeout=180000)
    await pg.wait_for_timeout(6000)
    html = await pg.content()
    head = html.split('</head>')[0]
    pre = re.findall(r'<link[^>]*rel="preload"[^>]*>', head)
    first_css = head.find('stylesheet')
    print('head preloads (before the first stylesheet: %s):' % all(head.find(p) < first_css for p in pre[:2]))
    for p in pre:
        print('   ', re.sub(r'//[^"]*/', '', p)[:160])
    res = await pg.evaluate("""performance.getEntriesByType('resource').filter(e => e.initiatorType === 'img' || e.initiatorType === 'css' || e.initiatorType === 'link' || /\\.(webp|png|jpe?g|avif|gif)(\\?|$)/.test(e.name))
      .filter(e => /\\.(webp|png|jpe?g|avif|gif|svg)(\\?|$)/.test(e.name)).map(e => [e.name.split('/').pop().split('?')[0], Math.round(e.startTime), Math.round(e.responseEnd), e.initiatorType])""")
    res.sort(key=lambda r: r[1])
    print('first 10 image requests (name, start ms, end ms, initiator):')
    for r in res[:10]:
        print('   ', r)
    tone = next((r for r in res if r[0].startswith('st-hd-tone-')), None)
    collage = [r for r in res if r[0].startswith('st-hd-nails-') and not r[0].startswith('st-hd-nails-on-me')]
    before_tone_end = [r[0] for r in res if tone and r[1] < tone[2] and r[0] != tone[0] and not r[0].startswith('st-hd-nails-on-me')]
    print('tone', tone, '| collage .is-ready at', await pg.evaluate('window.__ready'), 'ms | first other sheet start',
          min((r[1] for r in collage), default=None), '| images started before the tone ended (excl. set-1 sheet):', before_tone_end)
    print('LCP entries', await pg.evaluate('window.__lcp'))
    print('liquid', [x for x in ('Liquid error', 'translation missing') if x in html] or 'clean', '| errors', [e for e in errs if 'shop.app' not in e and 'Content Security' not in e and 'status of 403' not in e] or 'none')
    await ctx.close()


FAMILY_FILES = {  # computed family (first in stack) -> subset files by weight/style
    'fraunces': {700: 'st-fraunces-700', 900: 'st-fraunces-900'},
    'caveat': {0: 'st-caveat'}, 'barlow semi condensed': {600: 'st-barlow-sc-600', 700: 'st-barlow-sc-700'}, 'kalam': {0: 'st-kalam-300'},
    'ibm plex sans condensed': {0: 'st-plex-cond-700'}, 'dm sans': {0: 'st-dm-sans'},
    'source serif 4': {500: 'st-source-serif-500', 700: 'st-source-serif-700', 900: 'st-source-serif-900', 'italic': 'st-source-serif-italic-400'},
}
CMAPS = {}


def cmap(name):
    if name not in CMAPS:
        CMAPS[name] = set(TTFont(TB / 'src/assets' / f'{name}.woff2').getBestCmap())
    return CMAPS[name]


async def fonts(b):
    ctx = await b.new_context(viewport={'width': 390, 'height': 844})
    pg = await ctx.new_page()
    stacks = {}
    for path in ['/', '/products/bill-idhar', '/blogs/journal/on-me', '/blogs/the-talks']:
        await pg.goto(url(path), wait_until='load', timeout=120000)
        await pg.wait_for_timeout(800)
        runs = await pg.evaluate("""(() => { const out = {}; const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
          let n; while ((n = w.nextNode())) { const t = n.nodeValue; if (!t.trim()) continue; const el = n.parentElement; if (!el || el.closest('script,style,noscript,template,[hidden]')) continue;
            const cs = getComputedStyle(el); if (cs.display === 'none' || cs.visibility === 'hidden') continue;
            const key = cs.fontFamily + '|' + cs.fontWeight + '|' + cs.fontStyle; out[key] = (out[key] || '') + t; }
          return out; })()""")
        for key, text in runs.items():
            stacks.setdefault(key, set()).update(ch for ch in text if not ch.isspace())
        await asyncio.sleep(3)
    problems = []
    for key, chars in sorted(stacks.items()):
        fam, weight, style = key.split('|')
        families = [f.strip().strip('"\'').lower() for f in fam.split(',')]
        first = families[0]
        files = FAMILY_FILES.get(first)
        if not files:
            print('  (not a theme face)', fam[:60], weight, ''.join(sorted(chars))[:40])
            continue
        w = int(weight)
        f = files.get('italic') if style == 'italic' and 'italic' in files else files.get(w) or files.get(0) or files[min((k for k in files if isinstance(k, int)), key=lambda k: abs(k - w))]
        missing = sorted(ch for ch in chars if ord(ch) not in cmap(f))
        dm = 'dm sans' in families
        left = [ch for ch in missing if not (dm and ord(ch) in cmap('st-dm-sans'))]
        tag = 'OK' if not left else 'SYSTEM FALLBACK'
        print(f'  {tag:15} {first:24} {weight:>3} {style:6} {len(chars):3} chars  via {f}  non-ASCII [{"".join(sorted(c for c in chars if ord(c) > 0x7e))}]' + (f'  -> DM Sans for {"".join(missing)}' if missing and not left else '') + (f'  MISSING {"".join(left)}' if left else ''))
        if left:
            problems.append((first, weight, ''.join(left)))
    print('font check:', 'no system fallback' if not problems else problems)
    await ctx.close()


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        if 'load' in PARTS:
            await load(b)
        if 'fonts' in PARTS:
            await fonts(b)
        await b.close()


asyncio.run(main())
