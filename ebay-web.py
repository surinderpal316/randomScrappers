import requests
from bs4 import BeautifulSoup
from forex_python.converter import CurrencyRates

def convert_usd_to_inr(price_usd):
    # Use the current exchange rate to convert USD to INR
    c = CurrencyRates()
    exchange_rate = c.get_rate('USD', 'INR')
    price_inr = price_usd * exchange_rate
    return round(price_inr, 2)

def get_ebay_product_info(url):
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

    if response is None:
        print("Response is None. Check your network connection or the URL.")
        return None

    if response.status_code != 200:
        print(f"Failed to retrieve valid response. Status code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extracting title
    title_element = soup.find('span', {'class': 'class="ux-textspans ux-textspans--BOLD'})
    title = title_element.text.strip() if title_element else "Title not found"

    # Extracting price in USD
    price_element = soup.find('span', {'class': 'ux-textspans'})
    raw_price_usd = price_element.text.strip() if price_element else "Price not found"

    # Clean up the price information
    cleaned_price_usd = float(''.join(filter(str.isdigit, raw_price_usd))) if raw_price_usd.isdigit() else 0.0

    return {'title': title, 'price_usd': cleaned_price_usd}

# Example usage for an eBay product URL
url = 'https://www.ebay.com/itm/325734963310?hash=item4bd751186e:g:QDsAAOSwb~1kZ~Sh&amdata=enc%3AAQAIAAAA4DaBTK104BKPicA9PPIgZqk1UKhXefEeN5bnj6n5db31j8ToJn%2FW9JXhyisP%2BcibzT%2FNvXfZcbcqD0DADzKxREEiZ73%2B%2FW8JmbOlU442Y4TDPfF3saGCMZdZnqluG4dcw%2F%2BQRQ1U72s4%2F2rlWbacinuVDwhCG%2BdmqWopZg3XAByOUVJEMBtpwkLTUJXmxE%2BRk%2Bc5OPZlejfHdJiIlD0smESRg%2B9aYFP4YH%2B7QR0JX0b9I5HOtsjFtiwITIJ%2F%2F7WNhYxSykQ5U753M4x6Cn3uSOq%2F33%2FHbogF94tYOpeuVY%2FZ%7Ctkp%3ABFBMtqKqmKJj'  # Replace with the desired eBay product URL
product_info = get_ebay_product_info(url)

if product_info:
    print(f"Title: {product_info['title']}")
    print(f"Price in USD: ${product_info['price_usd']}")
    
    # Convert the price to Indian Rupees
    price_inr = convert_usd_to_inr(product_info['price_usd'])
    print(f"Price in INR: ₹{price_inr}")
