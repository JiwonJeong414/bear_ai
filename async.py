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
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        for i in range(len(prompts)):
            await page.goto("https://chatgpt.com/")
            # Find Input 
            await page.wait_for_selector('div[contenteditable="true"]')
            await page.click('div[contenteditable="true"]')
            await page.type('div[contenteditable="true"]', prompts[i], delay=50)
            # Submit the prompt
            await page.keyboard.press("Enter")    
        await browser.close()

# Run the async main function
asyncio.run(main())