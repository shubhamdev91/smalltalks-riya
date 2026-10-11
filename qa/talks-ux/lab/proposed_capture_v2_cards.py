"""PROPOSED v2 renders of the talks UX (lab only, no theme write): v0's cards and composer + st-fable REVIEW-1 (A–D),
st-copy v1.5.1. Each screen loads the real build preview (real header, footer, fonts, nail sheets), swaps #MainContent
(or the landing teaser's rows) for the proposed markup, and injects qa/talks-ux/lab/proposed.css.
REAL STATE ONLY (REVIEW-1 A): the 9 real threads, all with 0 replies. The one place replies are drawn is a separate
frame with a visible band "example replies: layout preview, not real posts". Nothing here is fixture data for the theme.
Topics: st-copy's proposed 5 (TLK-006); the as-built 4 only in the alternative crop.
Output: qa/talks-ux/renders/proposed-<screen>-<w>x<h>.png. Usage: python -I qa/talks-ux/lab/proposed_capture.py"""
import asyncio, html, json, os, time
from playwright.async_api import async_playwright

BASE, Q = 'https://0nev20-vn.myshopify.com', '?preview_theme_id=186651934933'
OUT = 'qa/talks-ux/renders'
os.makedirs(OUT, exist_ok=True)
SIZES = [(390, 844), (1536, 703), (1920, 1080)]
CSS = open('qa/talks-ux/lab/proposed.css', encoding='utf-8').read()
DATA = json.load(open('qa/talks-ux/lab/data.json', encoding='utf-8'))['threads']
C = json.load(open('qa/talks-ux/lab/copy.json', encoding='utf-8'))
HIDE = ('[id^="PBar"], #preview-bar-iframe { display: none !important; } html, body, .page-wrapper { scroll-behavior: auto !important; } '
        '*, *::before, *::after { transition: none !important; animation: none !important; caret-color: transparent !important; }')
e = html.escape
ARROW = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 12 L12 4 M5.5 4 H12 V10.5"/></svg>'
BUBBLE = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M2.5 3.5h11v7h-6l-3 2.5v-2.5h-2z"/></svg>'
X = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 3 L13 13 M13 3 L3 13"/></svg>'
DICE = ('<svg viewBox="0 0 16 16" aria-hidden="true"><rect x="2.5" y="2.5" width="11" height="11" rx="3"/>'
        '<circle cx="6" cy="6" r=".8" fill="currentColor"/><circle cx="10" cy="10" r=".8" fill="currentColor"/>'
        '<circle cx="10" cy="6" r=".8" fill="currentColor"/><circle cx="6" cy="10" r=".8" fill="currentColor"/></svg>')
LABEL = {h: l for h, l, _ in C['topics5'] + C['topics4']}


def av(base, set_key, size=''):
    return (f'<span class="tk-av {size}"><span class="st-tavatar" style="--st-nails: url(\'{base}st-hd-nails-{set_key}.webp\')" '
            f'aria-hidden="true"><span class="st-tavatar__nail"></span></span></span>')


def card(t, base, show_topic):
    tag = f'<span class="tk-meta__topic">{e(LABEL[t["topic"]])}</span>' if show_topic else ''
    return (f'<a class="tk-card" href="#"><span class="tk-card__av">{av(base, t["avatar"])}</span>'
            f'<span class="tk-meta"><b>{e(t["alias"])}</b><span>· 1d</span>{tag}'
            f'<span class="tk-meta__count">{BUBBLE}{e(C["no_replies"])}</span></span>'
            f'<h3 class="tk-card__title">{e(t["title"])}</h3><span class="tk-card__ex">{e(t["body"])}</span></a>')


def bar(base, closed=False):
    if closed:
        return (f'<div class="tk-bar tk-bar--closed" role="note">{av(base, "on-me")}'
                f'<span class="tk-bar__text">{e(C["prelaunch"])}</span><span class="tk-bar__go">{ARROW}</span></div>')
    return (f'<button class="tk-bar" type="button">{av(base, "on-me")}<span class="tk-bar__text">{e(C["trigger"])}</span>'
            f'<span class="tk-bar__go">{ARROW}</span></button>')


def chips(current, topics):
    items = [('all', C['all'], 9)] + topics
    return '<nav class="tk-chips" aria-label="topics">' + ''.join(
        f'<a class="tk-chip" href="#"{" aria-current=page" if h == current else ""}><span>{e(l)}</span></a>' for h, l, _ in items) + '</nav>'


