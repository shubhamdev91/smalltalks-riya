import asyncio
from playwright.async_api import async_playwright
U="https://0nev20-vn.myshopify.com/?preview_theme_id=186651934933"
OUT="C:/Users/SSTS/Desktop/Riya/qa/foundation/"
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(channel='chrome')
        for w,h in [(320,700),(390,844),(430,932),(1280,900)]:
            c=await b.new_context(viewport={'width':w,'height':h},device_scale_factor=2 if w<700 else 1,is_mobile=w<700,has_touch=w<700)
            pg=await c.new_page(); await pg.goto(U,wait_until='load'); await pg.wait_for_timeout(1500)
            await pg.screenshot(path=f'{OUT}02-header-{w}.png',clip={'x':0,'y':0,'width':w,'height':120})
            info=await pg.evaluate("""()=>{const q=s=>document.querySelector(s);const r=e=>e&&e.getBoundingClientRect();
              return {menuBtn:!!(q('.st-header__menu-button')&&r(q('.st-header__menu-button')).width),nav:r(q('.st-header__nav'))?.width,talks:q('.st-header__talks')&&getComputedStyle(q('.st-header__talks')).fontFamily,logo:getComputedStyle(q('.st-logo')).color,sw:document.documentElement.scrollWidth}}""")
            print(w,info)
            if w<990:
                await pg.click('.st-header__menu-button'); await pg.wait_for_timeout(500)
                op=await pg.evaluate("document.querySelector('.st-drawer').open")
                await pg.screenshot(path=f'{OUT}02-drawer-{w}.png')
                seq=[]
                for i in range(10):
                    await pg.keyboard.press('Tab')
                    seq.append(await pg.evaluate("(()=>{const a=document.activeElement;return (a.closest('dialog')?'IN:':'OUT:')+(a.textContent||a.tagName).trim().slice(0,14)})()"))
                await pg.keyboard.press('Escape'); await pg.wait_for_timeout(500)
                after=await pg.evaluate("[document.querySelector('.st-drawer').open, document.activeElement.className]")
                print('  drawer open:',op,'tab seq:',seq,'after Esc (open, focus):',after)
            await c.close()
        await b.close()
asyncio.run(main())
