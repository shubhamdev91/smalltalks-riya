"""Re-measure chapter nail rows, product name and pill boxes on board-3 columns (css px at 390)."""
import json, os
import numpy as np
from PIL import Image
from scipy import ndimage

C = os.path.join(os.path.dirname(__file__), "..", "crops")
CH = {  # name: (col, y0, y1, ground seed (x,y))
    "diet-cherry": (1, 1062, 1700, (30, 1250)),
    "brainwave": (2, 0, 850, (370, 250)),
    "green-flag": (2, 850, 1715, (30, 1000)),
    "shaadi-shift": (3, 545, 1320, (330, 640)),
    "on-me": (3, 1320, 2387, (360, 1500)),
    "wild-card": (4, 0, 850, (360, 240)),
    "pinky-promise": (4, 850, 1715, (360, 950)),
}


def main():
    out = {}
    for n, (col, y0, y1, (sx, sy)) in CH.items():
        a = np.array(Image.open(os.path.join(C, f"landing-col{col}@390.png")).convert("RGB")).astype(int)
        sec = a[y0:y1]
        g = np.median(a[sy - 5:sy + 5, sx - 5:sx + 5].reshape(-1, 3), 0)
        nonground = np.abs(sec - g).sum(2) > 110
        # nail row: rows where 5 separate blobs span x 20-370
        cand = []
        for y in range(sec.shape[0]):
            row = nonground[y, 15:375]
            lab, k = ndimage.label(row)
            if k >= 5:
                sizes = ndimage.sum(row, lab, range(1, k + 1))
                if (sizes > 25).sum() == 5:
                    cand.append(y)
        cand = np.array(cand)
        if len(cand):
            # longest consecutive run
            runs = np.split(cand, np.nonzero(np.diff(cand) > 3)[0] + 1)
            r = max(runs, key=len)
            ny0, ny1 = int(r[0]) + y0, int(r[-1]) + y0
        else:
            ny0 = ny1 = None
        # pill: white rows (>85% of a 150px centred span white) below the nail row
        white = (sec.min(2) > 225)
        py = [y for y in range(sec.shape[0]) if white[y, 120:270].mean() > 0.6 and (ny1 is None or y + y0 > ny1 + 20)]
        if py:
            runs = np.split(np.array(py), np.nonzero(np.diff(py) > 2)[0] + 1)
            r = max(runs, key=len)
            p0, p1 = int(r[0]) + y0, int(r[-1]) + y0
            wr = white[(p0 + p1) // 2 - y0]
            xs = np.nonzero(wr)[0]
            mid = xs[(xs > 60) & (xs < 330)]
            px0, px1 = int(mid.min()), int(mid.max())
        else:
            p0 = p1 = px0 = px1 = None
        # name text: rows between nails bottom and pill top with text ink
        name = None
        if ny1 and p0:
            band = nonground[ny1 - y0 + 6:p0 - y0 - 4, 80:310]
            rows = np.nonzero(band.mean(1) > 0.03)[0]
            if len(rows):
                name = [int(rows[0]) + ny1 + 6, int(rows[-1]) + ny1 + 6]
        out[n] = {"col": col, "nails_y": [ny0, ny1], "name_y": name, "pill": [px0, p0, px1, p1]}
        print(n, out[n])
    json.dump(out, open(os.path.join(C, "..", "landing-remeasure.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
