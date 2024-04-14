import requests
from bs4 import BeautifulSoup

def get_price_amazon(url):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
    }
    response = requests.get(url, headers=header)
    
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
        return None

    soup = BeautifulSoup(response.content, "lxml")
    price_element = soup.find(class_="a-price-whole")

    if price_element:
        price_str = price_element.get_text()
        # Clean and convert the price to an integer value
        price = int(price_str.replace("₹", "").replace(",", "").split(".")[0])
        print(f"Price: ₹{price}")
        return price
    else:
        print("Price not found")
        return None

# Example usage
url = input("Enter Amazon product URL: ")
get_price_amazon(url)
