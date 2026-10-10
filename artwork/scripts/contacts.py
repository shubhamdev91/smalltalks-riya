"""Per-asset contact sheets on all seven campaign backgrounds -> tests/contact-*.png"""
import json, os
from PIL import Image, ImageDraw
from stlib import BGS, hexrgb

ROOT = os.path.join(os.path.dirname(__file__), "..")
T = os.path.join(ROOT, "tests")


def on(bg, im):
    b = Image.new("RGBA", im.size, hexrgb(bg) + (255,))
    b.alpha_composite(im)
    return b.convert("RGB")


def label(img, text):
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 8 * len(text) + 8, 16], fill="white")
    d.text((4, 2), text, fill="black")
    return img


def grid(tiles, cols, gap=6):
    w, h = tiles[0].size
    rows = (len(tiles) + cols - 1) // cols
    s = Image.new("RGB", (cols * (w + gap) - gap, rows * (h + gap) - gap), "white")
    for i, t in enumerate(tiles):
        s.paste(t, ((i % cols) * (w + gap), (i // cols) * (h + gap)))
    return s


def main():
    nm = json.load(open(os.path.join(ROOT, "nails", "manifest.json")))
    # nails: one sheet per set, the 3-cell sprite on all 7 backgrounds (1x)
    for h in nm["sets"]:
        im = Image.open(os.path.join(ROOT, "nails", f"{h}.webp")).convert("RGBA")
        grid([label(on(bg, im), bg) for bg in BGS], 4).save(os.path.join(T, f"contact-nails-{h}.png"))
    # fingers: 4 tones x 7 backgrounds, top 420 px at 1x
    tiles = []
    for bg in BGS:
        for k in range(4):
            im = Image.open(os.path.join(ROOT, "fingers", f"tone-{k + 1}.webp")).convert("RGBA").crop((0, 0, 310, 420))
            tiles.append(label(on(bg, im), f"{bg} t{k + 1}"))
    grid(tiles, 8).save(os.path.join(T, "contact-fingers.png"))
    # hand (no nails): 1x full on 7 bgs, and 3x of the concealed-thumb edge on 7 bgs
    hand = Image.open(os.path.join(ROOT, "hand", "preview-hand.webp")).convert("RGBA")
    grid([label(on(bg, hand), bg) for bg in BGS], 4).save(os.path.join(T, "contact-hand-1x.png"))
    box = (40, 130, 300, 390)  # radial edge where the thumb was (exported px)
    z = hand.crop(box).resize(((box[2] - box[0]) * 3, (box[3] - box[1]) * 3), Image.LANCZOS)
    grid([label(on(bg, z), bg + " 3x") for bg in BGS], 4).save(os.path.join(T, "contact-hand-3x-thumb-edge.png"))


if __name__ == "__main__":
    main()
