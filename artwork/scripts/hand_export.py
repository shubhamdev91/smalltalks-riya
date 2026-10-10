"""Export preview-hand.webp + preview-hand.json, then composite tests on all seven backgrounds."""
import json, math, os
import numpy as np
from PIL import Image
from hand import build
from stlib import save_webp, BGS, hexrgb

ROOT = os.path.join(os.path.dirname(__file__), "..")
SCALE = 0.5  # export scale from the 1086x1448 source
NAILS = json.load(open(os.path.join(ROOT, "nails", "manifest.json")))
CELL_W, CELL_H = NAILS["cell"]["width"], NAILS["cell"]["height"]
AX, AY = NAILS["anchor"]["x"], NAILS["anchor"]["y"]
SPRITE_NAIL_W = 185  # signature nail width inside a cell, px (182-187 across sets)

# Measured on the full-res thumbless hand (source px). Finger axes were read from the
# nail outlines (cuticle apex -> free edge); cuticles from the colour mask (index by eye).
SLOTS_SRC = [
    ("index", (163.8, 1151.1), (-0.66, 0.75), 72.0, 0),
    ("middle", (229.1, 1263.4), (-0.67, 0.74), 69.7, 6),
    ("ring", (371.8, 1270.0), (-0.69, 0.72), 70.0, 6),
    ("little", (573.8, 1221.1), (-0.68, 0.73), 64.0, 0),
]
DEFAULT_COLUMNS = [0, 1, 2, 0]  # signature, accent, extra, signature (orchestrator may override)


def main():
    full = build()
    ys, xs = np.nonzero(full[..., 3])
    x0, y0, x1, y1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
    crop = Image.fromarray(full[y0:y1, x0:x1]).convert("RGBa")
    W, H = round((x1 - x0) * SCALE), round((y1 - y0) * SCALE)
    hand = crop.resize((W, H), Image.LANCZOS).convert("RGBA")
    ha = np.array(hand)
    ha[ha[..., 3] == 0, :3] = 0
    hand = Image.fromarray(ha)
    path = os.path.join(ROOT, "hand", "preview-hand.webp")
    size, mode = save_webp(hand, path, 200)

    slots = []
    for name, (cx, cy), d, pw, side in SLOTS_SRC:
        d = np.array(d) / math.hypot(*d)
        rot = math.degrees(math.atan2(d[0], -d[1]))
        s_src = pw * 1.24 / SPRITE_NAIL_W          # cell scale in source px
        s = s_src * SCALE                          # cell scale in exported hand px
        cx, cy = cx - d[0] * 5, cy - d[1] * 5  # tuck the cuticle 5 src px under the fold
        cx, cy = cx - d[1] * side, cy + d[0] * side  # sideways nudge (+ = toward screen upper-left)
        px, py = (cx - x0) * SCALE, (cy - y0) * SCALE
        # cell centre = anchor + rotated offset from anchor to cell centre
        off = np.array([(0.5 - AX) * CELL_W, (0.5 - AY) * CELL_H]) * s
        r = math.radians(rot)
        ox = off[0] * math.cos(r) - off[1] * math.sin(r)
        oy = off[0] * math.sin(r) + off[1] * math.cos(r)
        slots.append({
            "finger": name,
            "cuticle": {"x": round(px / W, 4), "y": round(py / H, 4)},
            "center": {"x": round((px + ox) / W, 4), "y": round((py + oy) / H, 4)},
            "rotation_deg": round(rot, 1),
            "scale": round(s, 4),
            "cell_width_frac_of_hand": round(CELL_W * s / W, 4),
        })
    meta = {
        "file": "hand/preview-hand.webp", "width": W, "height": H, "bytes": size, "encoding": mode,
        "source": "desi-preview-hand-base.png, thumb removed with a smooth radial-edge contour, alpha cleaned, 0.5x",
        "enters_from": "top-right (wrist touches top and right edges of the image)",
        "display": {"recommended_css_width_px_at_390": 146,
                    "note": "interpretation of the 20-24% brief: the four-finger span (index tip to little-finger outer edge) is ~59% of the image width, so 146 css px of image gives a ~86 css px (22%) finger span; nails render ~13 css px wide. If the brief meant the whole image width, use 78-94 css px (nails ~8 px). File is 511 px wide = 3.5x at 146 css px."},
        "slot_convention": {
            "sprite_cell": [CELL_W, CELL_H], "sprite_anchor": [AX, AY],
            "how_to_place": "size the nail element to cell_width_frac_of_hand * hand width (aspect = cell), transform-origin at the sprite anchor (50% 92.5%), put that origin on `cuticle`, rotate(rotation_deg) clockwise. `center` is the same placement expressed as the cell centre (transform-origin 50% 50%).",
            "scale": "cell px -> exported hand px", "order": "index, middle, ring, little (visible top-left to bottom-right)",
            "default_columns": DEFAULT_COLUMNS},
        "slots": slots,
    }
    json.dump(meta, open(os.path.join(ROOT, "hand", "preview-hand.json"), "w"), indent=2)
    print("hand", W, H, size, mode)
    composite_tests(hand, meta)


