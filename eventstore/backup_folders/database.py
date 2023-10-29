# import mysql.connector

# class DatabaseConnection:
#     _instance = None

#     def __new__(cls, host, user, password, database):
#         if cls._instance is None:
#             cls._instance = super(DatabaseConnection, cls).__new__(cls)
#             cls._instance.connection = None
#             cls._instance.cursor = None
#             cls._instance.host = host
#             cls._instance.user = user
#             cls._instance.password = password
#             cls._instance.database = database
#         if cls._instance.connection is None:
#             cls._instance.connect_to_database()
#         return cls._instance

#     def connect_to_database(self):
#         try:
#             self.connection = mysql.connector.connect(
#                 host=self.host,
#                 user=self.user,
#                 password=self.password,
#                 database=self.database
#             )
#             self.cursor = self.connection.cursor()
#         except mysql.connector.Error as e:
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
#         except mysql.connector.Error as e:
#             print("Error executing query:", str(e))
#             return None
        

#     def insert_data(self, query, params=None):
#         try:
#             if self.connection is None:
#                 self.connect_to_database()
#             if params:
#                 self.cursor.execute(query, params)
#         except mysql.connector.Error as e:
#             print("Error inserting data:", str(e))

#     def close_database(self):
#         if self.connection:
#             try:
#                 self.connection.commit()
#                 self.cursor.close()
#                 self.connection.close()
#                 self.connection = None
#                 self.cursor = None
#             except mysql.connector.Error as e:
#                 print("Error closing the database:", str(e))
