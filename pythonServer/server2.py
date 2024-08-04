from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Výchozí hodnoty status kódu a zprávy
state = {
    'status_code': 200,
    'message': 'OK'
}

# Definice pevného názvu serveru
FIXED_NAME = "Server 1"


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


@app.route('/', methods=['GET'])
def get_state_html():
    html_template = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Status Page</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background-color: #f4f4f4;
            }
            .card {
                background: #fff;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                max-width: 400px;
                padding: 20px;
                text-align: center;
                border: 1px solid #ddd;
            }
            .card-header {
                font-size: 1.5em;
                font-weight: bold;
                margin-bottom: 10px;
                border-bottom: 1px solid #ddd;
                padding-bottom: 10px;
            }
            .card-body {
                margin-top: 20px;
            }
            .status-code {
                font-size: 1.2em;
                margin: 10px 0;
                color: #333;
            }
            .message {
                font-size: 1em;
                color: #666;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <div class="card-header">{{ fixed_name }}</div>
            <br>
            <div class="card-body">
                <div class="status-code">Status Code: {{ status_code }} </div>
                <div class="status-code">Server Message: {{ message }}</div>

            </div>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html_template, fixed_name=FIXED_NAME, status_code=state['status_code'],
                                  message=state['message'])


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Run a simple Flask server.')
    parser.add_argument('--port', type=int, default=5000, help='Port to listen on.')
    args = parser.parse_args()

    app.run(host='0.0.0.0', port=args.port)
