"""
仮説
# 動きの前は取引量が増加する
(1) 過去15分の平均取引量 < 最新3分の取引量 
(2) 過去2分連続して下がっていていま上がり出したときに参入、谷を特定する感じ lagがあったので1つ前のデータで判定
"""

def calc_entry_signal(df):
    volume_mean = df[-15:]['volume'].mean() # 過去15分の取引量の平均
    volume_std = df[-15:]['volume'].std() # 過去15分の取引量の標準偏差
    rule1 = df[-3:]['volume'].mean() > volume_mean 
    rule2 = df['close'].diff(1)[197] > 0 and df['close'].diff(1)[196] < 0 #and df['close'].diff(1)[196] < 0
    
    return rule1 # and rule2  条件(2)をなかなか満たさないので and以降コメントアウト

def calc_close_signal(df, entry_price, best_ask):
    rule1 = entry_price * 1.005 < best_ask
    rule2 = df['close'][199] < entry_price * 0.9 # loss cut
    return rule1 or rule2
