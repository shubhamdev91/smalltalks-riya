"""Preview hand: remove the thumb from desi-preview-hand-base.png with a smooth
radial-edge contour, add a soft edge falloff along the new contour, export."""
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage
from stlib import load, clean, save_webp

HERE = os.path.dirname(__file__)
SCR = r"C:\Users\SSTS\AppData\Local\Temp\claude\C--Users-SSTS-Desktop-Riya\c88f0826-6dbb-4d8c-845c-66305c0e9e45\scratchpad"

# New radial contour (source px), from the index finger's visible top edge up to the wrist.
CONTOUR = [(185, 950), (215, 900), (245, 850), (278, 797), (328, 746), (360, 703),
           (388, 648), (420, 588), (468, 525), (530, 468), (610, 416), (700, 374), (800, 344), (850, 318)]


def catmull(pts, n=24):
    p = [pts[0]] + pts + [pts[-1]]
    out = []
    for i in range(1, len(p) - 2):
        p0, p1, p2, p3 = map(np.array, p[i - 1:i + 3])
        for t in np.linspace(0, 1, n, endpoint=False):
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t
                              + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    out.append(np.array(pts[-1]))
    return [tuple(map(float, q)) for q in out]


def build(ss=4):
    a = clean(load("desi-preview-hand-base.png")).astype(np.float32)
    H, W = a.shape[:2]
    curve = catmull(CONTOUR)
    # keep-region polygon: everything below/right of the curve (supersampled for AA)
    poly = [(x * ss, y * ss) for x, y in curve]
    poly += [(curve[-1][0] * ss, 0), (W * ss, 0), (W * ss, H * ss), (0, H * ss), (0, curve[0][1] * ss)]
    m = Image.new("L", (W * ss, H * ss), 0)
    ImageDraw.Draw(m).polygon(poly, fill=255)
    keep = np.array(m.resize((W, H), Image.LANCZOS)).astype(np.float32) / 255.0
    # 1.2px feather so the cut matches the photographic edge softness
    keep = ndimage.gaussian_filter(keep, 0.6)
    newal = a[..., 3] * keep
    # soft falloff (rounded-form shading) only along the new cut, ~10px, max 22% darker
    cut = (keep < 0.999) & (a[..., 3] > 250)
    dist = ndimage.distance_transform_edt(~(keep < 0.5))
    near_cut = ndimage.binary_dilation(cut, iterations=14)
    shade = np.where(near_cut, np.clip(1 - dist / 12.0, 0, 1) ** 1.6 * 0.22, 0)
    a[..., :3] *= (1 - shade)[..., None]
    a[..., 3] = newal
    a[newal < 1, :3] = 0
    # drop anything now disconnected (the thumb tip island, if any)
    out = clean(np.round(a).astype(np.uint8))
    return out


if __name__ == "__main__":
    out = build()
    Image.fromarray(out).save(os.path.join(SCR, "hand_nothumb_full.png"))
    print("ok", out.shape)


