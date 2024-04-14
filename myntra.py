from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from bs4 import BeautifulSoup
import time

def get_product_info_selenium(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1200x600')

    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get(url)

        # Wait for the title and price elements to be clickable
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'span.sc-eDvSVe.fhfLdV'))
            and EC.element_to_be_clickable((By.CSS_SELECTOR, 'h4.sc-eDvSVe.biMVPh'))
        )

        # Give some time for the dynamic content to load
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        title_element = soup.find('span', {'class': 'sc-eDvSVe fhfLdV'})
        title = title_element.text.strip() if title_element else "Title not found"

        price_element = soup.find('h1', {'class': 'sc-eDvSVe biMVPh'})
        price = price_element.text.strip() if price_element else "Price not found"

        return {'title': title, 'price': price}

    finally:
        driver.quit()

# Example usage for a URL
url = "https://www.myntra.com/tshirts/here&now/here&now-men-pack-of-3-slim-fit-solid-round-neck-t-shirts/1909063/buy"
product_info = get_product_info_selenium(url)

if product_info and product_info.get('title') and product_info.get('price'):
    print(f"Title: {product_info['title']}")
    print(f"Price: {product_info['price']}")
else:
    print("Title or price not found or could not be retrieved.")
