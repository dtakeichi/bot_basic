"""
仮説
# 動きの前は取引量が増加する
(1) 過去15分の平均取引量 < 最新1分の取引量  取引が加熱している
(2) 過去2分連続して下がっているていま上がり出したときに参入、谷を特定する感じ
"""

def calc_entry_signal():
    df = get_ohlcv(limit=1)
    volume_mean = df[-15:]['volume'].mean() # 過去15分の取引量の平均
    volume_std = df[-15:]['volume'].std() # 過去15分の取引量の標準偏差
    rule1 = df['volume'][198] > volume_mean + 2*volume_std
    rule2 = df['close'].diff(1)[198] > 0 and df['close'].diff(1)[197] < 0 and df['close'].diff(1)[196] < 0
    
    return rule1 # and rule2  条件(2)をなかなか満たさないので and以降コメントアウト
