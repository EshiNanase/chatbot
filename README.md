# Devman Notifications Telegram Bot

Telegram bot specifically for notifying if my homework on devman.org is checked

## Prerequisites

Virtual environment needs to be:

```
python==3.10
```
## Installing

First, you need to clone the code:

```
git clone https://github.com/EshiNanase/chatbot.git
```
Second, you need to install requirements.txt:

```
pip install -r requirements.txt
```
## Environment variables

The code needs .env file with such environment variables as:

```
DEVMAN_TOKEN = you can find it here https://dvmn.org/api/docs/
TELEGRAM_TOKEN = token of your Telegram bot, text https://t.me/BotFather to create one
TELEGRAM_CHAT_ID = you can find it here https://t.me/userinfobot
```
## Running

The code should be ran in cmd like so:

```
python main.py
```
Then type /start to created bot and wait till your homework is checked

