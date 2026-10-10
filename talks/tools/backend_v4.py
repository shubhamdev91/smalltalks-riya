"""Backend v4: no IP burst guard without an IP key (behind the App Proxy the key is empty and 'post:' would be one
store-wide bucket). Adds a regression test. Run from talks/backend."""

p = 'app.py'
s = open(p, encoding='utf-8').read()
a = """    burst_guard(f'{kind}:{device_key}')
    burst_guard(f'{kind}:{ip_key}', limit=6)
"""
b = """    burst_guard(f'{kind}:{device_key}')
    if ip_key:  # only in direct (CORS) mode; behind the App Proxy there is no network key at all (decision A)
        burst_guard(f'{kind}:{ip_key}', limit=6)
"""
assert s.count(a) == 1
s = s.replace(a, b)
open(p, 'w', encoding='utf-8', newline='\n').write(s)

t = 'tests/test_talks.py'
s = open(t, encoding='utf-8').read()
a = """    def test_bot_gets_fake_success(self):"""
b = """    def test_proxy_has_no_store_wide_bucket(self):
        # behind the App Proxy every shopper arrives from Shopify's address: 12 different devices posting at once
        # must all get through (no shared burst bucket, no IP query, nothing IP-derived stored)
        statuses = [self.post(f'talk number {i} from its own phone', ip='23.227.38.10')[0] for i in range(12)]
        self.assertEqual(statuses, [201] * 12)
        self.assertNotIn('post:', talks._burst)
        self.assertTrue(all(not s.get('ip_key') for s in self.store.list_type('talk_signal')))

    def test_bot_gets_fake_success(self):"""
assert s.count(a) == 1
s = s.replace(a, b)
open(t, 'w', encoding='utf-8', newline='\n').write(s)
print('ok')
