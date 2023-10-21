import sqlite3
import uuid
import config
filepath = config.filepath


def replay(event_id):
    connection = sqlite3.connect(filepath)
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM eventstore WHERE event_id = ?", (event_id,))
    count = cursor.fetchone()[0]
    print(count)

    if count > 0:
        cursor.execute("SELECT * FROM eventstore WHERE event_id = ?", (event_id,))
        existing_data = cursor.fetchone()
        current_version = int(existing_data[8])
        new_version = current_version + 1
        new_event_id = str(uuid.uuid4())
        insert_query = """
        INSERT INTO eventstore (
            event_id, timestamp, event_type, subdomain, userid,
            data, corelation_id, causation_id, version, process_status, trace_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        values = (
            new_event_id, existing_data[1], existing_data[2], existing_data[3],
            existing_data[4], existing_data[5], existing_data[6],
            existing_data[7], str(new_version), "N", existing_data[10]
        )
        cursor.execute(insert_query, values)
    else:
        print(f"Event with event_id '{event_id}' does not exist.")
    connection.commit()
    cursor.close()
    connection.close()
replay("event1")
