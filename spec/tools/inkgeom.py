"""Per-note tilt + line pitch, per-headline-line baseline arc (radius, tilt), measured on board 3 ink."""
import json, os
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = os.path.join(os.path.dirname(__file__), "..")
NOTES = {  # chapter: (col, box, ink)
    "diet-cherry": (1, (80, 1105, 300, 1205), "white"),
    "brainwave": (2, (125, 105, 375, 230), "white"),
    "green-flag": (2, (70, 890, 305, 990), "white"),
    "shaadi-shift": (3, (55, 620, 335, 692), "white"),
    "on-me": (3, (95, 1385, 340, 1485), "black"),
    "wild-card": (4, (50, 35, 335, 105), "black"),
    "pinky-promise": (4, (25, 872, 388, 950), "white"),
}
HEADS = {
    "diet-cherry": (1, (60, 1200, 355, 1330), "white"),
    "brainwave": (2, (55, 240, 370, 355), "white"),
    "green-flag": (2, (30, 1005, 389, 1115), "white"),
    "shaadi-shift": (3, (55, 715, 370, 830), "white"),
    "on-me": (3, (35, 1510, 380, 1590), "black"),
    "wild-card": (4, (80, 100, 370, 235), "black"),
    "pinky-promise": (4, (65, 925, 365, 1065), "white"),
}


def ink(col, box, kind):
    a = np.array(Image.open(os.path.join(ROOT, "crops", f"landing-col{col}@390.png")).convert("RGB").crop(box)).astype(int)
    if kind == "white":
        m = (a.min(2) > 200) & ((a.max(2) - a.min(2)) < 60)
    else:
        m = a.max(2) < 70
    lab, n = ndimage.label(m)
    sz = ndimage.sum(m, lab, range(1, n + 1))
    keep = np.isin(lab, [i + 1 for i, s in enumerate(sz) if s >= 6])
    return keep


def best_angle(m):
    im = Image.fromarray((m * 255).astype(np.uint8))
    best = None
    for ang in np.arange(-22, 6, 0.5):
        r = np.array(im.rotate(-ang, resample=Image.BILINEAR, expand=True)) > 100
        p = r.sum(1).astype(float)
        score = (p ** 2).sum()
        if best is None or score > best[0]:
            best = (score, ang, r)
    return best[1], best[2]


def lines(r):
    p = ndimage.gaussian_filter1d(r.sum(1).astype(float), 2)
    thr = p.max() * 0.25
    on = p > thr
    runs, s = [], None
    for i, v in enumerate(list(on) + [False]):
        if v and s is None: s = i
        if not v and s is not None:
            if i - s > 4: runs.append((s, i))
            s = None
    # x-height band centre and core height per line
    out = []
    for a, b in runs:
        seg = p[a:b]; c = a + np.average(np.arange(len(seg)), weights=seg)
        core = (seg > seg.max() * 0.5).sum()
        out.append((round(float(c), 1), int(core), a, b))
    return out


def circle(p1, p2, p3):
    (x1, y1), (x2, y2), (x3, y3) = p1, p2, p3
    d = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
    if abs(d) < 1e-6: return float("inf")
    ux = ((x1**2 + y1**2) * (y2 - y3) + (x2**2 + y2**2) * (y3 - y1) + (x3**2 + y3**2) * (y1 - y2)) / d
    uy = ((x1**2 + y1**2) * (x3 - x2) + (x2**2 + y2**2) * (x1 - x3) + (x3**2 + y3**2) * (x2 - x1)) / d
    R = np.hypot(x1 - ux, y1 - uy)
    return R if uy > y2 else -R  # positive = convex up (centre below)


def head_lines(m):
    rows = m.sum(1)
    p = ndimage.gaussian_filter1d(rows.astype(float), 2)
    on = p > p.max() * 0.15
    runs, s = [], None
    for i, v in enumerate(list(on) + [False]):
        if v and s is None: s = i
        if not v and s is not None:
            if i - s > 10: runs.append((s, i))
            s = None
    res = []
    for a, b in runs:
        band = m[max(a - 6, 0):b + 6]
        xs = np.nonzero(band.any(0))[0]
        if len(xs) < 30: continue
        x0, x1 = xs.min(), xs.max()
        pts = []
        for fx in (0.08, 0.5, 0.92):
            cx = int(x0 + (x1 - x0) * fx)
            win = band[:, max(cx - 12, 0):cx + 12]
            # baseline ~ 85th percentile of ink rows in window (ignores descenders mostly)
            ys = np.nonzero(win)[0]
            if len(ys) == 0: continue
            pts.append((cx, float(np.percentile(ys, 85)) + max(a - 6, 0)))
        if len(pts) == 3:
            R = circle(*pts)
            tilt = np.degrees(np.arctan2(pts[2][1] - pts[0][1], pts[2][0] - pts[0][0]))
            sag = pts[1][1] - (pts[0][1] + pts[2][1]) / 2
            res.append({"width": int(x1 - x0), "baseline_pts": [[int(x), round(y, 1)] for x, y in pts],
                        "radius": round(float(R), 0) if np.isfinite(R) else None, "chord_tilt_deg": round(float(tilt), 1),
                        "sag_px": round(float(sag), 1)})
    return res


def main():
    out = {"notes": {}, "headlines": {}}
    for k, (col, box, kind) in NOTES.items():
        m = ink(col, box, kind)
        ang, r = best_angle(m)
        ls = lines(r)
        pitch = round(ls[1][0] - ls[0][0], 1) if len(ls) > 1 else None
        out["notes"][k] = {"tilt_deg": float(ang), "lines": len(ls), "line_pitch_px": pitch,
                           "x_core_px": [l[1] for l in ls]}
        print("note", k, out["notes"][k])
    for k, (col, box, kind) in HEADS.items():
        m = ink(col, box, kind)
        out["headlines"][k] = head_lines(m)
        print("head", k, out["headlines"][k])
    json.dump(out, open(os.path.join(ROOT, "landing-inkgeom.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
