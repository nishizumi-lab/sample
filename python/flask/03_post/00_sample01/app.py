from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
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

# /post にアクセスされた場合の処理
@app.route('/post', methods=['GET', 'POST'])
def post():
    title = "いらっしゃい"
    if request.method == 'POST':
        # リクエストフォームから「名前」を取得
        name = request.form['name']
        # nameとtitleをindex.htmlに変数展開
        return render_template('index.html',
                               name=name, title=title)
    else:
        # エラーなどでリダイレクトしたい場合
        return redirect(url_for('index'))


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.debug = True  # デバッグモード有効化
    app.run(host="0.0.0.0", port=port)
