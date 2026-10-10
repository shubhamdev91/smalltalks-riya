"""Lab sheets for the desktop chapters: the 7 chapter shots of one size (from tools/desk_check.py) on one image,
two columns, each at half size with its key. Usage: python -I tools/desk_sheet.py [prefix] [dir]
Writes <dir>/<prefix>-sheet-<w>x<h>.png for every size found."""
import pathlib, re, sys
from PIL import Image, ImageDraw

TB = pathlib.Path(__file__).resolve().parents[1]
PREFIX = sys.argv[1] if len(sys.argv) > 1 else 'desk'
D = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else TB / 'lab/shots'
ORDER = ['diet-cherry', 'brainwave', 'green-flag', 'shaadi-shift', 'on-me', 'wild-card', 'pinky-promise']
sizes = sorted({m.group(1) for f in D.glob(f'{PREFIX}-*x*-*.png') if (m := re.match(rf'{PREFIX}-(\d+x\d+)-', f.name)) and 'sheet' not in f.name})
for sz in sizes:
    ims = [(k, Image.open(D / f'{PREFIX}-{sz}-{k}.png').convert('RGB')) for k in ORDER if (D / f'{PREFIX}-{sz}-{k}.png').exists()]
    w, h = ims[0][1].size
    tw, th = w // 2, h // 2
    sheet = Image.new('RGB', (tw * 2 + 30, (th + 26) * ((len(ims) + 1) // 2) + 10), 'white')
    dr = ImageDraw.Draw(sheet)
    for i, (k, im) in enumerate(ims):
        x, y = 10 + (i % 2) * (tw + 10), 10 + (i // 2) * (th + 26)
        sheet.paste(im.resize((tw, th), Image.LANCZOS), (x, y + 16))
        dr.text((x, y), f'{sz}  {k}', fill='black')
    out = D / f'{PREFIX}-sheet-{sz}.png'
    sheet.save(out)
    print(out)
