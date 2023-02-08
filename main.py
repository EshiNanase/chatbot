import time
import requests
import telegram
import os
import dotenv
import logging


def main() -> None:
    dotenv.load_dotenv()

    longpolling_url = 'https://dvmn.org/api/long_polling/'
    devman_token = os.environ['DEVMAN_TOKEN']
    headers = {
        'Authorization': devman_token
    }
    timestamp = time.time()
    payload = {'timestamp': timestamp}

    telegram_token = os.environ['TELEGRAM_TOKEN']

    bot = telegram.Bot(token=telegram_token)
    telegram_chat_id = os.environ['TELEGRAM_CHAT_ID']

    class TelegramLogsHandler(logging.Handler):

        def emit(self, record):
            log_entry = self.format(record)
            bot.send_message(chat_id=telegram_chat_id, text=log_entry)

    logger = logging.getLogger('Logger')
    logger.setLevel(logging.WARNING)
    logger.addHandler(TelegramLogsHandler())
    logger.warning('Бот запущен')

    while True:
        try:
            response = requests.get(longpolling_url, headers=headers, params=payload)
            response.raise_for_status()

            reviews_information = response.json()

            if reviews_information['status'] == 'found':
                text = \
                    f'''
                    Преподаватель проверил: "{reviews_information["new_attempts"][0]["lesson_title"]}"
                    {reviews_information["new_attempts"][0]["lesson_url"]}

                    '''
                if reviews_information["new_attempts"][0]["is_negative"] is False:
                    text += 'Ноль ошибок, едем дальше!'
                else:
                    text += 'Правь код, позорник'
                bot.send_message(chat_id=telegram_chat_id, text=text)
                payload = {'timestamp': reviews_information['last_attempt_timestamp']}
            else:
                payload = {'timestamp': reviews_information['timestamp_to_request']}

        except requests.exceptions.ReadTimeout:
            text = \
                f'''
                Боту прилетело {requests.exceptions.ReadTimeout}
                '''
            logger.warning(text)
        except requests.exceptions.ConnectionError:
            text = \
                f'''
                    Боту прилетело {requests.exceptions.ConnectionError}
                '''
            logger.warning(text)
            time.sleep(10)


if __name__ == "__main__":
    main()
    logging.basicConfig(level=logging.ERROR)
    logger.setLevel(logging.DEBUG)
