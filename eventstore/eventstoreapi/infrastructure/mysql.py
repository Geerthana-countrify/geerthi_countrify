from infrastructure.base import UnitOfWork , Repository
import mysql.connector

class MySQLRepository(Repository):
    def __init__(self, connection):
        self.connection = connection

    def insert(self, query, value=None):
        cursor = self.connection.cursor()
        try:
            if value is None:
                cursor.execute(query)
            else:
                cursor.execute(query, value)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
        
    def update(self, query, value=None):
        cursor = self.connection.cursor()
        try:
            if value is None:
                cursor.execute(query)
            else:
                cursor.execute(query, value)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cursor.close()         
        

    def delete(self, query, value=None):
        cursor = self.connection.cursor()
        try:
            if value is None:
                cursor.execute(query)
            else:
                cursor.execute(query, value)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cursor.close()        
        

    def get(self, query, value=None):
        print(self.connection)
        cursor = self.connection.cursor()
        print(cursor)
        try:
            if value is None:
                cursor.execute(query)
            else:
                cursor.execute(query, value)
            result = cursor.fetchone()
            if result is None:
                return None
            return result
            
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            cursor.close()

    def commit(self):
        self.connection.commit()
        pass
    def rollback(self):
        self.connection.rollback()
        pass    


class MySQLUnitOfWork(UnitOfWork):
    _instance = None
    def __new__(cls, host, user, password, database):
        if cls._instance is None:
            cls._instance = super(MySQLUnitOfWork, cls).__new__(cls)
            cls._instance.connection = None
            cls._instance.cursor = None
            cls._instance.host = host
            cls._instance.user = user
            cls._instance.password = password
            cls._instance.database = database
        if cls._instance.connection is None:
            cls._instance.connect()
        return cls._instance
    
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
        except mysql.connector.Error as e:
            print("Error connecting to the database:", str(e))
    def disconnect(self):
        if self.connection:
            try:
                self.connection.close()
                self.connection = None 
            except mysql.connector.Error as e:
                print("Error closing the database:", str(e))
