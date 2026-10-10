import json, os
from PIL import Image, ImageDraw
from stlib import BGS, hexrgb
from contacts import on, label, grid

ROOT = os.path.join(os.path.dirname(__file__), "..")
T = os.path.join(ROOT, "tests")
R = json.load(open(os.path.join(ROOT, "phase2.json")))
H = list(R["characters"].keys())


def img(rel):
    return Image.open(os.path.join(ROOT, rel)).convert("RGBA")


def main():
    # characters: each on all 7 colours (scaled 0.5)
    for i, h in enumerate(H):
        im = img(R["characters"][h]["file"])
        im = im.resize((im.width // 2, im.height // 2), Image.LANCZOS)
        grid([label(on(bg, im), bg) for bg in BGS], 7).save(os.path.join(T, f"contact-character-{h}.png"))
    # characters in hero placement on own colour (390x700 scene at 1x css, art at 150 css width)
    tiles = []
    for i, h in enumerate(H):
        e = R["characters"][h]
        im = img(e["file"]); s = 150 / im.width
        im = im.resize((150, round(im.height * s)), Image.LANCZOS)
        cv = Image.new("RGBA", (390, 700), hexrgb(BGS[i]) + (255,))
        ax, ay = e["anchor"]["x"], e["anchor"]["y"]
        x = 0 if ax == 0 else 390 - im.width if ax == 1 else (390 - im.width) // 2
        y = 0 if ay == 0 else 700 - im.height if ay == 1 else (700 - im.height) // 2
        cv.alpha_composite(im, (x, y))
        tiles.append(label(cv.convert("RGB"), h))
    grid(tiles, 7).save(os.path.join(T, "contact-characters-hero-placement.png"))
    # chapters: raw + fade (on true colour), side by side per set
    tiles = []
    for i, h in enumerate(H):
        e = R["chapters"][h]
        raw = img(e["file"]); fade = img(e["fade_variant"]["file"])
        pair = Image.new("RGB", (raw.width * 2 + 6, raw.height), "white")
        pair.paste(raw.convert("RGB"), (0, 0)); pair.paste(on(BGS[i], fade), (raw.width + 6, 0))
        tiles.append(label(pair, f"{h} raw | fade on {BGS[i]}"))
    grid(tiles, 7).save(os.path.join(T, "contact-chapters.png"))
    # finger states on 7 colours
    fs = [img(R["shop_finger_states"][h]["file"]) for h in H]
    rows = []
    for bg in BGS:
        rows.append(grid([on(bg, f.resize((f.width // 2, f.height // 2), Image.LANCZOS)) for f in fs], 7, 2))
    grid(rows, 1).save(os.path.join(T, "contact-finger-states.png"))
    # lifestyle composites
    grid([label(img(R["shop_lifestyle"][h]["file"]).convert("RGB"), h) for h in H], 4).save(os.path.join(T, "contact-lifestyle.png"))
    # guide on 7 colours
    g = img(R["guide"]["cleaned"]["file"]); g = g.resize((g.width // 3, g.height // 3), Image.LANCZOS)
    grid([label(on(bg, g), bg) for bg in BGS], 7).save(os.path.join(T, "contact-guide.png"))
    # packaging on 7 colours (own colour each)
    grid([label(on(BGS[i], img(R["packaging"][h]["file"])), h + " (awaiting hi-res)") for i, h in enumerate(H)], 7).save(os.path.join(T, "contact-packaging.png"))


if __name__ == "__main__":
    main()
