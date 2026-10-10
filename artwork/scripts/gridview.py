import sys
from PIL import Image, ImageDraw
def g(src,box,out,k=2,bg=None):
    im=Image.open(src).convert('RGBA').crop(box)
    if bg: b=Image.new('RGBA',im.size,bg+(255,)); b.alpha_composite(im); im=b
    im=im.convert('RGB').resize((round(im.width*k),round(im.height*k)),Image.LANCZOS); d=ImageDraw.Draw(im)
    x0,y0=box[:2]; st=20 if k>=1.5 else 100
    for x in range((x0//st+1)*st,box[2],st):
        X=(x-x0)*k; d.line([(X,0),(X,8 if x%100 else 16)],fill=(0,255,255))
        if x%100==0: d.text((X+2,16),str(x),fill=(0,255,255))
    for y in range((y0//st+1)*st,box[3],st):
        Y=(y-y0)*k; d.line([(0,Y),(8 if y%100 else 16,Y)],fill=(0,255,255))
        if y%100==0: d.text((18,Y),str(y),fill=(0,255,255))
    im.save(out)
if __name__=='__main__':
    a=sys.argv; bg=tuple(int(a[8].lstrip('#')[i:i+2],16) for i in (0,2,4)) if len(a)>8 else None
    g(a[1],tuple(int(v) for v in a[2:6]),a[6],float(a[7]),bg)
