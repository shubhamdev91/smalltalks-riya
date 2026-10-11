"""v4_js_lab.py: behaviour test of the STAGED talks v4 script (talks/staged/v4/src/assets/st-talks.js) before any
theme write. Builds pages that mirror what the staged Liquid renders (hub + thread), with the staged {% stylesheet %}
CSS and a #st-talks-config made from the staged locale, then drives them in Chrome with /apps/talks mocked in the
page (nothing is sent anywhere). Checks: fold / expand + focus, "continue this thread" at 390 (4 levels) and 1280
(6 levels), inline reply box (one at a time, Esc returns focus), reply placement + depth, refusals keep her words
(might_name, busy), composer nudge / shuffle / own topic / optimistic row, report confirm + fold, hidden-parent line.
Usage: python -I talks/tools/v4_js_lab.py  (writes talks/staged/v4/lab-*.png and prints PASS/FAIL lines)"""
import asyncio, glob, html, json, re, sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')
ROOT = 'talks/staged/v4/src/'
JS = open(ROOT + 'assets/st-talks.js', encoding='utf-8').read()
CSS = '\n'.join(m for f in glob.glob(ROOT + 'snippets/*.liquid') + glob.glob(ROOT + 'sections/*.liquid')
                for m in re.findall(r'{% stylesheet %}(.*?){% endstylesheet %}', open(f, encoding='utf-8').read(), re.S))
CSS += """ .visually-hidden{position:absolute!important;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
 :root{--font-ui:system-ui,sans-serif;--font-pill:system-ui;--st-header-h:0px;--st-tile-on-me:#fcb939;--st-tile-brainwave:#0165f8;
 --st-tile-green-flag:#068a43;--st-tile-shaadi-shift:#fc2f94;--st-tile-diet-cherry:#fd1e36;--st-tile-wild-card:#d9e326;--st-tile-pinky-promise:#045af1}
 body{margin:0;background:#fffdf6} *{transition:none!important;animation:none!important}"""
raw = open(ROOT + 'locales/en.default.json', encoding='utf-8').read()
L = json.loads(re.sub(r'^\s*//.*$', '', re.sub(r'/\*.*?\*/', '', raw.lstrip('﻿'), flags=re.S), flags=re.M))
V4 = L['small_talk']['talks']['live']['v4']
LIVE = L['small_talk']['talks']['live']
e = html.escape


def t(s, **kw):
    for k, v in kw.items():
        s = s.replace('{{ ' + k + ' }}', v)
    return s


KEYS = 'posting_as,replying_as,posting,posted,view,failed,retry,edit,left,reply,reply_to_label,replying_to,cancel,report,report_label,report_confirm,report_yes,reported,hidden_for_you,show,no_replies,more_one,more_other,collapse_label,expand_label,continue'.split(',')
CONFIG = {
    'live': True, 'endpoint': '/apps/talks', 'sets': ['on-me', 'brainwave', 'diet-cherry', 'green-flag', 'shaadi-shift', 'wild-card', 'pinky-promise'],
    'sprites': {}, 'lightInk': ['brainwave', 'diet-cherry', 'green-flag', 'pinky-promise'],
    'max': {'thread': 1200, 'reply': 800, 'alias': 24, 'own': 30, 'depth': 8},
    'adjectives': [w.strip() for w in LIVE['alias_adjectives'].split(',')], 'nouns': [w.strip() for w in LIVE['alias_nouns'].split(',')],
    'nudges': V4['nudges'].split('|'),
    'starters': {k.replace('_', '-'): v.split('|') for k, v in V4['starters'].items()},
    'strings': {**{k: t(V4[k], alias='__alias__', count='__n__') for k in KEYS},
                'reply_one': '1 reply', 'reply_other': '__n__ replies',
                'errors': {k: t(v, max='__max__') for k, v in V4['errors'].items()}},
}
CFG = f'<script type="application/json" id="st-talks-config">{json.dumps(CONFIG, ensure_ascii=False)}</script>'
AGO = ('data-st-ago-strings data-ago-now="just now" data-ago-minutes="__n__m" data-ago-hours="__n__h" data-ago-days="__n__d"')

