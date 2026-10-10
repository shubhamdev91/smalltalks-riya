"""Fit the landing chapters to the spec boxes (spec/landing.md, board 3 at 390).
Renders lab/landing.html, measures note / headline / nail row / name / pill per chapter, compares with the spec boxes,
updates lab/params.json (positions in board px, note and headline sizes) and rebuilds. Repeat N rounds.
Usage: python -I tools/landing_fit.py [rounds]"""
import asyncio, json, pathlib, subprocess, sys
from playwright.async_api import async_playwright

TB = pathlib.Path(__file__).resolve().parents[1]
PARAMS = TB / 'lab/params.json'
ROUNDS = int(sys.argv[1]) if len(sys.argv) > 1 else 2

# spec boxes, section-relative (col y - section y0): x0, y0, x1, y1
SPEC = {
    'diet-cherry':   dict(note=(70, 23, 290, 113), head=(60, 108, 360, 238), nails=(22, 248, 368, 378), name=(None, 393, None, 428), pill=(118, 443, 272, 488)),
    'brainwave':     dict(note=(130, 105, 370, 220), head=(60, 235, 365, 345), nails=(22, 365, 368, 500), name=(None, 525, None, 555), pill=(105, 565, 295, 612)),
    'green-flag':    dict(note=(80, 25, 310, 135), head=(40, 140, 385, 275), nails=(22, 285, 368, 400), name=(None, 430, None, 460), pill=(105, 475, 285, 522)),
    'shaadi-shift':  dict(note=(60, 80, 330, 145), head=(60, 160, 365, 285), nails=(22, 315, 368, 440), name=(None, 470, None, 495), pill=(140, 505, 322, 555)),
    'on-me':         dict(note=(100, 60, 335, 160), head=(40, 190, 375, 260), nails=(22, 295, 368, 435), name=(None, 455, None, 480), pill=(120, 490, 295, 540)),
    'wild-card':     dict(note=(55, 40, 330, 100), head=(85, 105, 365, 230), nails=(22, 255, 368, 385), name=(None, 435, None, 462), pill=(145, 470, 320, 522)),
    'pinky-promise': dict(note=(30, 15, 385, 95), head=(70, 85, 360, 205), nails=(22, 240, 368, 360), name=(None, 395, None, 425), pill=(120, 440, 298, 490)),
}

MEASURE = '''(() => { const out = {};
  for (const s of document.querySelectorAll('section.st-ch')) {
    const o = s.querySelector('.st-land__inner').getBoundingClientRect(); const k = o.width / 390;
    const rel = (r) => [ (r.left - o.left) / k, (r.top - o.top) / k, (r.right - o.left) / k, (r.bottom - o.top) / k ].map(v => Math.round(v));
    const range = (el) => { const r = document.createRange(); r.selectNodeContents(el); return r.getBoundingClientRect(); };
    const texts = [...s.querySelectorAll('.st-arc')].map(t => t.getBoundingClientRect());
    const head = texts.reduce((a, r) => ({ left: Math.min(a.left, r.left), top: Math.min(a.top, r.top), right: Math.max(a.right, r.right), bottom: Math.max(a.bottom, r.bottom) }), { left: 1e9, top: 1e9, right: -1e9, bottom: -1e9 });
    const nails = [...s.querySelectorAll('.st-ch__nail')].map(n => n.getBoundingClientRect());
    const nb = { left: nails[0].left, right: nails[nails.length - 1].right, top: nails[0].top, bottom: nails[0].bottom };
    out[s.dataset.land] = { note: rel(range(s.querySelector('.st-ch__note'))), head: rel(head), nails: rel(nb),
      name: rel(range(s.querySelector('.st-ch__name'))), pill: rel(s.querySelector('.st-ch__pill').getBoundingClientRect()) };
  }
  return out; })()'''

# visible nail inside its cell: top 10/354, bottom 327/354
NAIL_TOP, NAIL_BOT = 10 / 354, 327 / 354


async def measure():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        pg = await b.new_page(viewport={'width': 390, 'height': 900})
        await pg.goto((TB / 'lab/landing.html').as_uri())
        await pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager')"); await pg.evaluate('Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; })))'); await pg.evaluate('Promise.all([...document.images].map(i => i.decode().catch(() => 0)))'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(400)
        m = await pg.evaluate(MEASURE)
        await b.close()
        return m


def fit_round(params, m):
    report = []
    for key, sp in SPEC.items():
        P, M = params[key], m[key]
        # note: scale size to the spec width, then move top-left
        sw = sp['note'][2] - sp['note'][0]; mw = M['note'][2] - M['note'][0]
        P['note_fs'] = round(P['note_fs'] * (sw / mw) ** 0.8, 2)
        P['note_y'] = round(P['note_y'] + (sp['note'][1] - M['note'][1]), 1)
        P['note_x'] = round(P['note_x'] + (sp['note'][0] - M['note'][0]), 1)
        # headline: width drives the size (capped), top drives y
        sw = sp['head'][2] - sp['head'][0]; mw = M['head'][2] - M['head'][0]
        P['head_fs'] = round(min(P['head_fs'] * sw / mw, 84), 2)
        P['head_dx'] = round(P.get('head_dx', 0) + ((sp['head'][0] + sp['head'][2]) / 2 - (M['head'][0] + M['head'][2]) / 2), 1)
        # head_y, nails_y, name_y and pill_y follow the board's ink bands (tools/ink_bands.py), not the spec boxes:
        # several spec boxes sit 20-35 px off the board and text bounding boxes include the font's ascent gap.
        P['pill_x'] = sp['pill'][0]
        report.append((key, {k: (M[k], sp[k]) for k in ('note', 'head', 'nails', 'name', 'pill')}))
    return report


def main():
    params = json.loads(PARAMS.read_text(encoding='utf-8'))
    for r in range(ROUNDS + 1):
        subprocess.run([sys.executable, '-I', str(TB / 'tools/build_landing.py')], check=True, capture_output=True)
        m = asyncio.run(measure())
        if r == ROUNDS:
            for key, sp in SPEC.items():
                M = m[key]
                print(key, ' '.join(f"{k}:{M[k]} vs {list(sp[k])}" for k in ('note', 'head', 'nails', 'name', 'pill')))
            break
        fit_round(params, m)
        PARAMS.write_text(json.dumps(params, indent=1), encoding='utf-8')


if __name__ == '__main__':
    main()
