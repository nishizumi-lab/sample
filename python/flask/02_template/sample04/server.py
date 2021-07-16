# -*- coding: utf-8 -*-
from flask import Flask, render_template, url_for, request, redirect
 # 分割したモジュールをインポート
from index import index_app
from page1 import page1_app

app = Flask(__name__)

# 分割先のコントローラー(Blueprint)を登録
app.register_blueprint(index_app)
app.register_blueprint(page1_app)


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=8080)