"""st-fable: logo round 2. Designer exploration: one idea per mark, built as real vectors from the brand's OFL fonts
(fontTools outlines) plus hand-drawn shapes. Renders EXPLORE-SHEET.png: each direction at hero size, at header size and
as a 32 / 16 px favicon. Colour: --st-logo-blue on --st-cream. Nothing here touches the theme."""
import asyncio, math, pathlib, sys
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
from playwright.async_api import async_playwright

HERE = pathlib.Path(__file__).resolve().parent
FONTS = pathlib.Path(r'C:/Users/SSTS/Desktop/Riya/spec/fonts')
BLUE, CREAM = '#1412d5', '#fdf6e9'
F = {
    'ss4': FONTS / 'sourceserif4/SourceSerif4[opsz,wght].ttf',
    'fraunces': FONTS / 'fraunces/Fraunces[SOFT,WONK,opsz,wght].ttf',
    'dmserif': FONTS / 'dmserifdisplay/DMSerifDisplay-Regular.ttf',
    'abril': FONTS / 'abrilfatface/AbrilFatface-Regular.ttf',
    'caprasimo': FONTS / 'caprasimo/Caprasimo-Regular.ttf',
    'young': FONTS / 'youngserif/YoungSerif-Regular.ttf',
    'playfair': FONTS / 'playfairdisplay/PlayfairDisplay[wght].ttf',
    'dmsans': FONTS / 'dmsans/DMSans[opsz,wght].ttf',
}
_cache = {}


def font(key, **axes):
    k = (key, tuple(sorted(axes.items())))
    if k not in _cache:
        f = TTFont(F[key])
        if axes and 'fvar' in f:
            f = instancer.instantiateVariableFont(f, axes)
        _cache[k] = f
    return _cache[k]


def pair_kern(f, left, right):
    if 'GPOS' not in f:
        return 0
    for li in f['GPOS'].table.LookupList.Lookup:
        subs = [s.ExtSubTable for s in li.SubTable] if li.LookupType == 9 else li.SubTable
        for st in subs:
            if not hasattr(st, 'Coverage') or not hasattr(st, 'Format') or getattr(st, 'LookupType', 2) not in (2,):
                if not (hasattr(st, 'PairSet') or hasattr(st, 'Class1Record')):
                    continue
            cov = st.Coverage.glyphs
            if left not in cov:
                continue
            if st.Format == 1:
                for pvr in st.PairSet[cov.index(left)].PairValueRecord:
                    if pvr.SecondGlyph == right:
                        return (getattr(pvr.Value1, 'XAdvance', 0) or 0) if pvr.Value1 else 0
            elif st.Format == 2:
                c1 = st.ClassDef1.classDefs.get(left, 0); c2 = st.ClassDef2.classDefs.get(right, 0)
                v = st.Class1Record[c1].Class2Record[c2].Value1
                return (getattr(v, 'XAdvance', 0) or 0) if v else 0
    return 0


class Run:
    """A text run as an SVG path in font units with y down (baseline y=0), scaled so upm -> 1000."""
    def __init__(self, key, text, ls=0.0, skip=(), **axes):
        f = font(key, **axes); self.f = f
        upm = f['head'].unitsPerEm; s = 1000.0 / upm
        cmap = f.getBestCmap(); gs = f.getGlyphSet(); hm = f['hmtx']
        names = [cmap[ord(c)] for c in text]
        x = 0.0; self.pos = {}; sp = SVGPathPen(gs, ntos=lambda v: '%.1f' % v); bp = BoundsPen(gs)
        for i, g in enumerate(names):
            self.pos[i] = x * s
            if i not in skip:
                gs[g].draw(TransformPen(sp, (s, 0, 0, -s, x * s, 0)))
                gs[g].draw(TransformPen(bp, (s, 0, 0, -s, x * s, 0)))
            x += hm[g][0] + ls * upm
            if i + 1 < len(names):
                x += pair_kern(f, g, names[i + 1])
        self.d = sp.getCommands(); self.width = x * s
        self.bounds = bp.bounds or (0, 0, 0, 0)
        self.xh = -BoundsPen(gs).bounds if False else None
        b = BoundsPen(gs); gs[cmap[ord('x')]].draw(TransformPen(b, (s, 0, 0, -s, 0, 0))); self.xheight = -b.bounds[1]
        b = BoundsPen(gs); gs[cmap[ord('l')]].draw(TransformPen(b, (s, 0, 0, -s, 0, 0))); self.asc = -b.bounds[1]
        self.stem = stem_width(gs, cmap[ord('l')], s)

    def cross(self, i, text, y):
        gs = self.f.getGlyphSet(); cmap = self.f.getBestCmap(); s = 1000.0 / self.f['head'].unitsPerEm
        return crossings(gs, cmap[ord(text[i])], s, y, self.pos[i])

    def gbounds(self, i, text):
        gs = self.f.getGlyphSet(); cmap = self.f.getBestCmap(); upm = self.f['head'].unitsPerEm; s = 1000.0 / upm
        b = BoundsPen(gs); gs[cmap[ord(text[i])]].draw(TransformPen(b, (s, 0, 0, -s, self.pos[i], 0))); return b.bounds


