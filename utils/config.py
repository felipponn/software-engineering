from configparser import ConfigParser

def config(filename="config/database.ini", section="postgresql"):
    """
    Reads the database configuration from the provided .ini file and returns the parameters as a dictionary.

    Args:
        filename (str): The path to the .ini configuration file. Default is "config/database.ini".
        section (str): The section in the .ini file that contains the database connection details. Default is "postgresql".

    Returns:
        dict: A dictionary containing the database connection parameters such as host, database, user, and password.

    Raises:
        Exception: If the specified section is not found in the .ini file.
    """
    # Create a ConfigParser instance to read the .ini file.
    parser = ConfigParser()
    
    # Read the configuration file.
    parser.read(filename)
    
    # Initialize an empty dictionary to hold the database connection parameters.
    db = {}
    
    # Check if the specified section exists in the .ini file.
    if parser.has_section(section):
        # Retrieve the key-value pairs from the section and store them in the dictionary.
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        # Raise an exception if the section is not found in the file.
        raise Exception(f'Section {section} is not found in the {filename} file.')
    
    # Return the dictionary containing the database connection parameters.
    return db