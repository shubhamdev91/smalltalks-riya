"""Prove the deployed app.py differs from the tested one only by literal zero-width characters (run from talks/backend)."""
import hashlib

s = open('app.py', 'rb').read()
bs = chr(92).encode()
escaped = b"ZERO_WIDTH = re.compile('[" + bs + b"u200b-" + bs + b"u200f" + bs + b"u2060" + bs + b"ufeff" + bs + b"u00ad]')"
literal = "ZERO_WIDTH = re.compile('[​-‏⁠﻿­]')".encode('utf-8')
assert s.count(escaped) == 1, 'escaped line not found'
t = s.replace(escaped, literal)
print('local tested    ', hashlib.md5(s).hexdigest()[:12])
print('with literal ZW ', hashlib.md5(t).hexdigest()[:12], '(deployed reports b3ce60f7f6e6)')
ns1, ns2 = {}, {}
exec(b"import re\n" + escaped, ns1)
exec(b"import re\n" + literal, ns2)
probe = 'a​b‏c⁠d﻿e­f‍g'
print('same behaviour:', ns1['ZERO_WIDTH'].sub('', probe) == ns2['ZERO_WIDTH'].sub('', probe),
      repr(ns2['ZERO_WIDTH'].sub('', probe)))
