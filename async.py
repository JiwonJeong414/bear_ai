import os
import time
import json
import random
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from urllib.parse import urlparse

# Setup Chrome driver
CHROMEDRIVER_PATH = "/Users/jiwonjeong/Documents/bear_ai/chromedriver-mac-arm64/chromedriver"

options = Options()
options.add_argument(f"--user-data-dir=~/Library/Application Support/Google/Chrome")
options.add_argument("--profile-directory=Default")

service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

# 📂 make sure outputs folder exists
os.makedirs("outputs", exist_ok=True)


def load_all_conversations():
    driver.get("https://chat.openai.com/")
    time.sleep(10)  # Wait for page to load

    # Click “Show more” button repeatedly to load all conversations
    while True:
        try:
            show_more_btn = driver.find_element(By.XPATH, '//button//div[text()="Show more"]')
            driver.execute_script("arguments[0].click();", show_more_btn)
            time.sleep(2)
        except:
            break


def save_data(data, date_str):
    # Save JSON
    with open(f"outputs/conversations_{date_str}.json", "w") as f:
        json.dump(data, f, indent=2)
    # Save CSV
    df = pd.DataFrame([
        {
            "conversation_id": c["id"],
            "title": c["title"],
            "sender": msg["sender"],
            "text": msg["text"]
        }
        for c in data["conversations"] for msg in c["messages"]
    ])
    df.to_csv(f"outputs/conversations_{date_str}.csv", index=False)


def scrape_conversations():
    data = {"conversations": []}
    conv_index = 1

    while True:
        try:
            # find conversation link in the sidebar
            conversation = driver.find_element(By.XPATH, f'(//nav//a)[{conv_index}]')
            title = conversation.text
            conversation.click()
            time.sleep(2)

            # get conversation ID from URL
            current_url = driver.current_url
            url_id = urlparse(current_url).path.split("/")[-1]

            print(f"[{conv_index}] {title} ({url_id})")

            # collect Q&A pairs
            i = 2
            messages = []
            while True:
                try:
                    question = driver.find_element(
                        By.XPATH, f'(//main//div/div/div/div[{i}]/div/div[2])')
                    answer = driver.find_element(
                        By.XPATH, f'(//main//div/div/div/div[{i+1}]/div/div[2])')

                    messages.append({"sender": "human", "text": question.text})
                    messages.append({"sender": "bot", "text": answer.text})

                    i += 2
                except:
                    break

            data["conversations"].append({
                "id": url_id,
                "title": title,
                "messages": messages
            })

            conv_index += 1
            time.sleep(random.uniform(1, 2))
            driver.back()
            time.sleep(2)

        except:
            break

    return data


def main():
    print("🚀 Opening ChatGPT…")
    driver.get("https://chat.openai.com/")

    print("⏳ Log in to ChatGPT if needed…")
    time.sleep(20)  # give yourself time to log in manually

    load_all_conversations()
    scraped_data = scrape_conversations()

    date_str = time.strftime("%Y-%m-%d_%H-%M-%S")
    save_data(scraped_data, date_str)

    print(f"✅ Done. Saved to outputs/conversations_{date_str}.json and .csv")
    driver.quit()


if __name__ == "__main__":
    main()
