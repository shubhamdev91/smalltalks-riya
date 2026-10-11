"""PROPOSED v4 renders of the talks UX (lab only, no theme write): the owner's round 2. The writing box is the hero
(start a thread at the top of the hub; the same friendly box, smaller, replies under ANY comment), and threads are
Reddit-style (a vertical line per depth, a fold toggle on each line, 4 levels on phones then "continue this thread").
REAL STATE: the hub shows the 9 real threads (0 replies). Every frame with replies carries the visible band
"example replies: layout preview, not real posts"; aliases there are "alias one…six". No theme fixture data.
Each screen loads the real build preview and swaps #MainContent for the proposed markup + qa/talks-ux/lab/proposed.css.
Output: qa/talks-ux/renders/proposed-<screen>-<w>x<h>.png. Usage: python -I qa/talks-ux/lab/proposed_capture.py"""
import asyncio, html, json, os, time
from playwright.async_api import async_playwright

BASE, Q = 'https://0nev20-vn.myshopify.com', '?preview_theme_id=186651934933'
OUT = 'qa/talks-ux/renders'
os.makedirs(OUT, exist_ok=True)
SIZES = [(390, 844), (1536, 703)]
CSS = open('qa/talks-ux/lab/proposed.css', encoding='utf-8').read()
DATA = json.load(open('qa/talks-ux/lab/data.json', encoding='utf-8'))['threads']
C = json.load(open('qa/talks-ux/lab/copy.json', encoding='utf-8'))
V = C['v4']
import base64, pathlib
_F = pathlib.Path('spec/fonts')
# Wordmark V2 (owner kept the ORIGINAL Caveat, refined; st-fable's recommended V2, qa/talks-ux/wordmark/render_caveat.py
# COMMON + VARS['V2'], spec CAVEAT-REFINE.md). Lab-only data-URI font; production = outlined SVG mark + live-text arrow.
_INK = '#0d0b10'
_SWASH = ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 12' preserveAspectRatio='none'%3E"
          "%3Cpath d='M2 8 C 25 3, 55 2, 98 6' fill='none' stroke='%23c3021d' stroke-width='2.4' stroke-linecap='round'/%3E%3C/svg%3E\")")
WORDMARK_CSS = (
    "@font-face{font-family:'WM Caveat';src:url(data:font/ttf;base64,%s) format('truetype');font-weight:400 700;font-display:block;}"
    % base64.b64encode((_F / 'caveat' / 'Caveat[wght].ttf').read_bytes()).decode()
    + f".wmc{{display:inline-flex;align-items:baseline;gap:0;color:{_INK};font-family:'WM Caveat',cursive;white-space:nowrap;line-height:1;}}"
    " .wmc .t, .wmc .k{display:inline-block;} h1 .wmc{margin-bottom:0.22em;}"
    f" .wmc-arr{{font-family:var(--font-ui,'DM Sans'),sans-serif;font-weight:500;font-size:0.5em;line-height:1;margin-left:0.22em;align-self:center;transform:translateY(-0.12em);color:{_INK};}}"
    f" .wmc{{font-weight:700;letter-spacing:-0.015em;transform:rotate(-3deg);}} .wmc .t{{margin-right:0.2em;}}"
    f" .wmc .k{{padding-bottom:0.16em;background:{_SWASH} left bottom / 100% 0.3em no-repeat;}}"
    " .tk .tk-wordmark{font-size:40px;} @media (min-width:1024px){ .tk .tk-wordmark{font-size:52px;} }")
MARK = """() => {
  const els = [...document.querySelectorAll('.st-header__talks, .st-drawer__talks, .tk-wordmark')];
  els.forEach(e => {
    const fs = parseFloat(getComputedStyle(e).fontSize);
    const arrow = e.classList.contains('st-header__talks') ? '<span class="wmc-arr" aria-hidden="true">\u2197</span>' : '';
    e.innerHTML = '<span class="wmc" style="font-size:' + fs + 'px"><span class="t">the</span><span class="k">talks</span></span>' + arrow;
    e.style.fontFamily = 'inherit';
  });
  return els.length;
}"""
HIDE = ('[id^="PBar"], #preview-bar-iframe { display: none !important; } html, body, .page-wrapper { scroll-behavior: auto !important; } '
        '*, *::before, *::after { transition: none !important; animation: none !important; caret-color: transparent !important; }')
