import psycopg2
from config import config


def connect(file_path):
    connection = None

    with open(file_path, 'r') as file:
        file_content = file.read()

    try:    
        params = config()
        print('Connecting to the postgreSQL database ...')
        connection = psycopg2.connect(**params)

        crsr = connection.cursor()
        crsr.execute(file_content) # executes the sql query
        feeback = crsr.fetchall()
        print(feeback)
        connection.commit() # confirms the cange on the database
        crsr.close()

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection != None:
            connection.close()
            print("Database connection terminated")