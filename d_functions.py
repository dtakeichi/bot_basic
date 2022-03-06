import pandas as pd
import requests
import time
import sys
import traceback
from datetime import datetime
import talib

"""
get_ohlcv関数
calc_features関数
"""

#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------

def get_ohlcv(symbol="BTCUSDT", limit=1000, interval=1):
    """
    使用例
    df = fetch_ohlcv_v2(symbol="XTZUSDT", limit=600,interval=1)
    symbol = 通貨名, limit = 取得行数, interval = 取得間隔(分)
    """

    # 関数の中で関数を定義
    def fetch_ohlcv(symbol=symbol, l=200, interval=interval, k=1):
        base_url = "https://api-testnet.bybit.com/public/linear/kline"
        params = {
            "symbol": symbol,  
            "interval": interval,  
            "limit": l, # 取得件数(The number of data points to return)
            "from" : int(time.time() - interval*l*60*k) #今より昔のものをとる　#分・個数=秒
        }
    
        res = requests.get(base_url, params, timeout = 10).json()
        Time, Open, High, Low, Close, Volume = [],[],[],[],[],[]
        for i in res['result']:
            Time.append(datetime.fromtimestamp(i["open_time"]))
            Open.append(i["open"])
            High.append(i["high"])
            Low.append(i["low"])
            Close.append(i["close"])
            Volume.append(i["volume"]) # volumefrom (BTCの単位) vlumeto(USDTの単位)
    
        candles = pd.DataFrame({
            "time": Time,  # 時刻
            "open": Open,  # 始値
            "high": High,  # 高音
            "low": Low,    # 安値
            "close": Close, # 終値
            "volume": Volume #出来高
        })

        return(candles)
    

    df = fetch_ohlcv(interval=interval, l=200, k=1)
    iter = int(limit/200) - 1
    for i in range(iter):
        df2 = fetch_ohlcv(interval=interval, l=200, k=i+1)
        df = pd.concat([df2,df],ignore_index=True)
        df = df.set_index("time")
    
    return(df)

#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------

import talib

