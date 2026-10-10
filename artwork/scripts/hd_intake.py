"""HD intake for the ChatGPT v2 art pack (see ACCEPTANCE.md "HD intake").

Usage:  python hd_intake.py [--in DIR] [--out DIR] [--only NAME ...]
Defaults: --in ../chatgpt   --out ../hd   (contact sheets -> ../tests/hd, rejects listed, never deleted)

Per file: classify by name -> automatic checks -> cutout/key if needed -> fit/derive -> contact sheet.
Writes <out>/intake.json and merges an "hd" group into ../manifest.json (status from <out>/decisions.json,
which holds my visual verdicts; default "pending-visual"). Originals are never modified.
"""
import argparse, glob, io, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.normpath(os.path.join(HERE, ".."))

SETS = ["on-me", "brainwave", "diet-cherry", "green-flag", "shaadi-shift", "wild-card", "pinky-promise"]
SET_BG = {"on-me": "#ffb900", "brainwave": "#073df1", "diet-cherry": "#e10019", "green-flag": "#007948",
          "shaadi-shift": "#ff0078", "wild-card": "#b7ef00", "pinky-promise": "#6620f2"}
PROPS = {"on-me-receipt-hand", "brainwave-sketchbook", "diet-cherry-can-hand", "green-flag-phone",
         "shaadi-shift-fabric-pin", "wild-card-cards-hand"}
NAIL_COUNT = {"green-flag": 2, "pinky-promise": 1}
HD_CELL = (450, 780)          # x2.2 of the Phase-1 cell 204x354, same normalised anchor
P1_CELL = (204, 354)
ANCHOR = (0.5, 0.925)
HD_FINGER = (558, 1512)       # x1.8 of 310x840 (largest the ChatGPT finger sources support without upscaling)
FINGER_ANCHOR_Y = 0.2649
WEB_Q = 92


def hexrgb(h):
    h = h.lstrip("#"); return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], float)


# ---------------------------------------------------------------- colour science
def srgb_to_lab(rgb):
    c = np.asarray(rgb, float) / 255.0
    c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    M = np.array([[0.4124564, 0.3575761, 0.1804375], [0.2126729, 0.7151522, 0.0721750], [0.0193339, 0.1191920, 0.9503041]])
    xyz = c @ M.T / np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > 216 / 24389, np.cbrt(xyz), (24389 / 27 * xyz + 16) / 116)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], -1)


def de2000(l1, l2):
    L1, a1, b1 = np.moveaxis(np.asarray(l1, float), -1, 0)
    L2, a2, b2 = np.moveaxis(np.asarray(l2, float), -1, 0)
    C1, C2 = np.hypot(a1, b1), np.hypot(a2, b2)
    Cb = (C1 + C2) / 2
    G = 0.5 * (1 - np.sqrt(Cb ** 7 / (Cb ** 7 + 25 ** 7)))
    a1p, a2p = (1 + G) * a1, (1 + G) * a2
    C1p, C2p = np.hypot(a1p, b1), np.hypot(a2p, b2)
    h1p = np.degrees(np.arctan2(b1, a1p)) % 360
    h2p = np.degrees(np.arctan2(b2, a2p)) % 360
    dL, dC = L2 - L1, C2p - C1p
    dh = h2p - h1p
    dh = np.where(C1p * C2p == 0, 0, np.where(dh > 180, dh - 360, np.where(dh < -180, dh + 360, dh)))
    dH = 2 * np.sqrt(C1p * C2p) * np.sin(np.radians(dh / 2))
    Lb, Cbp = (L1 + L2) / 2, (C1p + C2p) / 2
    hs = h1p + h2p
    hb = np.where(C1p * C2p == 0, hs, np.where(np.abs(h1p - h2p) <= 180, hs / 2, np.where(hs < 360, (hs + 360) / 2, (hs - 360) / 2)))
    T = (1 - 0.17 * np.cos(np.radians(hb - 30)) + 0.24 * np.cos(np.radians(2 * hb)) + 0.32 * np.cos(np.radians(3 * hb + 6))
         - 0.20 * np.cos(np.radians(4 * hb - 63)))
    SL = 1 + 0.015 * (Lb - 50) ** 2 / np.sqrt(20 + (Lb - 50) ** 2)
    SC, SH = 1 + 0.045 * Cbp, 1 + 0.015 * Cbp * T
    RT = -2 * np.sqrt(Cbp ** 7 / (Cbp ** 7 + 25 ** 7)) * np.sin(np.radians(60 * np.exp(-((hb - 275) / 25) ** 2)))
    return np.sqrt((dL / SL) ** 2 + (dC / SC) ** 2 + (dH / SH) ** 2 + RT * (dC / SC) * (dH / SH))


def kmeans_lab(lab, k=3, it=12):
    X = lab.reshape(-1, 3)
    if len(X) > 40000:
        X = X[np.random.default_rng(0).choice(len(X), 40000, replace=False)]
    cent = np.percentile(X, np.linspace(10, 90, k), axis=0)
    for _ in range(it):
        lbl = np.argmin(((X[:, None, :] - cent[None]) ** 2).sum(-1), 1)
        for j in range(k):
            if (lbl == j).any():
                cent[j] = X[lbl == j].mean(0)
    w = np.bincount(lbl, minlength=k) / len(lbl)
    return cent, w


