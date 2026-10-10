"""the talks (live): functional + visual checks on preview theme 186651934933.

Usage (from C:/Users/SSTS/Desktop/Riya):
  python -I talks/qa_live.py mock 390     # backend stubbed in the browser (UI states; nothing is sent to Shopify)
  python -I talks/qa_live.py real 390     # real backend through the App Proxy (after the owner setup); posts are
                                          # marked "[qa]" and listed in talks/qa-created.json for deletion
Screenshots go to qa/talks/. Prints a JSON report.
"""
import asyncio
import json
import re
import sys
import time
from pathlib import Path

from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')
MODE = sys.argv[1] if len(sys.argv) > 1 else 'mock'
W = int(sys.argv[2]) if len(sys.argv) > 2 else 390
BASE = 'https://0nev20-vn.myshopify.com'
PREVIEW = 'preview_theme_id=186651934933'
SHOTS = Path('qa/talks')
SHOTS.mkdir(parents=True, exist_ok=True)
CREATED = Path('talks/qa-created.json')
SEED = 'what-s-your-smallest-friendship-green-flag'


def url(path):
    sep = '&' if '?' in path else '?'
    return f'{BASE}{path}{sep}{PREVIEW}&_cb={time.time_ns()}'


class Mock:
    """Answers POST /apps/talks like the backend would, one scripted reply per request."""

    def __init__(self):
        self.queue = []
        self.seen = []

    def push(self, status, body, delay=0.6, network_error=False):
        self.queue.append((status, body, delay, network_error))

    async def handle(self, route):
        req = route.request
        if req.method != 'POST':
            return await route.continue_()
        payload = json.loads(req.post_data or '{}')
        self.seen.append(payload)
        status, body, delay, network_error = self.queue.pop(0) if self.queue else (500, {'ok': False, 'code': 'server'}, 0.3, False)
        await asyncio.sleep(delay)
        if network_error:
            return await route.abort('failed')
        if callable(body):
            body = body(payload)
        await route.fulfill(status=status, content_type='application/json', body=json.dumps(body))