e = html.escape
ARROW = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 12 L12 4 M5.5 4 H12 V10.5"/></svg>'
BUBBLE = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M2.5 3.5h11v7h-6l-3 2.5v-2.5h-2z"/></svg>'
X = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 3 L13 13 M13 3 L3 13"/></svg>'
CHEV = '<svg viewBox="0 0 12 12" aria-hidden="true"><path d="M3 4.5 L6 7.5 L9 4.5"/></svg>'
SPARK = '<svg viewBox="0 0 12 12" aria-hidden="true"><path d="M6 1.5v3M6 7.5v3M1.5 6h3M7.5 6h3"/></svg>'
LABEL = {h: l for h, l, _ in C['topics5'] + C['topics4']}
TOPICS = C['topics5']


def av(base, set_key, size=''):
    return (f'<span class="tk-av {size}"><span class="st-tavatar" style="--st-nails: url(\'{base}st-hd-nails-{set_key}.webp\')" '
            f'aria-hidden="true"><span class="st-tavatar__nail"></span></span></span>')


def row(t, base):
    return (f'<li><a class="tk-row" href="#"><span class="tk-row__av">{av(base, t["avatar"])}</span><span>'
            f'<span class="tk-meta"><b>{e(t["alias"])}</b> · 1d</span>'
            f'<h3 class="tk-row__title">{e(t["title"])}</h3><span class="tk-row__ex">{e(t["body"])}</span>'
            f'<span class="tk-foot">{BUBBLE}{e(C["no_replies"])}</span></span></a></li>')


def chips(current):
    items = [('all', C['all'], 9)] + TOPICS
    return '<nav class="tk-chips" aria-label="topics">' + ''.join(
        f'<a class="tk-chip" href="#"{" aria-current=page" if h == current else ""}><span>{e(l)}</span></a>' for h, l, _ in items) + '</nav>'


def side(current):
    items = [('all', C['all'], 9)] + TOPICS
    nav = ''.join(f'<a href="#"{" aria-current=page" if h == current else ""}>{e(l)}<span>{n}</span></a>' for h, l, n in items)
    return f'<aside class="tk-side"><p class="tk-label">topics</p><nav class="tk-nav" aria-label="topics">{nav}</nav></aside>'


def rules_card():
    lis = ''.join(f'<li>{e(x)}</li>' for x in C['rules_card'])
    return f'<div class="tk-card"><h2>{e(C["rules_card_h"])}</h2><ul class="tk-ruleslist">{lis}</ul><a class="tk-all" href="#">{e(C["rules_all"])}</a></div>'


def hero(focus=False, typed=None, topic='plot-twists'):
    text = (f'{e(typed)}<span class="tk-caret"></span>' if typed else
            f'<span class="tk-hero__ph">{e(V["hero_ph1"])}<small>{e(V["hero_ph2"])}</small></span>')
    return (f'<section class="tk-hero{" tk-hero--focus" if focus else ""}" aria-label="{e(C["cta"])}">'
            f'<div class="tk-hero__box" role="textbox" aria-multiline="true">{text}'
            f'<span class="tk-pill tk-pill--ghost"><span>{SPARK}{e(V["nudge"])}</span></span></div>'
            f'<div class="tk-hero__row"><span class="tk-pill"><span>{e(LABEL[topic])}{CHEV}</span></span>'
            f'<button class="tk-post" type="button">{e(C["post"])}</button></div>'
            f'<p class="tk-hero__fine"><span>posting as <b>plotpari</b> · <a href="#">shuffle</a></span><span>{e(C["rules_short"].split(".")[0])}.</span></p></section>')


def reply_box(to_alias=None):
    # TLK-026 in every inline box; TLK-134 "replying to {alias} ✕" gives the context (the ✕ = "cancel reply")
    to = (f'<p class="tk-to"><span>{e(V["replying_to"]).replace("{alias}", "<b>" + e(to_alias) + "</b>")}</span>'
          f'<button aria-label="cancel reply">{X}</button></p>' if to_alias else '')
    return (f'<div class="tk-hero tk-hero--reply{" tk-hero--focus" if to_alias else ""}">{to}'
            f'<div class="tk-hero__box" role="textbox" aria-multiline="true"><span class="tk-hero__ph">{e(V["reply_ph"])}</span></div>'
            f'<div class="tk-hero__row"><span class="tk-hero__fine"><span>replying as <b>plotpari</b></span></span>'
            f'<span><button class="tk-cancel">{e(V["cancel"])}</button> <button class="tk-post">{e(V["reply_btn"])}</button></span></div></div>')


