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
    title_element = soup.find('h1', {'class': 'prod-name'})
    title = title_element.text.strip() if title_element else "Title not found"

    # Extracting price (assuming it's a div)
    price_element = soup.find('div', {'class': 'prod-sp'})
    price = price_element.text.strip() if price_element else "Price not found"

    return {'title': title, 'price': price}

# Example usage for the provided URL
url = 'https://www.ajio.com/jaguar-classic-black-eau-de-toilette/p/4908240150_multi'
product_info = get_product_info(url)

if product_info:
    print(f"Title: {product_info['title']}")
    print(f"Price: {product_info['price']}")
