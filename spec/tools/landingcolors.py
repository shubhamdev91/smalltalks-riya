import json, os
import numpy as np
from PIL import Image

ROOT = os.path.join(os.path.dirname(__file__), "..")
# section: (col, y0, y1, seed x, seed y)
SECTIONS = {
    "hero-on-me": (1, 69, 722, 370, 500),
    "tiles": (1, 722, 1062, 200, 1040),
    "chapter-diet-cherry": (1, 1062, 1700, 30, 1250),
    "talks-teaser": (1, 1700, 2264, 300, 1800),
    "chapter-brainwave": (2, 0, 850, 370, 250),
    "chapter-green-flag": (2, 850, 1715, 30, 1000),
    "journal-teaser": (2, 1715, 2387, 350, 1780),
    "nail-guide-teaser": (3, 0, 545, 30, 150),
    "chapter-shaadi-shift": (3, 545, 1320, 330, 640),
    "chapter-on-me": (3, 1320, 2387, 360, 1500),
    "chapter-wild-card": (4, 0, 850, 360, 240),
    "chapter-pinky-promise": (4, 850, 1715, 360, 950),
    "shop-all-faq-footer": (4, 1715, 2348, 30, 1780),
}


def hexc(c):
    return "#%02x%02x%02x" % tuple(int(round(v)) for v in c)


def main():
    out = {}
    for name, (col, y0, y1, sx, sy) in SECTIONS.items():
        a = np.array(Image.open(os.path.join(ROOT, "crops", f"landing-col{col}@390.png")).convert("RGB")).astype(float)
        seed = np.median(a[sy - 6:sy + 6, sx - 6:sx + 6].reshape(-1, 3), 0)
        sec = a[y0:y1]
        m = np.abs(sec - seed).sum(2) < 75
        px = sec[m]
        L = px.mean(1)
        lo, mid, hi = (px[(L >= np.percentile(L, p - 5)) & (L <= np.percentile(L, p + 5))].mean(0) for p in (8, 50, 92))
        ys, xs = np.nonzero(m)
        Lm = sec.mean(2)
        top = m & (Lm >= np.percentile(L, 90))
        ty, tx = np.nonzero(top)
        h = y1 - y0
        out[name] = {"col": col, "y_range_in_col": [y0, y1], "height_px": h, "ground": hexc(mid),
                     "glow_inner": hexc(hi), "glow_outer": hexc(lo),
                     "glow_centre_pct": [round(tx.mean() / 390 * 100), round(ty.mean() / h * 100)] if len(tx) else None,
                     "coverage": round(float(m.mean()), 2)}
        print(name, out[name])
    json.dump(out, open(os.path.join(ROOT, "landing-colours.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
