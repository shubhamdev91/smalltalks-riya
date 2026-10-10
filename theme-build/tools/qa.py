"""QA runner: python tools/qa.py <name> <path> [widths=390,1280] [--full] [--js "expr"]
Saves qa/foundation/<name>-<w>.png and prints overflow + console errors."""
import sys, json, asyncio
from playwright.async_api import async_playwright
BASE="https://0nev20-vn.myshopify.com"
OUT="C:/Users/SSTS/Desktop/Riya/qa/foundation/"
args=sys.argv[1:]
name, path = args[0], args[1]
widths=[390,1280]; full='--full' in args; js=None; el=None; css=None; reduce='--reduce' in args
for i,a in enumerate(args):
    if a.startswith('widths='): widths=[int(x) for x in a[7:].split(',')]
    if a=='--js': js=args[i+1]
    if a=='--el': el=args[i+1]
    if a=='--css': css=open(args[i+1],encoding='utf-8').read()
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(channel='chrome', headless=True)
        for w in widths:
            ctx=await b.new_context(viewport={'width':w,'height':844 if w<700 else 900}, device_scale_factor=1 if w>700 else 2, is_mobile=w<700, has_touch=w<700, reduced_motion='reduce' if reduce else 'no-preference')
            pg=await ctx.new_page(); errs=[]
            pg.on('console', lambda m: errs.append(m.text) if m.type=='error' else None)
            pg.on('pageerror', lambda e: errs.append('PAGEERROR '+str(e)))
            sep='&' if '?' in path else '?'
            await pg.goto(BASE+path+sep+'preview_theme_id=186651934933', wait_until='load', timeout=60000)
            await pg.add_style_tag(content='#PBarNextFrameWrapper,#preview-bar-iframe{display:none!important}')
            if css: await pg.add_style_tag(content=css)
            await pg.wait_for_timeout(1500)
            if full:
                await pg.add_style_tag(content='html:has(.page-wrapper),html:has(.page-wrapper) body,.page-wrapper{height:auto!important;overflow:visible!important}')
                await pg.evaluate('async()=>{for(let y=0;y<document.body.scrollHeight;y+=400){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,120))}window.scrollTo(0,0)}')
                await pg.wait_for_timeout(1200)
            ov=await pg.evaluate(r"""()=>{const W=document.documentElement.clientWidth;const bad=[];for(const el of document.querySelectorAll('body *')){const r=el.getBoundingClientRect();if(r.width&&r.right>W+1&&getComputedStyle(el).position!=='fixed'&&!(el.parentElement&&el.parentElement.closest('.st-hero,.st-chapter,.st-gallery__media,.st-teaser__tile,.st-teaser__avatar,.st-sprite,[data-st-clip]'))){bad.push((el.tagName+'.'+[...el.classList].join('.')).slice(0,80)+' r='+Math.round(r.right))}}return {sw:document.documentElement.scrollWidth,cw:W,bad:bad.slice(0,8),liquid:(document.body.innerText.match(/Liquid error.{0,120}/g)||[]).slice(0,5)}}""")
            print(f'[{w}] scrollW={ov["sw"]} clientW={ov["cw"]} overflow={ov["bad"]} liquid={ov["liquid"]}')
            if js:
                print(f'[{w}] js:', json.dumps(await pg.evaluate(js), ensure_ascii=False)[:3000])
            if el:
                await pg.locator(el).first.screenshot(path=f'{OUT}{name}-{w}.png')
            else:
                await pg.screenshot(path=f'{OUT}{name}-{w}.png', full_page=full)
            if errs: print(f'[{w}] console errors:', errs[:6])
            await ctx.close()
        await b.close()
asyncio.run(main())
