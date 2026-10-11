"""st-fable: compare the outlined V1 SVG against the live-text V1 (browser-shaped Caveat 700) at header and hub sizes."""
import asyncio, base64, pathlib
from playwright.async_api import async_playwright
HERE = pathlib.Path(__file__).resolve().parent
svg = (HERE / 'st-talks-wordmark-v1.svg').read_text(encoding='utf-8')
face = "@font-face{font-family:'WM Caveat';src:url(data:font/ttf;base64,%s) format('truetype');font-weight:400 700;}" % base64.b64encode(pathlib.Path(r'C:/Users/SSTS/Desktop/Riya/spec/fonts/caveat/Caveat[wght].ttf').read_bytes()).decode()
rows = ''
for fs in (19.5, 23.8, 40, 52):
    rows += f"""<div class=r><span class=l>{fs}px</span>
      <span class=wmc style="font-size:{fs}px"><span class=t>the</span><span class=k>talks</span></span>
      <span class=svg style="height:calc({fs}px * 0.8377);color:#0d0b10">{svg}</span>
      <a class=hdr style="font-size:{fs}px"><span class=svg style="height:0.8377em">{svg}</span><span class=arr aria-hidden=true>&#8599;</span></a></div>"""
html = f"""<!doctype html><meta charset=utf-8><style>{face}
body{{margin:0;background:#fdfdfc;font-family:Arial}} .r{{display:flex;gap:36px;align-items:center;padding:10px 16px;border-bottom:1px solid #eee}} .l{{width:60px;font-size:12px;color:#666}}
.wmc{{display:inline-flex;align-items:baseline;white-space:nowrap;line-height:1;color:#0d0b10;font-family:'WM Caveat';font-weight:700;letter-spacing:-0.015em;transform:rotate(-3deg)}} .wmc .t{{margin-right:0.2em}}
.svg{{display:inline-block}} .svg svg{{height:100%;width:auto;display:block}}
.hdr{{display:inline-flex;align-items:center;min-height:44px;color:#0d0b10;outline:1px dashed #ccc}} .arr{{font-family:'DM Sans',Arial;font-weight:500;font-size:0.5em;margin-left:0.22em;transform:translateY(-0.12em)}}
</style>{rows}"""
(HERE / 'v1-check.html').write_text(html, encoding='utf-8')
async def main():
    async with async_playwright() as p:
        br = await p.chromium.launch(channel='chrome'); pg = await br.new_page(viewport={'width': 760, 'height': 400}, device_scale_factor=2)
        await pg.goto((HERE / 'v1-check.html').as_uri()); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(400)
        await pg.screenshot(path=str(HERE / 'v1-check.png'), full_page=True); await br.close()
asyncio.run(main())
