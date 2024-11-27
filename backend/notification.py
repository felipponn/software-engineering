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

    @staticmethod
    def check_stock(machine_id, product_id):
        """
        Check the stock of a product in a specific machine.
        Returns True if out of stock, False otherwise.
        """
        query = """
        SELECT quantity
        FROM Coffee_Machine_Products
        WHERE machine_id = %s AND product_id = %s
        """
        result = execute_query_fetchone(query, (machine_id, product_id))
        return result['quantity'] == 0

    @staticmethod
    def notify_user_out_of_stock(user_id):
        """
        Notify users about products out of stock for their selected machines.
        """
        query = """
        SELECT 
            u.email AS user_email,
            p.name AS product_name,
            cm.location AS machine_location
        FROM User_Selected_Machines usm
        JOIN Users u ON usm.user_id = u.user_id
        JOIN Coffee_Machine_Products cmp ON cmp.machine_id = usm.machine_id
        JOIN Products p ON p.product_id = cmp.product_id
        JOIN Coffee_Machines cm ON cm.machine_id = usm.machine_id
        WHERE u.user_id = %s AND cmp.quantity = 0
        """
        results = execute_query_fetchall(query, (user_id,))
        for row in results:
            notification = Notification(
                user_email=row['user_email'],
                product_name=row['product_name'],
                machine_location=row['machine_location']
            )
            notification.send_email()