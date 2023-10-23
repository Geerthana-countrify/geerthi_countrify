import sqlite3

def connect_to_database(path , db_name):
    filepath = path+db_name+'.db'
    connection = sqlite3.connect(filepath)
    cursor = connection.cursor()
    return connection, cursor

def execute_query(cursor, query, params=None):
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    return cursor.fetchone()

def insert_data(cursor, query, params=None):
    if params:
        cursor.execute(query, params)
    return 

def close_database(connection):
    connection.commit()
    connection.close()