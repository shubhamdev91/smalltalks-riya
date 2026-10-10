"""Mock of the chapter product-name highlight (marker swipe) on the board-3 chapter crops at 390.
Renders the proposed CSS geometry, then MEASURES the minimum contrast over every glyph pixel (text vs what is
actually under it), so the 4.5:1 claim is verified on pixels, not assumed. Mock only: the old baked name is covered
with the local ground colour (the real site renders live text)."""
import json, math, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from contrast import cr, L as relL

ROOT = os.path.join(os.path.dirname(__file__), "..")
FONT = os.path.join(ROOT, "fonts", "barlowsemicondensed", "BarlowSemiCondensed-Bold.ttf")
SETS = {  # name, col crop, name centre y (col coords), ground, highlight, text
    "on-me": ("On Me", 3, 1780, "#fbbe10", "#ffe59a", "#470100"),
    "brainwave": ("Brainwave", 2, 540, "#033bd6", "#dfe7ff", "#0a2a9e"),
    "diet-cherry": ("Diet Cherry", 1, 1507, "#d40319", "#ffd6d0", "#7a0010"),
    "green-flag": ("Green Flag", 2, 1302, "#046f41", "#cdeedb", "#013a1d"),
    "shaadi-shift": ("Shaadi Shift", 3, 1028, "#f30b5e", "#ffd3e3", "#8e0016"),
    "wild-card": ("Wild Card", 4, 449, "#aee60d", "#f2ffbf", "#0f0b5c"),
    "pinky-promise": ("Pinky Promise", 4, 1249, "#6919f9", "#e4d6ff", "#5e0412"),
}
FS = 26            # px at 390 (was 22 / 600)
PAD_X = 0.38       # em, band extends beyond the ink left/right
PAD_Y = 0.20       # em, band extends beyond the ink top/bottom (must exceed rotation lift + edge blur)
SKEW = -10         # deg (skewX)
ROT = -1.5         # deg
RADIUS = 0.42      # em
EDGE_BLUR = 0.8    # px, marker edge softness (CSS filter: blur on the ::before)
GLOW = (0, 0.55)   # soft flash peak opacity (ellipse)
GLOW_RX, GLOW_RY = 0.78, 1.45   # ellipse radii as a fraction of the stroke box (centre-aligned)
K = 4


def rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def render(key, bgcrop):
    name, col, cy, ground, hl, tx = SETS[key]
    f = ImageFont.truetype(FONT, FS * K)
    text = f"“{name}”"
    bb = f.getbbox(text)                       # ink box at K
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    W, H = bgcrop.size
    cx = W * K // 2
    cyk = (bgcrop.height // 2) * K
    ox, oy = cx - tw // 2 - bb[0], cyk - th // 2 - bb[1]
    # marker stroke: quad around ink + padding with uneven, angled ends (CSS clip-path polygon), rotated
    px, py = PAD_X * FS * K, PAD_Y * FS * K
    x0, y0, x1, y1 = cx - tw / 2 - px, cyk - th / 2 - py, cx + tw / 2 + px, cyk + th / 2 + py
    bw, bh = x1 - x0, y1 - y0
    poly = [(x0 + 0.03 * bw, y0 + 0.10 * bh), (x0 + 0.99 * bw, y0), (x0 + 0.97 * bw, y0 + 0.92 * bh), (x0, y0 + bh)]
    band = Image.new("L", (W * K, H * K), 0)
    ImageDraw.Draw(band).polygon(poly, fill=255)
    band = band.rotate(-ROT, resample=Image.BICUBIC, center=(cx, cyk))
    band = band.resize((W, H), Image.LANCZOS)
    core = np.array(band).astype(float) / 255
    soft = np.array(band.filter(ImageFilter.GaussianBlur(EDGE_BLUR))).astype(float) / 255
    # soft flash: elliptical radial gradient behind the stroke (CSS radial-gradient on ::after)
    yy, xx = np.mgrid[0:H, 0:W].astype(float)
    ex, ey = (bw / K) * GLOW_RX, (bh / K) * GLOW_RY
    rr = np.sqrt(((xx - cx / K) / ex) ** 2 + ((yy - cyk / K) / ey) ** 2)
    glow = np.clip(1 - rr, 0, 1) ** 1.6 * GLOW[1]
    base = np.array(bgcrop.convert("RGB")).astype(float)
    # mock only: remove the baked board name by diffusion inpainting of its pixels
    g = np.array(rgb(ground), float)
    reg = np.zeros((H, W), bool); reg[H // 2 - 18:H // 2 + 18, 70:320] = True
    reg &= ~(np.abs(base - np.array([255, 255, 255])).sum(-1) < 40) | True
    d = np.abs(base - base[reg].reshape(-1, 3).mean(0)).sum(-1)
    gdist = np.abs(base - g).sum(-1)
    ink = reg & (gdist > 90)              # anything clearly off the ground colour inside the old name strip
    from scipy import ndimage as ndi
    ink = ndi.binary_dilation(ink, iterations=3) & reg
    fill = base.copy()
    for _ in range(300):
        blur = np.stack([ndi.uniform_filter(fill[..., c], 5) for c in range(3)], -1)
        fill[ink] = blur[ink]
    base = fill
    h = np.array(rgb(hl), float)
    a = np.maximum(soft, glow)[..., None]
    comp = base * (1 - a) + h * a
    out = Image.fromarray(np.clip(comp, 0, 255).astype(np.uint8))
    # text
    tl = Image.new("L", (W * K, H * K), 0)
    ImageDraw.Draw(tl).text((ox, oy), text, font=f, fill=255)
    tl = tl.resize((W, H), Image.LANCZOS)
    tm = np.array(tl)
    out.paste(Image.new("RGB", out.size, rgb(tx)), (0, 0), tl)
    # verify: contrast of text colour vs what lies under every glyph pixel (alpha>=128)
    under = comp[tm >= 128]
    worst = min(cr(tx, "#%02x%02x%02x" % tuple(int(v) for v in p)) for p in np.unique(np.round(under).astype(int), axis=0))
    cov = float((soft[tm >= 128] >= 0.995).mean())
    return out, {"text_px": FS, "ink_box_px": [round(tw / K, 1), round(th / K, 1)], "band_box_px": [round((x1 - x0) / K, 1), round((y1 - y0) / K, 1)],
                 "min_contrast_text_vs_under_glyphs": round(worst, 2), "glyph_px_on_solid_core": round(cov, 4),
                 "text_vs_highlight": round(cr(tx, hl), 2), "text_vs_ground": round(cr(tx, ground), 2), "highlight_vs_ground": round(cr(hl, ground), 2)}


def main():
    tiles, res = [], {}
    for key, (name, col, cy, *_ ) in SETS.items():
        full = Image.open(os.path.join(ROOT, "crops", f"landing-col{col}@390.png")).convert("RGB")
        top = cy - 120
        crop = full.crop((0, top, 390, cy + 120))
        win = full.crop((0, cy - 30, 390, cy + 30))
        mock, r = render(key, win)
        crop.paste(mock, (0, 90))
        before = full.crop((0, top, 390, cy + 120))
        t = Image.new("RGB", (790, 262), "white"); t.paste(before, (0, 22)); t.paste(crop, (400, 22))
        ImageDraw.Draw(t).text((4, 4), f"{key}: board (before) | proposal   min contrast on glyphs {r['min_contrast_text_vs_under_glyphs']}:1, glyph px on solid core {r['glyph_px_on_solid_core']*100:.1f}%", fill="black")
        tiles.append(t); res[key] = r
        print(key, r)
    s = Image.new("RGB", (790 * 2 + 10, 262 * 4), "white")
    for i, t in enumerate(tiles):
        s.paste(t, ((i % 2) * 800, (i // 2) * 262))
    s.save(os.path.join(ROOT, "..", "artwork", "tests", "name-highlight-mock.png"))
    json.dump(res, open(os.path.join(ROOT, "name-highlight-check.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
