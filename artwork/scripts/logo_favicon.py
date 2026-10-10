"""Logo-derived favicon candidates (crops/masks of the official wordmark only) vs the current nail favicon.
V1 full stacked wordmark, V2 's' alone, V3 's'+'t' in their own wordmark positions (left edge of the logo, 'm'/'a' masked).
All in the exact logo blue on the site paper colour (rounded square); apple = square + opaque."""
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

ART = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
LOGO = os.path.join(ART, "hd", "logo", "small-talk-logo-trim.png")
PAPER = (253, 253, 252, 255)       # --st-paper #fdfdfc
M = 1024


def glyph_mask():
    a = np.array(Image.open(LOGO).convert("RGBA"))
    al = a[..., 3]
    lab, n = ndimage.label(al > 0, structure=np.ones((3, 3)))
    return a, al, lab


def comp_at(lab, x, y):
    return lab[y, x]


def variant(name):
    a, al, lab = glyph_mask()
    keep = np.zeros(al.shape, bool)
    if name == "wordmark":
        keep[:] = True
    elif name == "s":
        keep = lab == comp_at(lab, 100, 300)
    elif name == "st":
        s = lab == comp_at(lab, 100, 300)
        ta = lab == comp_at(lab, 300, 700)
        cut = np.zeros(al.shape, bool); cut[:, :431] = True   # 't' ends at x~428; the 'a' starts at x~425 low down
        keep = s | (ta & cut)
    g = a.copy(); g[~keep] = 0
    ys, xs = np.nonzero(g[..., 3] > 0)
    g = g[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    return Image.fromarray(g)


def compose(glyph, fill, rounded=True, size=M):
    s = fill * size / max(glyph.size)
    gl = glyph.convert("RGBa").resize((round(glyph.width * s), round(glyph.height * s)), Image.LANCZOS).convert("RGBA")
    bg = Image.new("RGBA", (size, size), PAPER)
    if rounded:
        m = Image.new("L", (size * 4, size * 4), 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, size * 4 - 1, size * 4 - 1], radius=int(0.22 * size * 4), fill=255)
        bg.putalpha(m.resize((size, size), Image.LANCZOS))
    cv = Image.new("RGBA", (size, size), (0, 0, 0, 0)); cv.alpha_composite(bg)
    cv.alpha_composite(gl, ((size - gl.width) // 2, (size - gl.height) // 2))
    return cv


def down(im, n):
    r = im.convert("RGBa").resize((n, n), Image.LANCZOS).convert("RGBA")
    a = np.array(r); a[a[..., 3] == 0, :3] = 0
    return Image.fromarray(a)


FILLS = {"wordmark": 0.84, "s": 0.74, "st": 0.80}


def main():
    cands = {k: compose(variant(k), f) for k, f in FILLS.items()}
    nail = Image.open(os.path.join(ART, "hd", "favicon", "_master-1024.png")).convert("RGBA")
    cands["nail (current)"] = nail
    rows = []
    for ground in ((242, 242, 242), (35, 35, 40)):
        row = Image.new("RGB", (1500, 270), ground); d = ImageDraw.Draw(row); x = 10
        for name, im in cands.items():
            d.text((x, 6), name, fill=(140, 140, 140))
            i16, i32, i180 = down(im, 16), down(im, 32), down(im, 180)
            row.paste(i16, (x, 40), i16); row.paste(i32, (x + 26, 40), i32)
            z16 = i16.resize((64, 64), Image.NEAREST); z32 = i32.resize((64, 64), Image.NEAREST)
            row.paste(z16, (x, 90), z16); row.paste(z32, (x + 70, 90), z32)
            row.paste(i180.resize((90, 90), Image.LANCZOS), (x + 150, 40), i180.resize((90, 90), Image.LANCZOS))
            d.text((x, 160), "16 32 | 16x4 32x4 | 180", fill=(140, 140, 140))
            x += 370
        rows.append(row)
    s = Image.new("RGB", (1500, 540), "white"); s.paste(rows[0], (0, 0)); s.paste(rows[1], (0, 270))
    s.save(os.path.join(ART, "tests", "hd", "contact-favicon-logo-candidates.png"))
    os.makedirs(os.path.join(ART, "hd", "favicon-logo", "_candidates"), exist_ok=True)
    for k, im in cands.items():
        if "nail" in k: continue
        im.save(os.path.join(ART, "hd", "favicon-logo", "_candidates", f"{k}-1024.png"))


if __name__ == "__main__":
    main()
