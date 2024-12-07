from utils.connect_db import Database
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
        Static method to return a list of Product ids and names from the database.

        Returns:
        - dict
            The dictionary with the Product ids and names.
        """
        db = Database()
        query = """
                SELECT product_id, name
                FROM Products;
                """
        products_data = db.execute_query_fetchall(query)
        # products_data = {id[0]: id[1] for id in products_data}
        return products_data
    
    def get_profile(self):
        """
        Method to get all the informations about the product.

        returnz;
        -list
            The list of atributes of the product.
        """
        db = Database()
        profile_query = """
            SELECT *
            FROM Products
            WHERE product_id = %s;
            """
        product_data = db.execute_query_fetchone(profile_query, (str(self.product_id)))

        available_machines_query = """
            SELECT m.machine_id, m.location, mp.quantity
            FROM Coffee_Machines m
            JOIN Coffee_Machine_Products mp
            ON m.machine_id = mp.machine_id
            WHERE mp.product_id = %s AND mp.quantity > 0;
            """
        available_machines = db.execute_query_fetchall(available_machines_query, (str(self.product_id)))
        available_machines = [{'machine_id': m[0], 'location': m[1], 'quantity': m[2]} for m in available_machines]

        product_reviews_query = """
            SELECT r.product_review_id, u.name, r.rating, r.comment, r.created_at
            FROM Product_Reviews r
            JOIN Users u
            ON r.user_id = u.user_id
            WHERE r.product_id = %s;
            """
        product_reviews = db.execute_query_fetchall(product_reviews_query, (str(self.product_id)))

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
                'num_filtered_reviews': 0,
                'reviews': []
            }
        
        # Calculate mean rating
        mean_rating = sum(review[2] for review in reviews) / len(reviews)
        count_reviews = len(reviews)
        most_recent = max(review[4] for review in reviews)
        filtered_reviews = [review for review in reviews if review[3] and review[3].strip() != '']
        num_filtered_reviews = len(filtered_reviews)

        processed_reviews = []
        for review in filtered_reviews:
            review_id, user_name, rating, comment, created_at = review
            processed_reviews.append({
                'review_id': review_id,
                'user_name': user_name,
                'rating': rating,
                'comment': comment,
                'created_at': created_at.strftime('%Y-%m-%d')
            })
        
        reviews_info = {
            'mean_rating': mean_rating,
            'count_reviews': count_reviews,
            'most_recent': most_recent,
            'num_filtered_reviews': num_filtered_reviews,
            'reviews': processed_reviews
        }

        return reviews_info
    