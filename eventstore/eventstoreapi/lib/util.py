from flask import jsonify, current_app
import uuid
import sqlite3
from lib import db_connection

def replay(event_id):
    filepath = current_app.config['filepath'] 
    try:
        connection, cursor = db_connection.connect_to_database(filepath , 'eventstore')
        count = db_connection.execute_query(cursor,"SELECT COUNT(*) FROM eventstore WHERE event_id = ?", (event_id,))[0]

        if count > 0:
            existing_data = db_connection.execute_query(cursor,"SELECT * FROM eventstore WHERE (event_id = ? ) AND version = (SELECT max(cast(version as INTEGER)) FROM eventstore WHERE event_id = ? );", (event_id, event_id,))
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
            db_connection.insert_data(cursor, insert_query, values)
            db_connection.close_database(connection)
            
        else:
            return jsonify({'message': f"Event with event_id '{event_id}' does not exist."}), 404
        
    except sqlite3.Error as e:
        return jsonify({'error': 'Database error'}), 500
    

def get_updated_event_id(event_id):
    filepath = current_app.config['filepath'] 
    try:
        connection, cursor = db_connection.connect_to_database(filepath ,'eventstore')
        count = db_connection.execute_query(cursor, "SELECT COUNT(*) FROM eventstore WHERE event_id = ?", (event_id,))[0]
        if count > 0:
            row = db_connection.execute_query(cursor,"SELECT * FROM eventstore WHERE (event_id = ? ) AND version = (SELECT max(cast(version as INTEGER)) FROM eventstore WHERE event_id = ? );", (event_id, event_id,))
            event_data = {
                "event_id": row[0],
                "timestamp": row[1],
                "event_type": row[2],
                "subdomain": row[3],
                "userid": row[4],
                "data": row[5],
                "corelation_id": row[6],
                "causation_id": row[7],
                "version": row[8],
                "process_status": row[9],
                "trace_id": row[10]
            }
        else:
            event_data = {}
    except sqlite3.Error as e:
        event_data = {"error": "Database error"}
    finally:
        if connection:
            db_connection.close_database(connection)
    return jsonify(event_data)

