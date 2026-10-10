"""Favicon set from the frozen HD On Me signature nail (hd/nails/on-me.webp, cell 0, lossless master).
Derivative only: crop + rotate + scale onto a flat On Me mustard square. No drawing."""
import hashlib, io, json, os
import numpy as np
from PIL import Image, ImageDraw

ART = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ART, "hd", "favicon")
GROUND = (255, 185, 0, 255)      # On Me campaign mustard #ffb900
ROT = -35                        # tip leans up-right (PIL: negative = clockwise)
FILL = 0.86                      # nail diagonal extent as a fraction of the square
RADIUS = 0.22                    # rounded corners for the tab/manifest icons (apple: square, iOS rounds itself)
MASTER = 1024


def nail():
    sh = Image.open(os.path.join(ART, "hd", "nails", "on-me.webp")).convert("RGBA")
    c = sh.crop((0, 0, 450, 780))
    a = np.array(c); ys, xs = np.nonzero(a[..., 3] > 0)
    c = c.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    r = c.convert("RGBa").rotate(ROT, resample=Image.BICUBIC, expand=True).convert("RGBA")
    a = np.array(r); ys, xs = np.nonzero(a[..., 3] > 8)
    return r.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))


def master(rounded):
    n = nail()
    s = FILL * MASTER / max(n.size)
    n = n.convert("RGBa").resize((round(n.width * s), round(n.height * s)), Image.LANCZOS).convert("RGBA")
    cv = Image.new("RGBA", (MASTER, MASTER), (0, 0, 0, 0))
    bg = Image.new("RGBA", (MASTER, MASTER), GROUND)
    if rounded:
        m = Image.new("L", (MASTER * 4, MASTER * 4), 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, MASTER * 4 - 1, MASTER * 4 - 1], radius=int(RADIUS * MASTER * 4), fill=255)
        bg.putalpha(m.resize((MASTER, MASTER), Image.LANCZOS))
    cv.alpha_composite(bg)
    cv.alpha_composite(n, ((MASTER - n.width) // 2, (MASTER - n.height) // 2))
    return cv


def down(im, size):
    r = im.convert("RGBa").resize((size, size), Image.LANCZOS).convert("RGBA")
    a = np.array(r); a[a[..., 3] == 0, :3] = 0
    return Image.fromarray(a)


def md5(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()


def main():
    os.makedirs(OUT, exist_ok=True)
    rounded, square = master(True), master(False)
    rounded.save(os.path.join(OUT, "_master-1024.png"))
    files = {}
    for name, im, size in (("favicon-16.png", rounded, 16), ("favicon-32.png", rounded, 32), ("favicon-48.png", rounded, 48),
                           ("favicon-192.png", rounded, 192), ("favicon-512.png", rounded, 512)):
        p = os.path.join(OUT, name); down(im, size).save(p, optimize=True); files[name] = p
    p = os.path.join(OUT, "apple-touch-icon-180.png"); down(square, 180).convert("RGB").save(p, optimize=True); files["apple-touch-icon-180.png"] = p
    p = os.path.join(OUT, "favicon.ico")
    down(rounded, 48).save(p, format="ICO", sizes=[(16, 16), (32, 32), (48, 48)]); files["favicon.ico"] = p
    # contact sheet: 16/32/180 at 1x and 4x on light + dark tab grounds
    tiles = []
    for ground in ((245, 245, 245), (40, 40, 44)):
        row = Image.new("RGB", (1320, 300), ground); d = ImageDraw.Draw(row); x = 10
        for name, k in (("favicon-16.png", 1), ("favicon-32.png", 1), ("apple-touch-icon-180.png", 1), ("favicon-16.png", 4), ("favicon-32.png", 4)):
            im = Image.open(files[name]).convert("RGBA")
            im = im.resize((im.width * k, im.height * k), Image.NEAREST)
            row.paste(im, (x, 40), im)
            d.text((x, 10), f"{name.split('.')[0]} x{k}", fill=(128, 128, 128)); x += im.width + 40
        tiles.append(row)
    sheet = Image.new("RGB", (1320, 600), "white")
    sheet.paste(tiles[0], (0, 0)); sheet.paste(tiles[1], (0, 300))
    sp = os.path.join(ART, "tests", "hd", "contact-favicon.png"); sheet.save(sp)
    rec = {"source": "hd/nails/on-me.webp (frozen lossless master, md5 a3b8cf149fc4355b8a19d124968c261e), cell 0 = On Me signature burgundy nail",
           "derivation": f"crop + rotate {ROT} deg + scale to {FILL} of the square, centred on flat #ffb900 (On Me mustard); rounded corners r={RADIUS} on tab/manifest icons; apple icon square + opaque",
           "files": {k: {"path": os.path.relpath(v, ART).replace("\\", "/"), "bytes": os.path.getsize(v), "md5": md5(v)} for k, v in files.items()},
           "contact_sheet": "tests/hd/contact-favicon.png",
           "html": ['<link rel="icon" href="favicon.ico" sizes="48x48">', '<link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png">',
                    '<link rel="icon" type="image/png" sizes="192x192" href="favicon-192.png">', '<link rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon-180.png">'],
           "note": "temporary until the owner uploads a real logo (SD27)"}
    mp = os.path.join(ART, "manifest.json"); m = json.load(open(mp, encoding="utf-8"))
    m["hd"]["favicon"] = rec
    json.dump(m, open(mp, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    for k, v in rec["files"].items():
        print(f"{k:26s} {v['bytes']:>6}  {v['md5']}")


if __name__ == "__main__":
    main()
