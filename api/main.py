import http.client
import os
import re

from flask import Flask, request, Response
from flask_cors import CORS

from audio2text_new import get_text
from text_process import web_bot

app = Flask(__name__)
CORS(app)


def get_notifications_to_user(user_id):
    return [{"id": 1, "text": "Вы не закончили форму"},
            {"id": 2, "text": "Скоро закрывается форма для регистрации соревнования"}]


def union_article_and_url(article: str, url: str) -> str:
    return f"<a href='{url}' target='_blank'>{article}</a>"

@app.route('/api', methods=['POST'])
def handle_request():
    # get the data from the request
    file = request.files.get('file')
    text = request.form.get('text')
    is_web = request.values.get('is_web', False)

    from_url = request.form.get('from_url')
    # process the data (for example, send it to another server and get the response)
    if text is None or len(text) == 0:
        return Response("Text is null", status=http.HTTPStatus.BAD_REQUEST)
    try:
        result = web_bot(text)
    except Exception as e:
        print(e)
        return {"text": "У меня нет идей... А ещё нейросеть упала:"+str(e)}
    if type(result) is str:
        if is_web:
            result = find_and_format_email(result)
        return {"text": result}
    if result is None:
        return {"text": "У меня нет идей... А резлуьтат нейронки ПУСТОТА???"}
    if len(result) < 1:
        return {"text": "У меня нет идей..."}
    union = result[0]
    if type(union) is not list and len(union) < 2:
        return {"text": "Проблемка... на выходе из нейронки не лист или не пара имя-ссылка"}
    if is_web:
        msg = union_article_and_url(union[0], union[1])
    else:
        msg = ' '.join(union)
    if is_web:
        msg = find_and_format_email(msg)
    return {"text": msg}
    # return the response to the bot
    return {"text": "Response from the API server", "buttons_text": ["Only", "One", "Word"]}


def find_and_format_email(msg: str) -> str:
    # Regular expression pattern for matching email addresses
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    # Find all email addresses in the string using regex
    matches = re.findall(email_pattern, msg)

    # Replace each email address with the formatted version
    for match in matches:
        msg = msg.replace(match, f'<b>{match}</b>')

    return msg


@app.route('/api/voice', methods=['POST'])
def handle_request_audio():
    # get the data from the request
    audio = request.values.get('file')

    from_url = request.form.get('from_url')
    is_web = request.values.get('is_web', False)
    # process audio to text
    text = get_text(audio)

    # process the data (for example, send it to another server and get the response)
    result = web_bot(text)
    if is_web:
        result = find_and_format_email(result)
    return {"text": ' '.join(result[0])}
    # return the response to the bot
    return {"text": "Response from the API server", "buttons_text": ["Only", "One", "Word"]}


@app.route('/api/notifications', methods=['GET'])
def handle_request_notifications():
    from_url = request.form.get('from_url')
    # process audio to text
    user_id = request.form.get('user_id')

    return {"notifications": get_notifications_to_user(user_id)}


@app.route('/api/notifications/acknowledge', methods=['POST'])
def handle_request_acknowledge_notification():
    pass

    return http.client.OK


if __name__ == '__main__':
    # get port from sys env PORT or default to 8080
    port = int(os.environ.get('PORT', 8080))
    print(f"Starting API server on port {port}...")
    app.run(host='0.0.0.0', port=port)
