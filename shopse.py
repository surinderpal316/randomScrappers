import requests
from bs4 import BeautifulSoup

def get_product_info(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

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

    if response is None or response.status_code != 200:
        print("Failed to retrieve valid response.")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extracting title
    title_element = soup.find('div', {'class':'css-901oao r-op4f77 r-dta0w2 r-1vgyyaa r-1b43r93 r-1rsjblm&'})
    title = title_element.text.strip() if title_element else "Title not found"

    # Extracting price
    price_element = soup.find('div', {'class': 'css-901oao r-op4f77 r-1vgyyaa r-adyw6z'})
    price = price_element.text.strip() if price_element else "Price not found"

    return {'title': title, 'price': price}

# Example usage for the provided URL
url = 'https://www.shopsy.in/digiway-myzk-20w-type-c-fast-charger-pd-3-0-usb-wall-adapter-3-mobile/p/itme63ae7b4cf0a2?pid=XBCGUW8HXVZ6E4P7&lid=LSTXBCGUW8HXVZ6E4P7HURM29&marketplace=FLIPKART&q=charger+type+c&store=tyy%2F4mr%2Ftp2&pageUID=1705822103072'
product_info = get_product_info(url)

if product_info:
    print(f"Title: {product_info['title']}")
    print(f"Price: {product_info['price']}")
