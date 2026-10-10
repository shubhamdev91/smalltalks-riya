"""Batch E: Shaadi Shift full-face woman (owner ChatGPT, real alpha). Mask-only derivative: alpha clean (stlib.clean),
right-edge dupatta cut feathered (bottom-right only), trim; master lossless + web q92 at the chapter-women height.
Checks: fringe metrics, composites on white / black / pink / the Shaadi landing ground, fidelity colours vs reference."""
import hashlib, io, json, os, shutil, sys
import numpy as np
from PIL import Image, ImageDraw, ImageOps
from scipy import ndimage as ndi

sys.path.insert(0, os.path.dirname(__file__))
import stlib
import hd_intake as HI

ART = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ART, "chatgpt", "E", "Shaadi Shift Portrait with Gold Pin.png")
REF = os.path.join(ART, "ChatGPT-upload", "E", "1-shaadi-shift-reference.png")
HD = os.path.join(ART, "hd")
THEME_NAME = "st-hd-shaadi-shift-woman.webp"
WEB_H = 1022                     # wild-card-woman-v2 is 773 x 1022
GROUND = "#f30b5e"               # landing Shaadi Shift chapter ground (tokens.css)
FEATHER_X = 64                   # right-edge feather width (src px)
FEATHER_Y = (1150, 1235)         # feather weight ramps in over these rows (cut rows are 1265-1442)


def smooth(t):
    t = np.clip(t, 0, 1); return t * t * (3 - 2 * t)


def build():
    src = np.array(Image.open(SRC).convert("RGBA"))
    a = stlib.clean(src)                                  # alpha remap 24/232, largest component, rim defringe
    H, W = a.shape[:2]
    al = a[..., 3].astype(float)
    xr = smooth((W - 1 - np.arange(W)) / FEATHER_X)       # 0 at the right edge -> 1 inside
    wy = smooth((np.arange(H) - FEATHER_Y[0]) / (FEATHER_Y[1] - FEATHER_Y[0]))
    fade = 1 - wy[:, None] * (1 - xr[None, :])
    al *= fade
    a[..., 3] = np.round(al).astype(np.uint8)
    a[a[..., 3] == 0, :3] = 0
    a, box = HI.trim(a, pad=0)
    return src, a, box


def edge_report(a):
    al = a[..., 3]
    out = {}
    for n, l in (("top", al[0]), ("bottom", al[-1]), ("left", al[:, 0]), ("right", al[:, -1])):
        out[n] = {"solid_pct": round(float((l >= 200).mean() * 100), 1), "soft_pct": round(float(((l > 8) & (l < 200)).mean() * 100), 1)}
    return out


def med_lab(rgb, mask):
    return HI.srgb_to_lab(np.median(rgb[mask].reshape(-1, 3), 0)[None, :].astype(float))[0]


def colour_masks(rgb, alpha=None):
    f = rgb.astype(float); mx, mn = f.max(-1), f.min(-1); sat = (mx - mn) / np.maximum(mx, 1)
    r, g, b = f[..., 0], f[..., 1], f[..., 2]
    ok = np.ones(rgb.shape[:2], bool) if alpha is None else alpha >= 250
    pink = ok & (r > 170) & (g < 90) & (b > 50) & (b < 160) & (sat > 0.6)
    skin = ok & (r > 150) & (r < 235) & (g > 80) & (g < 160) & (b > 40) & (b < 120) & (r - g > 45) & (g - b > 15) & (sat > 0.35) & (sat < 0.7)
    gold = ok & (r > 190) & (g > 140) & (b < 90) & (r - b > 120)
    return {"dupatta_pink": pink, "skin": skin, "gold": gold}


def fidelity(a):
    ref = np.array(Image.open(REF).convert("RGB"))
    mr, mn = colour_masks(ref), colour_masks(a[..., :3], a[..., 3])
    res = {}
    for k in mr:
        if mr[k].sum() > 500 and mn[k].sum() > 500:
            l1, l2 = med_lab(ref, mr[k]), med_lab(a[..., :3], mn[k])
            res[k] = {"dE00": round(float(HI.de2000(l1[None], l2[None])[0]), 2), "ref_px": int(mr[k].sum()), "new_px": int(mn[k].sum())}
    g = HI.srgb_to_lab(np.array([stlib.hexrgb(GROUND)], float))
    res["dupatta_vs_ground_dE00"] = round(float(HI.de2000(med_lab(a[..., :3], mn["dupatta_pink"])[None], g)[0]), 2)
    return res


def on(a, colour, mirror=False):
    im = Image.fromarray(a)
    if mirror:
        im = ImageOps.mirror(im)
    bg = Image.new("RGBA", im.size, colour if isinstance(colour, tuple) else stlib.hexrgb(colour) + (255,))
    bg.alpha_composite(im); return bg.convert("RGB")


