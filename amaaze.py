import requests
from bs4 import BeautifulSoup

def get_amazon_product_info(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8'
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to retrieve valid response. Status code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    # Extracting title
    title_element = soup.find('span', {'id': 'productTitle'})
    title = title_element.text.strip() if title_element else "Title not found"

    # Extracting price using class
    price_element = soup.find('span', {'class': 'a-offscreen'})
    price_str = price_element.text.strip() if price_element else "Price not found"

    # Clean and convert the price to an integer value
    price = int(price_str.replace("₹", "").replace(",", "").split(".")[0]) if price_str.isdigit() else "Price not found"

    return {'title': title, 'price': price, 'url': url}

# Example usage
url = 'https://www.amazon.in/Samsung-Segments-Smartphone-Octa-Core-Processor/dp/B0BZCSSNV7/?_encoding=UTF8&_encoding=UTF8&ref_=dlx_gate_sd_dcl_tlt_e132d1c2_dt_pd_gw_unk&pd_rd_w=sTG7T&content-id=amzn1.sym.d761a35c-62db-40b5-a8d7-a59fbc8858c4&pf_rd_p=d761a35c-62db-40b5-a8d7-a59fbc8858c4&pf_rd_r=PZNBWJVPH9ZPPJ7BTPTF&pd_rd_wg=9vCVN&pd_rd_r=6bea76c2-254b-471b-a433-eb57c5723dfb'
product_info = get_amazon_product_info(url)

if product_info:
    print(f"Title: {product_info['title']}")
    print(f"Price: {product_info['price']}")
    print(f"URL: {product_info['url']}")
