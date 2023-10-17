from flask import Flask, request, jsonify

app = Flask(__name__)
data = {}

@app.route('/data', methods=['POST'])
def create_data():
    data_id = request.json.get('id')
    data_value = request.json.get('value')
    
    if data_id and data_value:
        data[data_id] = data_value
        return jsonify({'message': 'Data created successfully'}), 201
    else:
        return jsonify({'error': 'Invalid data format'}), 400
    

@app.route('/data/<data_id>', methods=['GET'])
def get_data(data_id):
    if data_id in data:
        return jsonify({'data': data[data_id]})
    else:
        return jsonify({'error': 'Data not found'}), 404

@app.route('/data/<data_id>', methods=['PUT'])
def update_data(data_id):
    data_value = request.json.get('value')
    
    if data_id in data and data_value:
        data[data_id] = data_value
        return jsonify({'message': 'Data updated successfully'}), 200
    else:
        return jsonify({'error': 'Data not found or invalid data format'}), 404

if __name__ == '__main__':
    app.run(debug=True)

