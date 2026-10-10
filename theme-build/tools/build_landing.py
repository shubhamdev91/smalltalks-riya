"""Landing build helper (st-foundation).
1. Writes src/snippets/st-landing-join.liquid from spec/joins.json (top-edge masks, heights, beelines, dash offsets).
2. Writes the generated chapter-position block in src/assets/st-landing.css from lab/params.json (fitted to the
   spec/landing.md boxes by tools/landing_fit.py) and src/snippets/st-landing-map.liquid (headline sizes, nail rows, art).
3. Writes lab/landing.html: the board-3 landing as static markup with the real art and the theme's own CSS.
Usage: python -I tools/build_landing.py   (run from theme-build)"""
import json, math, pathlib, urllib.parse, re
from fontTools.ttLib import TTFont

TB = pathlib.Path(__file__).resolve().parents[1]
RIYA = TB.parent
SPEC = RIYA / 'spec'
ART = RIYA / 'artwork'
J = json.loads((SPEC / 'joins.json').read_text(encoding='utf-8'))
SECTIONS = J['sections']
KEYS = [s['section'] for s in SECTIONS]
PARAMS_PATH = TB / 'lab/params.json'

DEFAULTS = {
    'diet-cherry':   dict(note_x=70, note_y=22, note_w=220, note_rot=-8, note_fs=36, head_y=96, head_fs=76, head_lead=0.92, nails_y=238, name_y=393, pill_x=118, pill_y=443, pill_w=154),
    'brainwave':     dict(note_x=130, note_y=105, note_w=240, note_rot=-8, note_fs=36, head_y=222, head_fs=76, head_lead=0.92, nails_y=357, name_y=525, pill_x=105, pill_y=565, pill_w=190),
    'green-flag':    dict(note_x=80, note_y=25, note_w=230, note_rot=-8, note_fs=36, head_y=128, head_fs=60, head_lead=0.92, nails_y=275, name_y=430, pill_x=105, pill_y=475, pill_w=180),
    'shaadi-shift':  dict(note_x=60, note_y=72, note_w=270, note_rot=-6, note_fs=36, head_y=148, head_fs=76, head_lead=0.92, nails_y=305, name_y=468, pill_x=140, pill_y=505, pill_w=182),
    'on-me':         dict(note_x=100, note_y=60, note_w=235, note_rot=-8, note_fs=36, head_y=178, head_fs=76, head_lead=0.92, nails_y=285, name_y=455, pill_x=120, pill_y=490, pill_w=175,
                          cap_x=50, cap_y=945, cap_w=280, cap_rot=-3, cap_fs=30),
    'wild-card':     dict(note_x=55, note_y=40, note_w=275, note_rot=-8, note_fs=36, head_y=93, head_fs=76, head_lead=0.92, nails_y=245, name_y=435, pill_x=145, pill_y=470, pill_w=175),
    'pinky-promise': dict(note_x=30, note_y=15, note_w=355, note_rot=-6, note_fs=36, head_y=73, head_fs=76, head_lead=0.92, nails_y=230, name_y=395, pill_x=120, pill_y=440, pill_w=178,
                          cap_x=230, cap_y=515, cap_w=155, cap_rot=-12, cap_fs=28),
}
PARAMS = json.loads(PARAMS_PATH.read_text(encoding='utf-8')) if PARAMS_PATH.exists() else DEFAULTS
for k, v in DEFAULTS.items():
    for kk, vv in v.items():
        PARAMS.setdefault(k, {}).setdefault(kk, vv)


def edge_svg(path, ch):
    """Mask image for a section's cap: fill below the edge path inside viewBox 0 0 390 ch."""
    pts = re.findall(r'-?\d+(?:\.\d+)?', path)
    close = f' L0,{ch:g} L390,{ch:g} Z' if float(pts[0]) > 195 else f' L390,{ch:g} L0,{ch:g} Z'
    svg = (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 390 {ch:g}' preserveAspectRatio='none'>"
           f"<path d='{path}{close}'/></svg>")
    return "url('data:image/svg+xml," + urllib.parse.quote(svg, safe=" =/:,.-") + "')"


# Beeline paths that follow the board where joins.json simplified them (st-fable review 1). Same x_in / x_out, so
# the chain still joins; dash offsets downstream are recomputed from the path lengths below.
# STORE-DESKTOP-SPEC v1.1 §1a/§1b (owner 10 Oct): the talks teaser (a slice of the real board) and the Journal teaser
# (half a screen) get new phone heights; their beeline segments are re-routed in the left gutter (x <= 14 board px),
# clear of the text, the board and the cards, entering and leaving at the same x as before (st-chapter.liquid's script
# carries the dash phase across every join).
HEIGHT_OVERRIDES = {'talks-teaser': 670, 'journal-teaser': 378}
_HT, _HJ = HEIGHT_OVERRIDES['talks-teaser'], HEIGHT_OVERRIDES['journal-teaser']
BEELINE_OVERRIDES = {
    'talks-teaser': f'M40,0 C46,20 56,40 50,60 C40,90 12,110 9,150 C7,190 6,220 6,260 L6,{_HT - 110} '
                    f'C6,{_HT - 55} 14,{_HT - 28} 22,{_HT}',
    'journal-teaser': f'M30,0 C24,30 10,50 7,90 L7,{_HJ - 40} C7,{_HJ - 10} 60,{_HJ - 8} 200,{_HJ - 6} '
                      f'C300,{_HJ - 4} 350,{_HJ - 2} 370,{_HJ}',
}
DASH = 9 + 5.5


def path_length(d, steps=64):
    """Length of an SVG path made of M/L/C/S/H/V commands (absolute), sampled."""
    toks = re.findall(r'[MLCSHVZ]|-?\d+(?:\.\d+)?', d)
    i, cur, start, last_c2, total, cmd = 0, (0.0, 0.0), (0.0, 0.0), None, 0.0, None
    def num():
        nonlocal i
        v = float(toks[i]); i += 1; return v
    while i < len(toks):
        if re.match(r'[MLCSHVZ]', toks[i]):
            cmd = toks[i]; i += 1
            if cmd == 'Z':
                total += ((cur[0] - start[0]) ** 2 + (cur[1] - start[1]) ** 2) ** 0.5; cur = start; continue
        if cmd == 'M':
            cur = start = (num(), num()); cmd = 'L'; last_c2 = None
        elif cmd in 'LHV':
            nx = num() if cmd != 'V' else cur[0]
            ny = num() if cmd == 'L' else (cur[1] if cmd == 'H' else nx)
            if cmd == 'V':
                nx, ny = cur[0], nx
            total += ((nx - cur[0]) ** 2 + (ny - cur[1]) ** 2) ** 0.5; cur = (nx, ny); last_c2 = None
        elif cmd in 'CS':
            if cmd == 'C':
                c1 = (num(), num())
            else:
                c1 = (2 * cur[0] - last_c2[0], 2 * cur[1] - last_c2[1]) if last_c2 else cur
            c2 = (num(), num()); end = (num(), num())
            prev = cur
            for k in range(1, steps + 1):
                t = k / steps; u = 1 - t
                x = u**3*cur[0] + 3*u*u*t*c1[0] + 3*u*t*t*c2[0] + t**3*end[0]
                y = u**3*cur[1] + 3*u*u*t*c1[1] + 3*u*t*t*c2[1] + t**3*end[1]
                total += ((x - prev[0]) ** 2 + (y - prev[1]) ** 2) ** 0.5; prev = (x, y)
            cur, last_c2 = end, c2
    return total


