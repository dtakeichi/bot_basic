# bot_basic

<dl>
<dt>functions.py</dt> 
(ohlcv取得の関数, 特徴量計算の関数)
def get_ohlcv

<dt>functoins2.py</dt>
(ポジション取得, 残高, longポジションをとる関数, long解消の関数, 成り行き注文を出す関数)

<dt>line_notify.py</dt>

<dt>strategy.py</dt>
strategy(df):
  y = signal

<dt>bot.py</dt>
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
</dl>

mdファイルの書き方はこちら
<https://qiita.com/oreo/items/82183bfbaac69971917f>
