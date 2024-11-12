from utils.connect_db import execute_query, execute_query_fetchone, execute_query_fetchall
from datetime import datetime

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

    @staticmethod
    def get_machines():
        """
        Static method to return a list of Machine ids from the database.

        Returns:
        - list
            The list of Machine objects.
        """
        query = """
                SELECT machine_id
                FROM Coffee_Machines;
                """
        machines_data = execute_query_fetchall(query)
        machines_data = [id[0] for id in machines_data]
        return machines_data

    def get_profile(self):
        """
        Method to get all the informations about the machine.

        returnz;
        -list
            The list of atributes of the machine.
        """
        profile_query = f"""
            SELECT *
            FROM Coffee_Machines
            WHERE machine_id = {self.machine_id};
        """
        machine_profile = execute_query_fetchone(profile_query)

        available_products_query = f"""
            SELECT p.name, p.price
            FROM Products p
            JOIN Coffee_Machine_Products cmp ON p.product_id = cmp.product_id
            WHERE cmp.machine_id = {self.machine_id} AND cmp.quantity > 0;
        """
        available_products = execute_query_fetchall(available_products_query)
        available_products = [{'name': p[0], 'price': f"{p[1]:.2f}"} for p in available_products]

        machine_reviews_query = f"""
            SELECT r.review_id, u.name AS user_name, r.rating, r.comment, r.created_at
            FROM Reviews r
            JOIN Users u ON r.user_id = u.user_id
            WHERE r.machine_id = {self.machine_id};
        """
        machine_reviews = execute_query_fetchall(machine_reviews_query)

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