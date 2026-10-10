"""zoom.py FILE x0 y0 x1 y1 SCALE BG OUT  -- native-pixel crop on a ground, nearest/lanczos upscale (display only)"""
import sys
from PIL import Image
f,x0,y0,x1,y1,k,bg,out=sys.argv[1:9]
im=Image.open(f).convert('RGBA').crop((int(x0),int(y0),int(x1),int(y1)))
b=Image.new('RGBA',im.size,tuple(int(bg.lstrip('#')[i:i+2],16) for i in (0,2,4))+(255,)); b.alpha_composite(im)
k=float(k); b.convert('RGB').resize((round(im.width*k),round(im.height*k)),Image.LANCZOS).save(out)
