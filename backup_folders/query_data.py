import sqlite3
filepath = "/home/geerthikumar/countrify/var/eventstore.db"
connection = sqlite3.connect(filepath)
cursor = connection.cursor()
# cursor.execute("SELECT COUNT(*) FROM eventstore WHERE event_id = ?", (event_id,))
new_event_id = "event1"
# cursor.execute("SELECT * FROM eventstore WHERE (event_id = ? OR event_id LIKE ?) AND version = (SELECT max(cast(version as INTEGER)) FROM eventstore WHERE event_id = ? OR event_id LIKE ?);", (new_event_id, f'{new_event_id}-%', new_event_id, f'{new_event_id}-%'))
# cursor.execute("SELECT max(cast(version as INTEGER)) FROM eventstore WHERE (event_id LIKE ?)", ('event1-%', ))
cursor.execute("DELETE FROM eventstore WHERE event_id != ? ;", (new_event_id,))
# cursor.execute("SELECT * FROM eventstore WHERE event_id not like ? ;", (f'{new_event_id}%',))
# cursor.execute("SELECT * FROM eventstore")
connection.commit()

result = cursor.fetchall()
print(result)