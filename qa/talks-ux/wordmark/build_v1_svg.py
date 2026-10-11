"""st-fable: outlined SVG of the owner-picked wordmark V1 ("the talks", Caveat 700, -0.015em, "the" + 0.2em + "talks",
rotated -3deg, ink #0d0b10). Glyphs from the OFL Caveat variable font instanced at wght 700, kerned with the font's GPOS
pair kerning. Writes st-talks-wordmark-v1.svg and v1-svg-meta.json (sizes for the header and hub title)."""
import json, math, pathlib
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

HERE = pathlib.Path(__file__).resolve().parent
SRC = pathlib.Path(r'C:/Users/SSTS/Desktop/Riya/spec/fonts/caveat/Caveat[wght].ttf')
font = instancer.instantiateVariableFont(TTFont(SRC), {'wght': 700})
upm = font['head'].unitsPerEm
cmap = font.getBestCmap(); hmtx = font['hmtx']; gs = font.getGlyphSet()


def pair_kern(left, right):
    """GPOS PairPos (formats 1 and 2) x-advance adjustment for a glyph pair, in font units."""
    if 'GPOS' not in font:
        return 0
    gpos = font['GPOS'].table
    for li in gpos.LookupList.Lookup:
        subs = li.SubTable
        if li.LookupType == 9:
            subs = [s.ExtSubTable for s in subs]
        for st in subs:
            if getattr(st, 'LookupType', 2) != 2 and li.LookupType not in (2, 9):
                continue
            if not hasattr(st, 'Format') or not hasattr(st, 'Coverage'):
                continue
            cov = st.Coverage.glyphs
            if left not in cov:
                continue
            if st.Format == 1:
                for pvr in st.PairSet[cov.index(left)].PairValueRecord:
                    if pvr.SecondGlyph == right:
                        v = pvr.Value1
                        return getattr(v, 'XAdvance', 0) or 0 if v else 0
            elif st.Format == 2:
                c1 = st.ClassDef1.classDefs.get(left, 0); c2 = st.ClassDef2.classDefs.get(right, 0)
                rec = st.Class1Record[c1].Class2Record[c2]
                v = rec.Value1
                return (getattr(v, 'XAdvance', 0) or 0) if v else 0
    return 0


LS = -0.015 * upm          # letter-spacing
GAP = 0.2 * upm            # margin between "the" and "talks"
x = 0.0
placed = []                # (glyphName, x)
for wi, word in enumerate(['the', 'talks']):
    names = [cmap[ord(c)] for c in word]
    for i, g in enumerate(names):
        placed.append((g, x))
        x += hmtx[g][0] + LS
        if i + 1 < len(names):
            x += pair_kern(g, names[i + 1])
    if wi == 0:
        x += GAP
# bounds (font units, y up)
bp = BoundsPen(gs)
for g, gx in placed:
    gs[g].draw(TransformPen(bp, (1, 0, 0, 1, gx, 0)))
xmin, ymin, xmax, ymax = bp.bounds
cx, cy = (xmin + xmax) / 2, (ymin + ymax) / 2
# path: flip y, rotate -3deg (counter-clockwise on screen) about the centre
a = math.radians(-3)
ca, sa = math.cos(a), math.sin(a)
# screen coords: X = x, Y = -y ; rotation about (cx, -cy) in screen space
def M(tx):
    # affine for a glyph at x offset tx: font (x, y) -> screen rotated
    # first: (x + tx, -y); then translate to centre, rotate, translate back
    # [ca -sa; sa ca] * ([x+tx, -y] - [cx, -cy]) + [cx, -cy]
    return (ca, sa, sa * -1 * -1 * 1 if False else sa, -ca, 0, 0)
sp = SVGPathPen(gs, ntos=lambda v: ('%d' % round(v)))
for g, gx in placed:
    # combined affine: p' = R * (S * p + t - c) + c, S = diag(1, -1), t = (gx, 0), c = (cx, -cy)
    # R*S = [[ca, sa], [sa, -ca]]  (R = [[ca, -sa], [sa, ca]], S flips y)
    tx = ca * (gx - cx) - sa * (cy) + cx
    ty = sa * (gx - cx) + ca * (cy) - cy
    gs[g].draw(TransformPen(sp, (ca, sa, sa, -ca, tx, ty)))
d = sp.getCommands()
# rotated bounds
bp2 = BoundsPen(gs)
for g, gx in placed:
    tx = ca * (gx - cx) - sa * (cy) + cx
    ty = sa * (gx - cx) + ca * (cy) - cy
    gs[g].draw(TransformPen(bp2, (ca, sa, sa, -ca, tx, ty)))
rx0, ry0, rx1, ry1 = bp2.bounds
pad = 0.02 * upm
vb = (rx0 - pad, ry0 - pad, (rx1 - rx0) + 2 * pad, (ry1 - ry0) + 2 * pad)
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb[0]:.1f} {vb[1]:.1f} {vb[2]:.1f} {vb[3]:.1f}" '
       f'aria-hidden="true" focusable="false"><path fill="currentColor" d="{d}"/></svg>')
(HERE / 'st-talks-wordmark-v1.svg').write_text(svg, encoding='utf-8')
# sizes: the SVG height in em of the text size it replaces (CSS: height: calc(<em> * font-size))
h_em = vb[3] / upm; w_em = vb[2] / upm
# baseline position inside the viewBox (for alignment): unrotated baseline y=0 at the centre x -> screen y = -(-cy)... approx
meta = {'upm': upm, 'viewBox': [round(v, 1) for v in vb], 'height_em': round(h_em, 4), 'width_em': round(w_em, 4),
        'sizes_px': {f'{fs}px': {'w': round(w_em * fs, 1), 'h': round(h_em * fs, 1)} for fs in (19.5, 23.8, 40, 52)},
        'bytes': len(svg.encode())}
(HERE / 'v1-svg-meta.json').write_text(json.dumps(meta, indent=1), encoding='utf-8')
print(json.dumps(meta, indent=1))