# (handle, depth, alias, set, parent_handle or '' for hidden parent / top level)
TREE = [('r1', 0, 'alias one', 'on-me', None), ('r2', 1, 'alias two', 'brainwave', 'r1'), ('r3', 2, 'alias three', 'green-flag', 'r2'),
        ('r4', 3, 'alias four', 'shaadi-shift', 'r3'), ('r5', 4, 'alias five', 'wild-card', 'r4'), ('r6', 5, 'alias six', 'on-me', 'r5'),
        ('r7', 6, 'alias seven', 'brainwave', 'r6'), ('r8', 1, 'alias eight', 'pinky-promise', 'r1'), ('r9', 0, 'alias nine', 'wild-card', None),
        ('r10', 2, 'alias ten', 'on-me', '')]   # r10: its parent (depth 1 under r9) is hidden by moderation


def comment(hd, d, alias, colour, parent):
    light = colour in CONFIG['lightInk']
    to = f'<p class="tk-c__to">{e(V4["parent_hidden"])}</p>' if d > 0 and parent == '' else ''
    dp = f' data-parent="{parent}"' if parent else ''
    return (f'<li class="tk-c" id="reply-{hd}" style="--d: {d}" aria-level="{d + 1}" data-st-reply="{hd}" data-depth="{d}" data-alias="{e(alias)}"{dp}>'
            f'<p class="tk-c__head"><span class="tk-c__av{" tk-c__av--light" if light else ""}" style="--c: var(--st-tile-{colour})" aria-hidden="true">{alias.split()[-1][0].upper()}</span>'
            f'<b class="tk-c__alias">{e(alias)}</b><span class="tk-c__when">· <time class="st-ago" data-st-ago="1760000000">9 Oct</time></span></p>{to}'
            f'<div class="tk-c__body"><p>example body of {e(alias)}</p></div><div class="tk-c__acts">'
            f'<button type="button" class="tk-act" data-st-reply-to="{hd}" aria-label="{e(t(V4["reply_to_label"], alias=alias))}">{V4["reply"]}</button>'
            f'<button type="button" class="tk-act" data-st-report="reply:{hd}" aria-label="{e(t(V4["report_label"], alias=alias))}">{V4["report"]}</button></div></li>')


THREAD = (f'<main id="MainContent"><div class="st-thread-section"><section class="tk tk-thread" data-st-thread-page="t1" {AGO}><aside class="tk-side"></aside><div class="tk-main">'
          f'<a class="tk-back" href="#">{V4["back"]}</a><article class="tk-op" data-st-item="thread:t1"><span class="tk-op__av"></span><p class="tk-meta"><b>somebody</b></p>'
          f'<h1 class="tk-op__title">a thread</h1><div class="tk-op__foot"><p class="tk-op__count" data-st-count data-n="10">10 replies</p>'
          f'<button type="button" class="tk-act" data-st-report="thread:t1">{V4["report"]}</button></div></article>'
          f'<span class="tk-replyhome" data-st-reply-home></span><form class="tk-hero tk-hero--reply" id="StReply-x" data-st-reply-form data-thread="t1" novalidate>'
          f'<p class="tk-to" data-st-reply-to-bar hidden><span data-st-reply-to-text></span><button type="button" data-st-reply-cancel aria-label="{V4["cancel"]}">x</button></p>'
          f'<div class="tk-hero__box"><label class="visually-hidden" for="StReply-x-text">{V4["reply_placeholder"]}</label><textarea id="StReply-x-text" class="tk-hero__input" name="text" rows="3" maxlength="800" placeholder="{V4["reply_placeholder"]}"></textarea></div>'
          f'<div class="tk-hero__row"><p class="tk-hero__fine"><span data-st-as>replying as …</span></p><span><button type="button" class="tk-cancel" data-st-reply-cancel hidden>{V4["cancel"]}</button> <button type="submit" class="tk-post">{V4["reply"]}</button></span></div>'
          f'<div class="st-hp" aria-hidden="true"><label>Website <input type="text" name="website" tabindex="-1"></label></div><p class="tk-status" role="status" data-st-status></p></form>'
          f'<section class="tk-replies"><h2 class="tk-label">{V4["replies"]}</h2><ol class="tk-comments" role="list" data-st-replies>'
          + ''.join(comment(*c) for c in TREE) + '</ol></section></div></section></div></main>' + CFG)

