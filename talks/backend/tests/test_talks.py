"""Local tests for api/talks.py (no network): python -I -m unittest discover -s tests -v  (run from talks/backend)."""
import hashlib
import hmac
import itertools
import json
import os
import re
import sys
import time
import unittest
from datetime import timedelta
from pathlib import Path
from urllib.parse import urlencode

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ.update({'SHOPIFY_SHOP': 'test-shop.myshopify.com', 'SHOPIFY_CLIENT_ID': 'cid', 'SHOPIFY_CLIENT_SECRET': 'hush'})
import app as talks  # noqa: E402  (the Vercel entrypoint module, app.py)

talks.time.sleep = lambda s: None  # no real waiting in list verification


class FakeStore:
    """In-memory metaobjects with the subset of search syntax the backend uses."""

    def __init__(self):
        self.items: dict[str, dict] = {}
        self.seq = itertools.count(1000)
        self.clock = talks.now_utc()

    def _new_id(self):
        return f'gid://shopify/Metaobject/{next(self.seq)}'

    def add(self, type_, handle, fields, status='ACTIVE'):
        gid = self._new_id()
        self.items[gid] = {'_type': type_, '_id': gid, '_handle': handle, '_status': status,
                           '_updated': talks.iso(talks.now_utc()), **fields}
        return gid

    def by_handle(self, type_, handle):
        for it in self.items.values():
            if it['_type'] == type_ and it['_handle'] == handle:
                return dict(it)
        return None

    def by_id(self, id_):
        return dict(self.items[id_]) if id_ in self.items else None

    def _match(self, it, query):
        for clause in re.findall(r'\((?:[^()]*)\)|\S+:[^\s()]+', query or ''):
            if clause.startswith('('):
                ors = re.findall(r'fields\.(\w+):"([^"]*)"', clause)
                if not any(it.get(k) == v for k, v in ors):
                    return False
                continue
            m = re.match(r'fields\.(\w+):"([^"]*)"', clause)
            if m:
                if it.get(m.group(1)) != m.group(2):
                    return False
                continue
            m = re.match(r'updated_at:([<>])"([^"]*)"', clause)
            if m:
                if (m.group(1) == '>' and not it['_updated'] > m.group(2)) or (m.group(1) == '<' and not it['_updated'] < m.group(2)):
                    return False
        return True

    def list_type(self, type_, query='', first=100):
        rows = [dict(it) for it in self.items.values() if it['_type'] == type_ and self._match(it, query)]
        return sorted(rows, key=lambda r: int(r['_id'].rsplit('/', 1)[1]), reverse=True)[:first]

    def create(self, type_, handle, fields, status=None):
        if self.by_handle(type_, handle):
            raise talks.TalkError('handle_taken', 409)
        gid = self.add(type_, handle, {k: v for k, v in fields.items() if v is not None}, status or 'ACTIVE')
        return {'id': gid, 'handle': handle}

    def update(self, id_, fields=None, status=None):
        it = self.items[id_]
        it.update(fields or {})
        if status:
            it['_status'] = status
        it['_updated'] = talks.iso(talks.now_utc())

    def delete(self, id_):
        self.items.pop(id_, None)

    def get_list(self, id_, key):
        raw = self.items[id_].get(key)
        return json.loads(raw) if raw else []

    def states(self, ids):
        return {i: {'status': self.items[i]['_status'], 'depth': int(self.items[i].get('depth') or 0)} for i in ids if i in self.items}


def seed(store: FakeStore):
    store.add('talk_settings', 'main', {'posting_open': 'true', 'hold_all': 'false'})
    store.add('talk_topic', 'all', {'label': 'All', 'pickable': 'false', 'threads': '[]'})
    for h, label in (('plot-twists', 'Plot twists'), ('tiny-wins', 'Tiny wins'), ('nail-talk', 'Nail talk'),
                     ('something-else', 'Something else')):
        store.add('talk_topic', h, {'label': label, 'pickable': 'true', 'threads': '[]'})


class Base(unittest.TestCase):
    def setUp(self):
        self.store = FakeStore()
        seed(self.store)
        talks.STORE = self.store
        talks._cache.clear()
        talks._burst.clear()
        self.n = 0

    def device(self):
        self.n += 1
        return f'device-{self.n:04d}-abcdefghijkl'

    def call(self, payload, ip='203.0.113.7', signed=True, headers=None):
        params = {'shop': 'test-shop.myshopify.com', 'logged_in_customer_id': '', 'path_prefix': '/apps/talks',
                  'timestamp': str(int(talks.time.time()))}
        msg = ''.join(sorted(f'{k}={v}' for k, v in params.items()))
        params['signature'] = hmac.new(b'hush', msg.encode(), hashlib.sha256).hexdigest() if signed else 'bad'
        h = {'content-type': 'application/json', 'x-forwarded-for': f'{ip}, 23.227.38.10', 'x-real-ip': '23.227.38.10'}
        h.update(headers or {})
        status, body, _ = talks.handle_request('POST', '/api/talks?' + urlencode(params), h, json.dumps(payload).encode())
        return status, body

    def post(self, text, topic='plot-twists', device=None, ip='203.0.113.7', **kw):
        p = {'action': 'post', 'text': text, 'topic': topic, 'alias': kw.pop('alias', 'softlaunchsamosa'),
             'avatar': 'on-me', 'device': device or self.device(), 'hp': '', 't': 9000, **kw}
        return self.call(p, ip=ip)


