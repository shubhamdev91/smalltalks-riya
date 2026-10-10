"""CURRENT | PROPOSED comparison sheets for the owner: qa/talks-ux/renders/compare-<screen>-<w>x<h>.png"""
from PIL import Image, ImageDraw, ImageFont
import os

R = 'qa/talks-ux/renders'
PAIRS = [('hub', 'hub'), ('composer', 'composer'), ('thread', 'thread'), ('thread-replies', 'thread-replies'), ('teaser', 'teaser')]
SIZES = ['390x844', '1536x703']
try:
    FONT = ImageFont.truetype('arialbd.ttf', 22)
    SMALL = ImageFont.truetype('arial.ttf', 16)
except OSError:
    FONT = SMALL = ImageFont.load_default()

for cur, pro in PAIRS:
    for s in SIZES:
        a, b = f'{R}/current-{cur}-{s}.png', f'{R}/proposed-{pro}-{s}.png'
        if not (os.path.exists(a) and os.path.exists(b)):
            continue
        A, B = Image.open(a).convert('RGB'), Image.open(b).convert('RGB')
        gap, head = 24, 44
        W, H = A.width + B.width + gap, max(A.height, B.height) + head
        sheet = Image.new('RGB', (W, H), '#f3efe9')
        sheet.paste(A, (0, head))
        sheet.paste(B, (A.width + gap, head))
        d = ImageDraw.Draw(sheet)
        d.text((10, 10), 'CURRENT (build, as installed)', fill='#5d5562', font=FONT)
        d.text((A.width + gap + 10, 10), 'PROPOSED (lab render)', fill='#a31a33', font=FONT)
        sheet.save(f'{R}/compare-{cur}-{s}.png')
        print('compare', cur, s, sheet.size)
