# # file for sqlite3 database
# import sqlite3

# class DatabaseConnection:
#     _instance = None

#     def __new__(cls, path, db_name):
#         if cls._instance is None:
#             cls._instance = super(DatabaseConnection, cls).__new__(cls)
#             cls._instance.connection = None
#             cls._instance.cursor = None
#             cls._instance.path = path
#             cls._instance.db_name = db_name
#         if cls._instance.connection is None:
#             cls._instance.connect_to_database()
#         return cls._instance

#     def connect_to_database(self):
#         filepath = self.path + self.db_name + '.db'
#         try:
#             self.connection = sqlite3.connect(filepath)
#             self.cursor = self.connection.cursor()
#         except sqlite3.Error as e:
#             print("Error connecting to the database:", str(e))

#     def execute_query(self, query, params=None):
#         try:
#             if self.connection is None:
#                 self.connect_to_database()
#             if params:
#                 self.cursor.execute(query, params)
#             else:
#                 self.cursor.execute(query)
#             return self.cursor.fetchone()
#         except sqlite3.Error as e:
#             print("Error executing query:", str(e))
#             return None

#     def insert_data(self, query, params=None):
#         try:
#             if self.connection is None:
#                 self.connect_to_database()
#             if params:
#                 self.cursor.execute(query, params)
#         except sqlite3.Error as e:
#             print("Error inserting data:", str(e))

#     def close_database(self):
#         if self.connection:
#             try:
#                 self.connection.commit()
#                 self.connection.close()
#                 self.connection = None
#                 self.cursor = None
#             except sqlite3.Error as e:
#                 print("Error closing the database:", str(e))

