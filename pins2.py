from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json

# URL of the Pinterest search page for blouse designs
search_url = "https://www.pinterest.com/search/pins/?q=blouse%20designs"
desired_image_count = 10  # Change this to the number of images you want to scrape

# Configure Chrome WebDriver with options to disable SSL certificate checks
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run Chrome in headless mode
options.add_argument("--disable-gpu")  # Disable GPU acceleration
options.add_argument("--ignore-certificate-errors")  # Ignore SSL certificate errors

# Create a WebDriver instance
driver = webdriver.Chrome(options=options)

# Navigate to the Pinterest search page
driver.get(search_url)

# Create a list to store pin information
pin_data = []

try:
    # Wait for pins to load on the page
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "GrowthUnauthPinImage")))

    # Scroll down to load more pins (you may need to adjust the scroll step)
    scroll_step = 5
    for _ in range(desired_image_count // scroll_step):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "GrowthUnauthPinImage")))

    # Get the page source after loading all pins
    page_source = driver.page_source

    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find all pin links on the page
    pin_links = soup.find_all('a', class_='GrowthUnauthPinImage')

    # Iterate through each pin link
    for pin_link in pin_links[:desired_image_count]:
        # Get the href attribute (partial URL) of the pin link
        partial_url = pin_link.get('href')

        # Construct the full URL of the pin's page
        pin_url = f"https://www.pinterest.com{partial_url}"

        # Extract the pin's title and description from the pin's page (you may need to adjust the selectors)
        title = pin_link.get('title', 'Title not found')
        description = pin_link.get('aria-label', 'Description not found')

        # Create a dictionary with pin information
        pin_info = {
            'pin_url': pin_url,
            'title': title,
            'description': description
        }

        # Append the pin information to the list
        pin_data.append(pin_info)

finally:
    # Close the WebDriver
    driver.quit()

# Save the pin information as JSON
with open('pinterest_pins.json', 'w', encoding='utf-8') as json_file:
    json.dump(pin_data, json_file, ensure_ascii=False, indent=4)

print(f"Scraped {len(pin_data)} pins with metadata and saved to pinterest_pins.json")
