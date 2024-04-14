import requests
from bs4 import BeautifulSoup
import re

def clean_price(raw_price):
    # Use regular expression to extract numerical and currency symbols
    cleaned_price = re.search(r'[\d,]+', raw_price)
    return cleaned_price.group() if cleaned_price else "Price not found"

def get_amazon_product_info(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
        return None
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
        return None
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
        return None
    except requests.exceptions.RequestException as err:
        print("Something went wrong:", err)
        return None

    if response is None:
        print("Response is None. Check your network connection or the URL.")
        return None

    if response.status_code != 200:
        print(f"Failed to retrieve valid response. Status code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extracting title
    title_element = soup.find('span', {'id': 'productTitle'})
    title = title_element.text.strip() if title_element else "Title not found"

    # Extracting price using class
    price_element = soup.find('span', {'class': 'a-offscreen'})
    raw_price = price_element.text.strip() if price_element else "Price not found"

    # Clean up the price information
    cleaned_price = clean_price(raw_price)

    return {'title': title, 'price': f'₹{cleaned_price}'}

# Example usage
url = 'https://www.amazon.in/OnePlus-Nord-Chromatic-128GB-Storage/dp/B0BY8MCQ9S/ref=zg_bs_c_electronics_d_sccl_2/260-6502112-1048969?pd_rd_w=ElTaW&content-id=amzn1.sym.7dd29d48-66c1-486c-967d-2ed40101f2ea&pf_rd_p=7dd29d48-66c1-486c-967d-2ed40101f2ea&pf_rd_r=DGYR443TW44M48B9PDTH&pd_rd_wg=QeI8y&pd_rd_r=1b7d44b0-952e-449b-83f3-b2ae7d99a223&pd_rd_i=B0BY8MCQ9S&th=1'
product_info = get_amazon_product_info(url)

if product_info:
    print(f"Title: {product_info['title']}")
    print(f"Price: {product_info['price']}")
