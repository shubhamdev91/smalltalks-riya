"""Shared helpers: alpha cleanup, defringe, WebP save. Never touches interior RGB."""
import io
import numpy as np
from PIL import Image
from scipy import ndimage

SRC = r"C:\Users\SSTS\Desktop\Riya\backup\theme-186649313493\atlas-images"
BGS = ["#ffb900", "#073df1", "#e10019", "#007948", "#ff0078", "#b7ef00", "#6620f2"]
LO, HI = 24, 232  # alpha <= LO -> 0, >= HI -> 255


def load(name):
    return np.array(Image.open(f"{SRC}\\{name}").convert("RGBA"))


def clean(arr, keep="largest", min_area=200):
    """arr: HxWx4 uint8. Returns cleaned copy.
    1. remap alpha (kills faint specks, makes interior exactly opaque)
    2. drop disconnected specks (keep largest component, or all >= min_area)
    3. rim defringe: pixels with alpha < 255 take RGB of nearest opaque pixel
    4. zero RGB where alpha == 0
    """
    a = arr.astype(np.float32)
    al = a[..., 3]
    al = np.clip((al - LO) * 255.0 / (HI - LO), 0, 255)
    lab, n = ndimage.label(al > 0, structure=np.ones((3, 3)))
    if n:
        sizes = ndimage.sum(np.ones_like(al), lab, range(1, n + 1))
        if keep == "largest":
            ok = {int(np.argmax(sizes)) + 1}
        else:
            ok = {i + 1 for i, s in enumerate(sizes) if s >= min_area}
        al[~np.isin(lab, list(ok))] = 0
    out = a.copy()
    out[..., 3] = al
    opaque = al >= 255
    if opaque.any():
        _, (iy, ix) = ndimage.distance_transform_edt(~opaque, return_indices=True)
        rim = (al > 0) & (al < 255)
        out[rim, :3] = a[iy[rim], ix[rim], :3]
    out[al == 0, :3] = 0
    return np.round(out).astype(np.uint8)


def bbox(arr):
    ys, xs = np.nonzero(arr[..., 3])
    return xs.min(), ys.min(), xs.max() + 1, ys.max() + 1


def save_webp(img, path, budget_kb, force_lossless=False):
    """Lossless if it fits budget, else highest lossy quality >= 92 that fits."""
    buf = io.BytesIO()
    img.save(buf, "WEBP", lossless=True, quality=100, method=6, exact=False)
    mode = "lossless"
    if buf.tell() > budget_kb * 1000 and not force_lossless:
        for q in range(100, 91, -1):
            buf = io.BytesIO()
            img.save(buf, "WEBP", quality=q, alpha_quality=100, method=6)
            mode = f"lossy q{q}"
            if buf.tell() <= budget_kb * 1000:
                break
    with open(path, "wb") as f:
        f.write(buf.getvalue())
    return buf.tell(), mode


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