def side(current, topics):
    items = [('all', C['all'], 9)] + topics
    nav = ''.join(f'<a href="#"{" aria-current=page" if h == current else ""}>{e(l)}<span>{n}</span></a>' for h, l, n in items)
    return (f'<aside class="tk-side"><div><h1 class="tk-title">{e(C["wordmark"])}</h1><p class="tk-tag">{e(C["tagline"])}</p></div>'
            f'<nav class="tk-nav" aria-label="topics">{nav}</nav></aside>')


def aside(base, with_bar=False):
    lis = ''.join(f'<li>{e(x)}</li>' for x in C['rules_card'])
    top = f'<div class="tk-box-card">{bar(base)}</div>' if with_bar else ''
    return (f'<aside class="tk-aside">{top}<div class="tk-box-card"><h2>{e(C["rules_card_h"])}</h2><ul class="tk-how">{lis}</ul></div>'
            f'<p class="tk-fine">{e(C["rules_row"])} · <a href="#">{e(C["rules_open"])}</a></p></aside>')


def hub(base, current='all', closed=False, topics=None):
    topics = topics or C['topics5']
    rows = DATA if current == 'all' else [t for t in DATA if t['topic'] == current]
    if rows:
        feed = '<div class="tk-feed">' + ''.join(card(t, base, current == 'all') for t in rows) + '</div>'
    else:
        line = (C['empty_p_closed'] if closed else C['empty_p']).replace('{topic}', LABEL.get(current, current))
        btn = '' if closed else f'<a class="tk-btn" href="#">{e(C["cta"])}</a>'
        feed = (f'<div class="tk-empty">{av(base, "pinky-promise", "tk-av-56")}<p class="tk-empty__h">{e(C["empty_h"])}</p>'
                f'<p class="tk-empty__p">{e(line)}</p>{btn}</div>')
    rules = C['rules_row'].split(' · ')
    return (f'<div class="tk tk-page">{side(current, topics)}<main class="tk-main">'
            f'<header class="tk-head"><h1 class="tk-title">{e(C["wordmark"])}</h1><p class="tk-tag">{e(C["tagline"])}</p></header>'
            f'<div class="tk-topbar">{bar(base, closed)}</div>{chips(current, topics)}'
            f'<div class="tk-feedhead"><span class="tk-label">{e(C["latest"])}</span><span>{len(rows)} talks</span></div>{feed}'
            f'<details class="tk-rules"><summary>{e(rules[0])} <span>{e(rules[1])} ›</span></summary></details>'
            f'<p class="tk-sign">{e(C["sign"])}</p></main>{aside(base)}</div>')


def reply(alias, colour, light, when, body, nested=False, to=''):
    to_html = f'<span class="tk-reply__to">↪ @{e(to)} </span>' if nested else ''
    return (f'<div class="tk-reply{" tk-reply--nested" if nested else ""}">'
            f'<span class="tk-reply__av{" tk-reply__av--light" if light else ""}" style="--c: var(--st-tile-{colour})" aria-hidden="true">{alias[0].upper()}</span>'
            f'<p class="tk-meta"><b>{e(alias)}</b><span>· {when}</span></p><p class="tk-reply__body">{to_html}{e(body)}</p>'
            f'<div class="tk-acts"><button class="tk-act">{e(C["reply"])}</button><button class="tk-act">{e(C["report"])}</button></div></div>')


def thread(base, example=False):
    t = DATA[0]
    if example:
        inner = (f'<p class="tk-example" role="note">{e(C["example_band"])}</p>' + ''.join([
            reply('alias one', 'on-me', False, '2h', 'An example reply, to show the layout.'),
            reply('alias two', 'brainwave', True, '1h', 'A nested reply sits one level in, with a soft connector.', nested=True, to='alias one'),
            reply('alias three', 'green-flag', True, '40m', 'Replies to a nested reply stay at this level and name who they answer.'),
        ]))
        count = 'example'
    else:
        inner = f'<p class="tk-noreplies">{e(C["zero_open"])}</p>'
        count = C['no_replies']
    who = C['replying_as'].replace('{alias}', '<b>plotpari</b>')
    rbar = (f'<div class="tk-replybar"><div class="tk-replybar__field"><span>{e(C["reply_field"])}</span><span class="tk-bar__go">{ARROW}</span></div>'
            f'<p class="tk-who">{who} · shuffle</p></div>')
    return (f'<div class="tk tk-page tk-page--thread">{side(t["topic"], C["topics5"])}<main class="tk-main">'
            f'<a class="tk-back" href="#">{e(C["back"])}</a>'
            f'<article class="tk-op"><div class="tk-meta">{av(base, t["avatar"], "tk-av-44")}<b>{e(t["alias"])}</b><span>· 1d</span>'
            f'<span class="tk-meta__topic">{e(LABEL[t["topic"]])}</span></div>'
            f'<h1 class="tk-op__title">{e(t["title"])}</h1><p class="tk-op__body">{e(t["body"])}</p>'
            f'<div class="tk-op__foot"><span>{e(count)}</span><button class="tk-act">{e(C["report"])}</button></div></article>'
            f'<section class="tk-replies"><h2 class="tk-label">{e(C["replies_label"])}</h2>{inner}</section>'
            f'<div class="tk-desk-only">{rbar}</div>'
            f'<div class="tk-own"><p>{e(C["own_h"])}</p><a href="#">{e(C["own_link"])}</a></div>'
            f'</main>{aside(base, with_bar=True)}<div class="tk-dock tk-phone-only">{rbar}</div></div>')


