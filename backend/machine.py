from utils.connect_db import Database
from datetime import datetime
import smtplib
from email.message import EmailMessage
from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, machine, product):
        pass

class UserObserver(Observer):
    def __init__(self, user_email):
        self.user_email = user_email

    def update(self, machine, product):
        msg = EmailMessage()
        msg['Subject'] = f'Produto "{product["name"]}" esgotado na máquina {machine.machine_id}'
        msg['From'] = 'donodaempresa242@gmail.com'
        msg['To'] = self.user_email
        msg.set_content(f'O produto "{product["name"]}" na máquina localizada em {machine.get_profile()[0]["location"]} está esgotado.')

        # Sending the email via SMTP server
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                smtp.starttls()  
                smtp.login('donodaempresa242@gmail.com', 'Abcd@1234')  
                smtp.send_message(msg)
                print(f"E-mail enviado com sucesso para {self.user_email}!")
        except Exception as e:
            print(f"Erro ao enviar e-mail para {self.user_email}: {e}")


class Machine:
    """
    Machine class to represent a vending machine.
    
    Attributes:
    - machine_id: int
        The unique identifier of the machine. 
        
    Methods:
    - __init__(self, machine_id: int, location: str, products: list,
                 status: bool, last_serviced_at: datetime, installed_at: datetime)
        Constructor to initialize the Machine object.
    - get_machines()
        Static method to return a list of Machine objects from the database.
    - get_profile()
        Method to get all the informations about the machine
    """
    
    def __init__(self, machine_id: int = None):
        """
        Constructor to initialize the Machine object.

        Attributes:
        - machine_id: int
            The unique identifier of the machine.
        """
        self.machine_id = machine_id
        self.observers = []

    def attach(self, observer: Observer):
        """Attach a new observer."""
        self.observers.append(observer)

    def detach(self, observer: Observer):
        """Remove an existing observer."""
        self.observers.remove(observer)

    def notify_observers(self, product):
        """Notify all observers about the state change."""
        for observer in self.observers:
            observer.update(self, product)

    @staticmethod
    def get_selected_users(machine_id):
        """Get users who have selected the machine as a favorite."""
        db = Database()
        query = """
                SELECT u.email
                FROM Users u
                JOIN User_Selected_Machines usm ON u.user_id = usm.user_id
                WHERE usm.machine_id = %s;
                """
        users = db.execute_query_fetchall(query, (machine_id,))
        return [user[0] for user in users]

    def load_observers(self):
        """Load observers from the database."""
        user_emails = self.get_selected_users(self.machine_id)
        for email in user_emails:
            self.attach(UserObserver(email))

    def check_and_notify(self):
        """
        Check products and notify users if any product is out of stock.
        """
        _, available_products, _ = self.get_profile()
        for product in available_products:
            if product['quantity'] == 0:
                self.notify_observers(product)

    @staticmethod
    def get_machines():
        """
        Static method to return a list of Machine ids from the database.

        Returns:
        - list
            The list of Machine objects.
        """
        db = Database()
        query = """
                SELECT machine_id
                FROM Coffee_Machines;
                """
        machines_data = db.execute_query_fetchall(query)
        machines_data = [id[0] for id in machines_data]
        return machines_data

    def get_profile(self):
        """
        Method to get all the informations about the machine.

        returnz;
        -list
            The list of atributes of the machine.
        """
        db = Database()
        profile_query = f"""
            SELECT *
            FROM Coffee_Machines
            WHERE machine_id = {self.machine_id};
        """
        machine_profile = db.execute_query_fetchone(profile_query)

        available_products_query = f"""
            SELECT p.name, p.price, p.product_id, cmp.quantity
            FROM Products p
            JOIN Coffee_Machine_Products cmp ON p.product_id = cmp.product_id
            WHERE cmp.machine_id = {self.machine_id} AND cmp.quantity > 0;
        """
        available_products = db.execute_query_fetchall(available_products_query)
        available_products = [{'name': p[0], 'price': f"{p[1]:.2f}", "product_id": p[2],
                               'quantity': p[3]} for p in available_products]

        machine_reviews_query = f"""
            SELECT r.review_id, u.name AS user_name, r.rating, r.comment, r.created_at
            FROM Reviews r
            JOIN Users u ON r.user_id = u.user_id
            WHERE r.machine_id = {self.machine_id};
        """
        machine_reviews = db.execute_query_fetchall(machine_reviews_query)

        reviews_info = self.post_process_reviews(machine_reviews)

        profile = {
            'machine_id': machine_profile[0],
            'location': machine_profile[1],
            'status': machine_profile[2],
            'last_maintenance': machine_profile[3].strftime('%Y-%m-%d') if machine_profile[3] else 'N/A',
            'installation_date': machine_profile[4].strftime('%Y-%m-%d') if machine_profile[4] else 'N/A'
        }

        return profile, available_products, reviews_info

    @staticmethod
    def post_process_reviews(reviews):
        """
        Post-processes the list of reviews to calculate the average rating,
        count the total number of reviews, and filter out reviews without comments.

        Args:
            reviews (list): A list of tuples containing reviews data.

        Returns:
            dict: A dictionary containing the mean rating, count of all reviews, and filtered reviews.
        """
        # Initialize total rating and count of reviews
        if not reviews:
            return {
                'mean_rating': 0,
                'count_reviews': 0,
                'num_filtered_reviews': 0,
                'reviews': []
            }

        total_rating = sum([review[2] for review in reviews])
        mean_rating = total_rating / len(reviews)
        count_reviews = len(reviews)
        filtered_reviews = [review for review in reviews if review[3] and review[3].strip() != '']
        num_filtered_reviews = len(filtered_reviews)

        processed_reviews = []
        for review in filtered_reviews:
            processed_reviews.append({
                'review_id': review[0],
                'user_name': review[1],
                'rating': review[2],
                'comment': review[3],
                'created_at': review[4].strftime('%Y-%m-%d')
            })

        return {
            'mean_rating': round(mean_rating, 1),
            'count_reviews': count_reviews,
            'num_filtered_reviews': num_filtered_reviews,
            'reviews': processed_reviews 
        }

    def update_product_quantity(self, product_id, new_quantity):
        """
        Updates the quantity of a product and notifies observers if the quantity is zero.

        Args:
            product_id (int): ID of the product.
            new_quantity (int): New quantity of the product.
        """
        db = Database()
        update_query = """
            UPDATE Coffee_Machine_Products
            SET quantity = %s
            WHERE machine_id = %s AND product_id = %s;
        """
        db.execute_query(update_query, (new_quantity, self.machine_id, product_id))

        if new_quantity == 0:
            # Load observers and notify
            self.load_observers()
            # Get the product name for the message
            product_query = """
                SELECT name
                FROM Products
                WHERE product_id = %s;
            """
            product_name = db.execute_query_fetchone(product_query, (product_id,))[0]
            product = {'name': product_name}
            self.notify_observers(product)