class Moderation(unittest.TestCase):
    def blocked(self, text):
        return talks.moderate(text)[0]

    def held(self, text):
        return talks.moderate(text)[1]

    def test_contact_blocked(self):
        for t in ('call me 98765 43210', 'my no is +91-98765-43210', 'mail me at riya.k@gmail.com',
                  'write to me: ria at gmail dot com', 'pay to ria@okaxis', 'upi riya@ybl'):
            self.assertEqual(self.blocked(t), 'blocked_contact', t)

    def test_links_blocked(self):
        for t in ('see https://x.com/abc', 'go to www.something.in', 'check spillthetea.com/post', 'wa.me/91987', 'bit.ly/abc'):
            self.assertEqual(self.blocked(t), 'blocked_link', t)
        self.assertIn(self.blocked('wa.me/919876543210'), ('blocked_link', 'blocked_contact'))

    def test_handles_blocked(self):
        for t in ('follow @spilltea_daily', 'insta: priyaaa_x', 'ig id is tea.queen', 'snap -> chaiqueen'):
            self.assertEqual(self.blocked(t), 'blocked_handle', t)

    def test_slurs_blocked(self):
        for t in ('she is such a r a n d i', 'total chutiya move', 'what a whore', 'b h o s d i k e',
                  'he called him a f4ggot', 'that bhenchoddd'):
            self.assertEqual(self.blocked(t), 'blocked_words', t)

    def test_honest_posts_pass(self):
        for t in ('Group chat went silent after I said I liked pineapple on pizza. Plot twist: they all agreed.',
                  'pakki dosti hai, bas thoda drama',  # "pakki" must not trip the slur list
                  'Same Outfit, Different Confidence',  # Title Case headline
                  'Rehearsed a text for 20 mins and sent "hey". 2024-2025 batch energy.',
                  'Bill split to the last rupee: ₹1,240 / 4. Practical or tragic?',
                  'mera crush ne seen pe chhod diya 😭 kya karu',
                  'sara din bas zara sa kaam, khushi se muskan tak, akash jitna drama',
                  'Spent 3 hours on my nails for a 10 minute party lol'):
            self.assertIsNone(self.blocked(t), t)
            self.assertEqual(self.held(t), [], t)

    def test_real_person_held(self):
        for t in ('Riya from my floor keeps copying my nails', 'Mr Sharma in accounts is the worst',
                  'her name is anjali and she', 'Met Rohan Mehra yesterday and wow', 'girl in hostel 4 lied to everyone',
                  'everyone should know what she did', 'someone at LSR posted my pic', 'works at Infosys and acts rich'):
            self.assertIsNone(self.blocked(t), t)
            self.assertTrue(self.held(t), t)

    def test_extra_words(self):
        self.assertEqual(talks.moderate('this is a bad word zork', extra_blocked={'zork'})[0], 'blocked_words')
        self.assertTrue(talks.moderate('mention of brandx here', extra_held={'brandx'})[1])

    def test_alias(self):
        self.assertEqual(talks.check_alias('@softlaunchsamosa'), 'softlaunchsamosa')
        self.assertEqual(talks.check_alias('chai over coffee'), 'chai over coffee')
        for bad in ('x', 'Small Talk', 'small_talk', 'admin', 'Priya', 'riya sharma', 'call 9876543210', 'a' * 30,
                    'chutiya', '<script>'):
            with self.assertRaises(talks.TalkError, msg=bad):
                talks.check_alias(bad)

    def test_split_title(self):
        self.assertEqual(talks.split_title('Short one?'), ('Short one?', ''))
        self.assertEqual(talks.split_title('Headline here\nAnd the body\nsecond line'), ('Headline here', 'And the body\nsecond line'))
        long = 'Okay so this happened at the party yesterday. ' + 'Everyone was there and it was a lot to take in. ' * 4
        t, b = talks.split_title(long)
        self.assertEqual(t, 'Okay so this happened at the party yesterday.')
        self.assertTrue(b.startswith('Everyone was there'))
        t, b = talks.split_title('word ' * 60)
        self.assertTrue(t.endswith('…') and b.startswith('…') and len(t) <= 92)

    def test_slugify(self):
        self.assertEqual(talks.slugify('Anyone else rehearse a text & still send ‘hey’?'), 'anyone-else-rehearse-a-text-still-send-hey')
        self.assertEqual(talks.slugify('क्या चल रहा है'), 'talk')


