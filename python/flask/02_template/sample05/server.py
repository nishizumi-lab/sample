# -*- coding: utf-8 -*-
from flask import Flask, render_template, url_for, request, redirect
 # 分割したモジュールをインポート
from views import index
#from views import page1

app = Flask(__name__)

# 分割先のコントローラー(Blueprint)を登録
app.register_blueprint(index.index_app)
#app.register_blueprint(index.page1_app)


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=8080)