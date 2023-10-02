from selenium import webdriver
from bs4 import BeautifulSoup
import time
import json

# Any infinity scroll URL
url = "https://in.pinterest.com/search/pins/?rs=ac&len=2&q=blouse%20designs&eq=blouse%20designs&etslf=2236" 
desired_image_count = 2  #Change this to the number of pins you want to scrape
sleepTimer = 2  #Increase sleep time for slower connections (you can adjust as needed)

# Bluetooth bug circumnavigate
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])

driver = webdriver.Chrome(options=options) 

driver.get(url)

# Create a list to store pin data
pin_data = []

scroll_pause_time = sleepTimer
last_height = driver.execute_script("return document.body.scrollHeight")

while len(pin_data) < desired_image_count:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause_time)

    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    pin_links = soup.find_all('a', class_='GrowthUnauthPinImage')

    for pin_link in pin_links:
        pin_url = 'https://www.pinterest.com' + pin_link['href']
        driver.get(pin_url)

        pin_soup = BeautifulSoup(driver.page_source, 'html.parser')
        pin_image_element  = pin_soup.find('img', class_='hCL kVc L4E MIw')
        pin_image_url = pin_image_element['src'] if pin_image_element else ''

        pin_data[-1]['pin_image_url'] = pin_image_url
        pin_title_element = pin_soup.find('h1', class_='h1Css-uhp62p e1f5wbog0')
        pin_description_element = pin_soup.find('div', class_='hGzSLd')

        # Extract title and description text
        
        pin_title = pin_title_element.get_text() if pin_title_element else ''
        pin_description = pin_description_element.get_text() if pin_description_element else ''

        metadata = {
            'pin_url': pin_url,
            'pin_title': pin_title,
            'pin_description': pin_description,
            'pin_image_url': pin_image_url,
        }
        pin_data.append(metadata)

    last_height = new_height

# Save the data as JSON
with open('pinterest_pins.json', 'w', encoding='utf-8') as file:
    json.dump(pin_data, file, ensure_ascii=False, indent=4)

print(f"Scraped {len(pin_data)} pins with titles and descriptions and saved to pinterest_pins.json")

# Close the driver
driver.quit()