class Auth(unittest.TestCase):
    def test_signature_message_matches_docs(self):
        # shopify.dev "Authenticate app proxies": sorted 'k=v' pairs, multi-values joined by ','
        q = 'extra=1&extra=2&shop={shop}.myshopify.com&logged_in_customer_id=&path_prefix=%2Fapps%2Fawesome_reviews&timestamp=1317327555'
        expected_msg = 'extra=1,2logged_in_customer_id=path_prefix=/apps/awesome_reviewsshop={shop}.myshopify.comtimestamp=1317327555'
        sig = hmac.new(b'hush', expected_msg.encode(), hashlib.sha256).hexdigest()
        ok = talks.verify_proxy_signature(q + '&signature=' + sig, 'hush', now=1317327555)
        self.assertEqual(ok['extra'], ['1', '2'])
        self.assertIsNone(talks.verify_proxy_signature(q.replace('extra=2', 'extra=3') + '&signature=' + sig, 'hush', now=1317327555))
        self.assertIsNone(talks.verify_proxy_signature(q + '&signature=' + sig, 'hush', now=1317327555 + 3600))
        self.assertIsNone(talks.verify_proxy_signature(q + '&signature=' + sig, 'other-secret', now=1317327555))

    def test_client_ip(self):
        self.assertEqual(talks.client_ip({'x-forwarded-for': '1.2.3.4, 23.227.38.10', 'x-real-ip': '23.227.38.10'}, True), '1.2.3.4')
        self.assertIsNone(talks.client_ip({'x-forwarded-for': '23.227.38.10', 'x-real-ip': '23.227.38.10'}, True))
        self.assertEqual(talks.client_ip({'x-forwarded-for': '5.6.7.8', 'x-real-ip': '5.6.7.8'}, False), '5.6.7.8')

    def test_unsigned_rejected_and_get_health(self):
        status, body, _ = talks.handle_request('POST', '/api/talks', {'content-type': 'application/json'}, b'{}')
        self.assertEqual(status, 401)
        status, body, _ = talks.handle_request('GET', '/api/talks', {}, b'')
        self.assertEqual((body['ok'], body['service'], body['configured']), (True, 'talks', True))
        self.assertEqual(len(body['build']), 12)

    def test_salt_env(self):
        a = talks.keyed('1.2.3.4', 'ip')
        os.environ['TALKS_SALT'] = 'a-long-random-owner-salt'
        try:
            b = talks.keyed('1.2.3.4', 'ip')
        finally:
            del os.environ['TALKS_SALT']
        self.assertNotEqual(a, b)
        self.assertEqual(len(b), 24)
        self.assertNotIn('1.2.3.4', a + b)

    def test_cors_only_when_configured(self):
        h = {'content-type': 'application/json', 'origin': 'https://test-shop.myshopify.com'}
        self.assertEqual(talks.handle_request('OPTIONS', '/api/talks', h, b'')[0], 403)
        os.environ['TALKS_ALLOWED_ORIGINS'] = 'https://test-shop.myshopify.com'
        try:
            status, _, cors = talks.handle_request('OPTIONS', '/api/talks', h, b'')
            self.assertEqual((status, cors['Access-Control-Allow-Origin']), (204, 'https://test-shop.myshopify.com'))
            h2 = dict(h, origin='https://evil.example')
            self.assertEqual(talks.handle_request('POST', '/api/talks', h2, b'{}')[0], 401)
        finally:
            del os.environ['TALKS_ALLOWED_ORIGINS']


