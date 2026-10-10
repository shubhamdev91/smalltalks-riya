from PIL import Image, ImageDraw
import json
from stlib import hexrgb
m=json.load(open('../fingers/manifest.json')); W,H=m['canvas']['width'],m['canvas']['height']
ay=m['nail_bed_anchor']['y']*H
s=Image.new('RGBA',(W*4,H),hexrgb('#073df1')+(255,))
for k,t in enumerate(m['tones']):
    s.alpha_composite(Image.open('../'+t['file']).convert('RGBA'),(k*W,0))
d=ImageDraw.Draw(s); d.line([(0,ay),(W*4,ay)],fill='yellow'); 
for k in range(4): d.line([(k*W+W/2,0),(k*W+W/2,H)],fill='yellow')
s.crop((0,0,W*4,420)).save('../tests/fingers-contact.png')
