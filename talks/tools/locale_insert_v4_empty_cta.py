"""locale_insert_v4_empty_cta.py <base en.default.json> <out>: insert-only fix for the live "Translation missing:
en.small_talk.talks.live.v4.empty_cta" (TLK-165 "spill your tea", the button on an empty topic page; the key was left out
of the v4 insert). Inserts ONE line after "empty_title" inside small_talk > talks > live > v4 and proves the change is
insert-only (output minus the new line == base, byte for byte), that the JSON parses and that the key resolves."""
import json, re, sys
ANCHOR = '"empty_title": "it’s quiet in here…",'
NEW = '"empty_cta": "spill your tea",'
base_path, out_path = sys.argv[1], sys.argv[2]
raw = open(base_path, 'rb').read()
nl = '\r\n' if b'\r\n' in raw else '\n'
lines = raw.decode('utf-8').split(nl)
hits = [i for i, l in enumerate(lines) if l.strip() == ANCHOR]
assert len(hits) == 1, f'anchor not unique ({len(hits)})'
assert not any(l.strip() == NEW for l in lines), 'already present'
i = hits[0]
indent = lines[i][: len(lines[i]) - len(lines[i].lstrip())]
lines.insert(i + 1, indent + NEW)
out = nl.join(lines)
open(out_path, 'wb').write(out.encode('utf-8'))
kept = lines[:i + 1] + lines[i + 2:]
assert nl.join(kept).encode('utf-8') == raw, 'not insert-only'
data = json.loads(re.sub(r'^\s*//.*$', '', re.sub(r'/\*.*?\*/', '', out.lstrip('﻿'), flags=re.S), flags=re.M))
assert data['small_talk']['talks']['live']['v4']['empty_cta'] == 'spill your tea'
print(f'insert-only OK: +1 line after line {i + 1}; JSON parses; v4.empty_cta resolves')
