"""Backend v2 (orchestrator conditions): TALKS_SALT env var, signal retention constant + prune on every write + daily cron."""

p = 'api/talks.py'
s = open(p, encoding='utf-8').read()


def rep(a, b):
    global s
    assert s.count(a) == 1, a[:80]
    s = s.replace(a, b)


rep("""Optional:
  TALKS_ALLOWED_ORIGINS   comma-separated store origins; set it ONLY to enable direct (CORS) mode""",
    """  TALKS_SALT              a long random string; salts the one-way keys for device / network / text (if missing, a
                          salt is derived from SHOPIFY_CLIENT_SECRET, so rotating the secret also rotates the keys)
Optional:
  TALKS_ALLOWED_ORIGINS   comma-separated store origins; set it ONLY to enable direct (CORS) mode

Privacy: no name, email, account id, raw IP or raw device id is ever stored or logged. talk_signal rows hold salted
HMAC keys only and are deleted after SIGNAL_DAYS (pruned on every write and by a daily Vercel cron).""")
rep("""MAX_BODY_BYTES = 16 * 1024
""", """MAX_BODY_BYTES = 16 * 1024
SIGNAL_DAYS = 7  # talk_signal retention; the shopper-facing promise (TLK-148) is "within 30 days"
PRUNE_BATCH = 25
""")
rep("""    salt = hmac.new(env('SHOPIFY_CLIENT_SECRET').encode(), b'talks-keys-v1', hashlib.sha256).digest()""",
    """    salt = env('TALKS_SALT').encode() or hmac.new(env('SHOPIFY_CLIENT_SECRET').encode(), b'talks-keys-v1', hashlib.sha256).digest()""")
rep("""def prune_signals() -> None:
    old = iso(now_utc() - timedelta(days=7))
    for s in STORE.list_type('talk_signal', f'updated_at:<{_q(old)}', first=10):
        STORE.delete(s['_id'])
""", """_last_prune = {'at': 0.0}


def prune_signals(force: bool = False) -> int:
    \"\"\"Delete talk_signal rows older than SIGNAL_DAYS (at most PRUNE_BATCH per run, at most once a minute per
    instance unless forced). Runs alongside every write and from the daily cron, so nothing outlives ~SIGNAL_DAYS + 1.\"\"\"
    if not force and time.time() - _last_prune['at'] < 60:
        return 0
    _last_prune['at'] = time.time()
    old = iso(now_utc() - timedelta(days=SIGNAL_DAYS))
    rows = STORE.list_type('talk_signal', f'updated_at:<{_q(old)}', first=PRUNE_BATCH)
    for row in rows:
        STORE.delete(row['_id'])
    return len(rows)


def prune_quietly() -> None:
    try:
        prune_signals()
    except Exception as e:  # pruning must never break a post
        print(f'talks prune skipped: {type(e).__name__}')
""")
rep("""    with ThreadPoolExecutor(max_workers=3) as pool:
        jobs = [pool.submit(record_signal, 'post', ip_key, device_key, gid, body_key)]""",
    """    with ThreadPoolExecutor(max_workers=4) as pool:
        jobs = [pool.submit(record_signal, 'post', ip_key, device_key, gid, body_key), pool.submit(prune_quietly)]""")
rep("""    if random.random() < 0.1:
        prune_signals()
    return {'thread':""", """    return {'thread':""")
rep("""    with ThreadPoolExecutor(max_workers=2) as pool:
        sig = pool.submit(record_signal, 'reply', ip_key, device_key, gid, body_key)""",
    """    with ThreadPoolExecutor(max_workers=3) as pool:
        sig = pool.submit(record_signal, 'reply', ip_key, device_key, gid, body_key)
        pool.submit(prune_quietly)""")
rep("""    record_signal('report', ip_key, device_key, item['_id'])
    count =""", """    record_signal('report', ip_key, device_key, item['_id'])
    prune_quietly()
    count =""")
rep("""    if method == 'GET':
        if not (proxy or cors):
            return 200, {'ok': True, 'service': 'talks'}, {}""",
    """    if method == 'GET':
        if 'task=prune' in query:  # Vercel cron (daily): only deletes expired talk_signal rows, safe if called by anyone
            try:
                return 200, {'ok': True, 'pruned': prune_signals()}, {}
            except TalkError:
                return 200, {'ok': False}, {}
        if not (proxy or cors):
            return 200, {'ok': True, 'service': 'talks'}, {}""")
open(p, 'w', encoding='utf-8', newline='\n').write(s)

t = 'tests/test_talks.py'
s = open(t, encoding='utf-8').read()
rep("""    def test_cors_only_when_configured(self):""", """    def test_salt_env(self):
        a = talks.keyed('1.2.3.4', 'ip')
        os.environ['TALKS_SALT'] = 'a-long-random-owner-salt'
        try:
            b = talks.keyed('1.2.3.4', 'ip')
        finally:
            del os.environ['TALKS_SALT']
        self.assertNotEqual(a, b)
        self.assertEqual(len(b), 24)
        self.assertNotIn('1.2.3.4', a + b)

    def test_cors_only_when_configured(self):""")
rep("""    def test_bad_requests(self):""", """    def test_prune_old_signals(self):
        old = self.store.add('talk_signal', 'old-1', {'kind': 'post', 'device_key': 'x', 'at': '2026-01-01T00:00:00Z'})
        self.store.items[old]['_updated'] = '2026-01-01T00:00:00Z'
        new = self.store.add('talk_signal', 'new-1', {'kind': 'post', 'device_key': 'y', 'at': talks.iso(talks.now_utc())})
        status, body, _ = talks.handle_request('GET', '/api/talks?task=prune', {}, b'')
        self.assertEqual((status, body), (200, {'ok': True, 'pruned': 1}))
        self.assertNotIn(old, self.store.items)
        self.assertIn(new, self.store.items)

    def test_bad_requests(self):""")
open(t, 'w', encoding='utf-8', newline='\n').write(s)

v = 'vercel.json'
open(v, 'w', encoding='utf-8', newline='\n').write("""{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "functions": {
    "api/talks.py": { "maxDuration": 20 }
  },
  "crons": [
    { "path": "/api/talks?task=prune", "schedule": "17 3 * * *" }
  ]
}
""")
print('ok')
