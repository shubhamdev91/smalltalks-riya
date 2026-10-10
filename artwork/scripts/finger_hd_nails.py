"""Main-nail fit on the HD fingers: press-on visible width = WIDEN x measured plate width, sprite cell anchor
(0.5, 0.925) on the finger nail-bed anchor. Writes the geometry into hd/fingers/geometry.json and test sheets."""
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw

ART = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
SETS = ["on-me", "brainwave", "diet-cherry", "green-flag", "shaadi-shift", "wild-card", "pinky-promise"]
BG = ["#ffb900", "#073df1", "#e10019", "#007948", "#ff0078", "#b7ef00", "#6620f2"]
WIDEN = float(sys.argv[1]) if len(sys.argv) > 1 else 1.08
TUCK = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0   # px (finger canvas) the press-on base sits below the natural cuticle


def rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def nail_w_in_cell(cell):
    a = np.array(cell)[..., 3] > 128
    return int(a.any(0).sum())


def main():
    geo = json.load(open(os.path.join(ART, "hd", "fingers", "geometry-measured.json")))
    plate = float(np.mean([g["plate_width_px"] for g in geo]))
    W, H = geo[0]["canvas"]
    ax, ay = W * 0.5, 0.2649 * H
    sheets = {st: Image.open(os.path.join(ART, "hd", "nails", f"{st}.webp")).convert("RGBA") for st in SETS}
    cw, ch = 450, 780
    nail_ws = [nail_w_in_cell(sheets[st].crop((0, 0, cw, ch))) for st in SETS]
    nail_w = float(np.median(nail_ws))
    cell_scale = WIDEN * plate / nail_w                    # HD cell px -> HD finger px
    cell_w_frac = cw * cell_scale / W
    rows = []
    for t in range(1, 5):
        f = Image.open(os.path.join(ART, "hd", "fingers", f"tone-{t}.webp")).convert("RGBA")
        row = []
        for i, st in enumerate(SETS):
            cell = sheets[st].crop((0, 0, cw, ch)).convert("RGBa").resize((round(cw * cell_scale), round(ch * cell_scale)), Image.LANCZOS).convert("RGBA")
            cv = Image.new("RGBA", (W, H), rgb(BG[i]) + (255,)); cv.alpha_composite(f)
            cv.alpha_composite(cell, (round(ax - 0.5 * cell.width), round(ay + TUCK - 0.925 * cell.height)))
            row.append(cv.crop((0, 0, W, int(H * 0.42))))
        rows.append(row)
    tw, th = rows[0][0].size
    s = Image.new("RGB", (7 * (tw // 2 + 4), 4 * (th // 2 + 4)), "white")
    for r, row in enumerate(rows):
        for c, im in enumerate(row):
            s.paste(im.convert("RGB").resize((tw // 2, th // 2), Image.LANCZOS), (c * (tw // 2 + 4), r * (th // 2 + 4)))
    s.save(os.path.join(ART, "tests", "hd", "fingers-hd-main-nail-all.png"))
    # 2x base zoom (cuticle region) for tone 1 + tone 4, 3 sets
    z = []
    for t in (1, 4):
        for st in ("brainwave", "shaadi-shift", "pinky-promise"):
            im = rows[t - 1][SETS.index(st)]
            z.append(im.crop((int(ax - 170), int(ay - 150), int(ax + 170), int(ay + 60))).resize((680, 420), Image.LANCZOS))
    zs = Image.new("RGB", (3 * 686, 2 * 426), "white")
    for k, im in enumerate(z):
        zs.paste(im.convert("RGB"), ((k % 3) * 686, (k // 3) * 426))
    zs.save(os.path.join(ART, "tests", "hd", "fingers-hd-main-nail-base-2x.png"))
    out = {"canvas": [W, H], "nail_bed_anchor": {"x": 0.5, "y": 0.2649, "px": [round(ax, 1), round(ay, 1)],
                                                  "meaning": "proximal edge (cuticle) of the natural nail plate on its centre line; identical in all four tones (measured 279/401 each)"},
           "natural_plate_width_px": round(plate, 1), "natural_plate_width_frac": round(plate / W, 4),
           "main_nail": {"rule": f"press-on visible width = {WIDEN} x natural plate width; sprite cell anchor (0.5, 0.925) on the nail-bed anchor" + (f", {TUCK}px lower" if TUCK else ""),
                         "hd_cell_scale": round(cell_scale, 4), "cell_width_frac_of_finger_canvas": round(cell_w_frac, 4),
                         "p1_cell_scale_equiv": round(cell_scale * 450 / 204 * 310 / W, 4),
                         "press_on_visible_width_px": round(WIDEN * plate, 1), "press_on_top_y_px": round(ay + TUCK - 0.925 * ch * cell_scale + (ch * 0.925 - 700) * cell_scale, 1),
                         "tuck_px": TUCK},
           "vs_phase1": "P1 fingers: anchor (0.5, 0.2649), cell 0.5 of canvas width (cell scale 0.76). HD: same anchor, cell %.3f of canvas width (main nail ~%.0f%% narrower relative to the finger)." % (cell_w_frac, (1 - cell_w_frac / 0.5) * 100),
           "checks": ["tests/hd/fingers-plate-measure.png", "tests/hd/fingers-hd-main-nail-all.png", "tests/hd/fingers-hd-main-nail-base-2x.png"]}
    json.dump(out, open(os.path.join(ART, "hd", "fingers", "geometry.json"), "w"), indent=1)
    print(json.dumps(out["main_nail"]), out["vs_phase1"], "nail_ws", nail_ws)


if __name__ == "__main__":
    main()
