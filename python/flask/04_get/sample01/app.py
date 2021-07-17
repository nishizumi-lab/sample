from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
import os

# 自身の名称を app という名前でインスタンス化する
app = Flask(__name__)

# index にアクセスされた場合の処理
@app.route('/')
def index():
    message = "いらっしゃい"

    # GETメソッドの場合
    if request.method == 'GET':
        # リクエストフォームから「名前」を取得
        page_num = request.args.get('page')
        # nameとtitleをindex.htmlに変数展開
        return render_template('index.html',
                               name=page_num, message="GETパラメータがありません")

    # POSTメソッドの場合
    else:
        return redirect(url_for('index'))


if __name__ == "__main__":
    app.debug = True  # デバッグモード有効化
    app.run(host="127.0.0.1", port=8080)
