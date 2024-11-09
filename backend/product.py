from utils.connect_db import execute_query, execute_query_fetchone, execute_query_fetchall

class Procuct:
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

        # TODO: Add product review info when implemented

        profile = {
            "product_id": product_data[0],
            "name": product_data[1],
            "description": product_data[2],
            "price": product_data[3],
        }
        return profile, available_machines
    