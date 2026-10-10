"""Wild Card hint cards: Ace of spades + King of hearts as flat vector cards in the boards' ink style.
Geometry is built once in Python (absolute coordinates, no SVG transforms) and written both as SVG paths and
rasterised with Pillow at 4x supersampling (identical geometry -> PNG fallbacks match the SVG)."""
import math, os
import numpy as np
from PIL import Image, ImageDraw
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.basePen import BasePen

ART = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
FONT = os.path.join(ART, "..", "spec", "fonts", "sourceserif4", "SourceSerif4[opsz,wght].ttf")
OUT = os.path.join(ART, "hd", "wild-card")
W, H = 250, 350
INK = "#160301"; CREAM = "#fde3c6"; SHADE = "#f3cba2"; RED = "#dc0d17"; BLACK = "#160301"

HEART = "M50 92 C20 70 2 52 2 31 C2 14 14 4 28 4 C38 4 46 10 50 19 C54 10 62 4 72 4 C86 4 98 14 98 31 C98 52 80 70 50 92 Z"
SPADE = ("M50 3 C68 24 98 40 98 62 C98 76 87 86 74 86 C64 86 57 81 53 73 C55 84 59 92 67 98 L33 98 "
         "C41 92 45 84 47 73 C43 81 36 86 26 86 C13 86 2 76 2 62 C2 40 32 24 50 3 Z")


# ---------- path model: list of subpaths, each a list of ('M'|'L'|'C', pts) ----------
def parse(d):
    import re
    toks = re.findall(r"[MLCZ]|-?[\d.]+", d)
    subs, cur, i = [], None, 0
    while i < len(toks):
        t = toks[i]
        if t == "M":
            cur = [("M", [(float(toks[i + 1]), float(toks[i + 2]))])]; subs.append(cur); i += 3
        elif t == "L":
            cur.append(("L", [(float(toks[i + 1]), float(toks[i + 2]))])); i += 3
        elif t == "C":
            cur.append(("C", [(float(toks[i + k]), float(toks[i + k + 1])) for k in (1, 3, 5)])); i += 7
        else:
            i += 1
    return subs


class Collect(BasePen):
    def __init__(self, gs):
        super().__init__(gs); self.subs = []; self.cur = None

    def _moveTo(self, p):
        self.cur = [("M", [p])]; self.subs.append(self.cur)

    def _lineTo(self, p):
        self.cur.append(("L", [p]))

    def _curveToOne(self, a, b, c):
        self.cur.append(("C", [a, b, c]))

    def _qCurveToOne(self, a, b):
        p0 = self._getCurrentPoint()
        c1 = (p0[0] + 2 / 3 * (a[0] - p0[0]), p0[1] + 2 / 3 * (a[1] - p0[1]))
        c2 = (b[0] + 2 / 3 * (a[0] - b[0]), b[1] + 2 / 3 * (a[1] - b[1]))
        self.cur.append(("C", [c1, c2, b]))

    def _closePath(self):
        pass


_FONT = None


def glyph(ch):
    global _FONT
    if _FONT is None:
        f = TTFont(FONT)
        _FONT = instantiateVariableFont(f, {"wght": 900, "opsz": 60})
    gs = _FONT.getGlyphSet()
    name = _FONT.getBestCmap()[ord(ch)]
    pen = Collect(gs); gs[name].draw(pen)
    pts = [p for s in pen.subs for _, ps in s for p in ps]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    bbox = (min(xs), min(ys), max(xs), max(ys))
    # flip y (font units y-up) into a 0..w, 0..h box
    subs = [[(op, [(x - bbox[0], bbox[3] - y) for x, y in ps]) for op, ps in s] for s in pen.subs]
    return subs, (bbox[2] - bbox[0], bbox[3] - bbox[1])


def place(subs, src_w, src_h, x, y, h, rot180=False, cx=W / 2, cy=H / 2):
    """Scale a shape to height h with its top-left at (x, y); optional 180 deg rotation about the card centre."""
    s = h / src_h
    out = []
    for sub in subs:
        ns = []
        for op, ps in sub:
            q = []
            for px, py in ps:
                X, Y = x + px * s, y + py * s
                if rot180:
                    X, Y = 2 * cx - X, 2 * cy - Y
                q.append((X, Y))
            ns.append((op, q))
        out.append(ns)
    return out, src_w * s


def to_d(subs):
    parts = []
    for sub in subs:
        for op, ps in sub:
            parts.append(op + " ".join(f"{x:.2f} {y:.2f}" for x, y in ps))
        parts.append("Z")
    return "".join(parts)


def flatten(subs, n=24):
    polys = []
    for sub in subs:
        pts = []
        for op, ps in sub:
            if op in ("M", "L"):
                pts.append(ps[0])
            else:
                p0 = pts[-1]; p1, p2, p3 = ps
                for t in np.linspace(0, 1, n)[1:]:
                    u = 1 - t
                    pts.append((u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
                                u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1]))
        polys.append(pts)
    return polys


