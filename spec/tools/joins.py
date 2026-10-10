"""Trace section joins (colour boundary per x) and dashed beelines (dash-shaped blobs) on landing columns."""
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage, signal

C = os.path.join(os.path.dirname(__file__), "..", "crops")

# (col, name, y_lo, y_hi, upper colour sample (x,y), lower colour sample (x,y))
JOINS = [
    (1, "hero-to-tiles", 690, 760, (370, 690), (200, 745)),
    (1, "tiles-to-diet-cherry", 1030, 1120, (200, 1045), (200, 1110)),
    (1, "diet-cherry-to-talks", 1600, 1780, (330, 1470), (200, 1770)),
    (2, "brainwave-to-green-flag", 790, 900, (330, 600), (330, 900)),
    (2, "green-flag-to-journal", 1660, 1760, (200, 1690), (200, 1760)),
    (3, "nail-guide-to-shaadi", 500, 600, (100, 470), (200, 600)),
    (3, "shaadi-to-on-me", 1260, 1360, (200, 1230), (200, 1380)),
    (4, "wild-card-to-pinky", 800, 900, (200, 790), (200, 900)),
    (4, "pinky-to-shop-all", 1680, 1770, (300, 1690), (20, 1745)),
]


def hexc(c):
    return "#%02x%02x%02x" % tuple(int(v) for v in c)


def trace(a, ylo, yhi, up, lo, thr=70):
    cu = np.median(a[up[1] - 6:up[1] + 6, up[0] - 6:up[0] + 6].reshape(-1, 3), 0)
    cl = np.median(a[lo[1] - 6:lo[1] + 6, lo[0] - 6:lo[0] + 6].reshape(-1, 3), 0)
    ys = []
    for x in range(a.shape[1]):
        col = a[ylo:yhi, x]
        dl = np.abs(col - cl).sum(1)
        isl = dl < thr
        # first y from which >=80% of the next 12 px are lower colour
        run = np.convolve(isl.astype(float), np.ones(12) / 12, mode="valid")
        k = np.argmax(run >= 0.8) if (run >= 0.8).any() else -1
        ys.append(ylo + k if k >= 0 else np.nan)
    ys = np.array(ys, float)
    good = ~np.isnan(ys)
    # robust: median filter then reject points far from a rolling median
    if good.sum() > 20:
        med = ndimage.median_filter(np.where(good, ys, np.nanmedian(ys)), size=41, mode="nearest")
        bad = ~good | (np.abs(ys - med) > 14)
        ys[bad] = med[bad]
        ys = ndimage.gaussian_filter1d(ys, 6)
    return ys, cu, cl


def bezier_path(xs, ys, h_off):
    """Catmull-Rom through samples every 39 px -> cubic Bezier SVG path, y relative to h_off."""
    pts = [(float(x), float(y - h_off)) for x, y in zip(xs, ys)]
    d = f"M{pts[0][0]:.0f},{pts[0][1]:.1f}"
    for i in range(len(pts) - 1):
        p0 = pts[i - 1] if i else pts[i]; p1 = pts[i]; p2 = pts[i + 1]; p3 = pts[i + 2] if i + 2 < len(pts) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{c1[0]:.0f},{c1[1]:.1f} {c2[0]:.0f},{c2[1]:.1f} {p2[0]:.0f},{p2[1]:.1f}"
    return d


def dashes(a, mode):
    """Dash blobs: white-on-colour ('white') or red-on-cream ('red'). Returns list of (cx,cy,len,angle)."""
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    if mode == "white":
        m = (a.min(2) > 215) & ((a.max(2) - a.min(2)) < 40)
    else:
        m = (r > 150) & (g < 110) & (b < 120) & (r - g > 70)
    lab, n = ndimage.label(m)
    out = []
    for i, sl in enumerate(ndimage.find_objects(lab)):
        comp = lab[sl] == i + 1
        area = comp.sum()
        if not 10 <= area <= 90:
            continue
        ys, xs = np.nonzero(comp)
        P = np.stack([xs, ys], 1).astype(float)
        if len(P) < 5:
            continue
        cov = np.cov((P - P.mean(0)).T)
        w, v = np.linalg.eigh(cov)
        if w[0] <= 0:
            w[0] = 1e-3
        elong = np.sqrt(w[1] / w[0])
        L = 4 * np.sqrt(w[1])
        if elong < 2.6 or not 7 <= L <= 22:
            continue
        ang = np.degrees(np.arctan2(v[1, 1], v[0, 1]))
        out.append((P[:, 0].mean() + sl[1].start, P[:, 1].mean() + sl[0].start, L, ang))
    return out


def main():
    res = {"joins": {}, "dashes": {}}
    for col in range(1, 5):
        im = Image.open(os.path.join(C, f"landing-col{col}@390.png")).convert("RGB")
        a = np.array(im).astype(float)
        vis = im.copy(); d = ImageDraw.Draw(vis)
        for (c, name, ylo, yhi, up, lo) in [j for j in JOINS if j[0] == col]:
            ys, cu, cl = trace(a, ylo, yhi, up, lo, 22 if name == "diet-cherry-to-talks" else 70)
            xs = np.arange(0, 391, 39); xs[-1] = 389
            yk = ys[xs]
            top = float(np.floor(yk.min())) - 2
            path = bezier_path(xs, yk, top)
            h = float(np.ceil(yk.max() - top)) + 2
            res["joins"][name] = {"col": col, "y_top_in_col": top, "viewBox": f"0 0 390 {h:.0f}", "path_edge": path,
                                  "fill_lower_shape": path + f" L390,{h:.0f} L0,{h:.0f} Z",
                                  "upper": hexc(cu), "lower": hexc(cl),
                                  "amplitude_px": round(float(yk.max() - yk.min()), 1)}
            d.line(list(zip(range(390), ys[:390])), fill=(0, 255, 0), width=2)
        for mode, colr in (("white", (255, 0, 255)), ("red", (0, 200, 255))):
            ds = dashes(a, mode)
            res["dashes"][f"col{col}-{mode}"] = [[round(x, 1), round(y, 1), round(L, 1), round(t, 0)] for x, y, L, t in ds]
            for x, y, L, t in ds:
                d.ellipse([x - 4, y - 4, x + 4, y + 4], outline=colr, width=2)
        vis.save(os.path.join(C, f"landing-col{col}-traced.png"))
    json.dump(res, open(os.path.join(C, "..", "landing-geometry.json"), "w"), indent=1)
    for k, v in res["joins"].items():
        print(k, v["viewBox"], v["upper"], v["lower"], v["amplitude_px"])
    for k, v in res["dashes"].items():
        print(k, len(v), "dashes; median len", np.median([q[2] for q in v]) if v else None)


if __name__ == "__main__":
    main()