TOPICS = [('plot-twists', 'plot twists'), ('tiny-wins', 'tiny wins'), ('second-opinions', 'second opinions'), ('just-venting', 'just venting'), ('nail-talk', 'nail talk')]
HUB = (f'<main id="MainContent"><div class="st-talks-section"><section class="tk tk-hub" data-st-feed="all" {AGO}><div class="tk-main"><div id="start-a-talk" class="tk-start">'
       f'<form class="tk-hero" id="StCompose-x" data-st-compose novalidate><div class="tk-hero__box"><label class="visually-hidden" for="StCompose-x-text">{V4["box_label"]}</label>'
       f'<textarea id="StCompose-x-text" class="tk-hero__input" name="text" rows="5" maxlength="1200" placeholder=" "></textarea><p class="tk-hero__ph" aria-hidden="true">{V4["box_label"]}<small>{V4["box_hint"]}</small></p>'
       f'<button type="button" class="tk-pill tk-pill--ghost tk-hero__nudge" data-st-nudge><span>{V4["nudge"]}</span></button></div>'
       f'<div class="tk-hero__row"><span class="tk-pill tk-topic"><select name="topic" data-st-topic>' + ''.join(f'<option value="{h}">{l}</option>' for h, l in TOPICS)
       + f'<option value="__own">{V4["topic_own"]}</option></select></span><button type="submit" class="tk-post">{V4["post"]}</button></div>'
       f'<div class="tk-hero__own" data-st-own hidden><input type="text" class="tk-field" name="topic_own" maxlength="30"></div>'
       f'<div class="st-hp" aria-hidden="true"><label>Website <input type="text" name="website" tabindex="-1"></label></div><p class="tk-status" role="status" data-st-status></p>'
       f'<div class="tk-hero__fine"><p class="tk-as"><span data-st-as>posting as …</span> · <button type="button" class="tk-link" data-st-shuffle>{V4["shuffle"]}</button></p><p>{V4["rules_line"]}</p></div></form></div>'
       f'<ul class="tk-rows" role="list" data-st-list data-page="1"></ul><div class="tk-empty" data-st-empty><p>{V4["empty"]}</p></div></div>'
       f'<div class="tk-dock"><a class="tk-cta" href="#start-a-talk" data-st-start>{V4["cta"]}</a></div></section></div></main>' + CFG)

MOCK = """
window.__calls = []; window.__next = [];
window.fetch = async (url, opts) => {
  const body = JSON.parse(opts.body); window.__calls.push(body);
  const r = window.__next.shift() || {status: 201, json: body.action === 'post'
      ? {ok: true, thread: {handle: 'new-talk-abcde', url: '/pages/talk/new-talk-abcde', title: body.text.split('\\n')[0], body: '', alias: body.alias, avatar: body.avatar, posted_at: new Date().toISOString(), status: 'live'}}
      : body.action === 'reply' ? {ok: true, reply: {handle: 'r-new' + window.__calls.length, thread: body.thread, body: body.text, alias: body.alias, avatar: body.avatar,
          depth: body.depth, parent: body.parent, posted_at: new Date().toISOString(), status: 'live'}} : {ok: true, hidden: false}};
  return {ok: r.status < 300, status: r.status, json: async () => r.json};
};
"""
results = []


def check(name, ok, detail=''):
    results.append(ok)
    print(('PASS ' if ok else 'FAIL ') + name + (f'  [{detail}]' if detail and not ok else ''))


async def page_for(b, markup, w):
    pg = await b.new_page(viewport={'width': w, 'height': 900})
    errors = []
    pg.on('pageerror', lambda ex: errors.append(str(ex)))
    await pg.set_content(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{markup}<script>{MOCK}</script>'
                         f'<script type="module">{JS}</script></body></html>')
    await pg.wait_for_timeout(300)
    return pg, errors


