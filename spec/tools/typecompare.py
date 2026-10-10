"""Render 3-4 OFL candidates per type role against the board crop -> spec/type/compare-<role>.png
Score (straight single-line roles only): IoU of text masks after matching the text height and left/top."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from samples import SAMPLES, load

ROOT = os.path.join(os.path.dirname(__file__), "..")
F = os.path.join(ROOT, "fonts")
T = os.path.join(ROOT, "type")
K = 3  # sample enlargement


def font(path, size, **axes):
    f = ImageFont.truetype(os.path.join(F, path), size)
    if axes:
        names = [a["name"].decode() if isinstance(a["name"], bytes) else a["name"] for a in f.get_variation_axes()]
        vals = []
        for n, a in zip(names, f.get_variation_axes()):
            key = {"Weight": "wght", "Optical size": "opsz", "Optical Size": "opsz", "Softness": "SOFT", "Wonky": "WONK"}.get(n, n)
            vals.append(axes.get(key, a["default"]))
        f.set_variation_by_axes(vals)
    return f


CANDS = {
    "headline": [("Fraunces Black SOFT100 WONK1", "fraunces/Fraunces[SOFT,WONK,opsz,wght].ttf", dict(wght=900, SOFT=100, WONK=1, opsz=144)),
                 ("Fraunces Black SOFT50 opsz72", "fraunces/Fraunces[SOFT,WONK,opsz,wght].ttf", dict(wght=900, SOFT=50, WONK=0, opsz=72)),
                 ("Caprasimo", "caprasimo/Caprasimo-Regular.ttf", {}),
                 ("Corben Bold", "corben/Corben-Bold.ttf", {}), ("Young Serif", "youngserif/YoungSerif-Regular.ttf", {})],
    "note": [("Caveat 700", "caveat/Caveat[wght].ttf", dict(wght=700)), ("Caveat 600", "caveat/Caveat[wght].ttf", dict(wght=600)), ("Kalam Regular", "kalam/Kalam-Regular.ttf", {}), ("Caveat Brush", "caveatbrush/CaveatBrush-Regular.ttf", {}),
             ("Patrick Hand", "patrickhand/PatrickHand-Regular.ttf", {})],
    "pill": [("Barlow Semi Condensed Medium", "barlowsemicondensed/BarlowSemiCondensed-Medium.ttf", {}),
             ("Barlow Semi Condensed SemiBold", "barlowsemicondensed/BarlowSemiCondensed-SemiBold.ttf", {}),
             ("Roboto Condensed 500", "robotocondensed/RobotoCondensed[wght].ttf", dict(wght=500)),
             ("IBM Plex Sans Condensed Medium", "ibmplexsanscondensed/IBMPlexSansCondensed-Medium.ttf", {})],
    "talks": [("Caveat 600", "caveat/Caveat[wght].ttf", dict(wght=600)), ("Caveat 500", "caveat/Caveat[wght].ttf", dict(wght=500)), ("Nanum Pen Script", "nanumpenscript/NanumPenScript-Regular.ttf", {}),
              ("Reenie Beanie", "reeniebeanie/ReenieBeanie.ttf", {}), ("Shadows Into Light Two", "shadowsintolighttwo/ShadowsIntoLightTwo-Regular.ttf", {})],
    "shop-heading": [("Playfair Display 800", "playfairdisplay/PlayfairDisplay[wght].ttf", dict(wght=800)),
                     ("DM Serif Display", "dmserifdisplay/DMSerifDisplay-Regular.ttf", {}),
                     ("Abril Fatface", "abrilfatface/AbrilFatface-Regular.ttf", {}),
                     ("Source Serif 4 Bold opsz60", "sourceserif4/SourceSerif4[opsz,wght].ttf", dict(wght=700, opsz=60)),
                     ("Libre Caslon Text Bold", "librecaslontext/LibreCaslonText[wght].ttf", dict(wght=700)),
                     ("Fraunces 800 SOFT0 opsz72", "fraunces/Fraunces[SOFT,WONK,opsz,wght].ttf", dict(wght=800, SOFT=0, WONK=0, opsz=72))],
    "annotation": [("Kalam Light", "kalam/Kalam-Light.ttf", {}), ("Patrick Hand", "patrickhand/PatrickHand-Regular.ttf", {}),
                   ("Gochi Hand", "gochihand/GochiHand-Regular.ttf", {}), ("Caveat 400", "caveat/Caveat[wght].ttf", dict(wght=400))],
    "ui-sub": [("Barlow Semi Condensed SemiBold", "barlowsemicondensed/BarlowSemiCondensed-SemiBold.ttf", {}),
               ("DM Sans 600", "dmsans/DMSans[opsz,wght].ttf", dict(wght=600, opsz=14)),
               ("IBM Plex Sans Condensed SemiBold", "ibmplexsanscondensed/IBMPlexSansCondensed-SemiBold.ttf", {})],
    "ui-body": [("DM Sans 400", "dmsans/DMSans[opsz,wght].ttf", dict(wght=400, opsz=14)),
                ("Barlow Semi Condensed Regular", "barlowsemicondensed/BarlowSemiCondensed-Regular.ttf", {}),
                ("IBM Plex Sans Condensed Regular", "ibmplexsanscondensed/IBMPlexSansCondensed-Regular.ttf", {})],
}
ANGLE = {"note": -10, "annotation": -4}
SCORE = {"pill", "talks", "shop-heading", "ui-sub", "headline"}


def fgbg(a):
    border = np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]])
    bg = np.median(border, 0)
    d = np.abs(a - bg).sum(2)
    fg = a[d > np.percentile(d, 92)].mean(0)
    return fg, bg


def mask_of(a, fg, bg):
    d_fg = np.abs(a - fg).sum(2)
    d_bg = np.abs(a - bg).sum(2)
    return d_fg < d_bg


def draw(text, f, track):
    """Draw text char by char with extra tracking (px). Returns L mask image (tight)."""
    lines = text.split("\n")
    asc, desc = f.getmetrics()
    lh = int((asc + desc) * 0.95)
    widths = [sum(f.getlength(c) + track for c in ln) for ln in lines]
    W = int(max(widths) + abs(track) * 4 + f.size); H = lh * len(lines) + f.size
    im = Image.new("L", (W, H), 0); d = ImageDraw.Draw(im)
    for i, ln in enumerate(lines):
        x = f.size // 2
        for c in ln:
            d.text((x, f.size // 2 + i * lh), c, font=f, fill=255)
            x += f.getlength(c) + track
    return im


def tight(im, angle):
    if angle:
        im = im.rotate(-angle, resample=Image.BICUBIC, expand=True)
    m = np.array(im) > 127
    ys, xs = np.nonzero(m)
    return im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))


def render(text, fpath, axes, target_h, target_w, fg, bg, shape, origin, angle=0):
    track_em = 0.0
    for _ in range(3):
        lo, hi = 4, 800
        while lo < hi:
            s = (lo + hi) // 2
            f = font(fpath, s, **axes)
            if tight(draw(text, f, track_em * s), angle).height < target_h:
                lo = s + 1
            else:
                hi = s
        s = lo; f = font(fpath, s, **axes)
        n = max(len(max(text.split("\n"), key=len)) - 1, 1)
        a_, b_ = -0.25, 0.25
        for _ in range(20):
            m_ = (a_ + b_) / 2
            if tight(draw(text, f, m_ * s), angle).width < target_w:
                a_ = m_
            else:
                b_ = m_
        track_em = (a_ + b_) / 2
    layer = tight(draw(text, f, track_em * s), angle)
    canvas = Image.new("RGB", shape, tuple(int(v) for v in bg))
    col = Image.new("RGB", layer.size, tuple(int(v) for v in fg))
    canvas.paste(col, origin, layer)
    full = Image.new("L", shape, 0)
    full.paste(layer, origin)
    return canvas, np.array(full) > 127, s, track_em


def main():
    picks = {}
    for role, (src, box, text, note) in SAMPLES.items():
        crop = load(src).crop(box)
        crop = crop.resize((crop.width * K, crop.height * K), Image.LANCZOS)
        a = np.array(crop).astype(float)
        fg, bg = fgbg(a)
        bm = mask_of(a, fg, bg)
        ys, xs = np.nonzero(bm)
        th = ys.max() - ys.min() + 1
        origin = (int(xs.min()), int(ys.min()))
        rows = [(f"BOARD  ({note})", crop, None)]
        scored = []
        for name, path, axes in CANDS[role]:
            tw = xs.max() - xs.min() + 1
            img, cm, size, tr = render(text, path, axes, th, tw, fg, bg, crop.size, origin, ANGLE.get(role, 0))
            iou = (bm & cm).sum() / max((bm | cm).sum(), 1) if role in SCORE else None
            scored.append((name, iou, round(size / K, 1), round(tr, 3)))
            rows.append((f"{name}  {'IoU %.3f' % iou if iou is not None else ''}  (~{size / K:.0f}px at board scale, tracking {tr:+.3f}em)", img, iou))
        lh = 22
        W = max(r[1].width for r in rows) + 10
        sheet = Image.new("RGB", (W, sum(r[1].height + lh + 8 for r in rows)), "white")
        d = ImageDraw.Draw(sheet)
        y = 0
        for label, im, _ in rows:
            d.text((4, y + 4), label, fill="black")
            sheet.paste(im, (0, y + lh))
            y += im.height + lh + 8
        sheet.save(os.path.join(T, f"compare-{role}.png"))
        picks[role] = scored
        print(role, scored)
    return picks


if __name__ == "__main__":
    main()
