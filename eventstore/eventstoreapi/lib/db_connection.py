import sqlite3
import config

def connect_to_database(db_name):
    filepath = config.filepath+db_name+'.db'
    connection = sqlite3.connect(filepath)
    cursor = connection.cursor()
    return connection, cursor

def close_database(connection):
    connection.commit()
    connection.close()