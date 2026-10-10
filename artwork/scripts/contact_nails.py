from PIL import Image, ImageDraw
import json
from stlib import BGS, hexrgb
m=json.load(open('../nails/manifest.json'))
W,H=m['cell']['width'],m['cell']['height']; ax,ay=m['anchor']['x']*W,m['anchor']['y']*H
rows=[]
for i,(h,v) in enumerate(m['sets'].items()):
    im=Image.open('../'+v['file']).convert('RGBA')
    row=Image.new('RGB',(W*3*2+30,H),'white')
    for j,bg in enumerate([BGS[i],'#fffaf0']):
        b=Image.new('RGBA',im.size,hexrgb(bg)+(255,)); b.alpha_composite(im)
        d=ImageDraw.Draw(b)
        for c in range(3):
            x=c*W+ax; d.line([(x-6,ay),(x+6,ay)],fill='cyan'); d.line([(x,ay-6),(x,ay+6)],fill='cyan')
            d.rectangle([c*W,0,c*W+W-1,H-1],outline=(0,0,0,60))
        row.paste(b.convert('RGB'),(j*(W*3+30),0))
    rows.append(row)
s=Image.new('RGB',(rows[0].width,H*7),'white')
for i,r in enumerate(rows): s.paste(r,(0,i*H))
s.resize((s.width//2,s.height//2),Image.LANCZOS).save('../tests/nails-contact.png')
