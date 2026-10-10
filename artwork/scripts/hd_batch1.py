"""Batch 1 (board-corrections salvage): export fitted pieces from hd/fitplan.json -> hd/<group>/,
placements (css px at 390, section-relative for landing, frame-relative for hero), densities, contact sheets,
manifest.json -> hd.batches.board-corrections-1."""
import io, json, math, os
import numpy as np
from PIL import Image
import hdfit
import hd_intake as HI

ART = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
HD = os.path.join(ART, "hd")
TESTS = os.path.join(ART, "tests", "hd")
G = "chatgpt/_from-board-corrections/"
SEC_Y0 = {"diet-cherry": ("landing-col1", 1062), "on-me": ("landing-col3", 1320), "green-flag": ("landing-col2", 850), "shaadi-shift": ("landing-col3", 545),
          "brainwave": ("landing-col2", 0), "wild-card": ("landing-col4", 0), "pinky-promise": ("landing-col4", 850)}
SEC_H = {"diet-cherry": 638, "on-me": 1067, "green-flag": 865, "shaadi-shift": 775, "brainwave": 850, "wild-card": 850, "pinky-promise": 865}
SETC = {"diet-cherry": "#e10019", "on-me": "#ffb900", "brainwave": "#073df1", "green-flag": "#007948", "shaadi-shift": "#ff0078",
        "wild-card": "#b7ef00", "pinky-promise": "#6620f2", "journal": "#fdf6e9"}

# asset -> (group, set, [usages: (plan key, where)], status, notes)
ASSETS = {
    "on-me-woman": ("characters", "on-me", [("L-on-me-woman", "landing"), ("H-on-me-woman", "hero")], "accepted", []),
    "on-me-receipt-hand": ("props", "on-me", [("L-on-me-receipt-hand", "landing")], "accepted",
                           ["visible nails are all burgundy (4): matches board 3; prompt asked for burgundy+tortoise+gold. Board wins."]),
    "green-flag-woman": ("characters", "green-flag", [("L-green-flag-woman", "landing")], "accepted",
                         ["includes the phone cord + receiver; phone body is a separate asset (layer it BELOW the woman)"]),
    "green-flag-woman-hero": ("characters", "green-flag", [("H-green-flag-woman", "hero")], "accepted", ["bottom feathered (non-bleed cut)"]),
    "green-flag-phone": ("props", "green-flag", [("L-green-flag-phone", "landing")], "accepted",
                         ["minor: dial is plain cream (board/prompt: gold centre + black numbers)"]),
    "shaadi-shift-sweep": ("props", "shaadi-shift", [("L-shaadi-sweep", "landing")], "accepted", ["eye under dupatta + gold safety pin; replaces the v2 stand-in"]),
    "shaadi-shift-pin-hero": ("props", "shaadi-shift", [("H-shaadi-shift-prop", "hero")], "accepted", ["dupatta + pin only, face off-canvas per hero flag 2"]),
    "brainwave-sketchbook": ("props", "brainwave", [("L-brainwave-notebook", "landing")], "accepted",
                             ["replaces the F2 stand-in; crescent-bag sketches + blue pen, no machinery. Board's real bag + bottles are absent (not required)."]),
    "wild-card-woman": ("characters", "wild-card", [("L-wild-card-woman", "landing")], "interim", []),
    "wild-card-woman-hero": ("characters", "wild-card", [("H-wild-card-woman", "hero")], "interim", []),
    "wild-card-cards-hand": ("props", "wild-card", [("L-wild-card-cards-hand", "landing")], "interim", []),
    "wild-card-cards-hand-hero": ("props", "wild-card", [("H-wild-card-cards-hand", "hero")], "interim", []),
    "pinky-promise-scene": ("characters", "pinky-promise", [("L-pinky-promise-scene", "landing")], "interim", []),
    "pinky-promise-face-hero": ("characters", "pinky-promise", [("H-pinky-promise-woman", "hero")], "interim", []),
}
WILD_NOTES = ["INTERIM (owner edits coming). Woman is a short-bob character, not the board's long curly hair; teal top not lime/green saree.",
              "Card BACKS face the viewer (brief: correct). Backs are blue; board and prompt ask for red patterned backs.",
              "Nails lime / cobalt-white checker / blush-lime French: match the set."]
