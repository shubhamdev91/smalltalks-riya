"""Backend v7 (owner decisions, 10 Oct), on top of v5 (fail-closed, no diag) + v6 (nesting). Local only; it ships in the
one backend deploy after the owner's OK (v0 Publish).
NO REVIEW QUEUE: nothing a shopper writes waits for the owner.
- "might name someone" (moderate() reasons: names, institutions, identifiers, held words) is REFUSED at submit with
  code might_name (TLK-181). Nothing is saved (no thread/reply, no signal).
- The store-wide flood guard REFUSES with code busy (TLK-182, 429) instead of holding.
- Blocked content (contact details, links, handles, slurs) is refused at submit as before.
- The only automatic removal stays the auto-hide at 3 distinct reports. hold_all remains the owner's emergency lever
  and is "false" (it is the only path that can still hold).
- The hidden "something-else" topic is accepted only through "your own" (topic_own), never picked directly.
SECURITY tests are added for every item in talks/backend/SECURITY-v5.md. Run from talks/backend."""

p = 'app.py'
s = open(p, encoding='utf-8').read()
reps = [
    ("""FLOOD_PER_HOUR = {'post': 40, 'reply': 200}  # store-wide; above this new posts are held, not lost""",
     """FLOOD_PER_HOUR = {'post': 40, 'reply': 200}  # store-wide; above this new posts are refused for a while (busy)"""),
    ("""    \"\"\"Raises rate_limited / duplicate. Returns True when the store-wide flood guard says: hold for review.\"\"\"""",
     """    \"\"\"Raises rate_limited / duplicate. Returns True when the store-wide flood guard trips (the caller refuses: busy).\"\"\""""),
    # post: topic allow-list + refuse instead of hold
    ("""    topic_handle = OWN_TOPIC if own else str(p.get('topic') or '')
    topic = topics().get(topic_handle)
    if not topic or topic.get('pickable') != 'true':
        raise TalkError('need_topic')
    code, reasons = moderate(f'{own}\\n{text}', s['blocked'], s['held'])
    if code:
        raise TalkError(code)
    if is_bot(p):
        return {'thread': {'handle': '', 'url': '', 'status': 'live'}}
    body_key = keyed(re.sub(r'\\W+', '', text.lower()), 'text')
    flood = check_limits('post', ip_key, device_key, body_key)
    if flood:
        reasons.append('flood guard')
    if s['hold_all']:
        reasons.append('hold all')""",
     """    topic_handle = OWN_TOPIC if own else str(p.get('topic') or '')
    if topic_handle == OWN_TOPIC and not own:
        raise TalkError('need_topic')  # the hidden home of "your own" posts is never picked directly
    topic = topics().get(topic_handle)
    if not topic or topic.get('pickable') != 'true':
        raise TalkError('need_topic')
    code, reasons = moderate(f'{own}\\n{text}', s['blocked'], s['held'])
    if code:
        raise TalkError(code)
    if reasons:  # owner, 10 Oct: no review queue. Might name someone -> refused at submit, nothing saved (TLK-181)
        raise TalkError('might_name')
    if is_bot(p):
        return {'thread': {'handle': '', 'url': '', 'status': 'live'}}
    body_key = keyed(re.sub(r'\\W+', '', text.lower()), 'text')
    if check_limits('post', ip_key, device_key, body_key):
        raise TalkError('busy', 429, retry_after=600)  # store-wide flood: refused (TLK-182), never held
    reasons = ['hold all'] if s['hold_all'] else []  # the owner's emergency lever; "false" = no review queue"""),
    # reply
    ("""    code, reasons = moderate(text, s['blocked'], s['held'])
    if code:
        raise TalkError(code)
    if is_bot(p):
        return {'reply': {'handle': '', 'status': 'live'}}
    body_key = keyed(thread['_id'] + re.sub(r'\\W+', '', text.lower()), 'text')
    if check_limits('reply', ip_key, device_key, body_key):
        reasons.append('flood guard')
    if s['hold_all']:
        reasons.append('hold all')""",
     """    code, reasons = moderate(text, s['blocked'], s['held'])
    if code:
        raise TalkError(code)
    if reasons:  # no review queue: refused at submit, nothing saved (TLK-181)
        raise TalkError('might_name')
    if is_bot(p):
        return {'reply': {'handle': '', 'status': 'live'}}
    body_key = keyed(thread['_id'] + re.sub(r'\\W+', '', text.lower()), 'text')
    if check_limits('reply', ip_key, device_key, body_key):
        raise TalkError('busy', 429, retry_after=600)
    reasons = ['hold all'] if s['hold_all'] else []"""),
]
for a, b in reps:
    assert s.count(a) == 1, a[:80]
    s = s.replace(a, b)
