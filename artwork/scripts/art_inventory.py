"""Read-only inventory of approved art for desktop chapter candidates: size, alpha, which image edges carry an
opaque cut (bleed) vs a natural/feathered silhouette, feathered-edge detection, landing usage."""
import glob, json, os, re
import numpy as np
from PIL import Image

ROOT = r"C:\Users\SSTS\Desktop\Riya"
SRC = os.path.join(ROOT, "theme-build", "src")
LANDING_FILES = ["sections/st-hero.liquid", "sections/st-gallery.liquid", "sections/st-teaser.liquid", "snippets/st-landing-map.liquid",
                 "snippets/st-motion-map.liquid", "snippets/st-peek-map.liquid", "sections/st-chapter.liquid"]


def landing_refs():
    txt = ""
    for f in LANDING_FILES:
        p = os.path.join(SRC, f)
        if os.path.exists(p):
            txt += open(p, encoding="utf-8").read()
    return txt


def edges(path):
    im = Image.open(path)
    a = np.array(im.convert("RGBA"))
    al = a[..., 3]
    has_alpha = bool((al < 250).mean() > 0.01)
    out = {"px": list(im.size), "kb": round(os.path.getsize(path) / 1000), "alpha": has_alpha}
    if not has_alpha:
        out["edges"] = "opaque rectangle"
        return out
    H, W = al.shape
    res = {}
    for name, line, inner in (("top", al[0], al[6]), ("bottom", al[-1], al[-7]), ("left", al[:, 0], al[:, 6]), ("right", al[:, -1], al[:, -7])):
        solid = (line >= 200).mean()
        soft = ((line > 8) & (line < 200)).mean()
        inner_solid = (inner >= 200).mean()
        if solid > 0.05:
            res[name] = f"hard cut {solid*100:.0f}%"
        elif soft > 0.05 or (inner_solid > 0.05 and (line > 8).mean() > 0.02):
            res[name] = f"feathered {max(soft, (line > 8).mean())*100:.0f}%"
    out["edges"] = res or "free silhouette (all sides)"
    return out


def main():
    refs = landing_refs()
    rows = []
    for p in sorted(glob.glob(os.path.join(SRC, "assets", "st-*.webp")) + glob.glob(os.path.join(SRC, "assets", "st-*.png"))):
        n = os.path.basename(p)
        if re.match(r"st-hd-pack-.*-(240|360|480|720)\.webp", n) or n.startswith("st-hd-tone"):
            continue
        e = edges(p)
        e["name"] = n
        e["on_landing"] = n in refs or (n.startswith("st-hd-pack-") and False)
        rows.append(e)
    extra = []
    for p in (glob.glob(os.path.join(ROOT, "artwork", "hd", "props", "brainwave-pen-hand.webp")) +
              glob.glob(os.path.join(ROOT, "artwork", "shop", "web", "lifestyle-*.webp")) +
              glob.glob(os.path.join(ROOT, "artwork", "chapters", "web", "*-fade.webp")) +
              glob.glob(os.path.join(ROOT, "artwork", "hd", "photos", "*.web.webp"))):
        e = edges(p); e["name"] = os.path.relpath(p, ROOT).replace("\\", "/"); e["on_landing"] = False; extra.append(e)
    json.dump({"theme": rows, "artwork_only": extra}, open(os.path.join(ROOT, "qa", "desktop", "owner-v12", "art-inventory.json"), "w"), indent=1)
    for r in rows + extra:
        print(f"{r['name']:48s} {str(r['px']):12s} {r['kb']:>4}KB alpha={str(r['alpha'])[0]} landing={str(r['on_landing'])[0]} {r['edges']}")


if __name__ == "__main__":
    main()