def card(kind):
    rank, suit = ("A", "spade") if kind == "ace" else ("K", "heart")
    col = BLACK if suit == "spade" else RED
    pip = parse(SPADE if suit == "spade" else HEART)
    g, (gw, gh) = glyph(rank)
    layers = []   # (subs, fill, stroke, stroke_w)
    # corner index top-left + rotated bottom-right
    for rot in (False, True):
        ix, _ = place(g, gw, gh, 24, 24, 50, rot)
        layers.append((ix, col, None, 0))
        pw = 34
        p, _ = place(pip, 100, 100, 24 + (50 * gw / gh - pw) / 2, 82, pw, rot)
        layers.append((p, col, INK if suit == "heart" else None, 2.2))
    # centre: large rank + pip
    bigh = 112
    bw = bigh * gw / gh
    big, _ = place(g, gw, gh, (W - bw) / 2 + 6, 108, bigh)
    layers.append((big, col, None, 0))
    pw = 58
    cp, _ = place(pip, 100, 100, (W - pw) / 2 + 6, 236, pw)
    layers.append((cp, col, INK, 3.0))
    return layers


def write_svg(kind, layers, path):
    els = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{"Ace of spades" if kind == "ace" else "King of hearts"}">',
           '<defs><clipPath id="c"><rect x="6" y="6" width="238" height="338" rx="22"/></clipPath></defs>',
           f'<rect x="6" y="6" width="238" height="338" rx="22" fill="{SHADE}"/>',
           f'<rect x="6" y="6" width="226" height="326" rx="20" fill="{CREAM}" clip-path="url(#c)"/>',
           f'<rect x="16" y="16" width="218" height="318" rx="14" fill="none" stroke="{RED if kind == "king" else BLACK}" stroke-opacity=".35" stroke-width="2"/>']
    for subs, fill, stroke, sw in layers:
        st = f' stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"' if stroke else ""
        els.append(f'<path fill="{fill}" fill-rule="nonzero"{st} d="{to_d(subs)}"/>')
    els.append(f'<rect x="5" y="5" width="240" height="340" rx="22" fill="none" stroke="{INK}" stroke-width="6"/>')
    els.append("</svg>\n")
    open(path, "w").write("".join(els))


def hexrgb(h, a=255):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)) + (a,)


def raster(kind, layers, scale, K=4):
    S = scale * K
    im = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    r = lambda v: v * S
    d.rounded_rectangle([r(6), r(6), r(244), r(344)], radius=r(22), fill=hexrgb(SHADE))
    cream = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(cream).rounded_rectangle([r(6), r(6), r(232), r(332)], radius=r(20), fill=hexrgb(CREAM))
    clip = Image.new("L", im.size, 0); ImageDraw.Draw(clip).rounded_rectangle([r(6), r(6), r(244), r(344)], radius=r(22), fill=255)
    cream.putalpha(Image.fromarray(np.minimum(np.array(cream.getchannel("A")), np.array(clip))))
    im.alpha_composite(cream)
    d = ImageDraw.Draw(im)
    bc = hexrgb(RED if kind == "king" else BLACK, int(255 * .35))
    border = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(border).rounded_rectangle([r(16), r(16), r(234), r(334)], radius=r(14), outline=bc, width=round(r(2)))
    im.alpha_composite(border)
    for subs, fill, stroke, sw in layers:
        polys = flatten(subs)
        wind = np.zeros((im.size[1], im.size[0]), np.int16)
        for p in polys:   # nonzero winding: each contour adds +1/-1 by its orientation
            area = sum(p[i][0] * p[(i + 1) % len(p)][1] - p[(i + 1) % len(p)][0] * p[i][1] for i in range(len(p)))
            t = Image.new("L", im.size, 0); ImageDraw.Draw(t).polygon([(x * S, y * S) for x, y in p], fill=1)
            wind += np.array(t).astype(np.int16) * (1 if area > 0 else -1)
        m = Image.fromarray(((wind != 0) * 255).astype(np.uint8))
        layer = Image.new("RGBA", im.size, hexrgb(fill)); layer.putalpha(m); im.alpha_composite(layer)
        if stroke:
            for p in polys:
                ImageDraw.Draw(im).line([(x * S, y * S) for x, y in p] + [(p[0][0] * S, p[0][1] * S)], fill=hexrgb(stroke), width=max(1, round(sw * S)), joint="curve")
    ImageDraw.Draw(im).rounded_rectangle([r(6), r(6), r(244), r(344)], radius=r(22), outline=hexrgb(INK), width=round(r(6)))
    return im.resize((W * scale, H * scale), Image.LANCZOS)


def main():
    os.makedirs(OUT, exist_ok=True)
    for kind in ("ace", "king"):
        L = card(kind)
        write_svg(kind, L, os.path.join(OUT, f"cards-{kind}.svg"))
        for sc in (1, 2):
            raster(kind, L, sc).save(os.path.join(OUT, f"cards-{kind}@{sc}x.png"), optimize=True)
    print("ok")


if __name__ == "__main__":
    main()