def sheet(base, topic='plot-twists'):
    picks = ''.join(f'<span class="tk-chip" role="radio" aria-checked="{"true" if h == topic else "false"}"><span>{e(l)}</span></span>'
                    for h, l, _ in C['topics5']) + f'<span class="tk-chip" role="radio" aria-checked="false"><span>{e(C["your_own"])}</span></span>'
    starters = ''.join(f'<span class="tk-starter"><span>{e(s)}</span></span>' for s in C['starters'][topic])
    as_line = C['posting_as'].split(' · ')[0].replace('{alias}', '<b>plotpari</b>')
    return (f'<div class="tk"><div class="tk-scrim"></div><div class="tk-sheet" role="dialog" aria-modal="true" aria-label="{e(C["cta"])}">'
            f'<span class="tk-grab"></span><div class="tk-sheet__top"><h2 class="tk-sheet__h">{e(C["cta"])}</h2>'
            f'<button class="tk-x" aria-label="close">{X}</button></div>'
            f'<div><p class="tk-label">{e(C["what"])}</p><div class="tk-picks">{picks}</div></div>'
            f'<div class="tk-text">{e(C["box_ph"])}</div>'
            f'<div><p class="tk-label">{e(C["starters_label"])}</p><div class="tk-starters">{starters}</div></div>'
            f'<div class="tk-as"><span>{as_line}</span><button>{DICE}shuffle</button></div>'
            f'<p class="tk-ruleline">{e(C["rules_short"])}</p>'
            f'<button class="tk-btn">{e(C["post"])}</button><p class="tk-fine">{e(C["reassure"])} <a href="#">{e(C["rules_link"])}</a></p></div></div>')


EXTRA_CSS = (' @media (max-width: 1023px) { .tk-desk-only { display: none; } }'
             ' @media (min-width: 1024px) { .tk-phone-only { display: none; } }')
SWAP = """([markup, css]) => {
  const main = document.querySelector('#MainContent');
  main.innerHTML = markup; main.style.display = 'block'; main.style.padding = '0';
  const st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
}"""
DOCK = """(markup) => { const host = document.querySelector('.tk-page'); host.insertAdjacentHTML('beforeend', markup); }"""
ADD = """(markup) => { document.body.insertAdjacentHTML('beforeend', markup); }"""
TEASER = """([rows, barHtml, css]) => {
  const st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
  const old = document.querySelector('.st-tt__rows');
  const box = document.createElement('div'); box.className = 'tk tk-teaser'; box.innerHTML = '<div class="tk-feed">' + rows + '</div>';
  old.replaceWith(box);
  const cta = document.querySelector('.st-tt__cta'); const cs = getComputedStyle(cta);
  const wrap = document.createElement('div'); wrap.className = 'tk tk-teaser-cta';
  wrap.innerHTML = barHtml + '<a class="tk-seeall" href="/blogs/the-talks">see all talks ›</a>';
  for (const k of ['gridRow', 'gridColumn', 'alignSelf', 'justifySelf', 'marginTop', 'marginBottom', 'order']) wrap.style[k] = cs[k];
  cta.replaceWith(wrap);
  document.querySelector('.st-tt__pre')?.remove();  /* posting-ON state */
}"""
TEASER_CSS = """.tk-teaser .tk-feed { gap: 0; margin-top: 4px; border-top: 1px solid var(--tk-line); }
.tk-teaser .tk-card { padding: 10px 2px; border: 0; border-bottom: 1px solid var(--tk-line); border-radius: 0; background: transparent; }
.tk-teaser .tk-card:last-child { border-bottom: 0; } .tk-teaser .tk-card__ex, .tk-teaser .tk-meta__topic { display: none; }
.tk-teaser-cta { display: grid; gap: 4px; width: min(100%, 420px); }
.tk-seeall { display: inline-flex; align-items: center; justify-content: center; min-height: 44px; color: #a31a33; font-size: 15px; font-weight: 700; }
@media (max-width: 1023px) { .tk-teaser .tk-card:nth-child(n+3) { display: none; } .tk-teaser-cta { margin: 0 auto; } }
@media (min-width: 1024px) { .tk-teaser .tk-card:nth-child(n+4) { display: none; } }"""


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
    await pg.evaluate("() => { const c = document.querySelector('.tk-chips .tk-chip[aria-current]'); if (c) { const r = c.parentElement; r.scrollLeft = c.offsetLeft - r.clientWidth / 2 + c.clientWidth / 2; } }")


