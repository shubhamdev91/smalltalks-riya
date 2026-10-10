"""Per-cell geometry of nail sprite sheets (alpha>128): bbox, width/height fractions, base y at the cell centre
column, lowest opaque y, bbox centre x. Usage: nail_cells_table.py <dir> <cellW> <cellH> [--json out]"""
import json, os, sys
import numpy as np
from PIL import Image

SETS = ["on-me", "brainwave", "diet-cherry", "green-flag", "shaadi-shift", "wild-card", "pinky-promise"]


def cell_stats(a, cw, ch):
    m = a[..., 3] > 128
    ys, xs = np.nonzero(m)
    x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
    cx = (x0 + x1) / 2
    col = np.nonzero(m[:, int(round(cx)) - 2:int(round(cx)) + 3].any(1))[0]
    return {"w": round((x1 - x0) / cw, 4), "h": round((y1 - y0) / ch, 4), "top": round(y0 / ch, 4),
            "base_centre": round((col.max() + 1) / ch, 4), "base_lowest": round(y1 / ch, 4), "cx": round(cx / cw, 4),
            "px": [int(x0), int(y0), int(x1), int(y1)]}


def table(d, cw, ch):
    out = {}
    for st in SETS:
        sh = np.array(Image.open(os.path.join(d, f"{st}.webp")).convert("RGBA"))
        out[st] = [cell_stats(sh[:, k * cw:(k + 1) * cw], cw, ch) for k in range(sh.shape[1] // cw)]
    return out


if __name__ == "__main__":
    d, cw, ch = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    t = table(d, cw, ch)
    print(f"{'set':14s} col  width   height  top     base(ctr) base(low) cx")
    for st, cells in t.items():
        for k, c in enumerate(cells):
            print(f"{st:14s} {k}    {c['w']:.3f}   {c['h']:.3f}   {c['top']:.3f}   {c['base_centre']:.3f}     {c['base_lowest']:.3f}     {c['cx']:.3f}")
    if "--json" in sys.argv:
        json.dump(t, open(sys.argv[sys.argv.index("--json") + 1], "w"), indent=1)
