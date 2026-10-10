"""Batch 2 (ChatGPT folders A + B, renamed copies in chatgpt/named/): chapter splits, Our Vision tile,
Brainwave pen hand, HD nail sheets + finger tones; writes manifest.json -> hd.batches["chatgpt-AB-1"]."""
import io, json, os
import numpy as np
from PIL import Image
import hd_batch1 as B1
import hd_intake as HI

ART = B1.ART
HD = B1.HD
TESTS = B1.TESTS
N = "chatgpt/named/"

WC_NOTES = ["v2 edit (A1): long curly hair, lime/green saree, red card BACKS to the viewer (faces toward her: brief rule; the hero board frame shows faces, the brief wins).",
            "Nails lime / cobalt-white checker / blush-lime French: match the set."]
ASSETS = {
    "brainwave-woman": ("characters", "brainwave", [("L-brainwave-woman", "landing")], "accepted",
                        ["glasses, gold hoop, blue floral top; replaces the v2-atlas character", "headline sits above this art (z-order); it overlaps the H of 'Haan' only in flat composites"]),
    "brainwave-woman-hero": ("characters", "brainwave", [("H-brainwave-woman", "hero")], "accepted", ["hero frame 2 half-face, bleed left+top"]),
    "diet-cherry-woman": ("characters", "diet-cherry", [("L-diet-cherry-woman", "landing")], "accepted", ["jhumka, black top; bleed left+bottom"]),
    "diet-cherry-can-hand": ("props", "diet-cherry", [("L-diet-cherry-can-hand", "landing")], "accepted",
                             ["silver can with the 'Diet Coke' wordmark as on board 3: owner-accepted (orchestrator decision c)",
                              "nails deep red + one blush with red French tip: match", "hand enters from the RIGHT, so it can't replace the hero frame-3 can (enters bottom-left; mirroring would reverse the wordmark). Hero keeps desi-diet-can-v1."]),
    "wild-card-woman-v2": ("characters", "wild-card", [("L-wild-card-v2-woman", "landing")], "accepted", WC_NOTES),
    "wild-card-cards-hand-v2": ("props", "wild-card", [("L-wild-card-v2-cards", "landing")], "accepted", WC_NOTES),
    "wild-card-woman-v2-hero": ("characters", "wild-card", [("H-wild-card-v2-woman", "hero")], "accepted", WC_NOTES + ["hero cut: right edge feathered left of the cards (css 104-158, under the main finger)"]),
    "wild-card-cards-hand-v2-hero": ("props", "wild-card", [("H-wild-card-v2-cards", "hero")], "accepted", WC_NOTES + ["wrist fades out behind the pill"]),
}


