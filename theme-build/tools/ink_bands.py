"""Row profiles of text ink (white or near-black, per chapter) in the board crop and the lab render, split into bands.
Prints the y-ranges side by side so element positions can be matched to the board itself (not only the spec boxes).
Usage: python -I tools/ink_bands.py [key ...]"""
import sys, pathlib
from PIL import Image

TB = pathlib.Path(__file__).resolve().parents[1]
SH = TB / 'lab/shots'
INK = {'on-me': 'dark', 'wild-card': 'dark'}  # others: white ink
X0, X1 = 40, 350   # central columns, away from bleeding art at the edges


def profile(path, mode, ylimit=None):
    im = Image.open(path).convert('RGB')
    w, h = im.size
    px = im.load()
    rows = []
    for y in range(h if ylimit is None else min(h, ylimit)):
        n = 0
        for x in range(X0, X1, 2):
            r, g, b = px[x, y]
            if mode == 'white' and r > 232 and g > 232 and b > 232:
                n += 1
            elif mode == 'dark' and r < 60 and g < 60 and b < 60:
                n += 1
        rows.append(n)
    return rows


def bands(rows, thr=3, gap=6, minh=5):
    out, start, last = [], None, None
    for y, n in enumerate(rows):
        if n >= thr:
            if start is None:
                start = y
            last = y
        elif start is not None and y - last > gap:
            if last - start >= minh:
                out.append((start, last, max(rows[start:last + 1])))
            start = None
    if start is not None and last - start >= minh:
        out.append((start, last, max(rows[start:last + 1])))
    return out


keys = sys.argv[1:] or ['diet-cherry', 'brainwave', 'green-flag', 'shaadi-shift', 'on-me', 'wild-card', 'pinky-promise']
for k in keys:
    mode = INK.get(k, 'white')
    b = bands(profile(SH / f'board-{k}.png', mode, 640))
    m = bands(profile(SH / f'{k}-390.png', mode, 640))
    print(f'== {k} ({mode} ink)')
    print('  board:', [(a, z, n) for a, z, n in b])
    print('  build:', [(a, z, n) for a, z, n in m])
