"""Measure the natural nail plate on the HD finger tones: cuticle point (proximal edge of the plate on the
finger axis), plate width, tip; write hd/fingers/geometry.json and an overlay sheet."""
import json, os
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

ART = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))


def measure(k):
    a = np.array(Image.open(os.path.join(ART, "hd", "fingers", f"tone-{k}.webp")).convert("RGBA")).astype(float)
    H, W = a.shape[:2]
    r, g, b, al = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
    br = b / np.maximum(r, 1)
    # plate: pinkish-neutral (high b/r) and light; skin is orange (low b/r)
    plate = (al > 250) & (br > 0.62) & (r > 150)
    plate[int(H * 0.45):] = False
    plate = ndimage.binary_opening(plate, iterations=2)
    lab, n = ndimage.label(plate)
    seed = lab[int(H * 0.13), W // 2]
    if seed == 0:
        sz = ndimage.sum(plate, lab, range(1, n + 1)); seed = int(np.argmax(sz)) + 1
    m = ndimage.binary_fill_holes(ndimage.binary_closing(lab == seed, iterations=6))
    ys, xs = np.nonzero(m)
    cx = int(round(np.median(xs)))
    col = np.nonzero(m[:, cx - 3:cx + 4].any(1))[0]
    cut_y = int(col.max())          # proximal edge of the plate on the centre column
    tip_y = int(col.min())
    widths = m.sum(1)
    wmax = int(widths.max()); wy = int(np.argmax(widths))
    # finger silhouette width at the cuticle line
    fw = int((al[cut_y] > 128).sum())
    return {"tone": k, "canvas": [W, H], "plate_bbox": [int(xs.min()), tip_y, int(xs.max()), cut_y],
            "cuticle": {"x": round(cx / W, 4), "y": round(cut_y / H, 4), "px": [cx, cut_y]},
            "plate_width_px": wmax, "plate_width_frac": round(wmax / W, 4), "plate_widest_y": wy,
            "finger_width_at_cuticle_px": fw, "mask": m}


def main():
    res = [measure(k) for k in range(1, 5)]
    tiles = []
    for r in res:
        im = Image.open(os.path.join(ART, "hd", "fingers", f"tone-{r['tone']}.webp")).convert("RGBA")
        bg = Image.new("RGBA", im.size, (7, 61, 241, 255)); bg.alpha_composite(im)
        ov = np.array(bg.convert("RGB")); edge = r["mask"] ^ ndimage.binary_erosion(r["mask"], iterations=2)
        ov[edge] = [0, 255, 255]
        o = Image.fromarray(ov); d = ImageDraw.Draw(o)
        x, y = r["cuticle"]["px"]; d.line([(x - 40, y), (x + 40, y)], fill=(255, 0, 255), width=3)
        tiles.append(o.crop((0, 0, im.width, int(im.height * 0.42))))
    s = Image.new("RGB", (sum(t.width + 6 for t in tiles), tiles[0].height), "white"); x = 0
    for t in tiles:
        s.paste(t, (x, 0)); x += t.width + 6
    s.resize((s.width // 2, s.height // 2), Image.LANCZOS).save(os.path.join(ART, "tests", "hd", "fingers-plate-measure.png"))
    out = [{k: v for k, v in r.items() if k != "mask"} for r in res]
    for r in out:
        print(r)
    json.dump(out, open(os.path.join(ART, "hd", "fingers", "geometry-measured.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