async def scroll_by(pg, px):
    await pg.evaluate("""(px) => { const pw = document.querySelector('.page-wrapper');
      const s = pw && getComputedStyle(pw).overflowY !== 'visible' && pw.scrollHeight > pw.clientHeight ? pw : document.scrollingElement; s.scrollTop += px; }""", px)
    await pg.wait_for_timeout(300)


async def scroll_to(pg, selector, offset):
    await pg.evaluate("""([sel, off]) => { const el = sel.startsWith('section:') ? document.querySelector(sel.slice(8)).closest('.shopify-section') : document.querySelector(sel);
      const pw = document.querySelector('.page-wrapper');
      const s = pw && getComputedStyle(pw).overflowY !== 'visible' && pw.scrollHeight > pw.clientHeight ? pw : document.scrollingElement;
      s.scrollTop += el.getBoundingClientRect().top - off; }""", [selector, offset])
    await pg.wait_for_timeout(300)


async def render(b, name, w, h, markup, after=None):
    pg, base = await open_page(b, '/blogs/the-talks', w, h)
    await pg.evaluate(SWAP, [markup(base), CSS + EXTRA_CSS])
    await settle(pg)
    if after:
        await after(pg, base)
    await pg.screenshot(path=f'{OUT}/proposed-{name}-{w}x{h}.png')
    return pg


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        for w, h in SIZES:
            phone = w < 1024
            await (await render(b, 'hub', w, h, lambda base: hub(base))).close()
            if phone:  # REVIEW-1 B: after the top bar scrolls away, the same bar docks at the bottom
                async def dock(pg, base):
                    await scroll_by(pg, 640)
                    await pg.evaluate(DOCK, f'<div class="tk-dock">{bar(base)}</div>')
                    await pg.wait_for_timeout(300)
                await (await render(b, 'hub-scrolled', w, h, lambda base: hub(base), after=dock)).close()
            if w == 1920:
                continue
            await (await render(b, 'topic', w, h, lambda base: hub(base, current='tiny-wins'))).close()
            await (await render(b, 'thread', w, h, lambda base: thread(base))).close()
            pg = await render(b, 'thread-example', w, h, lambda base: thread(base, example=True))
            if phone:
                await scroll_to(pg, '.tk-replies', 90)
                await pg.screenshot(path=f'{OUT}/proposed-thread-example-{w}x{h}.png')
            await pg.close()
            async def open_sheet(pg, base):
                await pg.evaluate(ADD, sheet(base))
                await settle(pg)
            await (await render(b, 'composer', w, h, lambda base: hub(base), after=open_sheet)).close()
            await (await render(b, 'hub-prelaunch', w, h, lambda base: hub(base, closed=True))).close()
            await (await render(b, 'empty', w, h, lambda base: hub(base, current='second-opinions'))).close()
            if phone:
                for tag, topics in (('topics5', C['topics5']), ('topics4', C['topics4'])):
                    pg = await render(b, f'{tag}-row', w, h, lambda base, t=topics: hub(base, topics=t))
                    box = await pg.locator('.tk-chips').bounding_box()
                    await pg.screenshot(path=f'{OUT}/proposed-{tag}-crop-{w}.png', clip={'x': 0, 'y': box['y'] - 8, 'width': w, 'height': box['height'] + 16})
                    await pg.close()
            pg, base = await open_page(b, '/', w, h)
            await pg.evaluate(TEASER, [''.join(card(t, base, False) for t in DATA[:3]), bar(base), CSS + TEASER_CSS])
            await settle(pg)
            await scroll_to(pg, 'section:.tk-teaser', 76)
            await pg.screenshot(path=f'{OUT}/proposed-teaser-{w}x{h}.png')
            await pg.close()
        await b.close()


asyncio.run(main())
