from flask import Flask, request, jsonify
import sqlite3
import uuid

filepath = "/home/geerthikumar/countrify/var/eventstore.db"

app = Flask(__name__)

def replay(event_id):
    try:
        connection = sqlite3.connect(filepath)
        cursor = connection.cursor()
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

            connection.commit()
            cursor.close()
            connection.close()
            
        else:
            return jsonify({'message': f"Event with event_id '{event_id}' does not exist."}), 404
        
    except sqlite3.Error as e:
        return jsonify({'error': 'Database error'}), 500


@app.route('/<event_id>', methods=['GET'])
def get_updated_event_id(event_id):
    try:
        connection = sqlite3.connect(filepath)
        cursor = connection.cursor()
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
        cursor.close()
        connection.close()

    return jsonify(event_data)


@app.route('/create_event', methods=['POST', 'PUT'])
def insert_data():
    try:
        event_id = request.json.get('event_id')
        replay(event_id)
        return jsonify({'message':f"Event with event_id '{event_id}' created sucessfully"}), 201  
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
