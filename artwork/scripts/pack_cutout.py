"""HD packaging cutouts (owner-D-1): the boxes are axis-aligned cartons on a white studio ground with a soft floor
shadow. Edges are found by robust line fits (column/row scans for the first strongly non-white pixel), the alpha is a
4x-supersampled rounded quad inset 0.5 px (no shadow, no white halo), and the 2 px rim RGB is taken from the nearest
interior pixel (decontamination). Output: lossless master, product-media q95, web ladder q85, checks."""
import hashlib, io, json, os, sys
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

ART = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
D = os.path.join(ART, "chatgpt", "D")
OUT = os.path.join(ART, "hd", "packaging-hd")
TESTS = os.path.join(ART, "tests", "hd")
BOXES = {"on-me": "Mustard ON ME nail carton-2.png", "diet-cherry": "Diet Cherry Almond Press-On Nail Package-4.png",
         "green-flag": "Emerald Green Flag Press-On Nail Package-5.png", "wild-card": "Wild Card Lime Nail Carton-7.png",
         "pinky-promise": "Pinky Promise Lavender Burgundy Nail Package-8.png",
         "brainwave": "Cobalt Blue Brainwave Nail Set-3.png", "shaadi-shift": "Shaadi Shift Wedding Tea Nail Set-6.png"}
ALT = {"shaadi-shift": "Clinking teacups on Shaadi Shift-10.png"}
WEB = os.path.join(ART, "hd", "packaging")
LADDER = [240, 360, 480, 720, 960]
DIST = 120      # Euclidean RGB distance from the white ground that counts as "box"
RADIUS = float(sys.argv[1]) if len(sys.argv) > 1 else 6.0
INSET = 0.6


def edge_scan(dist, axis, from_end):
    """For each line along `axis`, index of the first pixel (scanning inward) above DIST. Returns positions, valid mask."""
    m = dist > DIST
    if axis == 0:      # scan columns vertically
        arr = m[::-1] if from_end else m
        idx = np.argmax(arr, axis=0).astype(float); ok = arr.any(axis=0)
        if from_end: idx = m.shape[0] - 1 - idx
    else:              # scan rows horizontally
        arr = m[:, ::-1] if from_end else m
        idx = np.argmax(arr, axis=1).astype(float); ok = arr.any(axis=1)
        if from_end: idx = m.shape[1] - 1 - idx
    return idx, ok


def robust_line(t, v):
    """Fit v = a*t + b with iterative MAD rejection (the box edge is straight; content touching it is rejected)."""
    keep = np.ones(len(t), bool)
    for _ in range(6):
        a, b = np.polyfit(t[keep], v[keep], 1)
        r = v - (a * t + b); mad = np.median(np.abs(r[keep])) + 0.3
        keep = np.abs(r) < 3 * mad
    return a, b, int(keep.sum())


def fit_box(rgb):
    dist = np.sqrt(((rgb.astype(float) - 250.0) ** 2).sum(-1))
    m = dist > DIST
    ys, xs = np.nonzero(m)
    x0, x1, y0, y1 = np.percentile(xs, 1), np.percentile(xs, 99), np.percentile(ys, 1), np.percentile(ys, 99)
    lines = {}
    cols = np.arange(int(x0 + 0.1 * (x1 - x0)), int(x1 - 0.1 * (x1 - x0)))
    rows = np.arange(int(y0 + 0.1 * (y1 - y0)), int(y1 - 0.1 * (y1 - y0)))
    for name, axis, end, rng in (("top", 0, False, cols), ("bottom", 0, True, cols), ("left", 1, False, rows), ("right", 1, True, rows)):
        idx, ok = edge_scan(dist, axis, end)
        t = rng[ok[rng]]; v = idx[t]
        if name == "bottom":
            # the floor shadow passes the DIST test; the true edge is the dark contact line just above it
            L = rgb.astype(float).mean(-1)
            v2 = []
            for x, y in zip(t, v.astype(int)):
                lo = max(0, y - 35); win = L[lo:y + 1, x]
                v2.append(lo + int(np.argmin(win)) + 0.5)
            v = np.array(v2)
        # sub-pixel: edge at the DIST crossing between the outside pixel and the first inside pixel
        a, b, n = robust_line(t.astype(float), v)
        lines[name] = (a, b, n, len(t))
    return lines, dist