def thread_ok(status='live'):
    def make(p):
        handle = 'qa-mock-' + str(int(time.time() * 1000))[-6:]
        title = p['text'].split('\n')[0][:110]
        return {'ok': True, 'thread': {'handle': handle, 'url': f'/pages/talk/{handle}', 'title': title, 'body': '',
                                       'alias': p['alias'], 'avatar': p['avatar'], 'topic': p['topic'] or 'something-else',
                                       'topic_label': p.get('topic_own') or p['topic'], 'posted_at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                                       'status': status}}
    return make


def reply_ok(status='live'):
    def make(p):
        handle = 'r-qamock' + str(int(time.time() * 1000))[-6:]
        return {'ok': True, 'reply': {'handle': handle, 'thread': p['thread'], 'body': p['text'], 'alias': p['alias'],
                                      'avatar': p['avatar'], 'depth': 1 if p.get('parent') else 0, 'parent': p.get('parent'),
                                      'reply_to': p.get('reply_to'), 'posted_at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                                      'status': status}}
    return make


async def shot(pg, name, full=False):
    await pg.add_style_tag(content='[id^="PBar"], #preview-bar-iframe { display: none !important; }')
    path = SHOTS / f'{name}-{W}.png'
    await pg.screenshot(path=str(path), full_page=full)
    return str(path)


async def status_text(pg, form_sel):
    return (await pg.locator(f'{form_sel} [data-st-status]').first.inner_text()).strip()


async def main():
    out = {'mode': MODE, 'width': W, 'checks': {}, 'shots': [], 'errors': []}
    c = out['checks']
    mock = Mock()
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel='chrome')
        ctx = await browser.new_context(viewport={'width': W, 'height': 900 if W < 700 else 1000})
        pg = await ctx.new_page()
        pg.on('pageerror', lambda e: out['errors'].append(str(e)[:200]))
        pg.on('console', lambda m: out['errors'].append('console: ' + m.text[:200]) if m.type == 'error' else None)
        posts = []
        if MODE == 'mock':
            await pg.route(re.compile(r'.*/apps/talks.*'), mock.handle)
        else:
            pg.on('request', lambda r: posts.append(r) if r.method == 'POST' and '/apps/talks' in r.url else None)

        # ---------- Hub ----------
        await pg.goto(url('/blogs/the-talks'), wait_until='load', timeout=60000)
        c['hub_rows'] = await pg.locator('[data-st-list] > li').count()
        c['hub_first_title'] = (await pg.locator('[data-st-list] .st-trow__title').first.inner_text()).strip()
        c['hub_chips'] = await pg.eval_on_selector_all('.st-talks__chips a', 'as => as.map(a => [a.textContent.trim(), a.getAttribute("href"), a.getAttribute("aria-current")])')
        c['hub_row_href'] = await pg.locator('[data-st-list] .st-trow__link').first.get_attribute('href')
        c['hub_scrollW'] = await pg.evaluate('document.documentElement.scrollWidth')
        c['posting_as'] = (await pg.locator('[data-st-compose] [data-st-as]').first.inner_text()).strip()
        c['me_avatar_sprite'] = await pg.evaluate("getComputedStyle(document.querySelector('[data-st-compose] [data-st-me-avatar] .st-tavatar')).getPropertyValue('--st-nails').slice(0, 60)")
        out['shots'].append(await shot(pg, 'hub'))
        ta = '[data-st-compose] textarea'
        await pg.locator(ta).click()
        c['composer_open'] = await pg.evaluate("document.querySelector('[data-st-compose]').hasAttribute('data-open')")
        out['shots'].append(await shot(pg, 'composer-open'))

        # need a topic
        await pg.locator(ta).fill('Testing the talks, please ignore [qa]')
        await pg.locator('[data-st-compose] .st-compose__post').click()
        await pg.wait_for_timeout(200)
        c['need_topic_msg'] = await status_text(pg, '[data-st-compose]')
        # client-side block: phone number
        await pg.locator('[data-st-compose] .st-pick').first.click()
        await pg.locator(ta).fill('call me on 98765 43210 [qa]')
        await pg.locator('[data-st-compose] .st-compose__post').click()
        await pg.wait_for_timeout(200)
        c['blocked_contact_msg'] = await status_text(pg, '[data-st-compose]')
        out['shots'].append(await shot(pg, 'blocked-contact'))

        if MODE == 'mock':
            # success: optimistic row first, then the confirmed link
            mock.push(201, thread_ok(), delay=1.2)
            await pg.locator(ta).fill('Rehearsed a text for an hour and sent hey [qa]\nPlot twist: they replied in a second.')
            t0 = time.time()
            await pg.locator('[data-st-compose] .st-compose__post').click()
            await pg.wait_for_selector('[data-st-list] > li.is-pending', timeout=1500)
            c['optimistic_ms'] = int((time.time() - t0) * 1000)
            c['pending_state'] = (await pg.locator('[data-st-list] > li.is-pending .st-trow__state').inner_text()).strip()
            out['shots'].append(await shot(pg, 'posting'))
            await pg.wait_for_selector('[data-st-list] > li.is-mine a.st-trow__link', timeout=8000)
            c['posted_href'] = await pg.locator('[data-st-list] > li.is-mine a.st-trow__link').first.get_attribute('href')
            c['posted_status'] = await status_text(pg, '[data-st-compose]')
            c['payload_keys'] = sorted(mock.seen[-1].keys())
            c['payload_t_ms'] = mock.seen[-1]['t']
            c['payload_has_email_or_name'] = any(k in mock.seen[-1] for k in ('email', 'name'))
            out['shots'].append(await shot(pg, 'posted'))
            # held
            mock.push(201, thread_ok('held'))
            await pg.locator(ta).fill('Priya from my floor copied my set again [qa]')
            await pg.locator('[data-st-compose] .st-compose__post').click()
            await pg.wait_for_selector('[data-st-list] > li.is-held', timeout=8000)
            c['held_tag'] = (await pg.locator('[data-st-list] > li.is-held .st-trow__state').first.inner_text()).strip()
            c['held_status'] = await status_text(pg, '[data-st-compose]')
            out['shots'].append(await shot(pg, 'held'))
            # network failure -> retry
            mock.push(0, {}, network_error=True)
            await pg.locator(ta).fill('This one fails first time [qa]')
            await pg.locator('[data-st-compose] .st-compose__post').click()
            await pg.wait_for_selector('[data-st-list] > li.is-failed', timeout=8000)
            c['failed_text'] = (await pg.locator('[data-st-list] > li.is-failed .st-trow__fail').inner_text()).strip()
            out['shots'].append(await shot(pg, 'failed'))
            mock.push(201, thread_ok())
            await pg.locator('[data-st-list] > li.is-failed .st-trow__fail button').first.click()
            await pg.wait_for_selector('[data-st-list] > li.is-mine:not(.is-failed):not(.is-pending) a.st-trow__link >> nth=0', timeout=8000)
            c['retry_ok'] = await pg.locator('[data-st-list] > li.is-failed').count() == 0
            # rate limited -> row removed, text back
            mock.push(429, {'ok': False, 'code': 'rate_limited', 'retry_after': 300})
            await pg.locator(ta).fill('Too many talks today [qa]')
            await pg.locator('[data-st-compose] .st-compose__post').click()
            await pg.wait_for_function("document.querySelector('[data-st-compose] [data-st-status]').dataset.tone === 'error'", timeout=8000)
            c['rate_limited_msg'] = await status_text(pg, '[data-st-compose]')
            c['rate_limited_text_back'] = await pg.locator(ta).input_value()
            out['shots'].append(await shot(pg, 'rate-limited'))
            # server-side block
            mock.push(422, {'ok': False, 'code': 'blocked_words'})
            await pg.locator(ta).fill('a server-side blocked word [qa]')
            await pg.locator('[data-st-compose] .st-compose__post').click()
            await pg.wait_for_function("document.querySelector('[data-st-compose] [data-st-status]').textContent.includes('word')", timeout=8000)
            c['blocked_words_msg'] = await status_text(pg, '[data-st-compose]')
            # alias change
            await pg.locator('[data-st-compose] [data-st-alias-toggle]').click()
            await pg.locator('[data-st-compose] [data-st-alias-input]').fill('small talk')
            await pg.locator('[data-st-compose] [data-st-alias-save]').click()
            c['alias_reserved_hint'] = (await pg.locator('[data-st-compose] [data-st-alias-hint]').inner_text()).strip()
            await pg.locator('[data-st-compose] [data-st-alias-input]').fill('chaiqueen')
            await pg.locator('[data-st-compose] [data-st-alias-save]').click()
            c['alias_after'] = (await pg.locator('[data-st-compose] [data-st-as]').inner_text()).strip()
        else:
            await pg.locator(ta).fill(f'qa run {time.strftime("%H:%M")}: does the talks board post straight away? [qa]')
            await pg.locator('[data-st-compose] .st-compose__post').click()
            await pg.wait_for_selector('[data-st-list] > li.is-mine:not(.is-pending)', timeout=20000)
            c['real_row'] = await pg.locator('[data-st-list] > li.is-mine').first.evaluate('li => ({cls: li.className, href: li.querySelector("a")?.getAttribute("href"), state: li.querySelector(".st-trow__state")?.textContent})')
            c['real_status'] = await status_text(pg, '[data-st-compose]')
            out['shots'].append(await shot(pg, 'real-posted'))

        # ---------- Topic page ----------
        await pg.goto(url('/pages/talks/tiny-wins'), wait_until='load', timeout=60000)
        c['topic_rows'] = await pg.locator('[data-st-list] > li:not(.is-mine)').count()
        c['topic_current'] = await pg.eval_on_selector_all('.st-talks__chips a[aria-current]', 'as => as.map(a => a.textContent.trim())')
        c['topic_preselected'] = await pg.evaluate("document.querySelector('[data-st-compose] input[name=topic]:checked')?.value")
        c['topic_scrollW'] = await pg.evaluate('document.documentElement.scrollWidth')
        out['shots'].append(await shot(pg, 'topic-tiny-wins'))

        # ---------- Thread page ----------
        await pg.goto(url(f'/pages/talk/{SEED}'), wait_until='load', timeout=60000)
        c['thread_title'] = (await pg.locator('.st-thread__title').inner_text()).strip()
        c['thread_meta'] = (await pg.locator('.st-thread__meta').inner_text()).strip()
        c['thread_report_on_brand'] = await pg.locator('.st-thread__header [data-st-report]').count()
        c['thread_has_email_field'] = await pg.locator('.st-reply input[type=email]').count()
        c['replying_as'] = (await pg.locator('[data-st-reply-form] [data-st-as]').inner_text()).strip()
        c['thread_scrollW'] = await pg.evaluate('document.documentElement.scrollWidth')
        out['shots'].append(await shot(pg, 'thread'))
        rta = '[data-st-reply-form] textarea'
        if MODE == 'mock':
            mock.push(201, reply_ok(), delay=1.0)
            await pg.locator(rta).fill('Mine sends me reels at 2am and checks if I slept [qa]')
            await pg.locator('[data-st-reply-form] .st-reply__submit').click()
            await pg.wait_for_selector('[data-st-replies] > li.is-pending', timeout=1500)
            out['shots'].append(await shot(pg, 'reply-posting'))
            await pg.wait_for_selector('[data-st-replies] > li.is-mine [data-st-reply-to]', timeout=8000)
            c['reply_count_text'] = (await pg.locator('[data-st-count]').inner_text()).strip()
            # nested reply
            await pg.locator('[data-st-replies] > li.is-mine [data-st-reply-to]').first.click()
            c['replying_to_bar'] = (await pg.locator('[data-st-reply-to-bar]').inner_text()).strip()
            mock.push(201, reply_ok())
            await pg.locator(rta).fill('Same! Green flag energy [qa]')
            await pg.locator('[data-st-reply-form] .st-reply__submit').click()
            await pg.wait_for_selector('[data-st-replies] > li.st-reply-item--nested.is-mine:not(.is-pending)', timeout=8000)
            c['nested_order'] = await pg.eval_on_selector_all('[data-st-replies] > li', 'lis => lis.map(li => li.dataset.depth)')
            c['nested_payload_parent'] = bool(mock.seen[-1].get('parent'))
            out['shots'].append(await shot(pg, 'reply-nested'))
            # report a reply
            mock.push(200, {'ok': True, 'hidden': False})
            await pg.locator('[data-st-replies] > li.is-mine').first.evaluate('li => li.querySelector(".st-reply-item__acts").append(Object.assign(document.createElement("button"), {type: "button", className: "st-act", textContent: "Report"}))')
            await pg.locator('[data-st-replies] > li.is-mine .st-act:has-text("Report")').first.evaluate('b => b.setAttribute("data-st-report", "reply:" + b.closest("li").dataset.stReply)')
            await pg.locator('[data-st-replies] > li.is-mine [data-st-report]').first.click()
            c['report_confirm'] = (await pg.locator('.st-confirm').first.inner_text()).strip()
            out['shots'].append(await shot(pg, 'report-confirm'))
            await pg.locator('.st-confirm .st-act--strong').first.click()
            await pg.wait_for_selector('[data-st-replies] > li.is-reported', timeout=8000)
            c['reported_note'] = (await pg.locator('[data-st-replies] > li.is-reported .st-folded').inner_text()).strip()
            c['report_payload'] = mock.seen[-1]
            out['shots'].append(await shot(pg, 'reported'))
            # client-side block in a reply
            await pg.locator(rta).fill('dm me @spilltea [qa]')
            await pg.locator('[data-st-reply-form] .st-reply__submit').click()
            await pg.wait_for_timeout(200)
            c['reply_blocked_handle'] = await status_text(pg, '[data-st-reply-form]')
        else:
            await pg.locator(rta).fill(f'qa reply {time.strftime("%H:%M")} [qa]')
            await pg.locator('[data-st-reply-form] .st-reply__submit').click()
            await pg.wait_for_selector('[data-st-replies] > li.is-mine:not(.is-pending)', timeout=20000)
            c['real_reply'] = await pg.locator('[data-st-replies] > li.is-mine').first.evaluate('li => ({cls: li.className, handle: li.dataset.stReply})')
            out['shots'].append(await shot(pg, 'real-reply'))

        # ---------- Old article URL forwards ----------
        await pg.goto(url(f'/blogs/the-talks/{SEED}'), wait_until='load', timeout=60000)
        await pg.wait_for_url(re.compile(r'/pages/talk/'), timeout=10000)
        c['article_forwards_to'] = pg.url.split('?')[0].replace(BASE, '')

        c['posts_sent'] = len(mock.seen) if MODE == 'mock' else len(posts)
        await browser.close()
    print(json.dumps(out, ensure_ascii=False, indent=1))


asyncio.run(main())
