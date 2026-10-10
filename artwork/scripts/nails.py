import json, os
import numpy as np
from PIL import Image
from scipy import ndimage
from stlib import load, clean, save_webp

OUT = os.path.join(os.path.dirname(__file__), "..", "nails")
HANDLES = ["on-me", "brainwave", "diet-cherry", "green-flag", "shaadi-shift", "wild-card", "pinky-promise"]
ANCHOR = (0.5, 0.925)


def nails_from(atlas_name, rows):
    """Return grid[row][col] of cleaned nail crops (RGBA arrays) ordered by position."""
    arr = load(atlas_name)
    lab, n = ndimage.label(arr[..., 3] > 128, structure=np.ones((3, 3)))
    objs = ndimage.find_objects(lab)
    sizes = ndimage.sum(np.ones(lab.shape), lab, range(1, n + 1))
    big = [i for i in range(n) if sizes[i] > 5000]
    assert len(big) == 7 * rows, (atlas_name, len(big))
    items = []
    for i in big:
        sy, sx = objs[i]
        pad = 6
        y0, y1 = max(sy.start - pad, 0), min(sy.stop + pad, arr.shape[0])
        x0, x1 = max(sx.start - pad, 0), min(sx.stop + pad, arr.shape[1])
        crop = arr[y0:y1, x0:x1].copy()
        # isolate this nail only (soft rim included via dilation of its own mask)
        own = ndimage.binary_dilation(lab[y0:y1, x0:x1] == i + 1, iterations=4)
        crop[~own] = 0
        items.append(((sy.start + sy.stop) / 2, (sx.start + sx.stop) / 2, clean(crop)))
    items.sort(key=lambda t: t[0])
    grid = []
    for r in range(rows):
        row = sorted(items[r * 7:(r + 1) * 7], key=lambda t: t[1])
        grid.append([t[2] for t in row])
    return grid


def tight(a):
    ys, xs = np.nonzero(a[..., 3])
    return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def main():
    ov = nails_from("desi-nail-overlays.png", 2)
    ac = nails_from("desi-nail-accents-v2.png", 1)
    cells = [[tight(ov[0][i]), tight(ov[1][i]), tight(ac[0][i])] for i in range(7)]
    # accents-v2 is drawn ~1.56x larger than the overlays; bring it to the signature
    # height (downscale only, premultiplied so the rim does not darken)
    target_h = max(c[0].shape[0] for c in cells)
    for c in cells:
        a = c[2]
        s = target_h / a.shape[0]
        im = Image.fromarray(a).convert("RGBa").resize(
            (round(a.shape[1] * s), target_h), Image.LANCZOS).convert("RGBA")
        r = np.array(im)
        r[r[..., 3] == 0, :3] = 0
        c[2] = tight(r)
    extra_scale = round(s, 4)
    maxw = max(c.shape[1] for s in cells for c in s)
    maxh = max(c.shape[0] for s in cells for c in s)
    # cell: nail bottom at 0.925H, keep >= 8px margin at top and sides
    H = int(np.ceil((maxh + 8) / ANCHOR[1]))
    H += H % 2
    W = maxw + 16
    W += W % 2
    man = {
        "cell": {"width": W, "height": H},
        "columns": ["signature", "accent", "extra_accent"],
        "anchor": {"x": ANCHOR[0], "y": ANCHOR[1],
                   "meaning": "cuticle point (lowest opaque pixel, horizontal centre of nail bbox) in each cell, normalised to the cell"},
        "background_size_css": "300% 100%; background-position: 0% / 50% / 100% for columns 0/1/2",
        "sources": {"signature": "desi-nail-overlays.png row 0", "accent": "desi-nail-overlays.png row 1",
                    "extra_accent": f"desi-nail-accents-v2.png, downscaled ~{extra_scale} (Lanczos, premultiplied) to match signature height"},
        "note": f"All three columns share one scale: nail height {target_h} px in a {H} px tall cell.",
        "sets": {},
    }
    ax, ay = round(ANCHOR[0] * W), round(ANCHOR[1] * H)
    for i, h in enumerate(HANDLES):
        sheet = Image.new("RGBA", (W * 3, H), (0, 0, 0, 0))
        boxes = []
        for c, nail in enumerate(cells[i]):
            nh, nw = nail.shape[:2]
            x = c * W + ax - nw // 2
            y = ay - nh
            sheet.alpha_composite(Image.fromarray(nail), (x, y))
            boxes.append({"x": x - c * W, "y": y, "w": nw, "h": nh})
        path = os.path.join(OUT, f"{h}.webp")
        size, mode = save_webp(sheet, path, 120, force_lossless=True)
        man["sets"][h] = {"motion_index": i, "file": f"nails/{h}.webp", "bytes": size, "encoding": mode,
                          "nail_boxes_px": boxes}
        print(h, sheet.size, size, mode)
    with open(os.path.join(OUT, "manifest.json"), "w") as f:
        json.dump(man, f, indent=2)


if __name__ == "__main__":
    main()

