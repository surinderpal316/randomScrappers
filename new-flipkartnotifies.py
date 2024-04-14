import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def get_flipkart_product_info(url, price_threshold, recipient_emails):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
        send_notification_email(recipient_emails, "Error fetching product information: HTTP Error.")
        return None
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
        send_notification_email(recipient_emails, "Error fetching product information: Connection Error.")
        return None
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
        send_notification_email(recipient_emails, "Error fetching product information: Timeout Error.")
        return None
    except requests.exceptions.RequestException as err:
        print("Something went wrong:", err)
        send_notification_email(recipient_emails, "Error fetching product information: Something went wrong.")
        return None

    if response.status_code != 200:
        print(f"Failed to retrieve valid response. Status code: {response.status_code}")
        send_notification_email(recipient_emails, "Failed to retrieve valid response. Product may be unavailable.")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # Check if the product is unavailable
    unavailable_message = soup.find('div', {'class': '_1YokD2 _2GoDe3'})
    if unavailable_message and "Sold Out" in unavailable_message.text:
        title_element = soup.find('span', {'class': 'B_NuCI'})
        title = title_element.text.strip() if title_element else "Title not found"
        print(f"Product '{title}' is currently not in stock.")
        send_notification_email(recipient_emails, f"The product '{title}' is currently not in stock. We will notify you when it becomes available. {url}")
        return None

    # Extracting title
    title_element = soup.find('span', {'class': 'B_NuCI'})
    title = title_element.text.strip() if title_element else "Title not found"

    # Extracting price
    price_element = soup.find('div', {'class': '_30jeq3 _16Jk6d'})
    price_str = price_element.text.strip() if price_element else "Price not found"

    # Clean and convert the price to an integer value
    price = int(price_str.replace("₹", "").replace(",", ""))

    # Check if the title indicates unavailability
    if "not available" in title.lower():
        print(f"Product '{title}' is not available.")
        send_notification_email(recipient_emails, f"The product '{title}' is not available. We will notify you when it becomes available. {url}")
        return None

    if price <= price_threshold:
        message = f"The product '{title}' is available at ₹{price}. Here is the link: {url}"
        send_notification_email(recipient_emails, message)
        print("Product is available and below the threshold.")
    else:
        message = f"The product '{title}' is not available or the price is above the threshold (₹{price}). We will notify you when the price drops or the product is in stock. {url}"
        send_notification_email(recipient_emails, message)
        print("Product is not available or above the threshold.")

    return {'title': title, 'price': price, 'url': url}

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

# Example usage for a Flipkart product URL
url = 'https://www.flipkart.com/google-pixel-7a-charcoal-128-gb/p/itmb4d7b100b1a4d?pid=MOBGZCQMHGWDYZQ7&lid=LSTMOBGZCQMHGWDYZQ71MTVC2&marketplace=FLIPKART&store=tyy%2F4io&srno=b_1_1&otracker=browse&fm=organic&iid=44c926fb-4561-432c-a078-a0eb42bd66f4.MOBGZCQMHGWDYZQ7.SEARCH&ppt=hp&ppn=homepage&ssid=n7dpft0gdc0000001705490005652'  # Replace with the desired Flipkart product URL
price_threshold = 50000
recipient_emails = ["sunny09052000singh@gmail.com"]
product_info = get_flipkart_product_info(url, price_threshold, recipient_emails)

if product_info:
    print(f"Title: {product_info['title']}")
    print(f"Price: {product_info['price']}")
    print(f"URL: {product_info['url']}")
    
    # Print availability
    availability = "Product is available." if "not available" not in product_info['title'].lower() else "Product is not available."
    print(availability)