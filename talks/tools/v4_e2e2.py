"""v4_e2e2.py: the orchestrator's E2E items not covered by v4_e2e.py, REAL on the build preview against /apps/talks.
Run ONLY while posting_open = "true".
- Device A:
  - posts in the new empty topic "just venting" at 390;
  - is refused for the same talk twice (duplicate), an @handle (browser), a slur (server, blocked_words);
  - a filled honeypot and a too-fast submit get a silent fake success: nothing is saved (checked afterwards via Admin).
- Devices A + B: a reply chain 5 deep (depth 0..4) on that talk.
  - 390: depth 4 waits behind "continue this thread ›" and opens in place; the fold "−" collapses a branch to
    "+ n more replies" and expands it again.
  - 1280: all 5 levels show (limit 6).
- Shots: the nested thread and the inline box under a mid-thread comment at 390 + 1536 -> qa/talks/v4-e2e/.
Prints CREATED handles for the cleanup.  Usage: python -I talks/tools/v4_e2e2.py"""
import asyncio, json, os, re, sys, time
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')
BASE, Q = 'https://0nev20-vn.myshopify.com', 'preview_theme_id=186651934933'
OUT = 'qa/talks/v4-e2e'
raw = open('talks/staged/v4/src/locales/en.default.json', encoding='utf-8').read()
L = json.loads(re.sub(r'^\s*//.*$', '', re.sub(r'/\*.*?\*/', '', raw.lstrip('﻿'), flags=re.S), flags=re.M))
V4 = L['small_talk']['talks']['live']['v4']
E = V4['errors']
HIDE = ('[id^="PBar"], #preview-bar-iframe { display: none !important; } html, body { scroll-behavior: auto !important; } '
        '*, *::before, *::after { transition: none !important; animation: none !important; caret-color: transparent !important; }')
results = []


def check(name, ok, detail=''):
    results.append(bool(ok))
    print(('PASS ' if ok else 'FAIL ') + name + ('' if ok else f'  [{detail}]'), flush=True)


async def goto(pg, path, tries=8):
    for _ in range(tries):
        res = await pg.goto(f'{BASE}{path}?{Q}&_cb={time.time_ns()}', wait_until='networkidle', timeout=60000)
        if res.status == 200:
            await pg.add_style_tag(content=HIDE)
            return True
        await asyncio.sleep(5)
    return False


async def wait_status(pg, form):
    for _ in range(80):
        s = (await pg.evaluate(f"document.querySelector('{form} [data-st-status]')?.textContent ?? ''")).strip()
        if s and s != V4['posting']:
            return s
        await asyncio.sleep(0.25)
    return s


async def post(pg, text, sent):
    await pg.click('[data-st-compose] textarea')
    await pg.fill('[data-st-compose] textarea', text)
    n = len(sent)
    await pg.click('[data-st-compose] .tk-post')
    s = await wait_status(pg, '[data-st-compose]')
    return s, len(sent) > n


