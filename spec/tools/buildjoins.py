"""Build spec/joins.json: per landing section top edge, beeline segment (x_in/x_out chained), dash style,
clear zones; verify continuity + clearance + dash phase; render tests image spec/crops/joins-check.png."""
import json, os, re
import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.join(os.path.dirname(__file__), "..")
G = json.load(open(os.path.join(ROOT, "landing-geometry.json")))["joins"]

DASH, GAP = 9.0, 5.5
STYLE = {"on_colour": {"stroke": "#ffffff", "stroke_opacity": 0.9, "stroke_width": 2.5},
         "on_cream": {"stroke": "#c23a2c", "stroke_opacity": 1, "stroke_width": 2.0},
         "dasharray": [DASH, GAP], "linecap": "butt", "fill": "none"}


def mirror(path):
    def f(m):
        x, y = float(m.group(1)), m.group(2)
        return f"{390 - x:.0f},{y}"
    return re.sub(r"(-?[\d.]+),(-?[\d.]+)", f, path)


def edge(key, mirror_x=False):
    j = G[key]
    h = float(j["viewBox"].split()[-1])
    p = mirror(j["path_edge"]) if mirror_x else j["path_edge"]
    return p, h


# name, height, ground kind, top edge (path, h) or None, beeline control path (section-local, starts x_in,0 ends x_out,h), clear zones
S = []


def add(name, h, kind, top, bee, zones, art=None):
    S.append(dict(name=name, h=h, kind=kind, top=top, bee=bee, zones=zones, art=art or []))


add("hero", 653, "colour", None, None, [])
add("tiles", 340, "cream", edge("hero-to-tiles"), None, [])
add("chapter-diet-cherry", 638, "colour", edge("tiles-to-diet-cherry"),
    "M388,0 C372,24 356,46 356,52 C356,58 380,60 383,62 L383,520 C383,560 300,575 200,585 C110,595 60,605 40,638",
    [[85, 55, 295, 135, "note"], [65, 143, 350, 260, "headline"], [22, 280, 368, 413, "nails"], [110, 433, 285, 511, "name+pill"]],
    [[0, 395, 150, 638, "character"], [235, 395, 390, 638, "can-hand"]])
add("talks-teaser", 564, "cream", edge("diet-cherry-to-talks"),
    "M40,0 C46,20 56,40 50,60 C40,90 18,110 16,150 C14,200 10,240 10,300 C10,380 12,450 14,490 C16,530 20,550 22,564",
    [[105, 45, 310, 115, "heading"], [95, 125, 325, 160, "sub"], [40, 205, 150, 225, "label"],
     [20, 258, 350, 375, "example"], [40, 400, 360, 452, "pill"], [40, 465, 350, 555, "caption"]])
add("chapter-brainwave", 850, "colour", edge("brainwave-to-green-flag", True),
    "M22,0 C22,60 30,140 34,200 C38,260 26,310 10,340 C5,360 5,430 5,500 C5,560 40,610 90,630 C160,655 280,640 340,665 C380,690 386,760 386,850",
    [[130, 105, 370, 220, "note"], [60, 235, 365, 345, "headline"], [15, 365, 375, 500, "nails"], [105, 525, 295, 612, "name+pill"]],
    [[0, 0, 150, 350, "character (beeline passes under)"], [0, 610, 390, 850, "props strip"]])
add("chapter-green-flag", 865, "colour", edge("brainwave-to-green-flag"),
    "M386,0 C300,12 120,8 60,18 C28,28 10,60 8,110 L8,410 C8,450 30,470 60,482 C92,494 96,530 62,560 C30,600 20,700 30,865",
    [[75, 50, 300, 135, "note"], [35, 140, 385, 260, "sparkles+headline"], [15, 285, 375, 405, "nails"], [105, 440, 287, 522, "name+pill"]],
    [[0, 550, 215, 865, "phone"], [180, 460, 390, 865, "character"]])
add("journal-teaser", 672, "cream", edge("green-flag-to-journal"),
    "M30,0 C25,60 8,120 6,165 L6,385 C6,430 30,470 50,500 C64,520 64,560 58,590 C55,620 80,640 140,646 C220,652 300,640 370,672",
    [[85, 40, 310, 140, "heading"], [15, 170, 380, 380, "cards"], [65, 400, 340, 455, "pill"], [105, 510, 330, 595, "handwriting"]])
add("nail-guide-teaser", 545, "cream", None,
    "M370,0 C330,12 200,10 120,14 C50,18 14,30 10,80 L8,290 C8,330 60,350 64,386 C64,420 30,445 20,470 C12,500 14,530 30,545",
    [[40, 45, 370, 145, "eyebrow+heading"], [35, 165, 235, 250, "handwriting"], [45, 460, 350, 518, "pill"]],
    [[180, 175, 390, 450, "finger art"]])
