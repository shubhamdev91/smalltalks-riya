"""stage_batch.py <targets.txt>: each line "local_path<TAB>staged_url<TAB>mime". PUTs the file to the signed staged URL,
re-downloads the public copy and checks its md5. Prints one line per file and the resourceUrl to use in themeFilesUpsert."""
import sys, subprocess, hashlib

ok = True
for line in open(sys.argv[1], encoding='utf-8'):
    line = line.strip()
    if not line:
        continue
    local, url, mime = line.split('\t')
    base = url.split('?')[0]
    put = subprocess.run(['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', '-X', 'PUT', '-H', 'Content-Type: ' + mime,
                          '--data-binary', '@' + local, url], capture_output=True, text=True).stdout
    body = subprocess.run(['curl', '-s', base], capture_output=True).stdout
    same = hashlib.md5(body).hexdigest() == hashlib.md5(open(local, 'rb').read()).hexdigest()
    ok &= put == '200' and same
    print(put, 'md5-ok' if same else 'MD5-MISMATCH', local, base)
print('ALL OK' if ok else 'PROBLEMS')