from fontTools.pens.basePen import BasePen


class _Flat(BasePen):
    def __init__(self, gs):
        super().__init__(gs); self.segs = []; self.cur = None; self.start = None
    def _moveTo(self, p): self.cur = self.start = p
    def _lineTo(self, p): self.segs.append((self.cur, p)); self.cur = p
    def _curveToOne(self, p1, p2, p3):
        p0 = self.cur
        for i in range(1, 13):
            t = i / 12
            p = tuple((1 - t) ** 3 * p0[j] + 3 * (1 - t) ** 2 * t * p1[j] + 3 * (1 - t) * t ** 2 * p2[j] + t ** 3 * p3[j] for j in range(2))
            self.segs.append((self.cur, p)); self.cur = p
    def _closePath(self):
        if self.cur and self.start: self.segs.append((self.cur, self.start))
    def _endPath(self): self._closePath()


def crossings(gs, gname, s, y, dx=0.0):
    """Sorted x of the glyph outline's crossings with the horizontal line y (font units*s, y down, baseline 0)."""
    fp = _Flat(gs); gs[gname].draw(TransformPen(fp, (s, 0, 0, -s, dx, 0)))
    return sorted(a[0] + (b[0] - a[0]) * (y - a[1]) / (b[1] - a[1]) for a, b in fp.segs if (a[1] - y) * (b[1] - y) < 0)


def stem_width(gs, gname, s):
    b = BoundsPen(gs); gs[gname].draw(TransformPen(b, (s, 0, 0, -s, 0, 0)))
    y = b.bounds[1] + (b.bounds[3] - b.bounds[1]) * 0.35
    xs = crossings(gs, gname, s, y)
    return (xs[1] - xs[0]) if len(xs) >= 2 else 150


def almond(cx, cy, w, h, rot=0, point=0.55):
    """Press-on nail silhouette: pointed-ish top (almond), round base. Rot in degrees about centre."""
    t = cy - h / 2; b = cy + h / 2; r = w / 2
    d = (f'M{cx:.1f} {t:.1f} C{cx + r * point:.1f} {t + h * 0.22:.1f} {cx + r:.1f} {cy - h * 0.05:.1f} {cx + r:.1f} {cy + h * 0.12:.1f} '
         f'C{cx + r:.1f} {b - r * 0.0:.1f} {cx + r * 0.55:.1f} {b:.1f} {cx:.1f} {b:.1f} '
         f'C{cx - r * 0.55:.1f} {b:.1f} {cx - r:.1f} {b - r * 0.0:.1f} {cx - r:.1f} {cy + h * 0.12:.1f} '
         f'C{cx - r:.1f} {cy - h * 0.05:.1f} {cx - r * point:.1f} {t + h * 0.22:.1f} {cx:.1f} {t:.1f} Z')
    return d, (f'rotate({rot} {cx} {cy})' if rot else '')


