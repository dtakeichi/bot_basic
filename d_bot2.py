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

from functions import get_ohlcv_v2
from functions import get_ohlcv
from functions2 import long_entry
from functions2 import long_close
from functions2 import limit_long_close
from functions2 import get_position
from functions2 import cancel_all_orders
from strategy import calc_entry_signal
from strategy import calc_close_signal
from line_notify import LineNotify


"""
## 準備 ##
"""
bybit = ccxt.bybit(
            {
                "apiKey": "?",
                "secret": "?",
                "urls": {
                    "api": "https://api-testnet.bybit.com/" # testnet（デモ版）を使用する場合はこの記述が必要
                }
            }
        )
symbol = "BTC/USDT" 
amount = 0.01

LINE_NOTIFY_TOKEN = "?"
line_notify = LineNotify(token = LINE_NOTIFY_TOKEN)


"""
## 実行部分 ##
# taker fee = 0.00075
"""

line_notify.send('bot runnning...')
while 1:
  try:
    entry_signal = False
    df = get_ohlcv(limit=200)
    entry_signal = calc_entry_signal(df)
    
    # 参入
    if entry_signal == True:
        entry_order_log = long_entry(bybit, qty=0.01) #参入し注文状況を受け取る
        entry_price = get_ohlcv(limit=1)['close'][0] #参入時の価格を保持
        line_notify.send(f'entry at {entry_price}')
        time.sleep(10)

        # longしてるとき
        while get_position(bybit) == 'long':
            time.sleep(10)
            df2 = get_ohlcv(limit=200)
            best_ask = bybit.fetch_order_book("BTC/USDT")['asks'][0][0] 
            close_signal = calc_close_signal(df=df2, price = entry_price, ask = best_ask)
            if close_signal == True:
                colse_order_log = limit_long_close(bybit, price = best_ask-0.5, qty=0.01) 
                line_notify.send(f'close order at {best_ask}')
                time.sleep(120)
                if get_position(bybit) == 'none':
                    break
                # キャンセル
                else:
                    cancel_all_orders(bybit)
                    line_notify.send(f'cancel orders')
                    # break
            
    time.sleep(10)
  except:
    line_notify.send(traceback.format_exc())
    sys.exit() # 何か例外が生じた際はLINE通知を飛ばしてBotを停止する
