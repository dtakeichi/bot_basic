import pandas as pd
import requests
import time
import sys
import traceback
from datetime import datetime
import talib
import ccxt # pip install ccxt==1.45.18  バージョン注意
from pprint import pprint
import requests

from functions import get_ohlcv
from functions2 import long_entry
from functions2 import long_close
from strategy import calc_entry_signal
from line_notify import LineNotify


"""
## 準備 ##
"""
bybit = ccxt.bybit(
            {
                "apiKey": "???",
                "secret": "??????",
                "urls": {
                    "api": "https://api-testnet.bybit.com/" # testnet（デモ版）を使用する場合はこの記述が必要
                }
            }
        )
symbol = "BTC/USDT" 
amount = 0.01

LINE_NOTIFY_TOKEN = "???"
line_notify = LineNotify(token = LINE_NOTIFY_TOKEN)


"""
## 実行部分 ##
# taker fee = 0.00075
"""

while 1:
    entry_signal = False
    df = get_ohlcv(limit=1)
    entry_signal = calc_entry_signal(df)
    
    if entry_signal == True:
        entry_order_log = long_entry(bybit) #参入し注文状況を受け取る
        entry_price = get_ohlcv(limit=1)['close'][199] #参入時の価格を保持
        line_notify.send(f'entry at {entry_price}')
        time.sleep(60)
        while 1:
            time.sleep(10)
            best_ask = bybit.fetch_order_book("BTC/USDT")['asks'][0][0]
            # 改良
            # close_signal = calc_close_signal()
            # if close_signal == Ture:
            if entry_price * 1.0025 < best_ask: # 1 + 2*taker = 1.0015 
                long_close(bybit) 
                line_notify.send(f'close at {best_ask}')
                break
            
    time.sleep(60)
