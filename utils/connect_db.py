import psycopg2
from utils.config import config

def execute_query(query: str, args: tuple = None):
    params = config()
    connection = psycopg2.connect(**params)
    cursor = connection.cursor()
    try:
        cursor.execute(query, args)
        connection.commit() # confirms the change on the database

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        cursor.close()
        connection.close()


def execute_query_fetchone(query: str, args: tuple = None, commit = False):
    params = config()
    connection = psycopg2.connect(**params)
    cursor = connection.cursor()
    try:
        cursor.execute(query, args)
        data = cursor.fetchone()
        if commit:
            connection.commit()
        
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        cursor.close()
        connection.close()
        return data

def execute_query_fetchall(query: str, args: tuple = None, commit = False):
    params = config()
    connection = psycopg2.connect(**params)
    cursor = connection.cursor()
    try:
        cursor.execute(query, args)
        data = cursor.fetchall()
        if commit:
            connection.commit()
        
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        cursor.close()
        connection.close()
        return data