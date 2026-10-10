"""Phase 2 readjustment: crops, masks, feathering, composites of approved art. No redraw/recolour."""
import io, json, os, shutil
import numpy as np
from PIL import Image
from scipy import ndimage
from stlib import clean, BGS, hexrgb

ROOT = os.path.join(os.path.dirname(__file__), "..")
SRC = os.path.join(ROOT, "_source")
HANDLES = ["on-me", "brainwave", "diet-cherry", "green-flag", "shaadi-shift", "wild-card", "pinky-promise"]
PRODUCT = {"on-me": "bill-idhar", "brainwave": "haan-mera-idea-tha", "diet-cherry": "haan-wohi-wali",
           "green-flag": "tum-aa-jao-main-dekh-lungi", "shaadi-shift": "dulhan-tu-duty-meri",
           "wild-card": "achha-tum-pehle", "pinky-promise": "haath-do-main-hoon"}
REPORT = {}


def src(name):
    return np.array(Image.open(os.path.join(SRC, name)).convert("RGBA"))


def write(img, rel, budget=200000):
    """Lossless master + q>=92 web derivative within budget; returns entry with sizes and RGB delta."""
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    img.save(p, "WEBP", lossless=True, quality=100, method=6)
    wrel = rel.replace("/", "/web/", 1) if rel.count("/") else "web/" + rel
    wp = os.path.join(ROOT, wrel)
    os.makedirs(os.path.dirname(wp), exist_ok=True)
    for q in range(100, 91, -1):
        b = io.BytesIO()
        img.save(b, "WEBP", quality=q, alpha_quality=100, method=6)
        if b.tell() <= budget:
            break
    open(wp, "wb").write(b.getvalue())
    a = np.array(img.convert("RGBA"))
    r = np.array(Image.open(io.BytesIO(b.getvalue())).convert("RGBA"))
    m = a[..., 3] == 255
    d = np.abs(r[m, :3].astype(int) - a[m, :3].astype(int)) if m.any() else np.zeros((1, 3))
    return {"file": rel, "web": wrel, "width": img.width, "height": img.height,
            "bytes": os.path.getsize(p), "web_bytes": b.tell(), "web_quality": q,
            "web_within_budget": b.tell() <= budget,
            "web_rgb_delta_on_opaque": {"max": int(d.max()), "mean": round(float(d.mean()), 3)}}


def smooth(x):
    x = np.clip(x, 0, 1)
    return x * x * (3 - 2 * x)


# ---------------------------------------------------------------- characters
CHAR_CELLS = [(17, 323), (338, 639), (650, 929), (944, 1232), (1248, 1528), (1542, 1834), (1845, 2155)]
# board 2 hero placement: which panel edges sit off-canvas (no feather there)
BLEED = {"on-me": ["left", "bottom"], "brainwave": ["left", "top"], "diet-cherry": ["left"],
         "green-flag": ["right"], "shaadi-shift": ["left", "bottom"], "wild-card": ["left"],
         "pinky-promise": ["left", "top"]}
ANCHOR = {"left": 0.0, "right": 1.0, "top": 0.0, "bottom": 1.0}
F = 36  # feather width, source px


