from selenium import webdriver
from bs4 import BeautifulSoup
import time
import json

# Any infinity scroll URL

url = "https://in.pinterest.com/search/pins/?rs=ac&len=2&q=blouse%20designs&eq=blouse%20designs&etslf=2236"
desired_image_count = 2  # Change this to the number of images you want to scrape
sleepTimer = 2  # Increase sleep time for slower connections (you can adjust as needed)

# Bluetooth bug circumnavigate
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])

driver = webdriver.Chrome(options=options)  # path=r'to/chromedriver.exe'
driver.get(url)

# Create a list to store image data
image_data = []

scroll_pause_time = sleepTimer
last_height = driver.execute_script("return document.body.scrollHeight")

while len(image_data) < desired_image_count:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause_time)

    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    for link in soup.find_all('img'):
        image_url = link.get('src')
        description = link.get('alt')  # Use 'alt' attribute to get the image description

        metadata = {
            'image_url': image_url,
            'description': description,
        }
        image_data.append(metadata)

    last_height = new_height

# Save the data as JSON
with open('pinterest_images.json', 'w', encoding='utf-8') as file:
    json.dump(image_data, file, ensure_ascii=False, indent=4)

print(f"Scraped {len(image_data)} images with metadata and saved to pinterest_images.json")