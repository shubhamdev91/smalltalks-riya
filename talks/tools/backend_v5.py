"""Backend v5 (scope approved by the orchestrator, 10 Oct; deploy needs the owner's OK + v0 Publish):
1. settings fail closed: posting is open only when talk_settings/main.posting_open == "true" (a missing entry,
   a missing field or any other value means closed);
2. ?diag=ip removed (it was a one-off check of the forwarded address; nothing stored, but no longer needed).
Reports stay ungated by posting_open (decided). Adds regression tests. Run from talks/backend."""

p = 'app.py'
s = open(p, encoding='utf-8').read()
reps = [
    ("""  GET  /api/talks        health: {"ok", "service", "build", "configured"}; ?diag=ip echoes the caller's own forwarding
                         headers (to check whether the shopper IP survives the App Proxy); ?task=prune = daily cron""",
     """  GET  /api/talks        health: {"ok", "service", "build", "configured"}; ?task=prune = daily cron; through the
                         App Proxy: {"ok", "open"} (what the posting switch reads)"""),
    ("""        return {'open': s.get('posting_open', 'true') != 'false', 'hold_all': s.get('hold_all') == 'true',""",
     """        # fail closed: only an explicit "true" opens posting (a missing entry or field keeps it shut)
        return {'open': s.get('posting_open') == 'true', 'hold_all': s.get('hold_all') == 'true',"""),
    ("""        if 'diag=ip' in query:  # what this app sees of the caller's own address (nothing stored or logged)
            chain = [p.strip() for p in (headers.get('x-forwarded-for') or '').split(',') if p.strip()]
            return 200, {'ok': True, 'via_proxy': bool(proxy), 'x_forwarded_for': chain,
                         'x_real_ip': headers.get('x-real-ip') or '',
                         'x_vercel_forwarded_for': headers.get('x-vercel-forwarded-for') or '',
                         'network_key_used': (not proxy) and bool(client_ip(headers, False))}, cors
""", ""),
]
for a, b in reps:
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)
open(p, 'w', encoding='utf-8', newline='\n').write(s)

t = 'tests/test_talks.py'
s = open(t, encoding='utf-8').read()
a = """    def test_diag_and_404(self):
        status, _, out = self.run_app('GET', '/api/talks', query='diag=ip',
                                      headers={'X-Forwarded-For': '1.2.3.4, 5.6.7.8', 'X-Real-IP': '5.6.7.8'})
        body = json.loads(out)
        self.assertEqual((body['via_proxy'], body['x_forwarded_for'], body['network_key_used']), (False, ['1.2.3.4', '5.6.7.8'], True))
        status, _, out = self.run_app('GET', '/nope')
        self.assertEqual(status, '404 Not Found')"""
b = """    def test_no_diag_and_404(self):
        # ?diag=ip is gone: the request gets the plain health answer and no forwarding headers are echoed
        status, _, out = self.run_app('GET', '/api/talks', query='diag=ip',
                                      headers={'X-Forwarded-For': '1.2.3.4, 5.6.7.8', 'X-Real-IP': '5.6.7.8'})
        body = json.loads(out)
        self.assertEqual(body.get('service'), 'talks')
        self.assertFalse({'x_forwarded_for', 'x_real_ip', 'via_proxy', 'network_key_used'} & set(body))
        self.assertNotIn('1.2.3.4', out.decode() if isinstance(out, bytes) else out)
        status, _, out = self.run_app('GET', '/nope')
        self.assertEqual(status, '404 Not Found')

    def test_settings_fail_closed(self):
        s = self.store.by_handle('talk_settings', 'main')
        for fields in ({'posting_open': None}, {'posting_open': ''}, {'posting_open': 'TRUE'}, {'posting_open': 'yes'}):
            talks._cache.clear()
            self.store.update(s['_id'], fields)
            status, body = self.post('hello there friends')
            self.assertEqual((status, body['code']), (403, 'closed'), fields)
            status, body = self.call({'action': 'reply', 'thread': 'x', 'text': 'hi', 'alias': 'plotpari', 'device': self.device(), 't': 9000})
            self.assertEqual((status, body['code']), (403, 'closed'), fields)
        talks._cache.clear()
        self.store.delete(s['_id'])  # no settings entry at all: closed, not open
        self.assertEqual(self.post('hello there friends')[1]['code'], 'closed')
        self.assertEqual(self.store.list_type('talk_thread'), [])
        self.assertEqual(self.store.list_type('talk_signal'), [])"""
assert s.count(a) == 1
s = s.replace(a, b)
open(t, 'w', encoding='utf-8', newline='\n').write(s)
print('ok')
