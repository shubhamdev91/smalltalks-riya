"""the talks: write path for Small Talk's anonymous threads (Vercel Python app, standard library only).

Vercel entrypoint: this file's WSGI `app` (pyproject.toml [tool.vercel] entrypoint = "app:app"); every path comes here.
  GET  /                 info page (no data)
  GET  /api/talks        health: {"ok", "service", "build", "configured"}; ?task=prune = daily cron; through the
                         App Proxy: {"ok", "open"} (what the posting switch reads)
  POST /api/talks        post | reply | report (App Proxy signature required)

Storefront  POST /apps/talks  (Shopify App Proxy, HMAC-signed)  ->  this app at /api/talks
            (or direct POST with CORS locked to the store origins, if the theme is set to direct mode)

Actions (JSON body): post | reply | report. Data lives in Shopify metaobjects (talk_thread, talk_reply,
talk_topic, private talk_signal / talk_settings). Visibility = the metaobject's own Active/Draft status.

Environment (set by the store owner in Vercel, never in code):
  SHOPIFY_SHOP            0nev20-vn.myshopify.com
  SHOPIFY_CLIENT_ID       Dev Dashboard app -> Settings -> Client ID
  SHOPIFY_CLIENT_SECRET   Dev Dashboard app -> Settings -> Client secret (also verifies App Proxy signatures)
  TALKS_SALT              a long random string; salts the one-way keys for device / network / text (if missing, a
                          salt is derived from SHOPIFY_CLIENT_SECRET, so rotating the secret also rotates the keys)
Optional:
  TALKS_ALLOWED_ORIGINS   comma-separated store origins; set it ONLY to enable direct (CORS) mode

Privacy: no name, email, account id, raw IP or raw device id is ever stored or logged. talk_signal rows hold: the
action kind, a salted HMAC key of the device id, a salted HMAC key of the text (duplicate check), the target entry id
and the time. Behind the App Proxy no network/IP key is used or stored at all (Vercel replaces the forwarded shopper
address with the proxy's, so it would be meaningless); only the optional direct (CORS) mode keys the network too.
Rows are deleted after SIGNAL_DAYS (pruned on every write and by a daily Vercel cron).
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import random
import re
import threading
import time
import unicodedata
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qsl, urlencode, urlsplit
from urllib.request import Request, urlopen

API_VERSION = '2026-10'
try:  # fingerprint of this file, shown by the health check so a deploy can be matched to the tested source
    with open(__file__, 'rb') as _src:
        BUILD = hashlib.md5(_src.read()).hexdigest()[:12]
except OSError:
    BUILD = 'unknown'
SETS = ('on-me', 'brainwave', 'diet-cherry', 'green-flag', 'shaadi-shift', 'wild-card', 'pinky-promise')
OWN_TOPIC = 'something-else'  # her own topic words are filed under this topic

LIMITS = {
    # kind: (max in 10 min, max in 24 h)
    'post': (3, 10),
    'reply': (8, 60),
    'report': (10, 20),
}
FLOOD_PER_HOUR = {'post': 40, 'reply': 200}  # store-wide; above this new posts are held, not lost
REPORTS_TO_HIDE = 3
THREAD_MIN, THREAD_MAX = 3, 1200
REPLY_MIN, REPLY_MAX = 1, 800
ALIAS_MIN, ALIAS_MAX = 2, 24
TOPIC_OWN_MAX = 30
TITLE_MAX = 110
LIST_CAP = 1024
MIN_COMPOSE_MS = 2000  # faster than this from opening the composer = bot
MAX_BODY_BYTES = 16 * 1024
SIGNAL_DAYS = 7  # talk_signal retention; the shopper-facing promise (TLK-148) is "within 30 days"
PRUNE_BATCH = 25
MAX_DEPTH = 8  # stored nesting cap; deeper replies stay at this depth (the theme shows 4 levels on phones)


def env(name: str, default: str = '') -> str:
    return (os.environ.get(name) or default).strip()


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


class TalkError(Exception):
    """A refusal the shopper should see (code maps to a theme string)."""

    def __init__(self, code: str, status: int = 422, **extra):
        super().__init__(code)
        self.code, self.status, self.extra = code, status, extra


# --------------------------------------------------------------------------------------------------------------
# Moderation. Pure functions; the contact/link/handle checks are mirrored in the theme's st-talks.js for instant
# feedback, the server stays the authority.
# --------------------------------------------------------------------------------------------------------------

ZERO_WIDTH = re.compile('[' + chr(0x200B) + '-' + chr(0x200F) + chr(0x2060) + chr(0xFEFF) + chr(0x00AD) + ']')
LEET = str.maketrans({'0': 'o', '1': 'i', '3': 'e', '4': 'a', '5': 's', '7': 't', '@': 'a', '$': 's', '!': 'i', '|': 'i'})

PHONE_RUN = re.compile(r'\+?\d[\d\s\-().]{6,}\d')
EMAIL = re.compile(r'[a-z0-9._%+\-]+@[a-z0-9\-]+(?:\.[a-z0-9\-]+)+', re.I)
EMAIL_SPELLED = re.compile(r'\b[a-z0-9._%+\-]{2,}\s*(?:\(at\)|\[at\]|\{at\}|\sat\s)\s*(?:gmail|yahoo|outlook|hotmail|icloud|rediffmail|rediff|proton|protonmail|live)\b', re.I)
UPI = re.compile(r'\b[a-z0-9._\-]{2,}@(?:ok)?(?:axis|hdfc|icici|sbi|ybl|paytm|upi|apl|ibl|axl)\b', re.I)
HANDLE = re.compile(r'(?:^|[^\w@])@[a-z0-9_.]{2,}', re.I)
SOCIAL_ID = re.compile(
    r'\b(?:insta|instagram|ig|snap|snapchat|sc|twitter|tiktok|telegram|tg|discord|threads|bumble|hinge|tinder|bereal)'
    r'\s*(?:id|handle|username|user\s*name|user)?\s*(?:[:=]|->|→)\s*@?[a-z0-9_.]{3,}', re.I)
SOCIAL_ID_WORDS = re.compile(
    r'\b(?:insta|instagram|ig|snap|snapchat|twitter|telegram|discord)\s+(?:id|handle|username)\s+(?:is\s+|hai\s+|:)?@?[a-z0-9_.]{3,}', re.I)
URL = re.compile(r'(?:https?://|\bwww\.)\S+', re.I)
DOMAIN = re.compile(
    r'\b[a-z0-9][a-z0-9\-]{1,62}\.(?:com|in|net|org|co|io|me|ly|app|xyz|link|gg|tv|info|biz|shop|store|site|online|'
    r'live|club|page|to|fm|cc|ai|dev|lol|social|chat|bio|ink|xxx)(?:\.[a-z]{2,3})?\b(?:/\S*)?', re.I)
WA_LINK = re.compile(r'\bwa\.me\b|\bt\.me\b|\bbit\.ly\b|\blinktr\.ee\b', re.I)

# Identity slurs and severe abuse (English, Hindi, Hinglish). Matched on normalised whole words; the owner adds more
# in Shopify admin (Talks settings -> Extra blocked words).
BLOCKED_WORDS = {
    # race / ethnicity / religion
    'nigger', 'nigga', 'niggas', 'chink', 'chinki', 'paki', 'pakis', 'kike', 'spic', 'gook', 'coon', 'raghead',
    'towelhead', 'katua', 'katwa', 'katuwa', 'mulle', 'jihadi', 'jihadis', 'kafir', 'malechh', 'mleccha', 'chinky',
    # caste
    'chamar', 'chamaar', 'chamaro', 'bhangi', 'chuhra', 'dhed', 'neechjaat', 'neech-jaat', 'chandal',
    # sexuality / gender identity / disability
    'faggot', 'faggots', 'fag', 'fags', 'tranny', 'trannies', 'retard', 'retards', 'retarded', 'spastic', 'gandu',
    # misogynist abuse
    'whore', 'whores', 'cunt', 'cunts', 'randi', 'randiyan', 'raand', 'randibaaz', 'chinal', 'chinaal',
    'chhinal', 'kutiya', 'kuttiya',
    # severe gaalis
    'madarchod', 'maderchod', 'madarchood', 'madarjaat', 'maadarchod', 'behenchod', 'bhenchod', 'benchod',
    'behanchod', 'bhanchod', 'behenkelode', 'bhosdike', 'bhosadike', 'bhosdiwale', 'bhosdiwala', 'bhosdi', 'bhosda',
    'lavda', 'lawda', 'lauda', 'lodu', 'loda', 'chutiya', 'chutiye', 'chutia',
}
BLOCKED_PHRASES = ('neech jaat', 'neechi jaat', 'go back to pakistan', 'kill yourself', 'kys')

# Words that might be fine but often target someone: the post is held for a quick look instead of blocked.
HELD_WORDS = {
    'slut', 'sluts', 'chakka', 'chhakka', 'hijra', 'hijda', 'hijde', 'expose', 'exposed', 'exposing', 'leak', 'leaked',
    'leaking', 'stalk', 'stalked', 'stalking', 'doxx', 'dox', 'screenshot', 'screenshots', 'ss', 'nudes', 'mms',
    'address', 'pincode', 'surname',
}
HELD_PHRASES = (
    'her name', 'his name', 'their name', 'uska naam', 'uski naam', 'naam hai', 'name is', 'full name', 'real name',
    'everyone should know', 'sabko pata', 'sabko bata', 'tag her', 'tag him', 'her number', 'his number',
    'her insta', 'his insta', 'lives in', 'rehti hai', 'rehta hai', 'works at', 'studies at', 'padhti hai',
    'padhta hai', 'roll no', 'roll number',
)
SURNAMES = {
    'sharma', 'verma', 'gupta', 'singh', 'kumar', 'patel', 'shah', 'mehta', 'reddy', 'iyer', 'iyengar', 'nair', 'khan',
    'das', 'bose', 'chatterjee', 'banerjee', 'mukherjee', 'bhattacharya', 'agarwal', 'aggarwal', 'agrawal', 'jain',
    'malhotra', 'kapoor', 'khanna', 'chopra', 'arora', 'bhatia', 'sethi', 'joshi', 'pandey', 'mishra', 'tiwari',
    'trivedi', 'dwivedi', 'chaturvedi', 'yadav', 'rao', 'pillai', 'menon', 'ghosh', 'dutta', 'saxena', 'srivastava',
    'shrivastava', 'chauhan', 'rathore', 'thakur', 'kaur', 'gill', 'sandhu', 'dhillon', 'grewal', 'sidhu', 'bajwa',
    'chawla', 'khurana', 'bansal', 'goel', 'goyal', 'mittal', 'singhal', 'jindal', 'kohli', 'luthra', 'oberoi', 'sahni',
    'sawhney', 'tandon', 'tripathi', 'shukla', 'dubey', 'upadhyay', 'kulkarni', 'deshpande', 'deshmukh', 'patil',
    'pawar', 'jadhav', 'naidu', 'chowdhury', 'choudhary', 'chaudhary', 'mahajan', 'bhatt', 'desai', 'parikh',
    'modi', 'sinha', 'jha', 'mathur', 'bhargava', 'kashyap', 'rastogi', 'ahuja', 'bedi',
    'walia', 'hegde', 'shetty', 'kamath', 'krishnan', 'subramanian', 'venkatesh', 'raghavan',
    'qureshi', 'siddiqui', 'ansari', 'sheikh', 'syed', 'mirza', 'fernandes', 'dsouza', "d'souza", 'pereira', 'rodrigues',
}
# Only names that are rarely everyday Hindi/Hinglish words ("diya" = gave, "sara" = whole, "zara" = a little,
# "khushi", "muskan", "akash", "gaurav"… are left out on purpose: a hold is a review, but noise annoys honest users).
FIRST_NAMES = {
    'aanya', 'aishwarya', 'alia', 'ananya', 'anjali', 'ankita', 'anushka', 'apoorva', 'deepika', 'devika', 'ishita',
    'ishani', 'janhvi', 'jhanvi', 'kritika', 'neha', 'nikita', 'pallavi', 'priyanka', 'radhika', 'riya', 'rhea',
    'ritika', 'saloni', 'sanya', 'shreya', 'sonam', 'tanya', 'trisha', 'vaishnavi', 'vanshika', 'yashika', 'priya',
    'aarav', 'abhishek', 'amit', 'ankit', 'arjun', 'arnav', 'aryan', 'ayaan', 'ayush', 'ishaan', 'kunal', 'nikhil',
    'pranav', 'rahul', 'rishabh', 'rohan', 'rohit', 'saurabh', 'shivam', 'siddharth', 'vedant', 'vihaan', 'vikram',
}
INSTITUTIONS = re.compile(
    r'\b(?:iit|iim|nit|nift|nid|jnu|lsr|srcc|st\.?\s*stephen\'?s|miranda house|hindu college|ramjas|hansraj|kirori mal|'
    r'christ university|symbiosis|amity|manipal|bits pilani|vit|srm|st\.?\s*xavier\'?s|ashoka university|flame|mica|'
    r'nmims|jai hind|mithibai|ruia|loyola|presidency college|jamia|aligarh|bhu|du south campus|north campus)\b', re.I)
IDENTIFIERS = re.compile(
    r'\b(?:flat|house|room|wing|tower|block|sector|phase|hostel|pg|floor)\s*(?:no\.?|number|#)?\s*\d+[a-z]?\b|'
    r'\b(?:section|sec)\s+[a-h]\b|\b(?:batch|class)\s+of\s+\d{2,4}\b|'
    r'\b(?:works?|working|interns?|interning|job|office|manager|boss|team|hr)\s+(?:at|in|@)\s+[A-Z][\w&.]+', re.I)
CAPS_PAIR = re.compile(r'(?<![.!?\n]\s)(?<!^)\b([A-Z][a-z]{2,})\s+([A-Z][a-z]{2,})\b')
CAPS_ALLOWED = {
    'Small Talk', 'On Me', 'Diet Cherry', 'Green Flag', 'Shaadi Shift', 'Wild Card', 'Pinky Promise', 'Plot Twists',
    'Tiny Wins', 'Nail Talk', 'Something Else', 'Group Chat', 'Best Friend', 'New Year', 'Good Morning', 'Good Night',
}
RESERVED_ALIASES = {'smalltalk', 'small talk', 'small-talk', 'small_talk', 'admin', 'administrator', 'mod', 'moderator',
                    'official', 'team', 'support', 'shopify', 'staff', 'owner', 'founder', 'brand'}
ALIAS_OK = re.compile(r"^[\w .\-']+$", re.U)


def clean_text(text: str, keep_newlines: bool = True) -> str:
    text = unicodedata.normalize('NFKC', str(text or ''))
    text = ZERO_WIDTH.sub('', text).replace('\r\n', '\n').replace('\r', '\n')
    text = ''.join(ch for ch in text if ch == '\n' or ch == '\t' or unicodedata.category(ch)[0] != 'C')
    if keep_newlines:
        text = re.sub(r'[ \t]+', ' ', text)
        text = re.sub(r' ?\n ?', '\n', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
    else:
        text = re.sub(r'\s+', ' ', text)
    return text.strip()


def _squash(word: str) -> str:
    return re.sub(r'(.)\1+', r'\1', word)


def _join_spaced_letters(text: str) -> str:
    # "r a n d i" / "r.a.n.d.i" -> "randi"
    return re.sub(r'\b(?:\w[\s.\-_*]+){2,}\w\b', lambda m: re.sub(r'[\s.\-_*]+', '', m.group(0)), text)


def words_of(text: str) -> list[str]:
    t = unicodedata.normalize('NFKD', text.lower())
    t = ''.join(ch for ch in t if not unicodedata.combining(ch))
    t = _join_spaced_letters(t.translate(LEET))
    return re.findall(r"[a-z']+", t)


def spaced_runs(text: str) -> list[str]:
    """Letters typed apart ("a r a n d i", "b.h.o.s.d.i") joined, so a blocked word can be found inside the run."""
    t = unicodedata.normalize('NFKD', text.lower()).translate(LEET)
    return [re.sub(r'[\s.\-_*]+', '', m) for m in re.findall(r'\b(?:[a-z][\s.\-_*]+){3,}[a-z]\b', t)]


def _has_word(words: list[str], vocab: set[str]) -> str | None:
    for w in words:
        w2 = w.strip("'")
        sq = _squash(w2)
        if w2 in vocab or (len(sq) >= 5 and sq in vocab):
            return w2
    return None


def contact_code(text: str) -> str | None:
    """Phone numbers, emails, UPI ids, @handles, social ids and links are never allowed."""
    for run in PHONE_RUN.findall(text):
        if len(re.sub(r'\D', '', run)) >= 10:
            return 'blocked_contact'
    if EMAIL.search(text) or EMAIL_SPELLED.search(text) or UPI.search(text):
        return 'blocked_contact'
    if URL.search(text) or WA_LINK.search(text) or DOMAIN.search(text):
        return 'blocked_link'
    if HANDLE.search(text) or SOCIAL_ID.search(text) or SOCIAL_ID_WORDS.search(text):
        return 'blocked_handle'
    return None


def moderate(text: str, extra_blocked: set[str] = frozenset(), extra_held: set[str] = frozenset()) -> tuple[str | None, list[str]]:
    """Returns (block_code or None, hold_reasons)."""
    code = contact_code(text)
    if code:
        return code, []
    low = ' '.join(words_of(text))
    words = low.split()
    padded = f' {low} '
    if _has_word(words, BLOCKED_WORDS | set(extra_blocked)) or any(f' {p} ' in padded for p in BLOCKED_PHRASES):
        return 'blocked_words', []
    for run in spaced_runs(text):
        if any(len(w) >= 4 and w in run for w in BLOCKED_WORDS | set(extra_blocked)):
            return 'blocked_words', []
    for phrase in extra_blocked:
        if ' ' in phrase and f' {phrase} ' in padded:
            return 'blocked_words', []
    reasons = []
    hit = _has_word(words, HELD_WORDS | set(extra_held))
    if hit:
        reasons.append(f'word "{hit}"')
    for phrase in HELD_PHRASES + tuple(p for p in extra_held if ' ' in p):
        if f' {phrase} ' in padded:
            reasons.append(f'phrase "{phrase}"')
            break
    name = _has_word(words, SURNAMES) or _has_word(words, FIRST_NAMES)
    if name:
        reasons.append(f'name "{name}"')
    if INSTITUTIONS.search(text):
        reasons.append('names a college')
    if IDENTIFIERS.search(text):
        reasons.append('identifying detail')
    tokens = re.findall(r"[A-Za-z]+", text)
    title_case = tokens and sum(1 for t in tokens if t[0].isupper()) / len(tokens) > 0.5
    for a, b in ([] if title_case else CAPS_PAIR.findall(text)):
        if f'{a} {b}' not in CAPS_ALLOWED:
            reasons.append(f'"{a} {b}"')
            break
    return None, reasons


def check_alias(alias: str, extra_blocked: set[str] = frozenset()) -> str:
    alias = clean_text(alias, keep_newlines=False).lstrip('@').strip()
    if not (ALIAS_MIN <= len(alias) <= ALIAS_MAX) or not ALIAS_OK.match(alias):
        raise TalkError('bad_alias')
    flat = re.sub(r'[\s._\-]+', ' ', alias.lower()).strip()
    if flat in RESERVED_ALIASES or flat.replace(' ', '') in RESERVED_ALIASES or 'small talk' in flat or 'smalltalk' in flat.replace(' ', ''):
        raise TalkError('bad_alias')
    code, reasons = moderate(alias, extra_blocked)
    if code:
        raise TalkError('bad_alias')
    if any(r.startswith('name') or r.startswith('"') for r in reasons):
        raise TalkError('bad_alias')  # aliases must not look like a real name
    return alias


def split_title(text: str) -> tuple[str, str]:
    """First line (or its first sentence, up to 110 characters) becomes the headline, the rest the body."""
    first, _, rest = text.partition('\n')
    first, rest = first.strip(), rest.strip()
    if len(first) <= TITLE_MAX:
        return first, rest
    m = re.match(r'(.{8,%d}?[.?!…])(?:\s|$)' % TITLE_MAX, first)
    if m:
        title, remainder = m.group(1).strip(), first[m.end():].strip()
    else:
        cut = first.rfind(' ', 0, 90)
        cut = cut if cut > 40 else 90
        title, remainder = first[:cut].rstrip(' ,;:-') + '…', '…' + first[cut:].lstrip()
    return title, '\n'.join(x for x in (remainder, rest) if x)


def slugify(title: str) -> str:
    t = unicodedata.normalize('NFKD', title.lower())
    t = ''.join(ch for ch in t if ord(ch) < 128)
    t = re.sub(r'[^a-z0-9]+', '-', t).strip('-')
    if len(t) > 48:
        t = t[:48].rsplit('-', 1)[0] or t[:48]
    return t or 'talk'


def rand_suffix(n: int = 5) -> str:
    return ''.join(random.SystemRandom().choice('abcdefghjkmnpqrstuvwxyz23456789') for _ in range(n))


# --------------------------------------------------------------------------------------------------------------
# Request authentication
# --------------------------------------------------------------------------------------------------------------

def verify_proxy_signature(query: str, secret: str, max_age: int = 900, now: float | None = None) -> dict | None:
    """Shopify App Proxy: hex HMAC-SHA256 of the sorted 'k=v' params (multi-values joined by ',')."""
    if not secret or not query:
        return None
    params: dict[str, list[str]] = {}
    for k, v in parse_qsl(query, keep_blank_values=True):
        params.setdefault(k, []).append(v)
    signature = (params.pop('signature', [''])[0] or '').lower()
    if not signature:
        return None
    message = ''.join(sorted(f'{k}={",".join(v)}' for k, v in params.items()))
    expected = hmac.new(secret.encode(), message.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, signature):
        return None
    try:
        ts = int(params.get('timestamp', ['0'])[0])
    except ValueError:
        return None
    if abs((now or time.time()) - ts) > max_age:
        return None
    return {k: v[0] if len(v) == 1 else v for k, v in params.items()}


def client_ip(headers, via_proxy: bool) -> str | None:
    """Best-effort shopper IP. Through the App Proxy, Shopify sends X-Forwarded-For with the shopper's IP; if the
    host replaced it with the proxy's own address (equal to X-Real-IP), the IP is unknown and only device and global
    limits apply."""
    chain = [p.strip() for p in (headers.get('x-forwarded-for') or '').split(',') if p.strip()]
    real = (headers.get('x-real-ip') or '').strip()
    if not via_proxy:
        return real or (chain[-1] if chain else None)
    while chain and real and chain[-1] == real:
        chain.pop()
    return chain[-1] if chain else None


def keyed(value: str | None, purpose: str) -> str:
    if not value:
        return ''
    salt = env('TALKS_SALT').encode() or hmac.new(env('SHOPIFY_CLIENT_SECRET').encode(), b'talks-keys-v1', hashlib.sha256).digest()
    return hmac.new(salt, f'{purpose}:{value}'.encode(), hashlib.sha256).hexdigest()[:24]


# --------------------------------------------------------------------------------------------------------------
# Shopify Admin API (client-credentials token, cached per warm instance)
# --------------------------------------------------------------------------------------------------------------

_token_lock = threading.Lock()
_token = {'value': '', 'expires': 0.0}


def _http(url: str, data: bytes, headers: dict, timeout: float = 12.0) -> tuple[int, dict]:
    req = Request(url, data=data, headers=headers, method='POST')
    try:
        with urlopen(req, timeout=timeout) as res:
            return res.status, json.loads(res.read() or b'{}')
    except HTTPError as e:
        try:
            body = json.loads(e.read() or b'{}')
        except ValueError:
            body = {}
        return e.code, body
    except (URLError, TimeoutError, OSError):
        return 599, {}


def admin_token() -> str:
    with _token_lock:
        if _token['value'] and _token['expires'] - time.time() > 300:
            return _token['value']
        shop, cid, secret = env('SHOPIFY_SHOP'), env('SHOPIFY_CLIENT_ID'), env('SHOPIFY_CLIENT_SECRET')
        if not (shop and cid and secret):
            raise TalkError('server', 503, detail='not configured')
        status, body = _http(f'https://{shop}/admin/oauth/access_token',
                             urlencode({'grant_type': 'client_credentials', 'client_id': cid, 'client_secret': secret}).encode(),
                             {'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'application/json'})
        if status != 200 or not body.get('access_token'):
            raise TalkError('server', 502, detail=f'token {status}')
        _token['value'] = body['access_token']
        _token['expires'] = time.time() + int(body.get('expires_in') or 86399)
        return _token['value']


def gql(query: str, variables: dict | None = None) -> dict:
    url = f'https://{env("SHOPIFY_SHOP")}/admin/api/{API_VERSION}/graphql.json'
    payload = json.dumps({'query': query, 'variables': variables or {}}).encode()
    for attempt in range(3):
        status, body = _http(url, payload, {'Content-Type': 'application/json', 'X-Shopify-Access-Token': admin_token()})
        throttled = status == 429 or any((e.get('extensions') or {}).get('code') == 'THROTTLED' for e in body.get('errors') or [])
        if status == 401:
            _token['value'] = ''
        if (throttled or status >= 500 or status == 401) and attempt < 2:
            time.sleep(0.6 * (attempt + 1))
            continue
        if status != 200 or body.get('errors'):
            raise TalkError('server', 502, detail=f'gql {status} {str(body.get("errors"))[:200]}')
        return body['data']
    raise TalkError('server', 502, detail='gql retries')


def user_errors(result: dict) -> list:
    return [e for e in (result or {}).get('userErrors') or []]


class Store:
    """Everything that touches Shopify. Tests swap this for an in-memory fake."""

    MO_FIELDS = 'id handle updatedAt capabilities { publishable { status } } fields { key value }'

    @staticmethod
    def _mo(node: dict | None) -> dict | None:
        if not node:
            return None
        out = {f['key']: f['value'] for f in node.get('fields') or []}
        out['_id'], out['_handle'] = node['id'], node['handle']
        out['_status'] = ((node.get('capabilities') or {}).get('publishable') or {}).get('status') or 'ACTIVE'
        out['_updated'] = node.get('updatedAt')
        return out

    def by_handle(self, type_: str, handle: str) -> dict | None:
        q = 'query($h: MetaobjectHandleInput!) { metaobjectByHandle(handle: $h) { %s } }' % self.MO_FIELDS
        return self._mo(gql(q, {'h': {'type': type_, 'handle': handle}})['metaobjectByHandle'])

    def by_id(self, id_: str) -> dict | None:
        q = 'query($id: ID!) { metaobject(id: $id) { %s } }' % self.MO_FIELDS
        return self._mo(gql(q, {'id': id_})['metaobject'])

    def list_type(self, type_: str, query: str = '', first: int = 100) -> list[dict]:
        q = ('query($t: String!, $q: String, $n: Int!) { metaobjects(type: $t, query: $q, first: $n, sortKey: "id", '
             'reverse: true) { nodes { %s } } }' % self.MO_FIELDS)
        return [self._mo(n) for n in gql(q, {'t': type_, 'q': query or None, 'n': first})['metaobjects']['nodes']]

    def create(self, type_: str, handle: str, fields: dict, status: str | None = None) -> dict:
        m = {'type': type_, 'handle': handle, 'fields': [{'key': k, 'value': v} for k, v in fields.items() if v is not None]}
        if status:
            m['capabilities'] = {'publishable': {'status': status}}
        q = ('mutation($m: MetaobjectCreateInput!) { metaobjectCreate(metaobject: $m) { metaobject { id handle } '
             'userErrors { field message code } } }')
        r = gql(q, {'m': m})['metaobjectCreate']
        errs = user_errors(r)
        if errs:
            if any(e.get('code') == 'TAKEN' for e in errs):
                raise TalkError('handle_taken', 409)
            raise TalkError('server', 502, detail=f'create {type_}: {errs}')
        return r['metaobject']

    def update(self, id_: str, fields: dict | None = None, status: str | None = None) -> None:
        m: dict = {}
        if fields:
            m['fields'] = [{'key': k, 'value': v} for k, v in fields.items()]
        if status:
            m['capabilities'] = {'publishable': {'status': status}}
        q = ('mutation($id: ID!, $m: MetaobjectUpdateInput!) { metaobjectUpdate(id: $id, metaobject: $m) { '
             'metaobject { id } userErrors { field message code } } }')
        errs = user_errors(gql(q, {'id': id_, 'm': m})['metaobjectUpdate'])
        if errs:
            raise TalkError('server', 502, detail=f'update: {errs}')

    def delete(self, id_: str) -> None:
        gql('mutation($id: ID!) { metaobjectDelete(id: $id) { deletedId userErrors { field message } } }', {'id': id_})

    def get_list(self, id_: str, key: str) -> list[str]:
        q = 'query($id: ID!, $k: String!) { metaobject(id: $id) { field(key: $k) { value } } }'
        node = gql(q, {'id': id_, 'k': key})['metaobject']
        raw = ((node or {}).get('field') or {}).get('value')
        return json.loads(raw) if raw else []

    def states(self, ids: list[str]) -> dict[str, dict]:
        """id -> {'status', 'depth'} for replies (250 per call)."""
        out: dict[str, dict] = {}
        q = ('query($ids: [ID!]!) { nodes(ids: $ids) { ... on Metaobject { id capabilities { publishable { status } } '
             'depth: field(key: "depth") { value } } } }')
        for i in range(0, len(ids), 250):
            for n in gql(q, {'ids': ids[i:i + 250]})['nodes']:
                if n:
                    out[n['id']] = {'status': ((n.get('capabilities') or {}).get('publishable') or {}).get('status'),
                                    'depth': int(((n.get('depth') or {}).get('value')) or 0)}
        return out


STORE = Store()

# --------------------------------------------------------------------------------------------------------------
# Settings, topics, limits
# --------------------------------------------------------------------------------------------------------------

_cache: dict[str, tuple[float, object]] = {}
_burst: dict[str, list[float]] = {}
_burst_lock = threading.Lock()


def cached(key: str, ttl: float, load):
    hit = _cache.get(key)
    if hit and time.time() - hit[0] < ttl:
        return hit[1]
    value = load()
    _cache[key] = (time.time(), value)
    return value


def lines_to_set(value: str | None) -> set[str]:
    return {w.strip().lower() for w in (value or '').splitlines() if w.strip()}


def settings() -> dict:
    def load():
        s = STORE.by_handle('talk_settings', 'main') or {}
        # fail closed: only an explicit "true" opens posting (a missing entry or field keeps it shut)
        return {'open': s.get('posting_open') == 'true', 'hold_all': s.get('hold_all') == 'true',
                'blocked': lines_to_set(s.get('extra_blocked')), 'held': lines_to_set(s.get('extra_held'))}
    return cached('settings', 60, load)


def topics() -> dict[str, dict]:
    return cached('topics', 300, lambda: {t['_handle']: t for t in STORE.list_type('talk_topic', first=50)})


def burst_guard(key: str, limit: int = 4, window: float = 60.0) -> None:
    if not key:
        return
    with _burst_lock:
        stamps = [t for t in _burst.get(key, []) if time.time() - t < window]
        if len(stamps) >= limit:
            raise TalkError('rate_limited', 429, retry_after=int(window - (time.time() - stamps[0])) + 1)
        stamps.append(time.time())
        _burst[key] = stamps


def _q(value: str) -> str:
    return '"' + value.replace('\\', '').replace('"', '') + '"'


def check_limits(kind: str, ip_key: str, device_key: str, body_key: str = '') -> bool:
    """Raises rate_limited / duplicate. Returns True when the store-wide flood guard says: hold for review."""
    burst_guard(f'{kind}:{device_key}')
    if ip_key:  # only in direct (CORS) mode; behind the App Proxy there is no network key at all (decision A)
        burst_guard(f'{kind}:{ip_key}', limit=6)
    since = iso(now_utc() - timedelta(hours=24))
    who = [f'fields.device_key:{_q(device_key)}'] + ([f'fields.ip_key:{_q(ip_key)}'] if ip_key else [])
    query = f'fields.kind:{_q(kind)} AND ({" OR ".join(who)}) AND updated_at:>{_q(since)}'
    recent = STORE.list_type('talk_signal', query, first=100)
    ten_min_ago = iso(now_utc() - timedelta(minutes=10))
    short, day = LIMITS[kind]
    last10 = [s for s in recent if (s.get('at') or '') >= ten_min_ago]
    if len(last10) >= short:
        oldest = min(s.get('at') or '' for s in last10)
        wait = 600 - int((now_utc() - datetime.fromisoformat(oldest.replace('Z', '+00:00'))).total_seconds()) if oldest else 600
        raise TalkError('rate_limited', 429, retry_after=max(wait, 30))
    if len(recent) >= day:
        raise TalkError('rate_limited', 429, retry_after=3600)
    if body_key and any(s.get('body_key') == body_key for s in recent):
        raise TalkError('duplicate')
    if kind in FLOOD_PER_HOUR:
        hour = iso(now_utc() - timedelta(hours=1))
        everyone = STORE.list_type('talk_signal', f'fields.kind:{_q(kind)} AND updated_at:>{_q(hour)}', first=FLOOD_PER_HOUR[kind] + 1)
        return len(everyone) > FLOOD_PER_HOUR[kind]
    return False


def record_signal(kind: str, ip_key: str, device_key: str, target: str, body_key: str = '') -> None:
    STORE.create('talk_signal', f'{kind}-{int(time.time())}-{rand_suffix(6)}', {
        'kind': kind, 'ip_key': ip_key or None, 'device_key': device_key, 'target': target,
        'body_key': body_key or None, 'at': iso(now_utc())})


_last_prune = {'at': 0.0}


def prune_signals(force: bool = False) -> int:
    """Delete talk_signal rows older than SIGNAL_DAYS (at most PRUNE_BATCH per run, at most once a minute per
    instance unless forced). Runs alongside every write and from the daily cron, so nothing outlives ~SIGNAL_DAYS + 1."""
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


# --------------------------------------------------------------------------------------------------------------
# List maintenance (read, change, write, verify: a lost concurrent update is retried)
# --------------------------------------------------------------------------------------------------------------

def list_add(owner_id: str, key: str, gid: str, place) -> list[str]:
    """place(current_list) -> new list containing gid."""
    current: list[str] = []
    for attempt in range(4):
        current = STORE.get_list(owner_id, key)
        if gid not in current:
            current = place(current)[:LIST_CAP]
            STORE.update(owner_id, {key: json.dumps(current)})
        time.sleep(0.25 * (attempt + 1))
        current = STORE.get_list(owner_id, key)
        if gid in current:
            return current
    return current


def reply_place(new_id: str, parent_id: str | None, parent_depth: int = 0):
    """New top-level replies go last; a nested reply goes at the end of its parent's subtree (the run of following
    entries deeper than the parent), so the flat list stays in display order with siblings oldest first."""
    def place(current: list[str]) -> list[str]:
        if not parent_id or parent_id not in current:
            return current + [new_id]
        i = current.index(parent_id)
        after = current[i + 1:]
        states = STORE.states(after)
        j = next((k for k, rid in enumerate(after) if states.get(rid, {}).get('depth', 0) <= parent_depth), len(after))
        return current[:i + 1] + after[:j] + [new_id] + after[j:]
    return place


def recount_replies(thread: dict, reply_ids: list[str] | None = None) -> int:
    ids = reply_ids if reply_ids is not None else STORE.get_list(thread['_id'], 'replies')
    states = STORE.states(ids)
    return sum(1 for s in states.values() if s.get('status') == 'ACTIVE')


# --------------------------------------------------------------------------------------------------------------
# Actions
# --------------------------------------------------------------------------------------------------------------

def _common(p: dict, ctx: dict) -> tuple[dict, str, str]:
    s = settings()
    if not s['open']:
        raise TalkError('closed', 403)
    device = str(p.get('device') or '')
    if not re.fullmatch(r'[A-Za-z0-9\-]{16,64}', device):
        raise TalkError('bad_request', 400)
    return s, keyed(ctx.get('ip'), 'ip'), keyed(device, 'device')


def is_bot(p: dict) -> bool:
    try:
        t = int(p.get('t') or 0)
    except (TypeError, ValueError):
        t = 0
    return bool(str(p.get('hp') or '').strip()) or t < MIN_COMPOSE_MS


def action_post(p: dict, ctx: dict) -> dict:
    s, ip_key, device_key = _common(p, ctx)
    text = clean_text(p.get('text'))
    if len(text) < THREAD_MIN:
        raise TalkError('too_short')
    if len(text) > THREAD_MAX:
        raise TalkError('too_long')
    alias = check_alias(str(p.get('alias') or ''), s['blocked'])
    avatar = p.get('avatar') if p.get('avatar') in SETS else random.choice(SETS)
    own = clean_text(p.get('topic_own') or '', keep_newlines=False)[:TOPIC_OWN_MAX]
    topic_handle = OWN_TOPIC if own else str(p.get('topic') or '')
    topic = topics().get(topic_handle)
    if not topic or topic.get('pickable') != 'true':
        raise TalkError('need_topic')
    code, reasons = moderate(f'{own}\n{text}', s['blocked'], s['held'])
    if code:
        raise TalkError(code)
    if is_bot(p):
        return {'thread': {'handle': '', 'url': '', 'status': 'live'}}
    body_key = keyed(re.sub(r'\W+', '', text.lower()), 'text')
    flood = check_limits('post', ip_key, device_key, body_key)
    if flood:
        reasons.append('flood guard')
    if s['hold_all']:
        reasons.append('hold all')
    status = 'DRAFT' if reasons else 'ACTIVE'
    title, body = split_title(text)
    stamp = iso(now_utc())
    fields = {'title': title, 'body': body or None, 'topic': topic['_id'], 'topic_label': own or None, 'alias': alias,
              'avatar': avatar, 'by_brand': 'false', 'posted_at': stamp, 'reply_count': '0', 'report_count': '0',
              'mod_note': ('held: ' + ', '.join(reasons))[:250] if reasons else None,
              'source': 'storefront' + (' (signed-in customer)' if ctx.get('customer') else '')}
    created = None
    for _ in range(3):
        try:
            created = STORE.create('talk_thread', f'{slugify(title)}-{rand_suffix()}', fields, status)
            break
        except TalkError as e:
            if e.code != 'handle_taken':
                raise
    if not created:
        raise TalkError('server', 502, detail='handle')
    gid = created['id']
    lists = [topics()['all']['_id'], topic['_id']] if 'all' in topics() else [topic['_id']]
    with ThreadPoolExecutor(max_workers=4) as pool:
        jobs = [pool.submit(record_signal, 'post', ip_key, device_key, gid, body_key), pool.submit(prune_quietly)]
        jobs += [pool.submit(list_add, lid, 'threads', gid, lambda cur, g=gid: [g] + cur) for lid in lists]
        for j in jobs:
            j.result()
    return {'thread': {'handle': created['handle'], 'url': f'/pages/talk/{created["handle"]}', 'title': title,
                       'body': body, 'alias': alias, 'avatar': avatar, 'topic': topic_handle,
                       'topic_label': own or topic.get('label'), 'posted_at': stamp,
                       'status': 'held' if reasons else 'live'}}


def action_reply(p: dict, ctx: dict) -> dict:
    s, ip_key, device_key = _common(p, ctx)
    text = clean_text(p.get('text'))
    if len(text) < REPLY_MIN:
        raise TalkError('too_short')
    if len(text) > REPLY_MAX:
        raise TalkError('too_long')
    alias = check_alias(str(p.get('alias') or ''), s['blocked'])
    avatar = p.get('avatar') if p.get('avatar') in SETS else random.choice(SETS)
    thread = STORE.by_handle('talk_thread', str(p.get('thread') or ''))
    if not thread or thread['_status'] != 'ACTIVE':
        raise TalkError('not_found', 404)
    parent = None
    if p.get('parent'):
        parent = STORE.by_handle('talk_reply', str(p['parent']))
        if not parent or parent.get('thread') != thread['_id'] or parent['_status'] != 'ACTIVE':
            raise TalkError('not_found', 404)
    parent_depth = int(parent.get('depth') or 0) if parent else -1
    depth = min(parent_depth + 1, MAX_DEPTH)
    code, reasons = moderate(text, s['blocked'], s['held'])
    if code:
        raise TalkError(code)
    if is_bot(p):
        return {'reply': {'handle': '', 'status': 'live'}}
    body_key = keyed(thread['_id'] + re.sub(r'\W+', '', text.lower()), 'text')
    if check_limits('reply', ip_key, device_key, body_key):
        reasons.append('flood guard')
    if s['hold_all']:
        reasons.append('hold all')
    status = 'DRAFT' if reasons else 'ACTIVE'
    stamp = iso(now_utc())
    created = STORE.create('talk_reply', f'r-{rand_suffix(10)}', {
        'thread': thread['_id'], 'parent': parent['_id'] if parent else None, 'body': text, 'alias': alias, 'avatar': avatar,
        'reply_to': parent.get('alias') if parent else None, 'depth': str(depth), 'by_brand': 'false',
        'posted_at': stamp, 'report_count': '0', 'mod_note': ('held: ' + ', '.join(reasons))[:250] if reasons else None,
    }, status)
    gid = created['id']
    with ThreadPoolExecutor(max_workers=3) as pool:
        sig = pool.submit(record_signal, 'reply', ip_key, device_key, gid, body_key)
        pool.submit(prune_quietly)
        ids = list_add(thread['_id'], 'replies', gid, reply_place(gid, parent['_id'] if parent else None, max(parent_depth, 0)))
        sig.result()
    fields = {'reply_count': str(recount_replies(thread, ids))}
    if status == 'ACTIVE':
        fields['last_reply_at'] = stamp
    STORE.update(thread['_id'], fields)
    return {'reply': {'handle': created['handle'], 'thread': thread['_handle'], 'body': text, 'alias': alias,
                      'avatar': avatar, 'depth': depth, 'parent': parent['_handle'] if parent else None,
                      'reply_to': parent.get('alias') if parent else None, 'posted_at': stamp,
                      'status': 'held' if reasons else 'live'}}


def action_report(p: dict, ctx: dict) -> dict:
    device = str(p.get('device') or '')
    if not re.fullmatch(r'[A-Za-z0-9\-]{16,64}', device):
        raise TalkError('bad_request', 400)
    ip_key, device_key = keyed(ctx.get('ip'), 'ip'), keyed(device, 'device')
    kind, _, handle = str(p.get('target') or '').partition(':')
    if kind not in ('thread', 'reply') or not handle:
        raise TalkError('bad_request', 400)
    item = STORE.by_handle(f'talk_{kind}', handle)
    if not item:
        raise TalkError('not_found', 404)
    if item.get('by_brand') == 'true':
        return {'hidden': False}  # brand posts are reviewed by the owner directly
    check_limits('report', ip_key, device_key)
    previous = STORE.list_type('talk_signal', f'fields.kind:"report" AND fields.target:{_q(item["_id"])}', first=100)
    reporters = {s.get('device_key') for s in previous} | {s.get('ip_key') for s in previous if s.get('ip_key')}
    if device_key in reporters or (ip_key and ip_key in reporters):
        return {'hidden': item['_status'] != 'ACTIVE'}
    record_signal('report', ip_key, device_key, item['_id'])
    prune_quietly()
    count = len({s.get('device_key') for s in previous}) + 1
    hide = count >= REPORTS_TO_HIDE and item['_status'] == 'ACTIVE'
    fields = {'report_count': str(count)}
    if hide:
        fields['mod_note'] = f'auto-hidden: {count} reports ({iso(now_utc())[:10]})'
    STORE.update(item['_id'], fields, 'DRAFT' if hide else None)
    if hide and kind == 'reply' and item.get('thread'):
        thread = STORE.by_id(item['thread'])
        if thread:
            STORE.update(thread['_id'], {'reply_count': str(recount_replies(thread))})
    return {'hidden': hide or item['_status'] != 'ACTIVE'}


ACTIONS = {'post': action_post, 'reply': action_reply, 'report': action_report}


def handle_request(method: str, path: str, headers, body: bytes) -> tuple[int, dict, dict]:
    """Returns (status, json_body, extra_headers). Separate from the HTTP class so it can be tested directly."""
    started = time.time()
    query = urlsplit(path).query
    origin = (headers.get('origin') or '').rstrip('/')
    allowed = {o.strip().rstrip('/') for o in env('TALKS_ALLOWED_ORIGINS').split(',') if o.strip()}
    cors = {'Access-Control-Allow-Origin': origin, 'Vary': 'Origin', 'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS', 'Access-Control-Max-Age': '600'} if origin in allowed else {}
    if method == 'OPTIONS':
        return (204 if cors else 403), {}, cors
    proxy = verify_proxy_signature(query, env('SHOPIFY_CLIENT_SECRET'))
    if proxy and proxy.get('shop') != env('SHOPIFY_SHOP'):
        proxy = None
    if method == 'GET':
        if 'task=prune' in query:  # Vercel cron (daily): only deletes expired talk_signal rows, safe if called by anyone
            try:
                return 200, {'ok': True, 'pruned': prune_signals()}, {}
            except TalkError:
                return 200, {'ok': False}, {}
        if not (proxy or cors):
            configured = all(env(k) for k in ('SHOPIFY_SHOP', 'SHOPIFY_CLIENT_ID', 'SHOPIFY_CLIENT_SECRET'))
            return 200, {'ok': True, 'service': 'talks', 'build': BUILD, 'configured': configured}, {}
        try:
            return 200, {'ok': True, 'open': settings()['open']}, cors
        except TalkError:
            return 200, {'ok': True, 'open': None}, cors
    if method != 'POST':
        return 405, {'ok': False, 'code': 'bad_request'}, cors
    if not (proxy or cors):
        return 401, {'ok': False, 'code': 'unauthorised'}, {}
    if 'json' not in (headers.get('content-type') or ''):
        return 415, {'ok': False, 'code': 'bad_request'}, cors
    if len(body) > MAX_BODY_BYTES:
        return 413, {'ok': False, 'code': 'too_long'}, cors
    try:
        p = json.loads(body or b'{}')
        if not isinstance(p, dict):
            raise ValueError
    except ValueError:
        return 400, {'ok': False, 'code': 'bad_request'}, cors
    action = ACTIONS.get(str(p.get('action')))
    if not action:
        return 400, {'ok': False, 'code': 'bad_request'}, cors
    # Decision A (10 Oct): behind the App Proxy the shopper IP never reaches us, so no network key is used or stored.
    ctx = {'ip': None if proxy else client_ip(headers, False), 'customer': (proxy or {}).get('logged_in_customer_id') or ''}
    try:
        result = action(p, ctx)
        status, out = (201 if p.get('action') != 'report' else 200), {'ok': True, **result}
    except TalkError as e:
        status, out = e.status, {'ok': False, 'code': e.code, **{k: v for k, v in e.extra.items() if k != 'detail'}}
        if e.extra.get('detail'):
            print(f'talks {p.get("action")} {e.code}: {e.extra["detail"]}')
    except Exception as e:  # never leak internals to the shopper
        print(f'talks {p.get("action")} crash: {type(e).__name__}: {str(e)[:300]}')
        status, out = 500, {'ok': False, 'code': 'server'}
    print(f'talks {p.get("action")} -> {status} {out.get("code", "")} via={"proxy" if proxy else "cors"} '
          f'ip={"yes" if ctx["ip"] else "no"} {int((time.time() - started) * 1000)}ms')
    return status, out, cors


INFO_PAGE = (
    '<!doctype html><html lang="en"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex">'
    '<title>Small Talk talks</title><style>body{margin:0;padding:48px 20px;font:16px/1.5 system-ui,sans-serif;'
    'background:#fffdf5;color:#1a1a2e}main{max-width:36rem;margin:auto}h1{color:#820622;font-size:24px}</style>'
    '</head><body><main><h1>Small Talk talks</h1>'
    '<p>This app only saves posts, replies and reports from the talks on the Small Talk store.</p>'
    '<p>To moderate: Shopify admin → Content → Metaobjects → Talk thread / Talk reply '
    '(Draft hides, Active publishes).</p></main></body></html>'
)
REASONS = {200: 'OK', 201: 'Created', 204: 'No Content', 400: 'Bad Request', 401: 'Unauthorized', 403: 'Forbidden',
           404: 'Not Found', 405: 'Method Not Allowed', 409: 'Conflict', 413: 'Payload Too Large',
           415: 'Unsupported Media Type', 422: 'Unprocessable Entity', 429: 'Too Many Requests',
           500: 'Internal Server Error', 502: 'Bad Gateway', 503: 'Service Unavailable'}


class _Headers:
    """Case-insensitive request headers read from a WSGI environ."""

    def __init__(self, environ: dict):
        self.environ = environ

    def get(self, name: str, default=None):
        key = name.upper().replace('-', '_')
        if key not in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
            key = 'HTTP_' + key
        return self.environ.get(key, default)


def app(environ, start_response):  # Vercel's Python entrypoint (WSGI)
    method = (environ.get('REQUEST_METHOD') or 'GET').upper()
    path = environ.get('PATH_INFO') or '/'
    query = environ.get('QUERY_STRING') or ''
    if path in ('/', '/index.html') and method in ('GET', 'HEAD'):
        data = INFO_PAGE.encode()
        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8'), ('Cache-Control', 'no-store'),
                                  ('Content-Length', str(len(data)))])
        return [b''] if method == 'HEAD' else [data]
    if path.rstrip('/') != '/api/talks':
        status, payload, extra = 404, {'ok': False, 'code': 'not_found'}, {}
    else:
        try:
            length = int(environ.get('CONTENT_LENGTH') or 0)
        except ValueError:
            length = 0
        body = environ['wsgi.input'].read(min(length, MAX_BODY_BYTES + 1)) if length > 0 else b''
        status, payload, extra = handle_request(method, f'{path}?{query}', _Headers(environ), body)
    data = json.dumps(payload, ensure_ascii=False).encode() if (payload or status != 204) else b''
    headers = [('Content-Type', 'application/json; charset=utf-8'), ('Cache-Control', 'no-store'),
               ('X-Content-Type-Options', 'nosniff'), ('Content-Length', str(len(data)))]
    headers += list(extra.items())
    start_response(f'{status} {REASONS.get(status, "OK")}', headers)
    return [data]
