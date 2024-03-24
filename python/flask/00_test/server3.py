# -*- coding: utf-8 -*-
from flask import Flask

app = Flask(__name__)

# 1つ目のルーティングを作成
# パスに「'/'」を記述した場合、「http://127.0.0.1:8080/」(トップページ)にアクセスしたときの処理を関数に記述する
@app.route('/')
def index():
    # クライアントに以下の文字列(HTML)を返す
    return '<html><br><br><span>トップページです</span></html>'

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug = True)
    
    