class Flows(Base):
    def test_post_live_and_indexed(self):
        status, body = self.post('Rehearsed a text for an hour\nSent "hey". Again.')
        self.assertEqual(status, 201, body)
        th = body['thread']
        self.assertEqual((th['status'], th['title'], th['body']), ('live', 'Rehearsed a text for an hour', 'Sent "hey". Again.'))
        self.assertTrue(th['url'].startswith('/pages/talk/rehearsed-a-text-for-an-hour-'))
        stored = self.store.by_handle('talk_thread', th['handle'])
        self.assertEqual((stored['_status'], stored['alias'], stored['by_brand']), ('ACTIVE', 'softlaunchsamosa', 'false'))
        for topic in ('all', 'plot-twists'):
            self.assertEqual(self.store.get_list(self.store.by_handle('talk_topic', topic)['_id'], 'threads'), [stored['_id']])
        sig = self.store.list_type('talk_signal')
        self.assertEqual(len(sig), 1)
        self.assertNotIn('203.0.113.7', json.dumps(sig))  # never a raw IP

    def test_newest_first(self):
        d = self.device()
        _, a = self.post('first talk here', device=d)
        _, b = self.post('second talk here', device=d)
        lst = self.store.get_list(self.store.by_handle('talk_topic', 'all')['_id'], 'threads')
        self.assertEqual(lst[0], self.store.by_handle('talk_thread', b['thread']['handle'])['_id'])

    def test_own_topic(self):
        status, body = self.post('placement season is wild', topic='', topic_own='College chaos')
        self.assertEqual(status, 201, body)
        self.assertEqual((body['thread']['topic'], body['thread']['topic_label']), ('something-else', 'College chaos'))

    def test_need_topic_and_lengths(self):
        self.assertEqual(self.post('no topic here', topic='')[1]['code'], 'need_topic')
        self.assertEqual(self.post('hey', topic='all')[1]['code'], 'need_topic')
        self.assertEqual(self.post('hi')[1]['code'], 'too_short')
        self.assertEqual(self.post('x' * 1300)[1]['code'], 'too_long')

    def test_blocked_and_might_name_refused(self):
        status, body = self.post('dm me 9876543210')
        self.assertEqual((status, body['code']), (422, 'blocked_contact'))
        # owner, 10 Oct: no review queue. Might name someone -> refused at submit; nothing saved anywhere
        status, body = self.post('Priya Sharma from my class copied my set')
        self.assertEqual((status, body['code']), (422, 'might_name'))
        self.assertEqual(self.store.list_type('talk_thread'), [])
        self.assertEqual(self.store.list_type('talk_signal'), [])
        _, t = self.post('A talk to reply to')
        status, body = self.call({'action': 'reply', 'thread': t['thread']['handle'], 'text': 'her name is Riya and she lives in sector 5',
                                  'alias': 'plotpari', 'device': self.device(), 't': 5000})
        self.assertEqual((status, body['code']), (422, 'might_name'))
        self.assertEqual(self.store.list_type('talk_reply'), [])

    def test_flood_refuses_not_holds(self):
        for i in range(talks.FLOOD_PER_HOUR['post'] + 1):
            self.store.add('talk_signal', f'post-flood-{i}', {'kind': 'post', 'device_key': f'k{i}', 'at': talks.iso(talks.now_utc())})
        status, body = self.post('a perfectly fine talk')
        self.assertEqual((status, body['code']), (429, 'busy'))
        self.assertEqual(self.store.list_type('talk_thread'), [])

    def test_hidden_topic_only_via_your_own(self):
        status, body = self.call({'action': 'post', 'text': 'picking the hidden topic directly', 'topic': 'something-else',
                                  'alias': 'plotpari', 'device': self.device(), 't': 9000})
        self.assertEqual((status, body['code']), (422, 'need_topic'))
        status, body = self.call({'action': 'post', 'text': 'my own topic words', 'topic_own': 'hostel life',
                                  'alias': 'plotpari', 'device': self.device(), 't': 9000})
        self.assertEqual(status, 201, body)

    def test_rate_limit_and_duplicate(self):
        d = self.device()
        self.assertEqual(self.post('one more talk', device=d)[0], 201)
        self.assertEqual(self.post('one more talk', device=d)[1]['code'], 'duplicate')
        self.assertEqual(self.post('two more talk', device=d)[0], 201)
        self.assertEqual(self.post('three more talk', device=d)[0], 201)
        status, body = self.post('four more talk', device=d)
        self.assertEqual((status, body['code']), (429, 'rate_limited'))
        self.assertGreater(body['retry_after'], 0)
        # behind the App Proxy only the device counts (decision A): a new device on the same network may post
        talks._burst.clear()
        self.assertEqual(self.post('five more talk', ip='203.0.113.7')[0], 201)
        self.assertTrue(all(not s.get('ip_key') for s in self.store.list_type('talk_signal')))

    def test_proxy_has_no_store_wide_bucket(self):
        # behind the App Proxy every shopper arrives from Shopify's address: 12 different devices posting at once
        # must all get through (no shared burst bucket, no IP query, nothing IP-derived stored)
        statuses = [self.post(f'talk number {i} from its own phone', ip='23.227.38.10')[0] for i in range(12)]
        self.assertEqual(statuses, [201] * 12)
        self.assertNotIn('post:', talks._burst)
        self.assertTrue(all(not s.get('ip_key') for s in self.store.list_type('talk_signal')))

    def test_proxy_buckets_are_per_device(self):
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

    def test_bot_gets_fake_success(self):
        status, body = self.post('buy cheap stuff', hp='http://spam')
        self.assertEqual((status, body['thread']['handle']), (201, ''))
        status, body = self.post('too fast to be human', t=300)
        self.assertEqual(body['thread']['handle'], '')
        self.assertEqual(self.store.list_type('talk_thread'), [])

    def test_closed_and_hold_all(self):
        s = self.store.by_handle('talk_settings', 'main')
        self.store.update(s['_id'], {'posting_open': 'false'})
        self.assertEqual(self.post('hello there')[1]['code'], 'closed')
        talks._cache.clear()
        self.store.update(s['_id'], {'posting_open': 'true', 'hold_all': 'true'})  # the owner's emergency lever only
        self.assertEqual(self.post('hello there friends')[1]['thread']['status'], 'held')

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
        self.assertEqual(self.store.list_type('talk_signal'), [])

    def test_replies_nested_order_and_count(self):
        _, t = self.post('Thread for replies')
        h = t['thread']['handle']
        r = lambda text, parent=None, alias='chaioverthinker': self.call(
            {'action': 'reply', 'thread': h, 'parent': parent, 'text': text, 'alias': alias, 'avatar': 'wild-card',
             'device': self.device(), 'hp': '', 't': 5000}, ip=f'198.51.100.{self.n}')
        s1, a = r('first top-level')
        s2, b = r('second top-level')
        s3, a1 = r('nested under first', parent=a['reply']['handle'], alias='plotpari')
        s4, a2 = r('another nested under first', parent=a1['reply']['handle'])
        self.assertEqual((s1, s2, s3, s4), (201, 201, 201, 201), (a, b, a1, a2))
        self.assertEqual((a1['reply']['depth'], a1['reply']['reply_to']), (1, 'chaioverthinker'))
        thread = self.store.by_handle('talk_thread', h)
        order = [self.store.by_id(i)['body'] for i in self.store.get_list(thread['_id'], 'replies')]
        self.assertEqual(order, ['first top-level', 'nested under first', 'another nested under first', 'second top-level'])
        self.assertEqual(thread['reply_count'], '4')
        self.assertTrue(thread['last_reply_at'])

    def test_reddit_nesting_depth_order_and_parent(self):
        _, t = self.post('Thread for deep replies')
        h = t['thread']['handle']
        def r(text, parent=None):
            status, body = self.call({'action': 'reply', 'thread': h, 'parent': parent, 'text': text, 'alias': 'plotpari',
                                      'avatar': 'wild-card', 'device': self.device(), 't': 5000})
            self.assertEqual(status, 201, body)
            return body['reply']
        a = r('a: top')
        b = r('b: top')
        a1 = r('a1: reply to a', a['handle'])
        a1x = r('a1x: reply to a1', a1['handle'])
        a1xy = r('a1xy: reply to a1x', a1x['handle'])
        a2 = r('a2: second reply to a', a['handle'])
        a1z = r('a1z: second reply to a1', a1['handle'])
        self.assertEqual([x['depth'] for x in (a, a1, a1x, a1xy, a2, a1z)], [0, 1, 2, 3, 1, 2])
        thread = self.store.by_handle('talk_thread', h)
        order = [self.store.by_id(i)['body'].split(':')[0] for i in self.store.get_list(thread['_id'], 'replies')]
        # each reply sits at the end of its parent's subtree; siblings oldest first
        self.assertEqual(order, ['a', 'a1', 'a1x', 'a1xy', 'a1z', 'a2', 'b'])
        stored = self.store.by_handle('talk_reply', a1xy['handle'])
        self.assertEqual(stored['parent'], self.store.by_handle('talk_reply', a1x['handle'])['_id'])
        self.assertEqual(stored['reply_to'], 'plotpari')
        self.assertIsNone(self.store.by_handle('talk_reply', a['handle']).get('parent'))

    def test_nesting_capped_and_hidden_parent_refused(self):
        _, t = self.post('Thread for a long chain')
        h = t['thread']['handle']
        parent = None
        for i in range(talks.MAX_DEPTH + 3):
            status, body = self.call({'action': 'reply', 'thread': h, 'parent': parent, 'text': f'link {i}', 'alias': 'plotpari',
                                      'device': self.device(), 't': 5000})
            self.assertEqual(status, 201, body)
            parent = body['reply']['handle']
        self.assertEqual(body['reply']['depth'], talks.MAX_DEPTH)
        hidden = self.store.by_handle('talk_reply', parent)
        self.store.update(hidden['_id'], status='DRAFT')
        status, body = self.call({'action': 'reply', 'thread': h, 'parent': parent, 'text': 'to a hidden reply', 'alias': 'plotpari',
                                  'device': self.device(), 't': 5000})
        self.assertEqual((status, body['code']), (404, 'not_found'))

    def test_reply_to_hidden_thread_refused(self):
        _, t = self.post('Thread soon hidden')
        thread = self.store.by_handle('talk_thread', t['thread']['handle'])
        self.store.update(thread['_id'], status='DRAFT')
        status, body = self.call({'action': 'reply', 'thread': t['thread']['handle'], 'text': 'hello', 'alias': 'plotpari',
                                  'device': self.device(), 't': 5000})
        self.assertEqual((status, body['code']), (404, 'not_found'))

    def test_reports_hide_after_three_distinct(self):
        _, t = self.post('Thread to report')
        h = t['thread']['handle']
        rep = lambda dev, ip: self.call({'action': 'report', 'target': f'thread:{h}', 'device': dev}, ip=ip)
        d1 = self.device()
        self.assertEqual(rep(d1, '198.51.100.1')[1], {'ok': True, 'hidden': False})
        self.assertEqual(rep(d1, '198.51.100.1')[1], {'ok': True, 'hidden': False})  # same person twice = one report
        self.assertEqual(rep(self.device(), '198.51.100.2')[1]['hidden'], False)
        self.assertEqual(rep(self.device(), '198.51.100.3')[1]['hidden'], True)
        stored = self.store.by_handle('talk_thread', h)
        self.assertEqual((stored['_status'], stored['report_count']), ('DRAFT', '3'))
        self.assertTrue(stored['mod_note'].startswith('auto-hidden: 3 reports'))

    def test_reply_report_recounts(self):
        _, t = self.post('Thread with a bad reply')
        h = t['thread']['handle']
        _, r = self.call({'action': 'reply', 'thread': h, 'text': 'meh reply', 'alias': 'plotpari', 'device': self.device(), 't': 5000},
                         ip='198.51.100.50')
        for i in range(3):
            self.call({'action': 'report', 'target': 'reply:' + r['reply']['handle'], 'device': self.device()}, ip=f'198.51.100.{60 + i}')
        self.assertEqual(self.store.by_handle('talk_thread', h)['reply_count'], '0')

    def test_brand_posts_not_auto_hidden(self):
        gid = self.store.add('talk_thread', 'seed-thread', {'title': 'Seed', 'alias': 'small talk', 'by_brand': 'true'})
        for i in range(4):
            self.call({'action': 'report', 'target': 'thread:seed-thread', 'device': self.device()}, ip=f'198.51.100.{80 + i}')
        self.assertEqual(self.store.by_id(gid)['_status'], 'ACTIVE')

    def test_prune_old_signals(self):
        old = self.store.add('talk_signal', 'old-1', {'kind': 'post', 'device_key': 'x', 'at': '2026-01-01T00:00:00Z'})
        self.store.items[old]['_updated'] = '2026-01-01T00:00:00Z'
        new = self.store.add('talk_signal', 'new-1', {'kind': 'post', 'device_key': 'y', 'at': talks.iso(talks.now_utc())})
        talks._last_prune['at'] = 0
        status, body, _ = talks.handle_request('GET', '/api/talks?task=prune', {}, b'')
        self.assertEqual((status, body), (200, {'ok': True, 'pruned': 1}))
        self.assertNotIn(old, self.store.items)
        self.assertIn(new, self.store.items)

    def test_bad_requests(self):
        self.assertEqual(self.call({'action': 'nope'})[0], 400)
        self.assertEqual(self.call({'action': 'post', 'device': 'short', 'text': 'hello'})[1]['code'], 'bad_request')
        self.assertEqual(self.post('fine text', alias='Small Talk')[1]['code'], 'bad_alias')
        status, body = self.call({'action': 'post'}, signed=False)
        self.assertEqual(status, 401)


