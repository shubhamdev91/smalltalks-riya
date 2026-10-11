"""Backend v6 (talks UX v4, Reddit-style nesting), on top of v5. PROPOSAL, local only; it ships with the v5 deploy only
after the owner approves the design AND the store-data change below.
- A reply can answer ANY visible reply: depth = parent depth + 1 (stored up to MAX_DEPTH; the theme shows 4 levels on
  phones, then "continue this thread"), and the reply keeps a `parent` reference to the reply it answers.
- A new reply is placed at the end of its parent's subtree (siblings oldest first), so the flat `replies` list stays in
  display order for Liquid.
- Replying to a hidden (Draft) or foreign reply is refused (not_found), as replying to a hidden thread already is.
Store data this needs (shared data, owner approval): ONE new optional field on the talk_reply definition,
`parent` = metaobject_reference to talk_reply. It must exist BEFORE this backend is deployed, or replies would fail.
Moderation, reports and auto-hide are per reply and unchanged. Run from talks/backend."""

p = 'app.py'
s = open(p, encoding='utf-8').read()
reps = [
    ("""PRUNE_BATCH = 25
""", """PRUNE_BATCH = 25
MAX_DEPTH = 8  # stored nesting cap; deeper replies stay at this depth (the theme shows 4 levels on phones)
"""),
    ("""def reply_place(new_id: str, parent_id: str | None):
    def place(current: list[str]) -> list[str]:
        if not parent_id or parent_id not in current:
            return current + [new_id]
        i = current.index(parent_id)
        after = current[i + 1:]
        depths = STORE.states(after)
        j = next((k for k, rid in enumerate(after) if depths.get(rid, {}).get('depth', 0) == 0), len(after))
        return current[:i + 1] + after[:j] + [new_id] + after[j:]
    return place""",
     """def reply_place(new_id: str, parent_id: str | None, parent_depth: int = 0):
    \"\"\"New top-level replies go last; a nested reply goes at the end of its parent's subtree (the run of following
    entries deeper than the parent), so the flat list stays in display order with siblings oldest first.\"\"\"
    def place(current: list[str]) -> list[str]:
        if not parent_id or parent_id not in current:
            return current + [new_id]
        i = current.index(parent_id)
        after = current[i + 1:]
        states = STORE.states(after)
        j = next((k for k, rid in enumerate(after) if states.get(rid, {}).get('depth', 0) <= parent_depth), len(after))
        return current[:i + 1] + after[:j] + [new_id] + after[j:]
    return place"""),
    ("""    parent = None
    if p.get('parent'):
        parent = STORE.by_handle('talk_reply', str(p['parent']))
        if not parent or parent.get('thread') != thread['_id']:
            raise TalkError('not_found', 404)""",
     """    parent = None
    if p.get('parent'):
        parent = STORE.by_handle('talk_reply', str(p['parent']))
        if not parent or parent.get('thread') != thread['_id'] or parent['_status'] != 'ACTIVE':
            raise TalkError('not_found', 404)
    parent_depth = int(parent.get('depth') or 0) if parent else -1
    depth = min(parent_depth + 1, MAX_DEPTH)"""),
    ("""        'thread': thread['_id'], 'body': text, 'alias': alias, 'avatar': avatar,
        'reply_to': parent.get('alias') if parent else None, 'depth': '1' if parent else '0', 'by_brand': 'false',""",
     """        'thread': thread['_id'], 'parent': parent['_id'] if parent else None, 'body': text, 'alias': alias, 'avatar': avatar,
        'reply_to': parent.get('alias') if parent else None, 'depth': str(depth), 'by_brand': 'false',"""),
    ("""        ids = list_add(thread['_id'], 'replies', gid, reply_place(gid, parent['_id'] if parent else None))""",
     """        ids = list_add(thread['_id'], 'replies', gid, reply_place(gid, parent['_id'] if parent else None, max(parent_depth, 0)))"""),
    ("""                      'avatar': avatar, 'depth': 1 if parent else 0, 'parent': parent['_handle'] if parent else None,""",
     """                      'avatar': avatar, 'depth': depth, 'parent': parent['_handle'] if parent else None,"""),
]
for a, b in reps:
    assert s.count(a) == 1, a[:70]
    s = s.replace(a, b)
open(p, 'w', encoding='utf-8', newline='\n').write(s)

t = 'tests/test_talks.py'
s = open(t, encoding='utf-8').read()
a = """    def test_reply_to_hidden_thread_refused(self):"""
b = """    def test_reddit_nesting_depth_order_and_parent(self):
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

    def test_reply_to_hidden_thread_refused(self):"""
assert s.count(a) == 1
s = s.replace(a, b)
open(t, 'w', encoding='utf-8', newline='\n').write(s)
print('ok')