PINKY_NOTES = ["INTERIM (owner edits coming). One woman + a second person's hand from the right (board 3 composition); prompt asked for two women.",
               "Hands clasped, each wrist joined to its own arm, no extra/fused fingers seen at 3x. Nails lilac with burgundy asymmetric tip: match."]
for k in ASSETS:
    if k.startswith("wild-card"):
        ASSETS[k][4].extend(WILD_NOTES)
    if k.startswith("pinky"):
        ASSETS[k][4].extend(PINKY_NOTES)


def save_webs(arr, rel, web_w):
    p = os.path.join(HD, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    im = Image.fromarray(arr)
    im.save(p, "WEBP", lossless=True, quality=100, method=6)
    w = im
    if web_w < im.width:
        w = Image.fromarray(HI.resize_premul(arr, (web_w, round(im.height * web_w / im.width)))) if arr.shape[-1] == 4 else im.resize((web_w, round(im.height * web_w / im.width)), Image.LANCZOS)
    wrel = rel.replace(".webp", ".web.webp")
    b = io.BytesIO(); w.save(b, "WEBP", quality=92, alpha_quality=100, method=6)
    open(os.path.join(HD, wrel), "wb").write(b.getvalue())
    return {"file": f"hd/{rel}", "px": [im.width, im.height], "bytes": os.path.getsize(p),
            "web": f"hd/{wrel}", "web_px": [w.width, w.height], "web_bytes": b.tell()}


def export_assets(assets, plan):
    out = {}
    for name, (group, st, usages, status, notes) in assets.items():
        e0 = plan[usages[0][0]]
        pc = np.array(hdfit.piece(e0))
        # clip to the union of the regions visible at each usage (+8 css px margin): off-canvas pixels never render
        vis = np.zeros(pc.shape[:2], bool)
        for key, where in usages:
            e = plan[key]; s_ = e["width"] / (e["box"][2] - e["box"][0])
            if where == "landing":
                _, y0 = SEC_Y0[st]; ylo, yhi = y0, y0 + SEC_H[st] + 60
            else:
                ylo, yhi = 69, Image.open(os.path.join(hdfit.SPEC, e["board"])).height
            sx0 = max(0, int((0 - 8 - e["left"]) / s_)); sx1 = min(pc.shape[1], int(math.ceil((390 + 8 - e["left"]) / s_)))
            sy0 = max(0, int((ylo - 8 - e["top"]) / s_)); sy1 = min(pc.shape[0], int(math.ceil((yhi + 8 - e["top"]) / s_)))
            vis[sy0:sy1, sx0:sx1] = True
        pc[~vis] = 0
        t, (tx0, ty0, tx1, ty1) = HI.trim(pc, 0)
        scale0 = e0["width"] / (e0["box"][2] - e0["box"][0])
        places, css_ws = [], []
        for key, where in usages:
            e = plan[key]
            s = e["width"] / (e["box"][2] - e["box"][0])
            left = e["left"] + tx0 * s; top = e["top"] + ty0 * s; w = t.shape[1] * s
            css_ws.append(w)
            pl = {"where": where, "board_crop": f"spec/crops/{e['board']}", "scale_src_to_css": round(s, 4),
                  "left_css": round(left, 1), "width_css": round(w, 1), "height_css": round(t.shape[0] * s, 1),
                  "left_pct_of_390": round(left / 390 * 100, 2), "width_pct_of_390": round(w / 390 * 100, 2)}
            if where == "landing":
                col, y0 = SEC_Y0[st]
                pl.update({"section": f"chapter-{st}", "top_css_in_section": round(top - y0, 1), "column_crop": col})
            else:
                pl.update({"top_css_in_frame": round(top, 1), "top_css_in_scene": round(top - 69, 1)})
            places.append(pl)
        css_max = max(css_ws)
        web_w = min(t.shape[1], math.ceil(css_max * 3))
        rec = save_webs(t, f"{group}/{name}.webp", web_w)
        rec["density_at_spec"] = round(t.shape[1] / css_max, 2)
        rec["meets_3x"] = bool(t.shape[1] >= css_max * 3 - 1)
        fr = HI.fringe_metrics(t)
        rec.update({"set": st, "source": e0["src"], "source_box": e0["box"], "trim_in_box": [tx0, ty0, tx1, ty1],
                    "masks": {k: e0[k] for k in e0 if k.startswith(("mask", "feather"))},
                    "placements": places, "status": status, "notes": list(notes), "fringe": fr})
        if not rec["meets_3x"]:
            rec["notes"].append(f"below 3x: source gives {rec['density_at_spec']}x at the spec size (never upscaled)")
        sheet = os.path.join(TESTS, f"contact-{name}.png")
        HI.cutout_sheet(t, SETC[st], sheet, f"{name}: {t.shape[1]}x{t.shape[0]}, {rec['density_at_spec']}x at spec, {status}")
        rec["contact_sheet"] = os.path.relpath(sheet, ART).replace("\\", "/")
        out[name] = rec
        print(f"{name:28s} {status:9s} {t.shape[1]}x{t.shape[0]} css {css_max:.0f} -> {rec['density_at_spec']}x web {rec['web_px']} {rec['web_bytes']//1000}KB")
    return out


def main():
    plan = json.load(open(os.path.join(HD, "fitplan.json")))
    out = export_assets(ASSETS, plan)

    # journal pair: inset 6 px (drops the baked black outline + rounded corners; CSS radius 10), crop to tile aspect 182:210
    jp = np.array(Image.open(os.path.join(ART, G, "journal-pair.png")).convert("RGBA"))
    for name, (x0, x1), (y0, y1), note in (("journal-writing", (66, 592), (93, 700), "woman in glasses writing with a blue pen; nails are deep red/burgundy (not Brainwave cobalt): LND-034 alt needs updating"),
                                           ("journal-bag-notebook", (611, 1137), (75, 682), "black crescent bag + blue notebook + blue pen; LND-035 alt mentions a silver bag + sketchbook: update")):
        crop = jp[y0:y1, x0:x1, :3].copy()
        rec = save_webs(crop, f"journal/{name}.webp", min(crop.shape[1], 3 * 182))
        rec.update({"source": G + "journal-pair.png", "source_box": [x0, y0, x1, y1], "density_at_spec": round(crop.shape[1] / 182, 2),
                    "meets_3x": crop.shape[1] >= 545, "placements": [{"where": "landing journal teaser", "tile_css": [182, 210],
                    "radius_css": 10, "object_fit": "cover", "note": "left tile x 15-197, right x 205-380 (col2 y 1885-2095)"}],
                    "status": "accepted", "notes": ["opaque; baked black outline removed by a 6 px inset, CSS supplies the 10 px radius", note]})
        HI.photo_sheet(crop, os.path.join(TESTS, f"contact-{name}.png"), f"{name}: {crop.shape[1]}x{crop.shape[0]}")
        rec["contact_sheet"] = f"tests/hd/contact-{name}.png"
        out[name] = rec
        print(f"{name:28s} accepted  {crop.shape[1]}x{crop.shape[0]}")

    hand = json.load(open(os.path.join(ART, "hand", "hd", "preview-hand.json")))
    mp = os.path.join(ART, "manifest.json")
    m = json.load(open(mp, encoding="utf-8-sig"))
    hd = m.setdefault("hd", {})
    hd["criteria"] = "ACCEPTANCE.md > HD intake"
    hd.setdefault("batches", {})["board-corrections-1"] = {
        "date": "2026-10-09", "source_dir": "chatgpt/_from-board-corrections/ (originals: _source/board-corrections/)",
        "coords": "css px at 390; landing = section-relative (section y0 from spec/landing.md), hero = frame-relative incl. 69 px header",
        "assets": out,
        "preview_hand": {**hand, "status": "accepted", "contact_sheet": "tests/hd/contact-hd-hand.png",
                         "notes": ["photoreal bare-nail base, 4 fingers, thumb concealed, no baked nails; slots measured by hand",
                                   "canvas padded 48 px left / 96 px bottom so press-ons stay inside the image box",
                                   "slot convention unchanged from Phase 1 -> CONTRACT/motion only needs the new numbers"]}}
    json.dump(m, open(mp, "w", encoding="utf-8"), indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
