"""HD character peeks (HD batch 2: "Phase-2 character peeks -> HD") -> src/snippets/st-peek-map.liquid.

Same crop logic as the Phase-2 peeks: each component shows the character's eye at its board landing point and size.
The HD pieces are cut or feathered at one side (they bleed off the page on the landing), so the crop is searched:
zoom (eye size x m, m >= 1) and eye position are traded off (cost = (eye offset / quarter box)^2 + ((m - 1) / 0.2)^2)
over the crops whose box is covered by opaque art (alpha >= 200 on >= 99.6% of it; avatar circle 99%): no cut edge,
feather or empty corner inside the box. Never above source density (css width <= asset width). The avatar is a face
crop: its anchor is the face centre (FACE), not the eye. Shaadi's rect peeks come from the HD sweep (st-fable HD2
fix 2); its avatar keeps the Phase-2 character and numbers (the sweep has no full face).

Usage: python -I tools/build_peeks.py [--sheet out.png]
"""
import pathlib
import sys

import numpy as np
from PIL import Image, ImageDraw

TB = pathlib.Path(__file__).resolve().parents[1]
AS = TB / 'src/assets'
P2DIR = TB.parent / 'artwork/characters/web'

# set: (asset, eye_x, eye_y, eye_w) in asset px; eye = iris centre, eye_w = corner to corner (measured on the art)
HD = {
    'on-me': ('st-hd-on-me-woman.webp', 90, 392, 100),
    'brainwave': ('st-hd-brainwave-woman.webp', 95, 228, 105),
    'diet-cherry': ('st-hd-diet-cherry-woman.webp', 130, 525, 175),
    'green-flag': ('st-hd-green-flag-woman.webp', 690, 393, 150),
    'wild-card': ('st-hd-wild-card-woman-v2.webp', 95, 340, 100),
    'pinky-promise': ('st-hd-pinky-promise-scene.webp', 175, 302, 73),  # board-corrections re-fit, 904 x 797
    # st-fable HD2 fix 2: Shaadi's PDP / bag (and Our Story / guide) peeks from the HD sweep, eye under the dupatta.
    'shaadi-shift': ('st-hd-shaadi-shift-sweep.webp', 115, 495, 170),
}
# Parts that keep the Phase-2 numbers for a set (the sweep has no full face for the avatar circle).
P2_ONLY = {('avatar', 'shaadi-shift')}
# Per-set top band (css px) that must be fully opaque: st-fable V37 note 14a, the sweep's dupatta edge left a small
# transparent notch at the Shaadi boxes' top-right corner.
TOP_BAND = {'shaadi-shift': 16}
# Per-set eye size override (css px): st-fable HD2 fix 3, the Diet Cherry avatar face centres at eye ~40.
EYE_OVERRIDE = {('avatar', 'diet-cherry'): 40}
# avatar anchor: face centre (between the eye and the mouth), asset px
FACE = {'on-me': (110, 450), 'brainwave': (100, 290), 'diet-cherry': (100, 590), 'green-flag': (680, 450),
        'wild-card': (120, 400), 'pinky-promise': (213, 332)}
# component: box w, box h, eye target x, y (css px in the box), eye css width (Phase-2: ~43 asset px eye at its
# display scale), shape. Boxes: PDP coda 115 x 130 (eye 70,65, image 300 wide); bag 145 x 160 (108,122, 300 wide);
# Our Story 190 x 80 (48,42, 1.3x); guide 90 x 131 (70,54, 260 wide); talks-teaser avatar 80 circle, in 390-px units:
# face centre at the circle centre, eye ~26 (the HD faces are half faces, so the circle holds eye, nose and mouth).
COMP = {
    'pdp': (115, 130, 70, 65, 43, 'rect'),
    'bag': (145, 160, 108, 122, 43, 'rect'),
    'story': (190, 80, 48, 42, 56, 'rect'),
    'guide': (90, 131, 70, 54, 38, 'rect'),
    'avatar': (80, 80, 40, 40, 26, 'circle'),
}
# Phase-2 Shaadi, exactly what the sections computed before (src, intrinsic w, h, left, top, css width)
SHAADI = ('st-character-shaadi-shift.webp', 281, 622)
SHAADI_P2 = {'pdp': (-8, -130, 300), 'bag': (30, -73, 300), 'story': (-47, -196, 365), 'guide': (2, -115, 260),
             'avatar': (9, -27, 87)}
