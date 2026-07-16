from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import time

driver = webdriver.Chrome()

driver.get("https://www.picturehouses.com/cinema/finsbury-park?filter=")

time.sleep(5)

image_urls = set()

for img in driver.find_elements(By.TAG_NAME, "img"):
    src = img.get_attribute("src")
    data_src = img.get_attribute("data-src")

    if src:
        image_urls.add(src)

    if data_src:
        image_urls.add(data_src)

driver.quit()

with open("bg.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["image_url"])

    for url in sorted(image_urls):
        writer.writerow([url])

print(f"Saved {len(image_urls)} unique image URLs to bg.csv")