"""Sample hero colours per frame from the @390 crops: header, scene ground + radial glow, pill, buttons."""
import glob, json, os
import numpy as np
from PIL import Image

C = os.path.join(os.path.dirname(__file__), "..", "crops")
HDR = 69  # header height in the @390 crops (48 board px * 390/271)


def hexc(c):
    return "#%02x%02x%02x" % tuple(min(255, int(round(v))) for v in c)


def main():
    out = {}
    for p in sorted(glob.glob(os.path.join(C, "hero-*@390.png"))):
        name = os.path.basename(p)[5:-8]
        a = np.array(Image.open(p).convert("RGB")).astype(float)
        H, W = a.shape[:2]
        hdr = a[3:HDR - 3]
        hdr_bg = np.median(hdr.reshape(-1, 3), 0)
        sc = a[HDR + 2:]
        q = (sc // 16).astype(int)
        key = q[..., 0] * 256 + q[..., 1] * 16 + q[..., 2]
        sat = (sc.max(2) - sc.min(2)) > 80
        dom = np.bincount(key[sat].ravel()).argmax()
        domc = np.array([dom // 256, (dom // 16) % 16, dom % 16]) * 16 + 8
        dist = np.abs(sc - domc).sum(2)
        bg = dist < 90
        L = sc.mean(2)
        Lb = np.where(bg, L, np.nan)
        # glow: brightest 8% of ground pixels -> centroid
        thr = np.nanpercentile(Lb, 92)
        ys, xs = np.nonzero(bg & (L >= thr))
        cy, cx = ys.mean(), xs.mean()
        inner = sc[bg & (L >= thr)].mean(0)
        outer = sc[bg & (L <= np.nanpercentile(Lb, 8))].mean(0)
        mid = sc[bg].mean(0) if bg.any() else domc
        # radius where ground luminance crosses halfway between inner and outer
        yy, xx = np.nonzero(bg)
        r = np.hypot(yy - cy, xx - cx)
        lv = L[bg]
        half = (inner.mean() + outer.mean()) / 2
        bins = np.arange(0, r.max() + 20, 20)
        prof = [lv[(r >= b) & (r < b + 20)].mean() if ((r >= b) & (r < b + 20)).any() else np.nan for b in bins]
        rad = next((b for b, v in zip(bins, prof) if v < half), None)
        # pill: bottom band, take the most common non-ground colour in rows H-80..H-30 centre area
        band = a[H - 80:H - 30, 60:330].reshape(-1, 3)
        bq = (band // 12).astype(int)
        bk = bq[:, 0] * 10000 + bq[:, 1] * 100 + bq[:, 2]
        vals, cnt = np.unique(bk, return_counts=True)
        order = np.argsort(cnt)[::-1]
        cols = [np.array([v // 10000, (v // 100) % 100, v % 100]) * 12 + 6 for v in vals[order[:4]]]
        out[name] = {"frame_px": [W, H], "header_bg": hexc(hdr_bg), "ground_dominant": hexc(domc), "ground_mean": hexc(mid),
                     "glow": {"centre_pct": [round(cx / W * 100, 1), round((cy + HDR + 2) / H * 100, 1)],
                              "inner": hexc(inner), "outer": hexc(outer), "radius_px_at390": rad},
                     "pill_band_top_colours": [hexc(c) for c in cols]}
        print(name, json.dumps(out[name]))
    json.dump(out, open(os.path.join(C, "..", "hero-colours.json"), "w"), indent=2)


if __name__ == "__main__":
    main()

