import pandas as pd
pd.options.display.float_format = '{:.2f}'.format #小数点以下2桁まで表示
from pprint import pprint
import ccxt
import requests
import time
import sys
import traceback
from datetime import datetime

# 以下同じディレクトリの関数からimport
import d_functions
import d_functions2
from d_line_notify import LineNotify

##################################開始

# インスタンス化
bybit = ccxt.bybit(
            {
                "apiKey": "?????",
                "secret": "?????",
                "urls": {
                    "api": "https://api-testnet.bybit.com/" # testnet（デモ版）を使用する場合はこの記述が必要
                }
            }
        )

symbol = "BTC/USDT" 
amount = 0.0001

# Lineの設定
line_notify = LineNotify()
line_notify.send("Start trading")


while 1:
    entry_signal = calc_entry_signal()
    
    if entry_signal == True:
        long_entry(bybit)
        entry_price = get_ohlcv(limit=1)['close'][199] #参入時の価格を保持
        time.sleep(300)
        long_close(bybit) # 5分後にポジションは自動で解消することにする