COVER = {'rect': 0.996, 'circle': 0.99}
OPAQUE = 200


def bands(bw, bh, shape):
    """Box as horizontal bands (x0, y0, x1, y1); a circle is approximated by 4-px bands of its chords."""
    if shape == 'rect':
        return [(0, 0, bw, bh)]
    out = []
    r = bw / 2
    for y in range(0, bh, 4):
        yc = min(abs(y - r), abs(y + 4 - r)) if y < r < y + 4 else min(abs(y - r), abs(y + 4 - r))
        half = (r * r - yc * yc) ** 0.5 if yc < r else 0
        x0, x1 = int(np.floor(r - half)), int(np.ceil(r + half))
        if x1 > x0:
            out.append((x0, y, x1, min(y + 4, bh)))
    return out


def search(alpha, ex, ey, ew, comp, anchor=None, band=0):
    bw, bh, tx, ty, eye, shape = comp
    ax, ay = anchor or (ex, ey)
    q = min(bw, bh) / 4
    W, H = alpha.size
    B = bands(bw, bh, shape)
    area = sum((x1 - x0) * (y1 - y0) for x0, y0, x1, y1 in B)
    best = None
    for m in np.arange(1.0, 3.001, 0.02):
        f = eye * m / ew
        if f > 1.0:
            break
        ws, hs = round(W * f), round(H * f)
        if ws < bw or hs < bh:
            continue
        a = np.asarray(alpha.resize((ws, hs), Image.LANCZOS)) >= OPAQUE
        S = np.zeros((hs + 1, ws + 1), np.int32)
        S[1:, 1:] = a.cumsum(0).cumsum(1)
        nx, ny = ws - bw + 1, hs - bh + 1  # box origin in image coords: (u, v), u in [0, nx), v in [0, ny)
        cov = np.zeros((ny, nx), np.int64)
        for x0, y0, x1, y1 in B:
            cov += (S[y1:y1 + ny, x1:x1 + nx] - S[y0:y0 + ny, x1:x1 + nx]
                    - S[y1:y1 + ny, x0:x0 + nx] + S[y0:y0 + ny, x0:x0 + nx])
        ok = cov >= COVER[shape] * area
        if band:
            top = (S[band:band + ny, bw:bw + nx] - S[0:ny, bw:bw + nx] - S[band:band + ny, 0:nx] + S[0:ny, 0:nx])
            ok &= top >= 0.999 * band * bw
        # eye inside the box: centre at least half an eye from the sides, 12 px from top/bottom (avatar: 8)
        u = np.arange(nx)[None, :]
        v = np.arange(ny)[:, None]
        exb = ex * f - u
        eyb = ey * f - v
        half = eye * m / 2
        mv = 8 if shape == 'circle' else 12
        ok &= (exb >= half) & (exb <= bw - half) & (eyb >= mv) & (eyb <= bh - mv)
        if ok.any():
            d = ((ax * f - u - tx) ** 2 + (ay * f - v - ty) ** 2) / q ** 2 + ((m - 1) / 0.2) ** 2
            d = np.where(ok, d, np.inf)
            vv, uu = np.unravel_index(np.argmin(d), d.shape)
            if best is None or d[vv, uu] < best['cost']:
                best = dict(m=round(float(m), 2), f=f, w=ws, h=hs, left=-int(uu), top=-int(vv), cost=float(d[vv, uu]),
                            eye=(float(ex * f - uu), float(ey * f - vv)), cover=float(cov[vv, uu] / area))
    return best


def build():
    rows = {}
    for k, (src, ex, ey, ew) in HD.items():
        im = Image.open(AS / src)
        alpha = im.convert('RGBA').getchannel('A')
        for c, comp in COMP.items():
            if (c, k) in P2_ONLY:
                continue
            if (c, k) in EYE_OVERRIDE:
                comp = comp[:4] + (EYE_OVERRIDE[(c, k)],) + comp[5:]
            r = search(alpha, ex, ey, ew, comp, FACE.get(k) if c == 'avatar' else None,
                       TOP_BAND.get(k, 0) if comp[5] == 'rect' else 0)
            assert r, (k, c)
            rows[(c, k)] = (src, im.width, im.height, r['left'], r['top'], r['w'], r)
    for c, (l, t, w) in SHAADI_P2.items():
        if (c, 'shaadi-shift') in P2_ONLY:
            rows[(c, 'shaadi-shift')] = (*SHAADI, l, t, w, None)
    return rows


