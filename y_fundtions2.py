import ccxt

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
