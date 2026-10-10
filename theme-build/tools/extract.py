import json, sys, os, re
# usage: extract.py <tool-result-file> <outdir>
src, out = sys.argv[1], sys.argv[2]
raw = open(src, encoding='utf-8').read()
# tool result may be wrapped; find first '{'
data = json.loads(raw[raw.index('{'):])
if isinstance(data, list): data = json.loads(data[0]['text'])
nodes = data['data']['theme']['files']['nodes']
for n in nodes:
    b = n.get('body') or {}
    if 'content' in b:
        p = os.path.join(out, n['filename']); os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, 'w', encoding='utf-8', newline='\n').write(b['content'])
        print('wrote', n['filename'], len(b['content']))