def write(rows):
    L = ['{%- comment -%}',
         '  Generated by tools/build_peeks.py: do not edit by hand. HD character peeks (HD batch 2).',
         '  render with key (campaign handle) and part: pdp | bag | story | guide | avatar.',
         '  Echoes "src,width,height,left,top,css_width": src/width/height = the asset and its intrinsic size; left/top/',
         '  css_width = where the image sits in the peek box, css px (avatar: 390-px units, times --k). Same crop logic',
         '  as Phase-2: the eye at the board point and size, moved/zoomed only as far as needed to keep cut edges and',
         '  feathers out of the box; never above source density. Shaadi keeps its Phase-2 character (no HD face).',
         '{%- endcomment -%}',
         '{%- case part -%}']
    for c in COMP:
        L.append(f"  {{%- when '{c}' -%}}")
        L.append('    {%- case key -%}')
        for k in HD:
            src, iw, ih, l, t, w, _ = rows[(c, k)]
            L.append(f"      {{%- when '{k}' -%}}{src},{iw},{ih},{l},{t},{w}")
        L.append('    {%- endcase -%}')
    L += ['{%- endcase -%}', '']
    (TB / 'src/snippets/st-peek-map.liquid').write_text('\n'.join(L), encoding='utf-8', newline='\n')


def sheet(rows, out):
    S = 2
    cols = list(COMP)
    keys = list(HD)
    cw = 210 * S
    img = Image.new('RGB', (len(cols) * cw + 110, len(keys) * 190 * S), 'white')
    d = ImageDraw.Draw(img)
    for ri, k in enumerate(keys):
        d.text((4, ri * 190 * S + 4), k, fill='black')
        for ci, c in enumerate(cols):
            src, iw, ih, l, t, w, r = rows[(c, k)]
            bw, bh = COMP[c][:2]
            p = (AS / src) if src.startswith('st-hd') else (P2DIR / src.replace('st-character-', ''))
            im = Image.open(p).convert('RGBA')
            h = round(ih * w / iw)
            sc = im.resize((w * S, h * S), Image.LANCZOS)
            box = Image.new('RGBA', (bw * S, bh * S), (251, 246, 238, 255))
            layer = Image.new('RGBA', box.size, (0, 0, 0, 0))
            layer.paste(sc, (l * S, t * S))
            box.alpha_composite(layer)
            if COMP[c][5] == 'circle':
                mask = Image.new('L', box.size, 0)
                ImageDraw.Draw(mask).ellipse((0, 0, bw * S - 1, bh * S - 1), fill=255)
                bg = Image.new('RGBA', box.size, (255, 255, 255, 255))
                bg.paste(box, (0, 0), mask)
                box = bg
            X, Y = 110 + ci * cw, ri * 190 * S + 34
            img.paste(box.convert('RGB'), (X, Y))
            d.rectangle((X - 1, Y - 1, X + bw * S, Y + bh * S), outline=(200, 0, 0))
            note = f"{c} w{w} ({l},{t})"
            if r:
                note += f" m{r['m']} eye({r['eye'][0]:.0f},{r['eye'][1]:.0f}) src/css {iw / w:.2f}"
            else:
                note += ' Phase-2'
            d.text((X, Y - 30), note, fill='black')
    img.save(out)


if __name__ == '__main__':
    rows = build()
    write(rows)
    for (c, k), (src, iw, ih, l, t, w, r) in sorted(rows.items()):
        extra = f"m={r['m']} eye=({r['eye'][0]:.1f},{r['eye'][1]:.1f}) cover={r['cover']:.3f} src/css={iw / w:.2f}" if r else 'Phase-2'
        print(f'{c:7} {k:14} w={w:4} left={l:5} top={t:5} {extra}')
    if '--sheet' in sys.argv:
        sheet(rows, sys.argv[sys.argv.index('--sheet') + 1])
