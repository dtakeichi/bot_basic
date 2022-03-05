# API  https://min-api.cryptocompare.com/data/v2/histominute?fsym=BTC&tsym=USD&limit=5

import pandas as pd
import requests
import time
import sys
import traceback
from datetime import datetime

# API仕様書  https://min-api.cryptocompare.com/data/v2/histominute?fsym=BTC&tsym=USD&limit=5

def get_candles(timeframe="minute", limit=1000):
    # timeframe（時間軸）には"minute"（1分足）"hour" (1時間足) "day" (日足)のいずれかが入る
    # limitは取得する期間を指定
    base_url = f"https://min-api.cryptocompare.com/data/v2/histo{timeframe}" 

    params = {
        "fsym": "light",  # 通貨名(The cryptocurrency symbol of interest)
        "tsym": "USDT",  # 通貨名(The currency symbol to convert into)
        "limit": limit, # 取得件数(The number of data points to return)
    }

    res = requests.get(base_url, params, timeout = 10).json()

    time, open, high, low, close, volume = [], [], [], [], [], []

    for i in res["Data"]["Data"]:
        time.append(datetime.fromtimestamp(i["time"])) # datetime.fromtimestamp(1638864000) = datetime.datetime(2021, 12, 7, 17, 0)のこと
        open.append(i["open"])
        high.append(i["high"])
        low.append(i["low"])
        close.append(i["close"])
        volume.append(i["volumefrom"]) # volumefrom (BTCの単位) vlumeto(USDTの単位)
    
    candles = pd.DataFrame({
            "Time": time,  # 時刻
            "Open": open,  # 始値
            "High": high,  # 高音
            "Low": low,    # 安値
            "Close": close, # 終値
            "Volume": volume #出来高
        }
    )

    return candles
