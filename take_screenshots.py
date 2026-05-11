import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.set_viewport_size({"width": 1280, "height": 900})
        await page.goto("http://localhost:8501")
        await page.wait_for_timeout(6000)

        # Find the iframe and interact with it
        frames = page.frames
        target = None
        for f in frames:
            if f != page.main_frame:
                target = f
                break

        if target:
            await page.screenshot(path="final_hero.png")
            
            # Scroll inside iframe
            await target.evaluate("window.scrollBy(0, 1200)")
            await page.wait_for_timeout(1000)
            await page.screenshot(path="final_mid.png")
            
            await target.evaluate("window.scrollBy(0, 1200)")
            await page.wait_for_timeout(1000)
            await page.screenshot(path="final_features.png")
            
            await target.evaluate("window.scrollBy(0, 1200)")
            await page.wait_for_timeout(1000)
            await page.screenshot(path="final_howit.png")
            
            await target.evaluate("window.scrollBy(0, 1200)")
            await page.wait_for_timeout(1000)
            await page.screenshot(path="final_pricing.png")
            
            await target.evaluate("window.scrollBy(0, 1200)")
            await page.wait_for_timeout(1000)
            await page.screenshot(path="final_footer.png")
        else:
            await page.screenshot(path="final_hero.png")
            print("No iframe found, took single screenshot")

        await browser.close()
        print("All final screenshots done")

asyncio.run(main())
