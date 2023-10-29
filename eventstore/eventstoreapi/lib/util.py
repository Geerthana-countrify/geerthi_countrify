from flask import jsonify,current_app
import uuid
from infrastructure.base import Repository
from config import db
from infrastructure.mysql import MySQLUnitOfWork
from infrastructure.sqlite import SQLiteUnitOfWork

def replay(event_id):
    try:
        db.connect()
        repo = Repository(db.connection)
        if isinstance(db, MySQLUnitOfWork):
            count = repo.get("SELECT COUNT(*) FROM eventstore WHERE event_id = %s;", (event_id,))[0]
        elif isinstance(db, SQLiteUnitOfWork):
            count = repo.get("SELECT COUNT(*) FROM eventstore WHERE event_id = ?;", (event_id,))[0]
        if count > 0:
            if isinstance(db, MySQLUnitOfWork):
                existing_data = repo.get("SELECT * FROM eventstore WHERE event_id = %s AND version = (SELECT MAX(CAST(version AS SIGNED)) FROM eventstore WHERE event_id = %s);", (event_id, event_id))
            elif isinstance(db, SQLiteUnitOfWork):
                existing_data = repo.get("SELECT * FROM eventstore WHERE event_id = ? AND version = (SELECT MAX(CAST(version AS SIGNED)) FROM eventstore WHERE event_id = ?);", (event_id, event_id))
            if existing_data:
                current_version = int(existing_data[8])
                new_version = current_version + 1
                new_event_id = str(uuid.uuid4()).replace("-", "")
                if isinstance(db, MySQLUnitOfWork):
                    insert_query = """
                INSERT INTO eventstore (
                event_id, timestamp, event_type, subdomain, userid,
                data, corelation_id, causation_id, version, process_status, trace_id
                )
                VALUES (
                %s, NOW(), %s, %s, %s,
                %s, %s, %s, %s, %s, %s
                )
                """
                elif isinstance(db, SQLiteUnitOfWork):
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
                repo.insert(insert_query, values)
                repo.commit()
                return jsonify({'message': f"Event with event_id '{new_event_id}' created sucessfully."}), 200
        else:
            return jsonify({'message': f"Event with event_id '{event_id}' does not exist."}), 404
    except Exception as e:
        return jsonify({'error': 'Database error: ' + str(e)}), 500
    finally:
        if db:
            db.disconnect()



def get_updated_event_id(event_id):
    try:
        db.connect()
        repo = Repository(db.connection)
        if isinstance(db, MySQLUnitOfWork):
            count = repo.get("SELECT COUNT(*) FROM eventstore WHERE event_id = %s;", (event_id,))[0]
        elif isinstance(db, SQLiteUnitOfWork):
            count = repo.get("SELECT COUNT(*) FROM eventstore WHERE event_id = ?;", (event_id,))[0]
        if count > 0:
            if isinstance(db, MySQLUnitOfWork):
                row = repo.get("SELECT * FROM eventstore WHERE event_id = %s AND version = (SELECT MAX(CAST(version AS SIGNED)) FROM eventstore WHERE event_id = %s);", (event_id, event_id))
            elif isinstance(db, SQLiteUnitOfWork):
                row = repo.get("SELECT * FROM eventstore WHERE event_id = ? AND version = (SELECT MAX(CAST(version AS SIGNED)) FROM eventstore WHERE event_id = ?);", (event_id, event_id))
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
    except Exception as e:
        return jsonify({'error': 'Database error: ' + str(e)}), 500
    finally:
        db.disconnect()
    return jsonify(event_data)
