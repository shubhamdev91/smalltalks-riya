"""Locate board-2 frames (white-bordered phone frames) and save enlarged crops."""
import os, sys
import numpy as np
from PIL import Image

B = r"C:\Users\SSTS\AppData\Local\Temp\claude\C--Users-SSTS-Desktop-Riya\01e61cb4-b351-4d98-a557-f8818be4c4e7\images"
OUT = os.path.join(os.path.dirname(__file__), "..", "crops")


def runs(mask, minlen):
    r, s = [], None
    for i, v in enumerate(list(mask) + [False]):
        if v and s is None:
            s = i
        if not v and s is not None:
            if i - s >= minlen:
                r.append((s, i))
            s = None
    return r


def board2():
    im = Image.open(os.path.join(B, "2.jpg")).convert("RGB")
    a = np.array(im).astype(int)
    # saturated pixels = coloured scene areas
    sat = (a.max(2) - a.min(2)) > 60
    cols = runs(sat.mean(0) > 0.25, 150)
    rows = runs(sat.mean(1) > 0.25, 300)
    print("cols", cols, "rows", rows)
    return im, cols, rows


if __name__ == "__main__":
    board2()
