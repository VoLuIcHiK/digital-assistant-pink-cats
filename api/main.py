import os
from http.client import BAD_REQUEST

from flask import Flask, request, make_response
from flask_cors import CORS

from api.audio2text import get_text
from api.text_processing import web_bot

app = Flask(__name__)
CORS(app)


def get_notifications_to_user(user_id):
    return [{"id": 1, "text": "Вы не закончили форму"},
            {"id": 2, "text": "Скоро закрывается форма для регистрации соревнования"}]


@app.route('/api', methods=['POST'])
def handle_request():
    # get the data from the request
    file = request.files.get('file')
    text = request.form.get('text')

    from_url = request.form.get('from_url')
    # process the data (for example, send it to another server and get the response)
    result = web_bot(text)
    return {"text": ' '.join(result[0])}
    # return the response to the bot
    return {"text": "Response from the API server", "buttons_text": ["Only", "One", "Word"]}


@app.route('/api/voice', methods=['POST'])
def handle_request_audio():
    # get the data from the request
    audio = request.values.get('file')

    from_url = request.form.get('from_url')
    # process audio to text
    text = get_text()

    # process the data (for example, send it to another server and get the response)
    result = web_bot(text)
    return {"text": ' '.join(result[0])}
    # return the response to the bot
    return {"text": "Response from the API server", "buttons_text": ["Only", "One", "Word"]}


@app.route('/api/notifications', methods=['GET'])
def handle_request_notifications():
    from_url = request.form.get('from_url')
    # process audio to text
    user_id = request.form.get('user_id')

    return {"notifications": get_notifications_to_user(user_id)}


@app.route('/api/notifications', methods=['GET'])
def handle_request_notifications():
    from_url = request.form.get('from_url')
    # process audio to text
    user_id = request.form.get('user_id')

    return {"notifications": get_notifications_to_user(user_id)}


if __name__ == '__main__':
    # get port from sys env PORT or default to 8080
    port = int(os.environ.get('PORT', 8080))
    print(f"Starting API server on port {port}...")
    app.run(host='0.0.0.0', port=port)
