
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
                "secret": "???????",
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
"""

while 1:
    df = get_ohlcv(limit=1)
    entry_signal = calc_entry_signal(df)
    
    if entry_signal == True:
        long_entry(bybit)
        entry_price = get_ohlcv(limit=1)['close'][199] #参入時の価格を保持
        line_notify.send(f'entry at {entry_price}')
        time.sleep(100)
        while 1:
            now_price = get_ohlcv(limit=1)['low'][199]
            entry_price * 1.01 < now_price
            long_close(bybit) # 5分後にポジションは自動で解消することにする
            line_notify.send(f'close at {now_price}')
            break
            
    time.sleep(60)
