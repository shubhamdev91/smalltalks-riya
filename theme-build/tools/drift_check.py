"""Drift check of the build theme (186651934933) against a recorded manifest. Read-only: never uploads anything.

The Admin API is reached through the agents' Shopify Admin GraphQL tool (graphql_query); this file holds no credentials.
  1. python -I theme-build/tools/drift_check.py --query
     prints the page query. Run it with the tool, variables {"after": null}; while pageInfo.hasNextPage is true, run it
     again with {"after": "<endCursor>"}. Each response also carries the bodies of the key JSON files (templates/*.json,
     sections/*-group.json, config/settings_data.json), which makes it large enough for the tool to save it to a file
     (no hand-copied checksums) and gives the key-level diff its remote side.
  2. python -I theme-build/tools/drift_check.py --remote <page 1 file> [<page 2 file> ...]
     compares the remote checksums (manifest scope) with the manifest: changed / added / removed, old -> new md5, and
     for drifted key JSON files a key-level JSON diff, local mirror (theme-build/src) vs remote.
     Exit code 0 = no drift, 1 = drift, 2 = bad or incomplete input.
  3. --write-manifest <path> (with --remote): records the remote checksums as a new manifest (after a merge or a Riya
     session), in the baseline's format.
Options: --baseline <path> (default: the newest manifest in theme-build/manifest/), --no-json-diff.
Checks on the input: the theme is the build, the pages are complete (last page hasNextPage false), no filename twice,
every padded checksum copy agrees (p1 / p2), and every JSON body matches its checksumMd5 (as stored: without the
auto-generated header, or compact JSON)."""
import argparse, datetime, fnmatch, hashlib, json, pathlib, re, sys

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
TB = pathlib.Path(__file__).resolve().parents[1]
SRC = TB / 'src'
MANIFESTS = TB / 'manifest'
BUILD = 'gid://shopify/OnlineStoreTheme/186651934933'
JSON_GLOBS = ['templates/*.json', 'sections/*-group.json', 'config/settings_data.json']
MAX_DIFF_LINES = 150


def newest_manifest():
    files = sorted(MANIFESTS.glob('*.json'), key=lambda p: (re.findall(r'\d{4}-\d{2}-\d{2}(?:-\d{4,6})?', p.name) or [''])[0])
    if not files:
        sys.exit(f'no manifest in {MANIFESTS}')
    return files[-1]


def page_query(scope):
    globs = ', '.join(json.dumps(g) for g in scope)
    jglobs = ', '.join(json.dumps(g) for g in JSON_GLOBS)
    return ('query DriftPage($after: String) { theme(id: "%s") { id role updatedAt '
            'files(first: 250, after: $after, filenames: [%s]) { nodes { filename checksumMd5 p1: checksumMd5 p2: checksumMd5 } '
            'pageInfo { hasNextPage endCursor } } '
            'json: files(first: 50, filenames: [%s]) { nodes { filename checksumMd5 body { ... on OnlineStoreThemeFileBodyText { content } } } } } }'
            % (BUILD, globs, jglobs))


def body_matches(content, md5):
    """The Admin API serves JSON files with an auto-generated /* ... */ header and, for files stored compact, pretty-
    printed; checksumMd5 is over the stored bytes: the text without the header, or compact JSON with "/" escaped."""
    rest = re.sub(r'^\s*/\*.*?\*/\s*', '', content, count=1, flags=re.S)
    cands = [content, rest]
    try:
        o = json.loads(rest)
        for ea in (False, True):
            c = json.dumps(o, separators=(',', ':'), ensure_ascii=ea)
            cands += [c, c.replace('/', '\\/')]
    except ValueError:
        pass
    return any(hashlib.md5(c.encode('utf-8')).hexdigest() == md5 for c in cands)


