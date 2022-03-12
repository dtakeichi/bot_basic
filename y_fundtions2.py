import ccxt
#ポジション取得・資産残高取得・注文(マーケット・指値)・注文状況取得・注文キャンセル

#インスタンス化
bybit = ccxt.bybit({"apiKey":"?????????", "secret":"?????????",
                   "urls": {"api": "https://api-testnet.bybit.com/" # testnet（デモ版）を使用する場合はこの記述が必要
                    }})


def get_position():
		# ポジションを long short straddling noneの4つから返します
    Long = False
    Short = False
    res = bybit.privateLinearGetPositionList({"symbol": "BTCUSDT"})['result'] #ポジションの情報を見れます。resの中身もみてみてください
    for i in res:
        if i["side"] == "Buy" and float(i["size"]) > 0: # Buy(long)の情報のうちサイズが0より台ならフラグを立てる ポジションなしならsize=0です
            Long = True
        elif i["side"] == "Sell" and float(i["size"]) > 0:
            Short = True
 
    if Long and Short: # フラグから考えられるポジションを返します。
        return "straddling" # 両建て? 英語があってるかわかりません
    elif Long:
        return "long" # 買い　ロング
    elif Short:
        return "short" # 売り　ショート
		else:
				return "none" # ノーポジ

	# 使用例
	position = get_position()
	print(position)

# 資産残高の取得
bybit.fetch_balance({"coin": "USDT"})


# 注文を出す (マーケット注文、新規参入の場合)
order = bybit.create_order(
            symbol = "BTC/USDT",     # 通貨ペア
            type = "market", # 成行注文か指値注文か（market: 成行注文、limit: 指値注文）
            side = "buy",       # 買いか売りか（buy: 買い、sell: 売り）
            amount = 0.001, # 注文量（BTC)
            params = {
             # 取引所に対応したパラメータ
            "qty": 0.001
            }
        )


# 注文を出す (マーケット注文、ポジション解消(反対取引をする)の場合)
order = bybit.create_order(
            symbol = "BTC/USDT",     # 通貨ペア
            type = "market", # 成行注文か指値注文か（market: 成行注文、limit: 指値注文）
            side = "sell",       # 買いか売りか（buy: 買い、sell: 売り）
            amount = 0.001, # 注文量（BTC)
            params = {
             # 取引所に対応したパラメータ
            "qty": 0.001,
            "reduce_only":True # 反対取引をしてポジションを解消しようとする (ドテン)
            }
        )

#指値注文する
order = bybit.create_order(
            symbol = "BTC/USDT",     # 通貨ペア
            type = "limit", # 成行注文か指値注文か（market: 成行注文、limit: 指値注文）
            price = 40000,
            side = "buy",       # 買いか売りか（buy: 買い、sell: 売り）
            amount = 0.001, # 注文量（BTC)
            params = {
             # 取引所に対応したパラメータ 
            "qty": 0.001})


#注文状況を取得(最新のものから順番に辞書に入る)
orders = bybit.fetch_open_orders(
	symbol = "BTC/USDT")

for o in orders: #上から最新のものから表示
	print( o["id"] + " : 注文状況 " + o["status"] )

pprint( orders )



	#注文idを取得
	for o in orders:
		pprint( o["id"] )

#注文キャンセル(idを手動で指定) 特定のidをキャンセル
bybit.cancel_order(
	symbol = "BTC/USDT",
	id = "~~~~~~~~~~~~~~~~~")

#注文キャンセル(最新のものをキャンセル)
bybit.cancel_order(
	symbol = "BTC/USDT",
	id = orders[0]["id"]) 
#最新のものをキャンセル後、再度に注文状況を取得しないといけない(orders再定義)

#全ての注文をキャンセル
for o in orders:
	bybit.cancel_order(
		symbol = "BTC/USDT",
		id = o["id"])
