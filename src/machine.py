from datetime import datetime

class Machine:
    """
    Machine class to represent a vending machine.
    
    Attributes:
    - machine_id: int
        The unique identifier of the machine. 
    - location: str
        The location of the machine. 
    - products: list
        The list of products available in the machine. 
    - status: bool
        The status of the machine. True if the machine is operational, 
        False otherwise.
    - last_serviced_at: datetime
        The date and time when the machine was last serviced.
    - installed_at: datetime
        The date and time when the machine was installed.
        
    Methods:
    - __init__(self, machine_id: int, location: str, products: list,
                 status: bool, last_serviced_at: datetime, installed_at: datetime)
        Constructor to initialize the Machine object.
    - get_machines(machines: list) -> list
        Static method to return a list of Machine objects from a list of 
        dictionaries
    """
    
    def __init__(self, machine_id: int, location: str, products: list,
                 status: bool, last_serviced_at: datetime, installed_at: datetime):
        """
        Constructor to initialize the Machine object.

        Attributes:
        - machine_id: int
            The unique identifier of the machine.
        - location: str
            The location of the machine.
        - products: list
            The list of products available in the machine.
        - status: bool
            The status of the machine. True if the machine is operational,
            False otherwise.
        - last_serviced_at: datetime
            The date and time when the machine was last serviced.
        - installed_at: datetime
            The date and time when the machine was installed.
        """
        self.machine_id = machine_id
        self.location = location
        self.products = products
        self.status = status
        self.last_serviced_at = last_serviced_at
        self.installed_at = installed_at
        
    @staticmethod
    def get_machines(machines: list):
        """
        Static method to return a list of Machine objects from a list of
        dictionaries.

        Attributes:
        - machines: list
            The list of dictionaries representing the machines.
            
        Returns:
        - list
            The list of Machine objects.
        """
        return [machine.machine_id for machine in machines]
        