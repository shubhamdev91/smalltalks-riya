"""Arc-set headline comparison: glyphs on a circle (convex up), fitted to the board text width."""
import math, os, sys
import numpy as np
from PIL import Image, ImageDraw
from typecompare import font, CANDS, fgbg, mask_of, K
from samples import SAMPLES, load

T = os.path.join(os.path.dirname(__file__), "..", "type")


def arc_text(text, f, track, R, rot=0.0):
    """Return L image: text centred on an arc of radius R (px), centre below the text."""
    advs = [f.getlength(c) + track for c in text]
    total = sum(advs) - track
    size = int(f.size * 3 + total)
    im = Image.new("L", (size * 2, size * 2), 0)
    cx, cy = size, size + R
    s = -total / 2
    for c, a in zip(text, advs):
        mid = s + f.getlength(c) / 2
        th = mid / R  # radians along arc
        g = Image.new("L", (int(f.size * 2), int(f.size * 2)), 0)
        ImageDraw.Draw(g).text((f.size * 0.5, f.size * 0.2), c, font=f, fill=255)
        gw = f.getlength(c)
        # glyph baseline point inside g: (f.size*0.5 + gw/2, f.size*0.2 + ascent)
        asc = f.getmetrics()[0]
        bx, by = f.size * 0.5 + gw / 2, f.size * 0.2 + asc
        gr = g.rotate(-math.degrees(th), resample=Image.BICUBIC, center=(bx, by))
        px = cx + R * math.sin(th)
        py = cy - R * math.cos(th)
        im.paste(255, (int(px - bx), int(py - by)), gr)
        s += a
    if rot:
        im = im.rotate(-rot, resample=Image.BICUBIC)
    m = np.array(im) > 127
    ys, xs = np.nonzero(m)
    return im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))


def main(R=520, rot=-3):
    src, box, text, note = SAMPLES["headline"]
    crop = load(src).crop(box)
    crop = crop.resize((crop.width * K, crop.height * K), Image.LANCZOS)
    a = np.array(crop).astype(float)
    fg, bg = fgbg(a)
    bm = mask_of(a, fg, bg)
    ys, xs = np.nonzero(bm)
    tw, th = xs.max() - xs.min() + 1, ys.max() - ys.min() + 1
    rows = [("BOARD", crop, "")]
    res = []
    for name, path, axes in CANDS["headline"]:
        best = None
        for track_em in (-0.06, -0.04, -0.02, 0.0):
            lo, hi = 10, 600
            while lo < hi:
                sz = (lo + hi) // 2
                f = font(path, sz, **axes)
                if arc_text(text, f, track_em * sz, R * K, rot).width < tw:
                    lo = sz + 1
                else:
                    hi = sz
            f = font(path, lo, **axes)
            L = arc_text(text, f, track_em * lo, R * K, rot)
            canvas = Image.new("RGB", crop.size, tuple(int(v) for v in bg))
            canvas.paste(Image.new("RGB", L.size, tuple(int(v) for v in fg)), (int(xs.min()), int(ys.max() - L.height + 1)), L)
            cm = np.zeros(bm.shape, bool)
            Lm = np.array(L) > 127
            y0 = int(ys.max() - L.height + 1)
            yy0, yy1 = max(y0, 0), min(y0 + L.height, cm.shape[0])
            xx0 = int(xs.min()); xx1 = min(xx0 + L.width, cm.shape[1])
            cm[yy0:yy1, xx0:xx1] = Lm[yy0 - y0:yy1 - y0, :xx1 - xx0]
            iou = (bm & cm).sum() / (bm | cm).sum()
            if best is None or iou > best[0]:
                best = (iou, track_em, lo, canvas, L.height)
        iou, tr, sz, canvas, hh = best
        res.append((name, round(iou, 3), tr, round(sz / K, 1), hh / K))
        rows.append((f"{name}  arc R={R}px@390  IoU {iou:.3f}  size ~{sz / K:.0f}px@390  tracking {tr:+.2f}em  ink h {hh / K:.0f} vs board {th / K:.0f}", canvas, ""))
    W = max(r[1].width for r in rows)
    sheet = Image.new("RGB", (W, sum(r[1].height + 30 for r in rows)), "white")
    d = ImageDraw.Draw(sheet); y = 0
    for lab, im, _ in rows:
        d.text((4, y + 6), lab, fill="black"); sheet.paste(im, (0, y + 24)); y += im.height + 30
    sheet.save(os.path.join(T, "compare-headline.png"))
    for r in res:
        print(r)


if __name__ == "__main__":
    main(*(float(x) for x in sys.argv[1:]))
