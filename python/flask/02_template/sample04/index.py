from flask import Flask, render_template, url_for, request, redirect
# Blueprintをimportする
from flask import Blueprint

# 関数名(index)でBlueprintオブジェクトを生成
index_app = Blueprint('index', __name__)

# ルートページ
@index_app.route('/')
def index():
    name = "トップページ"
    message = "トップページのメッセージ"

    # 変数展開(messageとnameの値がHTMLに渡される)
    return render_template('index.html',
                           message=message, name=name)
