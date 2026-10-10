"""Wild Card hint cards v2 (st-fable spec, qa/desktop/owner-v12/README.md section D): ace of spades + king of hearts,
viewBox 0 0 46 64, face #fffdf6, rx 4.5, 1.2 ink outline. Flat, no ids/<use>/text so both can be inlined on one page.
Rank glyphs are Source Serif 4 Black outlines (shared with cards_svg.py); pips are the cards_svg Bezier pips.
Same geometry -> SVG paths and a Pillow raster (nonzero winding) for the contact sheet."""
import math, os, sys
import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(__file__))
import cards_svg as base

OUT = os.path.join(base.ART, "hd", "wild-card")
W, H = 46, 64
CX, CY = W / 2, H / 2
FACE, INK, RED = "#fffdf6", "#1a1410", "#c3021d"
OUTLINE = 1.2
RANK_H, RANK_X, RANK_Y = 10.5, 3.6, 3.8
PIP_H, PIP_GAP = 7.0, 1.3

# crown (king centre art, optional): 3 points with ball tips, on a band; drawn in a 100 x 60 box
CROWN = ("M6 52 L2 14 L28 34 L50 6 L72 34 L98 14 L94 52 Z")


def bbox(subs):
    pts = [p for s in subs for _, ps in s for p in ps]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)


def fit(subs, x, y, h=None, w=None, rot=False):
    """Scale the shape's tight bbox to height h (or width w), top-left at (x, y); optional 180 deg about the card centre."""
    x0, y0, x1, y1 = bbox(subs)
    s = h / (y1 - y0) if h else w / (x1 - x0)
    out = []
    for sub in subs:
        ns = []
        for op, ps in sub:
            q = []
            for px, py in ps:
                X, Y = x + (px - x0) * s, y + (py - y0) * s
                if rot:
                    X, Y = 2 * CX - X, 2 * CY - Y
                q.append((X, Y))
            ns.append((op, q))
        out.append(ns)
    return out, (x1 - x0) * s, (y1 - y0) * s


def circle(cx, cy, r):
    k = 0.5523 * r
    return [[("M", [(cx + r, cy)]), ("C", [(cx + r, cy + k), (cx + k, cy + r), (cx, cy + r)]),
             ("C", [(cx - k, cy + r), (cx - r, cy + k), (cx - r, cy)]), ("C", [(cx - r, cy - k), (cx - k, cy - r), (cx, cy - r)]),
             ("C", [(cx + k, cy - r), (cx + r, cy - k), (cx + r, cy)])]]


def card(kind, crown=True):
    rank, pipd, col = ("A", base.SPADE, INK) if kind == "ace" else ("K", base.HEART, RED)
    g, _ = base.glyph(rank)
    pip = base.parse(pipd)
    shapes = []
    for rot in (False, True):
        r, rw, rh = fit(g, RANK_X, RANK_Y, h=RANK_H, rot=rot)
        shapes += r
        p0 = fit(pip, 0, 0, h=PIP_H)
        pw = p0[1]
        p, _, _ = fit(pip, RANK_X + rw / 2 - pw / 2, RANK_Y + RANK_H + PIP_GAP, h=PIP_H, rot=rot)
        shapes += p
    if kind == "ace":
        cw = 21.0
        _, _, ch = fit(pip, 0, 0, w=cw)
        c, _, _ = fit(pip, CX - cw / 2, CY - ch / 2 - 0.4, w=cw)
        shapes += c
    else:
        cw = 17.0 if crown else 19.0
        _, _, ch = fit(pip, 0, 0, w=cw)
        if crown:
            crw = 13.0
            cr0 = base.parse(CROWN)
            _, _, crh = fit(cr0, 0, 0, w=crw)
            top = CY - (crh + 1.4 + ch) / 2
            cr, _, _ = fit(cr0, CX - crw / 2, top, w=crw)
            shapes += cr
            # ball tips on the three points
            s = crw / 96
            for tx, ty in ((2, 14), (50, 6), (98, 14)):
                shapes += circle(CX - crw / 2 + (tx - 2) * s, top + (ty - 6) * s, 1.05)
            c, _, _ = fit(pip, CX - cw / 2, top + crh + 1.4, w=cw)
        else:
            c, _, _ = fit(pip, CX - cw / 2, CY - ch / 2, w=cw)
        shapes += c
    return shapes, col