def characters():
    a = clean(src("desi-ink-characters-v2.png"), keep="all", min_area=20000)
    lab, _ = ndimage.label(a[..., 3] > 0)
    out = {}
    for h, (x0, x1) in zip(HANDLES, CHAR_CELLS):
        sub = a[:, x0 - 4:x1 + 4]
        ids = np.bincount(lab[:, x0 - 4:x1 + 4].ravel())
        ids[0] = 0
        keep = lab[:, x0 - 4:x1 + 4] == ids.argmax()
        sub = sub.copy()
        sub[~keep] = 0
        ys, xs = np.nonzero(sub[..., 3])
        cell = sub[ys.min():ys.max() + 1, xs.min():xs.max() + 1].copy()
        H, W = cell.shape[:2]
        # feather only the straight panel cuts (opaque pixels within 2 px of the bbox
        # sides/bottom), never the natural hair silhouette, and never a bleed edge
        op = cell[..., 3] > 128
        cut = np.zeros((H, W), bool)
        sides = {"left": (slice(None), slice(0, 2)), "right": (slice(None), slice(W - 2, W)),
                 "bottom": (slice(H - 2, H), slice(None)), "top": (slice(0, 2), slice(None))}
        for e, sl in sides.items():
            if e == "top" or e in BLEED[h]:
                continue
            cut[sl] = op[sl]
        dist = ndimage.distance_transform_edt(~cut) if cut.any() else np.full((H, W), 1e9)
        ramp = smooth(dist / F)
        al = cell[..., 3].astype(float) * ramp
        res = cell.copy()
        res[..., 3] = np.round(al).astype(np.uint8)
        res[res[..., 3] == 0, :3] = 0
        img = Image.fromarray(res)
        e = write(img, f"characters/{h}.webp")
        # verification: RGB where the result is still fully opaque equals the source
        m = res[..., 3] == 255
        e["rgb_delta_vs_source_on_opaque"] = int(np.abs(res[m, :3].astype(int) - cell[m, :3].astype(int)).max())
        ax = ANCHOR["left"] if "left" in BLEED[h] else ANCHOR["right"] if "right" in BLEED[h] else 0.5
        ay = ANCHOR["top"] if "top" in BLEED[h] else ANCHOR["bottom"] if "bottom" in BLEED[h] else 0.5
        e.update({"bleed_edges": BLEED[h], "feather_px": F, "anchor": {"x": ax, "y": ay},
                  "anchor_meaning": "pin this point of the image to the matching hero edge/corner; bleed edges sit at or past the canvas edge",
                  "css_width_at_390": 150, "css_width_note": f"native {W}px => 2x density at ~{W // 2} css px; do not exceed {W} css px",
                  "source": f"desi-ink-characters-v2.png x{x0}-{x1}"})
        out[h] = e
        print("char", h, e["width"], e["height"], e["bytes"], e["web_bytes"], e["rgb_delta_vs_source_on_opaque"])
    return out


# ---------------------------------------------------------------- chapters
FADE = 0.38  # top fraction faded to transparent in the -fade variant


def chapters():
    b = np.array(Image.open(os.path.join(SRC, "desi-ink-characters.png")).convert("RGB"))
    out = {}
    for i, h in enumerate(HANDLES):
        x0, x1 = round(i * 1916 / 7), round((i + 1) * 1916 / 7)
        x0 += 2; x1 -= 2  # drop the 1-2 px seam blend between panels
        panel = b[:, x0:x1]
        med = np.median(b[15:170, x0 + 15:x0 + 150].reshape(-1, 3), 0).astype(int)
        t = np.array(hexrgb(BGS[i]))
        img = Image.fromarray(panel).convert("RGBA")
        e = write(img, f"chapters/{h}.webp")
        # fade variant: top of the wall dissolves into the page's real campaign colour
        fa = np.array(img)
        Hh = fa.shape[0]
        y = np.arange(Hh)[:, None]
        fa[..., 3] = np.round(255 * smooth(y / (Hh * FADE))).astype(np.uint8).repeat(fa.shape[1], 1)
        fa[fa[..., 3] == 0, :3] = 0
        ef = write(Image.fromarray(fa), f"chapters/{h}-fade.webp")
        e.update({"fade_variant": ef, "ground_sampled": "#%02x%02x%02x" % tuple(med), "ground_target": BGS[i],
                  "ground_delta_rgb": (med - t).tolist(), "ground_match": bool(np.abs(med - t).max() <= 6),
                  "source": f"desi-ink-characters.png x{x0}-{x1}",
                  "resolution_note": f"{x1 - x0}px wide: 1x at {x1 - x0} css px, 2x only at <= {(x1 - x0) // 2} css px"})
        out[h] = e
        print("chap", h, e["width"], e["height"], e["web_bytes"], ef["web_bytes"], e["ground_delta_rgb"])
    return out


# ---------------------------------------------------------------- guide
def guide():
    raw = Image.open(os.path.join(SRC, "desi-nail-guide-v2.png")).convert("RGBA")
    e = write(raw, "guide/nail-guide-asis.webp")
    c = clean(np.array(raw))
    ec = write(Image.fromarray(c), "guide/nail-guide.webp")
    m = c[..., 3] == 255
    ec["rgb_delta_vs_source_on_opaque"] = int(np.abs(c[m, :3].astype(int) - np.array(raw)[m, :3].astype(int)).max())
    ec["note"] = "alpha cleanup only (despeckle stray red specks, snap 252/253 to 255); as-is copy is nail-guide-asis.webp"
    return {"cleaned": ec, "as_is": e}


# ---------------------------------------------------------------- shop finger states
STATE_ORDER = ["pinky-promise", "on-me", "brainwave", "green-flag", "shaadi-shift", "diet-cherry", "wild-card"]


