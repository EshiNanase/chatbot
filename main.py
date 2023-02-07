import time
import requests
import telegram
import os
import dotenv


def main() -> None:
    dotenv.load_dotenv()

    url_lp = 'https://dvmn.org/api/long_polling/'
    token_devman = os.environ['TOKEN_DEVMAN']
    headers = {
        'Authorization': token_devman
    }
    timestamp = 1675747546.087695
    payload = {'timestamp': timestamp}

    token_tg = os.environ['TOKEN_TG']

    bot = telegram.Bot(token=token_tg)
    chat_id = os.environ['CHAT_ID']

    while True:
        try:
            response = requests.get(url_lp, headers=headers, params=payload)
            response = response.json()

            if response['status'] == 'found':
                text = f'Преподаватель проверил: "{response["new_attempts"][0]["lesson_title"]}"\n' \
                       f'{response["new_attempts"][0]["lesson_url"]}\n\n'
                if response["new_attempts"][0]["is_negative"] is False:
                    text += 'Ноль ошибок, едем дальше!'
                else:
                    text += 'Правь код, позорник'
                bot.send_message(chat_id=chat_id, text=text)
                payload = {'timestamp': response['last_attempt_timestamp']}
            else:
                bot.send_message(chat_id=chat_id, text='Ничего :(')
                payload = {'timestamp': response['timestamp_to_request']}

        except requests.exceptions.ReadTimeout:
            time.sleep(5)
        except requests.exceptions.ConnectionError:
            time.sleep(5)


if __name__ == "__main__":
    main()
