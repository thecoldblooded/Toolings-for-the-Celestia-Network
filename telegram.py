import os
import urllib.parse
import requests

from custom_logging import logger
from constants import API_TOKEN, CHAT_ID


class TelegramNotification:

    def __init__(self):
        self.notifies = []
        self.api_token = API_TOKEN
        self.chat_id = CHAT_ID

    def __del__(self):
        self.flush()

    def append_message(self, message):
        self.notifies.append(message)

    def send(self, message):
        logger.info(f'Send message: {message}')
        url = f'https://api.telegram.org/bot{self.api_token}/sendMessage?text={message}&chat_id={self.chat_id}'
        response = requests.get(url)
        logger.info(f'Response: {response.json()}')

    def flush(self):
        if len(self.notifies) > 0:
            messages = '\n'.join(self.notifies)
            self.send(urllib.parse.quote(messages))
            self.notifies = []
