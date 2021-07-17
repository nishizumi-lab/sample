from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
import os

# 自身の名称を app という名前でインスタンス化する
app = Flask(__name__)

# index にアクセスされた場合の処理
@app.route('/')
def index():
    title = "ようこそ"
    message = "君の名前を教えてくれ"
    # messageとtitleをindex.htmlに変数展開
    return render_template('index.html',
                           message=message, title=title)

# /post にアクセスされ、GETもしくはPOSTメソッドでデータが送信された場合の処理
@app.route('/post', methods=['GET', 'POST'])
def post():
    title = "いらっしゃい"

    # GETメソッドの場合
    if request.method == 'GET':
        # トップページにリダイレクト
        return redirect(url_for('index'))

    # POSTメソッドの場合
    else:
        # リクエストフォームから「名前」を取得
        name = request.form['name']
        # nameとtitleをindex.htmlに変数展開
        return render_template('index.html',
                               name=name, title="POSTメソッドが使用されました")


if __name__ == "__main__":
    app.debug = True  # デバッグモード有効化
    app.run(host="127.0.0.1", port=8080)
