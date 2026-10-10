"""hero-v2 entries from st-fable's hero v3.4 notes (2026-10-10)."""
import json, os
import hd_batch1 as B1
ART = B1.ART
ASSETS = {
    "green-flag-woman-hero-v2": ("characters", "green-flag", [("H-green-flag-woman-v2", "hero")], "accepted",
        ["note 1: stray phone-outline slivers removed (largest-component cut); hair top feathered (source hair is cut at y=0)",
         "arm + coiled cord now continue down to the pill: scale 0.41 (was 0.32), bottom feathered behind the tone control. The source ends at its bottom edge, so reaching the pill needs this scale; her face is ~28% larger than v1. st-fable to judge vs board frame 4."]),
    "shaadi-shift-pin-hero-v2": ("props", "shaadi-shift", [("H-shaadi-shift-pin-v2", "hero")], "accepted",
        ["note 3: taller dupatta strip x 0-~115, y ~430-843 with the gold pin VERTICAL at x ~25-90, y ~620-750 as on board frame 5",
         "derived source hd/_derived/shaadi-shift-chapter-rot62.png = shaadi-shift-chapter.png rotated -61.6 deg (rotation only); face and the rotated source borders sit off-canvas left; top feathered under the headline"]),
    "pinky-promise-face-hero-v2": ("characters", "pinky-promise", [("H-pinky-promise-woman-v2", "hero")], "accepted",
        ["note 4: feather_right removed: full profile incl. cheek, lips and chin as on board frame 7; only a bottom fade at the jaw/shoulder"]),
}
def main():
    plan = json.load(open(os.path.join(B1.HD, "fitplan.json")))
    out = B1.export_assets(ASSETS, plan)
    mp = os.path.join(ART, "manifest.json"); m = json.load(open(mp, encoding="utf-8"))
    out["wild-card-woman-hero-v2"] = {"alias_of": "hd.batches.chatgpt-AB-1.assets.wild-card-woman-v2-hero", "status": "accepted",
        "notes": ["note 2: hero is cut from the A1 wild-card-chapter-v2 (long curly hair). That source also has its hair cut at y=0 (no extra headroom), so the top is feathered (0-70 src px); see tests/hd/wild-card-v2-split-check.png"]}
    m["hd"].setdefault("batches", {})["hero-v2"] = {"date": "2026-10-10", "from": "st-fable hero v3.4 notes", "assets": out,
        "supersedes": {"green-flag-woman-hero-v2": "green-flag-woman-hero", "shaadi-shift-pin-hero-v2": "shaadi-shift-pin-hero",
                       "pinky-promise-face-hero-v2": "pinky-promise-face-hero", "wild-card-woman-hero-v2": "wild-card-woman-hero (v1)"}}
    json.dump(m, open(mp, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
if __name__ == "__main__":
    main()
