"""Probe: the example-conversation blocks as <article>s in a <div> (staged) vs today's <li>s in a <ul>, by rewriting the
live DOM after load (no theme write). Runs axe (list, listitem) and pixel-diffs the examples group at 390 and 1280.
Usage: python -I examples_probe.py [/pages/the-talks]"""
import asyncio, io, json, sys, time
from PIL import Image, ImageChops
from playwright.async_api import async_playwright

PATH = sys.argv[1] if len(sys.argv) > 1 else '/pages/the-talks'
AXE = 'https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.2/axe.min.js'


SWAP = """() => {
    // the staged markup change, applied to the live DOM: examples <ul> -> <div>, cards <li> -> <article>
    const swap = (el, tag) => { const n = document.createElement(tag); for (const a of el.attributes) n.setAttribute(a.name, a.value);
        while (el.firstChild) n.appendChild(el.firstChild); el.replaceWith(n); return n; };
    let groups = 0, cards = 0;
    for (const ul of [...document.querySelectorAll('ul.st-talks__list')].filter(u => u.querySelector('.st-talk'))) {
        const d = swap(ul, 'div'); d.removeAttribute('role'); groups++;
        for (const li of [...d.querySelectorAll('li.st-talk')]) { swap(li, 'article'); cards++; }
    }
    return { groups, cards };
}"""


async def run(b, width, rewrite):
    ctx = await b.new_context(viewport={'width': width, 'height': 900})
    pg = await ctx.new_page()
    await pg.goto(f'https://0nev20-vn.myshopify.com{PATH}?preview_theme_id=186651934933&_cb={time.time_ns()}', wait_until='load', timeout=60000)
    await pg.wait_for_timeout(1500)
    theme = await pg.evaluate("window.Shopify && Shopify.theme ? Shopify.theme.id : null")
    await pg.add_style_tag(content='[id^="PBar"], #preview-bar-iframe { display: none !important; }')
    counts = await pg.evaluate(SWAP) if rewrite else {}
    await pg.add_script_tag(url=AXE)
    axe = await pg.evaluate("""async () => {
        const r = await axe.run(document, { runOnly: { type: 'rule', values: ['list', 'listitem'] } });
        return r.violations.map(v => ({ id: v.id, impact: v.impact, nodes: v.nodes.map(n => n.target.join(' ')) }));
    }""")
    group = pg.locator('.st-talks__list').filter(has=pg.locator('.st-talk')).first
    await group.scroll_into_view_if_needed()
    await pg.wait_for_timeout(300)
    shot = await group.screenshot()
    box = await group.bounding_box()
    tags = await pg.evaluate("[...document.querySelectorAll('.st-talk')].map(e => e.parentElement.className.split(' ')[0] + '>' + e.tagName).join(', ')")
    await ctx.close()
    return {'theme': theme, 'axe': axe, 'counts': counts, 'tags': tags, 'box': [round(v, 1) for v in box.values()]}, shot


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        for w in (390, 1280):
            before, s1 = await run(b, w, False)
            after, s2 = await run(b, w, True)
            a, c = Image.open(io.BytesIO(s1)).convert('RGB'), Image.open(io.BytesIO(s2)).convert('RGB')
            same_size = a.size == c.size
            diff = ImageChops.difference(a, c).getbbox() if same_size else 'size differs'
            if w == 390:
                c.save('qa/talks/examples-article-390.png')
            print(json.dumps({'width': w, 'before': before, 'after': after, 'sizes': [a.size, c.size], 'pixel_diff_bbox': diff}))
        await b.close()

asyncio.run(main())
