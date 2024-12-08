
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.connect_db import Database
from datetime import datetime
from backend.user import User
from backend.stock import Stock, AggregationStrategy, SumStrategy

class Manager(User):
    """
    A class representing a Manager in the system, allowing for actions like viewing all reported issues.

    Attributes:
    - user_name : str
        The name of the user.
    - password : str
        The user's password.
    - email : str
        The user's email.
    - phone : str
        The user's phone number.
    - user_id : UUID or None
        The unique identifier for the user, generated after saving to the database.
        
    Methods:
    - __init__(self, user_name: str, password: str, email: str, phone: str, user_id=None)
        Constructor to initialize the Manager object.
    - save_db(self)
        Saves the Manager to the database (used for sign-up).
    - authenticate(email, password)
        Authenticates a user by email and password, retrieving the user details from the database if valid.
    - view_all_issues(self, issue=None, machine=None, type=None, description=None
        Fetches all reported issues from the database based on optional filters for issue, machine, type, and description.
        Returns a list of dictionaries representing the issues.
    """
    def __init__(self, user_name: str, password: str, email: str, phone: str, user_id=None, favorite_machines=[], role=None):
        super().__init__(user_name, password, email, phone, user_id, favorite_machines, role)

    def save_db(self):
        """
        Saves the User to the database (used for sign-up). 

        After saving, the method sets the `user_id` by executing a query 
        to insert the user's details into the `Users` table and returning the generated `user_id`.
        """
        db = Database()
        query = """
                INSERT INTO Users (name, email, phone_number, password, role)
                VALUES (%s, %s, %s, %s ,'manager')
                RETURNING user_id;
                """
        
        # Executes the query and assigns the returned user_id to the user instance
        self.user_id = db.execute_query_fetchone(query, (self.user_name, self.email, self.phone, self.password), True)[0]

    @staticmethod
    def authenticate(email, password):
        """
        Authenticates a user by email and password, retrieving the user details from the database if valid.

        Parameters:
        ----------
        email : str
            The email of the user attempting to log in.
        password : str
            The password provided by the user.

        Returns:
        -------
        User or None:
            Returns a User object if authentication is successful, or None if the authentication fails.
        """
        db = Database()
        query = """
                SELECT user_id, name, email, password, phone_number, role
                FROM users 
                WHERE email = %s;
            """
        # Fetches user data from the database based on email
        user_data = db.execute_query_fetchone(query, (email,))

        if user_data:
            user_id, user_name, email, correct_password, phone, role = user_data

            # Checks if the provided password matches the stored password
            if correct_password == password:
                print(f"User {user_name} successfully logged in!")
                # Creates and returns a User object if authentication is successful

                favorites_query = """
                                 SELECT machine_id
                                 FROM User_Selected_Machines
                                 WHERE user_id = %s;
                                 """
                favorite_machines = db.execute_query_fetchall(favorites_query, (user_id,))
                favorite_machines = [row[0] for row in favorite_machines] if favorite_machines else []

                user = Manager(user_name, password, email, phone, user_id=user_id, favorite_machines=favorite_machines, role=role)
                return user
            
            else:
                print("Incorrect password!")
        else:
            print("User not found!")

    def view_all_issues(self, issue=None, machine=None, type=None, status=None):
        """
        Fetches all reported issues from the database based on optional filters for issue, machine, type, and status.
        Returns a list of dictionaries representing the issues.
        """
        db = Database()
        # Base query
        query = """
            SELECT report_id, user_id, machine_id, report_target, issue_type, description, status, created_at, resolved_at
            FROM User_Reports
            WHERE 1=1
        """
        
        # List to hold query parameters
        params = []

        # Apply filters if provided
        if issue:
            query += " AND report_target = %s"
            params.append(issue)
        
        if machine:
            query += " AND machine_id = %s"
            params.append(machine)
        
        if type:
            query += " AND issue_type = %s"
            params.append(type)
        
        if status:
            query += " AND status ILIKE %s"
            params.append(f'%{status}%')

        # Execute the query with the filters
        issues = db.execute_query_fetchall(query, params)

        # Return a structured list of issues
        return [
            {
                'report_id': issue[0],
                'user_id': issue[1],
                'machine_id': issue[2],
                'report_target': issue[3],
                'issue_type': issue[4],
                'description': issue[5],
                'status': issue[6],
                'created_at': issue[7],
                'resolved_at': issue[8],
            } for issue in issues
        ]

    def get_stock(self, machine_id=None, product_name=None, quantity_category=None, granularity="all", strategy=SumStrategy()):
        """
        Fetches and aggregates stock information based on filters, granularity, and strategy.

        Parameters:
        ----------
        machine_id : str or None
            Filter by machine_id.
        product_name : str or None
            Filter by product_name.
        quantity_category : str or None
            Filter by quantity_category.
        granularity : str
            Aggregation granularity ("all", "no_machine", "no_product").
        strategy : AggregationStrategy
            An instance of an aggregation strategy (e.g., SumStrategy, AverageStrategy, CountStrategy).

        Returns:
        -------
        list:
            List of dictionaries representing the aggregated stock information.
        """
        if not strategy or not isinstance(strategy, AggregationStrategy):
            raise ValueError("A valid AggregationStrategy instance must be provided.")

        db = Database()
        query = """
            WITH CategorizedStock AS (
                SELECT 
                    cm.machine_id,
                    cm.location,
                    p.name AS product_name,
                    cmp.quantity,
                    CASE 
                        WHEN cmp.quantity = 0 THEN 'Critical'
                        WHEN cmp.quantity < 10 THEN 'Low'
                        WHEN cmp.quantity < 50 THEN 'Medium'
                        WHEN cmp.quantity < 100 THEN 'High'
                        ELSE 'Full'
                    END AS quantity_category
                FROM 
                    Coffee_Machine_Products cmp
                JOIN 
                    Products p ON cmp.product_id = p.product_id
                JOIN 
                    Coffee_Machines cm ON cmp.machine_id = cm.machine_id
            )
            SELECT 
                machine_id,
                location,
                product_name,
                quantity,
                quantity_category
            FROM 
                CategorizedStock
            ORDER BY 
                quantity ASC;
        """

        stock_info = db.execute_query_fetchall(query)

        stock_data = [
            {
                'machine_id': row[0],
                'location': row[1],
                'product_name': row[2],
                'quantity': row[3],
                'quantity_category': row[4]
            } for row in stock_info
        ]

        # Instancia a classe Stock e aplica os filtros
        stock_instance = Stock(stock_data)
        filtered_data = stock_instance.filter_data(
            machine_id=machine_id,
            product_name=product_name,
            quantity_category=quantity_category
        )

        # Realiza a agregação nos dados filtrados usando a estratégia fornecida
        return Stock(filtered_data).aggregate(granularity, strategy)