def gloss(cx, cy, w, h, rot=0):
    """Slim highlight crescent on the upper left of a nail of size w x h."""
    x = cx - w * 0.22; y0 = cy - h * 0.32; y1 = cy + h * 0.05
    d = f'M{x:.1f} {y0:.1f} C{x - w * 0.10:.1f} {y0 + h * 0.12:.1f} {x - w * 0.10:.1f} {y1 - h * 0.1:.1f} {x + w * 0.02:.1f} {y1:.1f} C{x - w * 0.02:.1f} {y1 - h * 0.12:.1f} {x + w * 0.0:.1f} {y0 + h * 0.1:.1f} {x:.1f} {y0:.1f} Z'
    return d, (f'rotate({rot} {cx} {cy})' if rot else '')


def P(d, fill=BLUE, tr=''):
    return f'<path d="{d}" fill="{fill}"{(" transform=%r" % tr).replace("'", chr(34)) if tr else ""}/>'


def G(inner, tr):
    return f'<g transform="{tr}">{inner}</g>'


def svg(inner, x, y, w, h, pad=40):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x - pad:.0f} {y - pad:.0f} {w + 2 * pad:.0f} {h + 2 * pad:.0f}">{inner}</svg>'


def brush(x, y, L, ang, stem):
    """A polish brush: bristle tuft (tip at the origin), thin ferrule, round-ended cap; drawn along +x then rotated
    ang degrees about the tip (x, y)."""
    br = L * 0.30; fer = L * 0.16; cap = L - br - fer; w = stem
    tuft = (f'M0 0 C{br * 0.25:.0f} {-w * 0.30:.0f} {br * 0.6:.0f} {-w * 0.46:.0f} {br:.0f} {-w * 0.26:.0f} '
            f'L{br:.0f} {w * 0.26:.0f} C{br * 0.6:.0f} {w * 0.46:.0f} {br * 0.25:.0f} {w * 0.30:.0f} 0 0 Z')
    ferrule = f'M{br:.0f} {-w * 0.26:.0f} H{br + fer:.0f} V{w * 0.26:.0f} H{br:.0f} Z'
    r = w * 0.5
    capd = (f'M{br + fer:.0f} {-r:.0f} H{L - r:.0f} A{r:.0f} {r:.0f} 0 0 1 {L - r:.0f} {r:.0f} H{br + fer:.0f} Z')
    return P(tuft + ferrule + capd, tr=f'translate({x:.1f} {y:.1f}) rotate({ang})')


def bbox(*boxes):
    xs0 = min(b[0] for b in boxes); ys0 = min(b[1] for b in boxes); xs1 = max(b[2] for b in boxes); ys1 = max(b[3] for b in boxes)
    return xs0, ys0, xs1 - xs0, ys1 - ys0


DIRS = []


def direction(name, concept, main, icon):
    DIRS.append(dict(name=name, concept=concept, main=main, icon=icon))



_M = 0
BIG = 'maskUnits="userSpaceOnUse" x="-3000" y="-4000" width="12000" height="7000"'
BIGR = '<rect x="-3000" y="-4000" width="12000" height="7000" fill="#fff"/>'


def mask_id():
    global _M; _M += 1; return f'm{_M}'


def masked(d, removes, fill=BLUE):
    """The text path with shapes knocked out (one colour, no overlays)."""
    i = mask_id(); rm = ''.join(f'<path d="{r}" fill="#000"/>' for r in removes)
    return f'<mask id="{i}" {BIG}>{BIGR}{rm}</mask><path d="{d}" fill="{fill}" mask="url(#{i})"/>'


def knocked(inner, holes):
    """inner (blue shapes) with holes (list of (d, transform)) knocked out."""
    i = mask_id(); h = ''.join(f'<path d="{d}" fill="#000"{(" transform=%r" % t).replace(chr(39), chr(34)) if t else ""}/>' for d, t in holes)
    return f'<mask id="{i}" {BIG}>{BIGR}{h}</mask><g mask="url(#{i})">{inner}</g>'


