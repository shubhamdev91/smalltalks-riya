p='samples.py'; s=open(p,encoding='utf-8').read()
s=s.replace('"Same nails. Different moods."','"Same nails.\\n   Different moods."').replace('"Use a paper strip to find the widest part"','"Use a paper strip to find the widest part\\nof your natural nail, like this."')
open(p,'w',encoding='utf-8').write(s)