# ---------------------------------------------------------------- classification
def classify(stem):
    s = stem.lower()
    for st in SETS:
        if s == f"{st}-woman":
            return dict(kind="woman", set=st)
        m = re.fullmatch(rf"{st}-nail-(\d)", s)
        if m:
            return dict(kind="nail", set=st, col=int(m.group(1)) - 1)
        m = re.fullmatch(rf"{st}-pdp-(flatlay|hand|moment)", s)
        if m:
            return dict(kind="photo", set=st, role=m.group(1), ground=SET_BG[st])
        if s == f"{st}-pdp-packaging":
            return dict(kind="packaging", set=st)
    if s == "pinky-promise-pair":
        return dict(kind="woman", set="pinky-promise", pair=True)
    if s in PROPS:
        return dict(kind="prop", set=next(st for st in SETS if s.startswith(st)))
    m = re.fullmatch(r"finger-tone-(\d)", s)
    if m:
        return dict(kind="finger", tone=int(m.group(1)))
    if s == "our-vision-woman":
        return dict(kind="photo", set=None, role="our-vision", ground="#f6e7d2")
    m = re.fullmatch(r"guide-(measure|apply|remove)", s)
    if m:
        return dict(kind="photo", set=None, role=f"guide-{m.group(1)}", ground="#f4eff0")
    return dict(kind="unknown")


# ---------------------------------------------------------------- background analysis / keying
def border(a, w=6):
    return np.concatenate([a[:w].reshape(-1, a.shape[-1]), a[-w:].reshape(-1, a.shape[-1]),
                           a[:, :w].reshape(-1, a.shape[-1]), a[:, -w:].reshape(-1, a.shape[-1])])


def analyse_background(rgba):
    a = rgba.astype(float)
    alpha = a[..., 3]
    out = {"has_alpha": bool((alpha < 250).mean() > 0.02), "transparent_frac": round(float((alpha < 8).mean()), 3)}
    if out["has_alpha"]:
        out["type"] = "alpha"
        return out
    b = border(a[..., :3])
    med = np.median(b, 0)
    mad = np.median(np.abs(b - med), 0)
    out["border_median"] = "#%02x%02x%02x" % tuple(int(v) for v in med)
    out["border_mad"] = [round(float(v), 1) for v in mad]
    # painted checkerboard: low-sat, two grey levels in a corner patch
    patch = a[:96, :96, :3].reshape(-1, 3)
    sat = patch.max(1) - patch.min(1)
    L = patch.mean(1)
    lv = np.sort(L)
    lo, hi = lv[int(len(lv) * 0.25)], lv[int(len(lv) * 0.75)]
    if sat.mean() < 8 and lo > 150 and 10 < hi - lo < 90 and abs((L > (lo + hi) / 2).mean() - 0.5) < 0.2:
        out["type"] = "fake-checkerboard"
    elif mad.max() <= 8:
        out["type"] = "flat"
    else:
        out["type"] = "complex"
    return out


def key_flat(rgba, bg, t_lo=None, t_hi=None):
    """Key out a flat background colour. Background = bg-like region connected to the border,
    plus large flat enclosed holes. Soft alpha on a 3 px band; colour unmixing on the rim."""
    a = rgba[..., :3].astype(float)
    d = np.sqrt(((a - bg) ** 2).sum(-1))
    noise = np.median(np.abs(border(a) - bg).sum(-1)) + 1
    t_lo = t_lo or max(14.0, 3 * noise)
    t_hi = t_hi or t_lo + 45
    near = d < t_hi
    lab, n = ndimage.label(near)
    edge_ids = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    bgreg = np.isin(lab, list(edge_ids))
    # enclosed holes: flat components that are mostly very close to bg
    sizes = ndimage.sum(np.ones_like(d), lab, range(1, n + 1))
    core = ndimage.sum(d < t_lo, lab, range(1, n + 1))
    holes = [i + 1 for i in range(n) if (i + 1) not in edge_ids and sizes[i] > 400 and core[i] / sizes[i] > 0.9]
    bgreg |= np.isin(lab, holes)
    # known-F / known-B matting on an unknown band around the boundary:
    # F = colour of the nearest sure-foreground pixel, alpha = projection of (I-B) onto (F-B)
    sure_fg = ndimage.binary_erosion(~bgreg, iterations=4)
    unknown = ~sure_fg & ~(bgreg & (ndimage.distance_transform_edt(bgreg) > 2))
    alpha = np.where(bgreg, 0.0, 1.0)
    if sure_fg.any():
        _, (iy, ix) = ndimage.distance_transform_edt(~sure_fg, return_indices=True)
        uy, ux = np.nonzero(unknown)
        I = a[uy, ux]
        Fk = a[iy[uy, ux], ix[uy, ux]]
        FB = Fk - bg
        den = (FB ** 2).sum(1)
        proj = ((I - bg) * FB).sum(1) / np.maximum(den, 1e-6)
        dd = d[uy, ux]
        lin = np.clip((dd - t_lo) / (t_hi - t_lo), 0, 1)
        al_u = np.where(den > 30 ** 2, np.clip(proj, 0, 1), lin)
        al_u = np.where(dd < t_lo, 0.0, al_u)
        alpha[uy, ux] = al_u
    out = np.zeros_like(rgba, dtype=float)
    out[..., 3] = alpha * 255
    soft = (alpha > 0.02) & (alpha < 0.999)
    F = a.copy()
    F[soft] = (a[soft] - (1 - alpha[soft, None]) * bg) / alpha[soft, None]
    out[..., :3] = np.clip(F, 0, 255)
    out[alpha <= 0.02, :3] = 0
    out[alpha <= 0.02, 3] = 0
    # collision risk: subject colours inside the key tolerance (deep inside the subject, so not edge blend)
    interior = ndimage.binary_erosion(~bgreg, iterations=6)
    near_key = interior & (d < t_hi + 15)
    # bg region that reaches deep into the subject's bounding hull = likely eaten subject
    collision = float(near_key.sum() / max(interior.sum(), 1))
    return np.round(out).astype(np.uint8), {"t_lo": round(t_lo, 1), "t_hi": round(t_hi, 1), "holes_keyed": len(holes),
                                            "collision_frac": round(collision, 4)}


