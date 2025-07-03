import asyncio
from playwright.async_api import async_playwright

prompts = [
    "What are the best running shoes in 2025",
    "Top performance sneakers for athletes"
]

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://chatgpt.com/")
        await page.wait_for_selector('div[contenteditable="true"]')
        await page.click('div[contenteditable="true"]')
        await page.type('div[contenteditable="true"]', "Hello, ChatGPT!", delay=50)
        await page.keyboard.press("Enter")
        print(await page.title())
        await browser.close()

asyncio.run(main())