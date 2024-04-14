import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def get_product_info(url, price_threshold, recipient_emails):
    # Detect the platform based on the URL
    if "flipkart" in url:
        platform = "Flipkart"
    elif "amazon" in url:
        platform = "Amazon"
    else:
        print("Unsupported platform. Please provide a valid Amazon or Flipkart URL.")
        return None

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
        send_notification_email(recipient_emails, f"Error fetching product information from {platform}: HTTP Error.")
        return None
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
        send_notification_email(recipient_emails, f"Error fetching product information from {platform}: Connection Error.")
        return None
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
        send_notification_email(recipient_emails, f"Error fetching product information from {platform}: Timeout Error.")
        return None
    except requests.exceptions.RequestException as err:
        print("Something went wrong:", err)
        send_notification_email(recipient_emails, f"Error fetching product information from {platform}: Something went wrong.")
        return None

    if response.status_code != 200:
        print(f"Failed to retrieve valid response from {platform}. Status code: {response.status_code}")
        send_notification_email(recipient_emails, f"Failed to retrieve valid response from {platform}. Product may be unavailable.")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # Detect platform-specific elements
    if platform == "Flipkart":
        unavailable_message = soup.find('div', {'class': '_1YokD2 _2GoDe3'})
        title_element = soup.find('span', {'class': 'B_NuCI'})
        price_element = soup.find('div', {'class': '_30jeq3 _16Jk6d'})
    elif platform == "Amazon":
        unavailable_message = soup.find('span', {'class': 'a-size-medium a-color-success'})
        title_element = soup.find('span', {'id': 'productTitle'})
        price_element = soup.find('span', {'class': 'a-price-whole'})
    else:
        print(f"Unsupported platform: {platform}")
        return None

    # Initialize title before using it
    title = title_element.text.strip() if title_element else "Title not found"

    # Extracting price
    price_str = price_element.text.strip() if price_element else "Price not found"

    # Clean and convert the price to an integer value
    price = int(price_str.replace("₹", "").replace(",", "").rstrip('.'))

    # Rest of the code remains the same...

    return {'title': title, 'price': price, 'url': url, 'platform': platform}

def send_notification_email(recipient_emails, message):
    # Use environment variables or a configuration file to store sensitive information
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "pricedropalertssystem@gmail.com"
    sender_password = "qpafqzqmpcphrbyi"  # Use an app password for better security

    try:
        # Create a connection to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)

        # Create the email message
        msg = MIMEMultipart()
        msg["Subject"] = "Product Notification"
        msg["From"] = sender_email
        msg["To"] = ', '.join(recipient_emails)

        # Attach the message as plain text
        msg.attach(MIMEText(message, "plain"))

        # Send the email
        server.sendmail(sender_email, recipient_emails, msg.as_string())

        # Close the connection
        server.quit()

        print(f"Email sent successfully to {', '.join(recipient_emails)}")
    except Exception as e:
        print(f"Error sending email to {', '.join(recipient_emails)}: {e}")

# Example usage for the provided Flipkart product URL and price threshold
url = 'https://www.flipkart.com/google-pixel-7a-charcoal-128-gb/p/itmb4d7b100b1a4d?pid=MOBGZCQMHGWDYZQ7&lid=LSTMOBGZCQMHGWDYZQ71MTVC2&marketplace=FLIPKART&store=tyy%2F4io&srno=b_1_1&otracker=browse&fm=organic&iid=44c926fb-4561-432c-a078-a0eb42bd66f4.MOBGZCQMHGWDYZQ7.SEARCH&ppt=hp&ppn=homepage&ssid=n7dpft0gdc0000001705490005652'
price_threshold = 50000
recipient_emails = ["sunny09052000singh@gmail.com"]
product_info = get_product_info(url, price_threshold, recipient_emails)

if product_info:
    print(f"Title: {product_info['title']}")
