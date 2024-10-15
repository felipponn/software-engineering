import psycopg2
from config import config

def execute_query(query: str, args: tuple = None):
    """
    Executes a SQL query that modifies the database (e.g., INSERT, UPDATE, DELETE).

    Args:
        query (str): The SQL query to be executed.
        args (tuple, optional): Parameters to be passed into the SQL query. Default is None.

    Raises:
        Exception: Logs any database-related errors during query execution.
    """
    # Retrieve database connection parameters from the config file.
    params = config()

    # Establish a connection to the PostgreSQL database.
    connection = psycopg2.connect(**params)

    # Create a cursor object to interact with the database.
    cursor = connection.cursor()

    try:
        # Execute the SQL query with the provided arguments.
        cursor.execute(query, args)

        # Commit the transaction to confirm changes in the database.
        connection.commit()  
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        # Ensure that the cursor and connection are closed after the operation.
        cursor.close()
        connection.close()


def execute_query_fetchone(query: str, args: tuple = None):
    """
    Executes a SQL query that retrieves a single row from the database.

    Args:
        query (str): The SQL query to be executed.
        args (tuple, optional): Parameters to be passed into the SQL query. Default is None.

    Returns:
        tuple: The first row of the result set, or None if no rows are returned.

    Raises:
        Exception: Logs any database-related errors during query execution.
    """
    # Retrieve database connection parameters from the config file.
    params = config()

    # Establish a connection to the PostgreSQL database.
    connection = psycopg2.connect(**params)

    # Create a cursor object to interact with the database.
    cursor = connection.cursor()

    try:
        # Execute the SQL query with the provided arguments.
        cursor.execute(query, args)

        # Fetch a single row from the result set.
        data = cursor.fetchone()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        # Ensure that the cursor and connection are closed after the operation.
        cursor.close()
        connection.close()

        return data


def execute_query_fetchall(query: str, args: tuple = None):
    """
    Executes a SQL query that retrieves all rows from the result set.

    Args:
        query (str): The SQL query to be executed.
        args (tuple, optional): Parameters to be passed into the SQL query. Default is None.

    Returns:
        list: A list of all rows from the result set.

    Raises:
        Exception: Logs any database-related errors during query execution.
    """
    # Retrieve database connection parameters from the config file.
    params = config()

    # Establish a connection to the PostgreSQL database.
    connection = psycopg2.connect(**params)

    # Create a cursor object to interact with the database.
    cursor = connection.cursor()

    try:
        # Execute the SQL query with the provided arguments.
        cursor.execute(query, args)

        # Fetch all rows from the result set.
        data = cursor.fetchall()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        # Ensure that the cursor and connection are closed after the operation.
        cursor.close()
        connection.close()

        return data