def d_str(subs):
    f = lambda v: f"{v:.1f}".rstrip("0").rstrip(".") if abs(v - round(v)) > 1e-9 else str(int(round(v)))
    out = []
    for sub in subs:
        last = None
        for op, ps in sub:
            nums = " ".join(f"{f(x)} {f(y)}" for x, y in ps)
            out.append((op if op != last or op == "M" else " ") + nums)
            last = op
        out.append("Z")
    return "".join(out).replace(" -", "-")


def svg(kind, crown=True):
    shapes, col = card(kind, crown)
    label = "Ace of spades" if kind == "ace" else "King of hearts"
    i = OUTLINE / 2
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="{label}">'
            f'<rect x="{i}" y="{i}" width="{W - OUTLINE:.1f}" height="{H - OUTLINE:.1f}" rx="4.5" fill="{FACE}" stroke="{INK}" stroke-width="{OUTLINE}"/>'
            f'<path fill="{col}" d="{d_str(shapes)}"/></svg>\n')


def hexrgb(h, a=255):
    return tuple(int(h[k:k + 2], 16) for k in (1, 3, 5)) + (a,)


def raster(kind, px_w, crown=True, K=8):
    """Render at px_w css px wide (1x) using the same geometry; K x supersampling."""
    shapes, col = card(kind, crown)
    S = px_w / W * K
    im = Image.new("RGBA", (round(W * S), round(H * S)), (0, 0, 0, 0))
    i = OUTLINE / 2
    ImageDraw.Draw(im).rounded_rectangle([i * S, i * S, (W - i) * S, (H - i) * S], radius=4.5 * S, fill=hexrgb(FACE))
    wind = np.zeros((im.size[1], im.size[0]), np.int16)
    for p in base.flatten(shapes, 32):
        area = sum(p[k][0] * p[(k + 1) % len(p)][1] - p[(k + 1) % len(p)][0] * p[k][1] for k in range(len(p)))
        t = Image.new("L", im.size, 0); ImageDraw.Draw(t).polygon([(x * S, y * S) for x, y in p], fill=1)
        wind += np.array(t).astype(np.int16) * (1 if area > 0 else -1)
    lay = Image.new("RGBA", im.size, hexrgb(col)); lay.putalpha(Image.fromarray(((wind != 0) * 255).astype(np.uint8)))
    im.alpha_composite(lay)
    # outline: stroke centred on the inset rect -> outer edge at 0, inner edge at OUTLINE
    ring = Image.new("L", im.size, 0); dr = ImageDraw.Draw(ring)
    dr.rounded_rectangle([0, 0, W * S - 1, H * S - 1], radius=(4.5 + i) * S, fill=255)
    dr.rounded_rectangle([OUTLINE * S, OUTLINE * S, (W - OUTLINE) * S - 1, (H - OUTLINE) * S - 1], radius=(4.5 - i) * S, fill=0)
    ol = Image.new("RGBA", im.size, hexrgb(INK)); ol.putalpha(ring); im.alpha_composite(ol)
    return im.resize((round(W * S / K), round(H * S / K)), Image.LANCZOS)


def clearance(kind, crown=True):
    """Min gap (card units) between the centre art and either index, on the flattened outlines."""
    shapes, _ = card(kind, crown)
    n_idx = len(base.glyph("A" if kind == "ace" else "K")[0]) + 1
    polys = base.flatten(shapes, 32)
    idx = polys[:2 * n_idx]; centre = polys[2 * n_idx:]
    A = np.array([p for q in idx for p in q]); B = np.array([p for q in centre for p in q])
    return float(np.min(np.hypot(A[:, None, 0] - B[None, :, 0], A[:, None, 1] - B[None, :, 1])))


def main():
    os.makedirs(OUT, exist_ok=True)
    for kind, name in (("ace", "st-card-ace-spades.svg"), ("king", "st-card-king-hearts.svg")):
        s = svg(kind)
        open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\n").write(s)
        print(name, len(s.encode()), "bytes; clearance", round(clearance(kind), 2))
    # plain-heart king kept as an alternate for st-fable
    s = svg("king", crown=False)
    os.makedirs(os.path.join(OUT, "alt"), exist_ok=True)
    open(os.path.join(OUT, "alt", "st-card-king-hearts-plain.svg"), "w", encoding="utf-8", newline="\n").write(s)
    print("plain king", len(s.encode()), "bytes; clearance", round(clearance("king", False), 2))


if __name__ == "__main__":
    main()
