"""CURRENT renders of the talks UX, from the build preview (theme 186651934933), for the owner's side-by-side.
Posting is OFF on the build, so the composer, the reply box and nested replies are injected with the exact markup the
Liquid renders when posting is ON (st-talk-composer, st-talk-alias, st-talks-thread, st-talk-reply). Real data only (0 replies). Output: qa/talks-ux/renders/current-<screen>-<w>x<h>.png
Usage (from the repo root): python -I qa/talks-ux/lab/current_capture.py"""
import asyncio, os, time
from playwright.async_api import async_playwright

BASE = 'https://0nev20-vn.myshopify.com'
Q = '?preview_theme_id=186651934933'
OUT = 'qa/talks-ux/renders'
os.makedirs(OUT, exist_ok=True)
SIZES = [(390, 844), (1536, 703)]
# The alias picker's own CSS only loads when the snippet renders (posting ON), so add it for the injected markup.
ALIAS_CSS = open('theme-build/src/snippets/st-talk-alias.liquid', encoding='utf-8').read().split('{% stylesheet %}')[1].split('{% endstylesheet %}')[0]
HIDE = '[id^="PBar"], #preview-bar-iframe { display: none !important; } html, body, .page-wrapper { scroll-behavior: auto !important; } *, *::before, *::after { transition: none !important; animation: none !important; caret-color: transparent !important; }'

ALIAS = """<p class="st-alias"><span data-st-as>{as_text}</span><button type="button" class="st-alias__link">change</button></p>"""
PICKS = ''.join(f'<label class="st-pick"><input type="radio" name="topic" value="{v}"{" checked" if v == "plot-twists" else ""}><span>{l}</span></label>'
                for v, l in (('plot-twists', 'Plot twists'), ('tiny-wins', 'Tiny wins'), ('nail-talk', 'Nail talk'), ('something-else', 'Something else'), ('__own', 'Your own')))
COMPOSER = f"""<form class="st-compose st-compose--row" data-st-compose data-open novalidate>
  <div class="st-compose__head">
    <span class="st-compose__avatar" data-st-me-avatar>__AVATAR__</span>
    <div class="st-compose__field"><textarea class="st-compose__text" rows="1" placeholder="Spill it. Your first line is the headline."></textarea></div>
  </div>
  <div class="st-compose__more">
    {ALIAS.format(as_text='Posting as plotpari')}
    <fieldset class="st-compose__topics"><legend class="st-compose__label">Pick a topic</legend><div class="st-compose__picks">{PICKS}</div></fieldset>
    <div class="st-compose__foot"><p class="st-compose__status"></p><span class="st-compose__left"></span>
      <button type="submit" class="st-compose__post">Post<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 12 L12 4 M5.5 4 H12 V10.5"/></svg></button></div>
    <p class="st-compose__rules">Situations, not people. No names, numbers, handles or links. <a href="#house-rules">House rules</a> · Something here about you? Email <a href="#">riyaagg24@gmail.com</a> with the link and we’ll take it down.</p>
  </div>
</form>"""

REPLY_FORM = f"""<form class="st-reply" data-st-reply-form novalidate>
  <div class="st-reply__grid"><span class="st-reply__avatar" data-st-me-avatar>__AVATAR__</span>
    <div class="st-reply__body"><textarea class="st-reply__input" rows="1" placeholder="Add a reply…"></textarea></div>
    <button type="submit" class="st-reply__submit"><span class="visually-hidden">Post reply</span><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 12 L12 4 M5.5 4 H12 V10.5"/></svg></button></div>
  <div class="st-reply__who">{ALIAS.format(as_text='Replying as plotpari')}</div>
  <p class="st-reply__rule">Situations, not people. No names, numbers, handles or links. <a href="#house-rules">House rules</a></p>
</form>"""

INJECT_COMPOSER = """(html) => {
  const soon = document.querySelector('.st-talks__compose .st-compose--soon'); if (!soon) return 'no slot';
  const av = document.querySelector('.st-trow .st-tavatar'); soon.outerHTML = html.replace('__AVATAR__', av ? av.outerHTML : '');
  return 'ok';
}"""
async def page_for(b, path, w, h):
    pg = await b.new_page(viewport={'width': w, 'height': h})
    await pg.goto(f'{BASE}{path}{Q}&_cb={time.time_ns()}', wait_until='networkidle', timeout=60000)
    await pg.add_style_tag(content=HIDE + ALIAS_CSS)
    await pg.evaluate('document.fonts.ready')
    return pg