def load_pages(paths):
    """-> (theme info, {filename: md5}, {filename: content of key JSON files}); exits 2 on bad / incomplete input."""
    files, bodies, theme, last = {}, {}, None, None
    for p in paths:
        try:
            d = json.loads(pathlib.Path(p).read_text(encoding='utf-8'))
        except Exception as e:
            sys.exit(f'INPUT {p}: not JSON ({e})')
        if d.get('errors'):
            print(f'INPUT {p}: the response has errors: {json.dumps(d["errors"])[:300]}'); sys.exit(2)
        t = (d.get('data') or {}).get('theme')
        if not t or 'files' not in t:
            print(f'INPUT {p}: no data.theme.files (run the --query query)'); sys.exit(2)
        if t.get('id') != BUILD:
            print(f'INPUT {p}: theme {t.get("id")} is not the build {BUILD}'); sys.exit(2)
        theme = theme or {'id': t['id'], 'role': t.get('role'), 'updatedAt': t.get('updatedAt')}
        if t.get('updatedAt') != theme['updatedAt']:
            print(f'INPUT {p}: the theme changed between pages (updatedAt {theme["updatedAt"]} -> {t.get("updatedAt")}); re-run all pages'); sys.exit(2)
        for n in t['files']['nodes']:
            f, m = n['filename'], n['checksumMd5']
            if any(n.get(k) not in (None, m) for k in ('p1', 'p2')):
                print(f'INPUT {p}: {f}: checksum copies disagree (a hand-copied response?); re-run the query'); sys.exit(2)
            if f in files:
                print(f'INPUT {p}: {f} appears twice (the same page given twice?)'); sys.exit(2)
            files[f] = m
        for n in (t.get('json') or {}).get('nodes', []):
            c = (n.get('body') or {}).get('content')
            if c is None:
                continue
            if not body_matches(c, n['checksumMd5']):
                print(f'INPUT {p}: {n["filename"]}: body md5 != checksumMd5 (a hand-copied response?); re-run the query'); sys.exit(2)
            bodies[n['filename']] = c
        last = t['files']['pageInfo']
    if last and last.get('hasNextPage'):
        print(f'INPUT incomplete: run the query again with variables {{"after": "{last["endCursor"]}"}} and add that file'); sys.exit(2)
    return theme, files, bodies


def in_scope(f, scope):
    return any(fnmatch.fnmatchcase(f, g) for g in scope)


def is_key_json(f):
    return any(fnmatch.fnmatchcase(f, g) for g in JSON_GLOBS)


def parse_json(text):
    """Shopify JSON templates may start with an auto-generated /* ... */ comment."""
    return json.loads(re.sub(r'^\s*/\*.*?\*/', '', text, count=1, flags=re.S))


def short(v):
    s = json.dumps(v, ensure_ascii=False)
    return s if len(s) <= 100 else s[:97] + '...'


def json_diff(a, b, path=''):
    """Key-level differences between two JSON values: (+ added, - removed, ~ changed) lines."""
    out = []
    if isinstance(a, dict) and isinstance(b, dict):
        for k in a.keys() | b.keys():
            p = f'{path}.{k}' if path else str(k)
            if k not in b:
                out.append(f'- {p}: {short(a[k])}')
            elif k not in a:
                out.append(f'+ {p}: {short(b[k])}')
            else:
                out += json_diff(a[k], b[k], p)
    elif isinstance(a, list) and isinstance(b, list) and len(a) == len(b) and not all(isinstance(x, (str, int, float, bool)) or x is None for x in a + b):
        for i, (x, y) in enumerate(zip(a, b)):
            out += json_diff(x, y, f'{path}[{i}]')
    elif a != b:
        out.append(f'~ {path or "(root)"}: {short(a)} -> {short(b)}')
    return sorted(out, key=lambda l: l[2:])


