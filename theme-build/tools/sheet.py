# sheet.py <png> <out.jpg> [cols] : slice a tall full-page screenshot into side-by-side columns
import sys
from PIL import Image
src,out=sys.argv[1],sys.argv[2]; cols=int(sys.argv[3]) if len(sys.argv)>3 else 4
im=Image.open(src).convert('RGB'); w,h=im.size
seg=-(-h//cols)
sheet=Image.new('RGB',(w*cols+10*(cols-1),seg),(255,255,255))
for i in range(cols):
    part=im.crop((0,i*seg,w,min(h,(i+1)*seg)))
    sheet.paste(part,(i*(w+10),0))
scale=min(1,2000/sheet.width, 2000/sheet.height)
sheet=sheet.resize((int(sheet.width*scale),int(sheet.height*scale)))
sheet.save(out,quality=78)
print(sheet.size)
