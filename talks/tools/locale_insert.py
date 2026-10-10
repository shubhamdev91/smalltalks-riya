"""locale_insert.py <base en.default.json> <out> : insert-only locale change for st-talks.
Inserts each NEW line right after its anchor line inside "small_talk" › "talks" › "live", then proves the change is
insert-only: the output minus the inserted lines is byte-identical to the base, the JSON (comments stripped) parses,
and every new key resolves to its value. Run it on the CURRENT remote file (re-fetch the md5 first).
Usage: python -I talks/tools/locale_insert.py theme-build/src/locales/en.default.json <out>"""
import json
import re
import sys

# (anchor line, stripped; new line, without indentation) — TLK-156 (st-copy v1.4.11)
INSERTS = [
    ('"prelaunch": "Posting isn’t open yet. Read along for now.",', '"no_replies_closed": "No replies yet",'),
]
EXPECT = {('small_talk', 'talks', 'live', 'no_replies_closed'): 'No replies yet'}

base_path, out_path = sys.argv[1], sys.argv[2]
raw = open(base_path, 'rb').read()
nl = '\r\n' if b'\r\n' in raw else '\n'
lines = raw.decode('utf-8').split(nl)
added = []
for anchor, new in INSERTS:
    hits = [i for i, l in enumerate(lines) if l.strip() == anchor]
    assert len(hits) == 1, f'anchor not unique: {anchor} ({len(hits)})'
    i = hits[0]
    assert not any(l.strip() == new for l in lines), f'already present: {new}'
    indent = lines[i][: len(lines[i]) - len(lines[i].lstrip())]
    lines.insert(i + 1, indent + new)
    added.append(i + 1)
out = nl.join(lines)
open(out_path, 'wb').write(out.encode('utf-8'))

# proofs
kept = [l for j, l in enumerate(lines) if j not in added]
assert nl.join(kept).encode('utf-8') == raw, 'not insert-only'
data = json.loads(re.sub(r'^\s*//.*$', '', re.sub(r'/\*.*?\*/', '', out.lstrip('﻿'), flags=re.S), flags=re.M))
for path, value in EXPECT.items():
    node = data
    for k in path:
        node = node[k]
    assert node == value, (path, node)
print(f'ok: {len(added)} line(s) inserted at {[a + 1 for a in added]}; all other {len(kept)} lines byte-identical')
