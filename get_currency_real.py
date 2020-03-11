"""
 Получение валютных пар через API
 см. документацию: https://www.alphavantage.co/documentation/

https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=USD&to_currency=RUB&apikey=demo

https://www.alphavantage.co/query?function=FX_DAILY&from_symbol=EUR&to_symbol=USD&apikey=demo

"""

import os
import json
import requests
from dotenv import load_dotenv  # pip3 install python-dotenv

from telegram_notyfy import SendNotify

# from telethon import TelegramClient, events  # pip3 install Telethon

# получение данных окружения
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
# print((dotenv_path))
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
app_api_id = os.getenv("TLG_APP_API_ID")
app_api_hash = os.getenv("TLG_APP_API_HASH")
app_name = os.getenv("TLG_APP_NAME")
bot_token = os.getenv("I_BOT_TOKEN")
api_key = os.getenv("API_KEY")
# END получение данных окружения

currency_from = "USD"
currency_to = "RUB"
filename = f"last_{currency_from}_{currency_to}.json"

urls = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={currency_from}&" \
       f"to_currency={currency_to}&apikey={api_key}"


tlg = SendNotify()


session = requests.Session()
# session.auth = HttpNtlmAuth(user_auth, passw_auth)
r = session.get(urls)
print(r.status_code)

if (r.status_code == 200):
    # print(r.headers)
    print(r.content)

    data_currency_now = r.json()


data_currency_last = None

try:
    # read data from json file
    data_currency_last = json.load(open(filename))
except FileNotFoundError:
    print(f"Нет файла {filename}. Возможно это первый запуск программы.")

#print(data_currency_last)

# TEST string
"""
data_currency_now = {'Realtime Currency Exchange Rate':
                 {'1. From_Currency Code': 'USD',
                  '2. From_Currency Name': 'United States Dollar',
                  '3. To_Currency Code': 'RUB',
                  '4. To_Currency Name': 'Russian Ruble',
                  '5. Exchange Rate': '72.02800000',
                  '6. Last Refreshed': '2020-03-11 20:38:02',
                  '7. Time Zone': 'UTC',
                  '8. Bid Price': '72.01800000',
                  '9. Ask Price': '72.03800000'
                  }
                     }
"""

if data_currency_last is not None:
    # сравнение текущей цены с последней сохраненной
    pass

# save json into file
json.dump(data_currency_now, open(filename, "w"))
#print(data_currency_now)

data_curr = data_currency_now["Realtime Currency Exchange Rate"]

msg_txt = f"{data_curr['1. From_Currency Code']}->{data_curr['3. To_Currency Code']}\n" \
    f"Exchage Rate: {data_curr['5. Exchange Rate']}\n" \
    f"Time: {data_curr['6. Last Refreshed']} {data_curr['7. Time Zone']}"

tlg.send_msg(msg_txt)
