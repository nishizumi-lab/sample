# -*- coding: utf-8 -*-
from flask import Flask

app = Flask(__name__)

# ルーティング(クライアントからの要求内容に応じて、処理を切り換える)を記述
# index(トップ)にアクセスしたときの処理
@app.route('/')
def index():
    # クライアントに以下の文字列(HTML)を返す
    return '<html><br><br><span style="color:#ff0000;">■■■■■■■■■■Hello World!■■■■■■■■■■■</span></html>'


if __name__ == '__main__':
     # デバッグモード有効化
    app.debug = True
    # アプリの起動設定(IPアドレスとポート番号)
    app.run(host='127.0.0.1', port=8080)
