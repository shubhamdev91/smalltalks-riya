"""st-fable HD1 fixes (2026-10-10): Green Flag 3-layer (woman < phone < hand+receiver), Pinky clasp re-crop,
dedicated On Me hero cut. Updates manifest hd.batches.board-corrections-1 in place + verify sheet."""
import json, os
from PIL import Image, ImageDraw
import hd_batch1 as B1

ART = B1.ART
ASSETS = {
    "green-flag-phone": ("props", "green-flag", [("L-green-flag-phone", "landing")], "accepted",
                         ["REVISED 2026-10-10: smaller and further left as on board 3 (whole dial visible). Z-ORDER: above green-flag-woman (in front of her hair), below green-flag-hand.",
                          "minor: dial is plain cream (board/prompt: gold centre + black numbers)"]),
    "green-flag-hand": ("props", "green-flag", [("L-green-flag-hand", "landing")], "accepted",
                        ["NEW 2026-10-10: her hand + pink receiver cut from the same source at the SAME transform as green-flag-woman (pixel-aligned), hair between the fingers removed. Top layer: woman < phone < hand."]),
    "pinky-promise-scene": ("characters", "pinky-promise", [("L-pinky-promise-scene", "landing")], "accepted",
                            ["REVISED 2026-10-10: scale 0.45 (was 0.74) so the full clasp + lilac sleeve are in frame (clasp x ~204-354, sleeve bleeding right) with the face at board size; density 2.2x (was 1.35x)."]),
    "on-me-woman-hero": ("characters", "on-me", [("H-on-me-woman", "hero")], "accepted",
                         ["NEW 2026-10-10: dedicated hero frame-1 cut (head top to chin, bleed left + bottom behind the pill; right side sits under the main finger). Replaces any use of the landing on-me-woman in the hero.",
                          "source is 1200x800 (on-me-chapter): ~2x at the hero size is the maximum without upscaling"]),
}


def main():
    plan = json.load(open(os.path.join(B1.HD, "fitplan.json")))
    out = B1.export_assets(ASSETS, plan)
    mp = os.path.join(ART, "manifest.json")
    m = json.load(open(mp, encoding="utf-8"))
    b = m["hd"]["batches"]["board-corrections-1"]["assets"]
    b.update(out)
    gw = b["green-flag-woman"]
    gw["notes"] = [n for n in gw["notes"] if not n.startswith("includes the phone cord")] + [
        "LAYERS (2026-10-10): green-flag-woman (base) < green-flag-phone < green-flag-hand. The hand layer duplicates her hand+receiver pixel-aligned so the phone can sit in front of her hair."]
    if "on-me-woman" in b:
        b["on-me-woman"]["placements"] = [p for p in b["on-me-woman"]["placements"] if p["where"] != "hero"]
        b["on-me-woman"]["notes"].append("hero placement moved to on-me-woman-hero (2026-10-10)")
    json.dump(m, open(mp, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    verify(b)


def verify(A):
    SPEC = os.path.join(ART, "..", "spec", "crops")
    rows = []
    for crop, y0, h, names, key in (("landing-col2@390.png", 850, 865, ["green-flag-woman", "green-flag-phone", "green-flag-hand"], "top_css_in_section"),
                                    ("landing-col4@390.png", 850, 865, ["pinky-promise-scene"], "top_css_in_section"),
                                    ("hero-1-on-me@390.png", 0, 885, ["on-me-woman-hero"], "top_css_in_frame")):
        board = Image.open(os.path.join(SPEC, crop)).convert("RGBA").crop((0, y0, 390, y0 + h)); comp = board.copy()
        for n in names:
            a = A[n]; pl = [p for p in a["placements"] if key in p][0]
            im = Image.open(os.path.join(ART, a["web"])).convert("RGBA").resize((round(pl["width_css"]), round(pl["height_css"])), Image.LANCZOS)
            comp.alpha_composite(im, (round(pl["left_css"]), round(pl[key])))
        t = Image.new("RGB", (790, h), "white"); t.paste(board.convert("RGB"), (0, 0)); t.paste(comp.convert("RGB"), (400, 0)); rows.append(t)
    W = sum(r.width + 10 for r in rows); H = max(r.height for r in rows)
    s = Image.new("RGB", (W, H), "white"); x = 0
    for r in rows:
        s.paste(r, (x, 0)); x += r.width + 10
    s.resize((s.width // 2, s.height // 2), Image.LANCZOS).save(os.path.join(ART, "tests", "hd", "verify-fixes1-from-manifest.png"))


if __name__ == "__main__":
    main()
