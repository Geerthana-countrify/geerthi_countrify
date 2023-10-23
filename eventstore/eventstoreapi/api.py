from flask import Flask, request, jsonify, Blueprint
import sqlite3
from lib import util
import db_connection
app = Flask(__name__)
app_blueprints = Blueprint('app_routes' ,__name__)

@app_blueprints.route('/<event_id>', methods=['GET'])
def get_updated_event_id(event_id):
    try:
        connection, cursor = db_connection.connect_to_database('eventstore')
        cursor.execute("SELECT COUNT(*) FROM eventstore WHERE event_id = ?", (event_id,))
        count = cursor.fetchone()[0]

        if count > 0:
            new_event_id = event_id.split("-")[0]
            cursor.execute("SELECT * FROM eventstore WHERE (event_id = ? OR event_id LIKE ?) AND version = (SELECT max(cast(version as INTEGER)) FROM eventstore WHERE event_id = ? OR event_id LIKE ?);", (new_event_id, f'{new_event_id}-%', new_event_id, f'{new_event_id}-%'))
            row = cursor.fetchone()
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


@app_blueprints.route('/create_event', methods=['POST', 'PUT'])
def insert_data():
    try:
        event_id = request.json.get('event_id')
        util.replay(event_id)
        return jsonify({'message':f"Event with event_id '{event_id}' created sucessfully"}), 201  
    except Exception as e:
        return jsonify({'error': str(e)}), 500
