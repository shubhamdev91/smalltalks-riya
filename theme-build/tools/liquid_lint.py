"""Pre-upload Liquid lint (URL upserts drop invalid Liquid silently: job done, no userErrors): block tags balanced and
properly nested (if/unless/case/for/capture/comment/raw/paginate/form/javascript/stylesheet/schema/doc, inside
{% liquid %} too), {% schema %} JSON parses. Usage: python -I tools/liquid_lint.py <file.liquid> ..."""
import json, pathlib, re, sys

sys.stdout.reconfigure(encoding='utf-8')
BLOCKS = {'if', 'unless', 'case', 'for', 'capture', 'comment', 'raw', 'paginate', 'form', 'javascript', 'stylesheet', 'schema', 'doc', 'tablerow'}
RAWISH = {'comment', 'raw', 'javascript', 'stylesheet', 'schema', 'doc'}


def tags(src):
    """(name, line) for every tag, {% liquid %} bodies expanded line by line."""
    for m in re.finditer(r'\{%-?\s*(\w+)(.*?)-?%\}', src, re.S):
        name, body = m.group(1), m.group(2)
        line = src.count('\n', 0, m.start()) + 1
        if name == 'liquid':
            for k, ln in enumerate(body.split('\n')):
                w = ln.strip().split()
                if w:
                    yield w[0], line + k
        else:
            yield name, line


def lint(path):
    src = pathlib.Path(path).read_text(encoding='utf-8')
    stack, errs = [], []
    raw = None
    for name, line in tags(src):
        if raw:
            if name == 'end' + raw:
                stack.pop(); raw = None
            continue
        if name in BLOCKS:
            stack.append((name, line))
            if name in RAWISH:
                raw = name
        elif name.startswith('end') and name[3:] in BLOCKS:
            if not stack or stack[-1][0] != name[3:]:
                errs.append(f'line {line}: {name} closes {stack[-1] if stack else "nothing"}')
                break
            stack.pop()
    if stack and not errs:
        errs.append(f'unclosed {stack}')
    m = re.search(r'\{%-?\s*schema\s*-?%\}(.*?)\{%-?\s*endschema\s*-?%\}', src, re.S)
    if m:
        try:
            json.loads(m.group(1))
        except Exception as e:
            errs.append(f'schema JSON: {e}')
    return errs


if __name__ == '__main__':
    bad = 0
    for f in sys.argv[1:]:
        e = lint(f)
        bad += bool(e)
        print(f'{"OK " if not e else "BAD"} {f}' + ('' if not e else ' -> ' + '; '.join(e)))
    sys.exit(1 if bad else 0)
