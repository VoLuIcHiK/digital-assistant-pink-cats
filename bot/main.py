import os
import requests
import telebot
import json

from telebot.types import Message

# get token from system env
token = os.environ.get('TELEGRAM_BOT_TOKEN', None)

bot = telebot.TeleBot(token)

# get api url from system env or default
api_url = os.environ.get('API_URL', 'http://192.168.0.198:8080/api')
print(f"API URL: {api_url}")

# define the handler for audio messages
@bot.message_handler(content_types=["audio"])
def handle_audio(message):
    try:
        # download the audio file from Telegram's servers
        file_info = bot.get_file(message.audio.file_id)
        file = requests.get(f'https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}').content

        # send the audio file and text message to the API server
        data = {"file": file, "text": message.caption}
        response = requests.post(api_url, data=data)

        # send the response from the API server back to the user
        bot.send_message(message.chat.id, response.text)
    except Exception as e:
        # if an exception occurs, send the problem to the chat
        bot.send_message(message.chat.id, f"Problem sending audio to API: {e}")


# define the handler for audio messages
@bot.message_handler(content_types=["voice"])
def handle_voice(message: Message):
    try:
        # download the audio file from Telegram's servers
        file_info = bot.get_file(message.voice.file_id)
        file = requests.get(f'https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}').content

        # send the audio file and text message to the API server
        data = {"file": file}
        response = requests.post(api_url+'/voice', data=data)

        # send the response from the API server back to the user
        bot.send_message(message.chat.id, response.text)
    except Exception as e:
        # if an exception occurs, send the problem to the chat
        bot.send_message(message.chat.id, f"Problem sending audio to API: {e}")



# define the handler for text messages
@bot.message_handler(content_types=["text"])
def handle_text(message):
    try:
        # send the text message to the API serverф
        data = {"text": message.text}
        response = requests.post(api_url, data=data)

        # send the response from the API server back to the user
        bot.send_message(message.chat.id, json.loads(response.text)['text'])
    except Exception as e:
        # if an exception occurs, send the problem to the chat
        bot.send_message(message.chat.id, f"Problem sending text to API: {e}")


# start the Telegram bot
bot.polling()
