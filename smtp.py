# smtp.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email = "sender@gmail.com"
receiver_email = "receiver@gmail.com"
smtp_server = "smtp.gmail.com"
smtp_port = 587  # Port for STARTTLS
password = "supersecureshithere"

def send_email(subject, message):
    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Add body to email
    msg.attach(MIMEText(message, 'plain'))

    # Create SMTP session
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Secure the connection
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)

if __name__ == "__main__":
    subject = "[Alert] Node is down."
    message = "Check yo shit!"

    send_email(subject, message)
    print("Email sent successfully.")
