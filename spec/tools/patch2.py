p='typecompare.py'; s=open(p,encoding='utf-8').read()
s=s.replace('''    "note": [("Kalam Regular"''','''    "note": [("Caveat 700", "caveat/Caveat[wght].ttf", dict(wght=700)), ("Caveat 600", "caveat/Caveat[wght].ttf", dict(wght=600)), ("Kalam Regular"''')
s=s.replace('''("Gochi Hand", "gochihand/GochiHand-Regular.ttf", {}), ("Patrick Hand", "patrickhand/PatrickHand-Regular.ttf", {})],
    "pill"''','''("Patrick Hand", "patrickhand/PatrickHand-Regular.ttf", {})],
    "pill"''')
s=s.replace('''                     ("Fraunces 800 SOFT0 opsz72", "fraunces/Fraunces[SOFT,WONK,opsz,wght].ttf", dict(wght=800, SOFT=0, WONK=0, opsz=72))],''','''                     ("Source Serif 4 Bold opsz60", "sourceserif4/SourceSerif4[opsz,wght].ttf", dict(wght=700, opsz=60)),
                     ("Libre Caslon Text Bold", "librecaslontext/LibreCaslonText[wght].ttf", dict(wght=700)),
                     ("Fraunces 800 SOFT0 opsz72", "fraunces/Fraunces[SOFT,WONK,opsz,wght].ttf", dict(wght=800, SOFT=0, WONK=0, opsz=72))],''')
s=s.replace('''                 ("Corben Bold", "corben/Corben-Bold.ttf", {})],''','''                 ("Corben Bold", "corben/Corben-Bold.ttf", {}), ("Young Serif", "youngserif/YoungSerif-Regular.ttf", {})],''')
s=s.replace('"talks": [("Caveat 500"','"talks": [("Caveat 600", "caveat/Caveat[wght].ttf", dict(wght=600)), ("Caveat 500"')
open(p,'w',encoding='utf-8').write(s)
p='samples.py'; s=open(p,encoding='utf-8').read()
s=s.replace('"got this.", "hero note 2nd line','"I\\u2019ve\\ngot this.", "hero note')
open(p,'w',encoding='utf-8').write(s)
