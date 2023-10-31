from infrastructure.mysql import MySQLUnitOfWork
from infrastructure.sqlite import SQLiteUnitOfWork

db = MySQLUnitOfWork('localhost', 'root', 'Gathu@01', 'countrify_practice')

# db = SQLiteUnitOfWork(path = "/home/geerthikumar/countrify/var/" , db_name = 'eventstore')




