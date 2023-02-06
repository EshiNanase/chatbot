import time
import requests
import telegram
import os

from dotenv import load_dotenv
load_dotenv()

URL_REVIEWS = 'https://dvmn.org/api/user_reviews/'
URL_LP = 'https://dvmn.org/api/long_polling/'
TOKEN_DEVMAN = os.environ['TOKEN_DEVMAN']
HEADERS = {
    'Authorization': TOKEN_DEVMAN
}
TIMESTAMP = 0
PAYLOAD = {'timestamp': TIMESTAMP}

TOKEN_TG = os.environ['TOKEN_TG']

bot = telegram.Bot(token=TOKEN_TG)
CHAT_ID = bot.get_updates()[-1].message.chat_id

while True:
    try:
        print('Making a request...')
        requests.get(URL_REVIEWS, headers=HEADERS)
        print('Success!\n')
        response = requests.get(URL_LP, headers=HEADERS, params=PAYLOAD).json()

        if response['status'] == 'found':
            text = f'Преподаватель проверил: "{response["new_attempts"][0]["lesson_title"]}"\n' \
                   f'{response["new_attempts"][0]["lesson_url"]}\n\n'
            if response["new_attempts"][0]["is_negative"] is True:
                text += 'Ноль ошибок, едем дальше!'
            else:
                text += 'Правь код, позорник'
            bot.send_message(chat_id=CHAT_ID, text=text)
            break
        else:
            bot.send_message(chat_id=CHAT_ID, text='Ничего :(')
            TIMESTAMP = response['timestamp_to_request']

    except requests.exceptions.ReadTimeout:
        print('ReadTimeout\n')
        time.sleep(5)
    except requests.exceptions.ConnectionError:
        print('No internet connection!\n')
        time.sleep(5)
