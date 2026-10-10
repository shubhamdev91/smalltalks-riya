import asyncio, json
from playwright.async_api import async_playwright
BASE="https://0nev20-vn.myshopify.com"
PATHS=["/","/collections/all","/cart","/search?q=nail","/pages/our-story","/blogs/journal","/pages/contact"]
JS=r"""()=>{const ld=[...document.querySelectorAll('script[type="application/ld+json"]')].map(s=>{try{const j=JSON.parse(s.textContent);return j['@type']+(j.itemListElement?':'+j.itemListElement.map(i=>i.name).join('>'):'')+(j.offers?':offers='+j.offers.length:'')}catch(e){return 'INVALID JSON: '+e.message}});
return {title:document.title,desc:document.querySelector('meta[name=description]')?.content?.slice(0,80),canon:document.querySelector('link[rel=canonical]')?.href,robots:[...document.querySelectorAll('meta[name=robots]')].map(m=>m.content),ld}}"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(channel='chrome'); pg=await b.new_page()
        for path in PATHS:
            sep='&' if '?' in path else '?'
            await pg.goto(BASE+path+sep+'preview_theme_id=186651934933',wait_until='domcontentloaded')
            print(path, json.dumps(await pg.evaluate(JS),ensure_ascii=False))
        await b.close()
asyncio.run(main())
