from flask import Flask, request, jsonify

app = Flask(__name__)

# Výchozí hodnoty status kódu a zprávy
state = {
    'status_code': 200,
    'message': 'OK'
}


@app.route('/state', methods=['GET'])
def get_state():
    return jsonify(state), state['status_code']


@app.route('/state', methods=['POST'])
def set_state():
    data = request.json
    if 'status_code' in data and 'message' in data:
        state['status_code'] = data['status_code']
        state['message'] = data['message']
        return jsonify({"message": "State updated successfully"}), 200
    else:
        return jsonify({"error": "Invalid request. 'status_code' and 'message' are required."}), 400


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Run a simple Flask server.')
    parser.add_argument('--port', type=int, default=5000, help='Port to listen on.')
    args = parser.parse_args()

    app.run(host='0.0.0.0', port=args.port)
