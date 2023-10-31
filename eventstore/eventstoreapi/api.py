from flask import Flask, request, jsonify
from lib import util
from config import db
app = Flask(__name__)

@app.route('/<event_id>', methods=['GET'])
def get_data(event_id):
    try:
        return util.get_updated_event_id(event_id,db)    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/create_event', methods=['POST', 'PUT'])
def insert_data():
    try:
        event_id = request.json.get('event_id')
        return util.replay(event_id,db)  
    except Exception as e:
        return jsonify({'error': str(e)}), 500
