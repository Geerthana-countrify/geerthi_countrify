from infrastructure.mysql import MySQLUnitOfWork
from infrastructure.sqlite import SQLiteUnitOfWork

# db = MySQLUnitOfWork('localhost', 'root', 'Gathu@01', 'countrify_practice')

filepath = "/home/geerthikumar/countrify/var/"
db = SQLiteUnitOfWork(filepath, 'eventstore')