def ss4_leg(sr, xh):
    """A leg like Source Serif Black's k leg, growing out of the stem's right edge x=sr (y down, baseline 0)."""
    return (f'M{sr:.0f} {-xh * 0.72:.0f} L{sr + 346:.0f} {-xh * 0.08:.0f} L{sr + 346:.0f} 0 H{sr + 86:.0f} L{sr:.0f} {-xh * 0.46:.0f} Z')


def ss4_arm(sr, xh):
    """The thin arm with its flag serif, like the font's."""
    return (f'M{sr:.0f} {-xh * 0.46:.0f} L{sr + 182:.0f} {-xh * 0.97:.0f} L{sr + 292:.0f} {-xh * 0.97:.0f} '
            f'L{sr + 292:.0f} {-xh * 1.0:.0f} L{sr + 150:.0f} {-xh * 1.0:.0f} L{sr + 40:.0f} {-xh * 0.62:.0f} L{sr:.0f} {-xh * 0.58:.0f} Z')


def whole_k_removed(r, i, text):
    kb = r.gbounds(i, text); asc = r.asc
    return masked(r.d, [f'M{kb[0] - 10:.0f} {-asc - 400} H{kb[2] + 200:.0f} V300 H{kb[0] - 10:.0f} Z'])


# ---------------------------------------------------------------- 1. the owner's idea: k as a finger being painted
def d1():
    r = Run('ss4', 'small talk', opsz=60, wght=900); st = r.stem; xh = r.xheight; asc = r.asc
    sl, sr = r.cross(9, 'small talk', -asc * 0.85)
    text = whole_k_removed(r, 9, 'small talk')
    cx = (sl + sr) / 2; w = sr - sl; top = -asc
    finger = f'M{sl:.0f} 0 V{top + w * 0.5:.0f} A{w / 2:.0f} {w / 2:.0f} 0 0 1 {sr:.0f} {top + w * 0.5:.0f} V0 Z'
    nail, _ = almond(cx, top + w * 0.78, w * 0.70, w * 1.48, point=0.6)
    gl, _ = gloss(cx, top + w * 0.78, w * 0.70, w * 1.48)
    leg = ss4_leg(sr, xh)
    arm = brush(cx + w * 0.30, top + w * 0.30, xh * 0.92, -44, st * 0.9)
    k = knocked(P(finger), [(nail, '')]) + P(gl) + P(leg) + arm
    inner = text + k
    W = sr + 346 + 40
    main = svg(inner, 0, -asc - 300, W, asc + 320, 30)
    icon = svg(k, sl - 30, -asc - 300, sr + 346 - sl + 60, asc + 320, 10)
    direction('1  k = a finger, brush on the nail', 'The owner\'s idea, done as type: the k\'s upright is a finger seen side-on with its nail on top; the k\'s arm IS the little polish brush, painting it. The leg stays the font\'s own. One line, because the brush rises above the ascender.', main, icon)


# ---------------------------------------------------------------- 2. k = a finger (no brush), stacked
def d2():
    r = Run('ss4', 'small', opsz=60, wght=900); t = Run('ss4', 'talk', opsz=60, wght=900); st = t.stem; xh = t.xheight; asc = t.asc
    sl, sr = t.cross(3, 'talk', -asc * 0.85)
    text = whole_k_removed(t, 3, 'talk')
    cx = (sl + sr) / 2; w = sr - sl; top = -asc
    finger = f'M{sl:.0f} 0 V{top + w * 0.5:.0f} A{w / 2:.0f} {w / 2:.0f} 0 0 1 {sr:.0f} {top + w * 0.5:.0f} V0 Z'
    nail, _ = almond(cx, top + w * 0.78, w * 0.70, w * 1.48, point=0.6)
    gl, _ = gloss(cx, top + w * 0.78, w * 0.70, w * 1.48)
    k = knocked(P(finger), [(nail, '')]) + P(gl) + P(ss4_arm(sr, xh)) + P(ss4_leg(sr, xh))
    talk = text + k; tw = sr + 346 - t.pos[0]; sw = r.width
    line = asc * 1.06
    inner = G(P(r.d), f'translate(0 {-line:.0f})') + G(talk, f'translate({(sw - tw) / 2 + 40:.0f} 0)')
    main = svg(inner, 0, -line - asc - 40, sw, line + asc + 60, 30)
    direction('2  k = a finger, no brush', "The quiet version: the k's upright is the finger with its nail, and the arm and leg stay the font's. Works in the current stacked layout with nothing else changed.", main, svg(k, sl - 30, -asc - 40, sr + 346 - sl + 60, asc + 60, 10))


