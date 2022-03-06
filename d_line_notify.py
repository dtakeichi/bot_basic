# LINE通知の設定を行うためのファイル
import requests

"""
使い方
(1) インスタンス化 line_notify = LineNotify()
(2) 贈りたいメッセージをHelloとすると line_notify.send("Hello")
"""

class LineNotify:
    def __init__(self, token):
        self.line_notify_token = token
        self.line_notify_api = "https://notify-api.line.me/api/notify"
        self.headers = {
          "Authorization": f"Bearer {self.line_notify_token}"
        }

    def send(self, msg):
        msg = { "message": f" {msg}" }
        requests.post(self.line_notify_api, headers = self.headers, data = msg)
