# -*- coding: utf-8 -*-
from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)

# ルートページ
@app.route('/page1')
def page1():
    name = "ページ1"
    message = "ページ1のメッセージ"

    # 変数展開(messageとnameの値がHTMLに渡される)
    return render_template('page1.html',
                           message=message, name=name)

# ルートページ
@app.route('/')
def index():
    name = "トップページ"
    message = "トップページのメッセージ"

    # 変数展開(messageとnameの値がHTMLに渡される)
    return render_template('index.html',
                           message=message, name=name)


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=8080)