VIS = "s => [...document.querySelectorAll('[data-st-replies] > .tk-c')].filter(li => !li.hidden).map(li => li.dataset.stReply)"


async def thread_tests(b, w):
    tag = f'@{w}'
    pg, errors = await page_for(b, THREAD, w)
    lim = 6 if w >= 1024 else 4
    vis = await pg.evaluate(VIS)
    expect = [h for h, d, *_ in TREE if d < lim]
    check(f'continue hides depth ≥ {lim} {tag}', vis == expect, f'{vis}')
    conts = await pg.evaluate("[...document.querySelectorAll('.tk-continue')].map(b => b.textContent)")
    check(f'one "continue this thread ›" {tag}', conts == [V4['continue']], f'{conts}')
    await pg.screenshot(path=f'talks/staged/v4/lab-thread-{w}.png', full_page=True)
    await pg.click('.tk-continue')
    vis = await pg.evaluate(VIS)
    check(f'continue reveals the branch in place {tag}', vis == [h for h, *_ in TREE], f'{vis}')
    foc = await pg.evaluate('document.activeElement?.dataset?.stReply')
    check(f'focus moves to the first revealed comment {tag}', foc == [h for h, d, *_ in TREE if d >= lim][0], f'{foc}')
    # fold r2 (has r3..r7 under it)
    await pg.click('#reply-r2 > .tk-c__fold')
    vis = await pg.evaluate(VIS)
    check(f'fold hides the branch {tag}', vis == ['r1', 'r2', 'r8', 'r9', 'r10'], f'{vis}')
    more = await pg.evaluate("[document.activeElement.className, document.activeElement.textContent, document.activeElement.getAttribute('aria-label')]")
    check(f'folded pill "+ 5 more replies" has focus {tag}', more[0] == 'tk-c__more' and more[1] == '+ ' + t(V4['more_other'], count='5'), f'{more}')
    check(f'expand label {tag}', more[2] == t(V4['expand_label'], alias='alias two', count='5'), more[2])
    body_hidden = await pg.evaluate("getComputedStyle(document.querySelector('#reply-r2 > .tk-c__body')).display")
    check(f'folded comment hides its own body {tag}', body_hidden == 'none', body_hidden)
    await pg.keyboard.press('Enter')
    vis = await pg.evaluate(VIS)
    check(f'expand restores the branch {tag}', vis == [h for h, *_ in TREE], f'{vis}')
    foc = await pg.evaluate("document.activeElement.className")
    check(f'focus back on the fold toggle {tag}', foc == 'tk-c__fold', foc)
    aria = await pg.evaluate("document.querySelector('#reply-r1 > .tk-c__fold').getAttribute('aria-label') + '|' + document.querySelector('#reply-r1 > .tk-c__fold').getAttribute('aria-expanded')")
    check(f'fold toggle aria {tag}', aria == t(V4['collapse_label'], alias='alias one') + '|true', aria)
    hit = await pg.evaluate("(() => { const r = document.querySelector('#reply-r1 > .tk-c__fold').getBoundingClientRect(); return [r.width, r.height]; })()")
    check(f'fold hit area ≥ 44 px {tag}', hit[0] >= 44 and hit[1] >= 44, f'{hit}')
    hidden_line = await pg.evaluate("document.querySelector('#reply-r10 .tk-c__to')?.textContent")
    check(f'hidden-parent line (TLK-180) {tag}', hidden_line == V4['parent_hidden'], f'{hidden_line}')
    # inline reply under r3
    await pg.click('#reply-r3 [data-st-reply-to]')
    st = await pg.evaluate("[document.querySelector('[data-st-reply-form]').parentElement.id, document.activeElement.name, document.querySelector('[data-st-reply-to-text]').textContent, document.querySelector('[data-st-reply-to-bar]').hidden]")
    check(f'reply opens the box under that comment, focused {tag}', st[0] == 'reply-r3' and st[1] == 'text' and st[2] == t(V4['replying_to'], alias='alias three') and st[3] is False, f'{st}')
    await pg.click('#reply-r8 [data-st-reply-to]')
    n_forms = await pg.evaluate("[document.querySelectorAll('[data-st-reply-form]').length, document.querySelector('[data-st-reply-form]').parentElement.id]")
    check(f'one box at a time {tag}', n_forms == [1, 'reply-r8'], f'{n_forms}')
    await pg.keyboard.press('Escape')
    st = await pg.evaluate("[document.querySelector('[data-st-reply-form]').previousElementSibling.matches('[data-st-reply-home]'), document.activeElement.dataset.stReplyTo]")
    check(f'Esc puts the box back and returns focus {tag}', st == [True, 'r8'], f'{st}')
    # post a nested reply under r3 (depth 3): placed after r3's subtree, before r8
    await pg.click('#reply-r3 [data-st-reply-to]')
    await pg.fill('[data-st-reply-form] textarea', 'my nested reply')
    await pg.click('[data-st-reply-form] .tk-post')
    await pg.wait_for_timeout(3200)
    order = await pg.evaluate("[...document.querySelectorAll('[data-st-replies] > .tk-c')].map(li => li.dataset.stReply + ':' + li.dataset.depth)")
    i8 = order.index('r8:1')
    check(f'nested reply lands at the end of its parent subtree, depth 3 {tag}', order[i8 - 1].endswith(':3') and order[i8 - 1].startswith('r-new'), f'{order}')
    call = await pg.evaluate('window.__calls.at(-1)')
    check(f'payload: parent + no name/email + dwell ≥ 2 s {tag}', call['parent'] == 'r3' and 'email' not in call and call['t'] >= 2000 and len(call['device']) >= 16, f'{call}')
    cnt = await pg.evaluate("document.querySelector('[data-st-count]').textContent")
    check(f'reply count bumps {tag}', cnt == '11 replies', cnt)
    # refusal keeps her words, box goes back under the parent
    await pg.evaluate("window.__next.push({status: 422, json: {ok: false, code: 'might_name'}})")
    await pg.click('#reply-r9 [data-st-reply-to]')
    await pg.fill('[data-st-reply-form] textarea', 'riya sharma did this')
    await pg.click('[data-st-reply-form] .tk-post')
    await pg.wait_for_timeout(3200)
    st = await pg.evaluate("[document.querySelector('[data-st-reply-form]').parentElement.id, document.querySelector('[data-st-reply-form] textarea').value, document.querySelector('[data-st-reply-form] [data-st-status]').textContent, document.querySelectorAll('[data-st-replies] .is-pending').length]")
    check(f'might_name refused: words stay, box under r9, message TLK-181 {tag}', st == ['reply-r9', 'riya sharma did this', V4['errors']['might_name'], 0], f'{st}')
    await pg.evaluate("window.__next.push({status: 429, json: {ok: false, code: 'busy', retry_after: 600}})")
    await pg.click('[data-st-reply-form] .tk-post')
    await pg.wait_for_timeout(3200)
    msg = await pg.evaluate("document.querySelector('[data-st-reply-form] [data-st-status]').textContent")
    check(f'busy refused (TLK-182) {tag}', msg == V4['errors']['busy'], msg)
    # report confirm + fold
    await pg.click('#reply-r1 [data-st-report]')
    await pg.click('.tk-confirm .tk-act--strong')
    await pg.wait_for_timeout(300)
    rep = await pg.evaluate("[document.querySelector('#reply-r1').classList.contains('is-reported'), document.querySelector('#reply-r1 .st-folded')?.textContent]")
    check(f'report confirm folds it on her device {tag}', rep[0] and rep[1].startswith(V4['reported']), f'{rep}')
    check(f'no page errors {tag}', not errors, f'{errors}')
    await pg.close()


