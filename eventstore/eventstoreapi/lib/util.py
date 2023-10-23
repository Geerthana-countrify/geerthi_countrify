from flask import jsonify
import config
filepath = config.filepath
import uuid
import sqlite3
import db_connection
def replay(event_id):
    try:
        connection, cursor = db_connection.connect_to_database('eventstore')
        cursor.execute("SELECT COUNT(*) FROM eventstore WHERE event_id = ?", (event_id,))
        count = cursor.fetchone()[0]

        if count > 0:
            cursor.execute("SELECT * FROM eventstore WHERE (event_id = ? ) AND version = (SELECT max(cast(version as INTEGER)) FROM eventstore WHERE event_id = ? );", (event_id, event_id,))
            existing_data = cursor.fetchone()
            current_version = int(existing_data[8])
            new_version = current_version + 1
            new_event_id = str(uuid.uuid4()).replace("-", "")
            insert_query = """
            INSERT INTO eventstore (
                event_id, timestamp, event_type, subdomain, userid,
                data, corelation_id, causation_id, version, process_status, trace_id
            )
            VALUES (?, DATETIME('now'), ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            values = (
                new_event_id, existing_data[2], existing_data[3],
                existing_data[4], existing_data[5], existing_data[6],
                existing_data[7], str(new_version), "N", existing_data[10]
            )
            cursor.execute(insert_query, values)
            db_connection.close_database(connection)
            
        else:
            return jsonify({'message': f"Event with event_id '{event_id}' does not exist."}), 404
        
    except sqlite3.Error as e:
        return jsonify({'error': 'Database error'}), 500