async def reply(pg, parent, text):
    before = set(await pg.evaluate("[...document.querySelectorAll('[data-st-replies] > .tk-c')].map(li => li.dataset.stReply).filter(Boolean)"))
    if parent:
        await pg.click(f'#reply-{parent} > .tk-c__acts [data-st-reply-to]')
    await pg.fill('[data-st-reply-form] textarea', text)
    await pg.click('[data-st-reply-form] .tk-post')
    s = await wait_status(pg, '[data-st-reply-form]')
    after = await pg.evaluate("[...document.querySelectorAll('[data-st-replies] > .tk-c')].map(li => li.dataset.stReply).filter(Boolean)")
    new = [h for h in after if h not in before]
    return s, (new[0] if new else None)


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        A = await b.new_context(viewport={'width': 390, 'height': 844})
        pg = await A.new_page()
        sent = []
        pg.on('request', lambda r: sent.append(r.post_data) if '/apps/talks' in r.url and r.method == 'POST' else None)
        errors = []
        pg.on('pageerror', lambda e: errors.append(str(e)))

        assert await goto(pg, '/pages/talks/just-venting')
        pre = await pg.evaluate("document.querySelector('[data-st-topic]').value")
        s, _ = await post(pg, 'e2e check five, will be deleted. today i felt like a nap', sent)
        href = await pg.evaluate("document.querySelector('.tk-rows > .tk-r.is-mine a.tk-row')?.getAttribute('href')")
        check('talk in "just venting" (empty topic) at 390', pre == 'just-venting' and s == V4['posted'] and href, f'{pre} {s} {href}')
        t5 = href.rsplit('/', 1)[1]
        print('CREATED thread', t5, flush=True)
        await pg.screenshot(path=f'{OUT}/talk5-just-venting-390.png')

        s, went = await post(pg, 'e2e check five, will be deleted. today i felt like a nap', sent)
        kept = await pg.input_value('[data-st-compose] textarea')
        check('the same talk twice: duplicate refused (TLK-129), words kept', s == E['duplicate'] and went and 'nap' in kept, f'{s}')
        s, went = await post(pg, 'e2e check, find me @someone_here', sent)
        check('@handle refused in the browser (nothing sent)', s == E['blocked_handle'] and not went, f'{s} {went}')
        s, went = await post(pg, 'e2e check, what a gandu move, will be deleted', sent)
        kept = await pg.input_value('[data-st-compose] textarea')
        check('slur refused by the server (TLK-126), words kept', s == E['blocked_words'] and went and 'gandu' in kept, f'{s}')
        # honeypot: a bot fills the hidden field -> silent fake success, nothing saved (checked via Admin afterwards)
        await pg.evaluate("document.querySelector('[data-st-compose] input[name=website]').value = 'http://bot.example'")
        s, went = await post(pg, 'e2e honeypot check, must not be saved', sent)
        check('honeypot: silent "posted", no link (fake success)', s == V4['posted'] and went, f'{s}')
        await pg.evaluate("document.querySelector('[data-st-compose] input[name=website]').value = ''")
        # min-time: a submit faster than 2 s (straight to the endpoint, as a bot would) -> silent fake success
        dev = await pg.evaluate("JSON.parse(localStorage.getItem('st-talks-me')).device")
        r = await pg.evaluate("""async (dev) => { const res = await fetch('/apps/talks', {method: 'POST', headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({action: 'post', text: 'e2e too-fast check, must not be saved', topic: 'just-venting', alias: 'fastbot', device: dev, t: 400})});
            return [res.status, await res.json()]; }""", dev)
        check('too fast (t = 400 ms): silent fake success, empty handle', r[0] == 201 and r[1].get('ok') and r[1]['thread']['handle'] == '', f'{r}')

        # reply chain 5 deep: A writes depth 0..3, B writes depth 4 (the per-device burst guard is 4 a minute)
        assert await goto(pg, f'/pages/talk/{t5}')
        chain, parent = [], None
        for d in range(4):
            s, h = await reply(pg, parent, f'e2e chain depth {d}, will be deleted')
            check(f'reply at depth {d}', s == V4['posted'] and h, f'{s} {h}')
            chain.append(h)
            parent = h
        B = await b.new_context(viewport={'width': 390, 'height': 844})
        q = await B.new_page()
        assert await goto(q, f'/pages/talk/{t5}')
        for _ in range(10):
            if await q.evaluate(f"!!document.querySelector('#reply-{parent}')"):
                break
            await asyncio.sleep(3)
            await goto(q, f'/pages/talk/{t5}')
        s, h = await reply(q, parent, 'e2e chain depth 4, will be deleted')
        check('reply at depth 4 (second device)', s == V4['posted'] and h, f'{s} {h}')
        chain.append(h)
        for c in chain:
            print('CREATED reply', c, flush=True)
        await B.close()

        # server-rendered tree at 390: depth 4 behind "continue this thread", then fold / expand
        for _ in range(10):
            await asyncio.sleep(3)
            assert await goto(pg, f'/pages/talk/{t5}')
            got = await pg.evaluate("[...document.querySelectorAll('[data-st-replies] > .tk-c:not(.is-mine)')].map(li => li.dataset.stReply)")
            if len(got) == 5:
                break
        tree = await pg.evaluate("[...document.querySelectorAll('[data-st-replies] > .tk-c')].map(li => [li.dataset.stReply, li.dataset.depth, li.hidden])")
        check('server order/depth 0..4', [t[:2] for t in tree] == [[c, str(i)] for i, c in enumerate(chain)], f'{tree}')
        cont = await pg.evaluate("[...document.querySelectorAll('.tk-continue')].map(b => b.textContent)")
        check('390: depth 4 hidden behind "continue this thread ›"', tree[-1][2] is True and cont == [V4['continue']], f'{tree[-1]} {cont}')
        await pg.screenshot(path=f'{OUT}/thread-deep-390.png', full_page=True)
        await pg.click('.tk-continue')
        vis = await pg.evaluate(f"!document.querySelector('#reply-{chain[4]}').hidden")
        check('"continue" opens it in place', vis)
        await pg.click(f'#reply-{chain[1]} > .tk-c__fold')
        st = await pg.evaluate(f"""[[...document.querySelectorAll('[data-st-replies] > .tk-c')].filter(li => !li.hidden).length,
            document.querySelector('#reply-{chain[1]} .tk-c__more')?.textContent, document.activeElement.className]""")
        check('fold collapses the branch to "+ 3 more replies" (focus on it)', st[0] == 2 and st[1] == '+ ' + V4['more_other'].replace('{{ count }}', '3') and st[2] == 'tk-c__more', f'{st}')
        await pg.screenshot(path=f'{OUT}/thread-folded-390.png')
        await pg.keyboard.press('Enter')
        n = await pg.evaluate("[...document.querySelectorAll('[data-st-replies] > .tk-c')].filter(li => !li.hidden).length")
        check('expand restores the branch', n == 5, n)
        # inline box under a mid-thread comment + nested thread shots at 390 and 1536
        for w, hgt in ((390, 844), (1536, 864)):
            await pg.set_viewport_size({'width': w, 'height': hgt})
            assert await goto(pg, f'/pages/talk/{t5}')
            if w >= 1024:
                cont = await pg.evaluate("document.querySelectorAll('.tk-continue').length")
                allv = await pg.evaluate("[...document.querySelectorAll('[data-st-replies] > .tk-c')].every(li => !li.hidden)")
                check('1536: all 5 levels show, no "continue" (limit 6)', cont == 0 and allv, f'{cont} {allv}')
            await pg.screenshot(path=f'{OUT}/thread-nested-{w}.png', full_page=True)
            await pg.click(f'#reply-{chain[2]} > .tk-c__acts [data-st-reply-to]')
            await pg.wait_for_timeout(300)
            await pg.evaluate(f"document.querySelector('#reply-{chain[1]}').scrollIntoView({{block: 'start'}}); window.scrollBy(0, -100)")
            await pg.wait_for_timeout(300)
            await pg.screenshot(path=f'{OUT}/inline-reply-midthread-{w}.png')
            await pg.keyboard.press('Escape')
        check('no page errors', not errors, f'{errors}')
        await A.close()
        await b.close()
    print(f'{sum(results)}/{len(results)} passed')

asyncio.run(main())