# ---------------------------------------------------------------- 3. the set: five nails, a hand
def d3():
    wm = Run('fraunces', 'small talk', SOFT=100, WONK=0, opsz=144, wght=600); asc = wm.asc
    H = asc * 1.1; W = H * 0.50
    spec = [(-2, 0.80, -18), (-1, 0.95, -9), (0, 1.0, 0), (1, 0.96, 9), (2, 0.76, 19)]
    icon_inner = ''
    for i, hf, rot in spec:
        cx = i * W * 1.2; base = H * 0.5 + H * 0.10 * (i / 2) ** 2
        h = H * hf; cy = base - h / 2
        a, _ = almond(cx, cy, W, h, point=0.95)
        icon_inner += P(a, tr=f'rotate({rot} {cx:.0f} {base:.0f})')
    half = W * 2.56 + W / 2 + 40; gap = W * 1.6
    inner = G(icon_inner, f'translate({half:.0f} {-asc * 0.42:.0f})') + G(P(wm.d), f'translate({2 * half + gap:.0f} 0)')
    main = svg(inner, 0, -asc * 0.42 - H * 0.66, 2 * half + gap + wm.width, H * 1.5, 30)
    icon = svg(icon_inner, -W * 3.3, -H * 0.62, W * 6.6, H * 1.45, 10)
    direction('3  the set', 'Five nails fanned like fingertips: a hand seen tip-on, and literally what Small Talk sells (a set). Reads as nails at any size; the wordmark is a soft Fraunces.', main, icon)


# ---------------------------------------------------------------- 4. quote nails
def d4():
    wm = Run('fraunces', 'small talk', SOFT=100, WONK=0, opsz=144, wght=700); asc = wm.asc; xh = wm.xheight
    h = xh * 0.70; w = h * 0.46
    def quote(x, flip):
        out = ''
        for i in (0, 1):
            cx = x + i * w * 1.3; cy = -asc + h * 0.5; rot = (-18 if not flip else 162)
            a, _ = almond(cx, cy, w, h, point=0.7)
            out += P(a, tr=f'rotate({rot} {cx:.1f} {cy:.1f})')
        return out
    gap = w * 1.4
    x0 = w * 2.6 + gap
    inner = quote(w * 0.6, False) + G(P(wm.d), f'translate({x0:.1f} 0)') + quote(x0 + wm.width + gap, True)
    W = x0 + wm.width + gap + w * 2.9
    main = svg(inner, 0, -asc - 30, W, asc + 50, 30)
    icon = svg(quote(0, False) + G(quote(0, True), f'translate({w * 2.9:.0f} {h * 1.35:.0f})'), -w * 0.9, -asc - 30, w * 6.0, h * 3.2, 0)
    direction('4  “quote nails”', 'Quotation marks are already nail-shaped. The name sits inside quotes made of four tiny press-ons: talk and nails in one device, and the quotes alone are the icon.', main, icon)


