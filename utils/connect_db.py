import psycopg2
from utils.config import config

class Database:
    """
    Singleton class to manage a PostgreSQL database connection.
    Ensures only one instance of the database connection exists.
    """

    _instance = None

    def __new__(cls):
        """
        Creates a new instance of the Database class if one does not already exist.
        """
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    

    def _initialize(self):
        """
        Initializes the database connection and cursor.
        """
        self.params = config()
        self.connection = psycopg2.connect(**self.params)
        self.cursor = self.connection.cursor()
        

    def execute_query(self, query: str, args: tuple = None):
        """
        Executes a SQL query that modifies the database (e.g., INSERT, UPDATE, DELETE).

        Args:
            query (str): The SQL query to be executed.
            args (tuple, optional): Parameters to be passed into the SQL query. Default is None.

        Raises:
            Exception: Logs any database-related errors during query execution.
        """
        try:
            # Execute the SQL query with the provided arguments.
            self.cursor.execute(query, args)

            # Commit the transaction to confirm changes in the database.
            self.connection.commit()  
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)


    def execute_query_fetchone(self, query: str, args: tuple = None, commit = False):
        """
        Executes a SQL query that retrieves a single row from the database.

        Args:
            query (str): The SQL query to be executed.
            args (tuple, optional): Parameters to be passed into the SQL query. Default is None.
            commit (bool, optional): If True, commits changes to the database. Default is False.

        Returns:
            tuple: The first row of the result set, or None if no rows are returned.

        Raises:
            Exception: Logs any database-related errors during query execution.
        """
        try:
            # Execute the SQL query with the provided arguments.
            self.cursor.execute(query, args)

            # Fetch a single row from the result set.
            data = self.cursor.fetchone()
            if commit:
                self.connection.commit()
                
            return data
            
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        

    def execute_query_fetchall(self, query: str, args: tuple = None, commit = False):
        """
        Executes a SQL query that retrieves all rows from the result set.

        Args:
            query (str): The SQL query to be executed.
            args (tuple, optional): Parameters to be passed into the SQL query. Default is None.
            commit (bool, optional): If True, commits changes to the database. Default is False.

        Returns:
            list: A list of all rows from the result set.

        Raises:
            Exception: Logs any database-related errors during query execution.
        """
        try:
            # Execute the SQL query with the provided arguments.
            self.cursor.execute(query, args)

            # Fetch all rows from the result set.
            data = self.cursor.fetchall()
            if commit:
                self.connection.commit()
                
            return data
            
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)

    def close(self):
        """
        Closes the database connection and cursor, and resets the singleton instance.
        """
        self.cursor.close()
        self.connection.close()
        Database._instance = None