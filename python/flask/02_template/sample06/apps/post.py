from flask import Flask, render_template, url_for, request, redirect, Blueprint
import os

# Blueprintオブジェクトを生成
app = Blueprint('post', __name__)

# /post にアクセスされた場合の処理
@app.route('/post', methods=['GET', 'POST'])
def post():
    title = "いらっしゃい"
    if request.method == 'POST':
        # リクエストフォームから「名前」を取得
        name = request.form['name']
        # nameとtitleをindex.htmlに変数展開
        return render_template('input_data.html',
                               name=name, title=title)
    else:
        # エラーなどでリダイレクトしたい場合
        return redirect(url_for('index'))
