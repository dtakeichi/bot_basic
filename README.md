# bot_basic


#functions.py 
(ohlcv取得の関数, 特徴量計算の関数)
def get_ohlcv

#functoins2.py
(ポジション取得, 残高, longポジションをとる関数, long解消の関数, 成り行き注文を出す関数)

#line_notify.py

#strategy.py
strategy(df):
  y = signal

#bot.py
(一連の流れ)
import functions.py

bybiy = ()

(except
try) 
while 
  df = get_ohlcv()
  dfをいじる
  参入のsignalを計算  siganl = starategy(df)
  解消のsignal
  functoins2の関数を呼び出す (参入、解消) ポジションがLONG NONEで分ける
  
