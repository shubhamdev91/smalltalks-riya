"""Overlay fitter for HD pieces against board crops (css px at 390).

hdfit.py PLAN.json OUT.png [name ...]
PLAN entries: {name: {src, box:[x0,y0,x1,y1] (source px), board: crop file, view:[x0,y0,x1,y1] (board px),
               left, top, width (css px in board coords), mask_poly?: [[x,y],...] source px polygon to keep}}
Renders per entry: board | board + piece at 60% | piece on board-ground mid-tone.
"""
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw

ART = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
SPEC = os.path.normpath(os.path.join(ART, "..", "spec", "crops"))


def piece(e):
    im = Image.open(os.path.join(ART, e["src"])).convert("RGBA").crop(tuple(e["box"]))
    if e.get("mask_poly"):
        m = Image.new("L", im.size, 0)
        ox, oy = e["box"][:2]
        ImageDraw.Draw(m).polygon([(x - ox, y - oy) for x, y in e["mask_poly"]], fill=255)
        a = np.array(im); a[..., 3] = np.minimum(a[..., 3], np.array(m)); im = Image.fromarray(a)
    a = np.array(im).astype(float)
    ox, oy = e["box"][:2]
    if e.get("mask_out_poly"):
        m = Image.new("L", im.size, 0)
        ImageDraw.Draw(m).polygon([(x - ox, y - oy) for x, y in e["mask_out_poly"]], fill=255)
        if e.get("mask_out_grow"):
            m = m.filter(__import__("PIL.ImageFilter", fromlist=["x"]).MaxFilter(2 * e["mask_out_grow"] + 1))
        mm = np.array(m.filter(__import__("PIL.ImageFilter", fromlist=["x"]).GaussianBlur(e.get("mask_out_blur", 1.2)))) / 255.0
        a[..., 3] *= (1 - mm)
    if e.get("remove_dark_blobs"):
        from scipy import ndimage as ndi
        rgb = a[..., :3]; sat = rgb.max(-1) - rgb.min(-1)
        dark = (rgb.max(-1) < 75) & (sat < 45) & (a[..., 3] > 0)
        core = ndi.binary_opening(dark, iterations=3)
        lab, n = ndi.label(core)
        if n:
            sz = ndi.sum(core, lab, range(1, n + 1))
            big = np.isin(lab, [i + 1 for i, v in enumerate(sz) if v >= e["remove_dark_blobs"]])
            hair = ndi.binary_dilation(big, iterations=2) & dark | big
            hair = ndi.binary_dilation(hair, iterations=1)
            soft = ndi.gaussian_filter(hair.astype(float), 1.0)
            a[..., 3] *= (1 - np.clip(soft * 1.5, 0, 1))
    for key, axis, rev in (("feather_bottom", 0, False), ("feather_top", 0, True), ("feather_left", 1, True), ("feather_right", 1, False)):
        if e.get(key):
            f0, f1 = (v - (oy if axis == 0 else ox) for v in e[key])
            n = a.shape[axis]
            t = np.clip((np.arange(n) - f0) / max(f1 - f0, 1), 0, 1)
            t = t * t * (3 - 2 * t)
            ramp = (1 - t) if not rev else t
            a[..., 3] *= ramp[:, None] if axis == 0 else ramp[None, :]
    if e.get("keep_largest"):
        from scipy import ndimage as ndi
        lab, n = ndi.label(a[..., 3] > 0, structure=np.ones((3, 3)))
        if n > 1:
            sz = ndi.sum(np.ones(lab.shape), lab, range(1, n + 1))
            a[lab != (int(np.argmax(sz)) + 1)] = 0
    a[a[..., 3] < 1, :3] = 0
    return Image.fromarray(np.round(a).astype(np.uint8))


def render(e, alpha=0.6):
    board = Image.open(os.path.join(SPEC, e["board"])).convert("RGBA")
    p = piece(e)
    s = e["width"] / p.width
    ps = p.convert("RGBa").resize((max(1, round(p.width * s)), max(1, round(p.height * s))), Image.LANCZOS).convert("RGBA")
    lay = Image.new("RGBA", board.size, (0, 0, 0, 0))
    lay.paste(ps, (round(e["left"]), round(e["top"])), ps)
    ov = board.copy()
    l2 = lay.copy(); l2.putalpha(l2.getchannel("A").point(lambda v: int(v * alpha)))
    ov.alpha_composite(l2)
    full = board.copy(); full.alpha_composite(lay)
    v = tuple(e["view"])
    return [board.crop(v), ov.crop(v), full.crop(v)], s


def render_group(plan, names, alpha=0.6):
    e0 = plan[names[0]]
    board = Image.open(os.path.join(SPEC, e0["board"])).convert("RGBA")
    lay = Image.new("RGBA", board.size, (0, 0, 0, 0))
    for n in names:
        e = plan[n]; p = piece(e); s = e["width"] / p.width
        ps = p.convert("RGBa").resize((max(1, round(p.width * s)), max(1, round(p.height * s))), Image.LANCZOS).convert("RGBA")
        l1 = Image.new("RGBA", board.size, (0, 0, 0, 0)); l1.paste(ps, (round(e["left"]), round(e["top"])), ps)
        lay.alpha_composite(l1)
    ov = board.copy(); l2 = lay.copy(); l2.putalpha(l2.getchannel("A").point(lambda v: int(v * alpha))); ov.alpha_composite(l2)
    full = board.copy(); full.alpha_composite(lay)
    v = tuple(e0["view"])
    return [board.crop(v), ov.crop(v), full.crop(v)], 0


def main():
    plan = json.load(open(sys.argv[1]))
    names = sys.argv[3:] or list(plan)
    rows = []
    for n in names:
        if "+" in n:
            tiles, s = render_group(plan, n.split("+"))
        else:
            tiles, s = render(plan[n])
        rows.append((n, s, tiles))
    W = max(sum(t.width + 8 for t in tl) for _, _, tl in rows)
    H = sum(tl[0].height + 22 for _, _, tl in rows)
    out = Image.new("RGB", (W, H), "white"); d = ImageDraw.Draw(out); y = 0
    for n, s, tl in rows:
        d.text((4, y + 4), f"{n}  scale {s:.3f} (src px -> css px)  | board | overlay 60% | composite", fill="black")
        x = 0
        for t in tl:
            out.paste(t.convert("RGB"), (x, y + 20)); x += t.width + 8
        y += tl[0].height + 22
    out.save(sys.argv[2])


if __name__ == "__main__":
    main()
