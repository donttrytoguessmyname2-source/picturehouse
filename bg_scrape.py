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

with open("bg_raw.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["image_url"])

    for url in sorted(image_urls):
        writer.writerow([url])



input_file = "bg_raw.csv"

output_file = "bg.csv"

seen = set()

with open(input_file, "r", encoding="utf-8") as infile, \
     open(output_file, "w", newline="", encoding="utf-8") as outfile:

    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    header = next(reader)
    writer.writerow(header)

    for row in reader:
        if row[0] not in seen:
            seen.add(row[0])
            writer.writerow(row)

print(f"Removed duplicates. Saved {len(seen)} unique URLs to {output_file}")