def hub(base, current='all', focus=False, typed=None):
    rows = DATA if current == 'all' else [t for t in DATA if t['topic'] == current]
    feed = '<ul class="tk-rows">' + ''.join(row(t, base) for t in rows) + '</ul>'
    rules = C['rules_row'].split(' · ')
    return (f'<div class="tk tk-page{" tk-typing" if focus else ""}">{side(current)}<main class="tk-main">'
            f'<header><h1 class="tk-wordmark">{e(C["wordmark"])}</h1><p class="tk-promise">{e(C["promise"])}</p></header>'
            f'{hero(focus, typed)}{chips(current)}'
            f'<div class="tk-feedhead"><span class="tk-label">{e(C["latest"])}</span><span>{len(rows)} talks</span></div>{feed}'
            f'<details class="tk-rules"><summary>{e(rules[0])} <span>{e(rules[1])} ›</span></summary></details>'
            f'<p class="tk-sign">{e(C["sign"])}</p></main><aside class="tk-rail">{rules_card()}</aside>'
            f'<div class="tk-dock"><button class="tk-cta" type="button">{e(C["cta"])}{ARROW}</button></div></div>')


# The banded example tree: (depth, alias, colour, light, when, body, has_children)
TREE = [
    (0, 'alias one', 'on-me', False, '2h', 'This is an example reply, to show the layout.', True),
    (1, 'alias two', 'brainwave', True, '1h', 'Replies sit under the comment they answer.', True),
    (2, 'alias three', 'green-flag', True, '58m', 'You can reply to any comment, even mid-thread.', True),
    (3, 'alias four', 'shaadi-shift', False, '40m', 'Each level gets its own thread line.', True),
    (1, 'alias five', 'pinky-promise', True, '35m', 'Tap a thread line to fold that branch away.', False),
    (0, 'alias six', 'wild-card', False, '20m', 'A folded comment shows how many replies it hides.', True),
]


def comment(d, alias, colour, light, when, body, parent, folded=False, more=0, extra=''):
    cls = 'tk-c' + (' tk-c--parent' if parent and not folded else '') + (' tk-c--folded' if folded else '')
    # TLK-179: the fold toggle on the comment's thread line, "−" open / "+ {n}" folded (n = real hidden-reply count)
    toggle = ''
    if parent and not folded:
        toggle = (f'<button class="tk-c__fold" aria-expanded="true" aria-label="collapse {e(alias)}’s reply">'
                  f'<span class="tk-c__fold-ico">{e(V["fold_open"])}</span></button>')
    more_txt = V['more_one'] if more == 1 else V['more_n'].replace('{n}', str(more))
    more_btn = (f'<button class="tk-c__more" aria-expanded="false" aria-label="expand {e(alias)}’s reply, {more} more">'
                f'+ {e(more_txt)}</button>' if folded else '')
    return (f'<div class="{cls}" style="--d:{d}">{toggle}<p class="tk-c__head"><span class="tk-c__av{" tk-c__av--light" if light else ""}" '
            f'style="--c: var(--st-tile-{colour})" aria-hidden="true">{alias.split()[-1][0].upper()}</span>'
            f'<b>{e(alias)}</b><span>· {when}</span>{more_btn}</p><p class="tk-c__body">{e(body)}</p>'
            f'<div class="tk-c__acts"><button class="tk-act">{e(V["reply_btn"])}</button><button class="tk-act">{e(C["report"])}</button></div>{extra}</div>')


def comments(inline_under=None):
    out = [f'<p class="tk-example" role="note">{e(C["example_band"])}</p>']
    for d, alias, colour, light, when, body, parent in TREE:
        folded = alias == 'alias six'
        extra = reply_box(alias) if alias == inline_under else ''
        out.append(comment(d, alias, colour, light, when, body, parent, folded=folded, more=2, extra=extra))
        if alias == 'alias four':
            out.append(f'<a class="tk-continue" style="--d:4" href="#">{e(V["continue"])}</a>')
    return '<div class="tk-comments">' + ''.join(out) + '</div>'