def despeckle(rgba, min_frac=0.001):
    al = rgba[..., 3]
    lab, n = ndimage.label(al > 16, structure=np.ones((3, 3)))
    if n <= 1:
        return rgba, []
    sizes = ndimage.sum(np.ones(al.shape), lab, range(1, n + 1))
    big = sizes.max()
    drop = [i + 1 for i, s in enumerate(sizes) if s < big * min_frac]
    flagged = [int(s) for s in sizes if big * min_frac <= s < big * 0.02]
    out = rgba.copy()
    out[np.isin(lab, drop)] = 0
    return out, flagged


def fringe_metrics(rgba):
    """Halo: outer 2 px of the silhouette vs. the colour 5 px inside. Sticker: near-white outline."""
    a = rgba.astype(float)
    al = a[..., 3]
    solid = al >= 128
    if solid.sum() < 100:
        return {"rim_px": 0}
    din = ndimage.distance_transform_edt(solid)
    rim = solid & (din <= 2)
    inner = solid & (din >= 5) & (din <= 7)
    _, (iy, ix) = ndimage.distance_transform_edt(~inner, return_indices=True)
    ry, rx = np.nonzero(rim)
    rc = a[ry, rx, :3]
    ic = a[iy[ry, rx], ix[ry, rx], :3]
    Lr, Li = rc.mean(1), ic.mean(1)
    satr = rc.max(1) - rc.min(1)
    light_halo = (Lr - Li > 45) & (Lr > 215) & (satr < 30)
    dark_halo = (Li - Lr > 70) & (Lr < 40)
    semi = (al > 8) & (al < 248)
    return {"rim_px": int(len(ry)), "light_halo_frac": round(float(light_halo.mean()), 4),
            "dark_halo_frac": round(float(dark_halo.mean()), 4), "semi_alpha_px": int(semi.sum())}


def trim(rgba, pad=6):
    ys, xs = np.nonzero(rgba[..., 3] > 0)
    y0, y1, x0, x1 = max(ys.min() - pad, 0), min(ys.max() + 1 + pad, rgba.shape[0]), max(xs.min() - pad, 0), min(xs.max() + 1 + pad, rgba.shape[1])
    return rgba[y0:y1, x0:x1], (int(x0), int(y0), int(x1), int(y1))


def resize_premul(rgba, size):
    im = Image.fromarray(rgba).convert("RGBa").resize(size, Image.LANCZOS).convert("RGBA")
    r = np.array(im)
    r[r[..., 3] == 0, :3] = 0
    return r


def save_pair(rgba_or_rgb, rel, max_long=None, lossless_master=True):
    """master (lossless webp) + web (q92, optional downscale) ; returns sizes."""
    arr = rgba_or_rgb
    im = Image.fromarray(arr)
    mp = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(mp), exist_ok=True)
    im.save(mp, "WEBP", lossless=True, quality=100, method=6) if lossless_master else im.save(mp, "WEBP", quality=95, method=6)
    w = im
    if max_long and max(im.size) > max_long:
        s = max_long / max(im.size)
        ns = (round(im.width * s), round(im.height * s))
        w = Image.fromarray(resize_premul(arr, ns)) if arr.shape[-1] == 4 else im.resize(ns, Image.LANCZOS)
    wrel = rel.replace(".webp", ".web.webp")
    wp = os.path.join(OUT, wrel)
    b = io.BytesIO()
    w.save(b, "WEBP", quality=WEB_Q, alpha_quality=100, method=6)
    open(wp, "wb").write(b.getvalue())
    return {"file": f"hd/{rel}", "px": list(im.size), "bytes": os.path.getsize(mp),
            "web": f"hd/{wrel}", "web_px": list(w.size), "web_bytes": b.tell(),
            "max_sharp_css_width_at_3x": round(w.width / 3)}


