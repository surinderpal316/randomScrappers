import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def get_amazon_product_info(url, price_threshold, recipient_emails):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Error fetching product information:", e)
        send_notification_email(recipient_emails, "Error fetching product information.")
        return None

    if response.status_code != 200:
        print(f"Failed to retrieve valid response. Status code: {response.status_code}")
        send_notification_email(recipient_emails, "Failed to retrieve valid response. Product may be unavailable.")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # Check if the product is unavailable
    unavailable_message = soup.find('span', {'class': 'a-size-medium a-color-success'})
    if unavailable_message and "Currently unavailable" in unavailable_message.text:
        print("Product is currently not in stock.")
        send_notification_email(recipient_emails, "The product is currently not in stock.")
        return None

    # Extracting title
    title_element = soup.find('span', {'id': 'productTitle'})
    title = title_element.get_text(strip=True) if title_element else "Title not found"

    # Extracting price using class
    price_element = soup.find('span', {'class': 'a-price-whole'})
    raw_price = price_element.get_text(strip=True) if price_element else "Price not found"

    try:
        # Convert the price to an integer
        current_price = int(raw_price.replace(',', ''))
    except ValueError:
        print("Error converting price to integer:", raw_price)
        send_notification_email(recipient_emails, f"Error converting price to integer: {raw_price}")
        return None

    if current_price <= price_threshold:
        message = f"The product '{title}' is available at ₹{current_price}."
        send_notification_email(recipient_emails, message)
        print("Product is available.")
    else:
        message = f"The product '{title}' is not available. Price: ₹{current_price}."
        send_notification_email(recipient_emails, message)
        print("Product is not available.")

    return {'title': title, 'price': f'₹{raw_price}'}



def send_notification_email(recipient_emails, message):
    # Use environment variables or a configuration file to store sensitive information
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "pricedropalertssystem@gmail.com"
    sender_password =  "qpafqzqmpcphrbyi"  # Use an app password for better security

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

# Example usage
url = "https://www.amazon.in/iQOO-Storage-Snapdragon-Processor-44WFlashCharge/dp/B07WHS7MZ4/?_encoding=UTF8&ref_=dlx_gate_sd_dcl_tlt_256d979d_dt_pd_gw_unk&pd_rd_w=CQVk5&content-id=amzn1.sym.9e4ae409-2145-4395-aa6e-45d7f3e95c3e&pf_rd_p=9e4ae409-2145-4395-aa6e-45d7f3e95c3e&pf_rd_r=WJT4PG8ZNZPK0Q5ZB1NY&pd_rd_wg=EypNk&pd_rd_r=4c2b508a-2684-47a5-8917-988fdb31967b&th=1"
price_threshold = 200000
recipient_emails = ["sunny09052000singh@gmail.com"]
product_info = get_amazon_product_info(url, price_threshold, recipient_emails)

if product_info:
    print(f"Title: {product_info['title']}")
    print(f"Price: {product_info['price']}")
    
    # Print availability
    availability = "Product is available." if "not available" not in product_info['title'].lower() else "Product is not available."
    print(availability)