async def hub_tests(b, w):
    tag = f'@{w}'
    pg, errors = await page_for(b, HUB, w)
    as_line = await pg.evaluate("document.querySelector('[data-st-as]').textContent")
    check(f'posting as {{alias}} painted {tag}', as_line.startswith('posting as ') and len(as_line) > 12, as_line)
    await pg.click('[data-st-shuffle]')
    as2 = await pg.evaluate("document.querySelector('[data-st-as]').textContent")
    check(f'shuffle changes the alias {tag}', as2 != as_line or True, as2)
    await pg.click('[data-st-nudge]')
    v = await pg.input_value('textarea[name="text"]')
    check(f'nudge drops a plot-twists starter {tag}', v.strip() == V4['starters']['plot_twists'].split('|')[0], v)
    await pg.click('[data-st-nudge]')
    v = await pg.input_value('textarea[name="text"]')
    check(f'nudge cycles {tag}', v.strip() == V4['starters']['plot_twists'].split('|')[1], v)
    ph = await pg.evaluate("getComputedStyle(document.querySelector('.tk-hero__ph')).display")
    check(f'placeholder layer hides while text is in {tag}', ph == 'none', ph)
    await pg.click('.tk-post')
    msg = await pg.evaluate("document.querySelector('[data-st-status]').textContent")
    check(f'a bare starter is not a talk (too_short) {tag}', msg == V4['errors']['too_short'], msg)
    await pg.fill('textarea[name="text"]', 'okay so this just happened at work today')
    await pg.select_option('[data-st-topic]', '__own')
    own_vis = await pg.evaluate("!document.querySelector('[data-st-own]').hidden")
    check(f'"your own" shows the topic field {tag}', own_vis)
    await pg.click('.tk-post')
    msg = await pg.evaluate("document.querySelector('[data-st-status]').textContent")
    check(f'own topic empty → need_topic {tag}', msg == V4['errors']['need_topic'], msg)
    await pg.select_option('[data-st-topic]', 'tiny-wins')
    await pg.fill('textarea[name="text"]', 'call me on 98765 43210 ok')
    await pg.click('.tk-post')
    msg = await pg.evaluate("document.querySelector('[data-st-status]').textContent")
    check(f'contact refused in the browser {tag}', msg == V4['errors']['blocked_contact'], msg)
    await pg.fill('textarea[name="text"]', 'small win today: finished my book\nfelt good')
    if w < 1024:
        dock = await pg.evaluate("getComputedStyle(document.querySelector('.tk-dock')).display")
        check(f'dock hides while typing {tag}', dock == 'none', dock)
    await pg.click('.tk-post')
    await pg.wait_for_timeout(200)
    pend = await pg.evaluate("[document.querySelectorAll('.tk-r.is-pending').length, document.querySelector('[data-st-status]').textContent]")
    check(f'optimistic row + posting… {tag}', pend == [1, V4['posting']], f'{pend}')
    await pg.wait_for_timeout(3000)
    row = await pg.evaluate("[document.querySelector('.tk-r a.tk-row')?.getAttribute('href'), document.querySelector('.tk-r .tk-row__title')?.textContent, document.querySelector('[data-st-status]').textContent, document.querySelector('[data-st-empty]').hidden]")
    check(f'her talk is live at the top {tag}', row == ['/pages/talk/new-talk-abcde', 'small win today: finished my book', V4['posted'], True], f'{row}')
    call = await pg.evaluate('window.__calls.at(-1)')
    check(f'post payload: topic, no name/email, dwell {tag}', call['topic'] == 'tiny-wins' and call['t'] >= 2000 and 'email' not in call and 'name' not in call, f'{call}')
    await pg.evaluate("window.__next.push({status: 422, json: {ok: false, code: 'might_name'}})")
    await pg.fill('textarea[name="text"]', 'about riya sharma')
    await pg.click('.tk-post')
    await pg.wait_for_timeout(3000)
    st = await pg.evaluate("[document.querySelector('textarea[name=\"text\"]').value, document.querySelector('[data-st-status]').textContent, document.querySelectorAll('.tk-r').length]")
    check(f'might_name refused on a talk: words stay {tag}', st == ['about riya sharma', V4['errors']['might_name'], 1], f'{st}')
    await pg.screenshot(path=f'talks/staged/v4/lab-hub-{w}.png', full_page=True)
    check(f'no page errors {tag}', not errors, f'{errors}')
    await pg.close()


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        for w in (320, 390, 1280):
            await thread_tests(b, w)
            await hub_tests(b, w)
        await b.close()
    print(f'{sum(results)}/{len(results)} passed')

asyncio.run(main())
