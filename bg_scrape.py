from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

driver.get("https://www.picturehouses.com/cinema/finsbury-park?filter=")

time.sleep(5)

for img in driver.find_elements(By.TAG_NAME, "img"):
    src = img.get_attribute("src")
    data = img.get_attribute("data-src")

    if src:
        print(src)
    elif data:
        print(data)

driver.quit()