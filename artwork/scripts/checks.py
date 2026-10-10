import os
from PIL import Image
R='..'; O=f'{R}/tests/checks'; os.makedirs(O,exist_ok=True)
sc=Image.open(f'{R}/_source/desi-ink-characters.png'); ch=Image.open(f'{R}/_source/desi-ink-characters-v2.png').convert('RGBA')
x=lambda i: round(i*1916/7)
def sv(im,n,k=2): im=im.convert('RGB'); im.resize((im.width*k,im.height*k),Image.LANCZOS).save(f'{O}/{n}.png')
sv(sc.crop((x(1),480,x(2),821)),'scene-brainwave-bag-sketchbook')
sv(sc.crop((x(2),560,x(3),821)),'scene-diet-cherry-can-unbranded')
sv(sc.crop((x(3),560,x(4),821)),'scene-green-flag-rotary-phone')
sv(sc.crop((x(5),560,x(6),821)),'scene-wild-card-cards-face-her')
sv(sc.crop((x(6),250,x(7),821)),'scene-pinky-promise-no-hands')
sv(sc.crop((x(0),550,x(1),821)),'scene-on-me-no-bill')
sv(sc.crop((x(4),300,x(5),821)),'scene-shaadi-shift-no-safety-pin')
for n,b in {'char-on-me-bill':(17,250,323,687),'char-brainwave-notebook-pen':(338,350,639,687),'char-diet-cherry-can':(650,330,929,687),'char-green-flag-phone':(944,220,1232,687),'char-shaadi-shift-pin':(1248,200,1528,687),'char-wild-card-cards':(1542,300,1834,687),'char-pinky-promise-hands':(1845,380,2155,687)}.items():
    c=ch.crop(b); bg=Image.new('RGBA',c.size,(255,250,240,255)); bg.alpha_composite(c); sv(bg,n)
print(sorted(os.listdir(O)))