# ---------------------------------------------------------------- 5. a wave inside the bubble
def d5():
    wm = Run('dmserif', 'small talk'); asc = wm.asc; xh = wm.xheight
    bw = xh * 2.0; bh = xh * 1.22; r = bh * 0.5
    bx = wm.width + xh * 0.4; by = -xh * 1.05
    bubble = (f'M{bx + r:.1f} {by:.1f} H{bx + bw - r:.1f} A{r} {r} 0 0 1 {bx + bw:.1f} {by + r:.1f} V{by + bh - r:.1f} A{r} {r} 0 0 1 {bx + bw - r:.1f} {by + bh:.1f} '
              f'H{bx + bw * 0.36:.1f} L{bx + bw * 0.10:.1f} {by + bh + xh * 0.28:.1f} L{bx + bw * 0.17:.1f} {by + bh - r * 0.25:.1f} '
              f'A{r} {r} 0 0 1 {bx:.1f} {by + bh - r:.1f} V{by + r:.1f} A{r} {r} 0 0 1 {bx + r:.1f} {by:.1f} Z')
    holes = []
    nh = bh * 0.52; nw = nh * 0.56
    for i, (hf, rot) in enumerate([(0.88, -14), (1.0, 0), (0.88, 14)]):
        cx = bx + bw * (0.27 + 0.23 * i); base = by + bh * 0.76
        a, _ = almond(cx, base - nh * hf / 2, nw, nh * hf, point=0.95); holes.append((a, f'rotate({rot} {cx:.0f} {base:.0f})'))
    bub = knocked(P(bubble), holes)
    inner = P(wm.d) + bub
    main = svg(inner, 0, -asc - 20, bx + bw, asc + 60, 30)
    icon = svg(bub, bx - 10, by - 10, bw + 20, bh + xh * 0.32 + 20, 0)
    direction('5  a wave in the bubble', 'A speech bubble with three fanned nails knocked out of it: fingertips waving "hey". Talk and nails in one icon; the wordmark is DM Serif.', main, icon)


# ---------------------------------------------------------------- 6. small inside talk
def d6():
    big = Run('fraunces', 'talk', SOFT=100, WONK=1, opsz=144, wght=900); small = Run('fraunces', 'small', SOFT=100, WONK=0, opsz=9, wght=700)
    asc = big.asc; xh = big.xheight
    tb = big.gbounds(0, 'talk')
    s = 0.36
    sx = tb[0] - big.stem * 0.12 - small.width * s; sy = -xh * 0.99
    inner = P(big.d) + G(P(small.d), f'translate({sx:.1f} {sy:.1f}) scale({s})')
    x0 = sx - 20
    main = svg(inner, x0, -asc - 20, big.width - x0, asc + 40, 30)
    icon = main
    direction('6  a small "small"', 'The name is the joke, so the type tells it: "small" is set small, floating in at the crossbar of a big, soft, slightly wonky "talk". Pure type; nothing to decode.', main, icon)


def coffin(cx, cy, w, h):
    """Coffin / ballerina nail: tapered sides, flat rounded tip, round base."""
    tw = w * 0.62; r = w * 0.14
    t = cy - h / 2; b = cy + h / 2
    return (f'M{cx - tw / 2 + r:.0f} {t:.0f} H{cx + tw / 2 - r:.0f} Q{cx + tw / 2:.0f} {t:.0f} {cx + tw / 2 + r * 0.3:.0f} {t + r:.0f} '
            f'L{cx + w / 2:.0f} {cy + h * 0.12:.0f} C{cx + w / 2:.0f} {b:.0f} {cx - w / 2:.0f} {b:.0f} {cx - w / 2:.0f} {cy + h * 0.12:.0f} '
            f'L{cx - tw / 2 - r * 0.3:.0f} {t + r:.0f} Q{cx - tw / 2:.0f} {t:.0f} {cx - tw / 2 + r:.0f} {t:.0f} Z')


# ---------------------------------------------------------------- 7. the nail badge monogram
def d7():
    mono = Run('abril', 'st'); wm = Run('ss4', 'small talk', opsz=60, wght=700)
    H = 1400; W = H * 0.44
    nail = coffin(0, 0, W, H)
    mb = mono.bounds; mw = mb[2] - mb[0]; mh = mb[3] - mb[1]
    sc = (W * 0.74) / mw
    icon_inner = knocked(P(nail), [(mono.d, f'translate({-mw * sc / 2 - mb[0] * sc:.1f} {(H * 0.08) + mh * sc / 2 - mb[3] * sc:.1f}) scale({sc:.3f})')])
    asc = wm.asc
    inner = G(icon_inner, f'translate({W / 2:.0f} {-H / 2:.0f})') + G(P(wm.d), f'translate({W + 220:.0f} {-H * 0.5 + asc * 0.5:.0f})')
    main = svg(inner, 0, -H, W + 220 + wm.width, H, 30)
    icon = svg(icon_inner, -W / 2, -H / 2, W, H, 40)
    direction('7  "st" on a coffin nail', 'A monogram: st knocked out of one coffin-shaped nail, the shape every press-on buyer knows. Badge-like: app icon, box sticker, wax seal; the wordmark rides alongside.', main, icon)


