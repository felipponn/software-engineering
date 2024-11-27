from utils.connect_db import execute_query_fetchall, execute_query_fetchone
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailSender:
    def __init__(self, smtp_server, smtp_port, smtp_user, smtp_password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        
    def send_email(self, receiver_email, subject, body): 
        try:
            message = MIMEMultipart()
            message['From'] = self.smtp_user
            message['To'] = receiver_email
            message['Subject'] = subject
            message.attach(MIMEText(body, 'plain'))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(message)
                
            print("Email sent successfully")
            
        except Exception as e:
            print(f"Error sending email: {e}")
            
class Notification:
    def __init__(self):
        self.subscribers = []
        
    def subscribe(self, user_email):
        if user_email not in self.subscribers:
            self.subscribers.append(user_email)
            print(f"Subscribed {user_email}")
            
    def unsubscribe(self, user_email):
        if user_email in self.subscribers:
            self.subscribers.remove(user_email)
            print(f"Unsubscribed {user_email}")
            
    def notify(self, subject, body):
        email_sender = EmailSender("smtp.gmail.com", 587, "donodaempresa242@gmail.com", "Abcd@1234")
        
        for subscriber in self.subscribers:
            email_sender.send_email(subscriber, subject, body)
            
        print("All subscribers notified!")
        
    def check_stock(self):
        query = """
            SELECT 
                u.email, cm.location, p.name 
            FROM Coffee_Machine_Products cmp
            JOIN Coffee_Machines cm ON cmp.machine_id = cm.machine_id
            JOIN Products p ON cmp.product_id = p.product_id
            JOIN User_Selected_Machines usm ON cmp.machine_id = usm.machine_id
            JOIN Users u ON usm.user_id = u.user_id
            WHERE cmp.quantity = 0;
        """
        
        out_of_stock_products = execute_query_fetchall(query)
        
        if out_of_stock_products:
            for product in out_of_stock_products:
                email = product[0]
                machine_location = product[1]
                product_name = product[2]
                
                notification = Notification()
                notification.subscribe(email)
                notification.notify("Out of Stock Notification", f"{product_name} is out of stock in {machine_location}")
                
        else:
            print("No out of stock products found!")
            
        return out_of_stock_products
    
    def send_email(self):
        self.check_stock()