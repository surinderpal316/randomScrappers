import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_notification_email(email, message):
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

# Example usage
recipient_emails = ["sunny09052000singh@gmail.com"]
notification_message = "Hello! This is a price notification message."
add_recipient(recipient_emails, notification_message)