# ---------------------------------------------------------------- 8. speech bubble badge, nail-tipped tail
def d8():
    sm = Run('caprasimo', 'small'); ta = Run('caprasimo', 'talk'); asc = sm.asc
    line = asc * 1.12
    tw = max(sm.width, ta.width); H = line + asc
    padx, pady = 170, 150
    bw = tw + 2 * padx; bh = H + 2 * pady; r = 260
    bx, by = -padx, -line - asc - pady
    bubble = (f'M{bx + r:.0f} {by:.0f} H{bx + bw - r:.0f} A{r} {r} 0 0 1 {bx + bw:.0f} {by + r:.0f} V{by + bh - r:.0f} A{r} {r} 0 0 1 {bx + bw - r:.0f} {by + bh:.0f} '
              f'H{bx + r:.0f} A{r} {r} 0 0 1 {bx:.0f} {by + bh - r:.0f} V{by + r:.0f} A{r} {r} 0 0 1 {bx + r:.0f} {by:.0f} Z')
    tx, ty = bx + bw * 0.24, by + bh + 40
    tail, _ = almond(tx, ty, 300, 760, point=0.5)
    body = P(bubble) + P(tail, tr=f'rotate(180 {tx:.0f} {ty:.0f})')
    inner = knocked(body, [(sm.d, f'translate({(tw - sm.width) / 2:.0f} {-line:.0f})'), (ta.d, f'translate({(tw - ta.width) / 2:.0f} 0)')])
    main = svg(inner, bx, by, bw, bh + 420, 30)
    icon = main
    direction('8  the bubble', 'The name inside one chunky speech bubble whose tail is a nail (an almond, tip down). Reversed, friendly Caprasimo: a sticker you recognise before you read it.', main, icon)


def d0():
    base = (HERE.parent / 'base.svg').read_text(encoding='utf-8')
    base = base.replace('#001df9', BLUE).replace('#001DF9', BLUE)
    direction('0  current logo (for comparison)', 'The official stacked serif wordmark as it is today.', base, base)


def d1b():
    r = Run('ss4', 'small', opsz=60, wght=900); t = Run('ss4', 'talk', opsz=60, wght=900); st = t.stem; xh = t.xheight; asc = t.asc
    sl, sr = t.cross(3, 'talk', -asc * 0.85)
    text = whole_k_removed(t, 3, 'talk')
    cx = (sl + sr) / 2; w = sr - sl; top = -asc
    finger = f'M{sl:.0f} 0 V{top + w * 0.5:.0f} A{w / 2:.0f} {w / 2:.0f} 0 0 1 {sr:.0f} {top + w * 0.5:.0f} V0 Z'
    nail, _ = almond(cx, top + w * 0.78, w * 0.70, w * 1.48, point=0.6)
    gl, _ = gloss(cx, top + w * 0.78, w * 0.70, w * 1.48)
    # the brush lies flat so it stays under "small"
    arm = brush(cx + w * 0.34, top + w * 0.50, xh * 0.92, 6, st * 0.9)
    k = knocked(P(finger), [(nail, '')]) + P(gl) + P(ss4_leg(sr, xh)) + arm
    talk = text + k; tw = sr + 346 + 20 - t.pos[0]; sw = r.width
    line = asc * 1.06
    inner = G(P(r.d), f'translate(0 {-line:.0f})') + G(talk, f'translate({(sw - tw) / 2 + 60:.0f} 0)')
    main = svg(inner, 0, -line - asc - 40, max(sw, (sw - tw) / 2 + 60 + tw + 300), line + asc + 60, 30)
    direction('1b  the same k, stacked', 'Direction 1 in the current stacked layout: the brush lies flatter and paints in from the right, under "small".', main, svg(k, sl - 30, -asc - 200, sr + 500 - sl, asc + 220, 10))