add("chapter-shaadi-shift", 775, "colour", edge("nail-guide-to-shaadi"),
    "M30,0 C20,80 12,200 10,300 L8,440 C8,500 30,570 120,580 C220,585 300,600 360,640 C385,660 386,720 386,775",
    [[60, 80, 330, 145, "note"], [60, 160, 365, 285, "headline"], [22, 315, 368, 440, "nails"], [140, 470, 322, 555, "name+pill"]],
    [[0, 0, 70, 775, "dupatta strip"]])
add("chapter-on-me", 1067, "colour", edge("shaadi-to-on-me"),
    "M386,0 C330,14 140,4 60,14 C22,14 12,24 10,50 C9,120 8,180 8,230 L8,430 C8,560 30,700 60,800 C120,880 300,890 386,900 L386,1067",
    [[30, 40, 75, 100, "sparkles L"], [100, 60, 335, 160, "note"], [280, 130, 310, 170, "sparkles R"], [40, 190, 375, 260, "headline"],
     [22, 295, 368, 435, "nails"], [120, 455, 295, 540, "name+pill"], [50, 945, 330, 1030, "handwriting"]],
    [[0, 450, 190, 930, "character"], [160, 580, 390, 900, "hand+bill"]])
add("chapter-wild-card", 850, "colour", edge("wild-card-to-pinky", True),
    "M386,0 L386,540 C386,600 300,640 200,700 C100,760 20,780 14,850",
    [[55, 40, 330, 100, "note"], [300, 85, 330, 110, "sparkles"], [85, 105, 365, 230, "headline"], [15, 255, 375, 385, "nails"], [145, 435, 320, 522, "name+pill"]],
    [[0, 260, 150, 850, "character"], [100, 580, 390, 830, "cards-hand"]])
add("chapter-pinky-promise", 865, "colour", edge("wild-card-to-pinky"),
    "M14,0 L14,380 C14,430 60,470 100,500 C150,520 200,515 205,540 C222,570 222,610 200,640",
    [[30, 15, 385, 95, "note"], [70, 85, 360, 205, "headline"], [22, 240, 368, 360, "nails"], [120, 395, 298, 490, "name+pill"], [230, 515, 385, 650, "handwriting"]],
    [[0, 500, 390, 865, "character+hands (beeline passes under)"]])
add("shop-all-faq-footer", 633, "cream", edge("pinky-to-shop-all"), None, [])


def cubic_points(path, n=40):
    toks = re.findall(r"[MLC]|-?[\d.]+", path)
    pts, cur, i = [], None, 0
    while i < len(toks):
        t = toks[i]
        if t == "M":
            cur = (float(toks[i + 1]), float(toks[i + 2])); pts.append(cur); i += 3
        elif t == "L":
            p = (float(toks[i + 1]), float(toks[i + 2]))
            for s in np.linspace(0, 1, n)[1:]:
                pts.append((cur[0] + (p[0] - cur[0]) * s, cur[1] + (p[1] - cur[1]) * s))
            cur = p; i += 3
        elif t == "C":
            c1 = (float(toks[i + 1]), float(toks[i + 2])); c2 = (float(toks[i + 3]), float(toks[i + 4])); p = (float(toks[i + 5]), float(toks[i + 6]))
            for s in np.linspace(0, 1, n)[1:]:
                u = 1 - s
                pts.append((u ** 3 * cur[0] + 3 * u * u * s * c1[0] + 3 * u * s * s * c2[0] + s ** 3 * p[0],
                            u ** 3 * cur[1] + 3 * u * u * s * c1[1] + 3 * u * s * s * c2[1] + s ** 3 * p[1]))
            cur = p; i += 7
        else:
            i += 1
    return np.array(pts)


