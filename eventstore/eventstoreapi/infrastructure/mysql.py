from countrifyplatform.abc.infrastructure import AbstractRepository, AbstractUnitOfWork
import mysql.connector

class MySQLUnitOfWork(AbstractUnitOfWork):
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
        return cls._instance
    
    def __init__(self,host, user, password, database):
        pass
    
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

    def get_repository(self):
        return MySQLRepository(self.connection)
    
    def commit(self):
        self.connection.commit()
        pass
    def rollback(self):
        self.connection.rollback()
        pass 

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is not None:
            self.rollback() 
        else:
            self.commit()
        self.disconnect()
 


class MySQLRepository(AbstractRepository):
    def __init__(self, connection):
        self.connection = connection

    def add(self, query, value=None):
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
