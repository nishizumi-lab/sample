from flask import Flask, render_template, url_for, request, redirect, Blueprint
import os

# Blueprintオブジェクトを生成
app = Blueprint('input_data', __name__)

# index にアクセスされた場合の処理
@app.route('/input_data', methods=['GET', 'POST'])
def input_data():
    title = "ようこそ"
    message = "君の名前を教えてくれ"
    # messageとtitleをindex.htmlに変数展開
    return render_template('input_data.html',
                           message=message, title=title)

