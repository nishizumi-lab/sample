# -*- coding: utf-8 -*-
from flask import Flask

# Webアプリを作成
app = Flask(__name__)

# 1つ目のルーティングを作成
# パスに「'/'」を記述した場合、「http://127.0.0.1:8080/」(トップページ)にアクセスしたときの処理を関数に記述する
@app.route('/')
def index():
    # クライアントに以下の文字列(HTML)を返す
    return '<html><br><br>トップページです</html>'

# 2つ目のルーティングを作成()
# パスに「'/login'」を記述した場合、「http://127.0.0.1:8080/login」にアクセスしたときの処理を関数に記述する
@app.route('/login')
def login():
    # クライアントに以下の文字列(HTML)を返す
    return '<html><br><br>ログインページページです</html>'

if __name__ == '__main__':
    # Flaskのインスタンスを実行
    # hostはホスト名。デフォルトはlocalhost(127.0.0.1)=自分のPC。
    # portはポート番号。デフォルトは5000。
    # debugはデバッグモードの有効。デフォルトはFalse。
    app.run(host='127.0.0.1', port=8080, debug = True)
    
    
