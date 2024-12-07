# notification.py
from observer import Observer
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Notification(Observer):
    def __init__(self, user_email, product_name, machine_location):
        self.user_email = user_email
        self.product_name = product_name
        self.machine_location = machine_location

    def update(self, product_name, machine_location):
        self.product_name = product_name
        self.machine_location = machine_location
        self.send_email()

    def send_email(self):
        msg = MIMEMultipart()
        msg['From'] = 'donodaempresa242@gmail.com'
        msg['To'] = self.user_email
        msg['Subject'] = 'Product Out of Stock Notification'
        body = f'The product {self.product_name} is out of stock at the vending machine located at {self.machine_location}. Please check another machine.'
        msg.attach(MIMEText(body, 'plain'))
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login('donodaempresa242@gmail.com', 'Abcd@1234')
            text = msg.as_string()
            server.sendmail('donodaempresa242@gmail.com', self.user_email, text)
            server.quit()
            print("Email sent successfully")
        except Exception as e:
            print(f"Failed to send email: {e}")