def sheet(src, a, web, out):
    grey = (128, 128, 128, 255)
    srcv = Image.new("RGBA", (src.shape[1], src.shape[0]), grey); srcv.alpha_composite(Image.fromarray(src))
    chk = Image.fromarray(HI.checker((a.shape[1], a.shape[0]))).convert("RGBA") if HI.checker((8, 8)).ndim == 3 else None
    if chk is None:
        chk = Image.new("RGBA", (a.shape[1], a.shape[0]), (200, 200, 200, 255))
    chk.alpha_composite(Image.fromarray(a))
    tiles = [("original (on grey)", srcv.convert("RGB")), ("cutout on checker", chk.convert("RGB")),
             ("on white", on(a, "#ffffff")), ("on black", on(a, "#000000")), ("on pink #ff0078", on(a, "#ff0078")),
             (f"on Shaadi ground {GROUND}, phone (unmirrored)", on(a, GROUND))]
    th = 520
    row1 = [(t, im.resize((round(im.width * th / im.height), th), Image.LANCZOS)) for t, im in tiles]
    # laptop mock: 1280 x 720 viewport strip on the ground, woman mirrored onto the right edge, bottom on the section bottom
    vw, vh = 1280, 720
    lap = Image.new("RGBA", (vw, vh), stlib.hexrgb(GROUND) + (255,))
    w = Image.fromarray(web); w = ImageOps.mirror(w)
    s = vh * 0.98 / w.height; w = w.resize((round(w.width * s), round(w.height * s)), Image.LANCZOS)
    lap.alpha_composite(w, (vw - w.width, vh - w.height))
    d = ImageDraw.Draw(lap); d.text((60, 300), "copy column (left)", fill=(255, 255, 255, 255))
    lap = lap.convert("RGB")
    # 100% crops: face/bindi, jhumka, pin, left-edge rim, feathered bottom-right
    H, W = a.shape[:2]
    crops = [("100% eyes + bindi", (300, 300, 640, 560)), ("100% jhumka", (360, 640, 600, 900)),
             ("100% pin", (580, 900, 940, 1220)), ("100% hair rim on white", (560, 120, 860, 420)),
             ("100% feathered right cut", (W - 260, H - 260, W, H))]
    crow = []
    for t, (x0, y0, x1, y1) in crops:
        bgc = "#ffffff" if "white" in t else GROUND
        crow.append((t, on(a, bgc).crop((x0, y0, x1, y1))))
    crow.append(("100% hair rim on black", on(a, "#000000").crop((560, 120, 860, 420))))
    Wt = max(sum(im.width + 10 for _, im in row1), lap.width + 10, sum(im.width + 10 for _, im in crow)) + 10
    Ht = th + 30 + lap.height + 30 + max(im.height for _, im in crow) + 30 + 10
    S = Image.new("RGB", (Wt, Ht), "white"); d = ImageDraw.Draw(S)
    x = 10
    for t, im in row1:
        d.text((x, 4), t, fill="black"); S.paste(im, (x, 20)); x += im.width + 10
    y = th + 30
    d.text((10, y), "laptop 1280x720 mock: web derivative mirrored, cut on the right screen edge, bottom on the section bottom", fill="black")
    S.paste(lap, (10, y + 16)); y += lap.height + 30
    x = 10
    for t, im in crow:
        d.text((x, y), t, fill="black"); S.paste(im, (x, y + 16)); x += im.width + 10
    S.save(out)


def md5(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()


def main():
    src, a, box = build()
    master = os.path.join(HD, "characters", "shaadi-shift-woman.webp")
    webp = os.path.join(HD, "characters", "shaadi-shift-woman.web.webp")
    Image.fromarray(a).save(master, "WEBP", lossless=True, quality=100, method=6)
    ww = round(a.shape[1] * WEB_H / a.shape[0])
    web = HI.resize_premul(a, (ww, WEB_H))
    b = io.BytesIO(); Image.fromarray(web).save(b, "WEBP", quality=92, alpha_quality=100, method=6)
    open(webp, "wb").write(b.getvalue())
    # read back the web file (what ships) for the checks
    web_rb = np.array(Image.open(webp).convert("RGBA"))
    rep = {"source": os.path.relpath(SRC, ART).replace("\\", "/"), "source_px": [src.shape[1], src.shape[0]],
           "source_alpha_note": "subject alpha was 252-253 (not 255); remapped to 255 by stlib.clean; 55 alpha-1 specks (117 px) dropped",
           "trim_box": list(box), "edges_master": edge_report(a), "edges_web": edge_report(web_rb),
           "fringe_master": HI.fringe_metrics(a), "fringe_web": HI.fringe_metrics(web_rb), "fidelity": fidelity(a),
           "feather": {"right_px": FEATHER_X, "rows_ramp": list(FEATHER_Y)}}
    out = os.path.join(ART, "tests", "hd", "contact-shaadi-shift-woman-E.png")
    sheet(src, a, web_rb, out)
    files = {"master": {"path": "hd/characters/shaadi-shift-woman.webp", "px": [a.shape[1], a.shape[0]], "bytes": os.path.getsize(master), "md5": md5(master)},
             "web": {"path": "hd/characters/shaadi-shift-woman.web.webp", "px": [ww, WEB_H], "bytes": os.path.getsize(webp), "md5": md5(webp),
                     "theme_asset": THEME_NAME}}
    rep["files"] = files; rep["contact_sheet"] = "tests/hd/contact-shaadi-shift-woman-E.png"
    json.dump(rep, open(os.path.join(ART, "tests", "hd", "batchE-report.json"), "w", encoding="utf-8"), indent=1)
    print(json.dumps(rep, indent=1))


if __name__ == "__main__":
    main()
