from utils.connect_db import execute_query, execute_query_fetchone, execute_query_fetchall
from datetime import datetime

class Machine:
    """
    Machine class to represent a vending machine.
    
    Attributes:
    - machine_id: int
        The unique identifier of the machine. 
    - location: str
        The location of the machine.  
    - status: str
        The status of the machine. If the machine is operational or not.
    - last_serviced_at: datetime
        The date and time when the machine was last serviced.
    - installed_at: datetime
        The date and time when the machine was installed.
        
    Methods:
    - __init__(self, machine_id: int, location: str, products: list,
                 status: bool, last_serviced_at: datetime, installed_at: datetime)
        Constructor to initialize the Machine object.
    - get_machines()
        Static method to return a list of Machine objects from the database.
    - save_db()
        Saves a Machine to the database.
    """
    
    def __init__(self, location: str, status: str, last_serviced_at: datetime,
                 installed_at: datetime, machine_id: int = None):
        """
        Constructor to initialize the Machine object.

        Attributes:
        - machine_id: int
            The unique identifier of the machine.
        - location: str
            The location of the machine.
        - status: str
            The status of the machine. If the machine is operational or not.
        - last_serviced_at: datetime
            The date and time when the machine was last serviced.
        - installed_at: datetime
            The date and time when the machine was installed.
        """
        self.machine_id = machine_id
        self.location = location
        self.status = status
        self.last_serviced_at = last_serviced_at
        self.installed_at = installed_at

    def save_db(self):
        """
        Saves the Machine to the database.
        """
        query = """
                INSERT INTO Machines (location, status, last_serviced_at, installed_at)
                VALUES (%s, %s, %s, %s)
                RETURNING machine_id;
                """
        self.machine_id = execute_query_fetchone(query, (
            self.location,
            self.status, 
            self.last_serviced_at, 
            self.installed_at
        ), True)[0]
        
    @staticmethod
    def get_machines():
        """
        Static method to return a list of Machine objects from the database.

        Returns:
        - list
            The list of Machine objects.
        """
        query = """
                SELECT machine_id, location, status, last_serviced_at, installed_at
                FROM Machines;
                """
        machines_data = execute_query_fetchall(query)
        
        machines = []
        for machine_data in machines_data:
            machine_id, location, status, last_serviced_at, installed_at = machine_data
            machines.append(Machine(
                machine_id=machine_id,
                location=location,
                status=status,
                last_serviced_at=last_serviced_at,
                installed_at=installed_at
            ))

        return machines