def thread(base, inline_under=None):
    t = DATA[0]
    return (f'<div class="tk tk-page">{side(t["topic"])}<main class="tk-main">'
            f'<a class="tk-back" href="#">{e(C["back"])}</a>'
            f'<article class="tk-op">{av(base, t["avatar"], "tk-av-48")}<p class="tk-meta"><b>{e(t["alias"])}</b> · 1d · {e(LABEL[t["topic"]])}</p>'
            f'<h1 class="tk-op__title">{e(t["title"])}</h1><p class="tk-op__body">{e(t["body"])}</p>'
            f'<div class="tk-op__foot"><span>example</span><button class="tk-act">{e(C["report"])}</button></div></article>'
            f'{reply_box() if not inline_under else ""}'
            f'<section class="tk-replies"><h2 class="tk-label">{e(C["replies_label"])}</h2>{comments(inline_under)}</section>'
            f'<div class="tk-own"><p>{e(C["own_h"])}</p><a href="#">{e(C["own_link"])}</a></div>'
            f'</main><aside class="tk-rail">{rules_card()}</aside></div>')


EXTRA_CSS = (' .tk-example { position: sticky; top: calc(var(--st-header-h, 76px) + 6px); z-index: 4; margin: 4px 0 6px; padding: 8px 12px; border-radius: 10px; background: repeating-linear-gradient(-45deg, #fff4c2 0 10px, #ffeaa0 10px 20px); color: #4a3b00; font-size: 13px; font-weight: 700; text-align: center; box-shadow: 0 4px 10px -6px rgb(74 59 0 / 0.5); }'
             ' .tk-op + .tk-hero--reply { margin-top: 12px; }')
SWAP = """([markup, css]) => {
  const main = document.querySelector('#MainContent');
  main.innerHTML = markup; main.style.display = 'block'; main.style.padding = '0';
  const st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
}"""


async def open_page(b, path, w, h):
    pg = await b.new_page(viewport={'width': w, 'height': h})
    await pg.goto(f'{BASE}{path}{Q}&_cb={time.time_ns()}', wait_until='networkidle', timeout=60000)
    await pg.add_style_tag(content=HIDE)
    base = await pg.evaluate("""() => { const s = [...document.querySelectorAll('script[src*="/assets/"], link[href*="/assets/"]')]
      .map(x => x.src || x.href).find(u => u.includes('/assets/')); return s.slice(0, s.indexOf('/assets/') + 8); }""")
    return pg, base


async def settle(pg):
    await pg.evaluate('document.fonts.ready')
    await pg.evaluate(r"""async () => { const urls = new Set([...document.querySelectorAll('[style*="st-hd-nails"]')]
      .map(e => (e.getAttribute('style').match(/url\('([^']+)'\)/) || [])[1]).filter(Boolean));
      await Promise.all([...urls].map(u => { const i = new Image(); i.src = u; return i.decode().catch(() => null); })); }""")
    await pg.wait_for_load_state('networkidle')
    await pg.wait_for_timeout(500)
    await pg.evaluate("() => { const pw = document.querySelector('.page-wrapper'); if (pw) pw.scrollTop = 0; window.scrollTo(0, 0); }")


async def scroll_to(pg, selector, offset):
    await pg.evaluate("""([sel, off]) => { const el = document.querySelector(sel); const pw = document.querySelector('.page-wrapper');
      const s = pw && getComputedStyle(pw).overflowY !== 'visible' && pw.scrollHeight > pw.clientHeight ? pw : document.scrollingElement;
      s.scrollTop += el.getBoundingClientRect().top - off; }""", [selector, offset])
    await pg.wait_for_timeout(300)


async def render(b, name, w, h, markup, scroll=None):
    pg, base = await open_page(b, '/blogs/the-talks', w, h)
    # owner, 10 Oct: A/B/C rejected; the refined original Caveat V2 (st-fable) is the default
    wm = os.environ.get('TALKS_WORDMARK', 'V2')  # 'now' = today's Caveat
    await pg.evaluate(SWAP, [markup(base), CSS + EXTRA_CSS + (WORDMARK_CSS if wm == 'V2' else '')])
    if wm == 'V2':
        await pg.evaluate(MARK)
    await settle(pg)
    if scroll:
        await scroll_to(pg, *scroll)
    await pg.screenshot(path=f'{OUT}/proposed-{name}-{w}x{h}.png')
    await pg.close()


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        for w, h in SIZES:
            phone = w < 1024
            await render(b, 'hub', w, h, lambda base: hub(base))
            await render(b, 'composer', w, h, lambda base: hub(base, focus=True, typed='okay so this just happened…'),
                         scroll=('.tk-hero', 90 if phone else 110))
            await render(b, 'thread', w, h, lambda base: thread(base), scroll=('.tk-replies', 90 if phone else 110))
            await render(b, 'inline-reply', w, h, lambda base: thread(base, inline_under='alias three'),
                         scroll=('.tk-hero--reply', 300 if phone else 330))
        await b.close()

asyncio.run(main())