def corners(lines):
    """Intersections of top/bottom (y = a x + b) with left/right (x = a y + b)."""
    def inter(h, v):
        ah, bh = h[:2]; av, bv = v[:2]
        y = (ah * bv + bh) / (1 - ah * av); x = av * y + bv
        return x, y
    T, B, L, R = (lines[k] for k in ("top", "bottom", "left", "right"))
    return [inter(T, L), inter(T, R), inter(B, R), inter(B, L)]


def quad_alpha(shape, quad, radius, ss=4):
    """quad corners are edge positions (pixel boundaries for the bottom; first-inside pixel index elsewhere)."""
    H, W = shape
    cx = sum(p[0] for p in quad) / 4; cy = sum(p[1] for p in quad) / 4
    # inset each corner toward the centre by INSET px (keeps the anti-aliased rim inside the printed edge)
    q = []
    for x, y in quad:
        dx, dy = cx - x, cy - y; d = np.hypot(dx, dy)
        q.append((x + dx / d * INSET * 1.41, y + dy / d * INSET * 1.41))
    m = Image.new("L", (W * ss, H * ss), 0)
    dr = ImageDraw.Draw(m)
    # rounded quad: draw the polygon, then round the corners by eroding/dilating with a disc (morphological opening)
    dr.polygon([((x + 0.5) * ss, (y + 0.5) * ss) for x, y in q], fill=255)
    if radius > 0:
        r = int(round(radius * ss))
        a = np.array(m) > 127
        disc = np.hypot(*np.mgrid[-r:r + 1, -r:r + 1]) <= r
        a = ndimage.binary_opening(a, structure=disc)
        m = Image.fromarray((a * 255).astype(np.uint8))
    return np.array(m.resize((W, H), Image.LANCZOS)).astype(float) / 255.0


def decontaminate(rgba):
    a = rgba.astype(float); al = a[..., 3]
    inner = al >= 254
    inner = ndimage.binary_erosion(inner, iterations=2)
    _, (iy, ix) = ndimage.distance_transform_edt(~inner, return_indices=True)
    rim = (al > 0) & ~inner
    a[rim, :3] = a[iy[rim], ix[rim], :3]
    a[al == 0, :3] = 0
    return np.round(a).astype(np.uint8)


