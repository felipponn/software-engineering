from ..utils.connect_db import execute_query, execute_query_fetchone

class User():
    def __init__(self, user_name, password, email, phone, user_id = None):
        self.user_name = user_name
        self.password = password
        self.email = email
        self.phone = phone
        self.user_id = user_id

    def save_db(self):
        """
        Saves a User (signs up) to the database
        """
        query = """
                INSERT INTO Users (name, email, phone_number, role)
                VALUES (%s, '%s', '%s', 'customer')
                RETURNING user_id;
                """
        
        self.user_id = execute_query_fetchone(query, (self.user_name, self.email, self.password))[0]


    @staticmethod
    def authenticate(email, password):
        """
        Authenticates if a user is in the database checking its email and password, creates a user if True.
        """
        query = """
                SELECT user_id, name, email, password, phone_number
                FROM users 
                WHERE email = %s;
            """
        user_data = execute_query_fetchone(query, (email,))

        if user_data:
            user_id, user_name, email, correct_password, phone = user_data

            if correct_password == password: # checks if the password is correct, if true creates a object User
                print(f"User {user_name} successfully logged!")
                user = User(user_name, password, email, phone)
                return user
            
            else:
                print("Incorrect password!")
        else:
            print("User not found!")


    def report(self, target, type, machine_id = None, message = None):
        query = """
                INSERT INTO User_Reports (user_id, machine_id, report_target, issue_type, description)
                VALUES (%s, %s, %s, %s, %s)
                """
        execute_query(query, (self.user_id, machine_id, target, type, message))
        