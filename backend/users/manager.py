
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.connect_db import Database
from datetime import datetime
from backend.users import UserFactory, AbstractUser


class ManagerFactory(UserFactory):
    """
    Factory for creating managers.
    """
    def create_user(self, user_name, password, email, phone, user_id=None, favorite_machines=[], role = None):
        return Manager(user_name, password, email, phone, user_id, favorite_machines, role)

    def authenticate(self, email, password):
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
        user_data = self._fetch_user_data(email)
        if user_data and user_data['password'] == password:
            print(f"Manager {user_data['name']} successfully logged in!")
            favorite_machines = self._fetch_favorite_machines(user_data['user_id'])
            return self.create_user(
                user_data['name'], password, user_data['email'], 
                user_data['phone'], user_data['user_id'], favorite_machines, user_data['role']
            )
        return None

    def _fetch_user_data(self, email):
        db = Database()
        query = """
            SELECT user_id, name, email, password, phone_number, role
            FROM users 
            WHERE email = %s;
        """
        result = db.execute_query_fetchone(query, (email,))
        if result:
            return dict(zip(['user_id', 'name', 'email', 'password', 'phone', 'role'], result))
        return None

    def _fetch_favorite_machines(self, user_id):
        db = Database()
        query = """
            SELECT machine_id FROM User_Selected_Machines WHERE user_id = %s;
        """
        rows = db.execute_query_fetchall(query, (user_id,))
        return [row[0] for row in rows] if rows else []



class Manager(AbstractUser):
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
    - view_all_issues(self, issue=None, machine=None, type=None, description=None
        Fetches all reported issues from the database based on optional filters for issue, machine, type, and description.
        Returns a list of dictionaries representing the issues.
    """
    def __init__(self, user_name: str, password: str, email: str, phone: str, user_id=None, favorite_machines=[], role = None):
        self.user_name = user_name
        self.password = password
        self.email = email
        self.phone = phone
        self.user_id = user_id
        self.favorite_machines = favorite_machines
        self.role = role

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

        self.role = 'manager'
        
        # Executes the query and assigns the returned user_id to the user instance
        self.user_id = db.execute_query_fetchone(query, (self.user_name, self.email, self.phone, self.password), True)[0]

    @staticmethod
    def view_all_issues(issue=None, machine=None, type=None, status=None):
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

    def get_stock(self, machine_id=None, product_name=None, quantity_category=None):
        """
        Fetches the stock information for a specific machine or product. If no filters are provided, fetches all stock information.
        
        Parameters:
        ----------
        machine_id : str or None
            The machine_id to filter the stock information.
        product_name : str or None
            The product_name to filter the stock information.
        quantity_category : str or None
            The quantity_category to filter the stock information.

        Returns:
        -------
        list:
            Returns a list of dictionaries representing the stock information.
        """
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
            WHERE 
                (machine_id = %s OR %s IS NULL)
                AND (quantity_category = %s OR %s IS NULL)
                AND (product_name = %s OR %s IS NULL)
            ORDER BY 
                quantity ASC;
        """
        
        stock_info = db.execute_query_fetchall(query, (machine_id, machine_id, quantity_category, quantity_category, product_name, product_name))

        return [
            {
                'machine_id': row[0],
                'location': row[1],
                'product_name': row[2],
                'quantity': row[3],
                'quantity_category': row[4]
            } for row in stock_info
        ]

    def add_favorite(self, machine_id):
        """
        Adds a machine to the user's favorites.

        Parameters:
        ----------
        machine_id : int
            The ID of the machine to be added to favorites.

        Returns:
        -------
        bool
            Returns True if the operation is successful, False otherwise.
        """
        if machine_id in self.favorite_machines:
            print("Machine already in favorites.")
            return False
        db = Database()
        query = """
                INSERT INTO User_Selected_Machines (user_id, machine_id)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING;
                """
        try:
            db.execute_query(query, (self.user_id, machine_id))
            self.favorite_machines.append(machine_id)
            print("Machine added to favorites successfully.")
            return True
        except Exception as e:
            print(f"Error adding favorite: {e}")
            return False
        
    def remove_favorite(self, machine_id):
        """
        Remove a machine from the user's favorites.

        Parameters:
        ----------
        machine_id : int
            The ID of the machine to be removed from favorites.

        Returns:
        --------
        bool
            Returns True if the operation is successful, False otherwise.
        """
        if machine_id not in self.favorite_machines:
            print("Machine not in favorites.")
            return False
        db = Database()
        query = """
                DELETE FROM User_Selected_Machines
                WHERE user_id = %s AND machine_id = %s;
                """
        try:
            db.execute_query(query, (self.user_id, machine_id))
            self.favorite_machines.remove(machine_id)
            print("Machine removed from favorites successfully.")
            return True
        except Exception as e:
            print(f"Error removing favorite: {e}")
            return False
    
    def is_favorite(self, machine_id):
        """
        Checks if a specific machine is in the user's list of favorite machines.

        Parameters:
        ----------
        machine_id : int
            The ID of the machine to check.

        Returns:
        -------
        bool
            Returns True if the machine is a favorite, False otherwise.
        """
        return machine_id in self.favorite_machines


    def report(self, target, type, machine_id=None, message=None):
        """
        Submits a user report (e.g., for a machine or the app).

        Parameters:
        ----------
        target : str
            The target of the report (e.g., "Machine", "App").
        type : str
            The type of issue being reported (e.g., "Broken Machine", "App Bug").
        machine_id : str, optional
            The ID of the machine being reported (default is None if not applicable).
        message : str, optional
            Additional information or description of the issue (default is None).
        """
        db = Database()
        query = """
                INSERT INTO User_Reports (user_id, machine_id, report_target, issue_type, description)
                VALUES (%s, %s, %s, %s, %s)
                """
        # Inserts the user report into the User_Reports table
        if machine_id:
            query = """
                INSERT INTO User_Reports (user_id, machine_id, report_target, issue_type, description)
                VALUES (%s, %s, %s, %s, %s)
                """
            db.execute_query(query, (self.user_id, machine_id, target, type, message))
        else:
            query = """
                INSERT INTO User_Reports (user_id, report_target, issue_type, description)
                VALUES (%s, %s, %s, %s)
                """
            db.execute_query(query, (self.user_id, target, type, message))