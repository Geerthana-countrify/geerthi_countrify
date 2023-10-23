from flask import Flask, request, jsonify, current_app
from lib import util
app = Flask(__name__)

@app.route('/<event_id>', methods=['GET'])
def get_data(event_id):
    try:
        return util.get_updated_event_id(event_id)    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/create_event', methods=['POST', 'PUT'])
def insert_data():
    try:
        event_id = request.json.get('event_id')
        util.replay(event_id)
        return jsonify({'message':f"Event with event_id '{event_id}' created sucessfully"}), 201  
    except Exception as e:
        return jsonify({'error': str(e)}), 500
