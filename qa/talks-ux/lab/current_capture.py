"""CURRENT renders of the talks UX, from the build preview (theme 186651934933), for the owner's side-by-side.
Posting is OFF on the build, so the composer, the reply box and nested replies are injected with the exact markup the
Liquid renders when posting is ON (st-talk-composer, st-talk-alias, st-talks-thread, st-talk-reply). The replies are
SAMPLE content for the review only. Output: qa/talks-ux/renders/current-<screen>-<w>x<h>.png
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
HIDE = '[id^="PBar"], #preview-bar-iframe { display: none !important; } *, *::before, *::after { transition: none !important; animation: none !important; caret-color: transparent !important; }'

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

def reply(alias, colour, light, when, body, nested=False, to=''):
    to_html = f'<span class="st-reply-item__to">Replying to {to}</span>' if nested and to else ''
    return (f'<li class="st-reply-item{" st-reply-item--nested" if nested else ""}" data-depth="{1 if nested else 0}">'
            f'<span class="st-reply-item__avatar{" st-reply-item__avatar--light" if light else ""}" style="--st-reply-bg: var(--st-tile-{colour})" aria-hidden="true">{alias[0].upper()}</span>'
            f'<div class="st-reply-item__text"><p class="st-reply-item__meta"><span class="st-reply-item__alias">{alias}</span> · <time class="st-ago">{when}</time>{to_html}</p>'
            f'<div class="st-reply-item__body"><p>{body}</p></div>'
            f'<div class="st-reply-item__acts"><button type="button" class="st-act">Reply</button><button type="button" class="st-act">Report</button></div></div></li>')

REPLIES = ''.join([
    reply('lowkeymomo', 'on-me', False, '2h ago', 'Mine sends me the voice-note version of every story. Seven minutes, no skips.'),
    reply('sleepyjalebi', 'brainwave', True, '1h ago', 'Voice notes are the love language, honestly.', nested=True, to='lowkeymomo'),
    reply('goldenchai', 'green-flag', True, '40 min ago', 'She remembers my chai order better than I do.'),
])
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
INJECT_THREAD = """([replies, form]) => {
  const list = document.querySelector('[data-st-replies]'); if (!list) return 'no list';
  list.innerHTML = replies;
  const count = document.querySelector('[data-st-count]'); if (count) { count.hidden = false; count.textContent = '3 replies'; }
  const soon = document.querySelector('.st-reply__soon');
  const av = document.querySelector('.st-thread__header .st-tavatar');
  if (soon) soon.outerHTML = form.replace('__AVATAR__', av ? av.outerHTML : '');
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


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        for w, h in SIZES:
            s = f'{w}x{h}'
            pg = await page_for(b, '/blogs/the-talks', w, h)
            await pg.screenshot(path=f'{OUT}/current-hub-{s}.png')
            print('composer', await pg.evaluate(INJECT_COMPOSER, COMPOSER))
            await pg.wait_for_timeout(300)
            await scroll_into(pg, '.st-talks__compose', 90 if w < 1024 else 120)
            await pg.screenshot(path=f'{OUT}/current-composer-{s}.png')
            await pg.close()

            pg = await page_for(b, '/pages/talk/what-s-your-smallest-friendship-green-flag', w, h)
            print('thread', await pg.evaluate(INJECT_THREAD, [REPLIES, REPLY_FORM]))
            await pg.wait_for_timeout(300)
            await pg.screenshot(path=f'{OUT}/current-thread-{s}.png')
            if w < 1024:
                await scroll_into(pg, '.st-thread__replies', 80)
                await pg.screenshot(path=f'{OUT}/current-thread-replies-{s}.png')
            await pg.close()

            pg = await page_for(b, '/', w, h)
            sel = '.st-tt__chips'
            if await pg.locator(sel).count():
                await scroll_into(pg, 'closest:.st-tt__chips', 76)
                await pg.wait_for_timeout(600)
                await pg.screenshot(path=f'{OUT}/current-teaser-{s}.png')
            else:
                print('teaser not found at', s)
            await pg.close()
        await b.close()

asyncio.run(main())
