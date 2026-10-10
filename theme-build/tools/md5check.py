# compare local md5 vs remote checksums given as JSON tool result file or stdin listing "filename md5"
import hashlib, sys, json
raw=sys.stdin.read()
d=json.loads(raw[raw.index('{'):])
for n in d['data']['theme']['files']['nodes']:
    loc=hashlib.md5(open('src/'+n['filename'],'rb').read()).hexdigest()
    print(('OK  ' if loc==n['checksumMd5'] else 'DIFF'), n['filename'])