async def scroll_into(pg, selector, offset=0):
    await pg.evaluate("""([sel, off]) => { const el = sel.startsWith('closest:') ? document.querySelector(sel.slice(8)).closest('.shopify-section') : document.querySelector(sel); const pw = document.querySelector('.page-wrapper');
      const top = el.getBoundingClientRect().top; if (pw && getComputedStyle(pw).overflowY !== 'visible' && pw.scrollHeight > pw.clientHeight) pw.scrollTop += top - off; else window.scrollBy(0, top - off); }""", [selector, offset])
    await pg.wait_for_timeout(400)


CLOSED_ROW = COMPOSER.replace(' data-open novalidate', ' novalidate')
NONE_LINE = '<p class="st-thread__none" data-st-empty>No replies yet. Go first, any alias works.</p>'
INJECT_THREAD_ZERO = """([form, none]) => {
  const soon = document.querySelector('.st-reply__soon');
  const av = document.querySelector('.st-thread__header .st-tavatar');
  const list = document.querySelector('[data-st-replies]');
  if (list) list.insertAdjacentHTML('afterend', none);
  if (soon) soon.outerHTML = form.replace('__AVATAR__', av ? av.outerHTML : '');
  return 'ok';
}"""


BAND = ('<p style="position:fixed;z-index:50;top:calc(var(--st-header-h,76px) + 6px);left:50%;transform:translateX(-50%);width:min(640px,calc(100% - 24px));'
        'margin:0;padding:8px 12px;border-radius:10px;box-shadow:0 4px 10px -6px rgb(74 59 0 / .5);background:repeating-linear-gradient(-45deg,#fff4c2 0 10px,#ffeaa0 10px 20px);'
        'color:#4a3b00;font:700 13px/1.3 DM Sans,sans-serif;text-align:center">example replies: layout preview, not real posts</p>')
EX_TREE = [(0, 'alias one', 'on-me', False, '2h ago', 'This is an example reply, to show the layout.', ''),
           (1, 'alias two', 'brainwave', True, '1h ago', 'Replies sit under the comment they answer.', 'alias one'),
           (1, 'alias three', 'green-flag', True, '58 min ago', 'You can reply to any comment, even mid-thread.', 'alias two'),
           (1, 'alias four', 'shaadi-shift', False, '40 min ago', 'Each level gets its own thread line.', 'alias three'),
           (1, 'alias five', 'pinky-promise', True, '35 min ago', 'Tap a thread line to fold that branch away.', 'alias one'),
           (0, 'alias six', 'wild-card', False, '20 min ago', 'A folded comment shows how many replies it hides.', '')]


def cur_reply(d, alias, colour, light, when, body, to):
    """today's st-talk-reply markup (depth 0/1); banded example content only"""
    to_html = f'<span class="st-reply-item__to">Replying to {to}</span>' if d and to else ''
    return (f'<li class="st-reply-item{" st-reply-item--nested" if d else ""}" data-depth="{d}">'
            f'<span class="st-reply-item__avatar{" st-reply-item__avatar--light" if light else ""}" style="--st-reply-bg: var(--st-tile-{colour})" aria-hidden="true">{alias.split()[-1][0].upper()}</span>'
            f'<div class="st-reply-item__text"><p class="st-reply-item__meta"><span class="st-reply-item__alias">{alias}</span> · <time class="st-ago">{when}</time>{to_html}</p>'
            f'<div class="st-reply-item__body"><p>{body}</p></div>'
            f'<div class="st-reply-item__acts"><button type="button" class="st-act">Reply</button><button type="button" class="st-act">Report</button></div></div></li>')


