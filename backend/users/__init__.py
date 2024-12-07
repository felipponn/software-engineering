from abc import ABC, abstractmethod
class UserFactory(ABC):
    """
    Abstract Factory class to define the interface for creating users.
    """
    @abstractmethod
    def create_user(self, user_name, password, email, phone, role, user_id=None, favorite_machines=[]):
        pass

    @abstractmethod
    def authenticate(self, email, password):
        pass
    
    @abstractmethod
    def _fetch_user_data(self):
        pass


class AbstractUser(ABC):
    @abstractmethod
    def __init__(self):
        super().__init__()
    
    @abstractmethod
    def save_db(self):
        pass


