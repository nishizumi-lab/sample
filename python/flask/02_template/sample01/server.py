# -*- coding: utf-8 -*-
from flask import Flask, render_template, url_for, request, redirect
import time, datetime

app = Flask(__name__)

@app.route('/')
def index():
    name1 = "ユーザー1"
    message1 = "メッセージ"

    # 現在の時刻を取得
    today = datetime.datetime.fromtimestamp(time.time())
    message1 = today.strftime('%Y/%m/%d %H:%M:%S')

    # index.htmlの変数展開(message1とname1の値がHTMLのmessage, nameに渡される)
    return render_template('index.html',
                           message=message1, name=name1)


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=8080)