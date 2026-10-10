"""Budget derivatives (<=120 KB, q>=92) from the lossless masters, with measured RGB deltas."""
import glob, io, json, os
import numpy as np
from PIL import Image

ROOT = os.path.join(os.path.dirname(__file__), "..")


def main():
    out = {}
    for d in ("nails", "fingers", "hand"):
        os.makedirs(os.path.join(ROOT, d, "web"), exist_ok=True)
        for p in sorted(glob.glob(os.path.join(ROOT, d, "*.webp"))):
            im = Image.open(p).convert("RGBA")
            a = np.array(im)
            for q in range(100, 91, -1):
                b = io.BytesIO()
                im.save(b, "WEBP", quality=q, alpha_quality=100, method=6)
                if b.tell() <= (200000 if d == "hand" else 120000):
                    break
            r = np.array(Image.open(io.BytesIO(b.getvalue())).convert("RGBA"))
            m = a[..., 3] == 255
            dd = np.abs(r[m, :3].astype(int) - a[m, :3].astype(int))
            name = os.path.basename(p)
            open(os.path.join(ROOT, d, "web", name), "wb").write(b.getvalue())
            out[f"{d}/web/{name}"] = {"master": f"{d}/{name}", "master_bytes": os.path.getsize(p),
                                      "bytes": b.tell(), "quality": q,
                                      "rgb_delta_on_opaque": {"max": int(dd.max()), "mean": round(float(dd.mean()), 3),
                                                              "p99": int(np.percentile(dd.max(1), 99))},
                                      "alpha_identical": bool((r[..., 3] == a[..., 3]).all())}
            print(name, os.path.getsize(p), b.tell(), q, out[f"{d}/web/{name}"]["rgb_delta_on_opaque"],
                  out[f"{d}/web/{name}"]["alpha_identical"])
    json.dump(out, open(os.path.join(ROOT, "derivatives.json"), "w"), indent=2)


if __name__ == "__main__":
    main()

