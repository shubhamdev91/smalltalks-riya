"""Print the DOM outline (tag.classes [x, y, w, h] "leaf text") of a preview page under a selector, at 390.
Usage: python -I tools/dom_outline.py <path> [selector] [max_depth]"""
import asyncio, sys, time
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')
PATH = '/' + (sys.argv[1].lstrip('/') if len(sys.argv) > 1 else '')
SEL = sys.argv[2] if len(sys.argv) > 2 else 'main'
DEPTH = int(sys.argv[3]) if len(sys.argv) > 3 else 9
JS = r'''([sel, maxd]) => {
  const root = document.querySelector(sel);
  if (!root) return 'no ' + sel;
  const lines = [];
  const walk = (e, d) => {
    if (d > maxd || ['SCRIPT', 'STYLE', 'LINK', 'path', 'TEMPLATE'].includes(e.tagName)) return;
    const r = e.getBoundingClientRect();
    if (r.height < 1 && r.width < 1) return;
    const cls = typeof e.className === 'string' ? e.className.split(/\s+/).filter(Boolean).slice(0, 3).join('.') : '';
    const leaf = e.children.length === 0 ? ' "' + (e.textContent || '').trim().slice(0, 40) + '"' : '';
    lines.push('  '.repeat(d) + e.tagName.toLowerCase() + (cls ? '.' + cls : '') + ' [' + [r.left, r.top + scrollY, r.width, r.height].map(Math.round).join(',') + ']' + leaf);
    for (const c of e.children) walk(c, d + 1);
  };
  walk(root, 0);
  return lines.join('\n');
}'''


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        pg = await b.new_page(viewport={'width': 390, 'height': 844})
        sep = '&' if '?' in PATH else '?'
        await pg.goto(f'https://0nev20-vn.myshopify.com{PATH}{sep}preview_theme_id=186651934933&_cb={int(time.time())}', wait_until='load')
        await pg.wait_for_timeout(1500)
        print(await pg.evaluate(JS, [SEL, DEPTH]))
        await b.close()

if __name__ == "__main__":
    asyncio.run(main())
