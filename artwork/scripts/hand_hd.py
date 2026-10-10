"""HD preview hand from preview-four-hand.png: trim, export master + web, nail slots, composite tests.
Slots measured by hand on 2x gridded zooms (tests/hd/_n12.png, _n34.png): cuticle = centre of the
proximal nail fold, tip = centre of the free edge, width = plate width perpendicular to the axis."""
import json, math, os, io
import numpy as np
from PIL import Image
import hand_export as HE
from stlib import BGS, hexrgb

ART = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ART, "chatgpt", "_from-board-corrections", "preview-four-hand.png")
OUT = os.path.join(ART, "hand", "hd")
TESTS = os.path.join(ART, "tests", "hd")
SPRITE_NAIL_W = 185
WIDEN = 1.24          # press-on width vs natural plate width (same as the accepted Phase-1 fit)
TUCK = 0.07           # cuticle tuck under the fold, fraction of plate width
OLD_NAIL_CSS = 12.75  # visible nail width at the accepted 146-css Phase-1 hand -> keep the same on screen

# source px: (finger, cuticle, tip, plate_width, side_nudge_px)
SLOTS_SRC = [
    ("index", (230.0, 877.5), (172.5, 985.0), 76.0, 0),
    ("middle", (315.0, 967.5), (262.5, 1090.0), 105.0, 0),
    ("ring", (470.0, 1002.5), (417.5, 1110.0), 95.0, 0),
    ("little", (670.0, 972.5), (627.5, 1062.5), 74.5, 0),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    src = np.array(Image.open(SRC).convert("RGBA"))
    ys, xs = np.nonzero(src[..., 3] > 8)
    x0, y0, x1, y1 = int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1
    hand = src[y0:y1, x0:x1].copy()
    hand[hand[..., 3] == 0, :3] = 0
    # pad left/bottom so the press-ons (longer than the natural nails) stay inside the image box
    PADL, PADB = 48, 96
    hand = np.pad(hand, ((0, PADB), (PADL, 0), (0, 0)))
    x0 -= PADL
    W, H = hand.shape[1], hand.shape[0]
    css_w = round(OLD_NAIL_CSS * W / (SLOTS_SRC[0][3] * WIDEN))
    web_w = min(W, css_w * 3)
    master = Image.fromarray(hand)
    master.save(os.path.join(OUT, "preview-hand.webp"), "WEBP", lossless=True, quality=100, method=6)
    web = Image.fromarray(hand).convert("RGBa").resize((web_w, round(H * web_w / W)), Image.LANCZOS).convert("RGBA")
    wa = np.array(web); wa[wa[..., 3] == 0, :3] = 0; web = Image.fromarray(wa)
    b = io.BytesIO(); web.save(b, "WEBP", quality=92, alpha_quality=100, method=6)
    open(os.path.join(OUT, "preview-hand.web.webp"), "wb").write(b.getvalue())

    slots = []
    for name, (cx, cy), (tx, ty), pw, side in SLOTS_SRC:
        d = np.array([tx - cx, ty - cy]); d = d / np.linalg.norm(d)
        n = np.array([-d[1], d[0]])
        c = np.array([cx, cy]) - d * (TUCK * pw) + n * side
        rot = math.degrees(math.atan2(d[0], -d[1]))
        s_master = pw * WIDEN / SPRITE_NAIL_W            # sprite cell px -> master px
        px, py = c[0] - x0, c[1] - y0
        slots.append({"finger": name,
                      "cuticle": {"x": round(px / W, 4), "y": round(py / H, 4)},
                      "rotation_deg": round(rot, 1),
                      "scale_master": round(s_master, 4),
                      "scale": round(s_master * web_w / W, 4),
                      "cell_width_frac_of_hand": round(HE.CELL_W * s_master / W, 4),
                      "plate_width_src": pw})
    meta = {"file": "hand/hd/preview-hand.webp", "web": "hand/hd/preview-hand.web.webp",
            "master_px": [W, H], "web_px": [web_w, web.height], "bytes": os.path.getsize(os.path.join(OUT, "preview-hand.webp")),
            "web_bytes": b.tell(), "source": "chatgpt/_from-board-corrections/preview-four-hand.png (photoreal, bare natural nails, thumb concealed), trimmed box %s" % [x0, y0, x1, y1],
            "enters_from": "top-right (wrist touches top and right edges)",
            "display": {"recommended_css_width_px_at_390": css_w,
                        "rule": "keeps the rendered press-on width equal to the accepted Phase-1 hand (~12.75 css px); web file is 3x of that"},
            "slot_convention": {"sprite_cell": [HE.CELL_W, HE.CELL_H], "sprite_anchor": [HE.AX, HE.AY],
                                "how_to_place": "unchanged from Phase 1: nail element width = cell_width_frac_of_hand x rendered hand width (aspect = cell); transform-origin 50% 92.5% on `cuticle`; rotate(rotation_deg)",
                                "scale": "cell px -> web file px (scale_master: -> master px)",
                                "order": "index, middle, ring, little", "columns": "manifest.preview_slots"},
            "slots": slots}
    json.dump(meta, open(os.path.join(OUT, "preview-hand.json"), "w"), indent=2)
    print(json.dumps({k: meta[k] for k in ("master_px", "web_px", "bytes", "web_bytes", "display")}))
    for s in slots:
        print(s)
    composites(web, meta)


def composites(hand, meta):
    man = json.load(open(os.path.join(ART, "manifest.json"), encoding="utf-8"))
    sets = list(man["nails"]["sets"].keys())
    W, H = hand.size
    tiles = []
    for i, st in enumerate(sets):
        nxt = sets[(i + 1) % 7]
        cols = man["preview_slots"][nxt]
        cv = Image.new("RGBA", (W, H), hexrgb(BGS[i]) + (255,))
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); lay.alpha_composite(hand)
        for slot, col in zip(meta["slots"], cols):
            HE.place(lay, HE.nail_cell(nxt, col), 0, 0, slot, W, H, 1.0)
        cv.alpha_composite(lay)
        cv.convert("RGB").save(os.path.join(TESTS, f"hd-hand-{i}-{st}-bg-{nxt}-nails.png"))
        tiles.append(cv.convert("RGB").resize((W // 2, H // 2), Image.LANCZOS))
        if i == 0:
            big = hand.resize((W * 2, H * 2), Image.LANCZOS)
            cv2 = Image.new("RGBA", big.size, hexrgb(BGS[i]) + (255,)); l2 = Image.new("RGBA", big.size, (0, 0, 0, 0)); l2.alpha_composite(big)
            for slot, col in zip(meta["slots"], cols):
                HE.place(l2, HE.nail_cell(nxt, col), 0, 0, slot, W, H, 2.0)
            cv2.alpha_composite(l2)
            cv2.convert("RGB").crop((0, int(H * 1.2), int(W * 1.3), H * 2)).save(os.path.join(TESTS, "hd-hand-detail-2x.png"))
            bare = Image.new("RGBA", big.size, hexrgb(BGS[i]) + (255,)); bare.alpha_composite(big)
            bare.convert("RGB").crop((0, int(H * 1.2), int(W * 1.3), H * 2)).save(os.path.join(TESTS, "hd-hand-detail-2x-bare.png"))
    sheet = Image.new("RGB", (tiles[0].width * 4 + 30, tiles[0].height * 2 + 10), "white")
    for k, t in enumerate(tiles):
        sheet.paste(t, ((k % 4) * (t.width + 10), (k // 4) * (t.height + 10)))
    sheet.save(os.path.join(TESTS, "contact-hd-hand.png"))


if __name__ == "__main__":
    main()
