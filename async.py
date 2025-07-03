import asyncio
from playwright.async_api import async_playwright

# Prompts to send to ChatGPT
prompts = [
    "What are the best running shoes in 2025",
    "Top performance sneakers for athletes"
]
"""
This script uses Playwright's async API to automate sending prompts to ChatGPT via the web interface.
"""
async def main():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False)
        for prompt in prompts:
            context = await browser.new_context()
            page = await context.new_page()
            # Go to Proxyium
            await page.goto("https://proxyium.com/")
            await page.fill('input#unique-form-control', "https://chatgpt.com/")
            
            await page.click('button[type="submit"]')
            
            await page.wait_for_selector('div[contenteditable="true"]', timeout=20000)
            await page.click('div[contenteditable="true"]')
            await page.type('div[contenteditable="true"]', prompt, delay=50)
            await page.keyboard.press("Enter")
            
            # Wait for the response container to appear
            await page.wait_for_selector('div.markdown', timeout=30000)
            
            # Wait for the response to finish updating
            last_text = ""
            stable_count = 0
            for _ in range(40):  # Try for up to 40 seconds
                content = await page.inner_text('div.markdown')
                if content == last_text:
                    stable_count += 1
                else:
                    stable_count = 0
                if stable_count >= 3:  # Consider stable after 3 checks
                    break
                last_text = content
                await asyncio.sleep(1)
            
            print(f"Prompt: {prompt}\nResponse: {last_text}\n{'-'*40}")
            await page.close()
            await context.close()
        await browser.close()

# Run the async main function
asyncio.run(main())