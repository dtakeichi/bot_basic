import ccxt # pip install ccxt==1.45.18  バージョン注意
from pprint import pprint

"""
long_entry関数
long_close関数
get_position関数
"""

def long_entry(instance, qty=0.001):
    """
    long, market注文で新規参入
    """
    if get_position(instance) == "long":
        return 0
        
    order = instance.create_order(
            symbol = "BTC/USDT",     # 通貨ペア
            type = "market",         # 成行注文か指値注文か（market: 成行注文、limit: 指値注文）
            side = "buy",            # 買いか売りか（buy: 買い、sell: 売り）
            amount = qty,            # 注文量（BTC)
            params = {
             # 取引所に対応したパラメータ
            "qty": qty
            }
        )
    return order

def long_close(instance, qty=0.001):
    """
    long position をmarket注文で解消
    """
    if get_position(instance) != "long":
        return 0
    
    order = instance.create_order(
            symbol = "BTC/USDT",     # 通貨ペア
            type = "market", # 成行注文か指値注文か（market: 成行注文、limit: 指値注文）
            side = "sell",       # 買いか売りか（buy: 買い、sell: 売り）
            amount = qty, # 注文量（BTC)
            params = {
             # 取引所に対応したパラメータ
            "qty": qty,
            "reduce_only":True # 反対取引をしてポジションを解消しようとする (ドテン)
            }
        )
    return order

def limit_long_close(instance, price ,qty=0.001):
    """
    long position をlimit注文で解消
    """
    if get_position(instance) != "long":
        return 0
    
    order = instance.create_order(
            symbol = "BTC/USDT",     # 通貨ペア
            type = "limit", # 成行注文か指値注文か（market: 成行注文、limit: 指値注文）
            side = "sell",       # 買いか売りか（buy: 買い、sell: 売り）
            price = price,
            amount = qty, # 注文量（BTC)
            params = {
             # 取引所に対応したパラメータ
            "qty": qty,
            "reduce_only":True # 反対取引をしてポジションを解消しようとする (ドテン)
            }
        )
    return order

def get_position(instance):
    """
    ポジションを long short straddling noneの4つから返します
    使用例  print(get_position(bybit))
    """
    Long = False
    Short = False
    res = instance.privateLinearGetPositionList({"symbol": "BTCUSDT"})['result'] #ポジションの情報を見れます。resの中身もみてみてください
    for i in res:
        if i["side"] == "Buy" and float(i["size"]) > 0: # Buy(long)の情報のうちサイズが0より台ならフラグを立てる ポジションなしならsize=0です
            Long = True
        elif i["side"] == "Sell" and float(i["size"]) > 0:
            Short = True
            
    if Long and Short: # フラグから考えられるポジションを返します。
        return "straddling" # 両建て
    elif Long:
        return "long" 
    elif Short:
        return "short" 
    else:
        return "none"
