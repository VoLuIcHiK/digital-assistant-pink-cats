import os
from flask import Flask, request, make_response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/api', methods=['POST'])
def handle_request():
    # get the data from the request
    file = request.files.get('file')
    text = request.form.get('text')

    # process the data (for example, send it to another server and get the response)
    # ...

    # return the response to the bot
    return {"text": "Response from the API server", "buttons_text": ["Only", "One", "Word"]}


if __name__ == '__main__':
    # get port from sys env PORT or default to 8080
    port = int(os.environ.get('PORT', 8080))
    print(f"Starting API server on port {port}...")
    app.run(host='0.0.0.0', port=port)