class Security(Base):
    """SECURITY-v5.md: one test per item (some items are also covered by older tests, named in the table)."""

    def signed_query(self, ts=None, shop=None):
        params = {'shop': shop or os.environ['SHOPIFY_SHOP'], 'logged_in_customer_id': '', 'path_prefix': '/apps/talks',
                  'timestamp': str(int(ts if ts is not None else time.time()))}
        msg = ''.join(sorted(f'{k}={v}' for k, v in params.items()))
        sig = hmac.new(os.environ['SHOPIFY_CLIENT_SECRET'].encode(), msg.encode(), hashlib.sha256).hexdigest()
        return '&'.join(f'{k}={v}' for k, v in params.items()) + '&signature=' + sig

    def raw(self, payload, query):
        return talks.handle_request('POST', '/api/talks?' + query, {'content-type': 'application/json'}, json.dumps(payload).encode())

    def test_hmac_required_fresh_and_this_shop_only(self):
        payload = {'action': 'post', 'text': 'signed talk', 'topic': 'plot-twists', 'alias': 'plotpari', 'device': self.device(), 't': 9000}
        self.assertEqual(self.raw(payload, self.signed_query())[0], 201)
        self.assertEqual(self.raw(payload, self.signed_query(ts=time.time() - 3600))[0], 401)        # stale
        self.assertEqual(self.raw(payload, self.signed_query(shop='other-shop.myshopify.com'))[0], 401)  # other shop
        self.assertEqual(self.raw(payload, self.signed_query().replace('signature=', 'signature=0'))[0], 401)  # tampered
        self.assertEqual(self.raw(payload, '')[0], 401)                                                  # unsigned

    def test_strict_lengths(self):
        self.assertEqual(self.post('x' * (talks.THREAD_MAX + 1))[1]['code'], 'too_long')
        self.assertEqual(self.post('hi')[1]['code'], 'too_short')
        self.assertEqual(self.post('fine length talk', alias='a' * (talks.ALIAS_MAX + 1))[1]['code'], 'bad_alias')
        _, t = self.post('thread for long replies')
        status, body = self.call({'action': 'reply', 'thread': t['thread']['handle'], 'text': 'y' * (talks.REPLY_MAX + 1),
                                  'alias': 'plotpari', 'device': self.device(), 't': 5000})
        self.assertEqual(body['code'], 'too_long')
        self.assertEqual(self.call({'action': 'post', 'text': 'unknown topic', 'topic': 'not-a-topic', 'alias': 'plotpari',
                                    'device': self.device(), 't': 9000})[1]['code'], 'need_topic')

    def test_unicode_normalised_and_controls_stripped(self):
        status, body = self.post('Cafe\u0301 talk\u0000 with \u200bhidden\u200d chars\u0007 here')
        self.assertEqual(status, 201, body)
        stored = self.store.by_handle('talk_thread', body['thread']['handle'])
        self.assertEqual(stored['title'], 'Café talk with hidden chars here')

    def test_json_never_carries_markup(self):
        status, body = self.post('<b>bold</b> <img src=x onerror=alert(1)> talk')
        self.assertEqual(status, 201, body)
        # stored and returned as plain text; the theme escapes it (see test_theme_escapes_user_text)
        self.assertEqual(body['thread']['title'], '<b>bold</b> <img src=x onerror=alert(1)> talk')
        self.assertEqual(json.loads(json.dumps(body))['thread']['title'], body['thread']['title'])

    def test_theme_escapes_user_text(self):
        root = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'theme-build', 'src')
        if not os.path.isdir(root):
            self.skipTest('theme mirror not present')
        import glob
        files = glob.glob(os.path.join(root, 'sections', 'st-talks-*.liquid')) + glob.glob(os.path.join(root, 'snippets', 'st-talk-*.liquid'))
        user = re.compile(r'\{\{-?\s*([^}]*?(?:\.(?:title|body|alias|topic_label|reply_to)\.value|t_alias|r_alias|excerpt)[^}]*)-?\}\}')
        bad = []
        for f in files:
            for m in user.finditer(open(f, encoding='utf-8').read()):
                expr = m.group(1)
                if '| escape' not in expr and '|escape' not in expr:
                    bad.append((os.path.basename(f), expr.strip()[:80]))
        self.assertEqual(bad, [])
        js = open(os.path.join(root, 'assets', 'st-talks.js'), encoding='utf-8').read()
        sinks = re.findall(r'(innerHTML|outerHTML)\s*=\s*([^;]+);', js)
        self.assertTrue(all(v.strip().startswith(("'", '"', '`')) and '${' not in v for _, v in sinks), sinks)
        self.assertNotIn('insertAdjacentHTML', js)

    def test_rate_limits_reply_and_report_per_device(self):
        _, t = self.post('thread for limits')
        d = self.device()
        codes = [self.call({'action': 'reply', 'thread': t['thread']['handle'], 'text': f'reply number {i}', 'alias': 'plotpari',
                            'device': d, 't': 5000})[0] for i in range(talks.LIMITS['reply'][0] + 1)]
        self.assertEqual(codes[-1], 429)
        talks._burst.clear()
        d2 = self.device()  # the duplicate-text fingerprint is per device: the same device can't post the same reply twice
        self.assertEqual(self.call({'action': 'reply', 'thread': t['thread']['handle'], 'text': 'same words twice', 'alias': 'plotpari',
                                    'device': d2, 't': 5000})[0], 201)
        self.assertEqual(self.call({'action': 'reply', 'thread': t['thread']['handle'], 'text': 'same words twice', 'alias': 'plotpari',
                                    'device': d2, 't': 5000})[1]['code'], 'duplicate')
        talks._burst.clear()
        dr = self.device()
        codes = []
        for i in range(talks.LIMITS['report'][0] + 1):
            _, ti = self.post(f'thread to report {i}')
            codes.append(self.call({'action': 'report', 'target': f"thread:{ti['thread']['handle']}", 'device': dr})[0])
            talks._burst.clear()
        self.assertEqual(codes[-1], 429)

    def test_honeypot_and_min_time(self):
        self.assertEqual(self.post('honeypot filled', hp='x')[1]['thread']['handle'], '')
        self.assertEqual(self.post('submitted too fast', t=talks.MIN_COMPOSE_MS - 1)[1]['thread']['handle'], '')
        self.assertEqual(self.store.list_type('talk_thread'), [])

    def test_body_size_cap(self):
        q = self.signed_query()
        big = json.dumps({'action': 'post', 'text': 'x' * (talks.MAX_BODY_BYTES + 10)}).encode()
        status, body, _ = talks.handle_request('POST', '/api/talks?' + q, {'content-type': 'application/json'}, big)
        self.assertEqual((status, body['code']), (413, 'too_long'))

    def test_no_ip_or_text_in_store_or_logs(self):
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            _, t = self.post('a talk with a secret word marmalade', ip='198.51.100.77')
            self.call({'action': 'reply', 'thread': t['thread']['handle'], 'text': 'reply marmalade', 'alias': 'plotpari',
                       'device': self.device(), 't': 5000}, ip='198.51.100.77')
            self.post('dm me 9876543210', ip='198.51.100.77')
        log = buf.getvalue()
        for secret in ('198.51.100.77', 'marmalade', '9876543210', 'plotpari'):
            self.assertNotIn(secret, log)
        for row in self.store.list_type('talk_signal'):
            self.assertFalse(row.get('ip_key'))
            self.assertNotIn('marmalade', json.dumps(row))

    def test_admin_api_surface_is_metaobjects_only(self):
        src = open(talks.__file__, encoding='utf-8').read()
        roots = set(re.findall(r'(?:query|mutation)\([^)]*\)\s*\{\s*(\w+)', src))
        roots |= set(re.findall(r"gql\('(?:query|mutation)[^{]*\{\s*(\w+)", src))
        self.assertTrue(roots)
        self.assertTrue(roots <= {'metaobjectByHandle', 'metaobject', 'metaobjects', 'metaobjectCreate', 'metaobjectUpdate',
                                  'metaobjectDelete', 'nodes'}, roots)

    def test_no_secrets_in_code(self):
        src = open(talks.__file__, encoding='utf-8').read()
        self.assertIsNone(re.search(r'shp(at|ss|ca|pa)_[0-9a-fA-F]{8,}', src))
        self.assertIsNone(re.search(r'(?i)(secret|token|salt)\s*=\s*[\'"][^\'"]{12,}[\'"]', src))
        for name in ('SHOPIFY_CLIENT_SECRET', 'SHOPIFY_CLIENT_ID', 'TALKS_SALT'):
            self.assertIn(f"env('{name}')", src)