def finger_states():
    a = clean(src("small-talk-seven-finger-states.png"), keep="all", min_area=20000)
    lab, n = ndimage.label(a[..., 3] > 0)
    objs = sorted([o for i, o in enumerate(ndimage.find_objects(lab)) if (lab[o] == i + 1).sum() > 20000],
                  key=lambda s: s[1].start)
    assert len(objs) == 7, len(objs)
    crops = []
    for o in objs:
        idx = np.bincount(lab[o].ravel()); idx[0] = 0
        c = a[o].copy(); c[lab[o] != idx.argmax()] = 0
        m = c[..., 3] > 128
        top = np.nonzero(m.any(1))[0][0]
        cx = np.nonzero(m[top:top + 80])[1].mean()
        crops.append((c, top, cx))
    half = max(max(cx, c.shape[1] - cx) for c, _, cx in crops)
    W = int(np.ceil(half)) * 2 + 8
    H = int(max(c.shape[0] - t for c, t, _ in crops)) + 6
    out = {}
    for h, (c, t, cx) in zip(STATE_ORDER, crops):
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        im.alpha_composite(Image.fromarray(c), (int(round(W / 2 - cx)), 6 - t))
        out[h] = write(im, f"shop/finger-state-{h}.webp", 120000)
        out[h]["tip_anchor"] = {"x": 0.5, "y": round(6 / H, 4), "meaning": "nail tip, same in all seven"}
    return out


# ---------------------------------------------------------------- lifestyle composites
def lifestyle():
    man = json.load(open(os.path.join(ROOT, "manifest.json")))
    hand = Image.open(os.path.join(ROOT, "hand", "preview-hand.webp")).convert("RGBA")
    import hand_export as HE
    meta = json.load(open(os.path.join(ROOT, "hand", "preview-hand.json")))
    W, H = hand.size
    out = {}
    for i, h in enumerate(HANDLES):
        cv = Image.new("RGBA", (W + 60, H + 40), hexrgb(BGS[i]) + (255,))
        layer = Image.new("RGBA", cv.size, (0, 0, 0, 0))
        ox, oy = 60, 0
        layer.alpha_composite(hand, (ox, oy))
        for slot, col in zip(meta["slots"], man["preview_slots"][h]):
            HE.place(layer, HE.nail_cell(h, col), ox, oy, slot, W, H, 1.0)
        cv.alpha_composite(layer)
        out[h] = write(cv.convert("RGB").convert("RGBA"), f"shop/lifestyle-{h}.webp")
        out[h]["columns"] = man["preview_slots"][h]
    return out


# ---------------------------------------------------------------- can + packaging
def can():
    a = src("desi-diet-can-v1.webp")
    rgb = a[..., :3].astype(int)
    red = (rgb[..., 0] > 170) & (rgb[..., 1] < 80) & (rgb[..., 2] < 80) & (a[..., 3] > 200)
    blk = (rgb.sum(-1) < 90) & (a[..., 3] > 200)
    region = np.zeros(red.shape, bool); region[150:700, 520:960] = True
    mark = (red | blk) & region
    ys = np.nonzero(mark.any(1))[0]
    y_end = int(ys.max())
    y0 = y_end + 24
    crop = Image.fromarray(a[y0:, :])
    rel = "rejected/can-crop-proposal-below-wordmark.webp"
    crop.save(os.path.join(ROOT, rel), "WEBP", quality=95)
    return {"source": "theme asset assets/desi-diet-can-v1.webp (theme 186649313493), 1189x1323",
            "brand_check": "FAIL: large legible 'Diet Coke' wordmark (black 'Diet' + red 'Coke' script) across the can",
            "wordmark_rows": [int(ys.min()), y_end], "crop_proposal": {"y_from": y0, "file": rel,
            "result": "lower can body + hand + 4 nails; no lettering. Loses the can top and the thumb nail."},
            "status": "not shipped; needs orchestrator/owner decision"}


def packaging():
    out = {}
    for h, p in PRODUCT.items():
        f = f"{p}-approved-package.png"
        im = Image.open(os.path.join(SRC, f)).convert("RGBA")
        e = write(im, f"packaging/{h}.webp")
        e.update({"source": f, "status": "awaiting hi-res from owner", "upscaled": False})
        out[h] = e
    return out


if __name__ == "__main__":
    R = {"characters": characters(), "chapters": chapters(), "guide": guide(),
         "shop_finger_states": finger_states(), "shop_lifestyle": lifestyle(), "diet_can": can(),
         "packaging": packaging()}
    json.dump(R, open(os.path.join(ROOT, "phase2.json"), "w"), indent=2)