open(p, 'w', encoding='utf-8', newline='\n').write(s)

t = 'tests/test_talks.py'
s = open(t, encoding='utf-8').read()
a = s[s.index("    def test_blocked_and_held(self):"):s.index("    def test_rate_limit_and_duplicate(self):")]
b = """    def test_blocked_and_might_name_refused(self):
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

"""
s = s.replace(a, b)
s = s.replace("""        self.store.update(s['_id'], {'posting_open': 'true', 'hold_all': 'true'})
        self.assertEqual(self.post('hello there friends')[1]['thread']['status'], 'held')""",
              """        self.store.update(s['_id'], {'posting_open': 'true', 'hold_all': 'true'})  # the owner's emergency lever only
        self.assertEqual(self.post('hello there friends')[1]['thread']['status'], 'held')""")

a = """class Wsgi(unittest.TestCase):"""
b = '''class Security(Base):
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
        status, body = self.post('Cafe\\u0301 talk\\u0000 with \\u200bhidden\\u200d chars\\u0007 here')
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
        user = re.compile(r'\\{\\{-?\\s*([^}]*?(?:\\.(?:title|body|alias|topic_label|reply_to)\\.value|t_alias|r_alias|excerpt)[^}]*)-?\\}\\}')
        bad = []
        for f in files:
            for m in user.finditer(open(f, encoding='utf-8').read()):
                expr = m.group(1)
                if '| escape' not in expr and '|escape' not in expr:
                    bad.append((os.path.basename(f), expr.strip()[:80]))
        self.assertEqual(bad, [])
        js = open(os.path.join(root, 'assets', 'st-talks.js'), encoding='utf-8').read()
        sinks = re.findall(r'(innerHTML|outerHTML)\\s*=\\s*([^;]+);', js)
        self.assertTrue(all(v.strip().startswith(("'", '"', '`')) and '${' not in v for _, v in sinks), sinks)
        self.assertNotIn('insertAdjacentHTML', js)

    def test_rate_limits_reply_and_report_per_device(self):
        _, t = self.post('thread for limits')
        d = self.device()
        codes = [self.call({'action': 'reply', 'thread': t['thread']['handle'], 'text': f'reply number {i}', 'alias': 'plotpari',
                            'device': d, 't': 5000})[0] for i in range(talks.LIMITS['reply'][0] + 1)]
        self.assertEqual(codes[-1], 429)
        self.assertEqual(self.call({'action': 'reply', 'thread': t['thread']['handle'], 'text': 'reply number 0', 'alias': 'plotpari',
                                    'device': self.device(), 't': 5000})[1]['code'], 'duplicate')
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
        roots = set(re.findall(r'(?:query|mutation)\\([^)]*\\)\\s*\\{\\s*(\\w+)', src))
        roots |= set(re.findall(r"gql\\('(?:query|mutation)[^{]*\\{\\s*(\\w+)", src))
        self.assertTrue(roots)
        self.assertTrue(roots <= {'metaobjectByHandle', 'metaobject', 'metaobjects', 'metaobjectCreate', 'metaobjectUpdate',
                                  'metaobjectDelete', 'nodes'}, roots)

    def test_no_secrets_in_code(self):
        src = open(talks.__file__, encoding='utf-8').read()
        self.assertIsNone(re.search(r'shp(at|ss|ca|pa)_[0-9a-fA-F]{8,}', src))
        self.assertIsNone(re.search(r'(?i)(secret|token|salt)\\s*=\\s*[\\'"][^\\'"]{12,}[\\'"]', src))
        for name in ('SHOPIFY_CLIENT_SECRET', 'SHOPIFY_CLIENT_ID', 'TALKS_SALT'):
            self.assertIn(f"env('{name}')", src)


class Wsgi(unittest.TestCase):'''
assert s.count(a) == 1
s = s.replace(a, b)
open(t, 'w', encoding='utf-8', newline='\n').write(s)
print('ok')