for fn in (d0, d1, d1b, d2, d3, d4, d5, d6, d7, d8):
    fn()


async def render():
    cards = ''
    for i, d in enumerate(DIRS):
        (HERE / f'r2-{i + 1}.svg').write_text(d['main'], encoding='utf-8')
        (HERE / f'r2-{i + 1}-icon.svg').write_text(d['icon'], encoding='utf-8')
        cards += f"""<div class=card><div class=h>{d['name']}</div><div class=c>{d['concept']}</div>
        <div class=row><div class=hero>{d['main']}</div>
        <div class=side><div class=lab>header size</div><div class=hdr>{d['main']}</div>
        <div class=lab>favicon 32 / 16 (real, then 4x)</div><div class=fav><span class=f32>{d['icon']}</span><span class=f16>{d['icon']}</span><span class=f32x>{d['icon']}</span><span class=f16x>{d['icon']}</span></div></div></div></div>"""
    html = f"""<!doctype html><meta charset=utf-8><style>
    body{{margin:0;background:{CREAM};font-family:'DM Sans',Arial,sans-serif;color:#0d0b10;padding:24px}}
    .grid{{display:grid;grid-template-columns:1fr 1fr;gap:22px}}
    .card{{background:#fff8ee;border:1px solid #e7dcc6;border-radius:14px;padding:16px 18px}}
    .h{{font-weight:700;font-size:20px;color:#1412d5}} .c{{font-size:13px;color:#555;margin:4px 0 12px;max-width:620px;line-height:1.35}}
    .row{{display:flex;gap:22px;align-items:flex-start}}
    .hero{{width:440px;height:300px;display:flex;align-items:center;justify-content:center}} .hero svg{{max-width:440px;max-height:300px;display:block}}
    .side{{width:220px}} .lab{{font-size:11px;color:#888;margin:4px 0}}
    .hdr{{background:{CREAM};border:1px solid #eee;height:64px;display:flex;align-items:center;padding:0 12px;width:196px}} .hdr svg{{max-height:48px;max-width:190px}}
    .fav span{{display:inline-block;vertical-align:top;margin-right:8px;background:#fff;border:1px solid #ddd}}
    .f32{{width:32px;height:32px}} .f16{{width:16px;height:16px}} .f32x{{width:128px;height:128px}} .f16x{{width:64px;height:64px}}
    .fav svg{{width:100%;height:100%;display:block;image-rendering:pixelated}}
    .f32x svg,.f16x svg{{image-rendering:pixelated}}
    </style><div class=grid>{cards}</div>"""
    (HERE / 'sheet.html').write_text(html, encoding='utf-8')
    async with async_playwright() as p:
        br = await p.chromium.launch(channel='chrome'); pg = await br.new_page(viewport={'width': 1500, 'height': 900}, device_scale_factor=1)
        await pg.goto((HERE / 'sheet.html').as_uri()); await pg.wait_for_timeout(400)
        # real-pixel favicons: raster the icon at 32/16 then scale up, so the 4x tiles show true pixels
        await pg.evaluate("""() => { for (const [cls, px] of [['f32x',32],['f16x',16]]) for (const el of document.querySelectorAll('.'+cls)) {
            const svg = el.querySelector('svg'); const xml = new XMLSerializer().serializeToString(svg);
            const img = new Image(); img.src = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(xml)));
            img.decode().then(() => { const c = document.createElement('canvas'); c.width = px; c.height = px; const g = c.getContext('2d');
              g.fillStyle = '#fff'; g.fillRect(0,0,px,px); g.drawImage(img, 0, 0, px, px); c.style.width = c.style.height = '100%'; c.style.imageRendering = 'pixelated'; el.innerHTML=''; el.appendChild(c); }); } }""")
        await pg.wait_for_timeout(600)
        await pg.screenshot(path=str(HERE / 'EXPLORE-SHEET.png'), full_page=True); await br.close()
    print('ok', len(DIRS))


asyncio.run(render())
