"""PROPOSED v3 renders of the talks UX (lab only, no theme write) = v1, APPROVED in st-fable's REVIEW-2, + its fixes:
REAL STATE ONLY (the 9 real threads, 0 replies; the reply design appears in ONE extra frame per size under a visible
band "example replies: layout preview, not real posts"), no DRAFT text (st-copy v1.5.2 placeholders TLK-170/171), and the desktop composer opening inline at the top of the feed. Copy: st-copy v1.5.1.
Each screen loads the real build preview (real header, footer, fonts, nail sheets) and swaps #MainContent (or the
landing teaser's rows) for the proposed markup + qa/talks-ux/lab/proposed.css. Nothing here is theme fixture data.
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
VH = 'position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap'


def av(base, set_key, size=''):
    return (f'<span class="tk-av {size}"><span class="st-tavatar" style="--st-nails: url(\'{base}st-hd-nails-{set_key}.webp\')" '
            f'aria-hidden="true"><span class="st-tavatar__nail"></span></span></span>')


def row(t, base):
    return (f'<li><a class="tk-row" href="#"><span class="tk-row__av">{av(base, t["avatar"])}</span><span>'
            f'<span class="tk-meta"><b>{e(t["alias"])}</b> · 1d</span>'
            f'<h3 class="tk-row__title">{e(t["title"])}</h3><span class="tk-row__ex">{e(t["body"])}</span>'
            f'<span class="tk-foot">{BUBBLE}{e(C["no_replies"])}</span></span></a></li>')


def chips(current, topics):
    items = [('all', C['all'], 9)] + topics
    return '<nav class="tk-chips" aria-label="topics">' + ''.join(
        f'<a class="tk-chip" href="#"{" aria-current=page" if h == current else ""}><span>{e(l)}</span></a>' for h, l, _ in items) + '</nav>'


def side(current, topics):
    items = [('all', C['all'], 9)] + topics
    nav = ''.join(f'<a href="#"{" aria-current=page" if h == current else ""}>{e(l)}<span>{n}</span></a>' for h, l, n in items)
    return f'<aside class="tk-side"><p class="tk-label">topics</p><nav class="tk-nav" aria-label="topics">{nav}</nav></aside>'


def rules_card():
    lis = ''.join(f'<li>{e(x)}</li>' for x in C['rules_card'])
    return (f'<div class="tk-card"><h2>{e(C["rules_card_h"])}</h2><ul class="tk-ruleslist">{lis}</ul>'
            f'<a class="tk-all" href="#">{e(C["rules_all"])}</a></div>')


def cta_card():
    return (f'<div class="tk-card"><button class="tk-cta" type="button">{e(C["cta"])}{ARROW}</button>'
            f'<p class="tk-fine" style="margin-top:10px">{e(C["reassure"])}</p></div>')


def composer(topic='plot-twists', topics=None):
    topics = topics or C['topics5']
    picks = ''.join(f'<span class="tk-chip" role="radio" aria-checked="{"true" if h == topic else "false"}"><span>{e(l)}</span></span>' for h, l, _ in topics) \
        + f'<span class="tk-chip" role="radio" aria-checked="false"><span>{e(C["your_own"])}</span></span>'
    starters = ''.join(f'<span class="tk-starter"><span>{e(s)}</span></span>' for s in C['starters'][topic])
    as_line = C['posting_as'].split(' · ')[0].replace('{alias}', '<b>plotpari</b>')
    return (f'<div class="tk-sheet tk-panel" role="dialog" aria-modal="true" aria-label="{e(C["cta"])}"><span class="tk-grab"></span>'
            f'<div class="tk-sheet__top"><h2 class="tk-sheet__h">{e(C["cta"])}</h2><button class="tk-x" aria-label="close">{X}</button></div>'
            f'<div><p class="tk-label">{e(C["what"])}</p><div class="tk-picks">{picks}</div></div>'
            f'<div><p class="tk-label">{e(C["starters_label"])}</p><div class="tk-starters">{starters}</div></div>'
            f'<div class="tk-fields"><span style="{VH}">{e(C["title_label"])}</span>'
            f'<div class="tk-input tk-input--title">{e(C["title_ph"])}</div>'
            f'<span style="{VH}">{e(C["details_label"])}</span><div class="tk-input tk-input--details">{e(C["details_ph"])}</div></div>'
            f'<div class="tk-as"><span>{as_line}</span><button>{DICE}shuffle</button></div>'
            f'<p class="tk-ruleline">{e(C["rules_short"])}</p>'
            f'<button class="tk-primary">{e(C["post"])}</button><p class="tk-fine">{e(C["reassure"])}</p></div>')


def hub(base, current='all', closed=False, topics=None, feed_composer=False):
    topics = topics or C['topics5']
    rows = DATA if current == 'all' else [t for t in DATA if t['topic'] == current]
    if rows:
        feed = '<ul class="tk-rows">' + ''.join(row(t, base) for t in rows) + '</ul>'
    else:
        line = (C['empty_p_closed'] if closed else C['empty_p']).replace('{topic}', LABEL.get(current, current))
        btn = '' if closed else f'<button class="tk-cta" type="button">{e(C["cta"])}{ARROW}</button>'
        feed = (f'<div class="tk-empty">{av(base, "pinky-promise", "tk-av-56")}<p class="tk-empty__h">{e(C["empty_h"])}</p>'
                f'<p class="tk-empty__p">{e(line)}</p>{btn}</div>')
    dock = (f'<div class="tk-dock tk-dock--closed"><p>{e(C["prelaunch"])}</p></div>' if closed else
            f'<div class="tk-dock"><button class="tk-cta" type="button">{e(C["cta"])}{ARROW}</button></div>')
    rail = (f'<div class="tk-card"><p class="tk-fine" style="text-align:left">{e(C["prelaunch"])}</p></div>' if closed else cta_card()) + rules_card()
    rules = C['rules_row'].split(' · ')
    panel = composer(topics=topics) if feed_composer else ''
    return (f'<div class="tk tk-page">{side(current, topics)}<main class="tk-main">{panel}'
            f'<header><h1 class="tk-wordmark">{e(C["wordmark"])}</h1><p class="tk-promise">{e(C["promise"])}</p></header>'
            f'{chips(current, topics)}<div class="tk-feedhead"><span class="tk-label">{e(C["latest"])}</span><span>{len(rows)} talks</span></div>'
            f'{feed}<details class="tk-rules"><summary>{e(rules[0])} <span>{e(rules[1])} ›</span></summary></details>'
            f'<p class="tk-sign">{e(C["sign"])}</p></main><aside class="tk-rail">{rail}</aside>{dock}</div>')


def reply(alias, colour, light, when, body, nested=False, to=''):
    to_html = f'<span class="tk-reply__to">↪ @{e(to)} </span>' if nested else ''
    return (f'<div class="tk-reply{" tk-reply--nested" if nested else ""}">'
            f'<span class="tk-reply__av{" tk-reply__av--light" if light else ""}" style="--c: var(--st-tile-{colour})" aria-hidden="true">{alias[0].upper()}</span>'
            f'<p class="tk-meta"><b>{e(alias)}</b> · {when}</p><p class="tk-reply__body">{to_html}{e(body)}</p>'
            f'<div class="tk-acts"><button class="tk-act">{e(C["reply"])}</button><button class="tk-act">{e(C["report"])}</button></div></div>')


def thread(base, example=False):
    t = DATA[0]
    if example:  # the ONLY frame with replies: a visible band says they are a layout preview, not real posts
        inner = (f'<p class="tk-example" role="note">{e(C["example_band"])}</p>' + ''.join([
            reply('alias one', 'on-me', False, '2h', 'An example reply, to show the layout.'),
            reply('alias two', 'brainwave', True, '1h', 'A nested reply sits one level in, with a 2 px rule.', nested=True, to='alias one'),
            reply('alias three', 'green-flag', True, '40m', 'Replies to a nested reply stay at this level and name who they answer.'),
        ]))
        count = 'example'
    else:
        inner = f'<p class="tk-noreplies">{e(C["zero_open"])}</p>'
        count = C['no_replies']
    who = C['replying_as'].replace('{alias}', '<b>plotpari</b>')
    field = f'<div class="tk-field"><span>{e(C["reply_field"])}</span><span class="tk-send">{ARROW}</span></div>'
    return (f'<div class="tk tk-page">{side(t["topic"], C["topics5"])}<main class="tk-main">'
            f'<a class="tk-back" href="#">{e(C["back"])}</a>'
            f'<article class="tk-op">{av(base, t["avatar"], "tk-av-48")}<p class="tk-meta"><b>{e(t["alias"])}</b> · 1d · {e(LABEL[t["topic"]])}</p>'
            f'<h1 class="tk-op__title">{e(t["title"])}</h1><p class="tk-op__body">{e(t["body"])}</p>'
            f'<div class="tk-op__foot"><span>{e(count)}</span><button class="tk-act">{e(C["report"])}</button></div></article>'
            f'<section class="tk-replies"><h2 class="tk-label">{e(C["replies_label"])}</h2>{inner}</section>'
            f'<div class="tk-replybox tk-desk-only">{field}<p class="tk-who" style="margin:6px 0 0 18px">{who}</p></div>'
            f'<div class="tk-own"><p>{e(C["own_h"])}</p><a href="#">{e(C["own_link"])}</a></div>'
            f'</main><aside class="tk-rail">{cta_card()}{rules_card()}</aside>'
            f'<div class="tk-dock">{field}<p class="tk-who">{who}</p></div></div>')


EXTRA_CSS = (' .tk-noreplies { margin-top: 8px; padding: 18px 16px; border: 1px dashed var(--tk-line); border-radius: 16px; color: var(--tk-muted); font-size: 16px; text-align: center; }'
             ' .tk-example { margin: 4px 0 6px; padding: 8px 12px; border-radius: 10px; background: repeating-linear-gradient(-45deg, #fff4c2 0 10px, #ffeaa0 10px 20px); color: #4a3b00; font-size: 13px; font-weight: 700; text-align: center; }'
             ' @media (max-width: 1023px) { .tk-desk-only { display: none; } }')
SWAP = """([markup, css]) => {
  const main = document.querySelector('#MainContent');
  main.innerHTML = markup; main.style.display = 'block'; main.style.padding = '0';
  const st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
}"""
SHEET = """(markup) => { const host = document.createElement('div'); host.className = 'tk';
  host.innerHTML = '<div class="tk-scrim"></div>' + markup; document.body.appendChild(host); }"""
TEASER = """([rows, css]) => {
  const st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
  const old = document.querySelector('.st-tt__rows');
  const box = document.createElement('div'); box.className = 'tk tk-teaser'; box.innerHTML = '<ul class="tk-rows">' + rows + '</ul>';
  old.replaceWith(box);
  document.querySelector('.st-tt__pre')?.remove();  /* posting-ON state */
}"""
TEASER_CSS = """.tk-teaser .tk-rows { margin-top: 4px; border-top: 1px solid var(--tk-line); } .tk-teaser li:last-child .tk-row { border-bottom: 0; }
@media (max-width: 1023px) { .tk-teaser li:nth-child(n+3) { display: none; } }
@media (min-width: 1024px) { .tk-teaser li:nth-child(n+4) { display: none; } .tk-teaser .tk-row__ex { display: none; } }"""


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
            if w == 1920:
                continue
            await (await render(b, 'topic', w, h, lambda base: hub(base, current='tiny-wins'))).close()
            await (await render(b, 'thread', w, h, thread)).close()
            pg = await render(b, 'thread-example', w, h, lambda base: thread(base, example=True))
            await scroll_to(pg, '.tk-replies', 90 if phone else 110)
            await pg.screenshot(path=f'{OUT}/proposed-thread-example-{w}x{h}.png')
            await pg.close()
            if phone:
                async def open_sheet(pg, base):
                    await pg.evaluate(SHEET, composer())
                    await settle(pg)
                await (await render(b, 'composer', w, h, lambda base: hub(base), after=open_sheet)).close()
            else:
                await (await render(b, 'composer', w, h, lambda base: hub(base, feed_composer=True))).close()
            await (await render(b, 'hub-prelaunch', w, h, lambda base: hub(base, closed=True))).close()
            await (await render(b, 'empty', w, h, lambda base: hub(base, current='second-opinions'))).close()
            if phone:
                for tag, topics in (('topics5', C['topics5']), ('topics4', C['topics4'])):
                    pg = await render(b, f'{tag}-row', w, h, lambda base, t=topics: hub(base, topics=t))
                    box = await pg.locator('.tk-chips').bounding_box()
                    await pg.screenshot(path=f'{OUT}/proposed-{tag}-crop-{w}.png', clip={'x': 0, 'y': box['y'] - 8, 'width': w, 'height': box['height'] + 16})
                    await pg.close()
            pg, base = await open_page(b, '/', w, h)
            await pg.evaluate(TEASER, [''.join(row(t, base) for t in DATA[:3]), CSS + EXTRA_CSS + TEASER_CSS])
            await settle(pg)
            await scroll_to(pg, 'section:.tk-teaser', 76)
            await pg.screenshot(path=f'{OUT}/proposed-teaser-{w}x{h}.png')
            await pg.close()
        await b.close()

asyncio.run(main())
