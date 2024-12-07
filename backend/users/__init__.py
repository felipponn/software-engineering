from abc import ABC, abstractmethod
from utils.connect_db import Database
class UserFactory():
    """
    Abstract Factory class to define the interface for creating users.
    """
    @abstractmethod
    def create_user(self, user_name, password, email, phone, role, user_id=None, favorite_machines=[]):
        pass

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
            print(f"{user_data['name']} successfully logged in!")
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


class AbstractUser(ABC):
    @abstractmethod
    def __init__(self):
        super().__init__()
    
    @abstractmethod
    def save_db(self):
        pass


