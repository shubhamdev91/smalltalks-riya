"""python tools/qa_pages.py name=path ... [widths=390,1280]  -> full-page shots + checks"""
import sys, json, asyncio
from playwright.async_api import async_playwright
BASE="https://0nev20-vn.myshopify.com"; OUT="C:/Users/SSTS/Desktop/Riya/qa/foundation/"
pairs=[a.split('=',1) for a in sys.argv[1:] if '=' in a and not a.startswith('widths=')]
widths=[390,1280]
for a in sys.argv[1:]:
    if a.startswith('widths='): widths=[int(x) for x in a[7:].split(',')]
CHECK=r"""()=>{const W=document.documentElement.clientWidth;const bad=[];for(const el of document.querySelectorAll('body *')){const r=el.getBoundingClientRect();if(r.width&&r.right>W+1&&getComputedStyle(el).position!=='fixed'&&!(el.parentElement&&el.parentElement.closest('.st-hero,.st-chapter,.st-gallery__media,.st-teaser__tile,.st-teaser__avatar,.st-sprite,.st-beats__track,slideshow-component,[data-st-clip]'))){bad.push((el.tagName+'.'+[...el.classList].join('.')).slice(0,70)+' r='+Math.round(r.right))}}
const h1=[...document.querySelectorAll('h1')].map(h=>h.textContent.trim().slice(0,50));
return {sw:document.documentElement.scrollWidth,cw:W,bad:bad.slice(0,6),h1,tpl:document.querySelector('main')?.dataset.template,title:document.title.slice(0,70),liquid:(document.body.innerText.match(/(Liquid error|translation missing).{0,90}/g)||[]).slice(0,4)}}"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(channel='chrome')
        for name,path in pairs:
            for w in widths:
                ctx=await b.new_context(viewport={'width':w,'height':844 if w<700 else 900},device_scale_factor=1,is_mobile=w<700,has_touch=w<700)
                pg=await ctx.new_page(); errs=[]
                pg.on('console', lambda m: errs.append(m.text[:120]) if m.type=='error' and 'shop.app' not in m.text and 'Failed to load resource' not in m.text else None)
                pg.on('pageerror', lambda e: errs.append('PAGEERROR '+str(e)[:150]))
                sep='&' if '?' in path else '?'
                r=await pg.goto(BASE+path+sep+'preview_theme_id=186651934933',wait_until='load',timeout=60000)
                await pg.add_style_tag(content='#PBarNextFrameWrapper{display:none!important} html:has(.page-wrapper),html:has(.page-wrapper) body,.page-wrapper{height:auto!important;overflow:visible!important}')
                await pg.wait_for_timeout(1200)
                await pg.evaluate('async()=>{for(let y=0;y<document.body.scrollHeight;y+=350){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,200))}window.scrollTo(0,0)}')
                await pg.wait_for_timeout(2000)
                info=await pg.evaluate(CHECK)
                print(f'{name}[{w}] {r.status} tpl={info["tpl"]} h1={info["h1"]} sw={info["sw"]}/{info["cw"]} bad={info["bad"]} liquid={info["liquid"]} errs={errs[:3]}')
                await pg.screenshot(path=f'{OUT}{name}-{w}.png',full_page=True)
                await ctx.close()
        await b.close()
asyncio.run(main())
