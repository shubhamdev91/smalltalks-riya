"""Audit / fix detached fragments in exported HD cutouts.
audit: list fragments with alpha >= 40 (visible) per file. fix: remove fragments whose max alpha < VIS or size < MIN
(always), and optionally listed files' visible fragments too (--drop-visible name ...). Rewrites master + web."""
import argparse, glob, io, os
import numpy as np
from PIL import Image
from scipy import ndimage

ART = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
SKIP = {"wild-card-woman", "wild-card-woman-hero", "wild-card-cards-hand", "wild-card-cards-hand-hero"}  # superseded


def files():
    out = []
    for g in ("characters", "props", "fingers", "nails"):
        for f in sorted(glob.glob(os.path.join(ART, "hd", g, "*.webp"))):
            n = os.path.basename(f)[:-5]
            if n.endswith(".web") or n in SKIP:
                continue
            out.append((g, n, f))
    return out


def frags(al):
    lab, n = ndimage.label(al > 0, structure=np.ones((3, 3)))
    if n <= 1:
        return lab, []
    sz = ndimage.sum(np.ones(al.shape), lab, range(1, n + 1))
    mx = ndimage.maximum(al, lab, range(1, n + 1))
    objs = ndimage.find_objects(lab)
    big = int(np.argmax(sz))
    res = [(i + 1, int(sz[i]), int(mx[i]), objs[i]) for i in range(n) if i != big]
    if "nails" in "":
        pass
    return lab, res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fix", action="store_true")
    ap.add_argument("--drop-visible", nargs="*", default=[])
    a = ap.parse_args()
    for g, n, f in files():
        im = np.array(Image.open(f).convert("RGBA"))
        al = im[..., 3]
        if g == "nails":   # each cell is its own subject
            parts = [(slice(None), slice(k * 450, (k + 1) * 450)) for k in range(al.shape[1] // 450)]
        else:
            parts = [(slice(None), slice(None))]
        removed = vis_kept = 0
        for sl in parts:
            sub = al[sl]
            lab, res = frags(sub)
            for lid, sz, mx, ob in res:
                visible = mx >= 40 and sz >= 6
                if (not visible) or (n in a.drop_visible):
                    if a.fix:
                        m = lab == lid
                        block = im[sl]; block[m] = 0; im[sl] = block
                    removed += 1
                else:
                    vis_kept += 1
                    if not a.fix:
                        ys, xs = ob
                        print(f"   {n}: visible fragment {sz}px max-alpha {mx} at x{xs.start}-{xs.stop} y{ys.start}-{ys.stop}")
        print(f"{g}/{n}: removable {removed}, visible kept {vis_kept}")
        if a.fix and removed:
            Image.fromarray(im).save(f, "WEBP", lossless=True, quality=100, method=6)
            wf = f.replace(".webp", ".web.webp")
            if os.path.exists(wf):
                w = Image.open(wf)
                r = Image.fromarray(im).convert("RGBa").resize(w.size, Image.LANCZOS).convert("RGBA")
                ra = np.array(r); ra[ra[..., 3] <= 3] = 0
                b = io.BytesIO(); Image.fromarray(ra).save(b, "WEBP", quality=92, alpha_quality=100, method=6)
                open(wf, "wb").write(b.getvalue())


if __name__ == "__main__":
    main()
