import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

URL = "https://www.picturehouses.com/cinema/finsbury-park?filter="

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

image_urls = set()

# Common image attributes
image_attrs = [
    "src",
    "data-src",
    "data-original",
    "data-lazy-src",
    "data-srcset",
    "srcset",
]

for tag in soup.find_all(["img", "source"]):
    for attr in image_attrs:
        value = tag.get(attr)
        if not value:
            continue

        # Handle srcset
        if "srcset" in attr:
            for item in value.split(","):
                img = item.strip().split(" ")[0]
                image_urls.add(urljoin(URL, img))
        else:
            image_urls.add(urljoin(URL, value))

# Background images in inline styles
for tag in soup.find_all(style=True):
    matches = re.findall(r'url\(["\']?(.*?)["\']?\)', tag["style"])
    for match in matches:
        image_urls.add(urljoin(URL, match))

print(f"Found {len(image_urls)} images:\n")


with open("bg.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["image_url"])  # Header

    for img in sorted(image_urls):
        writer.writerow([img])

print(f"Saved {len(image_urls)} image URLs to bg.csv")