def main():
    plan = json.load(open(os.path.join(HD, "fitplan.json")))
    out = B1.export_assets(ASSETS, plan)

    # Brainwave pen hand: no board slot (board 3 Brainwave has no hand); exported for PDP / journal use
    src = np.array(Image.open(os.path.join(ART, N, "brainwave", "brainwave-chapter.png")).convert("RGBA"))
    pc = src[380:1024, 1020:1536].copy()
    t, tb = HI.trim(pc, 0)
    rec = B1.save_webs(t, "props/brainwave-pen-hand.webp", t.shape[1])
    rec.update({"set": "brainwave", "source": N + "brainwave/brainwave-chapter.png", "source_box": [1020, 380, 1536, 1024],
                "placements": [], "status": "accepted",
                "notes": ["no board slot: available for journal story / PDP moment", "nails cobalt / pearly white / silver chrome / cobalt: match", "real alpha, five fingers"],
                "fringe": HI.fringe_metrics(t)})
    HI.cutout_sheet(t, "#073df1", os.path.join(TESTS, "contact-brainwave-pen-hand.png"), f"brainwave-pen-hand {t.shape[1]}x{t.shape[0]}")
    rec["contact_sheet"] = "tests/hd/contact-brainwave-pen-hand.png"
    out["brainwave-pen-hand"] = rec

    # Our Vision tile: landing tile 1 = 183 x 263 css (col1 x 10-193, y 738-1001), radius 10, opaque
    ov = np.array(Image.open(os.path.join(ART, N, "_shared", "our-vision-woman.png")).convert("RGB"))
    H = ov.shape[0]; W = round(H * 183 / 263); x0 = 150
    crop = ov[:, x0:x0 + W]
    rec = B1.save_webs(crop, "tiles/our-vision-woman.webp", 3 * 183)
    rec.update({"source": N + "_shared/our-vision-woman.png (orig chatgpt/A/Burgundy Gold Eye Portrait-4.png)", "source_box": [x0, 0, x0 + W, H],
                "density_at_spec": round(W / 183, 2), "meets_3x": True,
                "placements": [{"where": "landing tiles, left (LND-010 'Our Vision')", "tile_css": [183, 263], "left_css": 10, "top_css_in_section": 16,
                                "radius_css": 10, "object_fit": "cover", "note": "col1 y 738-1001; section 'tiles' starts at col1 y 722"}],
                "status": "accepted",
                "notes": ["eye + hand on cheek, burgundy and gold almond nails, jhumka, bindi: matches board tile and prompt",
                          "cream ground #f8e6cb (dE00 2.1 vs requested #f6e7d2)", "A5 (retry) set aside: softer, see hd/intake-map.json"]})
    HI.photo_sheet(crop, os.path.join(TESTS, "contact-our-vision-woman.png"), f"our-vision tile {W}x{H}")
    rec["contact_sheet"] = "tests/hd/contact-our-vision-woman.png"
    out["our-vision-woman-tile"] = rec

    intake = json.load(open(os.path.join(HD, "intake.json"), encoding="utf-8"))
    fingers = {k: intake[k] for k in sorted(intake) if k.startswith("finger-tone")}
    sheets = {}
    for st in ("on-me", "brainwave", "diet-cherry", "green-flag", "shaadi-shift", "wild-card", "pinky-promise"):
        p = os.path.join(HD, "nails", f"{st}.webp"); wp = os.path.join(HD, "nails", f"{st}.web.webp")
        im = Image.open(p)
        sheets[st] = {"file": f"hd/nails/{st}.webp", "web": f"hd/nails/{st}.web.webp", "px": list(im.size),
                      "bytes": os.path.getsize(p), "web_bytes": os.path.getsize(wp), "cell": [450, 780], "anchor": [0.5, 0.925],
                      "columns": [f"{st}-nail-{i}" for i in (1, 2, 3)]}
    sheets["green-flag"]["columns"] = ["green-flag-nail-1", "green-flag-nail-2", "green-flag-nail-2 (dup: equivalent col)"]
    sheets["pinky-promise"]["columns"] = ["pinky-promise-nail-1"] * 3

    mp = os.path.join(ART, "manifest.json")
    m = json.load(open(mp, encoding="utf-8"))
    imap = json.load(open(os.path.join(HD, "intake-map.json")))
    # Wild Card v1 interim pieces are superseded by v2
    b1 = m["hd"]["batches"]["board-corrections-1"]["assets"]
    for k in ("wild-card-woman", "wild-card-woman-hero", "wild-card-cards-hand", "wild-card-cards-hand-hero"):
        if k in b1:
            b1[k]["status"] = "superseded"
            b1[k]["notes"].insert(0, "SUPERSEDED by hd.batches.chatgpt-AB-1 wild-card-woman-v2 / wild-card-cards-hand-v2")
    m["hd"]["batches"]["chatgpt-AB-1"] = {
        "date": "2026-10-09", "source_dirs": ["chatgpt/A", "chatgpt/B"], "renamed_copies": "chatgpt/named/<set>/<canonical>.png",
        "name_map": imap, "coords": m["hd"]["batches"]["board-corrections-1"]["coords"],
        "assets": out,
        "nail_sheets": {"rule": "drop-in for nails/web/<set>.webp: same 3-col layout and normalised anchor (0.5, 0.925), cells 450x780 = 2.2x the P1 204x354. Use the same CSS (background-size 300% 100%). Slot/finger scales in px must be divided by 2.2; cell_width_frac_of_hand needs no change.",
                        "status": "accepted", "sets": sheets},
        "finger_tones": {"rule": "drop-in for fingers/web/tone-N.webp: same normalised nail-bed anchor (0.5, 0.2649), canvas 558x1512 = 1.8x P1 310x840 (largest the sources allow without upscaling)",
                         "status": "accepted", "files": {k: {x: v[x] for x in ("file", "web", "px", "web_px", "bytes", "web_bytes", "fit", "canvas", "nail_bed_anchor", "source") if x in v} for k, v in fingers.items()},
                         "check": "tests/hd/fingers-anchor-hd.png"},
    }
    json.dump(m, open(mp, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print("written", list(out))


if __name__ == "__main__":
    main()
