"""Stacked 'small / talk' logo candidates vs board 2 header crop (frame 1 at 390). Output spec/type/compare-logo.png."""
import os
import numpy as np
from PIL import Image, ImageDraw
from typecompare import font

ROOT = os.path.join(os.path.dirname(__file__), "..")
K = 4
BOX = (85, 0, 185, 69)  # in hero-1-on-me@390.png
CANDS = [
    ("DM Serif Display (current ST Display)", "dmserifdisplay/DMSerifDisplay-Regular.ttf", {}),
    ("Fraunces 900 opsz144 SOFT0 (shipped static)", "fraunces/Fraunces[SOFT,WONK,opsz,wght].ttf", dict(wght=900, opsz=144, SOFT=0, WONK=0)),
    ("Fraunces 900 opsz72 SOFT0", "fraunces/Fraunces[SOFT,WONK,opsz,wght].ttf", dict(wght=900, opsz=72, SOFT=0, WONK=0)),
    ("Source Serif 4 Black opsz60", "sourceserif4/SourceSerif4[opsz,wght].ttf", dict(wght=900, opsz=60)),
    ("Abril Fatface", "abrilfatface/AbrilFatface-Regular.ttf", {}),
    ("Young Serif", "youngserif/YoungSerif-Regular.ttf", {}),
]


def word(f, text, track):
    W = int(f.size * len(text) * 1.2); H = int(f.size * 2)
    im = Image.new("L", (W, H), 0); d = ImageDraw.Draw(im); x = f.size // 4
    for c in text:
        d.text((x, f.size // 2), c, font=f, fill=255); x += f.getlength(c) + track
    m = np.array(im) > 127; ys, xs = np.nonzero(m)
    return im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)), f.getmetrics()


def board():
    a = np.array(Image.open(os.path.join(ROOT, "crops", "hero-1-on-me@390.png")).convert("RGB").crop(BOX)
                 .resize(((BOX[2] - BOX[0]) * K, (BOX[3] - BOX[1]) * K), Image.LANCZOS)).astype(int)
    m = (a[..., 2] > 150) & (a[..., 0] < 120)
    return a, m


def render(path, axes, bm):
    ys, xs = np.nonzero(bm)
    H = bm.shape[0]
    rows = np.nonzero(bm.any(1))[0]
    # split lines at the emptiest row in the middle third
    mid = [r for r in range(int(H * 0.45), int(H * 0.65))]
    split = min(mid, key=lambda r: bm[r].sum())
    l1 = bm[:split]; l2 = bm[split:]
    def bb(m, off=0):
        y, x = np.nonzero(m); return x.min(), y.min() + off, x.max() + 1, y.max() + 1 + off
    b1, b2 = bb(l1), bb(l2, split)
    best = None
    tgt_h, tgt_w = b1[3] - b1[1], b1[2] - b1[0]
    for tr_em in (-0.06, -0.04, -0.02, 0.0):
        for sy in (1.0, 1.08, 1.16):
            lo, hi = 8, 900
            while lo < hi:
                s = (lo + hi) // 2
                f = font(path, s, **axes)
                if word(f, "small", tr_em * s)[0].width < tgt_w: lo = s + 1
                else: hi = s
            f = font(path, lo, **axes)
            w1, _ = word(f, "small", tr_em * lo); w2, _ = word(f, "talk", tr_em * lo)
            if sy != 1.0:
                w1 = w1.resize((w1.width, round(w1.height * sy)), Image.LANCZOS)
                w2 = w2.resize((w2.width, round(w2.height * sy)), Image.LANCZOS)
            canvas = Image.new("L", (bm.shape[1], bm.shape[0]), 0)
            canvas.paste(w1, (b1[0], b1[3] - w1.height))
            cx2 = (b2[0] + b2[2]) / 2
            canvas.paste(w2, (int(cx2 - w2.width / 2), b2[3] - w2.height))
            cm = np.array(canvas) > 127
            iou = (bm & cm).sum() / (bm | cm).sum()
            if best is None or iou > best[0]:
                best = (iou, tr_em, lo, canvas, w1, w2, sy, w1.height / tgt_h)
    iou, tr, s, canvas, w1, w2, sy, hr = best
    # derived metrics at 390 css px
    asc_cap = w1.height / K
    line_gap = (b2[3] - b1[3]) / K  # baseline-to-baseline approx (both bottoms are baselines; no descenders in small/talk)
    indent = ((b2[0] + b2[2]) / 2 - (b1[0] + b1[2]) / 2) / K
    talk_left_offset = (int(cx2 - w2.width / 2) - b1[0]) / K
    return dict(iou=iou, track=tr, size=s / K, lh_px=line_gap, lh=line_gap / (s / K), talk_offset_px=talk_left_offset,
                centre_shift=indent, canvas=canvas, sy=sy, hr=hr)


def main():
    a, bm = board()
    rows = [("BOARD (board 2 frame 1 header, at 4x)", Image.fromarray(a.astype(np.uint8)))]
    res = []
    for name, path, axes in CANDS:
        r = render(path, axes, bm)
        im = Image.new("RGB", (bm.shape[1], bm.shape[0]), (253, 253, 252))
        im.paste(Image.new("RGB", im.size, (20, 18, 213)), (0, 0), r["canvas"])
        ov = np.array(im).copy(); ov[bm & ~(np.array(r["canvas"]) > 127)] = (255, 120, 0)
        rows.append((f"{name}: IoU {r['iou']:.3f}, {r['size']:.1f}px, tracking {r['track']:+.2f}em, line {r['lh_px']:.1f}px ({r['lh']:.2f}), talk x-offset {r['talk_offset_px']:+.1f}px, scaleY {r['sy']:.2f}",
                     Image.fromarray(ov)))
        res.append((name, r))
        print(f"{name:45s} IoU {r['iou']:.3f} size {r['size']:.1f} track {r['track']:+.2f} lh {r['lh_px']:.1f}px/{r['lh']:.2f} talk_off {r['talk_offset_px']:+.1f} centre_shift {r['centre_shift']:+.1f} scaleY {r['sy']:.2f} h/board {r['hr']:.2f}")
    W = max(im.width for _, im in rows) + 20
    sheet = Image.new("RGB", (max(W, 720), sum(im.height + 28 for _, im in rows)), "white")
    d = ImageDraw.Draw(sheet); y = 0
    for lab, im in rows:
        d.text((4, y + 6), lab, fill="black"); sheet.paste(im, (0, y + 24)); y += im.height + 28
    sheet.save(os.path.join(ROOT, "type", "compare-logo.png"))


if __name__ == "__main__":
    main()
