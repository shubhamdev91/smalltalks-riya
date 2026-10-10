"""Clean-edge packaging derivatives. Content locked: no crop, no retouch, no upscale beyond 1.3x Lanczos.
The only change: light cut-out rim lines on the outer edge (1-4 px) become transparent; canvas size unchanged."""
import io, json, os
import numpy as np
from PIL import Image
from phase2 import PRODUCT, ROOT, SRC

MAXD = 4


def rim_depths(L):
    out = {}
    lines = {"top": lambda k: L[k], "bottom": lambda k: L[-1 - k], "left": lambda k: L[:, k], "right": lambda k: L[:, -1 - k]}
    for s, f in lines.items():
        ref = np.median([f(k).mean() for k in range(5, 10)])
        d = 0
        while d < MAXD and f(d).mean() > ref + 12:
            d += 1
        out[s] = d
    return out


def enc(img, path, lossless):
    b = io.BytesIO()
    if lossless:
        img.save(b, "WEBP", lossless=True, quality=100, method=6)
    else:
        img.save(b, "WEBP", quality=100, alpha_quality=100, method=6)
    open(path, "wb").write(b.getvalue())
    return b.tell()


def main():
    os.makedirs(os.path.join(ROOT, "packaging", "web"), exist_ok=True)
    R = json.load(open(os.path.join(ROOT, "phase2.json")))
    out = {}
    for h, p in PRODUCT.items():
        f = f"{p}-approved-package.png"
        a = np.array(Image.open(os.path.join(SRC, f)).convert("RGBA"))
        d = rim_depths(a[..., :3].astype(float).mean(2))
        al = a[..., 3].astype(float)
        H, W = al.shape
        for s, n in d.items():
            sl = {"top": (slice(0, n), slice(None)), "bottom": (slice(H - n, H), slice(None)),
                  "left": (slice(None), slice(0, n)), "right": (slice(None), slice(W - n, W))}[s]
            al[sl] = 0
            # one soft line just inside so the new edge is anti-aliased, not stair-stepped
            inner = {"top": (slice(n, n + 1), slice(None)), "bottom": (slice(H - n - 1, H - n), slice(None)),
                     "left": (slice(None), slice(n, n + 1)), "right": (slice(None), slice(W - n - 1, W - n))}[s]
            al[inner] = np.minimum(al[inner], 170)
        res = a.copy()
        res[..., 3] = al.astype(np.uint8)
        res[res[..., 3] == 0, :3] = 0
        im = Image.fromarray(res)
        master = os.path.join(ROOT, "packaging", f"{h}.webp")
        mb = enc(im, master, True)
        w1 = f"packaging/web/{h}.webp"
        b1 = enc(im, os.path.join(ROOT, w1), False)
        W2, H2 = int(W * 1.3), int(H * 1.3)  # floor keeps it <= 1.3x
        im2 = im.convert("RGBa").resize((W2, H2), Image.LANCZOS).convert("RGBA")
        a2 = np.array(im2); a2[a2[..., 3] == 0, :3] = 0
        w2 = f"packaging/web/{h}@1.3x.webp"
        b2 = enc(Image.fromarray(a2), os.path.join(ROOT, w2), False)
        m = res[..., 3] == 255
        delta = int(np.abs(res[m, :3].astype(int) - a[m, :3].astype(int)).max())
        out[h] = {"file": f"packaging/{h}.webp", "source": f, "width": W, "height": H, "bytes": mb,
                  "web": w1, "web_bytes": b1, "web_1_3x": w2, "web_1_3x_size": [W2, H2], "web_1_3x_bytes": b2,
                  "rim_cleared_px": d, "rgb_delta_vs_source_on_opaque": delta, "upscale": "1.3x Lanczos (premultiplied) only",
                  "content": "locked; not cropped or retouched (incl. Brainwave 'tha', Diet Cherry box can)"}
        print(h, W, H, d, mb, b1, (W2, H2), b2, delta)
    R["packaging"] = out
    json.dump(R, open(os.path.join(ROOT, "phase2.json"), "w"), indent=2)


if __name__ == "__main__":
    main()
