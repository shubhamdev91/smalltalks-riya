"""Verify RGB on fully-opaque pixels equals the source atlas (after placement), per cell."""
import io, json, os
import numpy as np
from PIL import Image
from scipy import ndimage
from stlib import load
import nails as N

ROOT = os.path.join(os.path.dirname(__file__), "..")


def match_delta(out_rgba, src_rgba):
    """Find src nail inside out by brute alignment of alpha bbox, return max/mean |dRGB| on opaque px."""
    o = out_rgba
    ys, xs = np.nonzero(o[..., 3] == 255)
    best = None
    sy, sx = np.nonzero(src_rgba[..., 3] >= 232)
    # align by bbox of high-alpha regions
    dy, dx = ys.min() - sy.min(), xs.min() - sx.min()
    for ddy in (-1, 0, 1):
        for ddx in (-1, 0, 1):
            yy, xx = ys - dy - ddy, xs - dx - ddx
            ok = (yy >= 0) & (yy < src_rgba.shape[0]) & (xx >= 0) & (xx < src_rgba.shape[1])
            d = np.abs(o[ys[ok], xs[ok], :3].astype(int) - src_rgba[yy[ok], xx[ok], :3].astype(int))
            r = (d.max(), d.mean(), (d.max(1) == 0).mean())
            if best is None or r[1] < best[1]:
                best = r
    return best


def main():
    ov = load("desi-nail-overlays.png")
    lab, n = ndimage.label(ov[..., 3] > 128, structure=np.ones((3, 3)))
    objs = [o for i, o in enumerate(ndimage.find_objects(lab))
            if (lab[o] == i + 1).sum() > 5000]
    objs.sort(key=lambda s: ((s[0].start > 300), s[1].start))
    m = json.load(open(os.path.join(ROOT, "nails", "manifest.json")))
    W = m["cell"]["width"]
    for i, h in enumerate(m["sets"]):
        sheet = np.array(Image.open(os.path.join(ROOT, "nails", f"{h}.webp")).convert("RGBA"))
        res = []
        for col in (0, 1):
            o = objs[col * 7 + i]
            src = ov[o[0].start - 6:o[0].stop + 6, o[1].start - 6:o[1].stop + 6]
            res.append(match_delta(sheet[:, col * W:(col + 1) * W], src))
        print(h, ["max %d mean %.3f identical %.1f%%" % (a, b, c * 100) for a, b, c in res])
    ft = load("desi-finger-tones.png")
    for k in range(4):
        t = np.array(Image.open(os.path.join(ROOT, "fingers", f"tone-{k + 1}.webp")).convert("RGBA"))
        x0 = [115, 514, 905, 1299][k]
        src = ft[100:, x0 - 10:x0 + 300]
        a, b, c = match_delta(t, src)
        print("tone", k + 1, "max %d mean %.3f identical %.1f%%" % (a, b, c * 100))


if __name__ == "__main__":
    main()
