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

import pandas as pd

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


def currency_exchange_rate(currency_from, currency_to):

    #currency_from = "USD"
    #currency_to = "RUB"
    filename = f"currency_exchange_rate_{currency_from}_{currency_to}.json"

    urls = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={currency_from}&" \
        f"to_currency={currency_to}&apikey={api_key}"

    session = requests.Session()    
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

    return msg_txt

def fx_intraday(currency_from, currency_to, interval = "15min", outputsize="compact"):

    filename = f"last_{currency_from}_{currency_to}.json"

    urls = f"https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol={currency_from}&" \
        f"to_symbol={currency_to}&interval={interval}&outputsize={outputsize}&apikey={api_key}"

    session = requests.Session()    
    r = session.get(urls)
    print(r.status_code)

    if (r.status_code == 200):
        # print(r.headers)
        #print(r.content)

        data_currency_now = r.json()
    
    data_currency_last = None

    try:
        # read data from json file
        data_currency_last = json.load(open(filename))
    except FileNotFoundError:
        print(f"Нет файла {filename}. Возможно это первый запуск программы.")

    #print(data_currency_last)

    # TEST string
    #data_currency_now = data_currency_last
    #print(data_currency_now)
    

    if data_currency_last is not None:
        # сравнение текущей цены с последней сохраненной
        pass

    # save json into file
    json.dump(data_currency_now, open(filename, "w"))
    #print(data_currency_now)

    msg_txt = "None"

    
    data_curr_meta = data_currency_now["Meta Data"]
    data_curr_timeseries = data_currency_now["Time Series FX (15min)"]

    df_curr_timeseries = pd.DataFrame(data_curr_timeseries)

    df_curr_timeseries = df_curr_timeseries.T

    #print(df_curr_timeseries.head())
    print()
    last_curr = df_curr_timeseries.iloc[0]

    msg_txt = f'{data_curr_meta["1. Information"]}\n{data_curr_meta["2. From Symbol"]}->{data_curr_meta["3. To Symbol"]}\n' \
        f'open: {last_curr[0]}\nhigh: {last_curr[1]}\nlow: {last_curr[2]}\nclose: {last_curr[3]}\nTime: {last_curr.name}\n'

    return msg_txt


if __name__ =="__main__":
    tlg = SendNotify()
    
    #msg = currency_exchange_rate(currency_from="USD", currency_to="RUB")
    msg = fx_intraday(currency_from="USD", currency_to="RUB", interval = "15min", outputsize="compact")
    print(msg)
    tlg.send_msg(msg)