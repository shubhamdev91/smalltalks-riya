import json
import numpy as np
from PIL import Image
m=json.load(open('../nails/manifest.json')); W=m['cell']['width']
for h in m['sets']:
    s=np.array(Image.open(f'../nails/{h}.webp').convert('RGBA')).astype(float)
    c=[s[:,i*W:(i+1)*W] for i in range(3)]
    out=[]
    for a,b in [(0,1),(0,2),(1,2)]:
        A,B=c[a],c[b]; u=(A[...,3]>128)|(B[...,3]>128); i=(A[...,3]>128)&(B[...,3]>128)
        # premultiplied over mid-grey to compare
        pa=A[...,:3]*A[...,3:]/255+128*(1-A[...,3:]/255); pb=B[...,:3]*B[...,3:]/255+128*(1-B[...,3:]/255)
        d=np.abs(pa-pb)[u].mean(); fr=(np.abs(pa-pb)[u].max(1)>40).mean()
        out.append(f'{a}v{b}: meanD {d:5.1f} px>40 {fr*100:4.1f}% IoU {i.sum()/u.sum():.3f}')
    print(h.ljust(14),' | '.join(out))