def main():
    out = {"convention": {
        "units": "css px at 390 wide; every section scales uniformly with width (multiply by 100vw/390)",
        "section_origin": "y=0 is the section's top = the highest point of its own top-edge curve; height h excludes the overlap below",
        "top_edge": "section clips itself with clip-path built from top_edge.path (viewBox 0 0 390 curve_h) + rect to bottom; it is pulled up by margin-top:-curve_h so it overlaps the section above",
        "beeline": "absolutely positioned SVG (viewBox 0 0 390 h), z-index above the ground and BELOW character/prop art and all text. Paths start at (x_in,0) and end at (x_out,h). x_out[n] == x_in[n+1]. The lower section draws on top, so the upper segment's last curve_h px are hidden behind it; both paths run vertically at that x through the overlap band, so the join reads continuous",
        "dash_phase": "set stroke-dashoffset = dashoffset to keep the dash rhythm continuous across sections (cumulative length mod (dash+gap))",
        "clear_zones": "rects [x0,y0,x1,y1,label] the beeline must stay >= 6 px away from; art_zones are drawn above the beeline (it may pass beneath)",
        "colour_switch": "stroke uses style.on_colour on chapter grounds, style.on_cream on cream sections",
    }, "style": STYLE, "sections": []}
    cum = 0.0
    prev_out = None
    problems = []
    tot_h = sum(s["h"] for s in S) + 10 * len(S)
    canvas = Image.new("RGB", (390, int(tot_h)), "white"); d = ImageDraw.Draw(canvas)
    y_off = 0
    for i, s in enumerate(S):
        e = None
        if s["top"]:
            p, ch = s["top"]
            e = {"path": p, "viewBox": f"0 0 390 {ch:.0f}", "curve_height_px": round(ch, 1),
                 "clip_polygon_hint": p + f" L390,{ch:.0f} L390,9999 L0,9999 L0,{ch:.0f} Z"}
        rec = {"order": i + 1, "section": s["name"], "height_px": s["h"], "ground": s["kind"], "top_edge": e or {"path": None, "curve_height_px": 0, "note": "straight join"},
               "clear_zones": s["zones"], "art_zones": s["art"]}
        col = (40, 40, 40) if s["kind"] == "cream" else (180, 180, 220)
        d.rectangle([0, y_off, 389, y_off + s["h"]], outline=col)
        d.text((4, y_off + 4), s["name"], fill=(0, 0, 0))
        for z in s["zones"]:
            d.rectangle([z[0], y_off + z[1], z[2], y_off + z[3]], outline=(255, 120, 0))
        for z in s["art"]:
            d.rectangle([z[0], y_off + z[1], z[2], y_off + z[3]], outline=(0, 160, 0))
        if s["bee"]:
            pts = cubic_points(s["bee"])
            x_in, x_out = pts[0][0], pts[-1][0]
            if abs(pts[0][1]) > 0.5:
                problems.append(f"{s['name']}: path must start at y=0")
            if prev_out is not None and abs(prev_out - x_in) > 0.5:
                problems.append(f"{s['name']}: x_in {x_in} != previous x_out {prev_out}")
            L = float(np.sum(np.linalg.norm(np.diff(pts, axis=0), axis=1)))
            for z in s["zones"]:
                inside = (pts[:, 0] > z[0] - 6) & (pts[:, 0] < z[2] + 6) & (pts[:, 1] > z[1] - 6) & (pts[:, 1] < z[3] + 6)
                if inside.any():
                    problems.append(f"{s['name']}: beeline within 6px of zone {z[4]}")
            rec["beeline"] = {"path": s["bee"], "viewBox": f"0 0 390 {s['h']}", "x_in": round(float(x_in), 1), "x_out": round(float(x_out), 1),
                              "ends_in_section": bool(abs(pts[-1][1] - s["h"]) > 0.5),
                              "length_px": round(L, 1), "dashoffset": round(float(-(cum % (DASH + GAP))), 2),
                              "style": "on_colour" if s["kind"] == "colour" else "on_cream"}
            cum += L
            prev_out = x_out if abs(pts[-1][1] - s["h"]) <= 0.5 else None
            colr = (255, 0, 200) if s["kind"] == "colour" else (200, 40, 40)
            dp = pts + [0, y_off]
            d.line([tuple(p) for p in dp], fill=colr, width=2)
        else:
            rec["beeline"] = None
            if prev_out is not None:
                problems.append(f"{s['name']}: previous beeline ends at bottom but this section has none")
            prev_out = None
        out["sections"].append(rec)
        y_off += s["h"] + 10
    out["single_section_screens"] = {
        "applies_to": ["shop", "product", "bag", "nail-guide", "talks", "conversation", "journal", "journal-story", "our-story", "help"],
        "header_to_main": {"path": None, "curve_height_px": 0, "note": "boards 4/5 show a straight join; header has no rule"},
        "main_to_footer": {"path": None, "curve_height_px": 0, "note": "straight; footer sits on the same paper colour, separated by 40-60 px space"},
        "beeline": None, "note": "boards 4 and 5 draw no beeline on inner screens",
    }
    out["verification"] = {"problems": problems, "continuity_ok": not any("x_in" in p for p in problems)}
    json.dump(out, open(os.path.join(ROOT, "joins.json"), "w"), indent=1)
    canvas.save(os.path.join(ROOT, "crops", "joins-check.png"))
    print("problems:", problems or "none")


if __name__ == "__main__":
    main()


