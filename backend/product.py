from utils.connect_db import execute_query, execute_query_fetchone, execute_query_fetchall
from datetime import datetime

class Product:
    """
    Product class to represent a product in a vending machine.

    Attributes:
    - product_id: int
        The unique identifier of the product.

    Methods:
    - __init__(self, product_id: int, name: str, price: float,
               quantity: int)
        Constructor to initialize the Product object.
    - get_products()
        Static method to return a list of Product objects from the database.
    - get_profile()
        Method to get all the informations about the product.
    """

    def __init__(self, product_id: int = None):
        """
        Constructor to initialize the Product object.

        Attributes:
        - product_id: int
            The unique identifier of the product.
        """
        self.product_id = product_id

    @staticmethod
    def get_products():
        """
        Static method to return a list of Product ids from the database.

        Returns:
        - list
            The list of Product objects.
        """
        query = """
                SELECT product_id
                FROM Products;
                """
        products_data = execute_query_fetchall(query)
        products_data = [id[0] for id in products_data]
        return products_data
    
    def get_profile(self):
        """
        Method to get all the informations about the product.

        returnz;
        -list
            The list of atributes of the product.
        """
        profile_query = f"""
            SELECT *
            FROM Products
            WHERE product_id = {self.product_id};
            """
        product_data = execute_query_fetchone(profile_query)

        available_machines_query = f"""
            SELECT m.machine_id, m.location
            FROM Coffee_Machines m
            JOIN Coffee_Machine_Products mp
            ON m.machine_id = mp.machine_id
            WHERE mp.product_id = {self.product_id} AND mp.quantity > 0;
            """
        available_machines = execute_query_fetchall(available_machines_query)

        product_reviews_query = f"""
            SELECT r.product_review_id, u.name, r.rating, r.created_at
            FROM Product_Reviews r
            JOIN Users u
            ON r.user_id = u.user_id
            WHERE r.product_id = {self.product_id};
            """
        product_reviews = execute_query_fetchall(product_reviews_query)

        reviews_info = self.post_process_reviews(product_reviews)

        profile = {
            "product_id": product_data[0],
            "name": product_data[1],
            "description": product_data[2],
            "price": product_data[3],
        }

        return profile, available_machines, reviews_info
    
    @staticmethod
    def post_process_reviews(reviews):
        """
        Method to post-process the reviews data.

        Args:
        - reviews: list
            The list of reviews data.

        Returns:
        - reviews_info: dict
            The dictionary that summarizes the reviews data.
        """
        # Empty reviews case
        if not reviews:
            return {
                'mean_rating': 0,
                'count_reviews': 0,
                'most_recent': datetime(year=1970, month=1, day=1),
            }
        
        # Calculate mean rating
        mean_rating = sum(review[2] for review in reviews) / len(reviews)
        count_reviews = len(reviews)
        most_recent = max(review[3] for review in reviews)

        reviews_info = {
            'mean_rating': mean_rating,
            'count_reviews': count_reviews,
            'most_recent': most_recent
        }

        return reviews_info
    