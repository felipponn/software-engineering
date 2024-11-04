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
                SELECT * FROM Coffee_Machines
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

        machine_reviews_query =f"""
                SELECT r.review_id, u.name AS user_name, r.rating, r.comment, r.created_at
                FROM Reviews r
                JOIN Users u ON r.user_id = u.user_id  -- Join with Users to get the reviewer’s name
                WHERE r.machine_id = {self.machine_id};  -- Replace <machine_id> with the actual machine ID you want to query
                """
        machine_reviews = execute_query_fetchall(machine_reviews_query)

        reviews_info = self.post_process_reviews(machine_reviews)

        return machine_profile, available_products, reviews_info
    

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
        total_rating = 0
        total_reviews_count = len(reviews)

        # Calculate total rating including reviews without comments
        for review in reviews:
            total_rating += review[2]  # Assume review[2] is the rating

        # Calculate the mean rating
        mean_rating = total_rating / total_reviews_count if total_reviews_count > 0 else 0

        # Filter reviews that have comments
        filtered_reviews = [review for review in reviews if review[3] is not None and review[3].strip() != '']

        num_filtered_reviews = len(filtered_reviews)

        # Prepare result
        result = {
            'mean_rating': mean_rating,
            'count_reviews': total_reviews_count,
            'filtered_reviews': filtered_reviews,
            'num_filtered_reviews': num_filtered_reviews,
        }
        
        return result