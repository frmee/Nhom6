import requests
import json
import pandas as pd
import numpy as np
import datetime as dt
import time
from discord_webhook import DiscordWebhook, DiscordEmbed
import re

symbols=input('Nhập các loại coin muốn theo dõi (VD: BTCBUSD, ETHBUSD,...): ')
url = 'https://discord.com/api/webhooks/975414041159819357/qkaDwdRevDECgNZPExUC9YoFoLSX0u60WuAWQvXCblCGN4LO-57mtR5BtCpH3WBsGxlb'
frequency='1h'
reg=re.compile(r'\w+')
list_symbols=[i.upper() for i in reg.findall(symbols)]

#lấy thông tin từ web binance
def get_price(symbol,frequency): 
    root_url='https://api.binance.com/api/v1/klines'
    url=root_url+'?symbol='+ symbol+'&interval='+frequency
    data=json.loads(requests.get(url,timeout=15).text)
    current_time=dt.datetime.now()
    df=pd.DataFrame(data[-2:])
    df.columns=['open_time','open','high','low','current','volumn','close_time','qav','num_trades','taker_base_vol',
                'taker_quote_vol','ignore']
    close_time=[dt.datetime.fromtimestamp(x/1000.0) for x in df.close_time]
    df.index=[close_time[0],current_time]
    df['current1']=df['current'].map(lambda x: eval(x))
    return df

def send_discord(url,notification):
    message=notification
    webhook=DiscordWebhook(url=url,content=message)
    webhook.execute()

def notify(symbol,frequency):
    while True:
        df=get_price(symbol,frequency)
        print('Thời gian:',dt.datetime.now())
        notification = 'Giá hiện tại của '+symbol+' : '+df['current'][1]
        print(notification)
        print('\n')
        send_discord(url,notification)
        # chỉ thông báo mỗi 1 phút 1 lần
        time.sleep(60)

notify(symbols, frequency)
       