# ---------------------------------------------------------------- nails
def nail_shape(mask):
    ys, xs = np.nonzero(mask)
    h, w = ys.max() - ys.min() + 1, xs.max() - xs.min() + 1
    sub = mask[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    widths = sub.sum(1)
    top = widths[: max(1, int(h * 0.15))].mean()
    bot = widths[int(h * 0.70):].mean()
    return {"h": int(h), "w": int(w), "aspect": round(h / w, 2), "top15_w": round(float(top), 1), "bottom30_w": round(float(bot), 1),
            "tip_up": bool(top < bot * 0.8), "aspect_ok": bool(1.5 <= h / w <= 2.6)}


def p1_cell(st, col):
    sheet = np.array(Image.open(os.path.join(ART, "nails", f"{st}.webp")).convert("RGBA"))
    W = P1_CELL[0]
    return sheet[:, col * W:(col + 1) * W]


def nail_colour_check(rgba, ref):
    def lab_of(x):
        m = ndimage.binary_erosion(x[..., 3] > 250, iterations=3)
        return srgb_to_lab(x[..., :3][m])
    c1, w1 = kmeans_lab(lab_of(rgba))
    c2, w2 = kmeans_lab(lab_of(ref))
    used, pairs = set(), []
    for i in np.argsort(-w1):
        d = [(de2000(c1[i], c2[j]), j) for j in range(len(c2)) if j not in used]
        dmin, j = min(d)
        used.add(j); pairs.append((float(dmin), float(w1[i])))
    wde = sum(d * w for d, w in pairs) / sum(w for _, w in pairs)
    return {"weighted_de00": round(wde, 1), "cluster_de00": [round(d, 1) for d, _ in pairs], "pass": bool(wde < 12)}


def fit_nail(rgba, st, col):
    """Scale to the Phase-1 nail height x2.2 and place with the same normalised anchor in a 450x780 cell."""
    man = json.load(open(os.path.join(ART, "nails", "manifest.json")))
    box = man["sets"][st]["nail_boxes_px"][col]
    sx = HD_CELL[1] / P1_CELL[1]
    tgt_h = round(box["h"] * sx)
    t, _ = trim(rgba, 0)
    s = tgt_h / t.shape[0]
    nw, nh = max(1, round(t.shape[1] * s)), tgt_h
    note = None
    if nw > HD_CELL[0] - 8:
        s2 = (HD_CELL[0] - 8) / nw
        nw, nh = HD_CELL[0] - 8, round(nh * s2); note = "width-limited"
    if s > 1:
        note = (note or "") + " WOULD-UPSCALE"
    r = resize_premul(t, (nw, nh))
    cell = np.zeros((HD_CELL[1], HD_CELL[0], 4), np.uint8)
    ax, ay = round(ANCHOR[0] * HD_CELL[0]), round(ANCHOR[1] * HD_CELL[1])
    x0, y0 = ax - nw // 2, ay - nh
    cell[y0:y0 + nh, x0:x0 + nw] = r
    return cell, {"scale": round(s, 3), "nail_px": [nw, nh], "p1_nail_px": [box["w"], box["h"]],
                  "width_ratio_vs_p1": round(nw / (box["w"] * sx), 2), "note": note}


def assemble_sheets(results):
    """Per set: 3-col HD sheet once all its nails are accepted (equivalent columns duplicated)."""
    dec = load_decisions()
    out = {}
    for st in SETS:
        n = NAIL_COUNT.get(st, 3)
        cells = []
        for c in range(n):
            nm = f"{st}-nail-{c + 1}"
            p = os.path.join(OUT, "nails", "cells", f"{nm}.png")
            if not (os.path.exists(p) and dec.get(nm, {}).get("status") == "accepted"):
                cells = None; break
            cells.append(np.array(Image.open(p)))
        if not cells:
            continue
        while len(cells) < 3:
            cells.append(cells[-1])  # green-flag col2 == col1 ; pinky cols 1,2 == col0 (distinct_accents)
        sheet = np.concatenate(cells, 1)
        out[st] = save_pair(sheet, f"nails/{st}.webp")
        out[st]["cell"] = list(HD_CELL); out[st]["anchor"] = list(ANCHOR)
    return out


# ---------------------------------------------------------------- packaging
def block_ncc(a, b, grid=(10, 8)):
    ga, gb = a.mean(-1), b.mean(-1)
    H, W = ga.shape
    res = np.zeros(grid)
    for i in range(grid[0]):
        for j in range(grid[1]):
            ys, ye = i * H // grid[0], (i + 1) * H // grid[0]
            xs, xe = j * W // grid[1], (j + 1) * W // grid[1]
            p, q = ga[ys:ye, xs:xe].ravel(), gb[ys:ye, xs:xe].ravel()
            p, q = p - p.mean(), q - q.mean()
            den = np.sqrt((p * p).sum() * (q * q).sum())
            res[i, j] = (p * q).sum() / den if den > 1e-6 else 1.0
    return res


def compare_packaging(cut, st, sheet_path):
    orig = np.array(Image.open(os.path.join(ART, "packaging", f"{st}.webp")).convert("RGBA"))
    o, _ = trim(orig, 0)
    n, _ = trim(cut, 0)
    nr = resize_premul(n, (o.shape[1], o.shape[0]))
    on_w = lambda x: (x[..., :3] * (x[..., 3:] / 255.0) + 255 * (1 - x[..., 3:] / 255.0))
    A, B = on_w(o.astype(float)), on_w(nr.astype(float))
    ncc = block_ncc(A, B)
    diff = ndimage.gaussian_filter(np.abs(A - B).mean(-1), 1.5)
    # sheet: original x2 | new (downsized to original) x2 | diff heat x2 | text-zone crops at native new res
    k = 2
    oi = Image.fromarray(A.astype(np.uint8)).resize((o.shape[1] * k, o.shape[0] * k), Image.LANCZOS)
    ni = Image.fromarray(B.astype(np.uint8)).resize((o.shape[1] * k, o.shape[0] * k), Image.LANCZOS)
    hm = np.clip(diff * 3, 0, 255).astype(np.uint8)
    heat = Image.fromarray(np.stack([hm, np.zeros_like(hm), 255 - hm], -1)).resize(oi.size)
    top = int(o.shape[0] * 0.48)
    o_txt = Image.fromarray(A[:top].astype(np.uint8)).resize((o.shape[1] * 3, top * 3), Image.LANCZOS)
    n_full = on_w(n.astype(float)).astype(np.uint8)
    n_txt = Image.fromarray(n_full[: int(n.shape[0] * 0.48)])
    n_txt = n_txt.resize(o_txt.size, Image.LANCZOS)
    bot0 = int(o.shape[0] * 0.86)
    o_bot = Image.fromarray(A[bot0:].astype(np.uint8)).resize((o.shape[1] * 3, (o.shape[0] - bot0) * 3), Image.LANCZOS)
    n_bot = Image.fromarray(n_full[int(n.shape[0] * 0.86):]).resize(o_bot.size, Image.LANCZOS)
    Wt = oi.width * 3 + 40
    Ht = oi.height + 30 + o_txt.height + o_bot.height + 60
    sh = Image.new("RGB", (max(Wt, o_txt.width * 2 + 30), Ht), "white")
    d = ImageDraw.Draw(sh)
    for i, (lbl, im) in enumerate((("ORIGINAL approved", oi), ("NEW (downsized to original)", ni), ("|diff| heat", heat))):
        sh.paste(im, (i * (oi.width + 20), 24)); d.text((i * (oi.width + 20) + 4, 6), lbl, fill="black")
    y = oi.height + 40
    d.text((4, y - 14), "TEXT ZONE (top 48%) original x3 | new", fill="black")
    sh.paste(o_txt, (0, y)); sh.paste(n_txt, (o_txt.width + 30, y))
    y += o_txt.height + 30
    d.text((4, y - 14), "BOTTOM STRIP (ALMOND PRESS-ONS) original x3 | new", fill="black")
    sh.paste(o_bot, (0, y)); sh.paste(n_bot, (o_bot.width + 30, y))
    sh.save(sheet_path)
    return {"block_ncc_mean": round(float(ncc.mean()), 3), "block_ncc_min": round(float(ncc.min()), 3),
            "worst_blocks": [[int(i), int(j)] for i, j in zip(*np.unravel_index(np.argsort(ncc.ravel())[:3], ncc.shape))],
            "mean_abs_diff": round(float(diff.mean()), 1), "orig_px": [o.shape[1], o.shape[0]], "new_px": [n.shape[1], n.shape[0]]}


# ---------------------------------------------------------------- fingers
def fit_finger(rgba):
    """Bottom-entering finger: scale so its width at 75% height matches the Phase-1 tone-1 finger x2.2,
    centre it, place the estimated cuticle on the shared anchor. Anchor must be confirmed visually."""
    t, _ = trim(rgba, 0)
    m = t[..., 3] > 128
    H = m.shape[0]
    w75 = m[int(H * 0.75)].sum()
    ref = np.array(Image.open(os.path.join(ART, "fingers", "tone-1.webp")).convert("RGBA"))[..., 3] > 128
    rH = ref.shape[0]
    ref_rows = np.nonzero(ref.any(1))[0]
    r_top = ref_rows[0]
    ref_w = ref[int(r_top + (rH - r_top) * 0.75)].sum()
    s = (ref_w * HD_FINGER[0] / 310) / max(w75, 1)
    nw, nh = round(t.shape[1] * s), round(H * s)
    r = resize_premul(t, (nw, nh))
    # cuticle = proximal edge of the natural nail plate on its centre column (plate = pinkish, b/r > 0.62)
    rf = r.astype(float); br = rf[..., 2] / np.maximum(rf[..., 0], 1)
    plate = (r[..., 3] > 250) & (br > 0.62) & (rf[..., 0] > 150)
    plate[int(nh * 0.45):] = False
    plate = ndimage.binary_opening(plate, iterations=2)
    lab, nlab = ndimage.label(plate)
    if nlab:
        sz = ndimage.sum(plate, lab, range(1, nlab + 1)); pm = lab == (int(np.argmax(sz)) + 1)
        pm = ndimage.binary_fill_holes(ndimage.binary_closing(pm, iterations=6))
        pys, pxs = np.nonzero(pm); pcx = int(round(np.median(pxs)))
        cut_y = int(np.nonzero(pm[:, pcx - 3:pcx + 4].any(1))[0].max()); plate_w = int(pm.sum(1).max())
    else:
        pcx, cut_y, plate_w = nw // 2, int(nh * 0.25), 0
    canvas = np.zeros((HD_FINGER[1], HD_FINGER[0], 4), np.uint8)
    ay = round(FINGER_ANCHOR_Y * HD_FINGER[1])
    y0 = ay - cut_y
    x0 = HD_FINGER[0] // 2 - pcx
    ys0, ys1 = max(0, y0), min(HD_FINGER[1], y0 + nh)
    xs0, xs1 = max(0, x0), min(HD_FINGER[0], x0 + nw)
    canvas[ys0:ys1, xs0:xs1] = r[ys0 - y0:ys1 - y0, xs0 - x0:xs1 - x0]
    return canvas, {"scale": round(s, 3), "cuticle_src_px": [int(pcx), int(cut_y)], "plate_width_px": plate_w, "would_upscale": bool(s > 1),
                    "bottom_reaches_edge": bool(y0 + nh >= HD_FINGER[1]), "anchor_needs_visual_confirm": True}


# ---------------------------------------------------------------- contact sheets
def checker(size, s=16):
    y, x = np.mgrid[:size[1], :size[0]]
    c = (((x // s) + (y // s)) % 2) * 40 + 200
    return np.stack([c, c, c, np.full_like(c, 255)], -1).astype(np.uint8)


def cutout_sheet(rgba, setc, path, title):
    h = 360
    s = h / rgba.shape[0]
    sm = Image.fromarray(resize_premul(rgba, (max(1, round(rgba.shape[1] * s)), h)))
    grounds = [setc or "#fffaf0", "#ffffff", "#111111"]
    tiles = []
    for g in grounds:
        b = Image.new("RGBA", sm.size, tuple(int(v) for v in hexrgb(g)) + (255,)); b.alpha_composite(sm); tiles.append((g, b))
    ck = Image.fromarray(checker(sm.size)); ck.alpha_composite(sm); tiles.append(("checker", ck))
    # 3x zoom on the densest rim window (native pixels x3)
    al = rgba[..., 3]
    rim = ((al > 8) & (al < 248)).astype(float)
    dens = ndimage.uniform_filter(rim, 80)
    cy, cx = np.unravel_index(np.argmax(dens), dens.shape)
    y0, x0 = max(cy - 60, 0), max(cx - 60, 0)
    win = rgba[y0:y0 + 120, x0:x0 + 120]
    zooms = []
    for g in (setc or "#fffaf0", "#111111"):
        b = Image.new("RGBA", (win.shape[1], win.shape[0]), tuple(int(v) for v in hexrgb(g)) + (255,))
        b.alpha_composite(Image.fromarray(win)); zooms.append((f"3x rim on {g}", b.resize((win.shape[1] * 3, win.shape[0] * 3), Image.NEAREST)))
    W = sum(t.width + 10 for _, t in tiles) + sum(z.width + 10 for _, z in zooms)
    H = max(h, max(z.height for _, z in zooms)) + 30
    sh = Image.new("RGB", (W, H), "white"); d = ImageDraw.Draw(sh); x = 0
    d.text((4, 2), title, fill="black")
    for lbl, t in tiles + zooms:
        sh.paste(t.convert("RGB"), (x, 26)); d.text((x + 3, 14), lbl, fill="black"); x += t.width + 10
    sh.save(path)


def photo_sheet(rgb, path, title):
    im = Image.fromarray(rgb)
    s = 520 / max(im.size)
    sm = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    cy, cx = rgb.shape[0] // 2, rgb.shape[1] // 2
    crop = im.crop((cx - 150, cy - 150, cx + 150, cy + 150)).resize((450, 450), Image.NEAREST)
    sh = Image.new("RGB", (sm.width + crop.width + 20, max(sm.height, crop.height) + 24), "white")
    d = ImageDraw.Draw(sh); d.text((4, 4), title + "   | right: centre 300px at 1.5x", fill="black")
    sh.paste(sm, (0, 22)); sh.paste(crop, (sm.width + 20, 22)); sh.save(path)


def nail_sheet(cell, ref, st, path, title):
    sc = 0.5
    a = Image.fromarray(resize_premul(cell, (round(cell.shape[1] * sc), round(cell.shape[0] * sc))))
    r = Image.fromarray(resize_premul(ref, (a.width, a.height)))  # display-only enlargement of the P1 cell
    tiles = []
    for g in (SET_BG[st], "#ffffff"):
        for lbl, im in (("HD", a), ("P1 ref", r)):
            b = Image.new("RGBA", im.size, tuple(int(v) for v in hexrgb(g)) + (255,)); b.alpha_composite(im)
            dd = ImageDraw.Draw(b); ax, ay = ANCHOR[0] * b.width, ANCHOR[1] * b.height
            dd.line([(ax - 8, ay), (ax + 8, ay)], fill="cyan"); dd.line([(ax, ay - 8), (ax, ay + 8)], fill="cyan")
            tiles.append((f"{lbl} on {g}", b))
    sh = Image.new("RGB", (sum(t.width + 8 for _, t in tiles), a.height + 30), "white"); d = ImageDraw.Draw(sh)
    d.text((4, 2), title, fill="black"); x = 0
    for lbl, t in tiles:
        sh.paste(t.convert("RGB"), (x, 26)); d.text((x + 2, 14), lbl, fill="black"); x += t.width + 8
    sh.save(path)


# ---------------------------------------------------------------- decisions / manifest
def load_decisions():
    p = os.path.join(OUT, "decisions.json")
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}


def lap_var(rgb):
    g = rgb.astype(float).mean(-1)
    return float(ndimage.laplace(g).var())


# ---------------------------------------------------------------- main per-file
def process(path):
    stem = os.path.splitext(os.path.basename(path))[0]
    info = classify(stem)
    rec = {"source": os.path.relpath(path, ART).replace("\\", "/"), **info}
    src = Image.open(path)
    rec["source_px"] = list(src.size)
    rec["source_mode"] = src.mode
    rgba = np.array(src.convert("RGBA"))
    issues = []
    if max(src.size) < 1024:
        issues.append(f"small source {src.size} (<1024 long side)")
    sheet = os.path.join(TESTS, f"{stem}.png")
    kind = info["kind"]
    setc = SET_BG.get(info.get("set")) if info.get("set") else None

    if kind == "unknown":
        rec["status_auto"] = "unrecognised-name"
        return stem, rec

    if kind in ("woman", "prop", "nail", "finger", "packaging"):
        bgi = analyse_background(rgba)
        rec["background"] = bgi
        if bgi["type"] == "fake-checkerboard":
            issues.append("painted checkerboard instead of transparency: REJECT, ask for real alpha")
            rec["issues"] = issues; rec["status_auto"] = "reject"
            photo_sheet(rgba[..., :3], sheet, f"{stem}: fake checkerboard")
            rec["contact_sheet"] = os.path.relpath(sheet, ART).replace("\\", "/")
            return stem, rec
        if bgi["type"] == "flat":
            rgba, kinfo = key_flat(rgba, hexrgb(bgi["border_median"]))
            rec["keyed"] = {"bg": bgi["border_median"], **kinfo}
            if kinfo["collision_frac"] > 0.01:
                issues.append(f"key colour collides with the subject (collision {kinfo['collision_frac']:.2%}): check for bitten-out areas; re-export on a contrasting key colour if any")
        elif bgi["type"] == "complex":
            issues.append("non-flat opaque background: cannot key cleanly: REJECT (ask for transparent or flat set-colour bg)")
            rec["issues"] = issues; rec["status_auto"] = "reject"
            photo_sheet(rgba[..., :3], sheet, f"{stem}: complex background")
            rec["contact_sheet"] = os.path.relpath(sheet, ART).replace("\\", "/")
            return stem, rec
        rgba, flagged = despeckle(rgba)
        if flagged:
            issues.append(f"{len(flagged)} detached pieces kept (2%> size >0.1%): check visually")
        fr = fringe_metrics(rgba)
        rec["fringe"] = fr
        if fr.get("light_halo_frac", 0) > 0.02:
            issues.append(f"light halo on {fr['light_halo_frac']:.1%} of the rim")
        if fr.get("dark_halo_frac", 0) > 0.02:
            issues.append(f"dark halo on {fr['dark_halo_frac']:.1%} of the rim")
        cut, bbox = trim(rgba)
        rec["trim_box"] = bbox

        if kind == "nail":
            from stlib import clean as p1_clean
            cut = p1_clean(cut, keep="largest")          # snap alpha (<=24 -> 0, >=232 -> 255), drop faint specks/glow residue
            cut, _ = trim(cut, 0)
            shape = nail_shape(cut[..., 3] > 128)
            rec["shape"] = shape
            if not shape["tip_up"]:
                issues.append("tip not up (top narrower than base check failed)")
            if not shape["aspect_ok"]:
                issues.append(f"aspect {shape['aspect']} outside 1.5-2.6")
            ref = p1_cell(info["set"], info["col"])
            rt, _ = trim(ref, 0)
            rec["colour"] = nail_colour_check(cut, rt)
            if not rec["colour"]["pass"]:
                issues.append(f"colour ΔE00 {rec['colour']['weighted_de00']} vs sprite col {info['col']}")
            cell, fit = fit_nail(cut, info["set"], info["col"])
            rec["fit"] = fit
            if fit["note"] and "UPSCALE" in fit["note"]:
                issues.append("nail too small: fitting would upscale")
            os.makedirs(os.path.join(OUT, "nails", "cells"), exist_ok=True)
            Image.fromarray(cell).save(os.path.join(OUT, "nails", "cells", f"{stem}.png"))
            rec["cell_file"] = f"hd/nails/cells/{stem}.png"
            nail_sheet(cell, ref, info["set"], sheet, f"{stem} -> sprite col {info['col']}  ΔE00 {rec['colour']['weighted_de00']}")
        elif kind == "finger":
            canvas, fit = fit_finger(cut)
            rec["fit"] = fit
            if fit["would_upscale"]:
                issues.append("finger too small: fitting would upscale")
            rec.update(save_pair(canvas, f"fingers/tone-{info['tone']}.webp"))
            rec["canvas"] = list(HD_FINGER); rec["nail_bed_anchor"] = [0.5, FINGER_ANCHOR_Y]
            cutout_sheet(canvas, "#073df1", sheet, f"{stem}: plate cuticle -> anchor (0.5, {FINGER_ANCHOR_Y}), plate {fit['plate_width_px']}px")
        elif kind == "packaging":
            rec["compare"] = compare_packaging(cut, info["set"], sheet)
            if rec["compare"]["block_ncc_min"] < 0.5:
                issues.append(f"structural mismatch vs original (min block NCC {rec['compare']['block_ncc_min']})")
            rec.update(save_pair(cut, f"packaging/{info['set']}.webp", max_long=1100))
        else:
            sub = "women" if kind == "woman" else "props"
            rec.update(save_pair(cut, f"{sub}/{stem}.webp", max_long=1200))
            cutout_sheet(cut, setc, sheet, f"{stem}: {kind}, trimmed {cut.shape[1]}x{cut.shape[0]}")
    else:  # photo
        rgb = rgba[..., :3]
        if (rgba[..., 3] < 250).mean() > 0.01:
            issues.append("photo has transparency (expected opaque)")
        b = border(rgb.astype(float))
        med = np.median(b, 0)
        de = float(de2000(srgb_to_lab(med), srgb_to_lab(hexrgb(info["ground"]))))
        rec["ground"] = {"requested": info["ground"], "border_median": "#%02x%02x%02x" % tuple(int(v) for v in med), "de00": round(de, 1)}
        if de > 10:
            issues.append(f"ground ΔE00 {de:.1f} from requested {info['ground']} (flag, not recoloured)")
        rec["sharpness_lapvar"] = round(lap_var(rgb), 1)
        rec.update(save_pair(rgb, f"photos/{stem}.webp", max_long=1200, lossless_master=False))
        photo_sheet(rgb, sheet, f"{stem}: ground {rec['ground']['border_median']} (ΔE00 {de:.1f} vs {info['ground']}), lapvar {rec['sharpness_lapvar']}")
    rec["issues"] = issues
    rec["status_auto"] = "auto-pass" if not issues else "auto-flag"
    rec["contact_sheet"] = os.path.relpath(sheet, ART).replace("\\", "/")
    return stem, rec


def main():
    global OUT, TESTS
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", default=os.path.join(ART, "chatgpt"))
    ap.add_argument("--out", default=os.path.join(ART, "hd"))
    ap.add_argument("--tests", default=os.path.join(ART, "tests", "hd"))
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--no-manifest", action="store_true")
    a = ap.parse_args()
    OUT, TESTS = a.out, a.tests
    os.makedirs(OUT, exist_ok=True); os.makedirs(TESTS, exist_ok=True)
    files = sorted(glob.glob(os.path.join(a.inp, "**", "*.*"), recursive=True))
    files = [f for f in files if f.lower().endswith((".png", ".webp", ".jpg", ".jpeg"))]
    if a.only:
        files = [f for f in files if os.path.splitext(os.path.basename(f))[0] in a.only]
    ip = os.path.join(OUT, "intake.json")
    intake = json.load(open(ip, encoding="utf-8")) if os.path.exists(ip) else {}
    for f in files:
        stem, rec = process(f)
        intake[stem] = rec
        print(f"{stem:32s} {rec.get('kind'):9s} {rec.get('status_auto'):18s} {'; '.join(rec.get('issues', []))}")
    sheets = assemble_sheets(intake)
    json.dump(intake, open(ip, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    if not a.no_manifest:
        dec = load_decisions()
        mp = os.path.join(ART, "manifest.json")
        m = json.load(open(mp, encoding="utf-8-sig"))
        files_out = {}
        for k, r in intake.items():
            d = dec.get(k, {})
            files_out[k] = {**{x: r[x] for x in r if x not in ("background",)},
                            "status": d.get("status", "pending-visual"), "reason": d.get("reason", "")}
        m.setdefault("hd", {}).update({"criteria": "ACCEPTANCE.md > HD intake", "files": files_out, "nail_sheets": sheets,
                   "nail_cell": list(HD_CELL), "nail_anchor": list(ANCHOR), "finger_canvas": list(HD_FINGER),
                   "finger_anchor": [0.5, FINGER_ANCHOR_Y]})
        json.dump(m, open(mp, "w", encoding="utf-8"), indent=2, ensure_ascii=False)


OUT = TESTS = None
if __name__ == "__main__":
    main()