INJECT_EXAMPLE = """([band, items, form, replyingTo]) => {
  const list = document.querySelector('[data-st-replies]');
  list.insertAdjacentHTML('beforebegin', band); list.innerHTML = items;
  const count = document.querySelector('[data-st-count]'); if (count) { count.hidden = false; count.textContent = 'example'; }
  const soon = document.querySelector('.st-reply__soon'); const av = document.querySelector('.st-thread__header .st-tavatar');
  if (soon) soon.outerHTML = form.replace('__AVATAR__', av ? av.outerHTML : '');
  if (replyingTo) { const bar = document.querySelector('[data-st-reply-to-bar]'); bar.hidden = false;
    bar.querySelector('[data-st-reply-to-text]').textContent = 'Replying to ' + replyingTo; }
  return 'ok';
}"""
FORM_WITH_BAR = REPLY_FORM.replace('<div class="st-reply__grid">', '<div class="st-reply__to" data-st-reply-to-bar hidden><span data-st-reply-to-text></span><button type="button" class="st-act">Cancel</button></div><div class="st-reply__grid">')


async def main_examples(b):
    items = ''.join(cur_reply(*r) for r in EX_TREE)
    for w, h in SIZES:
        s = f'{w}x{h}'
        for name, to in (('thread', None), ('inline-reply', 'alias three')):
            pg = await page_for(b, '/pages/talk/what-s-your-smallest-friendship-green-flag', w, h)
            print(name, await pg.evaluate(INJECT_EXAMPLE, [BAND, items, FORM_WITH_BAR, to]))
            await pg.wait_for_timeout(300)
            await scroll_into(pg, '.st-reply' if to else '.st-thread__replies', 300 if to else 90)
            await pg.screenshot(path=f'{OUT}/current-{name}-{s}.png')
            await pg.close()


async def main():
    """CURRENT, posting-ON state (like for like with PROPOSED), injected with the exact Liquid markup; prelaunch = as
    installed (posting OFF). REAL data only: 0 replies everywhere (REVIEW-1 A)."""
    async with async_playwright() as b_:
        b = await b_.chromium.launch(channel='chrome')
        for w, h in SIZES + [(1920, 1080)]:
            s = f'{w}x{h}'
            pg = await page_for(b, '/blogs/the-talks', w, h)
            await pg.screenshot(path=f'{OUT}/current-hub-prelaunch-{s}.png')
            print('hub', await pg.evaluate(INJECT_COMPOSER, CLOSED_ROW))
            await pg.wait_for_timeout(300)
            await pg.screenshot(path=f'{OUT}/current-hub-{s}.png')
            await pg.close()
            if w == 1920:
                continue
            pg = await page_for(b, '/blogs/the-talks', w, h)
            await pg.evaluate(INJECT_COMPOSER, COMPOSER)
            await pg.wait_for_timeout(300)
            await scroll_into(pg, '.st-talks__compose', 90 if w < 1024 else 120)
            await pg.screenshot(path=f'{OUT}/current-composer-{s}.png')
            await pg.close()
            pg = await page_for(b, '/pages/talks/tiny-wins', w, h)
            await pg.evaluate(INJECT_COMPOSER, CLOSED_ROW)
            await pg.wait_for_timeout(300)
            await pg.screenshot(path=f'{OUT}/current-topic-{s}.png')
            await pg.close()
            pg = await page_for(b, '/pages/talks/something-else', w, h)
            await pg.evaluate(INJECT_COMPOSER, CLOSED_ROW)
            await pg.wait_for_timeout(300)
            await pg.screenshot(path=f'{OUT}/current-empty-{s}.png')
            await pg.close()
            pg = await page_for(b, '/pages/talk/what-s-your-smallest-friendship-green-flag', w, h)
            print('thread', await pg.evaluate(INJECT_THREAD_ZERO, [REPLY_FORM, NONE_LINE]))
            await pg.wait_for_timeout(300)
            await pg.screenshot(path=f'{OUT}/current-thread-{s}.png')
            await pg.close()
            pg = await page_for(b, '/', w, h)
            if await pg.locator('.st-tt__chips').count():
                await scroll_into(pg, 'closest:.st-tt__chips', 76)
                await pg.wait_for_timeout(600)
                await pg.screenshot(path=f'{OUT}/current-teaser-{s}.png')
            await pg.close()
        await b.close()


async def examples_only():
    async with async_playwright() as p_:
        b = await p_.chromium.launch(channel='chrome')
        await main_examples(b)
        await b.close()

import sys as _sys
asyncio.run(examples_only() if 'examples' in _sys.argv else main())
