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

