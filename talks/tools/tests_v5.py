"""Tests requested by the orchestrator (10 Oct): proxy-mode buckets per device, explicit rejection without a device id.
Test-only change: app.py is untouched. Run from talks/backend."""

t = 'tests/test_talks.py'
s = open(t, encoding='utf-8').read()
a = """    def test_bot_gets_fake_success(self):"""
b = """    def test_proxy_buckets_are_per_device(self):
        # 8 posts from 8 different devices within 60 s, all through the proxy (same Shopify address): all succeed
        self.assertEqual([self.post(f'eight devices talk {i}', ip='23.227.38.10')[0] for i in range(8)], [201] * 8)
        # 5 posts from ONE device: the first 3 pass (3 per 10 min), the rest are throttled
        d = self.device()
        codes = [self.post(f'one device talk {i}', device=d, ip='23.227.38.10')[0] for i in range(5)]
        self.assertEqual(codes, [201, 201, 201, 429, 429])

    def test_missing_device_is_rejected_not_bucketed(self):
        for device in (None, '', 'short'):
            for payload in ({'action': 'post', 'text': 'hello there', 'topic': 'plot-twists', 'alias': 'plotpari', 't': 9000},
                            {'action': 'report', 'target': 'thread:anything'}):
                p = dict(payload)
                if device is not None:
                    p['device'] = device
                status, body = self.call(p)
                self.assertEqual((status, body['code']), (400, 'bad_request'), (device, payload['action']))
        self.assertFalse(any(k.endswith(':') for k in talks._burst))  # no empty-key bucket was ever created

    def test_bot_gets_fake_success(self):"""
assert s.count(a) == 1
s = s.replace(a, b)
open(t, 'w', encoding='utf-8', newline='\n').write(s)
print('ok')
