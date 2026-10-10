"""Compare the lab render's ink with the amended spec/landing.md chapter boxes (ink bounds), section-relative.
Note / headline / name: ink pixels (white or near-black per chapter) inside the box's x range and a +-40 px y window.
Nails: visible nail bounds from the DOM cells. Pill: DOM rect. Prints differences > 5 px."""
import asyncio, pathlib, sys
from PIL import Image
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import landing_fit as F

TB = pathlib.Path(__file__).resolve().parents[1]
Y0 = {'diet-cherry': 1062, 'brainwave': 0, 'green-flag': 850, 'shaadi-shift': 545, 'on-me': 1320, 'wild-card': 0, 'pinky-promise': 850}
SPEC = {  # amended landing.md (col coords): note, head, nails(y only), name(y only), pill
    'diet-cherry':   dict(note=(85, 1117, 295, 1197), head=(65, 1205, 350, 1322), nails=(1342, 1475), name=(1495, 1518), pill=(118, 1528, 278, 1573)),
    'brainwave':     dict(note=(130, 115, 370, 225), head=(60, 245, 365, 350), nails=(375, 505), name=(528, 552), pill=(105, 562, 295, 612)),
    'green-flag':    dict(note=(75, 900, 300, 985), head=(35, 1010, 385, 1110), nails=(1135, 1255), name=(1290, 1315), pill=(105, 1322, 287, 1372)),
    'shaadi-shift':  dict(note=(60, 630, 330, 685), head=(60, 720, 365, 825), nails=(857, 985), name=(1015, 1040), pill=(140, 1052, 322, 1102)),
    'on-me':         dict(note=(100, 1395, 335, 1480), head=(40, 1515, 375, 1585), nails=(1610, 1745), name=(1765, 1795), pill=(120, 1803, 295, 1853)),
    'wild-card':     dict(note=(55, 40, 330, 100), head=(85, 105, 365, 230), nails=(255, 385), name=(435, 462), pill=(145, 470, 320, 522)),
    'pinky-promise': dict(note=(30, 880, 385, 945), head=(70, 930, 360, 1060), nails=(1088, 1215), name=(1236, 1262), pill=(120, 1273, 298, 1321)),
}
DARK = {'on-me', 'wild-card'}


def ink_box(im, x0, x1, y0, y1, dark):
    px = im.load(); w, h = im.size
    xs, ys = [], []
    for y in range(max(0, y0), min(h, y1)):
        for x in range(max(0, x0), min(w, x1)):
            r, g, b = px[x, y]
            hit = (r < 55 and g < 55 and b < 55) if dark else (r > 236 and g > 236 and b > 236)
            if hit:
                xs.append(x); ys.append(y)
    return (min(xs), min(ys), max(xs), max(ys)) if xs else None


RESULTS = {}


def main():
    m = asyncio.run(F.measure())
    worst = []
    for k, sp in SPEC.items():
        y0 = Y0[k]
        im = Image.open(TB / f'lab/shots/{k}-390.png').convert('RGB')
        dark = k in DARK
        rel = lambda b: (b[0], b[1] - y0, b[2], b[3] - y0)
        res = {}
        for el in ('note', 'head'):
            s = rel(sp[el])
            # exclude the other text element's band: note window ends where the headline box starts and vice versa
            if el == 'note':
                win = (s[1] - 30, min(s[3] + 25, rel(sp['head'])[1] + 6))
            else:
                win = (max(s[1] - 25, rel(sp['note'])[3] - 6), s[3] + 30)
            b = ink_box(im, s[0] - 10, s[2] + 10, win[0], win[1], dark)
            res[el] = (s, b)
        sn = (sp['name'][0] - y0, sp['name'][1] - y0)
        pill_top = sp['pill'][1] - y0
        nb = ink_box(im, 120, 270, sn[0] - 12, min(sn[1] + 12, pill_top - 3), dark)
        res['name'] = ((None, sn[0], None, sn[1]), nb)
        cell = m[k]['nails']  # [x0, y0, x1, y1] of the cells
        ch = cell[3] - cell[1]
        vis = (cell[0], round(cell[1] + ch * 10 / 354), cell[2], round(cell[1] + ch * 327 / 354))
        res['nails'] = ((None, sp['nails'][0] - y0, None, sp['nails'][1] - y0), vis)
        res['pill'] = (rel(sp['pill']), tuple(m[k]['pill']))
        line = []
        for el, (s, b) in res.items():
            if not b:
                line.append(f'{el}: no ink'); continue
            dt, db = b[1] - s[1], b[3] - s[3]
            flag = '!' if max(abs(dt), abs(db)) > 5 else ''
            line.append(f'{el}{flag} top {dt:+d} bot {db:+d}')
            if flag:
                worst.append((k, el, s, b))
        print(f'{k:14}', ' | '.join(line))
        RESULTS[k] = res
    print('\n>5 px:')
    for k, el, s, b in worst:
        print(f'  {k} {el}: spec {s} build {b}')




def fit(rounds=2):
    """Move note / headline / nails / name / pill so their ink matches the spec ink boxes."""
    import json, subprocess
    pp = TB / 'lab/params.json'
    for r in range(rounds):
        subprocess.run([sys.executable, '-I', str(TB / 'tools/build_landing.py')], check=True, capture_output=True)
        subprocess.run([sys.executable, '-I', str(TB / 'tools/lab_shots.py'), '390'], check=True, capture_output=True)
        RESULTS.clear(); main()
        P = json.loads(pp.read_text(encoding='utf-8'))
        for k, res in RESULTS.items():
            Q = P[k]
            s, b = res['note']
            if b:
                Q['note_y'] = round(Q['note_y'] + ((s[1] + s[3]) - (b[1] + b[3])) / 2, 1)
            s, b = res['head']
            if b:
                Q['head_y'] = round(Q['head_y'] + (s[1] - b[1]), 1)
                lines = 1 if Q.get('head_lines', 2) == 1 or k == 'on-me' else 2
                if lines == 2:
                    extra = (s[3] - s[1]) - (b[3] - b[1])
                    Q['head_lead'] = round(max(0.8, min(1.15, Q['head_lead'] + extra / Q['head_fs'])), 3)
            s, b = res['nails']
            Q['nails_y'] = round(Q['nails_y'] + ((s[1] + s[3]) - (b[1] + b[3])) / 2, 1)
            s, b = res['name']
            if b:
                Q['name_y'] = round(Q['name_y'] + ((s[1] + s[3]) - (b[1] + b[3])) / 2, 1)
            s, b = res['pill']
            Q['pill_y'] = round(Q['pill_y'] + ((s[1] + s[3]) - (b[1] + b[3])) / 2, 1)
        pp.write_text(json.dumps(P, indent=1), encoding='utf-8')
    subprocess.run([sys.executable, '-I', str(TB / 'tools/build_landing.py')], check=True, capture_output=True)
    subprocess.run([sys.executable, '-I', str(TB / 'tools/lab_shots.py'), '390'], check=True, capture_output=True)
    RESULTS.clear(); main()


if __name__ == '__main__':
    fit(int(sys.argv[1])) if len(sys.argv) > 1 else main()
