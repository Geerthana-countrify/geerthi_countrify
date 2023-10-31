from countrifyplatform.abc.infrastructure import AbstractRepository, AbstractUnitOfWork
import sqlite3      

class SQLiteUnitOfWork(AbstractUnitOfWork):
    _instance = None
    def __new__(cls, path, db_name):
        if cls._instance is None:
            cls._instance = super(SQLiteUnitOfWork, cls).__new__(cls)
            cls._instance.connection = None
            cls._instance.path = path
            cls._instance.db_name = db_name
        if cls._instance.connection is None:
            cls._instance.connect()
        return cls._instance
    
    def __init__(self,path,db_name):
        pass

    def connect(self):
        filepath = self.path + self.db_name + '.db'
        try:
            self.connection = sqlite3.connect(filepath ,check_same_thread = False)
            print(self.connection)
        except sqlite3.Error as e:
            print("Error connecting to the database:", str(e))

    def disconnect(self):
        if self.connection:
            try:
                self.connection.close()
                self.connection = None
            except sqlite3.Error as e:
                print("Error closing the database:", str(e))

    def get_repository(self):
        return SQLiteRepository(self.connection)
    
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

class SQLiteRepository(AbstractRepository):
    def __init__(self, connection):
        self.connection = connection

    def add(self, query, value):
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
    
    def get(self, query, value):
        cursor = self.connection.cursor()
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

    def update(self, query, value):
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


    def delete(self, query, value):
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