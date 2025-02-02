"""
    отправка нотификации клиенту используя телеграмм бота

    использовать будем https://github.com/LonamiWebs/Telethon
"""

import os
from dotenv import load_dotenv
from telethon import TelegramClient, events, sync, connection
# pip install python-dotenv
# pip install Telethon

class SendNotify:

    # инициализация
    def __init__(self, namefile_env=".env"):
        dotenv_path = os.path.join(os.path.dirname(__file__), namefile_env)
        print((dotenv_path))
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)
        self.app_api_id = os.getenv("TLG_APP_API_ID")
        self.app_api_hash = os.getenv("TLG_APP_API_HASH")
        self.app_name = os.getenv("TLG_APP_NAME")
        self.bot_token = os.getenv("I_BOT_TOKEN")
        self.client = os.getenv("TLG_CLIENT")
        self.proxy_server = os.getenv("TLG_PROXY_SERVER")
        self.proxy_port = int(os.getenv("TLG_PROXY_PORT")) if os.getenv("TLG_PROXY_PORT") else 0
        self.proxy_key = os.getenv("TLG_PROXY_KEY")

        if self.proxy_server is None or self.proxy_port is None or self.proxy_key is None:
            print("Нет настроек прокси сервера телеграмма")
            self._tlg = TelegramClient(self.app_name, self.app_api_id, self.app_api_hash)
            self._tlg.start(bot_token=self.bot_token)
        else:
            proxy = (self.proxy_server, self.proxy_port, self.proxy_key)
            self._tlg = TelegramClient(self.app_name, self.app_api_id, self.app_api_hash,
                                       connection=connection.ConnectionTcpMTProxyRandomizedIntermediate,
                                       proxy=proxy)
            self._tlg.start(bot_token=self.bot_token)

    # добавление клиента которому нужно отправлять нотификации
    def add_clent(self, event):
        pass

    # отправка всем клиентам сообщения msg
    def send_msg(self, msg):
        self._tlg.send_message(self.client, msg)


if __name__ == "__main__":
    tlg = SendNotify()    
    print(tlg.send_msg("привет!"))
    
