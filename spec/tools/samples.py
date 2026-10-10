"""Cut board text samples per type role -> spec/type/sample-<role>.png (enlarged 3x)."""
import os
from PIL import Image

B = r"C:\Users\SSTS\AppData\Local\Temp\claude\C--Users-SSTS-Desktop-Riya\01e61cb4-b351-4d98-a557-f8818be4c4e7\images"
C = os.path.join(os.path.dirname(__file__), "..", "crops")
T = os.path.join(os.path.dirname(__file__), "..", "type")

SAMPLES = {
    # role: (file, box, text, note)
    "headline": ("crops/hero-1-on-me@390.png", (28, 258, 384, 356), "Bill idhar.", "hero headline, board 2 frame 1"),
    "note": ("crops/hero-1-on-me@390.png", (38, 128, 232, 252), "I\u2019ve\ngot this.", "hero note, board 2 frame 1, rotated ~-10deg"),
    "pill": ("crops/hero-1-on-me@390.png", (88, 800, 300, 856), "Shop \u201cOn Me\u201d", "hero pill, board 2 frame 1 (arrow excluded)"),
    "talks": ("crops/hero-1-on-me@390.png", (205, 18, 312, 62), "the talks", "header, board 2 frame 1"),
    "shop-heading": ("board:5.jpg", (1228, 118, 1452, 168), "Find your fit.", "nail guide heading, board 5"),
    "annotation": ("board:5.jpg", (80, 186, 250, 222), "Same nails.\n   Different moods.", "shop annotation, board 5 (blue hand)"),
    "ui-sub": ("board:5.jpg", (1262, 232, 1390, 252), "Measure your nails", "red subhead, board 5"),
    "ui-body": ("board:5.jpg", (1262, 252, 1470, 284), "Use a paper strip to find the widest part\nof your natural nail, like this.", "body grey, board 5"),
}


def load(src):
    if src.startswith("board:"):
        return Image.open(os.path.join(B, src[6:])).convert("RGB")
    return Image.open(os.path.join(C, "..", src)).convert("RGB")


if __name__ == "__main__":
    os.makedirs(T, exist_ok=True)
    for role, (src, box, text, note) in SAMPLES.items():
        c = load(src).crop(box)
        c.resize((c.width * 3, c.height * 3), Image.LANCZOS).save(os.path.join(T, f"sample-{role}.png"))
        print(role, c.size)
