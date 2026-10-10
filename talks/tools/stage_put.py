"""stage_put.py <sigs.txt> <X-Goog-Date>: expands "local<TAB>uuid/name<TAB>signature<TAB>mime" lines into signed staged-upload
URLs, then runs theme-build/tools/stage_batch.py (PUT + md5 readback). Run from theme-build/src. Deletes the expanded
targets file afterwards (it holds signed URLs)."""
import os
import subprocess
import sys

B = 'https://shopify-staged-uploads.storage.googleapis.com/tmp/83023397077/files/'
Q = ('?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=merchant-assets%40shopify-tiers.iam.gserviceaccount.com'
     '%2F20261010%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date={date}&X-Goog-Expires=604800&X-Goog-SignedHeaders=host'
     '&X-Goog-Signature=')
sigs, date = sys.argv[1], sys.argv[2]
out = []
for line in open(sigs, encoding='utf-8'):
    line = line.rstrip('\n')
    if line:
        local, path, sig, mime = line.split('\t')
        out.append(f'{local}\t{B}{path}{Q.format(date=date)}{sig}\t{mime}')
tmp = sigs + '.targets'
open(tmp, 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
try:
    subprocess.run([sys.executable, '-I', '../tools/stage_batch.py', tmp], check=False)
finally:
    os.remove(tmp)
    os.remove(sigs)
