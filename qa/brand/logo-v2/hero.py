"""st-fable: hero render of current + A/B/C (for iteration) and zoom crops of the edited letters."""
import asyncio, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from playwright.async_api import async_playwright
import make_logo as M
HERE = pathlib.Path(__file__).resolve().parent
ZOOM = {'A': (1120, 0, 1336, 460), 'B': (840, 540, 1240, 818), 'C': (840, 440, 1240, 818)}


async def main():
    cells = ''.join(f'<div class=c><div class=l>{k}</div>{M.svg(M.VARS.get(k), "#001df9")}</div>' for k in ['current', 'A', 'B', 'C'])
    zooms = ''.join(f'<div class=z><div class=l>{k} zoom</div><svg viewBox="{x0} {y0} {x1 - x0} {y1 - y0}" style="height:420px">'
                    f'{M.svg(M.VARS[k], "#001df9")[M.svg(M.VARS[k], "#001df9").index(">") + 1:-6]}</svg></div>' for k, (x0, y0, x1, y1) in ZOOM.items())
    html = f"""<!doctype html><style>body{{margin:0;background:#fdf6e9;font-family:Arial}} .c{{display:inline-block;padding:16px;width:560px}} .c svg{{width:540px;height:auto;display:block}}
      .l{{font-size:14px;color:#666;margin-bottom:6px}} .z{{display:inline-block;padding:16px}}</style>{cells}<div>{zooms}</div>"""
    (HERE / 'hero.html').write_text(html, encoding='utf-8')
    async with async_playwright() as p:
        br = await p.chromium.launch(channel='chrome'); pg = await br.new_page(viewport={'width': 2400, 'height': 900})
        await pg.goto((HERE / 'hero.html').as_uri()); await pg.wait_for_timeout(300)
        await pg.screenshot(path=str(HERE / 'hero-iter.png'), full_page=True); await br.close()


asyncio.run(main())
