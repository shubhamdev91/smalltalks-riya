"""v4_e2e.py: REAL end-to-end test of the installed talks v4 on the build preview (theme 186651934933) against the live
backend (/apps/talks -> b27475e7fe2b). Run ONLY while talk_settings/main posting_open = "true" (st-talks' E2E window).
Device A (one browser context = one device id):
  - posts at 390 (hub, tiny wins), 320 (the new, empty "second opinions" topic page) and 1280 (hub, "your own" topic);
  - is refused for a phone number and a link (in the browser), "might name someone" (server, TLK-181) and the 4th post
    in 10 minutes (server, TLK-128 slow-down), with her words kept every time;
  - replies on talk 1 at 390, 1280 and 320: a top-level reply, then nested replies 3 deep;
  - shoots the inline reply box at 390/1536/1920.
Devices B, C, D each report reply 3: it is auto-hidden at 3, and reply 4 then says "replying to a hidden comment"
(TLK-180).
Every created handle is printed (CREATED ...) for the cleanup. Shots: qa/talks/v4-e2e/.
Usage: python -I talks/tools/v4_e2e.py"""
import asyncio, json, os, re, sys, time
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')
BASE, Q = 'https://0nev20-vn.myshopify.com', 'preview_theme_id=186651934933'
OUT = 'qa/talks/v4-e2e'
os.makedirs(OUT, exist_ok=True)
raw = open('talks/staged/v4/src/locales/en.default.json', encoding='utf-8').read()
L = json.loads(re.sub(r'^\s*//.*$', '', re.sub(r'/\*.*?\*/', '', raw.lstrip('﻿'), flags=re.S), flags=re.M))
V4 = L['small_talk']['talks']['live']['v4']
E = V4['errors']
HIDE = ('[id^="PBar"], #preview-bar-iframe { display: none !important; } html, body { scroll-behavior: auto !important; } '
        '*, *::before, *::after { transition: none !important; animation: none !important; caret-color: transparent !important; }')
results, created = [], {'threads': [], 'replies': []}


def check(name, ok, detail=''):
    results.append(bool(ok))
    print(('PASS ' if ok else 'FAIL ') + name + ('' if ok else f'  [{detail}]'), flush=True)


def url(path):
    return f'{BASE}{path}{"&" if "?" in path else "?"}{Q}&_cb={time.time_ns()}'


async def goto(pg, path, tries=6):
    for i in range(tries):
        res = await pg.goto(url(path), wait_until='networkidle', timeout=60000)
        if res.status == 200:
            await pg.add_style_tag(content=HIDE)
            return True
        await asyncio.sleep(5)
    return False


async def status_of(pg, form_sel):
    return (await pg.evaluate(f"document.querySelector('{form_sel} [data-st-status]')?.textContent ?? ''")).strip()


async def wait_status(pg, form_sel, done, timeout=20):
    for _ in range(timeout * 4):
        s = await status_of(pg, form_sel)
        if s and s != V4['posting'] and (done is None or s in done or any(s.startswith(d) for d in done)):
            return s
        await asyncio.sleep(0.25)
    return await status_of(pg, form_sel)


async def post_talk(pg, text, topic=None, own=None):
    if topic:
        await pg.select_option('[data-st-topic]', topic)
    if own:
        await pg.select_option('[data-st-topic]', '__own')
        await pg.fill('input[name="topic_own"]', own)
    await pg.click('[data-st-compose] textarea')
    await pg.fill('[data-st-compose] textarea', text)
    calls = []
    pg.on('request', lambda r: calls.append(r.url) if '/apps/talks' in r.url and r.method == 'POST' else None)
    await pg.click('[data-st-compose] .tk-post')
    s = await wait_status(pg, '[data-st-compose]', None)
    return s, calls