def md5(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()


def process(st, fn):
    src = np.array(Image.open(os.path.join(D, fn)).convert("RGB"))
    lines, dist = fit_box(src)
    quad = corners(lines)
    al = quad_alpha(src.shape[:2], quad, RADIUS)
    rgba = np.dstack([src, np.round(al * 255).astype(np.uint8)])
    rgba = decontaminate(rgba)
    ys, xs = np.nonzero(rgba[..., 3] > 0)
    bb = (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)
    cut = rgba[bb[1]:bb[3], bb[0]:bb[2]]
    os.makedirs(OUT, exist_ok=True)
    im = Image.fromarray(cut)
    mp = os.path.join(OUT, f"{st}.png"); im.save(mp, optimize=True)
    med = os.path.join(OUT, f"{st}-media.webp")
    b = io.BytesIO(); im.save(b, "WEBP", quality=95, alpha_quality=100, method=6); open(med, "wb").write(b.getvalue())
    ladder = {}
    for w in [w for w in LADDER if w < im.width] + [im.width]:
        h = round(im.height * w / im.width)
        r = im.convert("RGBa").resize((w, h), Image.LANCZOS).convert("RGBA") if w < im.width else im
        ra = np.array(r); ra[ra[..., 3] == 0, :3] = 0
        os.makedirs(WEB, exist_ok=True)
        p = os.path.join(WEB, f"{st}-{w}.web.webp")
        bb2 = io.BytesIO(); Image.fromarray(ra).save(bb2, "WEBP", quality=85, alpha_quality=100, method=6); open(p, "wb").write(bb2.getvalue())
        ladder[w] = {"path": os.path.relpath(p, ART).replace("\\", "/"), "px": [w, h], "bytes": bb2.tell(), "md5": md5(p)}
    # fringe check on the cut: light halo on the rim vs 5 px inside
    alpha = cut[..., 3]
    solid = alpha >= 128
    din = ndimage.distance_transform_edt(solid)
    rim = solid & (din <= 2); inner = solid & (din >= 5) & (din <= 7)
    _, (iy, ix) = ndimage.distance_transform_edt(~inner, return_indices=True)
    ry, rx = np.nonzero(rim)
    Lr = cut[ry, rx, :3].astype(float).mean(1); Li = cut[iy[ry, rx], ix[ry, rx], :3].astype(float).mean(1)
    halo = float(((Lr - Li > 40) & (Lr > 215)).mean())
    # edge residual: how far the fitted lines are from the per-line scan (px)
    rec = {"source": f"chatgpt/D/{fn}", "source_px": [src.shape[1], src.shape[0]], "box_px": [im.width, im.height], "box_bbox_in_source": list(bb),
           "corners": [[round(x, 2), round(y, 2)] for x, y in quad],
           "edge_fit": {k: {"slope": round(v[0], 5), "inliers": f"{v[2]}/{v[3]}"} for k, v in lines.items()},
           "corner_radius_px": RADIUS, "inset_px": INSET, "light_halo_frac": round(halo, 4),
           "master": {"path": os.path.relpath(mp, ART).replace("\\", "/"), "bytes": os.path.getsize(mp), "md5": md5(mp), "format": "PNG lossless RGBA"},
           "media": {"path": os.path.relpath(med, ART).replace("\\", "/"), "bytes": os.path.getsize(med), "md5": md5(med), "format": "WebP q95 RGBA, full resolution"},
           "ladder_q85": ladder}
    return rec, cut


def sheets(results, suffix=""):
    # 1) cutouts on dark + campaign colour, with 4x corner zooms
    BG = {"on-me": (255, 185, 0), "diet-cherry": (225, 0, 25), "green-flag": (0, 121, 72), "wild-card": (183, 239, 0), "pinky-promise": (102, 32, 242),
          "brainwave": (7, 61, 241), "shaadi-shift": (255, 0, 120)}
    rows = []
    for st, (rec, cut) in results.items():
        st = st.replace("-alt", "") if st.replace("-alt", "") in BG else st
        im = Image.fromarray(cut); s = 360 / im.height; sm = im.convert("RGBa").resize((round(im.width * s), 360), Image.LANCZOS).convert("RGBA")
        tiles = []
        for g in ((20, 20, 20), BG[st], (255, 255, 255)):
            b = Image.new("RGBA", sm.size, g + (255,)); b.alpha_composite(sm); tiles.append(b)
        H, W = cut.shape[:2]
        for (cx, cy) in ((0, 0), (W - 60, H - 60), (0, H - 60)):
            z = Image.new("RGBA", (60, 60), (20, 20, 20, 255)); z.alpha_composite(im.crop((cx, cy, cx + 60, cy + 60)))
            tiles.append(z.resize((240, 240), Image.NEAREST))
        z = Image.new("RGBA", (60, 60), (255, 255, 255, 255)); z.alpha_composite(im.crop((W // 2 - 30, H - 60, W // 2 + 30, H)))
        tiles.append(z.resize((240, 240), Image.NEAREST))
        row = Image.new("RGB", (sum(t.width + 6 for t in tiles), 366), "white"); x = 0
        for t in tiles:
            row.paste(t.convert("RGB"), (x, 0)); x += t.width + 6
        rows.append(row)
    s = Image.new("RGB", (max(r.width for r in rows), len(rows) * 372), "white")
    for i, r in enumerate(rows): s.paste(r, (0, i * 372))
    s.save(os.path.join(TESTS, f"contact-packaging-hd-cutouts{suffix}.png"))
    # 2) vs approved 370 px box at the same display size (370 px tall... use the approved box height)
    rows = []
    for st, (rec, cut) in results.items():
        old = Image.open(os.path.join(ART, "packaging", f"{st.replace('-alt', '')}.webp")).convert("RGBA")
        oa = np.array(old); ys, xs = np.nonzero(oa[..., 3] > 0); old = old.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
        new = Image.fromarray(cut).convert("RGBa").resize((round(cut.shape[1] * old.height / cut.shape[0]), old.height), Image.LANCZOS).convert("RGBA")
        row = Image.new("RGB", (old.width + new.width + 30, old.height + 20), (235, 235, 235))
        row.paste(old, (0, 20), old); row.paste(new, (old.width + 30, 20), new)
        ImageDraw.Draw(row).text((4, 4), f"{st}: approved {old.width}x{old.height}  |  HD {cut.shape[1]}x{cut.shape[0]} shown at the same height", fill="black")
        rows.append(row)
    s = Image.new("RGB", (sum(r.width + 10 for r in rows), max(r.height for r in rows)), "white"); x = 0
    for r in rows:
        s.paste(r, (x, 0)); x += r.width + 10
    s.save(os.path.join(TESTS, f"contact-packaging-hd-vs-approved{suffix}.png"))


def main():
    results = {st: process(st, fn) for st, fn in BOXES.items()}
    alts = {}
    for st, fn in ALT.items():
        global OUT, WEB
        keep = (OUT, WEB); OUT = WEB = os.path.join(ART, "rejected", "hd", "packaging-alt")
        r, cut = process(st + "-alt", fn); alts[st] = (fn, r, cut); OUT, WEB = keep
    sheets(results)
    sheets({f"{k}-alt": (r, c) for k, (fn, r, c) in alts.items()}, suffix="-alt")
    mp = os.path.join(ART, "manifest.json"); m = json.load(open(mp, encoding="utf-8"))
    m["hd"].setdefault("batches", {})["owner-D-1"] = m["hd"]["batches"].get("owner-D-1", {})
    m["hd"]["batches"]["owner-D-1"]["packaging_alts"] = {st: {"file": fn, "light_halo_frac": r["light_halo_frac"], "edge_fit": r["edge_fit"], "box_px": r["box_px"], "master_md5": r["master"]["md5"]} for st, (fn, r, _) in alts.items()}
    m["hd"]["batches"]["owner-D-1"]["packaging"] = {
        "date": "2026-10-10", "rule": "derivative only: rounded-quad alpha from robust edge fits, floor shadow removed, rim decontaminated; never upscaled",
        "owner_decisions_2026-10-10": {"brainwave": "ACCEPTED -3: the printed box reads 'Haan, mera idea hai.'; the old 'tha' packaging exception is retired (handle haan-mera-idea-tha stays)",
                                       "shaadi-shift": "ACCEPTED new box (tray pink, red, daisy, pink, red, daisy, red); -6 used, -10 recorded as rejected alternate"},
        "ladder_naming": "hd/packaging/<set>-<w>.web.webp, w in 240/360/480/720 + the box's own width (~863-867). No 960: the boxes are narrower than 960 and are never upscaled.",
        "boxes": {st: r for st, (r, _) in results.items()},
        "checks": ["tests/hd/contact-packaging-hd-cutouts.png", "tests/hd/contact-packaging-hd-vs-approved.png"]}
    json.dump(m, open(mp, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    for st, (fn, r, _) in alts.items():
        print("ALT", st, r["box_px"], "halo", r["light_halo_frac"], {k: v["inliers"] for k, v in r["edge_fit"].items()})
    for st, (r, _) in results.items():
        print(st, r["box_px"], "halo", r["light_halo_frac"], {k: v["inliers"] for k, v in r["edge_fit"].items()}, {k: round(v["slope"], 4) for k, v in r["edge_fit"].items()})


if __name__ == "__main__":
    main()
