"""set_live.py on|off [root] : flips the talks posting switch, the single value in snippets/st-talk-live.liquid that the
composer, reply box, Report, the pre-launch notice (TLK-153) and house rule 5 (TLK-075 / TLK-154) all read.
Run from theme-build/src (default root '.'); upload only snippets/st-talk-live.liquid afterwards, under the lock."""
import re
import sys

value = sys.argv[1]
assert value in ('on', 'off'), 'use on or off'
root = sys.argv[2] if len(sys.argv) > 2 else '.'
path = f'{root}/snippets/st-talk-live.liquid'
s = open(path, encoding='utf-8').read()
s2, n = re.subn(r"assign st_talks_posting = '(on|off)'", f"assign st_talks_posting = '{value}'", s)
assert n == 1, 'switch line not found'
open(path, 'w', encoding='utf-8', newline='\n').write(s2)
print(path, '->', value)
