import asyncio, json
from playwright.async_api import async_playwright
U="https://0nev20-vn.myshopify.com/?preview_theme_id=186651934933"
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(channel='chrome')
        c=await b.new_context(viewport={'width':390,'height':844},reduced_motion='reduce')
        pg=await c.new_page(); await pg.goto(U,wait_until='load'); await pg.wait_for_timeout(1200)
        res=[]
        for i in range(30):
            await pg.keyboard.press('Tab')
            res.append(await pg.evaluate("""()=>{const a=document.activeElement;const cs=getComputedStyle(a);const vis=(cs.outlineStyle!=='none'&&parseFloat(cs.outlineWidth)>0)||cs.boxShadow!=='none';return (a.textContent||a.getAttribute('aria-label')||a.tagName).trim().replace(/\s+/g,' ').slice(0,28)+(vis?'':' [NO FOCUS STYLE]')}"""))
        print('tab order:', res)
        await pg.click('.st-header__menu-button'); await pg.wait_for_timeout(300)
        print('reduced motion drawer animation:', await pg.evaluate("getComputedStyle(document.querySelector('.st-drawer')).animationDuration"))
        print('controls disabled until controller:', await pg.evaluate("[...document.querySelectorAll('[data-st-hero-pause],[data-st-hero-tone]')].map(b=>b.getAttribute('aria-disabled'))"))
        print('lcp-ish image:', await pg.evaluate("[...document.querySelectorAll('img[fetchpriority=high]')].map(i=>i.currentSrc.split('/').pop().slice(0,50))"))
        await b.close()
asyncio.run(main())
