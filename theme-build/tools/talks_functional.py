"""the talks: functional checks on the preview (no form is ever sent: every POST is aborted).
Usage: python -I tools/talks_functional.py [path=/blogs/the-talks] [width=390]"""
import asyncio, json, sys, time
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')
PATH = '/' + (sys.argv[1] if len(sys.argv) > 1 else 'blogs/the-talks').lstrip('/')
W = int(sys.argv[2]) if len(sys.argv) > 2 else 390


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        pg = await b.new_page(viewport={'width': W, 'height': 844})
        posts = []
        async def guard(route):
            if route.request.method == 'POST':
                posts.append(route.request.url); await route.abort()
            else:
                await route.continue_()
        await pg.route('**/*', guard)
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)[:160]))
        sep = '&' if '?' in PATH else '?'
        await pg.goto(f'https://0nev20-vn.myshopify.com{PATH}{sep}preview_theme_id=186651934933&_cb={time.time_ns()}', wait_until='load', timeout=60000)
        await pg.add_style_tag(content='[id^="PBar"], #preview-bar-iframe { display: none !important; }')
        out = {}
        out['cta_href'] = await pg.evaluate("document.querySelector('.st-talks__cta')?.getAttribute('href')")
        out['anchor_exists'] = await pg.evaluate("!!document.getElementById('start-a-talk')")
        out['links'] = await pg.evaluate("[...document.querySelectorAll('a')].filter(a => /talks/.test(a.getAttribute('href') || '')).map(a => a.className.split(' ')[0] + ' ' + a.getAttribute('href'))")
        # Start-a-talk: submit empty -> client errors, no POST
        form = '#start-a-talk form'
        if await pg.locator(form).count():
            await pg.locator(form + ' button[type=submit]').click()
            await pg.wait_for_timeout(400)
            out['start_errors'] = await pg.evaluate(f"[...document.querySelectorAll('{form} .st-field__error')].map(e => e.textContent)")
            out['start_focus'] = await pg.evaluate("document.activeElement?.name")
            out['start_invalid'] = await pg.evaluate(f"[...document.querySelectorAll('{form} [aria-invalid=true]')].map(e => e.name + ' -> ' + e.getAttribute('aria-describedby'))")
            # targets >= 44
            out['small_targets'] = await pg.evaluate("""[...document.querySelectorAll('.st-talks a, .st-talks button, #start-a-talk input, #start-a-talk select, #start-a-talk textarea, #start-a-talk button, .st-trules a, .st-thread a, .st-thread button, .st-thread input, .st-thread textarea')]
              .map(e => { const r = e.getBoundingClientRect(); return [e.className || e.name || e.tagName, Math.round(r.width), Math.round(r.height)]; })
              .filter(([n, w, h]) => h < 44 && !(n + '').includes('st-trules'))""")
        # reply box (thread pages)
        if await pg.locator('.st-reply').count():
            out['more_hidden_before'] = await pg.evaluate("getComputedStyle(document.querySelector('.st-reply__more')).display")
            await pg.locator('.st-reply__input').focus()
            out['more_on_focus'] = await pg.evaluate("getComputedStyle(document.querySelector('.st-reply__more')).display")
            await pg.locator('.st-reply__submit').click(); await pg.wait_for_timeout(400)
            out['reply_errors'] = await pg.evaluate("[...document.querySelectorAll('.st-reply .st-field__error')].map(e => e.textContent)")
            out['reply_btn_name'] = await pg.evaluate("document.querySelector('.st-reply__submit').innerText.trim()")
        out['times'] = await pg.evaluate("[...document.querySelectorAll('time[data-st-ago]')].map(t => t.textContent + ' @' + t.getAttribute('datetime')).slice(0, 4)")
        out['posts_blocked'] = posts
        out['pageerrors'] = errs
        out['scrollW'] = await pg.evaluate('document.documentElement.scrollWidth')
        print(json.dumps(out, ensure_ascii=False, indent=1))
        await b.close()

asyncio.run(main())
