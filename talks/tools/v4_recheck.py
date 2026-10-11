"""v4_recheck.py: the minimal live re-check of backend b00440d7cd4a on the build preview (posting_open must be "true").
One device:
- a normal talk, then the same talk again straight away: refused as a duplicate (it was saved twice on b27475e7fe2b);
- two more talks, then a 4th inside 10 minutes: refused (slow down);
- one reply, then the same reply again straight away: refused as a duplicate.
Prints CREATED handles for the cleanup.  Usage: python -I talks/tools/v4_recheck.py"""
import asyncio, json, re, sys, time
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')
BASE, Q = 'https://0nev20-vn.myshopify.com', 'preview_theme_id=186651934933'
raw = open('talks/staged/v4/src/locales/en.default.json', encoding='utf-8').read()
L = json.loads(re.sub(r'^\s*//.*$', '', re.sub(r'/\*.*?\*/', '', raw.lstrip('﻿'), flags=re.S), flags=re.M))
V4 = L['small_talk']['talks']['live']['v4']
E = V4['errors']
results = []


def check(name, ok, detail=''):
    results.append(bool(ok))
    print(('PASS ' if ok else 'FAIL ') + name + ('' if ok else f'  [{detail}]'), flush=True)


async def goto(pg, path):
    for _ in range(8):
        r = await pg.goto(f'{BASE}{path}?{Q}&_cb={time.time_ns()}', wait_until='networkidle', timeout=60000)
        if r.status == 200:
            return
        await asyncio.sleep(5)
    raise RuntimeError(path)


async def status(pg, form):
    for _ in range(80):
        s = (await pg.evaluate(f"document.querySelector('{form} [data-st-status]')?.textContent ?? ''")).strip()
        if s and s != V4['posting']:
            return s
        await asyncio.sleep(0.25)
    return s


async def post(pg, text):
    await pg.click('[data-st-compose] textarea')
    await pg.fill('[data-st-compose] textarea', text)
    t0 = time.time()
    await pg.click('[data-st-compose] .tk-post')
    return await status(pg, '[data-st-compose]'), time.time() - t0


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        pg = await (await b.new_context(viewport={'width': 390, 'height': 844})).new_page()
        await goto(pg, '/pages/talks/tiny-wins')
        s, _ = await post(pg, 'e2e recheck one, will be deleted')
        href = await pg.evaluate("document.querySelector('.tk-rows > .tk-r.is-mine a.tk-row')?.getAttribute('href')")
        check('normal talk posted', s == V4['posted'] and href, f'{s} {href}')
        t1 = href.rsplit('/', 1)[1]
        print('CREATED thread', t1, flush=True)
        done_at = time.time()
        s, _ = await post(pg, 'e2e recheck one, will be deleted')
        gap = time.time() - done_at
        check(f'same talk again {gap:.1f} s later: refused as a duplicate', s == E['duplicate'], s)
        for n in ('two', 'three'):
            s, _ = await post(pg, f'e2e recheck {n}, will be deleted')
            check(f'talk {n} posted', s == V4['posted'], s)
        s, _ = await post(pg, 'e2e recheck four, will be deleted')
        check('4th talk inside 10 minutes: slow down', s == E['rate_limited'], s)
        await pg.fill('[data-st-compose] textarea', '')
        await pg.evaluate("localStorage.removeItem('st-talks-draft')")
        await goto(pg, f'/pages/talk/{t1}')
        await pg.fill('[data-st-reply-form] textarea', 'e2e recheck reply, will be deleted')
        await pg.click('[data-st-reply-form] .tk-post')
        s = await status(pg, '[data-st-reply-form]')
        h = await pg.evaluate("[...document.querySelectorAll('[data-st-replies] > .tk-c')].map(li => li.dataset.stReply).filter(Boolean)")
        check('reply posted', s == V4['posted'] and h, f'{s} {h}')
        await pg.evaluate("document.querySelector('[data-st-reply-form] [data-st-status]').textContent = ''")
        await pg.fill('[data-st-reply-form] textarea', 'e2e recheck reply, will be deleted')
        await pg.click('[data-st-reply-form] .tk-post')
        s = await status(pg, '[data-st-reply-form]')
        check('same reply again straight away: refused as a duplicate', s == E['duplicate'], s)
        await b.close()
    print(f'{sum(results)}/{len(results)} passed')

asyncio.run(main())