async def reply(pg, parent, text):
    before = set(await pg.evaluate("[...document.querySelectorAll('[data-st-replies] > .tk-c')].map(li => li.dataset.stReply).filter(Boolean)"))
    if parent:
        await pg.click(f'#reply-{parent} > .tk-c__acts [data-st-reply-to]')
    await pg.fill('[data-st-reply-form] textarea', text)
    await pg.click('[data-st-reply-form] .tk-post')
    s = await wait_status(pg, '[data-st-reply-form]', None)
    after = await pg.evaluate("[...document.querySelectorAll('[data-st-replies] > .tk-c')].map(li => [li.dataset.stReply, li.dataset.depth])")
    new = [h for h, d in after if h and h not in before]
    return s, (new[0] if new else None), after


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        A = await b.new_context(viewport={'width': 390, 'height': 844})
        pg = await A.new_page()
        errors = []
        pg.on('pageerror', lambda e: errors.append(str(e)))

        # --- talk 1 at 390, hub, tiny wins
        assert await goto(pg, '/blogs/the-talks')
        s, calls = await post_talk(pg, 'e2e check one, will be deleted. small win: finished a book', topic='tiny-wins')
        href = await pg.evaluate("document.querySelector('.tk-rows > .tk-r.is-mine a.tk-row')?.getAttribute('href')")
        check('talk 1 posted at 390 (live at the top)', s == V4['posted'] and href and href.startswith('/pages/talk/'), f'{s} {href}')
        t1 = href.rsplit('/', 1)[1] if href else None
        created['threads'].append(t1)
        print('CREATED thread', t1, flush=True)
        await pg.screenshot(path=f'{OUT}/talk1-posted-390.png')

        # --- talk 2 at 320, the new empty topic page (row styles must load there)
        await pg.set_viewport_size({'width': 320, 'height': 700})
        assert await goto(pg, '/pages/talks/second-opinions')
        pre = await pg.evaluate("document.querySelector('[data-st-topic]').value")
        check('empty topic page preselects its topic', pre == 'second-opinions', pre)
        s, _ = await post_talk(pg, 'e2e check two, will be deleted. need a second opinion on a jacket')
        info = await pg.evaluate("""() => { const r = document.querySelector('.tk-rows > .tk-r.is-mine'); const a = r?.querySelector('a.tk-row');
          return [a?.getAttribute('href'), a ? getComputedStyle(a).display : null, document.querySelector('[data-st-empty]')?.hidden]; }""")
        check('talk 2 posted at 320 on an empty topic, row styled', s == V4['posted'] and info[0] and info[1] == 'grid' and info[2], f'{s} {info}')
        t2 = info[0].rsplit('/', 1)[1] if info[0] else None
        created['threads'].append(t2)
        print('CREATED thread', t2, flush=True)
        await pg.screenshot(path=f'{OUT}/talk2-empty-topic-320.png')

        # --- talk 3 at 1280, hub, her own topic
        await pg.set_viewport_size({'width': 1280, 'height': 900})
        assert await goto(pg, '/blogs/the-talks')
        s, _ = await post_talk(pg, 'e2e check three, will be deleted. a thought about mornings', own='e2e')
        href3 = await pg.evaluate("document.querySelector('.tk-rows > .tk-r.is-mine a.tk-row')?.getAttribute('href')")
        check('talk 3 posted at 1280 with "your own" topic', s == V4['posted'] and href3, f'{s} {href3}')
        t3 = href3.rsplit('/', 1)[1] if href3 else None
        created['threads'].append(t3)
        print('CREATED thread', t3, flush=True)

        # --- refusals (her words stay in the box)
        assert await goto(pg, '/blogs/the-talks')
        s, calls = await post_talk(pg, 'e2e check, call me on 98765 43210', topic='plot-twists')
        kept = await pg.input_value('[data-st-compose] textarea')
        check('phone number refused in the browser (nothing sent)', s == E['blocked_contact'] and not calls and '98765' in kept, f'{s} {calls}')
        s, calls = await post_talk(pg, 'e2e check, see www.example.com for more')
        check('link refused in the browser (nothing sent)', s == E['blocked_link'] and not calls, f'{s} {calls}')
        s, calls = await post_talk(pg, 'e2e check about riya sharma from work, will be deleted')
        kept = await pg.input_value('[data-st-compose] textarea')
        check('might name someone: refused by the server (TLK-181), words kept', s == E['might_name'] and calls and 'riya sharma' in kept, f'{s} {calls}')
        s, calls = await post_talk(pg, 'e2e check four, will be deleted, one too many')
        kept = await pg.input_value('[data-st-compose] textarea')
        check('4th talk in 10 min: slow down (TLK-128), words kept', s == E['rate_limited'] and 'one too many' in kept, f'{s}')
        await pg.screenshot(path=f'{OUT}/refusal-slowdown-1280.png')
        await pg.fill('[data-st-compose] textarea', '')
        await pg.evaluate("localStorage.removeItem('st-talks-draft')")

        # --- replies on talk 1: top-level (390), nested (390), nested (1280), nested (320)
        await pg.set_viewport_size({'width': 390, 'height': 844})
        assert await goto(pg, f'/pages/talk/{t1}'), 'talk 1 page not reachable'
        s, r1, _ = await reply(pg, None, 'e2e reply one, will be deleted')
        check('top-level reply at 390', s == V4['posted'] and r1, f'{s} {r1}')
        s, r2, _ = await reply(pg, r1, 'e2e reply two, nested, will be deleted')
        check('nested reply at 390', s == V4['posted'] and r2, f'{s} {r2}')
        await pg.set_viewport_size({'width': 1280, 'height': 900})
        await asyncio.sleep(2)
        assert await goto(pg, f'/pages/talk/{t1}')
        s, r3, _ = await reply(pg, r2, 'e2e reply three, two deep, will be deleted')
        check('nested reply at 1280', s == V4['posted'] and r3, f'{s} {r3}')
        await pg.set_viewport_size({'width': 320, 'height': 700})
        assert await goto(pg, f'/pages/talk/{t1}')
        s, r4, _ = await reply(pg, r3, 'e2e reply four, three deep, will be deleted')
        check('nested reply at 320', s == V4['posted'] and r4, f'{s} {r4}')
        for r in (r1, r2, r3, r4):
            if r:
                created['replies'].append(r)
                print('CREATED reply', r, flush=True)
        # server-rendered order, depth and parent after a reload
        await asyncio.sleep(3)
        await pg.set_viewport_size({'width': 390, 'height': 844})
        assert await goto(pg, f'/pages/talk/{t1}')
        tree = await pg.evaluate("[...document.querySelectorAll('[data-st-replies] > .tk-c:not(.is-mine)')].map(li => [li.dataset.stReply, li.dataset.depth, li.dataset.parent || ''])")
        check('server order + depth + parent: r1(0) r2(1,r1) r3(2,r2) r4(3,r3)',
              tree == [[r1, '0', ''], [r2, '1', r1], [r3, '2', r2], [r4, '3', r3]], f'{tree}')
        cnt = await pg.evaluate("document.querySelector('[data-st-count]')?.textContent")
        check('reply count on the talk = 4', cnt == '4 replies', cnt)
        await pg.screenshot(path=f'{OUT}/thread-nested-390.png', full_page=True)
        # inline reply box shots (no submit)
        for w, h in ((390, 844), (1536, 864), (1920, 1080)):
            await pg.set_viewport_size({'width': w, 'height': h})
            assert await goto(pg, f'/pages/talk/{t1}')
            await pg.click(f'#reply-{r2} > .tk-c__acts [data-st-reply-to]')
            await pg.wait_for_timeout(300)
            await pg.evaluate(f"document.querySelector('#reply-{r1}').scrollIntoView({{block: 'start'}}); window.scrollBy(0, -100)")
            await pg.wait_for_timeout(300)
            await pg.screenshot(path=f'{OUT}/inline-reply-{w}.png')
            await pg.keyboard.press('Escape')
        check('no page errors (device A)', not errors, f'{errors}')

        # --- reports: devices B, C, D report reply 3 -> auto-hidden at 3; reply 4 says its parent is hidden
        for n, dev in enumerate('BCD', 1):
            ctx = await b.new_context(viewport={'width': 390, 'height': 844})
            q = await ctx.new_page()
            assert await goto(q, f'/pages/talk/{t1}')
            await q.click(f'#reply-{r3} > .tk-c__acts [data-st-report]')
            await q.click('.tk-confirm .tk-act--strong')
            await q.wait_for_timeout(2500)
            folded = await q.evaluate(f"[document.querySelector('#reply-{r3}').classList.contains('is-reported'), document.querySelector('#reply-{r3} .st-folded')?.textContent]")
            check(f'device {dev}: report confirm folds it on her device', folded[0] and folded[1].startswith(V4['reported']), f'{folded}')
            if n == 1:
                await q.screenshot(path=f'{OUT}/reported-390.png')
            await ctx.close()
        await asyncio.sleep(4)
        assert await goto(pg, f'/pages/talk/{t1}')
        tree = await pg.evaluate("[...document.querySelectorAll('[data-st-replies] > .tk-c')].map(li => [li.dataset.stReply, li.querySelector('.tk-c__to')?.textContent || ''])")
        hidden_ok = r3 not in [h for h, _ in tree] and [r4, V4['parent_hidden']] in tree
        check('3 reports auto-hide reply 3; reply 4 says "replying to a hidden comment"', hidden_ok, f'{tree}')
        cnt = await pg.evaluate("document.querySelector('[data-st-count]')?.textContent")
        check('reply count recounted = 3', cnt == '3 replies', cnt)
        await pg.screenshot(path=f'{OUT}/hidden-parent-390.png', full_page=True)
        await A.close()
        await b.close()
    print('CREATED-JSON ' + json.dumps(created))
    print(f'{sum(results)}/{len(results)} passed')

asyncio.run(main())
