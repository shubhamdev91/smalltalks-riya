"""Backend v3 (orchestrator decision A): behind the App Proxy no network/IP key is ever used or stored; ZERO_WIDTH
regex built from chr() so the file is transport-safe. Run from talks/backend."""

p = 'app.py'
s = open(p, encoding='utf-8').read()


def rep(a, b):
    global s
    assert s.count(a) == 1, a[:80]
    s = s.replace(a, b)


line = next(l for l in s.split('\n') if l.startswith('ZERO_WIDTH = '))
rep(line, "ZERO_WIDTH = re.compile('[' + chr(0x200B) + '-' + chr(0x200F) + chr(0x2060) + chr(0xFEFF) + chr(0x00AD) + ']')")
rep("""Privacy: no name, email, account id, raw IP or raw device id is ever stored or logged. talk_signal rows hold salted
HMAC keys only and are deleted after SIGNAL_DAYS (pruned on every write and by a daily Vercel cron).""",
    """Privacy: no name, email, account id, raw IP or raw device id is ever stored or logged. talk_signal rows hold: the
action kind, a salted HMAC key of the device id, a salted HMAC key of the text (duplicate check), the target entry id
and the time. Behind the App Proxy no network/IP key is used or stored at all (Vercel replaces the forwarded shopper
address with the proxy's, so it would be meaningless); only the optional direct (CORS) mode keys the network too.
Rows are deleted after SIGNAL_DAYS (pruned on every write and by a daily Vercel cron).""")
rep("""    ctx = {'ip': client_ip(headers, bool(proxy)), 'customer': (proxy or {}).get('logged_in_customer_id') or ''}""",
    """    # Decision A (10 Oct): behind the App Proxy the shopper IP never reaches us, so no network key is used or stored.
    ctx = {'ip': None if proxy else client_ip(headers, False), 'customer': (proxy or {}).get('logged_in_customer_id') or ''}""")
rep("""                         'client_ip_used': client_ip(headers, bool(proxy)) or ''}, cors""",
    """                         'network_key_used': (not proxy) and bool(client_ip(headers, False))}, cors""")
open(p, 'w', encoding='utf-8', newline='\n').write(s)

t = 'tests/test_talks.py'
s = open(t, encoding='utf-8').read()
rep("""        # a new device on the same network is limited too (per-IP), a different network is not
        talks._burst.clear()
        self.assertEqual(self.post('five more talk', ip='203.0.113.7')[1].get('code'), 'rate_limited')
        self.assertEqual(self.post('six more talk', ip='198.51.100.9')[0], 201)""",
    """        # behind the App Proxy only the device counts (decision A): a new device on the same network may post
        talks._burst.clear()
        self.assertEqual(self.post('five more talk', ip='203.0.113.7')[0], 201)
        self.assertTrue(all(not s.get('ip_key') for s in self.store.list_type('talk_signal')))""")
rep("""        self.assertEqual((body['via_proxy'], body['x_forwarded_for'], body['client_ip_used']), (False, ['1.2.3.4', '5.6.7.8'], '5.6.7.8'))""",
    """        self.assertEqual((body['via_proxy'], body['x_forwarded_for'], body['network_key_used']), (False, ['1.2.3.4', '5.6.7.8'], True))""")
open(t, 'w', encoding='utf-8', newline='\n').write(s)
print('ok')