def calc_features(df):
    """
    使用例  df = calc_features(df)
    get_candlesで撮ってきたdfを渡すことを想定
    取得したOHLCV形式のdfをかませると列を追加してくれます
    
    df.to_pickle('df_features.pkl') 保存する場合は'df_features.pkl'のように名前をつけて保存
    df = pd.read_pickle('df_features.pkl') で高速に呼び出せる
    """
    
    open = df['open']
    high = df['high']
    low = df['low']
    close = df['close']
    volume = df['volume']
    
    orig_columns = df.columns # もともとのdfの列名を保持

    hilo = (df['high'] + df['low']) / 2 # 高値と低値の平均を算出
    
    # 以下 68個の特徴量を片っ端から生み出す
    df['BBANDS_upperband'], df['BBANDS_middleband'], df['BBANDS_lowerband'] = talib.BBANDS(close, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)
    df['BBANDS_upperband'] -= hilo # hiloを引いてるのは基準化のため
    df['BBANDS_middleband'] -= hilo
    df['BBANDS_lowerband'] -= hilo
    df['DEMA'] = talib.DEMA(close, timeperiod=30) - hilo
    df['EMA'] = talib.EMA(close, timeperiod=30) - hilo
    df['HT_TRENDLINE'] = talib.HT_TRENDLINE(close) - hilo
    df['KAMA'] = talib.KAMA(close, timeperiod=30) - hilo
    df['MA'] = talib.MA(close, timeperiod=30, matype=0) - hilo
    df['MIDPOINT'] = talib.MIDPOINT(close, timeperiod=14) - hilo
    df['SMA'] = talib.SMA(close, timeperiod=30) - hilo
    df['T3'] = talib.T3(close, timeperiod=5, vfactor=0) - hilo
    df['TEMA'] = talib.TEMA(close, timeperiod=30) - hilo
    df['TRIMA'] = talib.TRIMA(close, timeperiod=30) - hilo
    df['WMA'] = talib.WMA(close, timeperiod=30) - hilo

    df['ADX'] = talib.ADX(high, low, close, timeperiod=14)
    df['ADXR'] = talib.ADXR(high, low, close, timeperiod=14)
    df['APO'] = talib.APO(close, fastperiod=12, slowperiod=26, matype=0)
    df['AROON_aroondown'], df['AROON_aroonup'] = talib.AROON(high, low, timeperiod=14)
    df['AROONOSC'] = talib.AROONOSC(high, low, timeperiod=14)
    df['BOP'] = talib.BOP(open, high, low, close)
    df['CCI'] = talib.CCI(high, low, close, timeperiod=14)
    df['DX'] = talib.DX(high, low, close, timeperiod=14)
    df['MACD_macd'], df['MACD_macdsignal'], df['MACD_macdhist'] = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    # skip MACDEXT MACDFIX たぶん同じなので
    df['MFI'] = talib.MFI(high, low, close, volume, timeperiod=14)
    df['MINUS_DI'] = talib.MINUS_DI(high, low, close, timeperiod=14)
    df['MINUS_DM'] = talib.MINUS_DM(high, low, timeperiod=14)
    df['MOM'] = talib.MOM(close, timeperiod=10)
    df['PLUS_DI'] = talib.PLUS_DI(high, low, close, timeperiod=14)
    df['PLUS_DM'] = talib.PLUS_DM(high, low, timeperiod=14)
    df['RSI'] = talib.RSI(close, timeperiod=14)
    df['STOCH_slowk'], df['STOCH_slowd'] = talib.STOCH(high, low, close, fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
    df['STOCHF_fastk'], df['STOCHF_fastd'] = talib.STOCHF(high, low, close, fastk_period=5, fastd_period=3, fastd_matype=0)
    df['STOCHRSI_fastk'], df['STOCHRSI_fastd'] = talib.STOCHRSI(close, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)
    df['TRIX'] = talib.TRIX(close, timeperiod=30)
    df['ULTOSC'] = talib.ULTOSC(high, low, close, timeperiod1=7, timeperiod2=14, timeperiod3=28)
    df['WILLR'] = talib.WILLR(high, low, close, timeperiod=14)

    df['AD'] = talib.AD(high, low, close, volume)
    df['ADOSC'] = talib.ADOSC(high, low, close, volume, fastperiod=3, slowperiod=10)
    df['OBV'] = talib.OBV(close, volume)

    df['ATR'] = talib.ATR(high, low, close, timeperiod=14)
    df['NATR'] = talib.NATR(high, low, close, timeperiod=14)
    df['TRANGE'] = talib.TRANGE(high, low, close)

    df['HT_DCPERIOD'] = talib.HT_DCPERIOD(close)
    df['HT_DCPHASE'] = talib.HT_DCPHASE(close)
    df['HT_PHASOR_inphase'], df['HT_PHASOR_quadrature'] = talib.HT_PHASOR(close)
    df['HT_SINE_sine'], df['HT_SINE_leadsine'] = talib.HT_SINE(close)
    df['HT_TRENDMODE'] = talib.HT_TRENDMODE(close)

    df['BETA'] = talib.BETA(high, low, timeperiod=5)
    df['CORREL'] = talib.CORREL(high, low, timeperiod=30)
    df['LINEARREG'] = talib.LINEARREG(close, timeperiod=14) - close
    df['LINEARREG_ANGLE'] = talib.LINEARREG_ANGLE(close, timeperiod=14)
    df['LINEARREG_INTERCEPT'] = talib.LINEARREG_INTERCEPT(close, timeperiod=14) - close
    df['LINEARREG_SLOPE'] = talib.LINEARREG_SLOPE(close, timeperiod=14)
    df['STDDEV'] = talib.STDDEV(close, timeperiod=5, nbdev=1)

    return df
