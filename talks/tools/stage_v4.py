"""stage_v4.py: staged uploads for the talks v4 window without retyping signed URLs.
  python -I talks/tools/stage_v4.py plan <theme path> ...   -> the stagedUploadsCreate `input` JSON (names v4__<path>)
  python -I talks/tools/stage_v4.py put                     -> reads the LATEST stagedUploadsCreate result from this
      session's transcript, PUTs each local file (talks/staged/v4/src/<path>) to its signed URL, re-downloads and checks
      the md5 (theme-build/tools/stage_batch.py), then prints the themeFilesUpsert `files` JSON. The signed URLs only
      live in a temp file that is deleted afterwards."""
import glob, json, os, subprocess, sys

SRC = 'talks/staged/v4/src/'
TRANSCRIPTS = os.path.expanduser('~/.claude/projects/C--Users-SSTS-Desktop-Riya/')
MIME = lambda p: 'text/javascript' if p.endswith('.js') else 'text/plain'
name_of = lambda p: 'v4__' + p.replace('/', '__')

if sys.argv[1] == 'plan':
    print(json.dumps([{'resource': 'FILE', 'filename': name_of(p), 'mimeType': MIME(p), 'httpMethod': 'PUT',
                       'fileSize': str(os.path.getsize(SRC + p))} for p in sys.argv[2:]]))
    sys.exit()

# put: newest transcript, last stagedUploadsCreate result
path = TRANSCRIPTS + os.environ.get('ST_SESSION', '58e3145d-f715-41a2-8d16-222e4877cbdd') + '.jsonl'  # st-talks' own transcript
targets = None
for line in open(path, encoding='utf-8'):
    if 'stagedTargets' not in line:
        continue
    try:
        d = json.loads(line)
    except ValueError:
        continue
    for b in (d.get('message') or {}).get('content') or []:
        if not isinstance(b, dict) or b.get('type') != 'tool_result':
            continue
        text = json.dumps(b.get('content'))
        if 'stagedTargets' not in text:
            continue
        parts = b['content'] if isinstance(b['content'], list) else [{'text': b['content']}]
        for part in parts:
            t = part.get('text', '') if isinstance(part, dict) else str(part)
            if 'stagedTargets' in t and 'v4__' in t:
                try:
                    found = json.loads(t[t.index('{'):], strict=False)['data']['stagedUploadsCreate']['stagedTargets']
                except (ValueError, KeyError, TypeError):
                    continue
                if found and all('/v4__' in x['url'] for x in found):
                    targets = found
assert targets, 'no stagedUploadsCreate result found'
rows, files = [], []
for tg in targets:
    staged = tg['url'].split('?')[0].rsplit('/', 1)[1]
    assert staged.startswith('v4__'), staged
    theme_path = staged[4:].replace('__', '/')
    rows.append(f"{SRC + theme_path}\t{tg['url']}\t{MIME(theme_path)}")
    files.append({'filename': theme_path, 'body': {'type': 'URL', 'value': tg['url'].split('?')[0]}})
tmp = 'talks/staged/v4/.targets.tmp'
open(tmp, 'w', encoding='utf-8', newline='\n').write('\n'.join(rows) + '\n')
try:
    subprocess.run([sys.executable, '-I', 'theme-build/tools/stage_batch.py', tmp], check=False)
finally:
    os.remove(tmp)
print('FILES ' + json.dumps(files))