def path_points(d, steps=24):
    """Points along an absolute M/L/C path (x,y pairs), sampled."""
    toks = re.findall(r'[MLCZ]|-?\d+(?:\.\d+)?', d)
    i, cur, pts, cmd = 0, (0.0, 0.0), [], None
    def num():
        nonlocal i
        v = float(toks[i]); i += 1; return v
    while i < len(toks):
        if re.match(r'[MLCZ]', toks[i]):
            cmd = toks[i]; i += 1
            if cmd == 'Z':
                continue
        if cmd == 'M':
            cur = (num(), num()); pts.append(cur); cmd = 'L'
        elif cmd == 'L':
            nxt = (num(), num())
            n = max(1, int(((nxt[0] - cur[0]) ** 2 + (nxt[1] - cur[1]) ** 2) ** 0.5 // 4))
            pts += [(cur[0] + (nxt[0] - cur[0]) * k / n, cur[1] + (nxt[1] - cur[1]) * k / n) for k in range(1, n + 1)]
            cur = nxt
        elif cmd == 'C':
            c1, c2, end = (num(), num()), (num(), num()), (num(), num())
            for k in range(1, steps + 1):
                t = k / steps; u = 1 - t
                pts.append((u**3*cur[0] + 3*u*u*t*c1[0] + 3*u*t*t*c2[0] + t**3*end[0], u**3*cur[1] + 3*u*u*t*c1[1] + 3*u*t*t*c2[1] + t**3*end[1]))
            cur = end
    return pts


# ---------------- owner v12.1 beeline (phone): the current route, pulled in and softened ----------------
# x -> 20 + x * 350 / 390 (edges 0 / 390 -> 20 / 370, centre kept); every L segment, and every C whose control points
# lie within 3 px of its chord, longer than 70 becomes n = max(1, round(len / 280)) smooth half-waves of amplitude
# min(11, 0.035 len), alternating sides, endpoints unchanged (st-fable's rebuild(), qa/desktop/owner-v12/beecur.js; the
# live path is rebuilt the same way by sections/st-chapter.liquid's script; this is the no-JS fallback).
_NUM = re.compile(r'-?\d+(?:\.\d+)?')


def _bee_parse(d):
    segs, cur = [], None
    for m in re.finditer(r'([MLC])([^MLC]*)', d):
        n = [float(v) for v in _NUM.findall(m.group(2))]
        if m.group(1) == 'M':
            cur = (n[0], n[1]); segs.append(('M', cur))
        elif m.group(1) == 'L':
            for i in range(0, len(n) - 1, 2):
                q = (n[i], n[i + 1]); segs.append(('L', cur, q)); cur = q
        else:
            for i in range(0, len(n) - 5, 6):
                c1, c2, q = (n[i], n[i + 1]), (n[i + 2], n[i + 3]), (n[i + 4], n[i + 5])
                segs.append(('C', cur, c1, c2, q)); cur = q
    return segs


def _bf(v):
    t = f'{round(v + 0.0, 1):.1f}'.rstrip('0').rstrip('.')
    return '0' if t in ('-0', '') else t


def bee_rebuild(d, mx=lambda x: 20 + x * 350 / 390, my=lambda y: y, unit=1.0):
    out = ''
    for sg in _bee_parse(d):
        if sg[0] == 'M':
            out += f'M{_bf(mx(sg[1][0]))},{_bf(my(sg[1][1]))}'; continue
        a = (mx(sg[1][0]), my(sg[1][1])); q = sg[-1]; q = (mx(q[0]), my(q[1]))
        ln = math.hypot(q[0] - a[0], q[1] - a[1])
        straight = sg[0] == 'L'
        if sg[0] == 'C':
            c1, c2 = (mx(sg[2][0]), my(sg[2][1])), (mx(sg[3][0]), my(sg[3][1]))
            def dch(pt):
                dx, dy = q[0] - a[0], q[1] - a[1]; L = math.hypot(dx, dy) or 1
                return abs((pt[0] - a[0]) * dy - (pt[1] - a[1]) * dx) / L
            straight = ln > 70 * unit and dch(c1) < 3 * unit and dch(c2) < 3 * unit
            if not straight:
                out += f' C{_bf(c1[0])},{_bf(c1[1])} {_bf(c2[0])},{_bf(c2[1])} {_bf(q[0])},{_bf(q[1])}'; continue
        if ln <= 70 * unit:
            out += f' L{_bf(q[0])},{_bf(q[1])}'; continue
        n = max(1, round(ln / (280 * unit)))
        amp = min(11 * unit, ln * 0.035)
        ux, uy = (q[0] - a[0]) / ln, (q[1] - a[1]) / ln
        nx, ny = -uy, ux
        for i in range(n):
            t0, t1, side = i / n, (i + 1) / n, (-1 if i % 2 else 1)
            q0 = (a[0] + (q[0] - a[0]) * t0, a[1] + (q[1] - a[1]) * t0)
            q1 = (a[0] + (q[0] - a[0]) * t1, a[1] + (q[1] - a[1]) * t1)
            k = 0.36 * ln / n
            c1 = (q0[0] + ux * k + nx * amp * side * 1.33, q0[1] + uy * k + ny * amp * side * 1.33)
            c2 = (q1[0] - ux * k + nx * amp * side * 1.33, q1[1] - uy * k + ny * amp * side * 1.33)
            out += f' C{_bf(c1[0])},{_bf(c1[1])} {_bf(c2[0])},{_bf(c2[1])} {_bf(q1[0])},{_bf(q1[1])}'
    return out


def bee_corner(key, d, part=None):
    """Wild Card's cards sit in the phone's top-right corner (v12.1 A3): On Me's join moves in to x 330 (its last run is
    behind the receipt hand) and Wild Card's line swings out to the edge below the cards."""
    if key == 'chapter-on-me' and part in (None, 'bot'):
        d = re.sub(r'386,(-?[\d.]+) L386,(-?[\d.]+)\s*$', r'336,\1 L330,\2', d)
    if key == 'chapter-wild-card':
        if part == 'top':
            d = re.sub(r'^M386,0$', 'M330,0 C330,34 386,58 386,118', d.strip())
        elif part is None:
            d = re.sub(r'^M386,0 L386,', 'M330,0 C330,34 386,58 386,118 L386,', d)
    return d


def join_data():
    out = {}
    for i, s in enumerate(SECTIONS):
        nxt = SECTIONS[i + 1] if i + 1 < len(SECTIONS) else None
        te = s['top_edge']
        ch = float(te.get('curve_height_px') or 0)
        nc = float(nxt['top_edge'].get('curve_height_px') or 0) if nxt else 0.0
        d = {'h': HEIGHT_OVERRIDES.get(s['section'], s['height_px']), 'c': ch, 'nc': nc}
        if te.get('path') and ch > 0:
            d['edge'] = edge_svg(te['path'], ch)
        b = s.get('beeline')
        if b:
            path = BEELINE_OVERRIDES.get(s['section'], b['path'])
            d['bee'] = {'path': path, 'style': b['style'], 'len': path_length(path), 'off': float(b['dashoffset'])}
        out[s['section']] = d
    return out


JD = join_data()


def style_vars(key):
    d = JD[key]
    v = f"--h: {d['h']:g}; --c: {d['c']:g}; --nc: {d['nc']:g};"
    if 'cmin' in d:
        v += f" --cmin: {d['cmin']:g}; --cmin2: {d['cmin2']:g}; --cmax: {d['cmax']:g};"
    if 'edge' in d:
        v += f" --edge: {d['edge']};"
    return v


def beeline(key):
    b = JD[key].get('bee')
    if not b:
        return ''
    cls = 'colour' if b['style'] == 'on_colour' else 'cream'
    sp = b.get('split')
    data = (f' data-top="{bee_corner(key, sp["top"], "top")}" data-x="{sp["x"]}" data-yb="{sp["yb"]}" data-bot="{bee_corner(key, sp["bot"], "bot")}"'
            f' data-head="{sp["head"]}"' if sp else '')
    # d = the phone route as drawn (v12.1, no-JS fallback); data-raw = the untouched route (the laptop line maps it)
    return (f'<svg class="st-land__beeline st-land__beeline--{cls}" viewBox="0 0 390 {JD[key]["h"]:g}" preserveAspectRatio="none"{data} '
            f'aria-hidden="true" focusable="false"><path d="{bee_rebuild(bee_corner(key, b["path"]))}" data-raw="{b["path"]}" '
            f'stroke-dashoffset="{round(b["off"], 2):g}"/></svg>')


def write_join_snippet():
    lines = ['{% doc %}',
             '  Landing joins and beeline per section, generated from spec/joins.json by theme-build/tools/build_landing.py',
             '  (do not hand-edit; re-run the tool when the spec changes).',
             "  part 'style': inline custom properties for .st-land (--h, --c, --nc, --edge).",
             "  part 'beeline': the section's dashed segment (aria-hidden SVG), or nothing.",
             '',
             '  @param {string} key - joins.json section key, e.g. chapter-diet-cherry, talks-teaser.',
             "  @param {string} part - 'style' or 'beeline'.",
             '',
             '  @example',
             "  <section class=\"st-land\" style=\"{% render 'st-landing-join', key: 'tiles', part: 'style' %}\">",
             '{% enddoc %}',
             '{%- case part -%}',
             "  {%- when 'style' -%}",
             '    {%- case key -%}']
    lines += [f"      {{%- when '{k}' -%}}{style_vars(k)}" for k in KEYS]
    lines += ['    {%- endcase -%}', "  {%- when 'beeline' -%}", '    {%- case key -%}']
    lines += [f"      {{%- when '{k}' -%}}{beeline(k)}" for k in KEYS if beeline(k)]
    lines += ['    {%- endcase -%}', '{%- endcase -%}', '']
    (TB / 'src/snippets/st-landing-join.liquid').write_text('\n'.join(lines), encoding='utf-8', newline='\n')


def write_positions_css():
    """One screen per chapter: the text stack (POS, from apply_compact), in board px from the section top."""
    comp = max(max(JD['chapter-' + k]['cmin'] + 20, JD['chapter-' + k]['cmin2']) for k in POS)
    css = ['/* >= 990: the shared section unit (--kt) also follows the height, sized by the tallest chapter minimum. */\n'
           + '.st-land {\n  --st-comp: ' + f'{comp:g}' + ';\n}']
    for key in PARAMS:
        L = POS[key]
        n = _num
        v = [f"--note-cx: {n(L['note_cx'])}; --note-b: {n(L['note_b'])}; --note-rot: {n(L['note_rot'])}deg; --note-fs: {n(L['note_fs'])}; --note-lh: {round(L['note_lh'], 4):g};",
             f"--head-y: {n(L['head_y'])}; --head-dx: {n(L['head_dx'])}; --nails-x: {n(L['nails_x'])}; --nails-y: {n(L['nails_y'])}; --nail-s: {L['nail_s']:g};",
             f"--name-y: {n(L['name_y'])}; --pill-x: {n(L['pill_x'])}; --pill-y: {n(L['pill_y'])}; --pill-w: {n(L['pill_w'])};",
             f"--ctop: {n(L['ctop'])}; --cspan: {n(L['cspan'])};"]
        dsz = [it['dsz'] for it in CHAPTERS[key]['art'] if it.get('dsz')]
        if key in GW_OVERRIDES:
            v.append(f"--gw: {n(GW_OVERRIDES[key])};")
        elif dsz:
            v.append(f"--gw: {n(max(d[1] + d[0] for d in dsz))};")
        cap = L.get('caption')
        if cap:
            vpos = f"--cap-y: {n(cap['cap_y'])};" if 'cap_y' in cap else f"--cap-b: {n(cap['cap_b'])};"
            v.append(f"--cap-x: {n(cap['cap_x'])}; {vpos} --cap-w: {n(cap['cap_w'])}; --cap-rot: {n(cap['cap_rot'])}deg; --cap-fs: {n(cap['cap_fs'])};")
        css.append(f".st-ch[data-land='{key}'] {{\n  " + '\n  '.join(v) + '\n}')
    p = TB / 'src/assets/st-landing.css'
    s = p.read_text(encoding='utf-8')
    a = s.index('/* BEGIN generated chapter positions')
    a = s.index('*/', a) + 3
    b = s.index('/* END generated chapter positions */')
    s = s[:a] + '\n\n'.join(css) + '\n' + s[b:]
    p.write_text(s, encoding='utf-8', newline='\n')


def write_desk_clear_css():
    """>= 1024 (CHAPTERS-DESKTOP-SPEC 3.2): a right-anchored piece keeps 16 px (17 here, for layout rounding) from every copy box, beside it (its left
    edge, 100cqw - rw x kr) or under it (its top, the section box's bottom - rh x kr). Its scale --kr is ka, reduced to
    the largest value that clears each box one way or the other, not below 1.0; if 1.0 still collides with a box it
    can't pass under, the copy moves left by that box's horizontal deficit (--cxs). Copy boxes (right / bottom edges as
    board px x kc + fixed px) come from tools/desk_boxes.py (lab/desk_boxes.json)."""
    src = TB / 'lab/desk_boxes.json'
    boxes = json.loads(src.read_text(encoding='utf-8')) if src.exists() else {}
    n = _num
    css = []
    for ck, bx in boxes.items():
        r = [it for it in CHAPTERS[ck]['art'] if it.get('anchor') == 'r']
        assert len(r) == 1 and r[0].get('bottom') is not None, ck
        it = r[0]
        w, h = DIMS[it['asset']]
        rw = 390 - it['left']
        rh = it['width'] * h / w + it['bottom']
        hsec = '(var(--fitd) + var(--nc) * var(--kt))'
        sh, kr = [], []
        for b in bx.values():
            right = f"({n(b['xr'])} * var(--kc) + {n(b['xrp'] + 17)}px)"
            bottom = f"({n(b['yb'])} * var(--kc) + {n(b['ybp'] + 17)}px)"
            sh.append(f"min(calc(var(--cx0) + {right} + {n(rw)}px - 100cqw), calc(var(--dy) + {bottom} + {n(rh)}px - {hsec}) * 100)")
            kr.append(f"max(calc((100cqw - var(--cxe) - {right}) / {n(rw)}), calc(({hsec} - var(--dy) - {bottom}) / {n(rh)}))")
        css.append(f"  .st-ch[data-land='{ck}'] {{\n    --cxs: max(0px, {', '.join(sh)});\n"
                   f"    --kr: clamp(1px, min({', '.join(kr)}), var(--ka));\n  }}")
    out = '@media screen and (min-width: 1024px) {\n' + '\n\n'.join(css) + '\n}\n' if css else ''
    p = TB / 'src/assets/st-landing.css'
    s = p.read_text(encoding='utf-8')
    a = s.index('/* BEGIN generated desktop clearance')
    a = s.index('*/', a) + 3
    b = s.index('/* END generated desktop clearance */')
    s = s[:a] + out + s[b:]
    p.write_text(s, encoding='utf-8', newline='\n')


# ---------------- headline arc ----------------
FR = TTFont(TB / 'fonts/out/st-fraunces-900.woff2')
FR_CMAP, FR_HM, FR_UPM = FR.getBestCmap(), FR['hmtx'], FR['head'].unitsPerEm
RADIUS, HALF = 420, 235
SAG = RADIUS - (RADIUS ** 2 - HALF ** 2) ** 0.5
# Board-measured headline geometry (landing.md "Measured ink geometry"): arc R 560 by default, 650 for lines wider
# than 300 px, Wild Card straight; whole-block chord tilt per chapter.
TILT = {'diet-cherry': -3, 'brainwave': -3, 'green-flag': -4, 'shaadi-shift': -5, 'on-me': -6, 'wild-card': 0, 'pinky-promise': -2}
STRAIGHT = {'wild-card'}
F7 = TTFont(TB / 'fonts/out/st-fraunces-700.woff2')
F7_CMAP, F7_HM, F7_UPM = F7.getBestCmap(), F7['hmtx'], F7['head'].unitsPerEm


def line_px(text, fs, ls=-0.03, ws=0.18):
    em = sum(F7_HM[F7_CMAP.get(ord(c), F7_CMAP[32])][0] for c in text) / F7_UPM
    return (em + ls * len(text) + ws * text.count(' ')) * fs


def arc_for(key, lines, fs):
    out = []
    for l in lines:
        if key in STRAIGHT:
            out.append((0, 0.0))
        else:
            r = 650 if line_px(l, fs) > 300 else 560
            out.append((r, r - (r * r - HALF * HALF) ** 0.5))
    return out


def split_lines(t):
    words = t.split()
    if len(words) == 1:
        return [t]
    parts = [p.strip() for p in t.replace('. ', '.|').split('|') if p.strip()]
    if len(parts) == 2:
        return parts
    best = None
    for i in range(1, len(words)):
        a, b = ' '.join(words[:i]), ' '.join(words[i:])
        key = (max(len(a), len(b)), len(a))
        if best is None or key < best[0]:
            best = (key, [a, b])
    return best[1]


def headline(text, uid, fs, lead, one_line=False, key=None):
    lines = [text] if one_line else split_lines(text)
    apex0 = fs * 0.8
    paths, texts = [], []
    arcs = arc_for(key, lines, fs)
    for i, l in enumerate(lines):
        y = apex0 + i * fs * lead
        r, sag = arcs[i]
        if r:
            paths.append(f'<path id="{uid}-arc{i}" d="M-40,{y + sag:.1f} A{r},{r} 0 0 1 430,{y + sag:.1f}"/>')
        else:
            paths.append(f'<path id="{uid}-arc{i}" d="M-40,{y:.1f} L430,{y:.1f}"/>')
        texts.append(f'<text class="st-arc" font-size="{fs:.1f}"><textPath href="#{uid}-arc{i}" startOffset="50%" text-anchor="middle">{l}</textPath></text>')
    vh = apex0 + (len(lines) - 1) * fs * lead + fs * 0.45
    return (f'<span class="visually-hidden">{text}</span>'
            f'<svg viewBox="0 0 390 {vh:.0f}" aria-hidden="true" focusable="false"><defs>{"".join(paths)}</defs>'
            f'<g transform="rotate({TILT.get(key, -3)} 195 {vh / 2:.0f})">{"".join(texts)}</g></svg>')


# ---------------- art and content (register text as installed) ----------------
A = lambda p: (ART / p).as_uri()
from PIL import Image as _Img

# theme asset name -> artwork source (byte-identical, see build log)
ASSETS = {
    **{f'st-character-{k}.webp': f'characters/web/{k}.webp' for k in
       ['on-me', 'brainwave', 'diet-cherry', 'green-flag', 'shaadi-shift', 'wild-card', 'pinky-promise']},
    **{f'st-chapter-{k}.webp': f'chapters/web/{k}-fade.webp' for k in
       ['on-me', 'brainwave', 'diet-cherry', 'green-flag', 'shaadi-shift', 'wild-card', 'pinky-promise']},
    'st-diet-can.webp': '_source/desi-diet-can-v1.webp',
    # HD batch "board-corrections-1" (artwork/manifest.json hd.batches): web files, byte-identical, never upscaled.
    'st-hd-on-me-woman.webp': 'hd/characters/on-me-woman.web.webp',
    'st-hd-on-me-receipt-hand.webp': 'hd/props/on-me-receipt-hand.web.webp',
    'st-hd-green-flag-woman.webp': 'hd/characters/green-flag-woman.web.webp',
    'st-hd-green-flag-phone.webp': 'hd/props/green-flag-phone.web.webp',
    'st-hd-green-flag-hand.webp': 'hd/props/green-flag-hand.web.webp',
    'st-hd-shaadi-shift-sweep.webp': 'hd/props/shaadi-shift-sweep.web.webp',
    'st-hd-brainwave-sketchbook.webp': 'hd/props/brainwave-sketchbook.web.webp',
    'st-hd-pinky-promise-scene.webp': 'hd/characters/pinky-promise-scene.web.webp',
    'st-hd-wild-card-woman.webp': 'hd/characters/wild-card-woman.web.webp',
    'st-hd-wild-card-cards-hand.webp': 'hd/props/wild-card-cards-hand.web.webp',
    'st-hd-journal-writing.webp': 'hd/journal/journal-writing.web.webp',
    'st-hd-journal-bag-notebook.webp': 'hd/journal/journal-bag-notebook.web.webp',
    # HD batch 2 ("chatgpt-AB-1")
    'st-hd-brainwave-woman.webp': 'hd/characters/brainwave-woman.web.webp',
    'st-hd-diet-cherry-woman.webp': 'hd/characters/diet-cherry-woman.web.webp',
    'st-hd-diet-cherry-can-hand.webp': 'hd/props/diet-cherry-can-hand.web.webp',
    'st-hd-wild-card-woman-v2.webp': 'hd/characters/wild-card-woman-v2.web.webp',
    'st-hd-wild-card-cards-hand-v2.webp': 'hd/props/wild-card-cards-hand-v2.web.webp',
    'st-hd-our-vision-woman.webp': 'hd/tiles/our-vision-woman.web.webp',
}
DIMS = {a: _Img.open(ART / src).size for a, src in ASSETS.items()}
for _a in ('st-hd-green-flag-woman-hero-v2.webp', 'st-hd-shaadi-shift-woman.webp'):
    DIMS[_a] = _Img.open(TB / 'src/assets' / _a).size
DIMS.setdefault('st-diet-can.webp', _Img.open(TB / 'src/assets/st-diet-can.webp').size)

# the art group's reference width where the spec gives it outright (v12.2 Shaadi: st-fable's 470, not left + width = 464)
GW_OVERRIDES = {'shaadi-shift': 470}


def art(asset, left, top, width, box=None, fade=None, z=None, alt=False, bottom=None, anchor='l', dfade=False, only=None, mirror=False,
        dsz=None, v12r=None):
    """alt=True: this layer carries the chapter's alt (SEO-045…051, from snippets/st-art-alt); every other layer is alt="".
    Two-layer scenes put it on the FIRST layer in the DOM, so each scene is described once."""
    # bottom=N anchors a bottom-cut piece to the SECTION bottom (board px, negative = past the edge, clipped there), so a
    # flat cut edge never floats above the section edge when the section box is taller than the board (cap overlap).
    # Desktop (>= 1024, CHAPTERS-DESKTOP-SPEC): anchor = the section edge its cut edges are on: 'l' left, 'r' right,
    # 'f' free (kept with the left group); dfade = a right-edge fade on the free side; only = 'mob' / 'desk' to show a
    # piece on one side of 1024 only; mirror = flipped (a desktop-only piece that bleeds left).
    # dsz = desktop geometry (v1.1): (width, left, bottom) in reference px of a 600 px screen, or (width, left, 'top', t)
    # for a top-cut piece; the chapter's art group scales by --ua (st-landing.css), --gw = its widest left + width.
    # v12r = owner v1.2 split chapters' right-hand piece (>= 1280, only='wide'): (width, right, bottom) in the art
    # group's reference px, scaled by --uar from the section's right edge (st-landing.css).
    return dict(asset=asset, left=left, top=top, width=width, box=box, fade=fade, z=z, alt=alt, bottom=bottom,
                anchor=anchor, dfade=dfade, only=only, mirror=mirror, dsz=dsz, v12r=v12r)


def cards_html(url):
    """Wild Card (owner v12.1): two small cards, ace of spades and king of hearts (st-artwork's SVGs), tucked half off
    the corner opposite the girl; decorative (the group is aria-hidden, the images alt="")."""
    return ('<div class="st-land__cards" aria-hidden="true">'
            f'<img class="st-land__card-ace" src="{url("st-hd-wild-card-ace.svg")}" width="46" height="64" alt="" loading="lazy" decoding="async">'
            f'<img class="st-land__card-king" src="{url("st-hd-wild-card-king.svg")}" width="46" height="64" alt="" loading="lazy" decoding="async">'
            '</div>')


ALT_TOKEN = '@@ALT@@'
ALT_DESK_TOKEN = '@@ALTD@@'  # alt='desk': a laptop-only layer with its own alt (st-art-alt kind 'chapter-desk')


def art_html(it, url):
    """Art in board px. box=(x0,y0,x1,y1) crops through a wrapper; fade = CSS mask for soft crop edges.
    url(asset) gives the src (file URI in the lab, Liquid asset_url in the theme)."""
    w, h = DIMS[it['asset']]
    alt = ALT_DESK_TOKEN if it.get('alt') == 'desk' else ALT_TOKEN if it.get('alt') else ''
    img_attrs = f'src="{url(it["asset"])}" width="{w}" height="{h}" alt="{alt}" loading="lazy" decoding="async" fetchpriority="low"'
    zs = f'z-index:{it["z"]};' if it.get('z') is not None else ''
    if it['box']:
        x0, y0, x1, y1 = it['box']
        mask = f'-webkit-mask:{it["fade"]};mask:{it["fade"]};' if it['fade'] else ''
        if it['fade'] and it['fade'].count('gradient(') > 1:
            # several feathers must intersect, not add (otherwise one opaque layer cancels the others)
            mask += '-webkit-mask-composite:source-in;mask-composite:intersect;'
        return (f'<div class="st-land__art" style="{zs}left:calc({x0}*var(--k));top:calc({y0}*var(--k));width:calc({x1 - x0}*var(--k));'
                f'height:calc({y1 - y0}*var(--k));overflow:hidden;{mask}">'
                f'<img style="position:absolute;left:calc({it["left"] - x0}*var(--k));top:calc({it["top"] - y0}*var(--k));'
                f'width:calc({it["width"]}*var(--k));height:auto" {img_attrs}></div>')
    vpos = (f'bottom:calc({_num(it["bottom"])}*var(--k))' if it.get('bottom') is not None
            else f'top:calc({_num(it["top"])}*var(--k) + var(--dy, 0px))')
    cls = 'st-land__art st-land__art--' + it.get('anchor', 'l')
    cls += ' st-land__art--dfade' if it.get('dfade') else ''
    cls += f' st-land__art--{it["only"]}' if it.get('only') else ''
    cls += ' st-land__art--mirror' if it.get('mirror') else ''
    rx = f'--rx:{_num(390 - it["left"] - it["width"])};' if it.get('anchor') == 'r' else ''
    d = it.get('dsz')
    if d:
        cls += ' st-land__art--dsz' + (' st-land__art--dtop' if len(d) == 4 else '')
        rx += f'--dw:{_num(d[0])};--dl:{_num(d[1])};' + (f'--dt:{_num(d[3])};' if len(d) == 4 else f'--db:{_num(d[2])};')
    v = it.get('v12r')
    if v:
        cls += ' st-land__art--v12r'
        rx += f'--rw:{_num(v[0])};--rr:{_num(v[1])};--rb:{_num(v[2])};'
    return (f'<div class="{cls}" style="{zs}{rx}left:calc({_num(it["left"])}*var(--k));{vpos};width:calc({_num(it["width"])}*var(--k))">'
            f'<img {img_attrs}></div>')


SOFT = 'linear-gradient(to bottom, transparent 0, #000 22%)'
CHAPTERS = {
    'diet-cherry': dict(note='New plans.\nSame favourite.', head='Haan, wohi wali.', name='Diet Cherry', cols=[1, 0, 2, 1, 1],
                        art=[art('st-hd-diet-cherry-woman.webp', -2, 388, 194.9, alt=True),
                             art('st-hd-diet-cherry-can-hand.webp', 277.3, 460, 120.9)]),
    'brainwave': dict(note='You had the thought.\nYou did the work.', head='Haan, mera idea hai.', name='Brainwave', cols=[1, 2, 0, 1, 0],
                      art=[art('st-hd-brainwave-woman.webp', -2, -2, 164.5, alt=True),
                           art('st-hd-brainwave-sketchbook.webp', 12, 615, 370)]),
    'green-flag': dict(note='Plans fell apart?\nBring yourself.', head='Tum aa jao. Main dekh lungi.', name='Green Flag', cols=[1, 0, 1, 0, 1], ticks='left',
                       # board-corrections-1 (10 Oct): woman (base, SEO-048) < phone (smaller, further left) < hand + receiver
                       # (cut at the woman's transform, so pixel-aligned with her).
                       art=[art('st-hd-green-flag-woman.webp', -7, 427.5, 405, alt=True),
                            art('st-hd-green-flag-phone.webp', -8, 630.8, 200.9),
                            art('st-hd-green-flag-hand.webp', 103.5, 585, 255.5)]),
    'shaadi-shift': dict(note='Her big day. Your cue.', head='Dulhan tu. Duty meri.', name='Shaadi Shift', cols=[2, 1, 0, 1, 2],
                         art=[art('st-hd-shaadi-shift-sweep.webp', 0, None, 398.2, alt=True, bottom=-4.4)]),
    'on-me': dict(note='Good company.\nOne more round.', head='Bill idhar.', name='On Me', one=True, cols=[0, 2, 1, 2, 0], note_ticks=True,
                  caption='Before anyone starts splitting…',
                  art=[art('st-hd-on-me-woman.webp', -6, 450, 364, alt=True),
                       art('st-hd-on-me-receipt-hand.webp', 111, 555, 287.4)]),
    'wild-card': dict(note='Cards down. Smile on.', head='Achha. Tum pehle.', name='Wild Card', cols=[1, 2, 1, 0, 1], note_ticks=True,
                      art=[art('st-hd-wild-card-woman-v2.webp', -8.2, 419.9, 363.3, alt=True),
                           art('st-hd-wild-card-cards-hand-v2.webp', 174.4, None, 217.8, bottom=-8.8)]),
    'pinky-promise': dict(note='Crowded room. Familiar hand.', head='Haath do. Main hoon.', name='Pinky Promise', cols=[0, 0, 0, 0, 0],
                          caption='Same people. Different days. Still us.',
                          art=[art('st-hd-pinky-promise-scene.webp', -8.4, 508, 406.8, alt=True)]),
}
NOTE_TICKS = ('<svg class="st-ch__note-ticks" viewBox="0 0 20 20" aria-hidden="true" focusable="false">'
              '<path d="M3,15 L8,3 M7,17 L18,8 M8,20 L19,19"/></svg>')
TICKS = {
    'left': '<svg class="st-land__ticks" style="left:calc(30*var(--k));top:calc(138*var(--k));width:calc(48*var(--k));height:calc(56*var(--k))" viewBox="0 0 48 56" aria-hidden="true" focusable="false"><path d="M44,6 L26,20 M42,30 L18,30 M44,52 L26,40"/></svg>',
    'onme': ('<svg class="st-land__ticks" style="left:calc(30*var(--k));top:calc(40*var(--k));width:calc(48*var(--k));height:calc(60*var(--k))" viewBox="0 0 48 60" aria-hidden="true" focusable="false"><path d="M6,4 L20,22 M4,34 L24,36 M10,58 L26,46"/></svg>'
             '<svg class="st-land__ticks" style="left:calc(282*var(--k));top:calc(130*var(--k));width:calc(30*var(--k));height:calc(42*var(--k))" viewBox="0 0 30 42" aria-hidden="true" focusable="false"><path d="M4,22 L26,6 M6,34 L28,36"/></svg>'),
    'wild': '<svg class="st-land__ticks" style="left:calc(300*var(--k));top:calc(80*var(--k));width:calc(32*var(--k));height:calc(32*var(--k))" viewBox="0 0 32 32" aria-hidden="true" focusable="false"><path d="M4,18 L26,4 M6,28 L30,26"/></svg>',
}


# ---------------- one screen per chapter (owner design change, 10 Oct 2026; st-fable's rules) ----------------
# qa/fidelity/OWNER-LANDING-CHANGE-1.md. A product chapter is one screen below the sticky header:
#   height = max(100svh - header, content minimum)        (assets/st-landing.css, .st-ch)
# The text stack (campaign body -> slogan -> nails -> name -> pill) is placed from the section top on visible ink gaps
# (GAPS, measured by tools/landing_ink.py); the art is absolute against the section bottom (it never grows the section)
# and may sit behind the nails, name and pill, never behind the slogan. Content minimum: --cmin = the pill's bottom
# (+ 20 px in CSS); --cmin2 = the room the bottom art needs below the nails' top, and the beeline's fixed parts. Each
# chapter's beeline is a top part (follows the stack) + a vertical run + a bottom part (follows the art), assembled for
# the live height by sections/st-chapter.liquid's script, which also carries the dash phase down the page; the path
# generated here (H_REF, stretched) is the no-JS fallback. lab/params.json (the board fit) stays the reference.
# Test heights in board px below the header: 595 (390x664), 612 (430x744), 620 (440x768); 775-786 at full height.
NOTE_SCALE = 0.5
CAP_F = 0.7
NAIL_W, NAIL_H = 77, 77 * 354 / 204
NAIL_S = 0.88          # plates 60.7 px at 390 (st-fable: >= 60), 3 px apart
NAME_FS = 26.13        # clamp(22px, 6.7vw, 29px) at 390
GAPS = {'note_head': 12, 'head_nails': 12, 'nails_name': 10, 'name_pill': 10}
H_REF = 620


# Per-cap overrides (board px): Wild Card's cap is the On Me join; at 10 its curve crosses the receipt hand's wrist just
# below the fold, so On Me's four nails and the slip stay on the screen, clear of the caption, while the wrist's cut
# still sits on the section edge.
CAP_OVERRIDE = {'chapter-wild-card': 10, 'chapter-pinky-promise': 12}  # Pinky: the stack rises for the clasp


def cap_new(c, key=None):
    if key in CAP_OVERRIDE:
        return CAP_OVERRIDE[key]
    return round(c * CAP_F) if c > 20 else c


def _num(v):
    return f'{round(v, 1):g}'


def map_y(path, fn):
    """Apply fn to every y of an absolute M/L/C path written as x,y pairs."""
    return re.sub(r'(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)', lambda m: f'{m.group(1)},{_num(fn(float(m.group(2))))}', path)


def piecewise(anchors):
    pts = sorted(anchors)
    def fn(y):
        for (a0, b0), (a1, b1) in zip(pts, pts[1:]):
            if y <= a1 or (a1, b1) == pts[-1]:
                return b0 + (y - a0) * (b1 - b0) / (a1 - a0) if a1 != a0 else b0
        return y
    return fn


INK_PATH = TB / 'lab/ink.json'
INK = json.loads(INK_PATH.read_text(encoding='utf-8')) if INK_PATH.exists() else None
INK_Y = {'note': 'note_y', 'head': 'head_y', 'nails': 'nails_y', 'name': 'name_y', 'pill': 'pill_y'}


def ink_gap(key, upper, lower):
    """Smallest visible gap between two parts as measured (columns where both have ink; the upper profile widened by
    4 px each way so diagonals count), or None without a measurement."""
    if not INK or key not in INK['ink'] or key not in INK['pos']:
        return None
    I = INK['ink'][key]
    if upper not in I or lower not in I:
        return None
    ub, lt = I[upper]['bot'], I[lower]['top']
    W = len(ub)
    best = None
    for x in range(W):
        if lt[x] is None:
            continue
        near = [ub[j] for j in range(max(0, x - 4), min(W, x + 5)) if ub[j] is not None]
        if near:
            g = lt[x] - max(near)
            best = g if best is None else min(best, g)
    return best


def place(key, upper, lower, L, target):
    """Set position of `lower` so its visible gap below `upper` (already placed in L) is `target`, or None."""
    g = ink_gap(key, upper, lower)
    if g is None:
        return None
    pos = INK['pos'][key]
    du = L[INK_Y[upper]] - pos[INK_Y[upper]]
    return pos[INK_Y[lower]] + target - g + du


def stack(key, o):
    """Text stack in board px from the section top, placed on visible gaps (GAPS) once lab/ink.json exists."""
    P = PARAMS[key]
    lines = 2 if '\n' in CHAPTERS[key]['note'] else 1
    pitch = P.get('note_pitch', 38) * NOTE_SCALE
    note_y = o['note_y']
    s = o.get('nail_s', NAIL_S)
    G = dict(GAPS, **o.get('gaps', {}))
    L = dict(note_y=note_y)
    if 'head_y' in o:
        L['head_y'] = o['head_y']
        g = ink_gap(key, 'note', 'head')
        if g is not None:  # a slogan placed by the art (Brainwave): the note is placed above it
            pos = INK['pos'][key]
            L['note_y'] = note_y = pos['note_y'] + (g - G['note_head']) + (L['head_y'] - pos['head_y'])
    else:
        L['head_y'] = place(key, 'note', 'head', L, G['note_head'])
        if L['head_y'] is None:
            L['head_y'] = note_y + lines * pitch + 12 - 0.08 * P['head_fs']
    L['nails_y'] = place(key, 'head', 'nails', L, G['head_nails'])
    if L['nails_y'] is None:
        L['nails_y'] = L['head_y'] + (P['nails_y'] - P['head_y']) - 4
    L['name_y'] = place(key, 'nails', 'name', L, G['nails_name'])
    if L['name_y'] is None:
        L['name_y'] = L['nails_y'] + NAIL_H * s + 10
    L['pill_y'] = place(key, 'name', 'pill', L, G['name_pill'])
    if L['pill_y'] is None:
        L['pill_y'] = L['name_y'] + NAME_FS * 1.5 + 10
    row = 5 * NAIL_W * s + 4 * (3 - 8 * s)  # cells overlap in their margins; visible plates 3 px apart
    return dict(L, note_fs=P['note_fs'] * NOTE_SCALE, pitch=pitch, note_b=note_y + lines * pitch, note_lh=pitch / (P['note_fs'] * NOTE_SCALE),
                note_cx=195 + P.get('head_dx', 0) + o.get('note_dx', 0), note_rot=o.get('note_rot', P['note_rot']),
                head_dx=P.get('head_dx', 0), nail_s=s, nails_x=195 - row / 2,
                pill_x=o.get('pill_x', P['pill_x']), pill_w=o.get('pill_w', P['pill_w']), pill_b=L['pill_y'] + 46)


# Per chapter (board px): where the note starts, the art (bottom-anchored unless noted: bottom = offset from the section
# bottom, negative = cropped there), captions, and the beeline split of the spec route (old board coordinates): 'top'
# (mapped onto the new stack), the run's x, and 'bot' (from y 'b0' to 'end', mapped relative to the section bottom with
# y-scale 'sb'; 'end_rel' = where its end sits above the bottom).
COMPACT = {
    # board crops at the chapter end: woman 68 px, can-hand 37 px
    'diet-cherry': dict(note_y=26,
                        art=lambda L: [art('st-hd-diet-cherry-woman.webp', -2, None, 194.9, alt=True, bottom=-68, dsz=(480, -2, 0)),
                                       art('st-hd-diet-cherry-can-hand.webp', 277.3, None, 120.9, bottom=-37, anchor='r'),
                                       art('st-diet-can.webp', 277.3, None, 120.9, bottom=-37, only='wide', v12r=(470, -6, -40))],
                        bee=dict(top='M388,0 C372,24 356,46 356,52 C356,58 380,60 383,62', x=383,
                                 bot='C383,560 300,575 200,585 C110,595 60,605 40,638', b0=520, end=638)),
    # the woman stays top-left at 0.82 (the slogan over her chin, the note beside her glasses); the sketchbook (0.82,
    # centred as before, board crop 35 -> 29) at the bottom
    'brainwave': dict(note_y=118, head_y=172, note_dx=12,
                      art=lambda L: [art('st-hd-brainwave-woman.webp', -2, -2, 164.5 * 0.82, alt=True, dsz=(300, -2, 'top', -2)),
                                     art('st-hd-brainwave-sketchbook.webp', 197 - 185 * 0.82, None, 370 * 0.82, bottom=-29, anchor='f',
                                         dsz=(468, 240, -46))],
                      # the sweep under the pill is drawn at about half its board depth (10-30 px below the pill), so the
                      # chapter still fits 390x664 with Brainwave's lower stack
                      bee=dict(top='M22,0 C22,60 30,140 34,200 C38,260 26,310 10,340 C5,360 5,430 5,500 C5,560 40,610 90,630 '
                                   'C160,655 280,640 340,665 C372,680 386,692 386,700', x=386, below=[(615, 16), (700, 56)])),
    # woman, phone and hand keep their offsets (pixel-aligned): the group's bottom 130 px are cropped (board: 68), so
    # at 390x664 her hair starts behind the nail row and her face sits below the pill; the phone's base is at the edge
    'green-flag': dict(note_y=26, ticks_dy=-32,
                       # desktop: the hero-v2 woman (receiver and arm, no phone body), mirrored like hero v3.8 so she bleeds
                       # left; the landing woman, phone and hand cut on opposite sides, so they stay phone-only
                       art=lambda L: [art('st-hd-green-flag-woman.webp', -7, None, 405, alt=True, bottom=-130, only='mob'),
                                      art('st-hd-green-flag-phone.webp', -8, None, 200.9, bottom=0, only='mob'),
                                      art('st-hd-green-flag-hand.webp', 103.5, None, 255.5, bottom=-130, only='mob'),
                                      art('st-hd-green-flag-woman-hero-v2.webp', -4, None, 400, alt=True, bottom=0, only='desk', mirror=True)],
                       bee=dict(top='M386,0 C300,12 120,8 60,18 C28,28 10,60 8,110 L8,410 C8,450 30,470 60,482 C92,494 96,530 62,560 '
                                    'C30,600 30,640 30,680', x=30)),
    # v12.2 (owner's full-face portrait, st-fable): phones keep the sweep; from 1024 the portrait, mirrored onto the right
    # edge by the v12 RIGHT layout, with its own alt (SEO-111, st-art-alt kind 'chapter-desk'; SEO-049 is the sweep's)
    'shaadi-shift': dict(note_y=26, art=lambda L: [art('st-hd-shaadi-shift-sweep.webp', 0, None, 398.2, alt=True, bottom=-4.4, only='mob'),
                                                   art('st-hd-shaadi-shift-woman.webp', 0, None, 398.2, alt='desk', bottom=-4.4, only='desk', dsz=(470, -6, -60))],
                         bee=dict(top='M30,0 C20,80 12,200 10,300 L8,440 C8,500 30,570 120,580 C220,585 300,600 360,640 '
                                      'C385,660 386,690 386,710', x=386)),
    # option D (accepted by st-fable): one balanced row under the centred name: the pill (18-178, 44 px target, 12 px
    # clear of the beeline) and the caption ("Before anyone starts splitting…", Caveat 30, 2 lines, its longest line
    # ending at ~372 = the pill's 18 mirrored) on one centre line, >= 16 px apart, on plain ground only; the name
    # >= 10 px above the row (16 on the ink). The caption is set at clamp(22px, 6.4vw, 28px) (st-fable), right-aligned
    # so its right ink edge sits at ~372 (= the pill's 18 mirrored) at any size, centred on the pill's line (CSS: On Me).
    # The woman stays at 0.62; the receipt hand at 0.47 (its four nails run to 89 % of its height), raised so all four
    # nails and the "On me. xx" slip are on the screen, >= 8 below the caption, with the wrist cut under the join curve.
    'on-me': dict(note_y=28, pill_x=18, pill_w=160, gaps={'name_pill': 16},
                  art=lambda L: [art('st-hd-on-me-woman.webp', -6, None, 364 * 0.62, alt=True, bottom=0, dsz=(500, -6, -40)),
                                 art('st-hd-on-me-receipt-hand.webp', 398.4 - 287.4 * 0.47, None, 287.4 * 0.47, bottom=-5.7, anchor='r'),
                                 art('st-hd-on-me-receipt-hand.webp', 398.4 - 287.4 * 0.47, None, 287.4 * 0.47, bottom=-5.7, only='wide',
                                     v12r=(330, -10, -8))],
                  caption=lambda L: dict(cap_x=209, cap_y=L['pill_y'] + 23, cap_w=160, cap_rot=-3, cap_fs=25),  # box ends at 369: Caveat's ink overhangs ~3
                  cap_clear=['st-hd-on-me-receipt-hand.webp'],
                  bee=dict(top='M386,0 C330,14 140,4 60,14 C22,14 12,24 10,50 C9,120 8,180 8,230 L4,430', x=4,
                           bot='C4,560 24,700 54,800 C120,880 300,890 386,900 L386,1067', b0=430, end=1067, sb=0.36)),
    # the woman's bottom 180 px are cropped so her face stays below the pill at 390x664; the cards hand as on the board.
    # The art hangs from the section box, which runs Pinky's cap (12, was 36) below the chapter: -24 keeps it where it was.
    'wild-card': dict(note_y=40,
                      art=lambda L: [art('st-hd-wild-card-woman-v2.webp', -8.2, None, 363.3, alt=True, bottom=-204, dsz=(588, -8, -176)),
                                     art('st-hd-wild-card-cards-hand-v2.webp', 174.4, None, 217.8, bottom=-32.8, anchor='f',
                                         dsz=(372, 300, -22))],
                      bee=dict(top='M386,0', x=386, bot='C386,600 300,640 200,700 C100,760 20,780 14,850', b0=540, end=850, sb=0.55)),
    # On Me's closing row (st-fable): the pill left (18-178), the caption ("Same people. / Different / days. Still
    # us.", -12°, board size) to its right on the pill's centre line, >= 24 px apart, right ink <= W - 17; the name
    # centred above. The scene keeps its full width (its art bleeds off both edges) and hangs so her eyes (108 board px
    # below its top) sit 8 px under the pill at 390x664; the clasp below the caption; the beeline ends in the scene
    # where it did on the board (132 px below its top).
    # The scene hangs from the bottom with its lowest nail 6 px above the fold (the whole clasp in view at every height);
    # eye_clear keeps her eye line >= 8 px under the left-hand pill, which makes Pinky ~28 px taller than one screen at
    # 390x664 (+7 at 430x744, +2 at 440x768): st-fable to choose between that and the eyes behind the pill there.
    'pinky-promise': dict(note_y=24, pill_x=18, pill_w=160, gaps={'note_head': 10, 'head_nails': 10, 'name_pill': 28}, eye_clear=108,
                          clasp_top=166.5,  # board px below the scene's top; the composed maximum keeps it <= 48 under the caption
                          art=lambda L: [art('st-hd-pinky-promise-scene.webp', -8.4, None, 406.8, alt=True, bottom=-36, dfade=True, dsz=(708, -8, -50))],
                          caption=lambda L: dict(cap_x=207, cap_y=L['pill_y'] + 23, cap_w=150, cap_rot=-12, cap_fs=28),
                          # down the left edge (12 px clear of the pill), past the pill's bottom, then into the scene,
                          # ending at her shoulder (190 px below the scene's top, inside the art)
                          bee=dict(top='M6,0', x=6, bot_fn=lambda L: (lambda e: (f'C6,{e - 40:.1f} 40,{e - 18:.1f} 100,{e - 10:.1f} '
                                                                                 f'C150,{e - 4:.1f} 185,{e - 2:.1f} 200,{e:.1f}', e - 80))(L['pill_b'] - 695 + 190))),
}
POS = {}
CLEAR = 10  # board px; >= 8 css px down to 320 wide (k 0.82)


def stack_boxes(key, L):
    """Ink boxes (l, t, r, b) of the stack's parts at their new places, from lab/ink.json (measured at 390, k = 1)."""
    if not INK or key not in INK['ink'] or key not in INK['pos']:
        return {}
    I, pos, out = INK['ink'][key], INK['pos'][key], {}
    for part, ykey in INK_Y.items():
        if part in I and ykey in pos:
            t, b, l, r = I[part]['box']
            dy = L[ykey] - pos[ykey]
            out[part] = (l, t + dy, r, b + dy)  # (the pill's 44 px minimum below ~373 wide: added in CSS, --hc)
    return out


def box_dist(p, bx):
    x, y = p
    l, t, r, b = bx
    return (max(l - x, 0, x - r) ** 2 + max(t - y, 0, y - b) ** 2) ** 0.5


def caption_box(key, L, H):
    """The caption's ink box at chapter height H: top-anchored ones follow the pill, bottom-anchored ones the bottom."""
    if not INK or 'cap' not in INK['ink'].get(key, {}) or not L.get('caption'):
        return None
    t, b, l, r = INK['ink'][key]['cap']['box']
    pos = INK['pos'][key]
    cap = L['caption']
    if 'cap_y' in cap and 'cap_y' in pos:
        dy = cap['cap_y'] - pos['cap_y']
        return (l, t + dy, r, b + dy)
    if 'cap_b' in cap and 'cap_b' in pos and 'hc' in pos:
        # measured with the chapter pos['hc'] tall and the caption pos['cap_b'] above its bottom
        dy = (H - cap['cap_b']) - (pos['hc'] - pos['cap_b'])
        return (l, t + dy, r, b + dy)
    return None


def min_height(key, L, top, x, yb, bot, base):
    """Smallest chapter height (board px, >= base) at which the beeline's moving parts (the vertical run and the
    bottom part) and a bottom-anchored caption keep CLEAR from every glyph box of the stack."""
    boxes = stack_boxes(key, L)
    if not boxes:
        return base
    cb0 = caption_box(key, L, 0)
    if cb0 and 'cap_y' in (L.get('caption') or {}):
        boxes = dict(boxes, cap=(cb0[0] - 6, cb0[1] - 14, cb0[2] + 6, cb0[3] + 6))
    ya = float(re.findall(r'-?\d+(?:\.\d+)?', top)[-1])
    end = re.findall(r'-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?', top)[-1]
    H = base
    while H < 1400:
        moving = path_points(f"M{end} L{x},{H + yb}" + (f" {map_y(bot, lambda y: y + H)}" if bot else ''))
        cb = caption_box(key, L, H)
        if cb:  # the rotated caption's element box runs beyond its ink (~6 px at the sides, ~14 at the top for -12°)
            cb = (cb[0] - 6, cb[1] - 14, cb[2] + 6, cb[3] + 6)
        ok = all(box_dist(pt, bx) >= CLEAR for pt in moving for bx in boxes.values())
        if ok and cb and 'cap_b' in L['caption']:
            ok = all(box_dist(c, bx) >= CLEAR for bx in (boxes.get('pill'), boxes.get('name')) if bx
                     for c in ((cb[0], cb[1]), (cb[2], cb[1]), (cb[0], cb[3]), (cb[2], cb[3]))) and not any(
                     cb[0] < bx[2] and bx[0] < cb[2] and cb[1] < bx[3] and bx[1] < cb[3] for bx in boxes.values())
        if ok:
            return H
        H += 2
    return H


def art_visible(it, nc=0.0):
    """Board px a bottom-anchored art piece reaches above the chapter's own end. It hangs from the section box, which
    runs nc further down (the next section's cap overlaps it there), so that much less shows above the end."""
    if it.get('bottom') is None:
        return 0
    w, h = DIMS[it['asset']]
    return it['width'] * h / w + it['bottom'] - nc


def apply_compact():
    """Chapter layout (POS for the CSS block, CHAPTERS art / ticks / beeline parts) and joins (JD) for one screen."""
    chain = 0.0
    for i, s in enumerate(SECTIONS):
        key = s['section']
        d = JD[key]
        te = s['top_edge']
        c_old = float(te.get('curve_height_px') or 0)
        c = cap_new(c_old, key)
        nxt = SECTIONS[i + 1] if i + 1 < len(SECTIONS) else None
        nc = cap_new(float(nxt['top_edge'].get('curve_height_px') or 0), nxt['section']) if nxt else 0.0
        if te.get('path') and c_old > 0:
            d['edge'] = edge_svg(map_y(te['path'], lambda y: y * c / c_old), c)
        d['c'], d['nc'] = c, nc
        ck = key.replace('chapter-', '')
        if key.startswith('chapter-') and ck in COMPACT:
            o = COMPACT[ck]
            L = stack(ck, o)
            P = PARAMS[ck]
            CHAPTERS[ck]['art'] = arts = o['art'](L)
            if o.get('ticks_dy') is not None and CHAPTERS[ck].get('ticks') == 'left':
                CHAPTERS[ck]['ticks_html'] = TICKS['left'].replace('top:calc(138*var(--k))', f"top:calc({_num(L['head_y'] + o['ticks_dy'])}*var(--k) + var(--dy, 0px))")
            B = o['bee']
            below = [(y_old, L['pill_b'] + dy) for y_old, dy in B.get('below', [])]
            fn = piecewise([(0, 0), (c_old, c), (P['note_y'], L['note_y']), (P['pill_y'] + 46, L['pill_b'])] + below + [(P['pill_y'] + 1046, L['pill_b'] + 1000)])
            top = map_y(B['top'], fn)
            ya = float(re.findall(r'-?\d+(?:\.\d+)?', top)[-1])
            if B.get('bot_fn'):
                bot, yb = B['bot_fn'](L)
            elif B.get('bot'):
                sb, end, rel = B.get('sb', 1), B['end'], B.get('end_rel', 0)
                bfn = lambda y: (y - end) * sb + rel
                bot = map_y(B['bot'], bfn)
                yb = bfn(B['b0'])
            else:
                bot, yb = '', 0.0
            L['caption'] = o['caption'](L) if 'caption' in o else None
            cmin2 = max([L['nails_y'] + art_visible(it, nc) for it in arts if it.get('only') not in ('desk', 'wide')] + [ya - yb + 10])
            if o.get('eye_clear'):
                sc = arts[0]; w_, h_ = DIMS[sc['asset']]; hs = sc['width'] * h_ / w_
                cmin2 = max(cmin2, L['pill_b'] + 8 - o['eye_clear'] - nc + sc['bottom'] + hs)
            cb = caption_box(ck, L, 0)
            if cb and 'cap_y' in L['caption']:
                cmin2 = max([cmin2] + [cb[3] + 8 + art_visible(it, nc) for it in arts if it['asset'] in o.get('cap_clear', [])])
            cmin2 = min_height(ck, L, top, B['x'], yb, bot, round(cmin2))
            L.update(c=c, cmin=L['pill_b'], cmin2=cmin2, bee_top=top, bee_x=B['x'], bee_yb=yb, bee_bot=bot)
            bx = stack_boxes(ck, L)
            ctop = bx['note'][1] if 'note' in bx else L['note_y']
            cbot = L['pill_b']
            cbx2 = caption_box(ck, L, 0)
            if cbx2 and 'cap_y' in (L.get('caption') or {}):
                cbot = max(cbot, cbx2[3])
            L.update(ctop=ctop, cspan=cbot - ctop)
            POS[ck] = L
            h_ref = max(H_REF, L['pill_b'] + 20, cmin2)
            static = f"{top} L{B['x']},{_num(h_ref + yb)}" + (f" {map_y(bot, lambda y: y + h_ref)}" if bot else '')
            d['bee']['path'] = static
            d['bee']['split'] = dict(top=top, x=B['x'], yb=_num(yb), bot=bot, head=_num(L['head_y']))
            d['h'] = round(h_ref, 1)
            d['cmin'], d['cmin2'] = round(L['pill_b'], 1), round(cmin2, 1)
            # composed maximum (st-fable, tall screens): the height at which the highest bottom-anchored art piece's top
            # sits 24 px under the pill, so the pill -> art gap never opens past 48 px; the chapter stops growing there
            reach = max([art_visible(it, nc) for it in arts if it.get('bottom') is not None and it.get('only') not in ('desk', 'wide')] or [0])
            d['cmax'] = round(L['pill_b'] + 24 + reach, 1)
            cbx = caption_box(ck, L, 0)
            if o.get('clasp_top') is not None and cbx:
                # Pinky: the subject is the clasp, under the caption: stop where the clasp's top sits 48 px under the
                # caption's ink (scene top = H - art_visible)
                sc = arts[0]
                d['cmax'] = round(max(cmin2, cbx[3] + 41 - o['clasp_top'] + art_visible(sc, nc)), 1)  # 41 board = <= 48 css px up to 440 wide
            L['cmax'] = d['cmax']
        if 'bee' in d:
            d['bee']['len'] = path_length(d['bee']['path'])
            d['bee']['off'] = -(chain % DASH) if chain % DASH else 0.0
            chain += d['bee']['len']


def write_map_snippet():
    """Per-set landing data for sections/st-chapter.liquid (generated; do not hand-edit)."""
    L = ['{% doc %}',
         '  Landing chapter data per campaign (board 3), generated by theme-build/tools/build_landing.py from lab/params.json and',
         '  the art table there (do not hand-edit). Positions of the text live in assets/st-landing.css (generated block).',
         "  - 'head': headline font size and line pitch in board px, then the line count (1 = keep on one line).",
         "  - 'row': sprite columns for the five-nail row.",
         "  - 'note_lines': 2 = break the note after its first sentence, 1 = one line.",
         "  - 'art': the set's character / prop art (decorative), positioned in board px.",
         "  - 'ticks': sparkle ticks, if the board draws them.",
         "  - 'arc': per headline line 'radius,sagitta' (radius 0 = straight), then the block tilt in degrees.",
         '',
         '  @param {string} key - Campaign handle.',
         "  @param {string} field - 'head', 'row', 'note_lines', 'art', 'ticks' or 'collage' (the tiles' nail scatter; key unused).",
         '',
         '  @example',
         "  {% render 'st-landing-map', key: 'on-me', field: 'art' %}",
         '{% enddoc %}',
         '{%- case field -%}']
    url = lambda a: "{{ '" + a + "' | asset_url }}"
    for field in ('head', 'row', 'note_lines', 'art', 'ticks', 'note_ticks', 'arc'):
        L.append(f"  {{%- when '{field}' -%}}")
        L.append('    {%- case key -%}')
        for k, c in CHAPTERS.items():
            P = PARAMS[k]
            if field == 'head':
                v = f"{P['head_fs']:g},{P['head_lead']:g},{1 if c.get('one') else 2}"
            elif field == 'row':
                v = ','.join(str(n) for n in c['cols'])
            elif field == 'note_lines':
                v = '2' if '\n' in c['note'] else '1'
            elif field == 'art':
                v = ''.join(art_html(it, url) for it in c['art'])
                if ALT_TOKEN in v:
                    v = ("{%- capture st_alt -%}{% render 'st-art-alt', key: '" + k + "', kind: 'chapter' %}{%- endcapture -%}"
                         + v.replace(ALT_TOKEN, '{{ st_alt | strip | escape }}'))
                if ALT_DESK_TOKEN in v:
                    v = ("{%- capture st_alt_desk -%}{% render 'st-art-alt', key: '" + k + "', kind: 'chapter-desk' %}{%- endcapture -%}"
                         + v.replace(ALT_DESK_TOKEN, '{{ st_alt_desk | strip | escape }}'))
                if c.get('art_note'):
                    v = '{% comment %}' + c['art_note'] + '{% endcomment %}' + v
                if k == 'wild-card':
                    v += cards_html(url)
            elif field == 'note_ticks':
                v = NOTE_TICKS if c.get('note_ticks') else ''
            elif field == 'arc':
                lines = [c['head']] if c.get('one') else split_lines(c['head'])
                arcs = arc_for(k, lines, P['head_fs'])
                arcs += [arcs[-1]] * (2 - len(arcs))
                v = ','.join(f'{r},{sg:.1f}' for r, sg in arcs[:2]) + f",{TILT.get(k, -3)}"
            else:
                v = c.get('ticks_html') or TICKS.get(c.get('ticks'), '')
            if v:
                L.append(f"      {{%- when '{k}' -%}}{v}")
        L.append('    {%- endcase -%}')
    collage = ''.join(
        f'<span class="st-tiles__nail" style="left:calc({x}*var(--k));top:calc({y}*var(--k));rotate:{r}deg;'
        f"--st-nails-src:url('{url('st-hd-nails-' + k + '.webp')}');--col:{c}\"></span>"
        for k, c, x, y, r in COLLAGE)
    L += ["  {%- when 'collage' -%}" + collage]
    # (The talks-teaser avatar face crop moved to snippets/st-peek-map, tools/build_peeks.py: HD characters.)
    L += ['{%- endcase -%}', '']
    (TB / 'src/snippets/st-landing-map.liquid').write_text('\n'.join(L), encoding='utf-8', newline='\n')


# ---------------- cream sections (lab markup = the Liquid sections' markup) ----------------
ASSETS.update({f'st-nails-{k}.webp': f'nails/web/{k}.webp' for k in
               ['on-me', 'brainwave', 'diet-cherry', 'green-flag', 'shaadi-shift', 'wild-card', 'pinky-promise']})
ASSETS['st-nail-guide.webp'] = 'guide/web/nail-guide.webp'
DIMS.update({a: _Img.open(ART / ASSETS[a]).size for a in ASSETS if a not in DIMS})
U = lambda a: A(ASSETS[a])

# Tiles collage: one nail per set (signature column), scattered and rotated, in the right card (180x260 board px).
COLLAGE = [(k, c, round(cx - 29), round(cy - 50), r) for k, c, cx, cy, r in [
    ('on-me', 0, 59, 63, -50), ('diet-cherry', 2, 123, 56, -40), ('on-me', 2, 43, 119, -55),
    ('green-flag', 1, 120, 133, -35), ('wild-card', 1, 128, 152, -35), ('wild-card', 0, 162, 117, 25),
    ('brainwave', 0, 30, 191, 35), ('pinky-promise', 0, 98, 176, -25), ('shaadi-shift', 1, 82, 219, -35),
    ('on-me', 2, 148, 222, -40)]]  # board 3 tile: tortoise, checks, lime, cobalt, red-tip ... all seven sets


def box(x, y, w, extra=''):
    return f'style="--x:{x};--y:{y};--w:{w};{extra}"'


def tiles_html(url):
    """The gallery as sections/st-gallery.liquid renders it (index.json labels and alt), the collage in its loaded state."""
    nails = ''.join(
        f'<span class="st-tiles__nail" style="left:calc({x}*var(--k));top:calc({y}*var(--k));rotate:{r}deg;'
        f"--st-nails-src:url('{url('st-hd-nails-' + k + '.webp')}');--col:{c}\"></span>"
        for k, c, x, y, r in COLLAGE)
    return f'''
    <a class="st-tiles__tile" href="#" style="--x: 10; --y: 16; --w: 183;">
      <span class="st-land__card" style="--w: 183; --hh: 263; --card-bg: #f8e6cb;">
        <img src="{url('st-hd-our-vision-woman.webp')}" width="549" height="789" alt="Illustration: a woman with a bindi resting her hand on her cheek, nails burgundy and gold." decoding="async" style="left: 0; top: 0; width: 100%; height: 100%; object-fit: cover;">
      </span>
      <span class="st-tiles__label">Our Vision <span class="st-arrow" aria-hidden="true">↗</span></span>
    </a>
    <a class="st-tiles__tile" href="#" style="--x: 205; --y: 18; --w: 180;">
      <span class="st-land__card st-tiles__collage is-ready" style="--w: 180; --hh: 260; --card-bg: #f5e9da;" aria-hidden="true">{nails}</span>
      <span class="st-tiles__label">Shop all nails <span class="st-arrow" aria-hidden="true">↗</span></span>
    </a>'''



# Real talk_topic 'all' threads (Admin read, 10 Oct): the lab renders what sections/st-teaser.liquid renders from them.
LAB_THREADS = [
    ('green-flag', 'What is your smallest friendship green flag?', 'Mine remembers the stories I never finished.', '2026-10-09T09:40:00+00:00'),
    ('shaadi-shift', 'Same outfit, different confidence.', 'What changed for you?', '2026-10-09T09:35:00+00:00'),
    ('pinky-promise', 'The compliment that stayed with you.', 'Still thinking about it.', '2026-10-09T09:30:00+00:00'),
]
LAB_TOPICS = ['Plot twists', 'Tiny wins', 'Nail talk']


def _asset(url, name):
    return url(name) if name in ASSETS else (TB / 'src/assets' / name).as_uri()


def talks_html(url):
    """sections/st-teaser.liquid, kind talks (v1.1 §1a), posting off: no "be the first", the pre-launch line shows."""
    chips = ''.join(f'<li><a class="st-tt__chip" href="#">{t}</a></li>' for t in LAB_TOPICS)
    rows = ''
    for i, (setk, title, body, at) in enumerate(LAB_THREADS):
        rows += (f'<li class="st-tt__row{" st-tt__row--desk" if i >= 2 else ""}"><a class="st-tt__link" href="#" aria-label="{title}, 0 replies">'
                 f'<span class="st-tavatar" style="--st-nails: url(\'{_asset(url, "st-nails-" + setk + ".webp")}\')" aria-hidden="true"><span class="st-tavatar__nail"></span></span>'
                 f'<span class="st-tt__text"><span class="st-tt__meta"><b>small talk</b> · <time class="st-ago" datetime="{at}">9 Oct</time></span>'
                 f'<span class="st-tt__title">{title}</span><span class="st-tt__ex">{body}</span></span>'
                 f'<span class="st-tt__reply">No replies yet</span></a></li>')
    return f'''
    <div class="st-tt">
      <h2 class="st-tt__h">the talks</h2>
      <p class="st-tt__hl">a little less filtered.</p>
      <p class="st-tt__sup">real talk on friendship, plans, overthinking and everything in between.</p>
      <div class="st-tt__board">
        <nav class="st-tt__chips" aria-label="Topics"><ul role="list">{chips}</ul></nav>
        <p class="st-tt__label">latest talks</p>
        <ol class="st-tt__rows" role="list">{rows}</ol>
      </div>
      <p class="st-tt__pre">Posting isn’t open yet. Read along for now.</p>
      <a class="st-tt__cta" href="#" aria-label="spill your tea on the talks">spill your tea <span class="st-arrow" aria-hidden="true">↗</span></a>
    </div>'''


def journal_html(url):
    """sections/st-teaser.liquid, kind journal (v1.1 §1b)."""
    return f'''
    <div class="st-jt">
      <h2 class="st-jt__h">Small stories.<br>Big feelings.</h2>
      <div class="st-jt__cards">
        <div class="st-jt__card st-jt__card--1"><img src="{_asset(url, 'st-hd-journal-writing.webp')}" width="526" height="607" alt="" loading="lazy" decoding="async"></div>
        <div class="st-jt__card st-jt__card--2"><img src="{_asset(url, 'st-hd-journal-bag-notebook.webp')}" width="526" height="607" alt="" loading="lazy" decoding="async"></div>
      </div>
      <a class="st-jt__pill" href="#">From the Journal <span class="st-arrow" aria-hidden="true">↗</span></a>
      <p class="st-jt__note">For the plans still taking shape…</p>
    </div>'''


def guide_html(url):
    w, h = DIMS['st-nail-guide.webp']
    return f'''
    <p class="st-land__box st-guide__eyebrow" {box(40, 43, 200)}>Nail Guide</p>
    <h2 class="st-land__box st-guide__heading" {box(40, 78, 340)}>Find your fit.</h2>
    <p class="st-land__box st-land__hand" {box(30, 170, 210, '--fs:30;--rot:-12deg')}>A little help, at your fingertips.</p>
    <div class="st-land__art" style="left:calc(67*var(--k));top:calc(10*var(--k));width:calc(400*var(--k))"><img src="{url('st-nail-guide.webp')}" width="{w}" height="{h}" alt="Illustration: a fingertip with a bare natural nail and a measuring tape wrapped across it." loading="lazy" decoding="async"></div>
    <a class="st-land__pill st-land__pill--filled" href="#" style="--x:45;--y:460;--w:305;--ph:58;--pill-bg:#c3021d">Open the guide <span class="st-arrow" aria-hidden="true">↗</span></a>'''


def faq_html(url):
    rows = [('How do I find my size?', 'Every kit has all 12 sizes, so there’s nothing to pick at checkout.'),
            ('How do I apply and remove?', 'Prep your nails, then press on with glue or tabs.'),
            ('What comes in the box?', '24 almond press-ons in 12 sizes, nail glue, adhesive tabs, a mini file and more.')]
    items = ''.join(f'<details class="st-faq2__item"><summary class="st-faq2__q">{q}<span class="st-faq2__plus" aria-hidden="true"></span></summary>'
                    f'<div class="st-faq2__a"><p>{a}</p></div></details>' for q, a in rows)
    return f'''
    <div class="st-faq2">
      <a class="st-land__pill st-land__pill--filled st-faq2__shop" href="#" style="--w:320;--ph:60;--fs:26;--pill-bg:#b80219">Shop all sets <span class="st-arrow" aria-hidden="true">↗</span></a>
      <h2 class="st-faq2__heading">FAQs</h2>
      <div class="st-faq2__list">{items}</div>
    </div>'''


def cream_section(key, inner, extra_class=''):
    return f'''<div class="shopify-section st-land-section">
<section class="st-land st-land--cream {extra_class}" data-land="{key}" style="{style_vars(key)}"><div class="st-land__inner">{beeline(key)}{inner}</div></section></div>'''


LAB_NAME_HL = True  # = sections/st-chapter.liquid name_highlight (st-fable approved the swipe, 10 Oct)


def chapter(key, c):
    jkey = 'chapter-' + key
    P = PARAMS[key]
    note = c['note'].replace('\n', '<br>')
    nails = ''.join(f'<span class="st-ch__nail" style="--st-nails:url(\'{A("nails/web/" + key + ".webp")}\');--col:{n}"></span>' for n in c['cols'])
    cap = f'<p class="st-ch__caption">{c["caption"]}</p>' if c.get('caption') else ''
    return f'''<div class="shopify-section st-land-section">
<section class="st-land st-ch{' st-ch--name-hl' if LAB_NAME_HL else ''}" data-land="{key}" style="{style_vars(jkey)}" aria-labelledby="h-{key}">
  <div class="st-land__inner">
    {beeline(jkey)}
    {''.join(art_html(it, lambda a: A(ASSETS[a]) if a in ASSETS else (TB / 'src/assets' / a).as_uri()) for it in c['art']).replace(ALT_TOKEN, '').replace(ALT_DESK_TOKEN, '')}
    {cards_html(lambda a: (TB / 'src/assets' / a).as_uri()) if key == 'wild-card' else ''}
    {c.get('ticks_html') or TICKS.get(c.get('ticks'), '')}
    <p class="st-ch__note{'' if '<br>' in note else ' st-ch__note--one'}">{note}{NOTE_TICKS if c.get('note_ticks') else ''}</p>
    <h2 class="st-ch__headline" id="h-{key}">{headline(c['head'], key, P['head_fs'], P['head_lead'], c.get('one', False), key)}</h2>
    <div class="st-ch__nails" aria-hidden="true">{nails}</div>
    <p class="st-ch__name"><span aria-hidden="true">“</span>{c['name']}<span aria-hidden="true">”</span></p>
    <a class="st-ch__pill" href="#">Shop set<span class="st-arrow" aria-hidden="true">↗</span></a>
    {cap}
  </div>
</section></div>'''


def cream(key, label):
    return f'''<div class="shopify-section st-land-section">
<section class="st-land" data-land="{key}" style="{style_vars(key)}"><div class="st-land__inner">{beeline(key)}
<p style="position:absolute;z-index:3;top:40%;width:100%;text-align:center;font:600 18px var(--font-ui);color:#999">{label} (placeholder)</p></div></section></div>'''


def footer_html():
    """The landing layout of sections/st-footer.liquid, with the theme's footer-group links (no social URLs set, so no
    icons: D5), the policy links that exist today (Contact us, Shipping, Privacy; Refund waits on the verified switch,
    Terms on its policy page) and the LND-062 copyright."""
    links = [('Shop', '#'), ('Our Story', '#'), ('the talks', '#'), ('Journal', '#'), ('Nail Guide', '#')]  # LND-060 v1.3.4
    legal = ['Contact us', 'Shipping policy', 'Privacy policy']
    nav = ''.join(f'<li><a href="{u}">{l}</a></li>' for l, u in links)
    leg = ''.join(f'<li><a href="#">{l}</a></li>' for l in legal)
    return f'''<div class="shopify-section"><div class="st-footer st-footer--landing">
  <a class="st-logo st-footer__logo" href="#"><span class="st-logo__words" aria-hidden="true"><span>small</span><span>talk</span></span></a>
  <p class="st-footer__tagline">Nails for real conversations.</p>
  <nav class="st-footer__nav"><ul role="list">{nav}</ul></nav>
  <ul class="st-footer__legal" role="list">{leg}</ul>
  <p class="st-footer__copyright">© 2026 Small Talk. All rights reserved.</p>
</div></div>'''


def lab():
    tokens = (TB / 'src/assets/st-tokens.css').read_text(encoding='utf-8')
    fonts = (TB / 'src/snippets/st-fonts.liquid').read_text(encoding='utf-8').split('{% style %}')[1].split('{% endstyle %}')[0]
    fonts = re.sub(r"\{\{ '([^']+)' \| asset_url \}\}", lambda m: (TB / 'fonts/out' / m.group(1)).as_uri(), fonts)
    css = (TB / 'src/assets/st-landing.css').read_text(encoding='utf-8')
    foot = (TB / 'src/sections/st-footer.liquid').read_text(encoding='utf-8').split('{% stylesheet %}')[1].split('{% endstylesheet %}')[0]
    hdr = (TB / 'src/sections/st-header.liquid').read_text(encoding='utf-8').split('{% stylesheet %}')[1].split('{% endstylesheet %}')[0]
    logo_css = hdr[hdr.index('  .st-logo {'):hdr.index('  .st-logo__image {')]
    avatar_css = (TB / 'src/snippets/st-talk-avatar.liquid').read_text(encoding='utf-8').split('{% stylesheet %}')[1].split('{% endstylesheet %}')[0]
    css += ':root { --minimum-touch-target: 44px; }' + logo_css + foot + avatar_css
    chapter_js = (TB / 'src/sections/st-chapter.liquid').read_text(encoding='utf-8').split('{% javascript %}')[1].split('{% endjavascript %}')[0]
    order = [('hero', None), ('tiles', 'Tiles'), ('diet-cherry', 'ch'), ('talks-teaser', 'the talks'), ('brainwave', 'ch'),
             ('green-flag', 'ch'), ('journal-teaser', 'Journal'), ('nail-guide-teaser', 'Nail Guide'), ('shaadi-shift', 'ch'),
             ('on-me', 'ch'), ('wild-card', 'ch'), ('pinky-promise', 'ch'), ('shop-all-faq-footer', 'Shop all / FAQ / footer')]
    body = []
    for k, kind in order:
        if k == 'hero':
            body.append('<div class="shopify-section"><div style="height:calc(653 * min(100vw / 390, 1.4px));background:radial-gradient(circle at 49% 22%,#fcc90a,#fbb804 45%,#e8a005);display:grid;place-items:center;font:600 18px sans-serif;color:#0006">hero (st-fable)</div></div>')
        elif kind == 'ch':
            body.append(chapter(k, CHAPTERS[k]))
        elif k == 'tiles':
            body.append(cream_section(k, tiles_html(lambda a: U(a) if a in ASSETS else (TB / 'src/assets' / a).as_uri())))
        elif k == 'talks-teaser':
            body.append(cream_section(k, talks_html(U)))
        elif k == 'journal-teaser':
            body.append(cream_section(k, journal_html(U)))
        elif k == 'nail-guide-teaser':
            body.append(cream_section(k, guide_html(U)))
        elif k == 'shop-all-faq-footer':
            body.append(cream_section(k, faq_html(U), 'st-land--flow'))
            body.append(footer_html())
        else:
            body.append(cream(k, kind))
    html = f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Landing lab</title>
<style>{tokens}{fonts}
* {{ box-sizing: border-box; }} body {{ margin: 0; background: var(--st-paper); }}
.visually-hidden {{ position: absolute !important; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }}
</style><style>{css}</style>
<style>@media screen and (min-width: 990px) {{ :root {{ --st-header-h: 76px; }} }}</style>
<script>{chapter_js}</script>
<body><div class="lab-header" style="position:sticky;top:0;z-index:20;height:var(--st-header-h);background:var(--st-paper);box-shadow:0 1px #0001"></div>{"".join(body)}</body></html>'''
    (TB / 'lab').mkdir(exist_ok=True)
    (TB / 'lab/landing.html').write_text(html, encoding='utf-8')


if __name__ == '__main__':
    PARAMS_PATH.parent.mkdir(exist_ok=True)
    if not PARAMS_PATH.exists():
        PARAMS_PATH.write_text(json.dumps(PARAMS, indent=1), encoding='utf-8')
    apply_compact()
    (TB / 'lab/pos.json').write_text(json.dumps({k: dict({x: L[x] for x in ('note_y', 'head_y', 'nails_y', 'name_y', 'pill_y')},
                                                         **{x: v for x, v in (L.get('caption') or {}).items() if x in ('cap_y', 'cap_b')}) for k, L in POS.items()}, indent=1), encoding='utf-8')
    for k, L in POS.items():
        print(f"{k:14} note {L['note_y']:6.1f}  head {L['head_y']:6.1f}  nails {L['nails_y']:6.1f}  name {L['name_y']:6.1f}  pill {L['pill_y']:6.1f}-{L['pill_b']:6.1f}"
              f"  cmin {L['cmin'] + 20:6.1f}  cmin2 {L['cmin2']:6.1f}  cmax {L['cmax']:6.1f}  (screen 595 / 612 / 620; full 775-786)")
    write_join_snippet()
    write_positions_css()
    write_desk_clear_css()
    write_map_snippet()
    lab()
    print('ok', len(KEYS), 'sections')