class Wsgi(unittest.TestCase):
    """The Vercel entrypoint itself: app(environ, start_response)."""

    def run_app(self, method, path, query='', body=b'', headers=None):
        import io
        environ = {'REQUEST_METHOD': method, 'PATH_INFO': path, 'QUERY_STRING': query,
                   'CONTENT_LENGTH': str(len(body)), 'wsgi.input': io.BytesIO(body)}
        for k, v in (headers or {}).items():
            key = k.upper().replace('-', '_')
            environ[key if key in ('CONTENT_TYPE', 'CONTENT_LENGTH') else 'HTTP_' + key] = v
        seen = {}
        out = b''.join(talks.app(environ, lambda status, hdrs: seen.update(status=status, headers=dict(hdrs))))
        return seen['status'], seen['headers'], out

    def test_info_page(self):
        status, headers, out = self.run_app('GET', '/')
        self.assertEqual(status, '200 OK')
        self.assertIn('text/html', headers['Content-Type'])
        self.assertIn('Small Talk talks'.encode(), out)
        self.assertIn('→'.encode(), out)

    def test_health_and_unsigned_post(self):
        status, _, out = self.run_app('GET', '/api/talks')
        body = json.loads(out)
        self.assertEqual((status, body['service'], body['build'], body['configured']), ('200 OK', 'talks', talks.BUILD, True))
        status, _, out = self.run_app('POST', '/api/talks', body=b'{"action":"post"}', headers={'Content-Type': 'application/json'})
        self.assertEqual((status, json.loads(out)['code']), ('401 Unauthorized', 'unauthorised'))

    def test_not_configured_never_crashes(self):
        saved = {k: os.environ.pop(k) for k in ('SHOPIFY_SHOP', 'SHOPIFY_CLIENT_ID', 'SHOPIFY_CLIENT_SECRET')}
        try:
            talks.STORE = talks.Store()
            status, _, out = self.run_app('GET', '/api/talks')
            self.assertEqual(json.loads(out)['configured'], False)
            talks._last_prune['at'] = 0
            status, _, out = self.run_app('GET', '/api/talks', query='task=prune')
            self.assertEqual((status, json.loads(out)), ('200 OK', {'ok': False}))
        finally:
            os.environ.update(saved)

    def test_no_diag_and_404(self):
        # ?diag=ip is gone: the request gets the plain health answer and no forwarding headers are echoed
        status, _, out = self.run_app('GET', '/api/talks', query='diag=ip',
                                      headers={'X-Forwarded-For': '1.2.3.4, 5.6.7.8', 'X-Real-IP': '5.6.7.8'})
        body = json.loads(out)
        self.assertEqual(body.get('service'), 'talks')
        self.assertFalse({'x_forwarded_for', 'x_real_ip', 'via_proxy', 'network_key_used'} & set(body))
        self.assertNotIn('1.2.3.4', out.decode() if isinstance(out, bytes) else out)
        status, _, out = self.run_app('GET', '/nope')
        self.assertEqual(status, '404 Not Found')



if __name__ == '__main__':
    unittest.main()
