"""locale_insert_v4.py <base en.default.json> <out> : insert-only locale change for the talks v4 window.
Inserts ONE new object, small_talk › talks › live › "v4" (st-copy register v1.7: TLK-005…182, lowercase), right after
the anchor line "moved" inside small_talk › talks › live. Proves the change is insert-only: the output minus the
inserted lines is byte-identical to the base, the JSON (comments stripped) parses, and every new key resolves to its
value. Run it on the CURRENT remote file (re-fetch the md5 first).
Usage: python -I talks/tools/locale_insert_v4.py theme-build/src/locales/en.default.json <out>"""
import json
import re
import sys

ANCHOR = '"moved": "This talk has moved.",'
V4 = {
    # hub (TLK-005, 007, 013, 015, 153, 156, 161, 163-165, 173-176, 104, 113, 143)
    'cta': 'spill your tea',
    'all': 'all',
    'latest': 'latest',
    'more': 'more talks',
    'no_replies': 'no replies yet',
    'empty': 'no talks yet. be the first to spill.',
    'empty_title': 'it’s quiet in here…',
    'empty_line': 'no talks in {{ topic }} yet. start it off?',
    'empty_topic_closed': 'nothing in {{ topic }} yet.',
    'prelaunch': 'posting isn’t open yet. read along for now.',
    'box_label': 'what’s the tea? start from the beginning…',
    'box_hint': 'your first line becomes the headline.',
    'nudge': 'need a nudge?',
    'nudges': 'the tea is…|small win today…|need a second opinion on…|plot twist…|today i felt…',
    'starters': {
        'plot_twists': 'the plot twist nobody saw coming…|okay so this just happened…',
        'tiny_wins': 'small win today…|proud of myself for…',
        'second_opinions': 'need a second opinion on…|help me decide…',
        'just_venting': 'today i felt…|can i just say…',
        'nail_talk': 'the set i keep coming back to…|my nails were in the photo when…',
    },
    'topic_label': 'what’s it about?',
    'topic_own': 'your own',
    'topic_own_placeholder': 'name your topic',
    'post': 'post it',
    'posting_as': 'posting as {{ alias }}',
    'replying_as': 'replying as {{ alias }}',
    'shuffle': 'shuffle',
    'rules_line': 'talk about situations, not people.',
    'rules_toggle': 'house rules · 30-second read',
    'rules_all': 'all house rules',
    'rules_all_label': 'read all the house rules',
    'posting': 'posting…',
    'posted': 'posted. it’s live.',
    'view': 'see it',
    'failed': 'didn’t post.',
    'retry': 'retry',
    'edit': 'edit',
    'left': '{{ count }} left',
    'noscript': 'posting needs JavaScript switched on.',
    'moved': 'this talk has moved.',
    # thread (TLK-020, 023, 025, 026, 039, 133-141, 152, 168, 169, 178-180)
    'back': 'the talks',
    'replies': 'replies',
    'no_replies_thread': 'no replies yet. be the first.',
    'reply_placeholder': 'add your two cents…',
    'reply': 'reply',
    'reply_to_label': 'reply to {{ alias }}',
    'replying_to': 'replying to {{ alias }}',
    'cancel': 'cancel',
    'report': 'report',
    'report_label': 'report reply by {{ alias }}',
    'report_thread_label': 'report this talk',
    'report_confirm': 'report this for breaking the house rules?',
    'report_yes': 'yes, report',
    'reported': 'reported. thanks for looking out.',
    'hidden_for_you': 'you reported this, so it’s hidden for you.',
    'show': 'show it',
    'own_tea': 'got your own tea?',
    'own_tea_cta': 'spill it ›',
    'continue': 'continue this thread ›',
    'more_one': '1 more reply',
    'more_other': '{{ count }} more replies',
    'collapse_label': 'collapse {{ alias }}’s reply',
    'expand_label': 'expand {{ alias }}’s reply, {{ count }} more',
    'parent_hidden': 'replying to a hidden comment',
    # TLK-009: short relative times
    'time': {'just_now': 'just now', 'minutes': '{{ count }}m', 'hours': '{{ count }}h', 'days': '{{ count }}d'},
    # refusals (TLK-120-131, 181, 182, 034)
    'errors': {
        'need_topic': 'pick a topic first.',
        'too_short': 'say a little more.',
        'too_long': 'that’s a lot of tea. trim it to {{ max }} characters.',
        'blocked_contact': 'no numbers, emails or UPI IDs here. take it out and try again.',
        'blocked_link': 'no links here. take it out and try again.',
        'blocked_handle': 'no @handles or social IDs. take it out and try again.',
        'blocked_words': 'that word’s not allowed here. try saying it another way?',
        'bad_alias': 'pick another alias. no real names, nothing that sounds official.',
        'rate_limited': 'you’re on a roll. give it a few minutes, then try again.',
        'duplicate': 'you’ve already posted that one.',
        'closed': 'posting is paused right now. try again later.',
        'not_found': 'this talk isn’t open for replies anymore.',
        'might_name': 'this might name someone. keep it about the situation, not the person.',
        'busy': 'it’s busy in here right now. try again in a few minutes.',
        'server': 'that didn’t go through. check your connection and try again.',
    },
}


def block(obj, indent, step='  '):
    """The object as JSON lines in the file's own style (2-space steps, ': ', no trailing comma on the last key)."""
    out = []
    items = list(obj.items())
    for n, (k, v) in enumerate(items):
        comma = ',' if n < len(items) - 1 else ''
        if isinstance(v, dict):
            out.append(f'{indent}{json.dumps(k)}: {{')
            out += block(v, indent + step, step)
            out.append(f'{indent}}}{comma}')
        else:
            out.append(f'{indent}{json.dumps(k)}: {json.dumps(v, ensure_ascii=False)}{comma}')
    return out


base_path, out_path = sys.argv[1], sys.argv[2]
raw = open(base_path, 'rb').read()
nl = '\r\n' if b'\r\n' in raw else '\n'
lines = raw.decode('utf-8').split(nl)
hits = [i for i, l in enumerate(lines) if l.strip() == ANCHOR]
assert len(hits) == 1, f'anchor not unique: {ANCHOR} ({len(hits)})'
assert not any(l.strip() == '"v4": {' for l in lines), 'v4 already present'
i = hits[0]
indent = lines[i][: len(lines[i]) - len(lines[i].lstrip())]
new = [f'{indent}"v4": {{'] + block(V4, indent + '  ') + [f'{indent}}},']
lines[i + 1:i + 1] = new
added = set(range(i + 1, i + 1 + len(new)))
out = nl.join(lines)
open(out_path, 'wb').write(out.encode('utf-8'))

# proofs
kept = [l for j, l in enumerate(lines) if j not in added]
assert nl.join(kept).encode('utf-8') == raw, 'not insert-only'
data = json.loads(re.sub(r'^\s*//.*$', '', re.sub(r'/\*.*?\*/', '', out.lstrip('﻿'), flags=re.S), flags=re.M))
assert data['small_talk']['talks']['live']['v4'] == V4, 'v4 does not resolve'
assert data['small_talk']['talks']['live']['moved'] == 'This talk has moved.'
print(f'insert-only OK: +{len(new)} lines after line {i + 1}; base md5 unchanged outside the block; JSON parses; v4 resolves')
