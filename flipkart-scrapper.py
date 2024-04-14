import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import matplotlib.pyplot as plt

def get_flipkart_product_info(url):
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

    if response is None or response.status_code != 200:
        print("Failed to retrieve valid response.")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extracting title
    title_element = soup.find('span', {'class': 'B_NuCI'})
    title = title_element.text.strip() if title_element else "Title not found"

    # Extracting price
    price_element = soup.find('div', {'class': '_30jeq3 _16Jk6d'})
    price = price_element.text.strip() if price_element else "Price not found"

    return {'title': title, 'price': price}

# Example usage for a Flipkart product URL
url = 'https://www.flipkart.com/redmi-note-12-pro-5g-glacier-blue-128-gb/p/itm8fbee21008560?pid=MOBGH2UVZHHQGRRP&lid=LSTMOBGH2UVZHHQGRRPHJOZCG&marketplace=FLIPKART&store=tyy%2F4io&srno=b_1_1&otracker=browse&fm=organic&iid=4767de21-4383-4b70-93f6-e91bbf97bf6b.MOBGH2UVZHHQGRRP.SEARCH&ppt=hp&ppn=homepage&ssid=dhkwjv6qts0000001705387667501'  # Replace with the desired Flipkart product URL
product_info = get_flipkart_product_info(url)

if product_info:
    print(f"Title: {product_info['title']}")
    print(f"Price: {product_info['price']}")
