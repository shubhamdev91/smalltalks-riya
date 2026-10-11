"""CURRENT | PROPOSED comparison sheets for the owner: qa/talks-ux/renders/compare-<screen>-<w>x<h>.png"""
from PIL import Image, ImageDraw, ImageFont
import os

R = 'qa/talks-ux/renders'
PAIRS = [('hub', 'hub'), ('composer', 'composer'), ('thread', 'thread'), ('inline-reply', 'inline-reply')]
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

# topic row: proposed 5 (st-copy TLK-006) vs the as-built 4, with a one-line pro/con each, for the owner
if not os.path.exists(f'{R}/proposed-topics5-crop-390.png'):
    raise SystemExit(0)
A, B = Image.open(f'{R}/proposed-topics5-crop-390.png').convert('RGB'), Image.open(f'{R}/proposed-topics4-crop-390.png').convert('RGB')
lines = [
    ('PROPOSED: 5 topics (st-copy): all · plot twists · tiny wins · second opinions · just venting · nail talk', '#a31a33'),
    ('+ names the two big reasons people come (advice, venting); "your own" covers the rest.', '#1a1a2e'),
    ('- 2 new shared topic entries; "something else" stays as the hidden home of "your own" posts; ~3.5 chips visible.', '#5d5562'),
    ('ALTERNATIVE: the 4 as built: all · plot twists · tiny wins · nail talk · something else', '#a31a33'),
    ('+ no data change, fewer chips.', '#1a1a2e'),
    ('- "something else" is vague, so advice and venting talks get lost in it.', '#5d5562'),
]
W, pad = 980, 16
H = pad * 2 + A.height + B.height + 6 * 24 + 40
sheet = Image.new('RGB', (W, H), '#f3efe9')
d = ImageDraw.Draw(sheet)
y = pad
for i, (img, block) in enumerate(((A, lines[:3]), (B, lines[3:]))):
    for text, col in block:
        d.text((pad, y), text, fill=col, font=SMALL)
        y += 24
    sheet.paste(img, (pad, y))
    y += img.height + 20
sheet.save(f'{R}/compare-topics-390.png')
print('compare topics', sheet.size)
