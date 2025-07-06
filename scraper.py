from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import os
import re
import time

os.makedirs("data", exist_ok=True)

options = Options()
# options.add_argument("--headless")  # Uncomment if you want no browser window
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

BASE_URL = "https://www.jumbo.com/producten/koffie-en-thee/?offSet="
ITEMS_PER_PAGE = 24
MAX_PAGES = 34

all_products = []

for page in range(MAX_PAGES):
    offset = page * ITEMS_PER_PAGE
    print(f"🌍 Scraping page {page + 1} with offset {offset}...")
    driver.get(BASE_URL + str(offset))
    time.sleep(2)

    if page == 0:
        try:
            accept_btn = driver.find_element(By.XPATH, "//button[contains(., 'Akkoord')]")
            accept_btn.click()
            print("✅ Clicked 'Akkoord'")
            time.sleep(1)
        except:
            print("⚠️ No cookie banner found")

    items = driver.find_elements(By.CSS_SELECTOR, "article.product-container")

    for item in items:
        try:
            name = item.find_element(By.CSS_SELECTOR, "h3.jum-heading.h6.title").text.strip()
            price_raw = item.find_element(By.CSS_SELECTOR, "div.jum-price").text.strip()
            match = re.search(r"€\s*(\d+,\d+)", price_raw)
            if match:
                price = float(match.group(1).replace(",", "."))
                all_products.append({
                    "name": name,
                    "price": price,
                    "page": page + 1
                })
            else:
                print(f"⚠️ Skipping item (no valid price): {price_raw}")
        except Exception as e:
            print("⚠️ Error parsing item:", e)

driver.quit()

df = pd.DataFrame(all_products)
df.to_csv("data/jumbo_prices.csv", index=False, sep=";", quoting=1)
print(f"✅ Scraped {len(df)} products and saved to 'data/jumbo_prices.csv'")