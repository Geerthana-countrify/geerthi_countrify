from infrastructure.base import UnitOfWork, Repository
import sqlite3      

class SQLiteUnitOfWork(UnitOfWork):
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
