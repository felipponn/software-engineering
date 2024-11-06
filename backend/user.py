from utils.connect_db import execute_query, execute_query_fetchone
class User:
    """
    A class representing a User in the system, allowing for actions like saving to the database,
    authenticating, and reporting issues.

    Attributes:
    ----------
    user_name : str
        The name of the user.
    password : str
        The user's password.
    email : str
        The user's email.
    phone : str
        The user's phone number.
    user_id : UUID or None
        The unique identifier for the user, generated after saving to the database.
    """

    def __init__(self, user_name, password, email, phone, user_id=None):
        """
        Initialize a new User instance.

        Parameters:
        ----------
        user_name : str
            The name of the user.
        password : str
            The password for the user.
        email : str
            The email for the user.
        phone : str
            The phone number for the user.
        user_id : UUID, optional
            The user's unique identifier (default is None, assigned after saving to the database).
        favorite_machines : list, optional
            List of machine_ids that the user has favorited (default is empty list).
        """
        self.user_name = user_name
        self.password = password
        self.email = email
        self.phone = phone
        self.user_id = user_id
        self.favorite_machines = []

    def save_db(self):
        """
        Saves the User to the database (used for sign-up). 

        After saving, the method sets the `user_id` by executing a query 
        to insert the user's details into the `Users` table and returning the generated `user_id`.
        """
        query = """
                INSERT INTO Users (name, email, phone_number, password, role)
                VALUES (%s, %s, %s, %s ,'customer')
                RETURNING user_id;
                """
        
        # Executes the query and assigns the returned user_id to the user instance
        self.user_id = execute_query_fetchone(query, (self.user_name, self.email, self.phone, self.password), True)[0]

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
        query = """
                SELECT user_id, name, email, password, phone_number
                FROM users 
                WHERE email = %s;
            """
        # Fetches user data from the database based on email
        user_data = execute_query_fetchone(query, (email,))

        if user_data:
            user_id, user_name, email, correct_password, phone = user_data

            # Checks if the provided password matches the stored password
            if correct_password == password:
                print(f"User {user_name} successfully logged in!")
                # Creates and returns a User object if authentication is successful
                user = User(user_name, password, email, phone, user_id=user_id)
                return user
            
            else:
                print("Incorrect password!")
        else:
            print("User not found!")

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
            execute_query(query, (self.user_id, machine_id, target, type, message))
        else:
            query = """
                INSERT INTO User_Reports (user_id, report_target, issue_type, description)
                VALUES (%s, %s, %s, %s)
                """
            execute_query(query, (self.user_id, target, type, message))
    