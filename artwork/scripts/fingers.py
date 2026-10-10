import json, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage
from stlib import load, clean, save_webp

OUT = os.path.join(os.path.dirname(__file__), "..", "fingers")
TOP_PAD = 8
# Cuticle point (centre of the natural nail's proximal fold) measured on tone-1 in
# source pixels relative to the finger's tip-centre / top edge. Same for all four
# because the four tones share one silhouette (checked visually in tests/fingers-contact.png).
CUTICLE_DY = float(sys.argv[1]) if len(sys.argv) > 1 else 215.0


def main():
    a = load("desi-finger-tones.png")
    c = clean(a, keep="all", min_area=20000)
    lab, n = ndimage.label(c[..., 3] > 0)
    assert n == 4
    objs = sorted(ndimage.find_objects(lab), key=lambda s: s[1].start)
    fingers = []
    for k, (sy, sx) in enumerate(objs):
        crop = c[sy, sx].copy()
        lid = np.bincount(lab[sy, sx].ravel())[1:].argmax() + 1
        crop[lab[sy, sx] != lid] = 0
        m = crop[..., 3] > 128
        ys = np.nonzero(m.any(1))[0]
        top = ys[0]
        band = m[top:top + 120]
        cx = np.nonzero(band)[1].mean()
        fingers.append((crop, top, cx))
    half = max(max(cx, f.shape[1] - cx) for f, _, cx in fingers)
    W = int(np.ceil(half)) * 2 + 16
    H = int(max(f.shape[0] - t for f, t, _ in fingers) + TOP_PAD)
    man = {"canvas": {"width": W, "height": H},
           "nail_bed_anchor": {"x": 0.5, "y": round((TOP_PAD + CUTICLE_DY) / H, 4),
                               "meaning": "cuticle centre of the natural nail, normalised to the canvas; identical in all four files"},
           "bottom_edge": "finger is cropped flat at the canvas bottom (enters from below)",
           "tones": []}
    for k, (f, t, cx) in enumerate(fingers):
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        im.alpha_composite(Image.fromarray(f), (int(round(W / 2 - cx)), TOP_PAD - t))
        p = os.path.join(OUT, f"tone-{k + 1}.webp")
        size, mode = save_webp(im, p, 120, force_lossless=True)
        man["tones"].append({"file": f"fingers/tone-{k + 1}.webp", "order": "light to deep", "index": k + 1,
                             "bytes": size, "encoding": mode})
        print(p, im.size, size, mode)
    json.dump(man, open(os.path.join(OUT, "manifest.json"), "w"), indent=2)


if __name__ == "__main__":
    main()

