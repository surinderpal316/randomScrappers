import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def get_amazon_product_info(url, price_threshold):
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

    if response.status_code != 200:
        print(f"Failed to retrieve valid response. Status code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extracting title
    title_element = soup.find('span', {'id': 'productTitle'})
    title = title_element.get_text(strip=True) if title_element else "Title not found"

    # Extracting price using class
    price_element = soup.find('span', {'class': 'a-price-whole'})
    raw_price = price_element.get_text(strip=True) if price_element else "Price not found"

    try:
        # Convert the price to a float for comparison
        current_price = float(raw_price.replace(',', ''))
    except ValueError:
        print("Error converting price to float.")
        return None

    if current_price <= price_threshold:
        return {'title': title, 'price': f'₹{raw_price}'}
    else:
        print("Price is above the threshold. No notification sent.")
        return None

def send_notification_email(email, message):
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

        # Create the email message as a multipart message
        msg = MIMEMultipart()
        msg["Subject"] = "Price Notification"
        msg["From"] = sender_email
        msg["To"] = email

        # Attach the message as plain text
        msg.attach(MIMEText(message, "plain"))

        # Send the email
        server.sendmail(sender_email, email, msg.as_string())

        # Close the connection
        server.quit()

        print(f"Email sent successfully to {email}")
    except Exception as e:
        print(f"Error sending email to {email}: {e}")

def add_recipient(recipients, message):
    for recipient in recipients:
        send_notification_email(recipient, message)

# Example usage for an Amazon product URL and price threshold
url = 'https://www.amazon.in/Samsung-Segments-Smartphone-Octa-Core-Processor/dp/B0BZCSSNV7/?_encoding=UTF8&_encoding=UTF8&ref_=dlx_gate_sd_dcl_tlt_e132d1c2_dt_pd_gw_unk&pd_rd_w=sTG7T&content-id=amzn1.sym.d761a35c-62db-40b5-a8d7-a59fbc8858c4&pf_rd_p=d761a35c-62db-40b5-a8d7-a59fbc8858c4&pf_rd_r=PZNBWJVPH9ZPPJ7BTPTF&pd_rd_wg=9vCVN&pd_rd_r=6bea76c2-254b-471b-a433-eb57c5723dfb'
price_threshold = 50000.0  # Set your desired price threshold
product_info = get_amazon_product_info(url, price_threshold)

if product_info:
    print(f"Title: {product_info['title']}")
    print(f"Price: {product_info['price']}")
    notification_message = f"Price drop alert for {product_info['title']}. Current price: {product_info['price']}"
    recipient_emails = ["surinderbhaker@gmail.com"]
    add_recipient(recipient_emails, notification_message)
