from utils.connect_db import execute_query_fetchall, execute_query_fetchone
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Notification:
    def __init__(self, user_email, product_name, machine_location):
        self.user_email = user_email
        self.product_name = product_name
        self.machine_location = machine_location

    def send_email(self):
        msg = MIMEMultipart()
        msg['From'] = 'noreply@vendingmachine.com'
        msg['To'] = self.user_email
        msg['Subject'] = 'Product Out of Stock Notification'

        body = f'The product {self.product_name} is out of stock at the vending machine located at {self.machine_location}. Please check another machine.'
        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login('your_email@gmail.com', 'your_password')
            text = msg.as_string()
            server.sendmail('noreply@vendingmachine.com', self.user_email, text)
            server.quit()
            print("Email sent successfully")
        except Exception as e:
            print(f"Failed to send email: {e}")

    @staticmethod
    def check_stock(machine_id, product_id):
        # This method should interact with the database to check the stock status
        # For simplicity, let's assume it returns True if out of stock, False otherwise
        # Replace this with actual database interaction code
        return True