def nail_cell(handle, col):
    sheet = Image.open(os.path.join(ROOT, "nails", f"{handle}.webp")).convert("RGBA")
    return sheet.crop((col * CELL_W, 0, (col + 1) * CELL_W, CELL_H))


def place(canvas, cell, ox, oy, slot, W, H, k=1.0):
    """Place via anchor+rotation (the documented contract) at hand offset ox,oy and zoom k."""
    s = slot["scale"] * k
    cw, ch = CELL_W * s, CELL_H * s
    c = cell.convert("RGBa").resize((max(1, round(cw)), max(1, round(ch))), Image.LANCZOS)
    # pad so rotation about the anchor keeps everything
    pad = int(max(cw, ch) * 2)
    big = Image.new("RGBa", (pad * 2, pad * 2), (0, 0, 0, 0))
    big.paste(c, (round(pad - AX * cw), round(pad - AY * ch)))
    big = big.rotate(-slot["rotation_deg"], resample=Image.BICUBIC, center=(pad, pad)).convert("RGBA")
    px = ox + slot["cuticle"]["x"] * W * k
    py = oy + slot["cuticle"]["y"] * H * k
    canvas.alpha_composite(big, (round(px - pad), round(py - pad)))


def composite_tests(hand, meta):
    handles = list(NAILS["sets"].keys())
    W, H = hand.size
    k = 1.0
    for i, h in enumerate(handles):
        nxt = handles[(i + 1) % 7]
        # hero-like crop: 390x? at 2x = 780 wide; hand top-right, partly off-canvas
        cv = Image.new("RGBA", (780, 900), hexrgb(BGS[i]) + (255,))
        layer = Image.new("RGBA", cv.size, (0, 0, 0, 0))
        ox, oy = 780 - W * k + 40, -80
        layer.alpha_composite(hand, (round(ox), round(oy)))
        for slot, col in zip(meta["slots"], DEFAULT_COLUMNS):
            place(layer, nail_cell(nxt, col), ox, oy, slot, W, H, k)
        cv.alpha_composite(layer)
        det = Image.new("RGBA", (W * 2, H * 2), hexrgb(BGS[i]) + (255,))
        dl = Image.new("RGBA", det.size, (0, 0, 0, 0))
        dl.alpha_composite(hand.resize((W * 2, H * 2), Image.LANCZOS))
        for slot, col in zip(meta["slots"], DEFAULT_COLUMNS):
            place(dl, nail_cell(nxt, col), 0, 0, slot, W, H, 2.0)
        det.alpha_composite(dl)
        det = det.crop((0, int(H * 1.2), int(W * 1.25), H * 2)).resize((780, round((H * 0.8) * 780 / (W * 1.25))), Image.LANCZOS)
        out = Image.new("RGBA", (1560, 900), hexrgb(BGS[i]) + (255,))
        out.alpha_composite(cv, (0, 0))
        out.alpha_composite(det, (780, (900 - det.height) // 2))
        out.convert("RGB").save(os.path.join(ROOT, "tests", f"hand-{i}-{h}-bg-with-{nxt}-nails.png"))


if __name__ == "__main__":
    main()





