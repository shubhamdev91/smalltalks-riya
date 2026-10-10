"""Board 3 landing: cut the 4 columns at 390 wide, find section joins, trace join curves -> SVG paths."""
import json, os
import numpy as np
from PIL import Image, ImageDraw

B = r"C:\Users\SSTS\AppData\Local\Temp\claude\C--Users-SSTS-Desktop-Riya\01e61cb4-b351-4d98-a557-f8818be4c4e7\images\3.jpg"
OUT = os.path.join(os.path.dirname(__file__), "..", "crops")
COLS = [(12, 264), (274, 513), (522, 761), (770, 1013)]
Y0, Y1 = 32, 1495


def cut():
    im = Image.open(B).convert("RGB")
    res = []
    for i, (x0, x1) in enumerate(COLS):
        c = im.crop((x0, Y0, x1, Y1))
        s = 390 / (x1 - x0)
        c = c.resize((390, round((Y1 - Y0) * s)), Image.LANCZOS)
        c.save(os.path.join(OUT, f"landing-col{i + 1}@390.png"))
        g = c.copy(); d = ImageDraw.Draw(g)
        for x in range(0, 391, 39):
            d.line([(x, 0), (x, g.height)], fill=(0, 255, 255))
        for y in range(0, g.height, 50):
            d.line([(0, y), (390 if y % 100 == 0 else 12, y)], fill=(0, 255, 255) if y % 100 == 0 else (255, 0, 255))
            if y % 100 == 0:
                d.text((2, y + 2), str(y), fill=(0, 255, 255))
        g.save(os.path.join(OUT, f"landing-col{i + 1}@390-grid.png"))
        res.append((c, s))
        print("col", i + 1, c.size, round(s, 3))
    return res


if __name__ == "__main__":
    cut()