def main():
    ap = argparse.ArgumentParser(description='Drift check of the build theme against a recorded manifest (read-only).')
    ap.add_argument('--query', action='store_true', help='print the Admin GraphQL page query to run')
    ap.add_argument('--remote', nargs='+', metavar='FILE', help='saved responses of the page query, all pages')
    ap.add_argument('--baseline', type=pathlib.Path, help='manifest to compare with (default: the newest in theme-build/manifest)')
    ap.add_argument('--write-manifest', type=pathlib.Path, metavar='PATH', help='record the remote checksums as a new manifest')
    ap.add_argument('--no-json-diff', action='store_true', help='skip the key-level JSON diffs')
    a = ap.parse_args()
    base_path = a.baseline or newest_manifest()
    base = json.loads(base_path.read_text(encoding='utf-8'))
    scope = base['scope']
    if a.query:
        print(page_query(scope))
        print('\nvariables: {"after": null}; then {"after": "<endCursor>"} while pageInfo.hasNextPage is true')
        return 0
    if not a.remote:
        ap.error('give --query or --remote')
    theme, remote_all, bodies = load_pages(a.remote)
    remote = {f: m for f, m in remote_all.items() if in_scope(f, scope)}
    old = base['files']
    changed = sorted(f for f in old.keys() & remote.keys() if old[f] != remote[f])
    added = sorted(remote.keys() - old.keys())
    removed = sorted(old.keys() - remote.keys())
    print(f'baseline  {base_path.relative_to(TB.parent) if base_path.is_relative_to(TB.parent) else base_path}: {len(old)} files, '
          f'build updatedAt {base.get("build_updatedAt")}, recorded {base.get("recorded", "?")}')
    print(f'remote    {theme["id"].split("/")[-1]} {theme["role"]}, updatedAt {theme["updatedAt"]}, {len(remote)} files in scope '
          f'({len(a.remote)} page{"s" * (len(a.remote) > 1)}, {len(bodies)} key JSON bodies)')

    def local_note(f, before, after):
        lp = SRC / f
        if not lp.exists():
            return 'local mirror: none'
        lm = hashlib.md5(lp.read_bytes()).hexdigest()
        return f'local mirror = {"new" if lm == after else "old" if lm == before else lm[:8]}'
    for f in changed:
        print(f'CHANGED   {f}  {old[f]} -> {remote[f]}  ({local_note(f, old[f], remote[f])})')
    for f in added:
        print(f'ADDED     {f}  -> {remote[f]}  ({local_note(f, None, remote[f])})')
    for f in removed:
        print(f'REMOVED   {f}  {old[f]} ->')
    drift = bool(changed or added or removed)
    print(f'drift     {"none" if not drift else f"{len(changed)} changed, {len(added)} added, {len(removed)} removed"}')

    if drift and not a.no_json_diff:
        for f in [x for x in changed + added if is_key_json(x)]:
            print(f'\n--- {f}: key-level diff, local mirror (theme-build/src/{f}) vs remote')
            if f not in bodies:
                print('    (no remote body in the responses: re-run --query, whose responses carry the key JSON bodies)'); continue
            lp = SRC / f
            if not lp.exists():
                print('    (no local mirror: the whole remote file is new)'); continue
            lm = hashlib.md5(lp.read_bytes()).hexdigest()
            if lm == remote[f]:
                print('    (the local mirror already equals the remote file)'); continue
            if f in old and lm != old[f]:
                print(f'    note: the local mirror ({lm[:8]}) is not the baseline version ({old[f][:8]}), so the diff also shows older differences')
            try:
                lines = json_diff(parse_json(lp.read_text(encoding='utf-8')), parse_json(bodies[f]))
            except Exception as e:
                print(f'    (could not parse: {e})'); continue
            for l in lines[:MAX_DIFF_LINES]:
                print('    ' + l)
            if len(lines) > MAX_DIFF_LINES:
                print(f'    ... {len(lines) - MAX_DIFF_LINES} more')
            if not lines:
                print('    (no key-level difference: formatting / key order only)')

    if a.write_manifest:
        m = {'theme_id_source': BUILD, 'equals_build': BUILD, 'build_updatedAt': theme['updatedAt'],
             'recorded': f'{datetime.date.today().isoformat()} by drift_check.py (Admin API checksumMd5 of the build)',
             'scope': scope, 'count': len(remote), 'files': dict(sorted(remote.items()))}
        a.write_manifest.parent.mkdir(parents=True, exist_ok=True)
        a.write_manifest.write_text(json.dumps(m, indent=1) + '\n', encoding='utf-8')
        print(f'manifest  written: {a.write_manifest} ({len(remote)} files)')
    return 1 if drift else 0


if __name__ == '__main__':
    sys.exit(main())
