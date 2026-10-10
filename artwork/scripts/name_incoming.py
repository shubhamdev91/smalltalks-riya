"""Copy ChatGPT downloads to canonical names (originals untouched). Order = the '-N' suffix ChatGPT puts on the
download name, cross-checked against file mtime order and a visual check (see hd/intake-map.json notes)."""
import glob, json, os, shutil
from pathlib import Path

ART = Path(__file__).resolve().parent.parent
B = ["on-me-nail-1", "on-me-nail-2", "on-me-nail-3", "brainwave-nail-1", "brainwave-nail-2", "brainwave-nail-3",
     "diet-cherry-nail-1", "diet-cherry-nail-2", "diet-cherry-nail-3", "green-flag-nail-1", "green-flag-nail-2",
     "shaadi-shift-nail-1", "shaadi-shift-nail-2", "shaadi-shift-nail-3", "wild-card-nail-1", "wild-card-nail-2",
     "wild-card-nail-3", "pinky-promise-nail-1", "finger-tone-1", "finger-tone-2", "finger-tone-3", "finger-tone-4"]
A = {1: "wild-card-chapter-v2", 2: "brainwave-chapter", 3: "diet-cherry-chapter", 4: "our-vision-woman"}
C = ["on-me-pdp-flatlay", "on-me-pdp-hand", "on-me-pdp-moment", "brainwave-pdp-flatlay", "brainwave-pdp-hand", "brainwave-pdp-moment",
     "diet-cherry-pdp-flatlay", "diet-cherry-pdp-hand", "diet-cherry-pdp-moment", "green-flag-pdp-flatlay", "green-flag-pdp-hand",
     "green-flag-pdp-moment", "shaadi-shift-pdp-flatlay", "shaadi-shift-pdp-hand", "shaadi-shift-pdp-moment", "wild-card-pdp-flatlay",
     "wild-card-pdp-hand", "wild-card-pdp-moment", "pinky-promise-pdp-flatlay", "pinky-promise-pdp-hand", "pinky-promise-pdp-moment",
     "guide-measure", "guide-apply", "guide-remove"]
# Folder C as delivered (orchestrator mapping 2026-10-10, verified by eye): suffix -> canonical; un-suffixed regenerations by name
C_BY_SUFFIX = {3: "on-me-pdp-hand", 4: "on-me-pdp-moment", 5: "brainwave-pdp-hand", 6: "brainwave-pdp-moment", 7: "diet-cherry-pdp-hand",
               8: "diet-cherry-pdp-moment", 9: "green-flag-pdp-flatlay", 10: "green-flag-pdp-hand", 11: "green-flag-pdp-moment",
               13: "shaadi-shift-pdp-flatlay", 14: "shaadi-shift-pdp-hand", 16: "shaadi-shift-pdp-moment", 17: "wild-card-pdp-flatlay",
               18: "wild-card-pdp-hand", 20: "wild-card-pdp-moment", 21: "pinky-promise-pdp-flatlay", 23: "pinky-promise-pdp-hand",
               24: "pinky-promise-pdp-moment", 25: "guide-measure", 26: "guide-apply", 28: "guide-remove"}
C_BY_NAME = {"Five-nail press-on fan in mustard": "on-me-pdp-flatlay", "Brainwave Cobalt Five-Nail Fan": "brainwave-pdp-flatlay",
             "Diet Cherry Five-Nail Fan": "diet-cherry-pdp-flatlay"}
SET_ASIDE = {("C", 1): "alternate diet-cherry-pdp-hand (fingers up, palm-side framing, 1312x1199 not square); -7 matches the prompt pose and finger order. Kept -7.",
             ("C", 2): "on-me-pdp-hand retry with the WRONG finger order (index->little burgundy, tortoise, gold, tortoise; prompt: tortoise, gold, tortoise, burgundy). -3 is correct. Rejected.",
             ("C", 12): "shaadi-shift flatlay alternate, wide 1536x1024 (square requested); same design as -13. Kept -13.",("A", 5): "retry of our-vision-woman (A4); visibly softer (eye-region Laplacian var 589 vs 851), background equivalent (dE00 1.4 vs 2.1). Kept A4."}


def order(f):
    stem = Path(f).stem
    return int(stem.rsplit("-", 1)[1]) if "-" in stem and stem.rsplit("-", 1)[1].isdigit() else None


def sub_for(canon):
    for st in ("on-me", "brainwave", "diet-cherry", "green-flag", "shaadi-shift", "wild-card", "pinky-promise"):
        if canon.startswith(st):
            return st
    return "_shared"


def main(folders=("A", "B", "C")):
    mp_path = ART / "hd" / "intake-map.json"
    mp = json.loads(mp_path.read_text()) if mp_path.exists() else {}
    for fold in folders:
        files = sorted(glob.glob(str(ART / "chatgpt" / fold / "*.png")), key=os.path.getmtime)
        by_mtime = [order(f) for f in files]
        for f in files:
            n = order(f)
            if (fold, n) in SET_ASIDE:
                mp.setdefault("_set_aside", [])
                rec = {"original": Path(f).relative_to(ART).as_posix(), "folder": fold, "order": n, "reason": SET_ASIDE[(fold, n)]}
                if rec not in mp["_set_aside"]:
                    mp["_set_aside"].append(rec)
                continue
            if fold == "C":
                canon = C_BY_SUFFIX.get(n) if n else C_BY_NAME.get(Path(f).stem)
            else:
                canon = {"A": A.get(n), "B": B[n - 1] if n and n <= len(B) else None}[fold]
            if not canon:
                mp.setdefault("_unmatched", []).append(Path(f).relative_to(ART).as_posix()); continue
            dst = ART / "chatgpt" / "named" / sub_for(canon) / f"{canon}.png"
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, dst)
            mp[canon] = {"original": Path(f).relative_to(ART).as_posix(), "folder": fold, "order": n,
                         "mtime_rank": files.index(f) + 1, "named": dst.relative_to(ART).as_posix()}
        print(fold, "files", len(files), "suffix order by mtime:", by_mtime)
    mp_path.write_text(json.dumps(mp, indent=1))


if __name__ == "__main__":
    import sys
    main(tuple(sys.argv[1:]) or ("A", "B"))
