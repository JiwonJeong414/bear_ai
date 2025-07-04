import asyncio
from playwright.async_api import async_playwright
import re
from collections import Counter
import csv

# Prompts to send to ChatGPT
prompts = [
    "What are the best running shoes in 2025",
    "Top performance sneakers for athletes",
    "Most comfortable sneakers for everyday wear",
    "Best shoes for marathon runners in 2025",
    "Top-rated basketball shoes this year",
    "What are the best shoes for trail running",
    "Best sneakers for flat feet",
    "Best lightweight shoes for speed workouts",
    "Most durable sneakers for heavy runners",
    "What are the trendiest sneakers in 2025"
]

# Store results for file output
results = []

"""
This script uses Playwright's async API to automate sending prompts to ChatGPT via the web interface.
"""
async def main():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False)
        for prompt in prompts:
            # Create a new browser context to reset cookies and session data for each prompt
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
            
            brand_counts = match_brands(last_text)
            print(f"Prompt: {prompt}")
            print(f"Brand counts: {brand_counts}")
            
            # Store result for file output
            results.append({
                'prompt': prompt,
                'brand_counts': dict(brand_counts)
            })

            await page.close()
            await context.close()
        await browser.close()
        
        # Save results to csv
        save_to_csv(results)

"""
Uses regex to count # of appearance of popular brands
""" 
def match_brands(text: str) -> int:
    pattern = r'\b(nike|adidas|hoka|new balance|jordan)\b'
    matches = re.findall(pattern, text, flags=re.IGNORECASE)
    counts = Counter(m.lower() for m in matches)
    return counts

"""
Save results to CSV file
"""
def save_to_csv(results, filename="brand_analysis_results.csv"):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Write header
        writer.writerow(['Prompt', 'Nike', 'Adidas', 'Hoka', 'New Balance', 'Jordan', 'Timestamp'])
        
        # Write data rows
        for result in results:
            brand_counts = result['brand_counts']
            writer.writerow([
                result['prompt'],
                brand_counts.get('nike', 0),
                brand_counts.get('adidas', 0),
                brand_counts.get('hoka', 0),
                brand_counts.get('new balance', 0),
                brand_counts.get('jordan', 0)
            ])
    print(f"Results saved to {filename}")
    
# Run the async main function
asyncio.run(main())