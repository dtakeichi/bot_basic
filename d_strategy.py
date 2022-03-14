"""
仮説
"""

def calc_entry_signal(df):
    rule1 = df[-3:]['volume'].mean() > df[-15:]['volume'].mean()
    rule2 = df['close'].diff(1)[199] > 0 and df['close'].diff(1)[198] < 0 #and df['close'].diff(1)[196] < 0
    mean = (df['high'].max() +df['low'].min())/2
    rule3 = df['close'][199] < mean

    return rule1 and rule2 and rule3 

def calc_close_signal(df, price, ask):
    rule1 = price + 100 < ask  #rule1 = price * 1.002 < ask
    rule2 = df['close'][199] < price - 100 # price * 0.99 # loss cut
    rule3 = df['close'].diff(1)[199] < 0 and df['close'].diff(1)[198] > 0

    return (rule1 and rule3) or rule2
