import numpy as np, json
from PIL import Image
from scipy import ndimage
SRC='chatgpt/_from-board-corrections/preview-four-hand.png'
a=np.array(Image.open(SRC).convert('RGBA'))
hsv=np.array(Image.fromarray(a[...,:3]).convert('HSV')).astype(float)
S,V=hsv[...,1],hsv[...,2]
rgb=a[...,:3].astype(float); br=rgb[...,2]/np.maximum(rgb[...,0],1)
m=(a[...,3]>250)&(br>0.6)&(rgb[...,0]>185)
m[:820]=False
m=ndimage.binary_opening(m,iterations=2); m=ndimage.binary_fill_holes(ndimage.binary_closing(m,iterations=5))
lab,n=ndimage.label(m); sz=ndimage.sum(m,lab,range(1,n+1))
ids=[i+1 for i in np.argsort(-sz)[:4]]
res=[]
for k in ids:
    ys,xs=np.nonzero(lab==k); P=np.stack([xs,ys],1).astype(float); c=P.mean(0)
    w,v=np.linalg.eigh(np.cov((P-c).T)); d=v[:,np.argmax(w)]
    if d[1]<0: d=-d   # tip direction: fingers point down-left -> +y
    nr=np.array([-d[1],d[0]]); al=(P-c)@d; ac=(P-c)@nr
    prox=np.percentile(al,0.5)
    cut=c+d*prox+nr*np.median(ac[al<prox+10])
    width=np.percentile(ac,99)-np.percentile(ac,1)
    length=np.percentile(al,99.5)-prox
    res.append(dict(centroid=c.round(1).tolist(),dir=np.round(d,3).tolist(),cuticle=np.round(cut,1).tolist(),width=round(float(width),1),length=round(float(length),1),area=int(len(P))))
res.sort(key=lambda r:r['cuticle'][0])
for r in res: print(r)
vis=a[...,:3].copy(); vis[m]=[0,255,255]
for r in res:
    x,y=map(int,r['cuticle']); vis[y-4:y+4,x-4:x+4]=[255,0,255]
Image.fromarray(vis).crop((100,820,800,1166)).save('tests/hd/_hand-nailmask.png')
json.dump(res,open('hd/_hand_measure.json','w'),indent=1)
