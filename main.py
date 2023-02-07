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
            response.raise_for_status()

            response_jsoned = response.json()
            if 'error' in response_jsoned:
                raise requests.exceptions.HTTPError(response_jsoned['error'])

            if response_jsoned['status'] == 'found':
                text = \
                    f'''
                    Преподаватель проверил: "{response_jsoned["new_attempts"][0]["lesson_title"]}"
                    {response_jsoned["new_attempts"][0]["lesson_url"]}
                    
                    '''
                if response_jsoned["new_attempts"][0]["is_negative"] is False:
                    text += 'Ноль ошибок, едем дальше!'
                else:
                    text += 'Правь код, позорник'
                bot.send_message(chat_id=chat_id, text=text)
                payload = {'timestamp': response_jsoned['last_attempt_timestamp']}
            else:
                bot.send_message(chat_id=chat_id, text='Ничего :(')
                payload = {'timestamp': response_jsoned['timestamp_to_request']}

        except requests.exceptions.ReadTimeout:
            pass
        except requests.exceptions.ConnectionError:
            time.sleep(10)


if __name__ == "__main__":
    main()
