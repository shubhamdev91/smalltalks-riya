"""Copy boxes for the desktop right-piece clearance (CHAPTERS-DESKTOP-SPEC §3.2), measured on lab/landing.html.
For each chapter with a right-anchored piece, every copy box (note, headline lines, the nail row, name, pill, caption)
is measured at kc 1.3 (1440x900, the v1.1 cap) and kc 1.0 (1440x580). Its right edge from the copy frame's left (--cxe)
and its bottom from the copy's offset (--dy) are close to linear in kc (board px x kc + fixed px: the name and caption
fonts don't scale): the line through the two gives right = xr*kc + xrp and bottom = yb*kc + ybp, raised by any excess
measured at kc 1.1 (1440x623) and 1.2 (1440x664) so it never under-reaches. Boxes another box beats on both edges at both scales are dropped. Writes lab/desk_boxes.json for build_landing.py. Usage: python -I tools/desk_boxes.py"""
import asyncio, json, pathlib, sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
TB = pathlib.Path(__file__).resolve().parents[1]
URL = (TB / 'lab/landing.html').as_uri()
VIEWS = [(1440, 900), (1440, 580), (1440, 623), (1440, 664)]

MEASURE = """() => {
  const out = {};
  for (const s of document.querySelectorAll('.st-ch[data-land]')) {
    if (!s.querySelector('.st-land__art--r')) continue;
    const r = s.getBoundingClientRect();
    const px = (v) => { const d = document.createElement('div'); d.style.cssText = `position:absolute;width:calc(${v})`; s.appendChild(d); const w = d.getBoundingClientRect().width; d.remove(); return w; };
    const kc = px('var(--kc) * 1000') / 1000, cx = px('var(--cxe)'), dy = px('var(--dy)');
    const B = (e) => { const b = e.getBoundingClientRect(); return b.width && b.height ? [b.right - r.left - cx, b.bottom - r.top - dy] : null; };
    const U = (els) => { const bs = els.map(B).filter(Boolean); return bs.length ? [Math.max(...bs.map(b => b[0])), Math.max(...bs.map(b => b[1]))] : null; };
    const boxes = {};
    const one = (n, e) => { const b = e && B(e); if (b) boxes[n] = b; };
    one('note', s.querySelector('.st-ch__note'));
    [...s.querySelectorAll('.st-ch__headline text')].forEach((e, i) => one('head' + i, e));
    const nails = U([...s.querySelectorAll('.st-ch__nail')]); if (nails) boxes.nails = nails;
    one('name', s.querySelector('.st-ch__name'));
    one('pill', s.querySelector('.st-ch__pill'));
    one('cap', s.querySelector('.st-ch__caption'));
    out[s.dataset.land] = { kc, boxes };
  }
  return out;
}"""


async def main():
    runs = []
    async with async_playwright() as p:
        br = await p.chromium.launch(channel='chrome')
        for w, h in VIEWS:
            pg = await br.new_page(viewport={'width': w, 'height': h})
            await pg.goto(URL, wait_until='load')
            await pg.evaluate('document.fonts.ready')
            await pg.wait_for_timeout(300)
            runs.append(await pg.evaluate(MEASURE))
            await pg.close()
        await br.close()
    a, b, *mids = runs
    res = {}
    for key in a:
        k1, k0 = a[key]['kc'], b[key]['kc']
        assert abs(k1 - 1.3) < 0.01 and abs(k0 - 1.0) < 0.01 and [round(m[key]['kc'], 2) for m in mids] == [1.1, 1.2], (key, k1, k0)
        lin = {}
        for n, (r1, b1) in a[key]['boxes'].items():
            r0, b0 = b[key]['boxes'][n]
            xr = (r1 - r0) / (k1 - k0); yb = (b1 - b0) / (k1 - k0)
            xrp = r1 - xr * k1 + max([0.0] + [m[key]['boxes'][n][0] - (r1 - xr * (k1 - m[key]['kc'])) for m in mids])
            ybp = b1 - yb * k1 + max([0.0] + [m[key]['boxes'][n][1] - (b1 - yb * (k1 - m[key]['kc'])) for m in mids])
            lin[n] = dict(xr=round(xr, 2), xrp=round(xrp, 2), yb=round(yb, 2), ybp=round(ybp, 2))
        at = lambda d, k: (d['xr'] * k + d['xrp'], d['yb'] * k + d['ybp'])
        keep = {}
        for n, d in lin.items():
            beaten = any(m != n and all(at(e, k)[0] >= at(d, k)[0] - 0.01 and at(e, k)[1] >= at(d, k)[1] - 0.01 for k in (1.0, 1.3))
                         and not (n < m and all(abs(at(e, k)[0] - at(d, k)[0]) < 0.01 and abs(at(e, k)[1] - at(d, k)[1]) < 0.01 for k in (1.0, 1.3)))
                         for m, e in lin.items())
            if not beaten:
                keep[n] = d
        res[key] = keep
        print(key, json.dumps(keep))
    (TB / 'lab/desk_boxes.json').write_text(json.dumps(res, indent=1), encoding='utf-8')


asyncio.run(main())
