import json
from PIL import Image
from stlib import BGS, hexrgb
fm=json.load(open('../fingers/manifest.json')); nm=json.load(open('../nails/manifest.json'))
FW,FH=fm['canvas']['width'],fm['canvas']['height']; fax,fay=fm['nail_bed_anchor']['x']*FW,fm['nail_bed_anchor']['y']*FH
CW,CH=nm['cell']['width'],nm['cell']['height']; ax,ay=nm['anchor']['x'],nm['anchor']['y']
S=float(__import__('sys').argv[1]) if len(__import__('sys').argv)>1 else 0.76
out=Image.new('RGB',(FW*7,520),'white')
for i,h in enumerate(nm['sets']):
    cv=Image.new('RGBA',(FW,FH),hexrgb(BGS[i])+(255,))
    cv.alpha_composite(Image.open(f'../fingers/tone-{i%4+1}.webp').convert('RGBA'))
    cell=Image.open(f'../nails/{h}.webp').convert('RGBA').crop((0,0,CW,CH)).convert('RGBa').resize((round(CW*S),round(CH*S)),Image.LANCZOS).convert('RGBA')
    cv.alpha_composite(cell,(round(fax-ax*CW*S),round(fay-ay*CH*S)))
    out.paste(cv.convert('RGB').crop((0,0,FW,520)),(i*FW,0))
out.save('../tests/finger-anchor-test.png')
